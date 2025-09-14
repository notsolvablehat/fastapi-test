import json
import requests

# Payload for the request
payload = {
  "project_id": "test-project-3",
  "file_id": "test-file-4",
  "prompt": "Personalized Study Plan Creator"
}

# The endpoint URL
url = "http://127.0.0.1:8000/get-or-generate-files"

try:
    with requests.post(url, json=payload, stream=True) as r:
        r.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        if r.headers.get('Content-Type') == 'application/x-ndjson':
            print("INFO: Receiving a streaming response...")
            for line in r.iter_lines():
                if line:
                    try:
                        # Decode and parse each line as a JSON object
                        data = json.loads(line.decode('utf-8'))
                        print(json.dumps(data, indent=2))
                        
                        # Check for completion or errors
                        if data.get("status") == "complete":
                            print("SUCCESS: Project generation is complete.")
                            break
                        elif data.get("status") == "error":
                            print(f"ERROR: {data.get('message')}")
                            break
                            
                    except json.JSONDecodeError:
                        print(f"ERROR: Could not decode JSON from line: {line}")
        else:
            # Handle non-streaming (e.g., cached files) JSON response
            print("INFO: Received a standard JSON response (not a stream).")
            response_data = r.json()
            print(json.dumps(response_data, indent=2))

except requests.exceptions.RequestException as e:
    print(f"FAILED to connect to the server: {e}")