import pytest
from src.rag.vector_store.qdrant_client import QdrantVectorStore

@pytest.mark.asyncio
@pytest.mark.integration
async def test_vector_store_constructs():
    store = QdrantVectorStore()
    assert store.collection
