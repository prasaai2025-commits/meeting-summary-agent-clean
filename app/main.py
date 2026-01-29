from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from app.agent import run_agent
import os, shutil, uuid

app = FastAPI()

UPLOAD_DIR = "app/uploads"
OUTPUT_DIR = "app/outputs"
STATUS_DIR = "app/status"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATUS_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "Meeting Summary Agent Running"}

def process_job(job_id: str, path: str):
    try:
        name = run_agent(path)
        with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
            f.write("done")
    except Exception as e:
        with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
            f.write(f"error:{str(e)}")

@app.post("/upload")
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    job_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
        f.write("processing")

    background_tasks.add_task(process_job, job_id, path)

    return {
        "job_id": job_id,
        "status": "processing"
    }

@app.get("/status/{job_id}")
def job_status(job_id: str):
    status_file = f"{STATUS_DIR}/{job_id}.txt"
    if not os.path.exists(status_file):
        return {"status": "unknown"}

    with open(status_file) as f:
        status = f.read()

    if status == "done":
        return {
            "status": "done",
            "docx": f"/download/docx/{job_id}",
            "pdf": f"/download/pdf/{job_id}"
        }

    return {"status": status}

@app.get("/download/docx/{job_id}")
def download_docx(job_id: str):
    return FileResponse(f"app/outputs/{job_id}.docx")

@app.get("/download/pdf/{job_id}")
def download_pdf(job_id: str):
    return FileResponse(f"app/outputs/{job_id}.pdf")
