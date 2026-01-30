import os
from app.transcribe import transcribe_audio
from app.summarize import summarize_text
from app.utils import create_docx, create_pdf

STATUS_DIR = "status"
OUTPUT_DIR = "outputs"


def run_agent(job_id: str, file_path: str):
    try:
        os.makedirs(STATUS_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
            f.write("TRANSCRIBING")

        transcript = transcribe_audio(file_path)

        with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
            f.write("SUMMARIZING")

        summary = summarize_text(transcript)

        create_docx(summary, f"{OUTPUT_DIR}/{job_id}.docx")
        create_pdf(summary, f"{OUTPUT_DIR}/{job_id}.pdf")

        with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
            f.write("COMPLETED")

    except Exception as e:
        with open(f"{STATUS_DIR}/{job_id}.txt", "w") as f:
            f.write("ERROR")
