"""Validation helpers for uploaded voice audio."""

from __future__ import annotations


SUPPORTED_AUDIO_TYPES = {
    "audio/wav",
    "audio/x-wav",
    "audio/mpeg",
    "audio/mp3",
    "audio/webm",
    "audio/ogg",
    "audio/mp4",
    "audio/aac",
}


MAX_AUDIO_BYTES = 10 * 1024 * 1024


class VoiceAudioValidationError(ValueError):
    """Raised when uploaded voice audio is invalid."""


def validate_audio(
    audio_bytes: bytes,
    content_type: str,
) -> None:

    if not audio_bytes:
        raise VoiceAudioValidationError(
            "Audio file is empty."
        )

    if len(audio_bytes) > MAX_AUDIO_BYTES:
        raise VoiceAudioValidationError(
            "Audio file exceeds the 10 MB limit."
        )

    normalized = content_type.lower().strip()

    if normalized not in SUPPORTED_AUDIO_TYPES:
        raise VoiceAudioValidationError(
            "Unsupported audio format."
        )
