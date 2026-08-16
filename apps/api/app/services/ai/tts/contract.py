"""Contracts for the HeritageAI text-to-speech service."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TTSResult:
    """Generated speech audio."""

    audio_bytes: bytes
    mime_type: str
    sample_rate: int
