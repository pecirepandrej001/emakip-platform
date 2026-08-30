from src.rag.chunking.recursive_chunker import recursive_chunk

def test_recursive_chunk_preserves_content():
    text = " ".join(["enterprise"] * 300)
    chunks = recursive_chunk(text, chunk_size=120, overlap=20)
    assert len(chunks) > 1
    assert all(len(c) <= 120 for c in chunks)
