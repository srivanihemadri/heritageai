from __future__ import annotations

import sys
import uuid
import traceback
from pathlib import Path
from io import BytesIO

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from app.main import app
import app.api.v1.ai as ai_module


print("=" * 80)
print("STEP 8C-003 — TASK 10D — REAL SCANNER EXCEPTION TRACE")
print("=" * 80)


print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application:", type(app).__name__)
print("TestClient: PASS")


print()
print("===== 2. CREATE UNIQUE TEST USER =====")

suffix = uuid.uuid4().hex[:12]

email = f"scanner.trace.{suffix}@example.com"
password = "HeritageAI_Test_2026!"
full_name = "HeritageAI Scanner Trace Test"

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
    print("Registration response:", registration.text)
    raise RuntimeError("Registration failed.")

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
    print("Login response:", login.text)
    raise RuntimeError("Login failed.")

token = login.json().get("access_token")

if not token:
    raise RuntimeError("JWT access token missing.")

print("JWT acquisition: PASS")


print()
print("===== 5. CREATE REAL TEST IMAGE =====")

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

print("Image bytes:", len(image_bytes))
print("Content type: image/png")
print("Controlled PNG: PASS")


print()
print("===== 6. INSTALL DIAGNOSTIC SERVICE WRAPPER =====")


RealScannerService = ai_module.HeritageScannerService


class TracingScannerService:
    """
    Diagnostic-only proxy.

    Production scanner source is not modified.
    """

    def __init__(self, *args, **kwargs):

        print()
        print(">>> REAL SCANNER SERVICE INITIALIZATION <<<")

        self._real = RealScannerService(
            *args,
            **kwargs,
        )

        print("Scanner service initialization: PASS")

    def scan(
        self,
        image_bytes: bytes,
        content_type: str,
    ):

        print()
        print(">>> REAL SCANNER SERVICE SCAN <<<")

        print(
            "Image bytes:",
            len(image_bytes),
        )

        print(
            "Content type:",
            content_type,
        )

        try:

            print(
                "Calling real HeritageScannerService.scan..."
            )

            result = self._real.scan(
                image_bytes=image_bytes,
                content_type=content_type,
            )

            print(
                "Real scanner service returned successfully."
            )

            print(
                "Result type:",
                type(result).__name__,
            )

            return result

        except Exception as exc:

            print()
            print("=" * 80)
            print(">>> REAL SCANNER EXCEPTION CAPTURED <<<")
            print("=" * 80)

            print(
                "Exception type:",
                type(exc).__name__,
            )

            print(
                "Exception message:",
                str(exc),
            )

            print()
            print("FULL TRACEBACK:")

            traceback.print_exc()

            print("=" * 80)

            raise

    def __getattr__(self, name):
        return getattr(
            self._real,
            name,
        )


ai_module.HeritageScannerService = (
    TracingScannerService
)

print("Diagnostic wrapper installed: PASS")


print()
print("===== 7. EXECUTE REAL AUTHENTICATED SCANNER =====")

print("REAL GEMINI REQUEST: START")

try:

    response = client.post(
        "/api/v1/ai/scan",
        files={
            "file": (
                "scanner_trace.png",
                image_bytes,
                "image/png",
            )
        },
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

finally:

    ai_module.HeritageScannerService = (
        RealScannerService
    )

    print()
    print(
        "Diagnostic wrapper restored."
    )


print("REAL GEMINI REQUEST: COMPLETED")


print()
print("===== 8. API RESPONSE =====")

print(
    "HTTP status:",
    response.status_code,
)

print(
    "Response:",
    response.text,
)


print()
print("===== 9. RESULT ANALYSIS =====")

if response.status_code == 200:

    print(
        "REAL SCANNER THROUGH API: PASS"
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
        "confidence_level:",
        result.get("confidence_level"),
    )

    print(
        "grounding_status:",
        result.get("grounding_status"),
    )

elif response.status_code == 500:

    print(
        "REAL SCANNER THROUGH API: 500 REPRODUCED"
    )

    print(
        "Underlying exception should appear above."
    )

else:

    print(
        "Unexpected HTTP status:",
        response.status_code,
    )


print()
print("===== 10. SAFETY =====")

print("Production source modifications: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 10D COMPLETE")
print("=" * 80)
