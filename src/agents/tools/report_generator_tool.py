from pathlib import Path
from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_excel(rows: list[dict], output_path: str) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_excel(path, index=False)
    return str(path)

def generate_pdf(title: str, paragraphs: list[str], output_path: str) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    y = height - 60
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, title)
    y -= 30
    pdf.setFont("Helvetica", 10)
    for paragraph in paragraphs:
        for line in _wrap(paragraph, 95):
            if y < 60:
                pdf.showPage()
                y = height - 60
                pdf.setFont("Helvetica", 10)
            pdf.drawString(50, y, line)
            y -= 14
        y -= 8
    pdf.save()
    return str(path)

def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines, current = [], []
    for word in words:
        candidate = " ".join(current + [word])
        if len(candidate) <= width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines
