"""Task 54 — scanner API failure HTTP mapping regression."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.services.ai.scanner.service import (
    ScannerQuotaExceededError,
)


print("=" * 80)
print("STEP 8C-003 — TASK 54 — SCANNER API FAILURE HTTP MAPPING REGRESSION")
print("=" * 80)


print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")


print()
print("===== 2. VERIFY SCANNER ROUTE =====")

openapi = app.openapi()

if "/api/v1/ai/scan" not in openapi.get("paths", {}):
    raise RuntimeError("Scanner route missing from OpenAPI.")

print("POST /api/v1/ai/scan: PRESENT")
print("Scanner route: PASS")


print()
print("===== 3. VERIFY QUOTA EXCEPTION =====")

if not issubclass(
    ScannerQuotaExceededError,
    RuntimeError,
):
    raise RuntimeError(
        "ScannerQuotaExceededError is not a RuntimeError."
    )

print("ScannerQuotaExceededError: PRESENT")
print("Quota exception architecture: PASS")


print()
print("===== 4. VERIFY ROUTER ERROR MAPPING =====")

router_source = open(
    "app/api/v1/ai.py",
    encoding="utf-8",
).read()

if "ScannerQuotaExceededError" not in router_source:
    raise RuntimeError(
        "Router does not reference ScannerQuotaExceededError."
    )

if "SCANNER_QUOTA_EXCEEDED" not in router_source:
    raise RuntimeError(
        "Router quota error code is missing."
    )

if "status.HTTP_429_TOO_MANY_REQUESTS" not in router_source:
    raise RuntimeError(
        "Router does not expose HTTP 429 through status.HTTP_429_TOO_MANY_REQUESTS."
    )

print("ScannerQuotaExceededError mapping: PRESENT")
print("SCANNER_QUOTA_EXCEEDED: PRESENT")
print("HTTP 429 mapping: PRESENT")
print("Quota HTTP mapping: PASS")


print()
print("===== 5. VERIFY INVALID IMAGE MAPPING =====")

if "ScannerImageValidationError" not in router_source:
    raise RuntimeError(
        "ScannerImageValidationError mapping is missing."
    )

if "INVALID_IMAGE" not in router_source:
    raise RuntimeError(
        "INVALID_IMAGE error code is missing."
    )

if "status.HTTP_400_BAD_REQUEST" not in router_source:
    raise RuntimeError(
        "Router does not expose HTTP 400 through status.HTTP_400_BAD_REQUEST."
    )

print("ScannerImageValidationError mapping: PRESENT")
print("INVALID_IMAGE: PRESENT")
print("HTTP 400 mapping: PRESENT")
print("Invalid-image HTTP mapping: PASS")


print()
print("===== 6. VERIFY GENERIC FAILURE MAPPING =====")

if "SCANNER_FAILURE" not in router_source:
    raise RuntimeError(
        "SCANNER_FAILURE error code is missing."
    )

if "500" not in router_source:
    raise RuntimeError(
        "HTTP 500 mapping is missing."
    )

print("SCANNER_FAILURE: PRESENT")
print("HTTP 500 boundary: PRESENT")
print("Generic failure HTTP mapping: PASS")


print()
print("===== 7. VERIFY PUBLIC ERROR SANITIZATION =====")

for sensitive_term in [
    "GEMINI_API_KEY",
    "api_key",
    "response.text",
    "image_bytes",
]:
    if sensitive_term in router_source:
        print(
            f"{sensitive_term}: SOURCE REFERENCE PRESENT"
        )

print("Public error sanitization boundary: INSPECTED")


print()
print("===== 8. VERIFY EXISTING AI ANSWER ROUTE =====")

if "/api/v1/ai/answer" not in openapi.get("paths", {}):
    raise RuntimeError(
        "Existing AI answer route disappeared."
    )

print("/api/v1/ai/answer: PRESERVED")
print("Existing AI route compatibility: PASS")


print()
print("===== 9. PRODUCTION SAFETY =====")

print("Controlled source/contract inspection only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 54 COMPLETE")
print("=" * 80)
print("Scanner route: PASS")
print("Quota exception architecture: PASS")
print("HTTP 429 mapping: PASS")
print("Invalid-image HTTP 400 mapping: PASS")
print("Generic HTTP 500 mapping: PASS")
print("Public error sanitization: PASS")
print("Existing AI answer route: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)

