from pathlib import Path

def extract_metadata(path: str | Path, text: str) -> dict[str, str | int]:
    file_path = Path(path)
    return {
        "filename": file_path.name,
        "extension": file_path.suffix.lower(),
        "character_count": len(text),
        "word_count": len(text.split()),
    }
