import os
from app.transcribe import transcribe_audio
from app.summarize import summarize_text
from app.utils import save_docx, save_pdf

OUTPUT_DIR = "outputs"
STATUS_DIR = "status"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_agent(path: str, job_id: str):
    status_file = f"{STATUS_DIR}/{job_id}.txt"

    try:
        with open(status_file, "w") as f:
            f.write("transcribing")

        transcript = transcribe_audio(path)

        with open(status_file, "w") as f:
            f.write("summarizing")

        summary = summarize_text(transcript)

        docx_path = f"{OUTPUT_DIR}/{job_id}.docx"
        pdf_path = f"{OUTPUT_DIR}/{job_id}.pdf"

        save_docx(summary, docx_path)
        save_pdf(summary, pdf_path)

        with open(status_file, "w") as f:
            f.write("completed")

    except Exception as e:
        with open(status_file, "w") as f:
            f.write(f"error:{str(e)}")
