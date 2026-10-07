#Use this when running FastAPI locally on VS Code, Termux, or Linux (clean and minimal)


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Local API")

# --- YOUR ROUTES GO HERE ---
@app.get("/")
def home():
    return {"message": "Hello from Local Machine!"}

# Run in terminal with: uvicorn local_starter:app --reload
