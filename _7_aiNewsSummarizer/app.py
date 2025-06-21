# AI News Summarizer using FastAPI and LM Studio serving the backend LLM model 
# This application provides an API endpoint to summarize news articles using a language model. 
#  It fetches news articles from an external API based on user-defined parameters. #   
# It serves a static HTML page for user interaction and handles user requests.
# Here we are using the model "qwen3-4b" hosted on LM Studio.

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json
 
app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Configuration
OLLAMA_URL = "http://127.0.0.1:1234/v1/completions"  # Updated URL for Ollama API
MODEL_NAME = "meta-llama-3.1-8b-instruct"  # Using Qwen model for news summarization
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"  # Example news API URL
NEWS_API_KEY = "47e5d2fcb4284d08be705596282618cd"  # Replace with your actual News API key

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/fetch_news")
def fetch_and_summarize_news(category: str = Query("technology")):
    """ Fetches latest news articles and summarizes them using Ollama """
    headers = {"Authorization": f"Bearer {NEWS_API_KEY}"}
    params = {"category": category, "language": "en", "apiKey": NEWS_API_KEY}
    
    try:
        news_response = requests.get(NEWS_API_URL, params=params, headers=headers)
        if news_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch news articles")

        news_data = news_response.json()
        if "articles" not in news_data or not news_data["articles"]:
            return {"summary": "No news articles found for this category."}

        # Extract top 3 articles
        articles = news_data["articles"][:3]
        news_text = "\n".join([f"- {article['title']} ({article['source']['name']})" for article in articles])

        # Send news text to Ollama for summarization
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": f"Summarize these news headlines in a very consise manner. Do not repeat the same lines or information again and again:\n{news_text}", "stream": False},
        )

        # Log response
        result = response.json()
        # print the response for debugging
        print("Response from LM Studio API:", json.dumps(result, indent=2))

        # Extract the content from the response
        summary = result.get("choices", [{}])[0].get("text", "")
        print("news_summary:",  summary)               
        return {"news_summary":  summary, 'articles': articles}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LM Studio API: {str(e)}")