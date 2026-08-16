from pathlib import Path
import traceback

from app.services.ai.voice.service import VoiceService

AUDIO = Path("scripts") / "ai_voice_controlled_test.wav"

print("=" * 80)
print("TASK 150 — DIRECT VOICE SERVICE CLIENTERROR DIAGNOSTIC")
print("=" * 80)

if not AUDIO.exists():
    raise RuntimeError("Controlled speech audio missing.")

audio_bytes = AUDIO.read_bytes()

print()
print("===== 1. AUDIO =====")
print("Audio:", AUDIO)
print("Bytes:", len(audio_bytes))
print("Audio: PASS")

service = None

try:
    print()
    print("===== 2. VOICE SERVICE =====")

    service = VoiceService()

    print("VoiceService initialization: PASS")
    print("Model:", service.model)

    print()
    print("===== 3. DIRECT GEMINI REQUEST =====")
    print("Calling VoiceService.transcribe() directly...")
    print("REAL GEMINI REQUEST: START")

    result = service.transcribe(
        audio_bytes=audio_bytes,
        content_type="audio/wav",
    )

    print()
    print("REAL GEMINI REQUEST: COMPLETED")
    print("Voice transcription: PASS")
    print()
    print("Result:")
    print(result.model_dump_json(indent=2))

except Exception as exc:

    print()
    print("=" * 80)
    print("EXACT GEMINI / VOICE SERVICE FAILURE")
    print("=" * 80)

    print("Exception type:")
    print(type(exc).__module__ + "." + type(exc).__name__)

    print()
    print("Exception message:")
    print(str(exc))

    print()
    print("Exception repr:")
    print(repr(exc))

    print()
    print("Full traceback:")
    traceback.print_exc()

finally:
    if service is not None:
        try:
            service.close()
        except Exception:
            pass

print()
print("=" * 80)
print("TASK 150 DIRECT DIAGNOSTIC COMPLETE")
print("=" * 80)
print("NO DATABASE MUTATION")
print("NO QDRANT CHANGES")
print("NO EMBEDDINGS")
print("NO SOURCE CHANGES")
print("=" * 80)
