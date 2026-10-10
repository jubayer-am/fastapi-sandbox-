#Use this whenever you practice inside Google Colab (includes the tunnel hacks)

# 1. Install localtunnel globally in npm environment quietly
!npm install -g localtunnel > /dev/null 2>&1

import nest_asyncio
import uvicorn
import asyncio
import subprocess
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 2. Allow nested event loops in Colab
nest_asyncio.apply()

# 3. Create the FastAPI app
app = FastAPI(title="jb's playground")

# In-memory storage
todo_db = {}

# Pydantic Schema
class TodoItem(BaseModel):
    title: str
    completed: bool = False

# Routes
@app.get("/") #Read / Retrieve data from the server
def read_root():
    return {"message": "Hello from Colab!"}

@app.post("/todos/{item_id}", status_code=201) #Create / Send new data to the server.
def create_todo(item_id: int, item: TodoItem):
    if item_id in todo_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    todo_db[item_id] = item
    return {"status": "success", "data": item}

@app.get("/todos/{item_id}") 
def get_todo(item_id: int):
    if item_id not in todo_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return todo_db[item_id]

# 4. Reliable localtunnel launcher using npx
print("🚀 Starting public tunnel using npx localtunnel...")
lt_process = subprocess.Popen(
    ["npx", "localtunnel", "--port", "8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(5)
url = None
for _ in range(10):
    line = lt_process.stdout.readline()
    if "url is" in line:
        url = line.strip().split("url is:")[-1].strip()
        print(f"🚀 Live Base URL: {url}")
        print(f"📚 Live Swagger Docs: {url}/docs")
        break

if not url:
    print("⚠️ Could not automatically parse localtunnel URL. Try running the cell again.")

# 5. Start Uvicorn Server
config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
server = uvicorn.Server(config)
asyncio.run(server.serve())
