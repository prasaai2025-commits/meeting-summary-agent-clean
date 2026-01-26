import os
from app.transcribe import transcribe_audio
from app.summarize import summarize_text
from app.utils import save_docx, save_pdf

OUTPUT_DIR = "app/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_agent(audio_path: str):
    filename = os.path.splitext(os.path.basename(audio_path))[0]

    print("🎧 Transcribing...")
    transcript = transcribe_audio(audio_path)

    print("🧠 Summarizing...")
    summary = summarize_text(transcript)

    docx_path = os.path.join(OUTPUT_DIR, f"{filename}.docx")
    pdf_path = os.path.join(OUTPUT_DIR, f"{filename}.pdf")

    save_docx(summary, docx_path)
    save_pdf(summary, pdf_path)

    return filename
