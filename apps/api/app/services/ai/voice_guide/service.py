"""HeritageAI Voice Guide orchestration service."""

from app.services.ai.generation import GroundedAnswerService
from app.services.ai.tts import (
    TTSProviderError,
    TTSQuotaExceededError,
    TTSService,
)
from app.services.ai.voice import VoiceService

from .contract import VoiceGuideResult


class VoiceGuideService:
    """Orchestrate speech recognition, grounded answering, and TTS."""

    def __init__(self) -> None:
        self.voice_service = VoiceService()
        self.answer_service = GroundedAnswerService()
        self.tts_service = TTSService()

    def process(
        self,
        audio_bytes: bytes,
        content_type: str,
        top_k: int = 5,
    ) -> VoiceGuideResult:
        """Process voice input through the complete AI pipeline."""

        transcription = self.voice_service.transcribe(
            audio_bytes=audio_bytes,
            content_type=content_type,
        )

        grounded_answer = self.answer_service.answer(
            query=transcription.transcript,
            top_k=top_k,
        )

        audio_bytes_result: bytes | None = None
        audio_mime_type: str | None = None
        audio_sample_rate: int | None = None

        tts_available = False
        tts_fallback_reason: str | None = None

        try:
            tts_result = self.tts_service.synthesize(
                text=grounded_answer.answer,
            )

            audio_bytes_result = tts_result.audio_bytes
            audio_mime_type = tts_result.mime_type
            audio_sample_rate = tts_result.sample_rate
            tts_available = True

        except TTSQuotaExceededError:
            print(
                "VOICE GUIDE TTS FALLBACK:"
                " Gemini TTS quota unavailable."
            )

            tts_fallback_reason = "TTS_QUOTA_EXCEEDED"

        except TTSProviderError as exc:
            print(
                "VOICE GUIDE TTS FALLBACK:"
                f" provider error: {type(exc).__name__}"
            )

            tts_fallback_reason = "TTS_PROVIDER_ERROR"

        return VoiceGuideResult(
            transcript=transcription.transcript,
            language=transcription.language,
            confidence=transcription.confidence,
            answer=grounded_answer.answer,
            grounded=grounded_answer.grounded,
            sources=grounded_answer.sources,
            audio_bytes=audio_bytes_result,
            audio_mime_type=audio_mime_type,
            audio_sample_rate=audio_sample_rate,
            tts_available=tts_available,
            tts_fallback_reason=tts_fallback_reason,
        )

    def close(self) -> None:
        """Close all underlying AI services."""

        self.voice_service.close()
        self.answer_service.close()
        self.tts_service.close()
