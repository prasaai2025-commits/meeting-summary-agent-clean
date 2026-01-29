import os, uuid, threading
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from app.agent import run_agent

UPLOAD_DIR = "uploads"
STATUS_DIR = "status"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STATUS_DIR, exist_ok=True)

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    path = f"{UPLOAD_DIR}/{job_id}_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
        f.write("queued")

    thread = threading.Thread(
        target=run_agent,
        args=(path, job_id),
        daemon=True
    )
    thread.start()

    return JSONResponse({
        "job_id": job_id,
        "status": "started"
    })

@app.get("/status/{job_id}")
def status(job_id: str):
    path = f"{STATUS_DIR}/{job_id}.txt"
    if not os.path.exists(path):
        return {"status": "unknown"}

    with open(path) as f:
        return {"status": f.read()}
