from pathlib import Path
from docx import Document

def load_docx(path: str | Path) -> str:
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
