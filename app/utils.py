from docx import Document
from reportlab.pdfgen import canvas

def create_docx(text: str, path: str):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(path)

def create_pdf(text: str, path: str):
    c = canvas.Canvas(path)
    text = text[:3000]  # PDF safety
    c.drawString(40, 800, text)
    c.save()
