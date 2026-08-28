from abc import ABC, abstractmethod

class VectorStore(ABC):
    @abstractmethod
    async def ensure_collection(self) -> None: ...

    @abstractmethod
    async def upsert(self, points: list[dict]) -> None: ...

    @abstractmethod
    async def search(self, vector: list[float], limit: int = 8) -> list[dict]: ...
