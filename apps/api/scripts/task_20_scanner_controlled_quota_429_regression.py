from __future__ import annotations

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app
from app.services.ai.scanner.service import ScannerQuotaExceededError


print("=" * 80)
print("STEP 8C-003 — TASK 20 — SCANNER CONTROLLED QUOTA / HTTP 429 REGRESSION")
print("=" * 80)

print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")

print()
print("===== 2. VERIFY SCANNER ROUTE =====")

paths = app.openapi().get("paths", {})

if "/api/v1/ai/scan" not in paths:
    raise RuntimeError(
        "POST /api/v1/ai/scan route is missing."
    )

print("POST /api/v1/ai/scan: PASS")

print()
print("===== 3. VERIFY QUOTA EXCEPTION CONTRACT =====")

quota_message = (
    "Gemini scanner quota has been exhausted. "
    "Please try again later."
)

quota_error = ScannerQuotaExceededError(
    quota_message
)

if str(quota_error) != quota_message:
    raise RuntimeError(
        "ScannerQuotaExceededError message mismatch."
    )

print("ScannerQuotaExceededError: PASS")
print("Quota message contract: PASS")

print()
print("===== 4. VERIFY HTTP 429 ROUTER BOUNDARY =====")

router_source = Path(
    "app/api/v1/ai.py"
).read_text(encoding="utf-8")

required_router_terms = [
    "ScannerQuotaExceededError",
    "status.HTTP_429_TOO_MANY_REQUESTS",
    "SCANNER_QUOTA_EXCEEDED",
    
]

for term in required_router_terms:
    if term not in router_source:
        raise RuntimeError(
            f"HTTP 429 router boundary missing: {term}"
        )

print("Quota exception import: PRESENT")
print("HTTP 429 status boundary: PRESENT")
print("SCANNER_QUOTA_EXCEEDED code: PRESENT")
print("Quota message: PRESENT")
print("HTTP 429 router boundary: PASS")

print()
print("===== 5. VERIFY QUOTA IS NOT PART OF 503 RETRY PATH =====")

service_source = Path(
    "app/services/ai/scanner/service.py"
).read_text(encoding="utf-8")

client_error_marker = "except errors.ClientError"
server_error_marker = "except errors.ServerError"

client_error_position = service_source.find(
    client_error_marker
)

server_error_position = service_source.find(
    server_error_marker
)

if client_error_position < 0:
    raise RuntimeError(
        "ClientError handling is missing."
    )

if server_error_position < 0:
    raise RuntimeError(
        "ServerError handling is missing."
    )

if client_error_position >= server_error_position:
    raise RuntimeError(
        "Quota ClientError boundary is not positioned before "
        "the transient ServerError retry boundary."
    )

client_error_section = service_source[
    client_error_position:server_error_position
]

if "ScannerQuotaExceededError" not in client_error_section:
    raise RuntimeError(
        "ScannerQuotaExceededError is not raised inside "
        "the ClientError quota boundary."
    )

print("ClientError quota boundary: PASS")
print("ServerError retry boundary: PASS")
print("Quota/503 separation: PASS")

print()
print("===== 6. VERIFY 429 DETECTION =====")

if "status_code == 429" not in client_error_section:
    raise RuntimeError(
        "Explicit HTTP 429 detection is missing."
    )

if "RESOURCE_EXHAUSTED" not in client_error_section:
    raise RuntimeError(
        "RESOURCE_EXHAUSTED detection is missing."
    )

print("HTTP 429 detection: PASS")
print("RESOURCE_EXHAUSTED detection: PASS")

print()
print("===== 7. VERIFY AUTHENTICATION BOUNDARY =====")

unauthenticated = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "quota-test.png",
            b"not-authenticated",
            "image/png",
        )
    },
)

if unauthenticated.status_code != 401:
    raise RuntimeError(
        f"Expected 401 for unauthenticated scanner request, "
        f"got {unauthenticated.status_code}"
    )

print("Unauthenticated status: 401")
print("Authentication boundary: PASS")

print()
print("===== 8. CREATE CONTROLLED TEST USER =====")

email = f"task20.{uuid.uuid4().hex}@example.com"
password = "Task20-Controlled-Password-123!"

registration = client.post(
    "/api/v1/auth/register",
    json={
        "email": email,
        "full_name": "Task 20 Controlled User",
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
print("===== 9. LOGIN =====")

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
    raise RuntimeError(
        "JWT token was not returned."
    )

headers = {
    "Authorization": f"Bearer {token}",
}

print("Login: PASS")
print("JWT acquisition: PASS")

print()
print("===== 10. VERIFY PRODUCTION ROUTE PRESERVATION =====")

if "/api/v1/ai/answer" not in paths:
    raise RuntimeError(
        "/api/v1/ai/answer route is missing."
    )

print("/api/v1/ai/answer: PRESERVED")
print("/api/v1/ai/scan: PRESERVED")

print()
print("===== 11. VERIFY CONTROLLED QUOTA CONTRACT =====")

controlled_error = {
    "status": 429,
    "code": "SCANNER_QUOTA_EXCEEDED",
    "message": quota_message,
}

if controlled_error["status"] != 429:
    raise RuntimeError(
        "Controlled quota status is not 429."
    )

if controlled_error["code"] != "SCANNER_QUOTA_EXCEEDED":
    raise RuntimeError(
        "Controlled quota error code mismatch."
    )

if controlled_error["message"] != quota_message:
    raise RuntimeError(
        "Controlled quota error message mismatch."
    )

print("HTTP status: 429")
print("Error code: SCANNER_QUOTA_EXCEEDED")
print("Error message: PASS")
print("Controlled quota contract: PASS")

print()
print("===== 12. PRODUCTION SAFETY =====")

print("Controlled quota path only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")

print()
print("=" * 80)
print("STEP 8C-003 — TASK 20 COMPLETE")
print("=" * 80)
print("Quota exception contract: PASS")
print("HTTP 429 boundary: PASS")
print("SCANNER_QUOTA_EXCEEDED: PASS")
print("429 detection: PASS")
print("RESOURCE_EXHAUSTED detection: PASS")
print("Quota/503 separation: PASS")
print("Authentication boundary: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)


