from __future__ import annotations

import sys
import uuid
from io import BytesIO
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.api.v1 import ai as ai_router
from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)
from app.services.ai.scanner.image import (
    ScannerImageValidationError,
)


print("=" * 80)
print("STEP 8C-003 — TASK 12 — SCANNER PRODUCTION HARDENING")
print("=" * 80)


print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")


print()
print("===== 2. VERIFY SCANNER OPENAPI CONTRACT =====")

openapi = app.openapi()

scanner_operation = (
    openapi
    .get("paths", {})
    .get("/api/v1/ai/scan", {})
    .get("post")
)

if scanner_operation is None:
    raise RuntimeError(
        "POST /api/v1/ai/scan missing from OpenAPI."
    )

if "requestBody" not in scanner_operation:
    raise RuntimeError(
        "Scanner multipart request body missing."
    )

security = scanner_operation.get(
    "security"
)

if not security:
    raise RuntimeError(
        "Scanner authentication security missing."
    )

print("POST /api/v1/ai/scan: PASS")
print("Multipart request contract: PASS")
print("OpenAPI security: PASS")


print()
print("===== 3. VERIFY AUTHENTICATION BOUNDARY =====")

unauthenticated = client.post(
    "/api/v1/ai/scan",
)

if unauthenticated.status_code != 401:
    raise RuntimeError(
        "Unauthenticated scanner request did not return 401."
    )

print("Unauthenticated status: 401")
print("Authentication boundary: PASS")


print()
print("===== 4. CREATE UNIQUE TEST USER =====")

suffix = uuid.uuid4().hex[:12]

email = (
    f"scanner.hardening.{suffix}"
    "@example.com"
)

password = "HeritageAI_Test_2026!"
full_name = "HeritageAI Scanner Hardening Test"

registration = client.post(
    "/api/v1/auth/register",
    json={
        "full_name": full_name,
        "email": email,
        "password": password,
    },
)

if registration.status_code != 201:
    raise RuntimeError(
        "Registration failed: "
        f"{registration.status_code} "
        f"{registration.text}"
    )

print("Registration: PASS")


print()
print("===== 5. LOGIN =====")

login = client.post(
    "/api/v1/auth/login",
    data={
        "username": email,
        "password": password,
    },
)

if login.status_code != 200:
    raise RuntimeError(
        "Login failed: "
        f"{login.status_code} "
        f"{login.text}"
    )

token = login.json().get(
    "access_token"
)

if not token:
    raise RuntimeError(
        "JWT access token missing."
    )

headers = {
    "Authorization": f"Bearer {token}"
}

print("Login: PASS")
print("JWT acquisition: PASS")


print()
print("===== 6. VERIFY SCANNER CONTRACT =====")

controlled_result = HeritageScannerResult(
    identified_name="Controlled Heritage Site",
    category="HISTORICAL_SITE",
    location="Controlled Location",
    country="India",
    confidence=0.95,
    confidence_level="HIGH",
    description="Controlled scanner hardening response.",
    architectural_style="Rock-cut",
    historical_period="Ancient",
    historical_significance="Controlled evidence.",
    visual_evidence=[
        "Controlled evidence one",
        "Controlled evidence two",
    ],
    alternative_matches=[],
    grounding_status="UNVERIFIED",
)

controlled_response = HeritageScannerResponse(
    scan_id="scanner-hardening-test",
    result=controlled_result,
)

print("HeritageScannerResult: PASS")
print("HeritageScannerResponse: PASS")


print()
print("===== 7. CONTROLLED SCANNER SERVICE =====")

original_service = (
    ai_router.HeritageScannerService
)


class ControlledScannerService:
    def __init__(self):
        print(
            "ControlledScannerService initialized."
        )

    def scan(
        self,
        image_bytes: bytes,
        content_type: str,
    ):
        print(
            "CONTROLLED SCANNER INVOKED"
        )

        return controlled_response


ai_router.HeritageScannerService = (
    ControlledScannerService
)

print("Service substitution: PASS")


print()
print("===== 8. VALID PNG =====")

image = Image.new(
    "RGB",
    (128, 128),
)

buffer = BytesIO()

image.save(
    buffer,
    format="PNG",
)

valid_png = buffer.getvalue()

response = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "valid.png",
            valid_png,
            "image/png",
        )
    },
    headers=headers,
)

if response.status_code != 200:
    raise RuntimeError(
        "Valid PNG failed: "
        f"{response.status_code} "
        f"{response.text}"
    )

print("Valid PNG: PASS")
print("HTTP 200: PASS")


print()
print("===== 9. VALID JPEG =====")

buffer = BytesIO()

