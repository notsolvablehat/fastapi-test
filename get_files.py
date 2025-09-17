import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

# --- Configuration ---
DATABASE_NAME = "ui_files"
COLLECTION_NAME = "generated_files"

# --- MODIFIED: Added FILE_ID for more specific filtering ---
PROJECT_ID = "test-project2-v3-test1"
# !! IMPORTANT: Set the specific file_id you want to retrieve !!
FILE_ID = "test-file-v3-test1" 

# --- MODIFIED: Output directory now includes both IDs for clarity ---
OUTPUT_DIR = f"{PROJECT_ID}_{FILE_ID}"

# --- Main Script ---

if not MONGO_URI:
    print("Error: MONGODB_URI not found in .env file.")
    exit(1)

client = None
files_written_count = 0

try:
    # 1. Connect to MongoDB
    print("Connecting to MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("Connection successful.")

    # 2. --- MODIFIED: Query now includes file_id ---
    print(f"Searching for documents with project_id='{PROJECT_ID}' and file_id='{FILE_ID}'...")
    query = {"project_id": PROJECT_ID, "file_id": FILE_ID}
    documents_cursor = collection.find(query)

    # 3. Loop through results and write files
    for document in documents_cursor:
        content = document.get("content")
        file_path_from_db = document.get("path")

        if content is None or file_path_from_db is None:
            print(f"⚠️  Skipping document with _id '{document.get('_id')}' due to missing 'content' or 'path' field.")
            continue

        # Create the full local path for the file
        output_file_path = os.path.join(OUTPUT_DIR, file_path_from_db)
        
        # Get the directory part of the path
        directory_for_file = os.path.dirname(output_file_path)
        
        # Create the necessary subdirectories
        os.makedirs(directory_for_file, exist_ok=True)

        # 4. Write the content to the file
        print(f"Writing file to '{output_file_path}'...")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        files_written_count += 1
    
    # 5. Final summary
    if files_written_count > 0:
        print(f"\n✅ Successfully saved {files_written_count} files to the '{OUTPUT_DIR}' directory.")
    else:
        print(f"❌ No documents found for project_id '{PROJECT_ID}' and file_id '{FILE_ID}'.")


except ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # 6. Ensure the connection is closed
    if client:
        client.close()
        print("Connection closed.")