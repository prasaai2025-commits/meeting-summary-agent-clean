from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
import os, uuid
from app.agent import run_agent

app = FastAPI()

UPLOAD_DIR = "uploads"
STATUS_DIR = "status"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STATUS_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...), bg: BackgroundTasks = None):
    job_id = str(uuid.uuid4())
    path = f"{UPLOAD_DIR}/{job_id}_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
        f.write("processing")

    bg.add_task(run_agent, path, job_id)

    return JSONResponse({"job_id": job_id})

@app.get("/status/{job_id}")
def status(job_id: str):
    p = f"{STATUS_DIR}/{job_id}.txt"
    if not os.path.exists(p):
        return {"status": "unknown"}
    return {"status": open(p).read()}
