from pathlib import Path
import fitz

def extract_pdf_tables_as_text(path: str | Path) -> list[str]:
    results: list[str] = []
    doc = fitz.open(str(path))
    for page in doc:
        finder = getattr(page, "find_tables", None)
        if not finder:
            continue
        for table in page.find_tables().tables:
            rows = table.extract()
            results.append("\n".join(" | ".join(str(c or "") for c in row) for row in rows))
    return results
