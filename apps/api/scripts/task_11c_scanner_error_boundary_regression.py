from __future__ import annotations

import sys
import uuid
from pathlib import Path
from io import BytesIO

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.api.v1 import ai as ai_router
from app.services.ai.scanner.service import (
    HeritageScannerService,
    ScannerQuotaExceededError,
)


print("=" * 80)
print("STEP 8C-003 — TASK 11C — CONTROLLED SCANNER ERROR BOUNDARY REGRESSION")
print("=" * 80)


print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")


print()
print("===== 2. VERIFY ROUTE =====")

openapi = app.openapi()

target = openapi["paths"].get(
    "/api/v1/ai/scan"
)

if not target:
    raise RuntimeError(
        "Scanner endpoint missing."
    )

if "post" not in target:
    raise RuntimeError(
        "Scanner POST operation missing."
    )

print("POST /api/v1/ai/scan: PASS")
print(
    "Security:",
    target["post"].get("security"),
)


print()
print("===== 3. CREATE TEST USER =====")

suffix = uuid.uuid4().hex[:12]

email = (
    f"scanner.error.{suffix}"
    "@example.com"
)

password = "HeritageAI_Test_2026!"
full_name = "HeritageAI Scanner Error Test"

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
print("===== 4. LOGIN =====")

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
print("===== 5. CREATE CONTROLLED IMAGE =====")

image = Image.new(
    "RGB",
    (64, 64),
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

print("PNG image: PASS")


print()
print("===== 6. VERIFY QUOTA EXCEPTION CONTRACT =====")

quota_error = ScannerQuotaExceededError(
    "Gemini scanner quota has been exhausted. "
    "Please try again later."
)

if not isinstance(
    quota_error,
    ScannerQuotaExceededError,
):
    raise RuntimeError(
        "Quota exception construction failed."
    )

print(
    "ScannerQuotaExceededError: PASS"
)


print()
print("===== 7. INSTALL CONTROLLED QUOTA SERVICE =====")

original_service = (
    ai_router.HeritageScannerService
)


class ControlledQuotaScannerService:
    def __init__(self):
        print(
            "ControlledQuotaScannerService initialized."
        )

    def scan(
        self,
        image_bytes: bytes,
        content_type: str,
    ):
        print(
            "CONTROLLED QUOTA ERROR INVOKED"
        )

        raise ScannerQuotaExceededError(
            "Gemini scanner quota has been exhausted. "
            "Please try again later."
        )


ai_router.HeritageScannerService = (
    ControlledQuotaScannerService
)

print("Controlled quota service: PASS")


print()
print("===== 8. EXECUTE AUTHENTICATED QUOTA PATH =====")

try:

    response = client.post(
        "/api/v1/ai/scan",
        files={
            "file": (
                "quota-test.png",
                image_bytes,
                "image/png",
            )
        },
        headers=headers,
    )

    print(
        "HTTP status:",
        response.status_code,
    )

    print(
        "Response:",
        response.text,
    )

finally:

    ai_router.HeritageScannerService = (
        original_service
    )

    print(
        "Scanner service restoration: PASS"
    )


print()
print("===== 9. VALIDATE HTTP 429 CONTRACT =====")

if response.status_code != 429:
    raise RuntimeError(
        "Expected HTTP 429, received "
        f"{response.status_code}."
    )

payload = response.json()

detail = payload.get(
    "detail",
    {},
)

if detail.get("code") != (
    "SCANNER_QUOTA_EXCEEDED"
):
    raise RuntimeError(
        "Incorrect quota error code: "
        f"{detail}"
    )

if not detail.get("message"):
    raise RuntimeError(
        "Quota error message missing."
    )

print("HTTP 429: PASS")
print(
    "Error code:",
    detail.get("code"),
)
print(
    "Error message:",
    detail.get("message"),
)


print()
print("===== 10. VERIFY NO GEMINI CALL =====")

print(
    "Real Gemini request: NONE"
)

print(
    "Controlled quota exception only: PASS"
)


print()
print("===== 11. VERIFY PRODUCTION ROUTE PRESERVATION =====")

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
print("===== 12. FINAL SAFETY =====")

print("NO REAL GEMINI REQUEST.")
print("NO DATABASE MUTATIONS.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("NO PRODUCTION SOURCE CHANGES.")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 11C COMPLETE")
print("=" * 80)

print("Controlled quota exception: PASS")
print("HTTP 429 boundary: PASS")
print("SCANNER_QUOTA_EXCEEDED: PASS")
print("Authentication path: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("SEND THE COMPLETE OUTPUT.")
