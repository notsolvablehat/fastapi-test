import os
import json
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pymongo import MongoClient
from google import genai

# Load environment variables from .env file
load_dotenv()

# Set up structured logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
# Load prompts from files
try:
    with open("step_prompt.txt", "r") as f:
        steps_prompt = f.read()
except FileNotFoundError as e:
    logger.error(f"Prompt file not found: {e}. 'steps_prompt' will be empty.")
    steps_prompt = ""

try:
    with open("file_structure_prompt.txt", "r") as f:
        file_structure_prompt = f.read()
except FileNotFoundError as e:
    logger.error(f"Prompt file not found: {e}. 'file_structure_prompt' will be empty.")
    file_structure_prompt = ""

# This dictionary will hold our shared resources for DB and AI clients.
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.
    """
    logger.info("Application starting up...")
    mongo_client = MongoClient(MONGODB_URI)
    db = mongo_client["ui_files"]
    genai_client = genai.Client(api_key=GEMINI_API_KEY)

    app_state["db"] = db
    app_state["genai_client"] = genai_client
    logger.info("Database connection and AI client initialized.")

    yield

    # Clean up resources on shutdown
    logger.info("Application shutting down...")
    mongo_client.close()
    logger.info("Database connection closed.")

class FilesResponse(BaseModel):
    html: List[str]
    js: List[str]

class GeneratedCodeFile(BaseModel):
    name: str
    content: str
    description: str = Field(..., description="A brief, human-readable description of what this AI-generated code file does.")

class PromptRequest(BaseModel):
    project_id: str
    file_id: str
    prompt: str


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def _create_file_template(request: PromptRequest, db, genai_client) -> dict:
    """
    Generates and saves the file structure template.
    Returns the file_structure dictionary on success.
    """
    logger.info(f"Attempting to generate file template for project: {request.project_id}")

    response = genai_client.models.generate_content(
        model="gemini-2.5-pro",
        config=genai.types.GenerateContentConfig(
            system_instruction=file_structure_prompt,
            response_schema=FilesResponse,
            response_mime_type="application/json",
            thinking_config = genai.types.ThinkingConfig(
                thinking_budget=10000,
            ),
        ),
        contents=[request.prompt],
    )

    parsed_template = FilesResponse.model_validate_json(response.candidates[0].content.parts[0].text)

    project_files_coll = db["project_files"]
    project_file_template = {
        "project_id": request.project_id,
        "file_id": request.file_id,
        "files": parsed_template.model_dump()
    }
    project_files_coll.insert_one(project_file_template)

    logger.info("File structure template created successfully.")
    return parsed_template.model_dump()


async def _generate_file_content_stream(request: PromptRequest, file_structure: dict, db, genai_client):
    """
    An async generator that creates file content in batches and yields progress.
    """
    generated_files_coll = db["generated_files"]
    chat = genai_client.chats.create(model="gemini-2.5-pro")

    initial_prompt = f"""
    First, carefully review this entire file architecture...
    # RULES
    {steps_prompt}
    # File architecture:
    {json.dumps(file_structure, indent=2)}
    # Screen specifications:
    {request.prompt}
    Acknowledge that you have understood the architecture.
    """
    chat.send_message(initial_prompt)
    logger.info("Gemini acknowledged and is ready to create the files.")

    process_order, batch_size = ["js", "html"], 8
    all_batches = [
        {"category": category, "files": file_structure[category][i:i + batch_size]}
        for category in process_order if category in file_structure
        for i in range(0, len(file_structure[category]), batch_size)
    ]

    total_batches = len(all_batches)
    for i, batch_info in enumerate(all_batches):
        category, files_to_generate = batch_info["category"], batch_info["files"]
        generation_prompt = f"Generate the code for all files in this batch: {json.dumps(files_to_generate)}"

        try:
            progress_message = f"Generating files... (Batch {i+1}/{total_batches})"
            yield json.dumps({"status": "progress", "message": progress_message, "files": files_to_generate}) + "\n"
            logger.info(f"{progress_message} for project {request.project_id}")

            response = chat.send_message(
                generation_prompt,
                config={"response_mime_type": "application/json", "response_schema": list[GeneratedCodeFile]}
            )
            generated_batch_data: list[GeneratedCodeFile] = response.parsed

            batch_documents = [
                {
                    "project_id": request.project_id, "file_id": request.file_id,
                    "path": f.name, "file_type": category, "content": f.content,
                    "created_at": datetime.now(timezone.utc), "description": f.description
                } for f in generated_batch_data
            ]

            if batch_documents:
                generated_files_coll.insert_many(batch_documents)
                files_info = [{"path": doc["path"], "file_type": doc["file_type"]} for doc in batch_documents]
                yield json.dumps({
                    "status": "progress", "message": f"Translating UX context into UI... (Batch {i+1}/{total_batches})", "data": files_info
                }) + "\n"
            # await asyncio.sleep(30)
        except Exception as e:
            logger.error(f"FAILED during batch generation for {files_to_generate}: {e}")
            yield json.dumps({"status": "error", "message": f"Failed during batch generation: {e}"}) + "\n"
            continue


async def _generate_and_stream_files(request: PromptRequest):
    """ The main async generator orchestrating the file creation process. """
    db = app_state["db"]
    genai_client = app_state["genai_client"]
    gen_files_coll = db["generated_files"]

    try:
        yield json.dumps({"status": "starting", "message": "Generating file structure..."}) + "\n"
        file_structure = await _create_file_template(request, db, genai_client)
        yield json.dumps({"status": "progress", "message": "Gathering UX context..."}) + "\n"
    except Exception as e:
        logger.error(f"Failed to generate template for project {request.project_id}: {e}", exc_info=True)
        yield json.dumps({"status": "error", "message": f"Failed to generate file structure: {str(e)}"}) + "\n"
        return

    async for update in _generate_file_content_stream(request, file_structure, db, genai_client):
        yield update

    all_files = list(gen_files_coll.find(
        {"project_id": request.project_id, "file_id": request.file_id},
        {"_id": 0, "created_at": 0}
    ))
    logger.info(f"Project generation complete for project: {request.project_id}")
    yield json.dumps({
        "status": "complete", "message": "Project generation completed.", "data": all_files
    }) + "\n"

@app.post("/get-or-generate-files")
async def get_or_generate_files(request: PromptRequest):
    """
    Checks if project files exist and returns them, otherwise starts the
    generation process and streams progress updates.
    """
    db = app_state["db"]
    gen_files_coll = db["generated_files"]

    existing_files = list(gen_files_coll.find(
        {"project_id": request.project_id, "file_id": request.file_id},
        {"_id": 0}
    ))

    if existing_files:
        logger.info(f"Files found in cache for project {request.project_id}. Returning them.")
        return JSONResponse(
            status_code=200,
            content={"status": "complete", "message": "Files already exist in DB.", "data": existing_files}
        )
    else:
        logger.info(f"Files not found for project {request.project_id}. Starting generation stream.")
        return StreamingResponse(_generate_and_stream_files(request), media_type="application/x-ndjson")

@app.get("/get-project-files")
def get_project_files(project_id: str = Query(...), file_id: str = Query(...)):
    """ Gets all files for a given project_id and file_id. """
    db = app_state["db"]
    gen_files_coll = db["generated_files"]
    try:
        docs = list(gen_files_coll.find({"project_id": project_id, "file_id": file_id}, {"_id": 0, "created_at": 0}))
        if docs:
            return JSONResponse(status_code=200, content={"message": "Fetched files successfully", "data": docs})
        else:
            return JSONResponse(status_code=200, content={"message": "No files found for this project", "data": []})
    except Exception as e:
        logger.error(f"Error fetching files for project {project_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error while fetching files.")

@app.get("/")
def health_check():
    """ A simple health check endpoint. """
    return JSONResponse(status_code=200, content={"message": "Server Running"})
