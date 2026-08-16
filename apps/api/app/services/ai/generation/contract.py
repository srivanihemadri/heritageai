from dataclasses import dataclass


@dataclass(frozen=True)
class AnswerSource:
    rank: int
    chunk_id: str
    document_id: str
    title: str
    similarity_score: float
    provenance_level: str
    is_verified: bool


@dataclass(frozen=True)
class GroundedAnswer:
    query: str
    answer: str
    sources: list[AnswerSource]
    grounded: bool
