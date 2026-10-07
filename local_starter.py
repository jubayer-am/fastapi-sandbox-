from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Local API")

# --- YOUR ROUTES GO HERE ---
@app.get("/")
def home():
    return {"message": "Hello from Local Machine!"}

# Run in terminal with: uvicorn local_starter:app --reload
