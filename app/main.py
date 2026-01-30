from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os, uuid, threading

from app.agent import run_agent

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
STATUS_DIR = os.path.join(BASE_DIR, "status")

for d in [UPLOAD_DIR, OUTPUT_DIR, STATUS_DIR]:
    os.makedirs(d, exist_ok=True)


# -------------------------
# UPLOAD ENDPOINT
# -------------------------
@app.post("/upload")
def upload(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # mark job as processing
    with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
        f.write("processing")

    # run agent in BACKGROUND THREAD
    threading.Thread(
        target=run_agent,
        args=(file_path, job_id),
        daemon=True
    ).start()

    return {"job_id": job_id}


# -------------------------
# STATUS ENDPOINT (YOU ASKED ABOUT THIS)
# -------------------------
@app.get("/status/{job_id}")
def status(job_id: str):
    path = f"{STATUS_DIR}/{job_id}.txt"

    if not os.path.exists(path):
        return {"status": "unknown"}

    with open(path) as f:
        return JSONResponse(content=eval(f.read()))
