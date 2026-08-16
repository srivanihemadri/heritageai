from sqlalchemy import text

from app.db.session import SessionLocal
from app.services.ai.embedding import GeminiEmbeddingService
from app.services.ai.retrieval.contract import (
    RetrievalEvidence,
    RetrievalResponse,
)
from app.services.ai.vector import QdrantVectorRepository


class RAGRetrievalService:

    def __init__(
        self,
        embedding_service: GeminiEmbeddingService | None = None,
        qdrant_repository: QdrantVectorRepository | None = None,
    ) -> None:

        self.embedding_service = (
            embedding_service
            or GeminiEmbeddingService()
        )

        self.qdrant = (
            qdrant_repository
            or QdrantVectorRepository()
        )


    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> RetrievalResponse:

        normalized_query = query.strip()

        if not normalized_query:
            raise ValueError(
                "Retrieval query cannot be empty."
            )

        if top_k < 1:
            raise ValueError(
                "top_k must be at least 1."
            )

        if top_k > 20:
            raise ValueError(
                "top_k cannot exceed 20."
            )


        query_vector = (
            self.embedding_service.embed_document(
                normalized_query
            )
        )


        if len(query_vector) != 768:
            raise RuntimeError(
                "Query embedding dimension mismatch."
            )


        points = self.qdrant.client.query_points(
            collection_name="heritageai_knowledge",
            query=query_vector,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        ).points


        if not points:
            return RetrievalResponse(
                query=normalized_query,
                top_k=top_k,
                results=[],
            )


        chunk_ids = [
            str(point.payload["chunk_id"])
            for point in points
            if point.payload
            and point.payload.get("chunk_id")
        ]


        if not chunk_ids:
            return RetrievalResponse(
                query=normalized_query,
                top_k=top_k,
                results=[],
            )


        db = SessionLocal()

        try:

            placeholders = ", ".join(
                f":chunk_{index}"
                for index in range(len(chunk_ids))
            )

            parameters = {
                f"chunk_{index}": chunk_id
                for index, chunk_id in enumerate(chunk_ids)
            }


            rows = db.execute(
                text(
                    f"""
                    SELECT
                        c.id AS chunk_id,
                        c.document_id,
                        c.content,

                        d.site_id,
                        d.source_id,
                        d.document_type,
                        d.title,
                        d.language,
                        d.provenance_level,
                        d.is_verified

                    FROM ai_knowledge_chunks c

                    INNER JOIN ai_knowledge_documents d
                        ON d.id = c.document_id

                    WHERE c.id IN ({placeholders})
                      AND c.is_active = 1
                      AND d.is_active = 1
                    """
                ),
                parameters,
            ).mappings().all()


            row_by_chunk_id = {
                str(row["chunk_id"]): row
                for row in rows
            }


            evidence = []


            for rank, point in enumerate(
                points,
                start=1,
            ):

                payload = point.payload or {}

                chunk_id = payload.get(
                    "chunk_id"
                )

                if not chunk_id:
                    continue


                row = row_by_chunk_id.get(
                    str(chunk_id)
                )

                if row is None:
                    continue


                evidence.append(
                    RetrievalEvidence(
                        rank=rank,
                        chunk_id=str(
                            row["chunk_id"]
                        ),
                        document_id=str(
                            row["document_id"]
                        ),
                        document_type=str(
                            row["document_type"]
                        ),
                        title=str(
                            row["title"]
                        ),
                        content=str(
                            row["content"]
                        ),
                        similarity_score=float(
                            point.score
                        ),
                        provenance_level=str(
                            row["provenance_level"]
                        ),
                        language=str(
                            row["language"]
                        ),
                        is_verified=bool(
                            row["is_verified"]
                        ),
                        site_id=str(
                            row["site_id"]
                        ),
                        source_id=(
                            str(row["source_id"])
                            if row["source_id"]
                            else None
                        ),
                    )
                )


            return RetrievalResponse(
                query=normalized_query,
                top_k=top_k,
                results=evidence,
            )

        finally:

            db.close()


    def close(self) -> None:

        self.qdrant.close()
