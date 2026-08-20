from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.core.config import settings


COLLECTION_NAME = "heritageai_knowledge"
VECTOR_SIZE = 768
DISTANCE = models.Distance.COSINE


def get_qdrant_path() -> Path:
    """
    Resolve the repository root and return the persistent
    local Qdrant storage directory.
    """

    project_root = Path(__file__).resolve().parents[5]

    return (
        project_root
        / "data"
        / "vector"
        / "qdrant"
    )


class QdrantVectorRepository:
    """
    Persistence boundary for HeritageAI semantic vectors.

    This repository owns Qdrant operations only.
    """

    def __init__(
        self,
        path: Path | None = None,
    ) -> None:

        if settings.QDRANT_URL:
            self.path = None
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
            )
        else:
            self.path = (
                path
                if path is not None
                else get_qdrant_path()
            )

            self.path.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.client = QdrantClient(
                path=str(self.path),
            )

        self._ensure_collection()

    def _ensure_collection(self) -> None:

        collections = [
            collection.name
            for collection
            in self.client.get_collections().collections
        ]

        if COLLECTION_NAME not in collections:

            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=VECTOR_SIZE,
                    distance=DISTANCE,
                ),
            )

            return

        info = self.client.get_collection(
            collection_name=COLLECTION_NAME,
        )

        vectors = info.config.params.vectors

        if vectors.size != VECTOR_SIZE:
            raise RuntimeError(
                "Qdrant collection dimension mismatch."
            )

        if vectors.distance != DISTANCE:
            raise RuntimeError(
                "Qdrant collection distance mismatch."
            )

    def upsert(
        self,
        point_id: str,
        vector: list[float],
        payload: dict[str, Any],
    ) -> None:

        if len(vector) != VECTOR_SIZE:
            raise ValueError(
                f"Expected {VECTOR_SIZE}-dimensional vector."
            )

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    def delete(
        self,
        point_id: str,
    ) -> None:

        self.client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=models.PointIdsList(
                points=[point_id],
            ),
        )

    def count(self) -> int:

        info = self.client.get_collection(
            collection_name=COLLECTION_NAME,
        )

        return info.points_count

    def close(self) -> None:
        self.client.close()

