from pathlib import Path
import fitz

def load_pdf(path: str | Path) -> str:
    document = fitz.open(str(path))
    return "\n\n".join(page.get_text("text") for page in document)
