from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class GroundedAnswerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's heritage knowledge question.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum number of retrieval evidence items.",
    )


class GroundedAnswerSourceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rank: int = Field(ge=1)
    chunk_id: str
    document_id: str
    title: str
    similarity_score: float
    provenance_level: str
    is_verified: bool


class GroundedAnswerResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    answer: str
    sources: list[GroundedAnswerSourceResponse]
    grounded: bool


class GroundedAnswerErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detail: str
    code: str

class VoiceGuideResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool = True
    transcript: str
    language: str | None = None
    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )
    answer: str
    grounded: bool
    sources: list[GroundedAnswerSourceResponse]
    audio_url: str | None = None
    audio_mime_type: str | None = None
    audio_sample_rate: int | None = Field(
        default=None,
        ge=1,
    )
    tts_available: bool = True
    tts_fallback_reason: str | None = None

