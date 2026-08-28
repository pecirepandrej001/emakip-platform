from functools import lru_cache
from sentence_transformers import CrossEncoder
from src.core.config import get_settings

@lru_cache(maxsize=1)
def get_reranker() -> CrossEncoder:
    return CrossEncoder(get_settings().reranker_model)

def rerank(query: str, documents: list[dict], top_k: int | None = None) -> list[dict]:
    if not documents:
        return []
    top_k = top_k or get_settings().rerank_top_k
    pairs = [(query, str(doc["text"])) for doc in documents]
    scores = get_reranker().predict(pairs)
    ranked = []
    for doc, score in zip(documents, scores, strict=True):
        ranked.append({**doc, "rerank_score": float(score)})
    return sorted(ranked, key=lambda item: item["rerank_score"], reverse=True)[:top_k]
