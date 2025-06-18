# pip install fastapi uvicorn requests
# FastAPI application as backend to serve a simple AI chat assistant using LM Studio API
# Build the frontend with HTML, CSS, and JavaScript in the static directory to facilitate user interaction.
# The LLM used here is Meta's Llama 3.1 8B model, but you can change it to any other model available in LM Studio.


from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests 
import os
import json

app = FastAPI()

# serve the frontend files from the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# LM studio settings
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"  # LM Studio default API endpoint
#LM_STUDIO_MODEL = "Llama 3.1 8B Claude 3.7 Sonnet Reasoning Distilled (Q4_0)"  # Default model
LM_STUDIO_MODEL = "meta-llama-3.1-8b-instruct"  # alternate model


@app.get("/")
def serve_homepage():
    """
    Serve the main HTML page.
    """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/chat")
def chat(prompt: str = Query(..., description="The input prompt to send to the model.")):
    """
    Sends a prompt to the LM Studio API and returns the response.
    
    Args:
        prompt (str): The input prompt to send to the model.
    
    Returns:
        dict: The response from the model.
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "model": LM_STUDIO_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.02,
        "max_tokens": 100,
        "stream": False
    }

    try:
        response = requests.post(LM_STUDIO_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        result = response.json()
        # LM Studio returns the result in choices[0]["text"]
        
        if not result.get("choices"):
            raise HTTPException(status_code=500, detail="No choices returned from the model.")
        # Extract the full content, strip whitespace/newlines
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        return {"ai_response": ''.join(content.strip(' \n'))}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

#Run the app with:
# uvicorn app:app --reload  
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
