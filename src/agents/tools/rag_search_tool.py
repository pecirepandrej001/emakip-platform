from src.rag.retriever import HybridRetriever

async def rag_search(query: str) -> list[dict]:
    return await HybridRetriever().retrieve(query)
