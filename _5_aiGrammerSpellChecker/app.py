# AI Proof Reader using FastAPI and LM Studio serving the backend LLM model 
# This application provides an API endpoint to check spelling, grammer and sentence structure using a language model.   
# It serves a static HTML page for user interaction and handles proof reading requests.
# Here we are using the model "deepseek-r1" hosted on LM Studio, which is based on LLaMA 3 architecture.

from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_URL = "http://127.0.0.1:1234/v1/completions"  # Updated URL for Ollama API
MODEL_NAME = "deepseek-r1-distill-llama-8b"  # Using deepseek model for proof reading

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/proofread_text")
def proofread_text(text: str = Form(...)):
    headers = {"Content-Type": "application/json"}

    # set up the prompt for the model
    prompt = f"Proofread the following text:\n\n{text}\n\nPlease provide the corrected version."    
     
    try:
        # Send the input prompt to Ollama for content generation
       
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            headers=headers
        )
        result = response.json()
        # print the response for debugging
        print("Response from LM Studio API:", json.dumps(result, indent=2))

        # Extract the content from the response
        corrected_text = result.get("choices", [{}])[0].get("text", "")
        print("returned_text:", corrected_text)        
        return {"returned_text": corrected_text}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LM Studio API: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)