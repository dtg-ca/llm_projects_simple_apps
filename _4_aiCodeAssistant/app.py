# AI Code assistant & Debugger using FastAPI and LM Studio serving the backend LLM model 
# This application provides an API endpoint to summarize text using a language model.   
# It serves a static HTML page for user interaction and handles code manipulation requests.
# Here we are using the model  "codelama-7b-python-10k-platypus-v3" from LM Studio, which is based on LLaMA 3 architecture.


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
MODEL_NAME = "codelama-7b-python-10k-platypus-v3"  # Using LLaMA 3 for code generation

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/generate_code")
def generate_code(prompt: str = Form(...), mode: str = Form(...)):
    headers = {"Content-Type": "application/json"}

    # set up the prompt for the model
    if mode ==  "code":
        full_prompt = f"Write a Python code snippet that {prompt}"
    elif mode == "debug":
        full_prompt = f"Debug the following Python code: {prompt}"
    else:
        raise HTTPException(status_code=400, detail="Invalid mode. Use 'code' or 'debug'.")
        
    
    try:
        # Send the input prompt to Ollama for content generation
       
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": full_prompt, "stream": False},
            headers=headers
        )
        result = response.json()
        # print the response for debugging
        print("Response from LM Studio API:", json.dumps(result, indent=2))

        # Extract the content from the response
        code = result.get("choices", [{}])[0].get("text", "")
        print("generated_code:", code)        
        return {"generated_code": code}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LM Studio API: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)