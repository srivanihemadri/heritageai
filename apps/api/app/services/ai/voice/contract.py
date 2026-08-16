"""Contracts for the AI Voice feature."""

from __future__ import annotations

from pydantic import BaseModel, Field


class VoiceTranscriptionResult(BaseModel):
    """Structured speech-to-text result."""

    transcript: str = Field(
        min_length=1,
        max_length=10000,
    )

    language: str | None = None

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )


class VoiceResponse(BaseModel):
    """Public authenticated voice response."""

    success: bool = True

    result: VoiceTranscriptionResult
