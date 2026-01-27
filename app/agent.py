from app.preprocess import chunk_text
from app.summarize import summarize_text
from faster_whisper import WhisperModel
from app.utils import save_docx, save_pdf
import os

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(file_path: str) -> str:
    segments, _ = model.transcribe(file_path)
    return " ".join(seg.text for seg in segments)

def run_agent(file_path: str):
    text = transcribe_audio(file_path)
    summary = summarize_text(text)

    name = os.path.splitext(os.path.basename(file_path))[0]

    save_docx(summary, f"app/outputs/{name}.docx")
    save_pdf(summary, f"app/outputs/{name}.pdf")

    return name
