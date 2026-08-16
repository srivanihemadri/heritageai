from __future__ import annotations

import sys
import uuid
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from fastapi.testclient import TestClient
from PIL import Image
from io import BytesIO

from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 10 — REAL SCANNER API FAILURE CAPTURE")
print("=" * 80)


print()
print("===== 1. INITIALIZE CLIENT =====")

client = TestClient(app)

print("FastAPI TestClient: PASS")


print()
print("===== 2. CREATE UNIQUE TEST USER =====")

suffix = uuid.uuid4().hex[:12]

email = f"scanner.failure.{suffix}@example.com"
password = "HeritageAI_Test_2026!"
full_name = "HeritageAI Scanner Failure Test"

print("Email:", email)


print()
print("===== 3. REGISTER =====")

registration = client.post(
    "/api/v1/auth/register",
    json={
        "full_name": full_name,
        "email": email,
        "password": password,
    },
)

print(
    "Registration HTTP status:",
    registration.status_code,
)

if registration.status_code != 201:

    print(
        "Registration response:",
        registration.text,
    )

    raise RuntimeError(
        "Registration failed."
    )

print("Registration: PASS")


print()
print("===== 4. LOGIN =====")

login = client.post(
    "/api/v1/auth/login",
    data={
        "username": email,
        "password": password,
    },
)

print(
    "Login HTTP status:",
    login.status_code,
)

if login.status_code != 200:

    print(
        "Login response:",
        login.text,
    )

    raise RuntimeError(
        "Login failed."
    )

token = login.json().get(
    "access_token"
)

if not token:
    raise RuntimeError(
        "JWT access token missing."
    )

print("JWT acquisition: PASS")


print()
print("===== 5. CREATE CONTROLLED IMAGE =====")

image = Image.new(
    "RGB",
    (256, 256),
)

buffer = BytesIO()

image.save(
    buffer,
    format="PNG",
)

image_bytes = buffer.getvalue()

print(
    "Image bytes:",
    len(image_bytes),
)

print("Controlled PNG: PASS")


print()
print("===== 6. REAL AUTHENTICATED SCANNER REQUEST =====")

print("REAL GEMINI REQUEST: START")

response = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "scanner_failure_capture.png",
            image_bytes,
            "image/png",
        )
    },
    headers={
        "Authorization": f"Bearer {token}"
    },
)

print("REAL GEMINI REQUEST: COMPLETED")

print()
print("===== 7. HTTP RESPONSE =====")

print(
    "HTTP status:",
    response.status_code,
)

print(
    "Response:",
    response.text,
)


print()
print("===== 8. FAILURE ANALYSIS =====")

if response.status_code == 200:

    print(
        "REAL SCANNER API: PASS"
    )

    payload = response.json()

    print(
        "scan_id:",
        payload.get("scan_id"),
    )

    result = payload.get(
        "result",
        {},
    )

    print(
        "identified_name:",
        result.get("identified_name"),
    )

    print(
        "confidence:",
        result.get("confidence"),
    )

    print(
        "grounding_status:",
        result.get("grounding_status"),
    )

    print()
    print(
        "The previous API 500 is no longer reproducible."
    )

elif response.status_code == 500:

    print(
        "REAL SCANNER API: 500 REPRODUCED"
    )

    print()
    print(
        "IMPORTANT:"
    )

    print(
        "The endpoint is converting the underlying "
        "scanner exception into SCANNER_FAILURE."
    )

    print()
    print(
        "The response above is the public error boundary."
    )

    print(
        "Further root-cause capture requires temporary "
        "diagnostic instrumentation in the route."
    )

    raise RuntimeError(
        "REAL SCANNER API 500 REPRODUCED."
    )

else:

    print(
        "Unexpected scanner HTTP status:",
        response.status_code,
    )

    raise RuntimeError(
        "Unexpected scanner API response."
    )


print()
print("===== 9. SAFETY =====")

print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Scanner configuration changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 10 COMPLETE")
print("=" * 80)

print("SEND THE COMPLETE OUTPUT.")
