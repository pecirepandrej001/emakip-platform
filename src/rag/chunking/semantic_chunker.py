from src.rag.chunking.recursive_chunker import recursive_chunk

def semantic_chunk(text: str, chunk_size: int = 700, overlap: int = 100) -> list[str]:
    # Lightweight deterministic fallback. In production this boundary detector can be
    # replaced with embedding-similarity segmentation without changing callers.
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buffer = ""
    for paragraph in paragraphs:
        candidate = f"{buffer}\n\n{paragraph}".strip()
        if len(candidate) <= chunk_size:
            buffer = candidate
        else:
            if buffer:
                chunks.extend(recursive_chunk(buffer, chunk_size, overlap))
            buffer = paragraph
    if buffer:
        chunks.extend(recursive_chunk(buffer, chunk_size, overlap))
    return chunks
