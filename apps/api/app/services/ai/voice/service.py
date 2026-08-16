"""Gemini-backed AI Voice transcription service."""

from __future__ import annotations

import json

from app.core.config import settings

from .audio import validate_audio
from .contract import VoiceTranscriptionResult


class VoiceService:
    """Convert uploaded speech audio into structured text."""

    def __init__(self) -> None:
        self.client = None

        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "Gemini SDK is not available."
            ) from exc

        api_key = getattr(
            settings,
            "GEMINI_API_KEY",
            None,
        )

        if not api_key:
            raise RuntimeError(
                "Gemini API key is not configured."
            )

        self.client = genai.Client(
            api_key=api_key,
        )

        self.model = getattr(
            settings,
            "GEMINI_VOICE_MODEL",
            "gemini-3.6-flash",
        )

    def transcribe(
        self,
        audio_bytes: bytes,
        content_type: str,
    ) -> VoiceTranscriptionResult:

        validate_audio(
            audio_bytes=audio_bytes,
            content_type=content_type,
        )

        from google.genai import types

        prompt = """
Transcribe the supplied audio exactly.

Return ONLY the transcription result.

Rules:
- Transcribe only the spoken words.
- Do not answer questions contained in the audio.
- Do not invent words.
- Preserve the speaker's meaning.
- If speech is unclear, provide the best faithful transcription.
- Identify the spoken language when possible.
- Confidence must be between 0 and 1.
"""

        audio_part = types.Part.from_bytes(
            data=audio_bytes,
            mime_type=content_type,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                prompt,
                audio_part,
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VoiceTranscriptionResult,
            ),
        )

        text = getattr(
            response,
            "text",
            None,
        )

        if not text:
            raise ValueError(
                "Gemini returned an empty voice transcription."
            )

        cleaned = text.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.replace(
                "```json",
                "",
                1,
            )
            cleaned = cleaned.replace(
                "```",
                "",
                1,
            )
            cleaned = cleaned.strip()

        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Gemini returned invalid voice JSON."
            ) from exc

        return VoiceTranscriptionResult.model_validate(
            payload
        )

    def close(self) -> None:
        client = self.client

        if client is None:
            return

        close_method = getattr(
            client,
            "close",
            None,
        )

        if callable(close_method):
            try:
                close_method()
            except Exception:
                pass

