from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import threading, os, uuid, json

from app.agent import run_agent

STATUS_DIR = "status"
UPLOAD_DIR = "uploads"

os.makedirs(STATUS_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

def background_job(path, job_id):
    status_path = f"{STATUS_DIR}/{job_id}.txt"
    try:
        with open(status_path, "w") as f:
            f.write("transcribing")

        result = run_agent(path, job_id)

        # ✅ write FINAL result as JSON
        with open(status_path, "w") as f:
            f.write(json.dumps({
                "status": "done",
                "outputs": result
            }))

    except Exception as e:
        with open(status_path, "w") as f:
            f.write(json.dumps({
                "status": "error",
                "message": str(e)
            }))


@app.post("/generate")
async def generate(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{job_id}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
        f.write("queued")

    threading.Thread(
        target=background_job,
        args=(file_path, job_id),
        daemon=True
    ).start()

    return JSONResponse({"job_id": job_id})


@app.get("/status/{job_id}")
def status(job_id: str):
    status_file = f"{STATUS_DIR}/{job_id}.txt"
    if not os.path.exists(status_file):
        return {"status": "unknown"}

    with open(status_file) as f:
        return json.loads(f.read())
