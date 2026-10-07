#Use this whenever you practice inside Google Colab (includes the tunnel hacks)

import nest_asyncio, uvicorn, asyncio, subprocess, time
from fastapi import FastAPI
from pydantic import BaseModel

nest_asyncio.apply()
app = FastAPI(title="Colab Playground")

# --- YOUR ROUTES GO HERE ---
@app.get("/")
def home():
    return {"message": "Hello from Colab!"}

# --- TUNNEL & SERVER RUNNER ---
lt_process = subprocess.Popen(["lt", "--port", "8000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
time.sleep(3)
for _ in range(5):
    line = lt_process.stdout.readline()
    if "url is" in line:
        url = line.strip().split("url is:")[-1].strip()
        print(f"🔗 Live Docs: {url}/docs")
        break

config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
server = uvicorn.Server(config)
asyncio.run(server.serve())
