from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from app.agent import run_agent
import os, shutil

app = FastAPI()

UPLOAD_DIR = "app/uploads"
OUTPUT_DIR = "app/outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "Meeting Summary Agent Running"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    name = run_agent(path)

    return {
        "status": "success",
        "docx": f"/download/docx/{name}",
        "pdf": f"/download/pdf/{name}"
    }

@app.get("/download/docx/{name}")
def download_docx(name: str):
    return FileResponse(f"app/outputs/{name}.docx", filename=f"{name}.docx")

@app.get("/download/pdf/{name}")
def download_pdf(name: str):
    return FileResponse(f"app/outputs/{name}.pdf", filename=f"{name}.pdf")
