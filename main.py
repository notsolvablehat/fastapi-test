from google import genai
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import asyncio
from pymongo import MongoClient
from datetime import datetime, timezone
from fastapi.middleware.cors import CORSMiddleware

# ---------------- Pydantic models ----------------

class FilesResponse(BaseModel):
    html: List[str]
    js: List[str]
    css: List[str]

class GeneratedCodeFile(BaseModel):
    name: str
    content: str
    description: str = Field(..., description="A brief, human-readable description of what this AI-generated code file does. This description should be easy for anyone to understand.")

class PromptRequest(BaseModel):
    project_id: str
    file_id: str
    prompt: str

# ---------------- Load env + app ----------------
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Load prompts ----------------
try:
    with open("step_prompt.txt", "r") as f:
        steps_prompt = f.read()
except FileNotFoundError as e:
    print(f"Error: Prompt file not found - {e}. Please ensure step_prompt.txt exists.")
    steps_prompt = ""

# ---------------- Helper Functions ----------------

async def _create_file_template(request: PromptRequest, db) -> dict:
    """
    Generates and saves the file structure template.
    Returns the file_structure dictionary on success.
    """
    print("INFO: Attempting to generate file template.")
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=steps_prompt,
            response_schema=FilesResponse,
            response_mime_type="application/json",
        ),
        contents=[request.prompt],
    )

    parsed_template = FilesResponse.model_validate_json(response.candidates[0].content.parts[0].text) # type: ignore

    project_files_coll = db["project_files"]
    project_file_template = {
        "project_id": request.project_id,
        "file_id": request.file_id,
        "files": parsed_template.model_dump()
    }
    project_files_coll.insert_one(project_file_template)

    print("INFO: File structure template created successfully.")
    return parsed_template.model_dump()


async def _generate_file_content_stream(request: PromptRequest, file_structure: dict, db):
    """
    An async generator that creates file content in batches and yields progress.
    """
    generated_files_coll = db["generated_files"]
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    chat = client.chats.create(model="gemini-2.5-flash")

    # Set context for the chat model
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
    print("INFO: Gemini acknowledged and is ready to create the files.");

    # Create and process batches
    process_order, batch_size = ["js", "html", "css"], 8
    all_batches_to_process = []

    for category in process_order:
        if category in file_structure and file_structure[category]:
            file_names = file_structure[category]
            for i in range(0, len(file_names), batch_size):
                batch = file_names[i:i + batch_size]
                all_batches_to_process.append({"category": category, "files": batch})

    total_batches = len(all_batches_to_process)
    for i, batch_info in enumerate(all_batches_to_process):
        category, files_to_generate = batch_info["category"], batch_info["files"]

        generation_prompt = f"Generate the code for all files in this batch... {json.dumps(files_to_generate)}"

        try:
            yield json.dumps({
                "status": "progress",
                "message": f"Generating files... {i+1}/{total_batches}",
                "files": files_to_generate
            }) + "\n"
            print(f"Generating files... {i+1}/{total_batches}",)
            response = chat.send_message(
                generation_prompt,
                config={"response_mime_type": "application/json", "response_schema": list[GeneratedCodeFile]}
            )
            generated_batch_data: list[GeneratedCodeFile] = response.parsed # type: ignore

            batch_documents = [
                {
                    "project_id": request.project_id, "file_id": request.file_id,
                    "path": f.name, "file_type": category, "content": f.content,
                    "created_at": datetime.now(timezone.utc),
                } for f in generated_batch_data
            ]

            if batch_documents:
                generated_files_coll.insert_many(batch_documents)
                files_info = [{"path": doc["path"], "file_type": doc["file_type"]} for doc in batch_documents]
                yield json.dumps({
                    "status": "progress",
                    "message": f"Translating UX context into UI...{i+1}/{total_batches}.",
                    "data": files_info
                }) + "\n"

        except Exception as e:
            print(f"FAILED during batch generation: {e}")
            yield json.dumps({"status": "error", "message": f"Failed during batch generation for {files_to_generate}: {e}"}) + "\n"
            continue

        if i < len(all_batches_to_process) - 1:
            yield json.dumps({"status": "waiting", "message": "Waiting 60s before next batch..."}) + "\n"
            await asyncio.sleep(60)


async def _generate_and_stream_files(request: PromptRequest):
    mongo_client = MongoClient(os.environ["MONGODB_URI"])
    db = mongo_client["ui_files"]
    gen_files_coll = db["generated_files"]

    # === Step 1: Generate Template ===
    try:
        yield json.dumps({"status": "starting", "message": "Generating files structure..."}) + "\n"
        file_structure = await _create_file_template(request, db)
        yield json.dumps({"status": "progress", "message": "Gathering UX context..."}) + "\n"
    except Exception as e:
        print(f"ERROR: Failed to generate template: {e}")
        yield json.dumps({"status": "error", "message": f"Failed to generate files: {str(e)}"}) + "\n"
        return

    # === Step 2: Generate Content in batches ===
    async for update in _generate_file_content_stream(request, file_structure, db):
        yield update

    # === Step 3: Fetch all generated files and return ===
    all_files = list(gen_files_coll.find(
        {"project_id": request.project_id, "file_id": request.file_id},
        {"_id": 0, "created_at": 0}
    ))
    print("Project Generation Compelete")
    yield json.dumps({
        "status": "complete",
        "message": "Project generation completed.",
        "data": all_files
    }) + "\n"

# ---------------- Endpoints ----------------

@app.post("/get-or-generate-files")
async def get_or_generate_files(request: PromptRequest):
    """
    Checks if project files exist. If they do, returns them immediately.
    If not, it starts the generation process and streams progress updates to the client.
    """
    mongo_client = MongoClient(os.environ["MONGODB_URI"])
    db = mongo_client["ui_files"]
    gen_files_coll = db["generated_files"]

    # Check if files already exist
    existing_files = list(gen_files_coll.find(
        {"project_id": request.project_id, "file_id": request.file_id},
        {"_id": 0, "created_at": 0}
    ))

    if existing_files:
        print("INFO: Files already exist. Returning them.")
        return JSONResponse(
            status_code=200,
            content={
                "status": "complete",
                "message": "Files already exist in DB.",
                "data": existing_files
            }
        )
    else:
        print("INFO: Files not found. Starting generation and streaming response.")
        return StreamingResponse(
            _generate_and_stream_files(request),
            media_type="application/x-ndjson"
        )

@app.get("/get-project-files")
def get_project_files(project_id: str = Query(...), file_id: str = Query(...)):
    """
    Get all the project's files.
    """
    mongo_client = MongoClient(os.environ.get("MONGODB_URI"))
    db = mongo_client["ui_files"]
    gen_files_coll = db["generated_files"]

    try:
        docs = list(gen_files_coll.find({"project_id": project_id, "file_id": file_id}, {"_id": 0, "created_at": 0}))
        if docs:
            return JSONResponse(status_code=200, content={"message": "Fetched files successfully", "data": docs})
        else:
            # It's better to return an empty list than a 500 error if nothing is found
            return JSONResponse(status_code=200, content={"message": "No files found for this project", "data": []})
    except Exception as e:
        print(f"ERROR: Fetching files: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error while fetching files.")


@app.get("/")
def get_slash():
    return JSONResponse(status_code=200, content={"message": "Server Running"})
