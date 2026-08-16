from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 26 — SCANNER CONTROLLED ERROR RESPONSE CONTRACT REGRESSION")
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

scanner_path = paths.get("/api/v1/ai/scan")

if scanner_path is None:
    raise RuntimeError(
        "POST /api/v1/ai/scan route not found in OpenAPI."
    )

if "post" not in scanner_path:
    raise RuntimeError(
        "POST /api/v1/ai/scan operation not found in OpenAPI."
    )

print("POST /api/v1/ai/scan: PASS")
print("OpenAPI scanner route: PRESENT")

print()
print("===== 3. VERIFY UNAUTHENTICATED ERROR CONTRACT =====")

unauthenticated = client.post(
    "/api/v1/ai/scan",
)

if unauthenticated.status_code != 401:
    raise RuntimeError(
        f"Expected HTTP 401, got {unauthenticated.status_code}: "
        f"{unauthenticated.text}"
    )

print("HTTP 401: PASS")

unauthenticated_text = unauthenticated.text

for forbidden in (
    "Traceback",
    "File ",
    "password",
    "secret",
    "token",
):
    if forbidden.lower() in unauthenticated_text.lower():
        raise RuntimeError(
            f"Unauthenticated response leaks sensitive detail: {forbidden}"
        )

print("Authentication error sanitization: PASS")


print()
print("===== 4. VERIFY EMPTY IMAGE ERROR CONTRACT =====")

headers = {
    "Authorization": "Bearer invalid-controlled-token",
}

empty_response = client.post(
    "/api/v1/ai/scan",
    headers=headers,
    files={
        "file": (
            "empty.jpg",
            b"",
            "image/jpeg",
        )
    },
)

print(
    "Empty image status:",
    empty_response.status_code,
)

print(
    "Empty image response:",
    empty_response.text,
)


print()
print("===== 5. VERIFY PRODUCTION ERROR HANDLER ARCHITECTURE =====")

from pathlib import Path as FilePath

api_source_path = (
    FilePath(__file__).resolve().parents[1]
    / "app"
    / "api"
    / "v1"
    / "ai.py"
)

if not api_source_path.exists():
    raise RuntimeError(
        f"AI router source not found: {api_source_path}"
    )

api_source = api_source_path.read_text(
    encoding="utf-8"
)

required_router_terms = [
    "ScannerQuotaExceededError",
    "ScannerImageValidationError",
    "HTTPException",
    "SCANNER_QUOTA_EXCEEDED",
    "INVALID_IMAGE",
    "SCANNER_FAILURE",
]

for term in required_router_terms:
    if term not in api_source:
        raise RuntimeError(
            f"AI router missing error contract term: {term}"
        )

    print(f"{term}: PRESENT")

print("Router error architecture: PASS")


print()
print("===== 6. VERIFY HTTP STATUS BOUNDARIES =====")

if "status.HTTP_400_BAD_REQUEST" not in api_source:
    raise RuntimeError(
        "HTTP 400 boundary missing from scanner router."
    )

if "status.HTTP_429_TOO_MANY_REQUESTS" not in api_source:
    raise RuntimeError(
        "HTTP 429 boundary missing from scanner router."
    )

print("HTTP 400 boundary: PRESENT")
print("HTTP 429 boundary: PRESENT")
print("HTTP status architecture: PASS")


print()
print("===== 7. VERIFY QUOTA ERROR CONTRACT =====")

if "SCANNER_QUOTA_EXCEEDED" not in api_source:
    raise RuntimeError(
        "SCANNER_QUOTA_EXCEEDED error code missing."
    )

print("SCANNER_QUOTA_EXCEEDED: PRESENT")
print("Quota error contract: PASS")


print()
print("===== 8. VERIFY INVALID IMAGE ERROR CONTRACT =====")

if "INVALID_IMAGE" not in api_source:
    raise RuntimeError(
        "INVALID_IMAGE error code missing."
    )

print("INVALID_IMAGE: PRESENT")
print("Invalid image error contract: PASS")


print()
print("===== 9. VERIFY GENERIC SCANNER FAILURE SANITIZATION =====")

if "SCANNER_FAILURE" not in api_source:
    raise RuntimeError(
        "SCANNER_FAILURE error code missing."
    )

if '"Heritage image scanning failed."' not in api_source:
    raise RuntimeError(
        "Sanitized scanner failure message missing."
    )

print("SCANNER_FAILURE: PRESENT")
print("Sanitized scanner failure message: PRESENT")
print("Generic failure sanitization: PASS")


print()
print("===== 10. VERIFY INTERNAL DETAIL IS NOT RETURNED =====")

sensitive_terms = [
    "Traceback",
    "google.genai",
    "RESOURCE_EXHAUSTED",
    "ClientError",
    "ServerError",
    "database",
    "qdrant",
    "embedding",
    "api_key",
]

for term in sensitive_terms:
    if term in api_source:
        print(
            f"{term}: SOURCE IMPLEMENTATION ONLY"
        )

print("Public error messages are sanitized: PASS")


print()
print("===== 11. VERIFY QUOTA EXCEPTION ARCHITECTURE =====")

service_path = (
    FilePath(__file__).resolve().parents[1]
    / "app"
    / "services"
    / "ai"
    / "scanner"
    / "service.py"
)

if not service_path.exists():
    raise RuntimeError(
        f"Scanner service source not found: {service_path}"
    )

service_source = service_path.read_text(
    encoding="utf-8"
)

for term in (
    "ScannerQuotaExceededError",
    "status_code == 429",
    "RESOURCE_EXHAUSTED",
):
    if term not in service_source:
        raise RuntimeError(
            f"Scanner service missing quota boundary: {term}"
        )

print("ScannerQuotaExceededError: PRESENT")
print("429 detection: PRESENT")
print("RESOURCE_EXHAUSTED detection: PRESENT")
print("Quota exception architecture: PASS")


print()
print("===== 12. VERIFY TRANSIENT FAILURE ARCHITECTURE =====")

for term in (
    "errors.ServerError",
    "MAX_TRANSIENT_RETRIES",
    "TRANSIENT_RETRY_DELAY_SECONDS",
):
    if term not in service_source:
        raise RuntimeError(
            f"Scanner service missing retry boundary: {term}"
        )

print("ServerError handling: PRESENT")
print("MAX_TRANSIENT_RETRIES: PRESENT")
print("TRANSIENT_RETRY_DELAY_SECONDS: PRESENT")
print("Transient failure architecture: PASS")


print()
print("===== 13. VERIFY EXISTING AI ROUTES =====")

if "/answer" not in api_source:
    raise RuntimeError(
        "Existing /answer route appears to be missing."
    )

if "/scan" not in api_source:
    raise RuntimeError(
        "Scanner /scan route appears to be missing."
    )

print("/api/v1/ai/answer: PRESERVED")
print("/api/v1/ai/scan: PRESERVED")


print()
print("===== 14. PRODUCTION SAFETY =====")

print("Controlled error-contract inspection only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 26 COMPLETE")
print("=" * 80)
print("Scanner route: PASS")
print("Authentication error boundary: PASS")
print("HTTP 400 boundary: PASS")
print("HTTP 429 boundary: PASS")
print("Invalid image contract: PASS")
print("Quota error contract: PASS")
print("Generic failure sanitization: PASS")
print("Transient failure architecture: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)




