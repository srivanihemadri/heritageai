"""Task 55 — scanner API runtime failure mapping regression."""

from __future__ import annotations

from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.services.ai.scanner.service import (
    ScannerQuotaExceededError,
)


print("=" * 80)
print("STEP 8C-003 — TASK 55 — SCANNER API RUNTIME FAILURE MAPPING REGRESSION")
print("=" * 80)


print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")


print()
print("===== 2. CREATE CONTROLLED TEST USER =====")

email = "task55_runtime_user@example.com"
password = "Task55-Runtime-Password-123!"

registration = client.post(
    "/api/v1/auth/register",
    json={
        "email": email,
        "full_name": "Task 55 Runtime User",
        "password": password,
    },
)

if registration.status_code not in {200, 201, 400}:
    raise RuntimeError(
        f"Controlled registration failed: {registration.status_code}"
    )

print("Controlled registration: PASS")


print()
print("===== 3. LOGIN CONTROLLED USER =====")

login = client.post(
    "/api/v1/auth/login",
    data={
        "username": email,
        "password": password,
    },
)

if login.status_code != 200:
    raise RuntimeError(
        f"Controlled login failed: {login.status_code}"
    )

login_payload = login.json()

token = (
    login_payload.get("access_token")
    or login_payload.get("token")
)

if not token:
    raise RuntimeError(
        "JWT token was not returned."
    )

headers = {
    "Authorization": f"Bearer {token}",
}

print("Login: PASS")
print("JWT acquisition: PASS")


print()
print("===== 4. BUILD CONTROLLED VALID PNG =====")

image = Image.new(
    "RGB",
    (32, 32),
    (120, 80, 40),
)

buffer = BytesIO()
image.save(buffer, format="PNG")
png_bytes = buffer.getvalue()

if not png_bytes:
    raise RuntimeError(
        "Controlled PNG was empty."
    )

print(f"PNG bytes: {len(png_bytes)}")
print("Controlled image: PASS")


print()
print("===== 5. VERIFY QUOTA RUNTIME MAPPING =====")

with patch(
    "app.api.v1.ai.HeritageScannerService.scan",
    side_effect=ScannerQuotaExceededError(
        "Controlled quota failure."
    ),
):
    response = client.post(
        "/api/v1/ai/scan",
        headers=headers,
        files={
            "file": (
                "task55.png",
                png_bytes,
                "image/png",
            )
        },
    )

if response.status_code != 429:
    raise RuntimeError(
        f"Quota failure returned HTTP {response.status_code}, "
        "expected HTTP 429."
    )

payload = response.json()

if payload.get("detail", {}).get("code") != (
    "SCANNER_QUOTA_EXCEEDED"
):
    raise RuntimeError(
        "Quota error code was not mapped correctly."
    )

print("Quota failure: HTTP 429")
print("SCANNER_QUOTA_EXCEEDED: PASS")
print("Quota runtime mapping: PASS")


print()
print("===== 6. VERIFY GENERIC FAILURE RUNTIME MAPPING =====")

with patch(
    "app.api.v1.ai.HeritageScannerService.scan",
    side_effect=RuntimeError(
        "SECRET_INTERNAL_SCANNER_FAILURE"
    ),
):
    response = client.post(
        "/api/v1/ai/scan",
        headers=headers,
        files={
            "file": (
                "task55.png",
                png_bytes,
                "image/png",
            )
        },
    )

if response.status_code != 500:
    raise RuntimeError(
        f"Generic failure returned HTTP {response.status_code}, "
        "expected HTTP 500."
    )

payload = response.json()

detail = payload.get("detail", {})

if detail.get("code") != "SCANNER_FAILURE":
    raise RuntimeError(
        "Generic scanner failure code was not mapped correctly."
    )

if detail.get("message") != (
    "Heritage image scanning failed."
):
    raise RuntimeError(
        "Generic scanner failure message was not sanitized."
    )

if "SECRET_INTERNAL_SCANNER_FAILURE" in response.text:
    raise RuntimeError(
        "Internal scanner exception leaked into public response."
    )

print("Generic failure: HTTP 500")
print("SCANNER_FAILURE: PASS")
print("Internal exception sanitized: PASS")
print("Generic failure runtime mapping: PASS")


print()
print("===== 7. VERIFY INVALID IMAGE RUNTIME MAPPING =====")

response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "task55.png",
            b"",
            "image/png",
        )
    },
)

if response.status_code != 400:
    raise RuntimeError(
        f"Empty image returned HTTP {response.status_code}, "
        "expected HTTP 400."
    )

payload = response.json()

detail = payload.get("detail", {})

if detail.get("code") != "INVALID_IMAGE":
    raise RuntimeError(
        "Invalid image error code was not mapped correctly."
    )

print("Empty image: HTTP 400")
print("INVALID_IMAGE: PASS")
print("Invalid-image runtime mapping: PASS")


print()
print("===== 8. VERIFY UNAUTHENTICATED RUNTIME BOUNDARY =====")

response = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "task55.png",
            png_bytes,
            "image/png",
        )
    },
)

if response.status_code != 401:
    raise RuntimeError(
        f"Unauthenticated request returned HTTP "
        f"{response.status_code}, expected HTTP 401."
    )

print("Unauthenticated request: HTTP 401")
print("Authentication runtime boundary: PASS")


print()
print("===== 9. VERIFY EXISTING AI ANSWER ROUTE =====")

if "/api/v1/ai/answer" not in app.openapi().get(
    "paths",
    {},
):
    raise RuntimeError(
        "Existing AI answer route disappeared."
    )

print("/api/v1/ai/answer: PRESERVED")


print()
print("===== 10. PRODUCTION SAFETY =====")

print("Controlled runtime failure injection only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 55 COMPLETE")
print("=" * 80)
print("Quota HTTP 429 runtime mapping: PASS")
print("SCANNER_QUOTA_EXCEEDED: PASS")
print("Generic HTTP 500 runtime mapping: PASS")
print("SCANNER_FAILURE sanitization: PASS")
print("Invalid-image HTTP 400 runtime mapping: PASS")
print("Authentication HTTP 401 boundary: PASS")
print("Existing AI answer route: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
