import os
from app.transcribe import transcribe_audio
from app.summarize import summarize_text
from app.utils import generate_docx, generate_pdf

BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
STATUS_DIR = os.path.join(BASE_DIR, "status")


def run_agent(file_path: str, job_id: str):
    try:
        # 1️⃣ Transcribe
        transcript = transcribe_audio(file_path)

        # 2️⃣ Summarize
        summary = summarize_text(transcript)

        # 3️⃣ Generate files
        docx_path = generate_docx(summary, job_id)
        pdf_path = generate_pdf(summary, job_id)

        # 4️⃣ WRITE FINAL STATUS
        with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
            f.write(str({
                "status": "done",
                "docx": f"/outputs/{os.path.basename(docx_path)}",
                "pdf": f"/outputs/{os.path.basename(pdf_path)}"
            }))

    except Exception as e:
        with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
            f.write(str({"status": "error"}))
