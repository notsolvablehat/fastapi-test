from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri)
    try:
        db = client["ui_files"]

        project_files = db["project_files"]

        # Insert a document (creates DB and collection if not existing)
        with open("files.json", "r") as f:
            files = f.read()

        file_content = {
            "file_id": "some_file_id",
            "files": files
        }
        result = project_files.insert_one(file_content)
        print(f"Inserted document ID: {result.inserted_id}")

        # Fetch the document back
        fetched_files = project_files.find_one({"file_id": "some_file_id"})
        print("Fetched document:", fetched_files)

        client.close()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
