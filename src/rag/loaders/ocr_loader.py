from pathlib import Path
from PIL import Image

def load_image_text(path: str | Path) -> str:
    try:
        import pytesseract
    except ImportError as exc:
        raise RuntimeError("OCR support requires optional package `pytesseract`.") from exc
    return pytesseract.image_to_string(Image.open(path))
