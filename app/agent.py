import os
from app.transcribe import transcribe_audio
from app.summarize import summarize_text
from app.utils import save_docx, save_pdf

OUTPUT_DIR = "outputs"
STATUS_DIR = "status"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATUS_DIR, exist_ok=True)

def run_agent(file_path: str, job_id: str) -> str:
    status_path = f"{STATUS_DIR}/{job_id}.txt"

    def update(msg):
        with open(status_path, "w") as f:
            f.write(msg)

    try:
        update("transcribing")
        transcript = transcribe_audio(file_path)

        update("summarizing")
        summary = summarize_text(transcript)

        docx_path = f"{OUTPUT_DIR}/{job_id}.docx"
        pdf_path = f"{OUTPUT_DIR}/{job_id}.pdf"

        update("saving_files")
        save_docx(summary, docx_path)
        save_pdf(summary, pdf_path)

        update("completed")
        return "completed"

    except Exception as e:
        update(f"error: {str(e)}")
        return "error"
