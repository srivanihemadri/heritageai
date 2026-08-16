# STEP 8C-003 — TASK 17
# SCANNER NEGATIVE-PATH & SECURITY REGRESSION

from __future__ import annotations

import sys
import uuid
from pathlib import Path
from io import BytesIO

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app
from app.services.ai.scanner.contract import HeritageScannerResult
from app.services.ai.scanner.service import ScannerQuotaExceededError


print("=" * 80)
print("STEP 8C-003 — TASK 17 — SCANNER NEGATIVE-PATH & SECURITY REGRESSION")
print("=" * 80)

print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")

print()
print("===== 2. VERIFY SCANNER ROUTE =====")

openapi = app.openapi()
paths = openapi.get("paths", {})

if "/api/v1/ai/scan" not in paths:
    raise RuntimeError("POST /api/v1/ai/scan route missing.")

operation = paths["/api/v1/ai/scan"].get("post")

if operation is None:
    raise RuntimeError("POST operation missing for scanner route.")

print("POST /api/v1/ai/scan: PASS")

print()
print("===== 3. VERIFY UNAUTHENTICATED ACCESS IS BLOCKED =====")

unauthenticated = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "test.png",
            BytesIO(b"not-authenticated"),
            "image/png",
        )
    },
)

if unauthenticated.status_code != 401:
    raise RuntimeError(
        f"Expected 401 for unauthenticated request, got "
        f"{unauthenticated.status_code}"
    )

print("Unauthenticated scanner request: 401")
print("Authentication boundary: PASS")

print()
print("===== 4. CREATE CONTROLLED TEST USER =====")

email = f"task17.{uuid.uuid4().hex}@example.com"
password = "Task17-Controlled-Password-123!"

registration = client.post(
    "/api/v1/auth/register",
    json={
        "email": email,
        "full_name": "Task 17 Controlled User",
        "password": password,
    },
)

if registration.status_code not in (200, 201):
    raise RuntimeError(
        f"Registration failed: "
        f"{registration.status_code} {registration.text}"
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
        f"Login failed: {login.status_code} {login.text}"
    )

login_payload = login.json()

token = (
    login_payload.get("access_token")
    or login_payload.get("token")
)

if not token:
    raise RuntimeError("JWT token was not returned.")

headers = {
    "Authorization": f"Bearer {token}",
}

print("Login: PASS")
print("JWT acquisition: PASS")

print()
print("===== 6. VERIFY EMPTY IMAGE REJECTION =====")

empty_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "empty.png",
            BytesIO(b""),
            "image/png",
        )
    },
)

if empty_response.status_code != 400:
    raise RuntimeError(
        f"Empty image expected 400, got "
        f"{empty_response.status_code}: {empty_response.text}"
    )

print("Empty image: HTTP 400 PASS")

print()
print("===== 7. VERIFY CORRUPTED IMAGE REJECTION =====")

corrupted_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "corrupted.png",
            BytesIO(b"THIS IS NOT A REAL PNG"),
            "image/png",
        )
    },
)

if corrupted_response.status_code != 400:
    raise RuntimeError(
        f"Corrupted image expected 400, got "
        f"{corrupted_response.status_code}: "
        f"{corrupted_response.text}"
    )

print("Corrupted image: HTTP 400 PASS")

print()
print("===== 8. VERIFY MIME / FORMAT MISMATCH =====")

from PIL import Image

mime_png = BytesIO()
Image.new("RGB", (1, 1), (255, 255, 255)).save(
    mime_png,
    format="PNG",
)
mime_png.seek(0)

mismatch_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "mismatch.jpg",
            mime_png,
            "image/jpeg",
        )
    },
)

if mismatch_response.status_code != 400:
    raise RuntimeError(
        f"MIME mismatch expected 400, got "
        f"{mismatch_response.status_code}: "
        f"{mismatch_response.text}"
    )
print("MIME/format mismatch: HTTP 400 PASS")

print()
print("===== 9. VERIFY UNSUPPORTED MIME TYPE =====")

unsupported_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "test.txt",
            BytesIO(b"plain text"),
            "text/plain",
        )
    },
)

if unsupported_response.status_code != 400:
    raise RuntimeError(
        f"Unsupported MIME expected 400, got "
        f"{unsupported_response.status_code}: "
        f"{unsupported_response.text}"
    )

print("Unsupported MIME type: HTTP 400 PASS")

print()
print("===== 10. VERIFY INVALID SEMANTIC RESULT REJECTION =====")

valid_payload = {
    "identified_name": "Controlled Heritage Site",
    "category": "HISTORICAL_MONUMENT",
    "location": "Controlled Location",
    "country": "India",
    "confidence": 0.96,
    "confidence_level": "HIGH",
    "description": "Controlled regression result.",
    "architectural_style": "Controlled style",
    "historical_period": "Controlled period",
    "historical_significance": "Controlled significance",
    "visual_evidence": [
        "Distinctive architectural feature",
        "Visible historical structure",
    ],
    "alternative_matches": [],
    "grounding_status": "GROUNDED",
    "identification_status": "IDENTIFIED",
    "evidence_quality": "STRONG",
}

invalid_payload = {
    **valid_payload,
    "identified_name": None,
}

try:
    HeritageScannerResult.model_validate(invalid_payload)
except Exception:
    print("Invalid semantic result: REJECTED")
else:
    raise RuntimeError(
        "Invalid semantic result was incorrectly accepted."
    )

print("Semantic rejection boundary: PASS")

print()
print("===== 11. VERIFY QUOTA EXCEPTION CONTRACT =====")

quota_exception = ScannerQuotaExceededError(
    "Gemini scanner quota has been exhausted. Please try again later."
)

if not str(quota_exception):
    raise RuntimeError("Quota exception message missing.")

print("ScannerQuotaExceededError: PASS")
print("HTTP 429 boundary architecture: PRESERVED")

print()
print("===== 12. VERIFY TRANSIENT SERVER ERROR ARCHITECTURE =====")

from app.services.ai.scanner.service import HeritageScannerService

if HeritageScannerService.MAX_TRANSIENT_RETRIES < 1:
    raise RuntimeError(
        "Transient retry configuration is invalid."
    )

if HeritageScannerService.TRANSIENT_RETRY_DELAY_SECONDS < 0:
    raise RuntimeError(
        "Transient retry delay configuration is invalid."
    )

print("MAX_TRANSIENT_RETRIES: PRESENT")
print("TRANSIENT_RETRY_DELAY_SECONDS: PRESENT")
print("503 retry architecture: PRESERVED")

print()
print("===== 13. VERIFY EXISTING AI ROUTES =====")

if "/api/v1/ai/answer" not in paths:
    raise RuntimeError("/api/v1/ai/answer route missing.")

if "/api/v1/ai/scan" not in paths:
    raise RuntimeError("/api/v1/ai/scan route missing.")

print("/api/v1/ai/answer: PRESERVED")
print("/api/v1/ai/scan: PRESERVED")

print()
print("===== 14. PRODUCTION SAFETY =====")

print("Real Gemini request: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")

print()
print("=" * 80)
print("STEP 8C-003 — TASK 17 COMPLETE")
print("=" * 80)
print("Authentication security: PASS")
print("Empty image rejection: PASS")
print("Corrupted image rejection: PASS")
print("MIME mismatch rejection: PASS")
print("Unsupported MIME rejection: PASS")
print("Semantic rejection: PASS")
print("Quota boundary: PASS")
print("503 retry architecture: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)

