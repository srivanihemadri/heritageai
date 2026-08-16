from dataclasses import dataclass
from typing import Any

from app.services.ai.embedding import EmbeddingProvider
from app.services.ai.vector import QdrantVectorRepository


@dataclass(frozen=True)
class EmbeddingResult:
    chunk_id: str
    dimensions: int
    provider: str
    model: str


class EmbeddingPipeline:
    """
    Coordinates embedding generation and vector persistence.

    Database registry writes are intentionally kept outside this
    first service implementation. The pipeline therefore provides
    the Qdrant boundary without prematurely mutating MySQL.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_repository: QdrantVectorRepository,
    ) -> None:

        self.embedding_provider = embedding_provider
        self.vector_repository = vector_repository

    def prepare_vector(
        self,
        chunk_id: str,
        content: str,
        payload: dict[str, Any],
    ) -> EmbeddingResult:

        vector = self.embedding_provider.embed_document(
            content,
        )

        self.vector_repository.upsert(
            point_id=chunk_id,
            vector=vector,
            payload=payload,
        )

        return EmbeddingResult(
            chunk_id=chunk_id,
            dimensions=len(vector),
            provider="google",
            model="gemini-embedding-001",
        )
