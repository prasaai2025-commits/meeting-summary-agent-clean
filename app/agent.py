
from app.transcribe import transcribe_audio
from app.summarize import summarize_text
from app.utils import save_docx, save_pdf
import os

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_agent(path, job_id):
    # 1. Transcribe
    text = transcribe_audio(path)

    # 2. Summarize
    summary = summarize_text(text)

    # 3. Save outputs
    docx_path = f"{OUTPUT_DIR}/{job_id}.docx"
    pdf_path = f"{OUTPUT_DIR}/{job_id}.pdf"

    save_docx(summary, docx_path)
    save_pdf(summary, pdf_path)

    # 4. Return file paths (IMPORTANT)
    return {
        "docx": docx_path,
        "pdf": pdf_path
    }
