"""Gemini-backed HeritageAI text-to-speech service."""

from __future__ import annotations

import time

from google import genai
from google.genai import errors
from google.genai import types

from app.core.config import settings

from .contract import TTSResult


class TTSQuotaExceededError(RuntimeError):
    """Raised when Gemini TTS quota has been exhausted."""


class TTSProviderError(RuntimeError):
    """Raised when Gemini TTS fails for a non-quota provider reason."""


class TTSService:
    """Convert HeritageAI answer text into speech audio."""

    DEFAULT_MODEL = "gemini-2.5-flash-preview-tts"
    DEFAULT_VOICE = "Kore"

    SAMPLE_RATE = 24000

    MAX_TRANSIENT_RETRIES = 3
    TRANSIENT_RETRY_DELAY_SECONDS = 3

    def __init__(self) -> None:
        api_key = getattr(
            settings,
            "GEMINI_API_KEY",
            None,
        )

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key,
        )

        self.model = getattr(
            settings,
            "GEMINI_TTS_MODEL",
            self.DEFAULT_MODEL,
        )

        self.voice = getattr(
            settings,
            "GEMINI_TTS_VOICE",
            self.DEFAULT_VOICE,
        )

    def synthesize(
        self,
        text: str,
    ) -> TTSResult:
        """Generate speech audio from text."""

        normalized_text = text.strip()

        if not normalized_text:
            raise ValueError(
                "Text cannot be empty."
            )

        last_error: Exception | None = None

        for attempt in range(
            1,
            self.MAX_TRANSIENT_RETRIES + 1,
        ):
            try:
                print(
                    "GEMINI TTS REQUEST:"
                    f" {attempt}/"
                    f"{self.MAX_TRANSIENT_RETRIES}"
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=normalized_text,
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=(
                                    types.PrebuiltVoiceConfig(
                                        voice_name=self.voice,
                                    )
                                )
                            )
                        ),
                    ),
                )

                return self._extract_audio(
                    response=response,
                )

            except errors.ServerError as exc:
                last_error = exc

                print(
                    "GEMINI TTS SERVER ERROR:"
                    f" type={type(exc).__name__}"
                    f" status={getattr(exc, 'status_code', None)}"
                    f" message={str(exc)}"
                )

                if attempt >= self.MAX_TRANSIENT_RETRIES:
                    raise RuntimeError(
                        "Gemini TTS provider is temporarily "
                        "unavailable after controlled retries."
                    ) from exc

                print(
                    "GEMINI TTS TRANSIENT ERROR:"
                    f" {getattr(exc, 'status_code', None)}"
                    f" ? retrying in "
                    f"{self.TRANSIENT_RETRY_DELAY_SECONDS}s"
                )

                time.sleep(
                    self.TRANSIENT_RETRY_DELAY_SECONDS
                )

            except errors.ClientError as exc:
                status_code = getattr(
                    exc,
                    "status_code",
                    None,
                )

                message = str(exc)

                print(
                    "GEMINI TTS CLIENT ERROR:"
                    f" type={type(exc).__name__}"
                    f" status={status_code}"
                    f" message={message}"
                )

                body = getattr(
                    exc,
                    "body",
                    None,
                )

                if body:
                    print(
                        "GEMINI TTS CLIENT ERROR BODY:",
                        body,
                    )

                if (
                    status_code == 429
                    or "RESOURCE_EXHAUSTED" in message
                    or "quota" in message.lower()
                ):
                    raise TTSQuotaExceededError(
                        "Gemini TTS quota is currently unavailable."
                    ) from exc

                raise TTSProviderError(
                    "Gemini TTS request was rejected by the provider."
                ) from exc

        raise RuntimeError(
            "Gemini TTS failed."
        ) from last_error

    def _extract_audio(
        self,
        response,
    ) -> TTSResult:
        """Extract PCM audio from a Gemini response."""

        candidates = getattr(
            response,
            "candidates",
            None,
        )

        if not candidates:
            raise RuntimeError(
                "Gemini returned no TTS candidates."
            )

        content = getattr(
            candidates[0],
            "content",
            None,
        )

        parts = getattr(
            content,
            "parts",
            None,
        )

        if not parts:
            raise RuntimeError(
                "Gemini returned no TTS content."
            )

        for part in parts:
            inline_data = getattr(
                part,
                "inline_data",
                None,
            )

            if inline_data is None:
                continue

            data = getattr(
                inline_data,
                "data",
                None,
            )

            if data:
                return TTSResult(
                    audio_bytes=data,
                    mime_type="audio/pcm",
                    sample_rate=self.SAMPLE_RATE,
                )

        raise RuntimeError(
            "Gemini returned no audio data."
        )

    def close(self) -> None:
        """Release the Gemini client when supported."""

        client = self.client

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
