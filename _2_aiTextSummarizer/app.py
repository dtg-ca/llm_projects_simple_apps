# AI Text Summarizer using FastAPI and LM Studio serving the backend LLM model 
# This application provides an API endpoint to summarize text using a language model.   
# It serves a static HTML page for user interaction and handles text summarization requests.
# Here we are using the model "meta-llama-3.1-8b-instruct" hosted on LM Studio.

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import FileResponse  
from fastapi.staticfiles import StaticFiles
import os
import json
import requests

app = FastAPI()
# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

LMStudio_API_URL = "http://localhost:1234/v1/completions"  # Replace with your LM Studio API URL
MODEL_NAME = "meta-llama-3.1-8b-instruct"  


@app.get("/")   
def serve_index():
    return FileResponse(os.path.join('static', 'index.html'))

@app.post("/summarize")
def summarize_text(text: str = Form(...)):
    if not text:
        raise HTTPException(status_code=400, detail="Text is required for summarization.")

    headers = {
        "Content-Type": "application/json",
        
    }

    payload = {
        "model": MODEL_NAME,
        "prompt": f"Summarize the following text:\n\n{text}",
        "max_tokens": 150,  # Adjust as needed
        "temperature": 0.2, # Adjust for more or less randomness
        "stream": False,  # Set to True if you want streaming responses
    }

    try:
        response = requests.post(LMStudio_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        print(result)  # Debugging line to see the response structure
        summary = result.get("choices", [{}])[0].get("text", "")
        return {"summary": summary}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Run the app with:
# uvicorn app:app --reload  
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)