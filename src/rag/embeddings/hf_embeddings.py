from functools import lru_cache
from sentence_transformers import SentenceTransformer
from src.core.config import get_settings

@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(get_settings().embedding_model)

def embed_texts(texts: list[str]) -> list[list[float]]:
    vectors = get_embedding_model().encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()

def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]

def embedding_dimension() -> int:
    return int(get_embedding_model().get_sentence_embedding_dimension())
