from preprocess import chunk_text
from faster_whisper import WhisperModel
from docx import Document
from fpdf import FPDF
import os

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(file_path: str) -> str:
    segments, _ = model.transcribe(file_path)
    text = " ".join(segment.text for segment in segments)
    return text

def summarize_text(text: str) -> str:
    chunks = chunk_text(text)
    summary = ""

    for chunk in chunks:
        summary += chunk[:500] + "\n\n"

    return summary

def save_outputs(summary: str, name: str):
    doc = Document()
    doc.add_paragraph(summary)
    doc_path = f"app/outputs/{name}.docx"
    doc.save(doc_path)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in summary.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf_path = f"app/outputs/{name}.pdf"
    pdf.output(pdf_path)

def run_agent(file_path: str):
    text = transcribe_audio(file_path)
    summary = summarize_text(text)

    name = os.path.splitext(os.path.basename(file_path))[0]
    save_outputs(summary, name)

    return name
