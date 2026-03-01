from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CommentInput(BaseModel):
    comment: str

class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    rating: int

@app.post("/comment", response_model=SentimentResponse)
async def analyze_comment(input_data: CommentInput):
    """Analyze sentiment of a comment and return structured JSON response."""
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sentiment analysis expert. Analyze the sentiment of the given comment and return the result as structured JSON."
                },
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of this comment: {input_data.comment}"
                }
            ],
            response_format=SentimentResponse,
        )
        
        result = response.choices[0].message.parsed
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Sentiment API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
