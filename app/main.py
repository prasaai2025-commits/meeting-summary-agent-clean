from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
import uuid, os

from app.agent import run_agent

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
STATUS_DIR = "status"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATUS_DIR, exist_ok=True)


@app.post("/upload")
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    job_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{job_id}_{file.filename}"

    # ✅ STREAM FILE (prevents 502)
    with open(file_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    # run in background
    background_tasks.add_task(run_agent, job_id, file_path)

    return {
        "job_id": job_id,
        "status": "processing"
    }


@app.get("/status/{job_id}")
def get_status(job_id: str):
    status_file = f"{STATUS_DIR}/{job_id}.txt"

    if not os.path.exists(status_file):
        return {"status": "processing"}

    with open(status_file) as f:
        status = f.read().strip()

    if status == "COMPLETED":
        return {
            "status": "done",
            "docx": f"/download/{job_id}/docx",
            "pdf": f"/download/{job_id}/pdf",
        }

    if status == "ERROR":
        return {"status": "error"}

    return {"status": "processing"}


@app.get("/download/{job_id}/{fmt}")
def download(job_id: str, fmt: str):
    path = f"{OUTPUT_DIR}/{job_id}.{fmt}"
    if not os.path.exists(path):
        return {"error": "file not ready"}
    return FileResponse(path, filename=os.path.basename(path))
