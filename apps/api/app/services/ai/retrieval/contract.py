from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalEvidence:
    rank: int
    chunk_id: str
    document_id: str
    document_type: str
    title: str
    content: str
    similarity_score: float
    provenance_level: str
    language: str
    is_verified: bool
    site_id: str
    site_name: str
    source_id: str | None


@dataclass(frozen=True)
class RetrievalResponse:
    query: str
    top_k: int
    results: list[RetrievalEvidence]

