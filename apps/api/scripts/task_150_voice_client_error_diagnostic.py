from pathlib import Path
import uuid
import traceback

from fastapi.testclient import TestClient

from app.main import app

AUDIO = Path("scripts") / "ai_voice_controlled_test.wav"

print("=" * 80)
print("TASK 150 — EXACT GEMINI VOICE CLIENTERROR DIAGNOSTIC")
print("=" * 80)

if not AUDIO.exists():
    raise RuntimeError("Controlled speech audio missing.")

audio_bytes = AUDIO.read_bytes()

client = TestClient(app)

email = f"voice_diag_{uuid.uuid4().hex[:12]}@heritageai.dev"
password = "VoiceRuntime123!"

print()
print("===== 1. TEMPORARY USER =====")

register = client.post(
    "/api/v1/auth/register",
    json={
        "full_name": "HeritageAI Voice Diagnostic",
        "email": email,
        "password": password,
    },
)

if register.status_code not in (200, 201):
    raise RuntimeError(
        f"Registration failed: {register.status_code} {register.text}"
    )

login = client.post(
    "/api/v1/auth/login",
    data={
        "username": email,
        "password": password,
    },
)

if login.status_code != 200:
    raise RuntimeError(
        f"Login failed: {login.status_code} {login.text}"
    )

token = login.json()["access_token"]

print("Authentication: PASS")

print()
print("===== 2. REAL GEMINI VOICE REQUEST =====")
print("Gemini request: START")

try:
    response = client.post(
        "/api/v1/ai/voice",
        headers={
            "Authorization": f"Bearer {token}",
        },
        files={
            "file": (
                "ai_voice_controlled_test.wav",
                audio_bytes,
                "audio/wav",
            )
        },
    )

    print("HTTP status:", response.status_code)

    if response.status_code == 200:
        print("Voice request: PASS")
        print("Unexpectedly successful diagnostic.")
    else:
        print()
        print("===== 3. API FAILURE =====")
        print("Response status:", response.status_code)
        print("Response body:", response.text)

except Exception as exc:
    print()
    print("===== 3. EXACT CLIENT ERROR =====")
    print("Exception type:", type(exc).__name__)
    print("Exception message:", str(exc))
    print()
    traceback.print_exc()

finally:
    print()
    print("===== 4. CLEANUP =====")

    try:
        from app.db.session import SessionLocal
        from app.models.user import User

        db = SessionLocal()

        try:
            user = (
                db.query(User)
                .filter(User.email == email)
                .first()
            )

            if user:
                db.delete(user)
                db.commit()
                print("Temporary user removed: PASS")
            else:
                print("Temporary user already absent: PASS")

        finally:
            db.close()

    except Exception as cleanup_exc:
        print(
            "Cleanup warning:",
            type(cleanup_exc).__name__,
            str(cleanup_exc),
        )

print()
print("=" * 80)
print("TASK 150 DIAGNOSTIC COMPLETE")
print("=" * 80)
print("NO APPLICATION SOURCE CHANGES")
print("NO DATABASE SCHEMA CHANGES")
print("NO QDRANT CHANGES")
print("NO EMBEDDINGS")
print("NO CREDENTIALS LOGGED")
print("NO RAW AUDIO LOGGED")
print("=" * 80)
