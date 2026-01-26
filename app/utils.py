from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def save_docx(text: str, path: str):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(path)

def save_pdf(text: str, path: str):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 40

    for line in text.split("\n"):
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(40, y, line[:120])
        y -= 14

    c.save()
