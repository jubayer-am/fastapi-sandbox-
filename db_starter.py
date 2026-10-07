#Use this when connecting to databases (like Supabase, PostgreSQL, or SQLite) using async/await and dependency injection


from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Database API")

# Fake DB connection dependency
def get_db():
    db = {"status": "connected"}
    return db

@app.get("/items")
def read_items(db = Depends(get_db)):
    return {"db_status": db["status"], "items": []}
