from qdrant_client import AsyncQdrantClient, models
from src.core.config import get_settings
from src.rag.embeddings.hf_embeddings import embedding_dimension
from src.rag.vector_store.base import VectorStore

class QdrantVectorStore(VectorStore):
    def __init__(self) -> None:
        settings = get_settings()
        self.client = AsyncQdrantClient(url=settings.qdrant_url)
        self.collection = settings.qdrant_collection

    async def ensure_collection(self) -> None:
        collections = await self.client.get_collections()
        if self.collection not in {c.name for c in collections.collections}:
            await self.client.create_collection(
                collection_name=self.collection,
                vectors_config=models.VectorParams(
                    size=embedding_dimension(),
                    distance=models.Distance.COSINE,
                ),
            )

    async def upsert(self, points: list[dict]) -> None:
        await self.ensure_collection()
        qpoints = [
            models.PointStruct(id=p["id"], vector=p["vector"], payload=p["payload"])
            for p in points
        ]
        await self.client.upsert(collection_name=self.collection, points=qpoints, wait=True)

    async def search(self, vector: list[float], limit: int = 8) -> list[dict]:
        await self.ensure_collection()
        response = await self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit,
            with_payload=True,
        )
        return [
            {"id": str(point.id), "score": float(point.score), "payload": point.payload or {}}
            for point in response.points
        ]

    async def delete_document(self, document_id: int) -> None:
        await self.ensure_collection()
        await self.client.delete(
            collection_name=self.collection,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(value=document_id),
                    )]
                )
            ),
            wait=True,
        )
