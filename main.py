from google import genai
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
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

class GeneratedCodeFile(BaseModel):
    name: str
    content: str

class GenerateFilesRequest(BaseModel):
    project_id: str
    file_id: str
    ui_prompt: str

class PromptRequest(BaseModel):
    prompt: str
    file_id: str
    project_id: str

# ---------------- Load env + app ----------------
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ---------------- Load prompts ----------------
try:
    with open("step_prompt.txt", "r") as f:
        steps_prompt = f.read()
except FileNotFoundError as e:
    print(f"Error: Prompt file not found - {e}. Please ensure step_prompt.txt and ui_prompt.txt exist.")
    steps_prompt, ui_prompt = "", ""

# ---------------- Endpoints ----------------
@app.post("/generate-initial")
async def generate_initial_files(request: GenerateFilesRequest):

    # Mongo client
    mongo_client = MongoClient(os.environ["MONGODB_URI"])
    db = mongo_client["ui_files"]
    generated_files_coll = db["generated_files"]

    try:
        files_template = db["project_files"]
        doc = files_template.find_one({"project_id": request.project_id, "file_id": request.file_id}, {"_id": 0, "files": 1})
        if doc:
            file_structure = doc["files"]
            print(f"INFO: Fetched files for {request.project_id}, {request.file_id}", file_structure)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="File or Project not found")

    screen_specs = request.ui_prompt
    with open("step_prompt.txt", "r") as f:
        sys_ins = f.read()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model="gemini-2.5-pro")

    # 1. Initial prompt
    initial_prompt = f"""
    First, carefully review this entire file architecture...
    # RULES
    {sys_ins}

    # File architecture:
    {json.dumps(file_structure, indent=2)}

    # Screen specifications:
    {screen_specs}
    Acknowledge that you have understood the architecture.
    """
    print("Sending initial architecture context to Gemini...")
    initial_response = chat.send_message(initial_prompt)
    print("Gemini Acknowledged:", initial_response.text)

    all_generated_files = []
    process_order, batch_size = ["js", "html"], 8
    all_batches_to_process = []

    # Create batches
    for category in process_order:
        print("Process order", process_order)
        if category in file_structure and file_structure[category]: # type: ignore
            print("Inside IF")
            file_names = file_structure[category] # type: ignore
            for i in range(0, len(file_names), batch_size):
                batch = file_names[i:i + batch_size]
                all_batches_to_process.append({"category": category, "files": batch})

    # Process each batch
    for i, batch_info in enumerate(all_batches_to_process):
        category, files_to_generate = batch_info["category"], batch_info["files"]
        print(f"\nRequesting generation for '{category}' batch: {files_to_generate}")

        generation_prompt = f"""
        Generate the code for all files in this batch...
        {json.dumps(files_to_generate)}
        """

        try:
            response = chat.send_message(
                generation_prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": list[GeneratedCodeFile],
                },
            )
            generated_batch_data: list[GeneratedCodeFile] = response.parsed # type: ignore

            # Prepare Mongo docs
            batch_documents = [
                {
                    "project_id": request.project_id,
                    "file_id": request.file_id,
                    "path": f.name,
                    "file_type": category,
                    "content": f.content,
                    "created_at": datetime.now(timezone.utc),
                }
                for f in generated_batch_data
            ]

            if batch_documents:
                result = generated_files_coll.insert_many(batch_documents)
                print(f"Inserted {len(result.inserted_ids)} files into Mongo.")

        except ValidationError as e:
            print(f"Skipping invalid batch: {e}")
            continue
        except Exception as e:
            print(f"FAILED during batch generation: {e}")
            continue

        if i < len(all_batches_to_process) - 1:
            print("\nFinished processing batch. Waiting 60s before next batch...")
            await asyncio.sleep(60)

    return JSONResponse(
        status_code=200,
        content={"message": "Project generation completed."},
    )

@app.post("/template")
def generate_template(request: PromptRequest):
    """
    Generates a file structure template based on a user prompt.
    Response is validated against FilesResponse schema.
    """
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    final_prompt = request.prompt

    print("Sending Request to Gemini")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=steps_prompt,
            response_schema=FilesResponse,
            response_mime_type="application/json",
        ),
        contents=[final_prompt],
    )

    if response and response.candidates:
        print("Request recieved from Gemini")
        text = response.candidates[0].content.parts[0].text  # type: ignore
        try:
            parsed = FilesResponse.model_validate_json(text)  # type: ignore
            with open("files.json", "w", encoding="utf-8") as f:
                json.dump(parsed.model_dump(), f, indent=4)

            uri = os.environ.get("MONGODB_URI")
            client = MongoClient(uri)

            db = client["ui_files"]

            project_files = db["project_files"]

            project_file_templates = {
                "project_id": request.project_id,
                "file_id": request.file_id,
                "files": parsed.model_dump()
            }

            result = project_files.insert_one(project_file_templates)

            print(f"File Templates written: {result.inserted_id}")

            return JSONResponse(content=parsed.model_dump())
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e), "raw": text})

    return JSONResponse(status_code=500, content={"message": "Failed to generate template from model."})

@app.get("/get-project-files")
def get_project_files(project_id: str = Query(...), file_id: str = Query(...)):
    uri = os.environ.get("MONGODB_URI")

    client = MongoClient(uri)

    db = client["ui_files"]
    gen_files = db["generated_files"]

    try:
        docs = list(gen_files.find({"project_id": project_id, "file_id": file_id}, {"_id": 0, "created_at": 0}))
        if docs:
            print(docs)
            return JSONResponse(status_code=200, content={"message": "Fetched files successfully", "data": docs})
        else:
            print("ERROR: Fetching files")
            return JSONResponse(status_code=500, content={"message": "Project or file not found"})
    except Exception as e:
        print("ERROR: Fetching files", e)
        return HTTPException(status_code=500, detail={"message": "Internal Server Error"})

@app.get("/")
def get_slash():
    return JSONResponse(status_code=200, content={"message": "Server Running"})
