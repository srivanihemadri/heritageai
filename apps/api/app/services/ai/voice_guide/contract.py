"""Contracts for the HeritageAI Voice Guide orchestration service."""

from __future__ import annotations

from dataclasses import dataclass

from app.services.ai.generation.contract import AnswerSource


@dataclass(frozen=True)
class VoiceGuideResult:
    """Complete result produced by the HeritageAI Voice Guide."""

    transcript: str
    language: str | None
    confidence: float | None

    answer: str
    grounded: bool
    sources: list[AnswerSource]

    audio_bytes: bytes | None
    audio_mime_type: str | None
    audio_sample_rate: int | None

    tts_available: bool
    tts_fallback_reason: str | None