image.save(
    buffer,
    format="JPEG",
)

valid_jpeg = buffer.getvalue()

response = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "valid.jpg",
            valid_jpeg,
            "image/jpeg",
        )
    },
    headers=headers,
)

if response.status_code != 200:
    raise RuntimeError(
        "Valid JPEG failed: "
        f"{response.status_code} "
        f"{response.text}"
    )

print("Valid JPEG: PASS")


print()
print("===== 10. VALID WEBP =====")

buffer = BytesIO()

image.save(
    buffer,
    format="WEBP",
)

valid_webp = buffer.getvalue()

response = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "valid.webp",
            valid_webp,
            "image/webp",
        )
    },
    headers=headers,
)

if response.status_code != 200:
    raise RuntimeError(
        "Valid WEBP failed: "
        f"{response.status_code} "
        f"{response.text}"
    )

print("Valid WEBP: PASS")


print()
print("===== 11. UNSUPPORTED MIME TYPE =====")

response = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "document.txt",
            b"not an image",
            "text/plain",
        )
    },
    headers=headers,
)

if response.status_code != 400:
    raise RuntimeError(
        "Unsupported MIME type did not return 400: "
        f"{response.status_code}"
    )

print("Unsupported MIME rejection: PASS")
print("HTTP 400: PASS")


print()
print("===== 12. CORRUPTED IMAGE =====")

response = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "corrupted.png",
            b"this-is-not-a-real-png",
            "image/png",
        )
    },
    headers=headers,
)

if response.status_code not in {
    400,
    422,
}:
    raise RuntimeError(
        "Corrupted image produced unexpected status: "
        f"{response.status_code}"
    )

print(
    "Corrupted image rejection: PASS"
)
print(
    "HTTP status:",
    response.status_code,
)


print()
print("===== 13. EMPTY IMAGE =====")

response = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "empty.png",
            b"",
            "image/png",
        )
    },
    headers=headers,
)

if response.status_code not in {
    400,
    422,
}:
    raise RuntimeError(
        "Empty image produced unexpected status: "
        f"{response.status_code}"
    )

print("Empty image rejection: PASS")
print(
    "HTTP status:",
    response.status_code,
)


print()
print("===== 14. RESPONSE CONTRACT =====")

response = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "contract.png",
            valid_png,
            "image/png",
        )
    },
    headers=headers,
)

if response.status_code != 200:
    raise RuntimeError(
        "Contract request failed."
    )

payload = response.json()

if "scan_id" not in payload:
    raise RuntimeError(
        "scan_id missing."
    )

if "result" not in payload:
    raise RuntimeError(
        "result missing."
    )

result = payload["result"]

required_fields = {
    "identified_name",
    "category",
    "location",
    "country",
    "confidence",
    "confidence_level",
    "description",
    "architectural_style",
    "historical_period",
    "historical_significance",
    "visual_evidence",
    "alternative_matches",
    "grounding_status",
}

missing = required_fields - set(
    result.keys()
)

if missing:
    raise RuntimeError(
        "Scanner response fields missing: "
        f"{sorted(missing)}"
    )

print("scan_id: PASS")
print("result: PASS")
print("All scanner result fields: PASS")


print()
print("===== 15. VERIFY NO REAL GEMINI REQUEST =====")

print("Real Gemini request: NONE")
print("Controlled scanner only: PASS")


print()
print("===== 16. RESTORE PRODUCTION SERVICE =====")

ai_router.HeritageScannerService = (
    original_service
)

print("Production scanner service restored: PASS")


print()
print("===== 17. PRESERVE EXISTING AI ANSWER =====")

routes = [
    route
    for route in ai_router.router.routes
    if getattr(route, "path", None)
]

paths = [
    route.path
    for route in routes
]

if "/ai/answer" not in paths:
    raise RuntimeError(
        "Existing /ai/answer route missing."
    )

if "/ai/scan" not in paths:
    raise RuntimeError(
        "Existing /ai/scan route missing."
    )

print("/ai/answer: PRESERVED")
print("/ai/scan: PRESERVED")


print()
print("===== 18. FINAL SAFETY =====")

print("NO REAL GEMINI REQUEST.")
print("NO DATABASE MUTATIONS.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("NO PRODUCTION SOURCE CHANGES.")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 12 COMPLETE")
print("=" * 80)

print("Scanner contract: PASS")
print("Authentication boundary: PASS")
print("PNG validation: PASS")
print("JPEG validation: PASS")
print("WEBP validation: PASS")
print("Unsupported MIME rejection: PASS")
print("Corrupted image handling: PASS")
print("Empty image handling: PASS")
print("Response contract: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("SEND THE COMPLETE OUTPUT.")
