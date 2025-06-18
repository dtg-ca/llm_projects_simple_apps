# AI Content Writer using FastAPI and LM Studio serving the backend LLM model 
# This application provides an API endpoint to generate text using a language model.   
# It serves a static HTML page for user interaction and handles text generation requests using uvicorn library.
# Here we are using the model "meta-llama-3.1-8b-instruct" hosted on LM Studio.

from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import json
import requests

app = FastAPI()
# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

LMStudio_API_URL = "http://localhost:1234/v1/completions"
MODEL_NAME = "meta-llama-3.1-8B-Instruct"

@app.get("/")
def serve_homepage():
    return FileResponse(os.path.join('static', 'index.html'))

@app.post("/generate")
def generate_content(topic: str = Form(...), style: str = Form(...)):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "prompt": f"Write a {style} tone, article about {topic}.",
        "max_tokens": 1000,
        "temperature": 0.5,
        "stream": False,
    }

    try:
        response = requests.post(LMStudio_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        result = response.json()
        # print the response for debugging
        print("Response from LM Studio API:", json.dumps(result, indent=2))

        # Extract the content from the response
        content = result.get("choices", [{}])[0].get("text", "")

        # ensure valid json response
        try:
            json.loads(content) # Check if content is valid JSON    
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Received invalid JSON from LM Studio API")
        return {"content": content}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LM Studio API: {str(e)}")

# Run the FastAPI app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.1", port=8000, reload=True, debug=True)    