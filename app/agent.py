from app.transcribe import transcribe_audio
from app.summarize import summarize_text
from app.utils import save_docx, save_pdf
import os

def run_agent(file_path: str):
    text = transcribe_audio(file_path)
    summary = summarize_text(text)

    name = os.path.splitext(os.path.basename(file_path))[0]

    save_docx(summary, f"app/outputs/{name}.docx")
    save_pdf(summary, f"app/outputs/{name}.pdf")

    return name
