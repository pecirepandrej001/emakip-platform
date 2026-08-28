from rank_bm25 import BM25Okapi
from src.core.config import get_settings
from src.core.telemetry import RAG_QUERIES
from src.rag.embeddings.hf_embeddings import embed_query
from src.rag.reranking.cross_encoder_reranker import rerank
from src.rag.vector_store.qdrant_client import QdrantVectorStore

class HybridRetriever:
    def __init__(self) -> None:
        self.store = QdrantVectorStore()

    async def retrieve(self, query: str) -> list[dict]:
        RAG_QUERIES.inc()
        settings = get_settings()
        vector_results = await self.store.search(embed_query(query), settings.top_k)
        docs = [
            {
                "id": item["id"],
                "text": str(item["payload"].get("text", "")),
                "filename": str(item["payload"].get("filename", "unknown")),
                "document_id": item["payload"].get("document_id"),
                "vector_score": item["score"],
            }
            for item in vector_results
            if item["payload"].get("text")
        ]
        if not docs:
            return []

        tokenized = [d["text"].lower().split() for d in docs]
        bm25 = BM25Okapi(tokenized)
        lexical_scores = bm25.get_scores(query.lower().split())

        max_lexical = max(float(max(lexical_scores)), 1.0)
        for doc, lexical in zip(docs, lexical_scores, strict=True):
            doc["lexical_score"] = float(lexical) / max_lexical
            doc["hybrid_score"] = 0.7 * doc["vector_score"] + 0.3 * doc["lexical_score"]

        candidates = sorted(docs, key=lambda d: d["hybrid_score"], reverse=True)
        try:
            return rerank(query, candidates, settings.rerank_top_k)
        except Exception:
            return candidates[: settings.rerank_top_k]
