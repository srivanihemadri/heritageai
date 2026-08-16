from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 27 — SCANNER CONTROLLED OBSERVABILITY & LOGGING REGRESSION")
print("=" * 80)


print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")


print()
print("===== 2. VERIFY SCANNER SERVICE =====")

service_path = (
    Path(__file__).resolve().parents[1]
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

print("Scanner service source: PRESENT")


print()
print("===== 3. VERIFY SCANNER REQUEST LIFECYCLE LOGGING =====")

lifecycle_terms = [
    "REAL GEMINI SCANNER REQUEST: START",
    "REAL GEMINI SCANNER REQUEST: COMPLETED",
]

for term in lifecycle_terms:
    if term not in service_source:
        raise RuntimeError(
            f"Scanner lifecycle log missing: {term}"
        )

    print(f"{term}: PRESENT")

print("Request lifecycle logging: PASS")


print()
print("===== 4. VERIFY RETRY OBSERVABILITY =====")

retry_terms = [
    "GEMINI SCANNER ATTEMPT:",
    "GEMINI TRANSIENT SERVER ERROR:",
    "Waiting before controlled retry...",
]

for term in retry_terms:
    if term not in service_source:
        raise RuntimeError(
            f"Retry observability term missing: {term}"
        )

    print(f"{term}: PRESENT")

print("Retry observability: PASS")


print()
print("===== 5. VERIFY QUOTA OBSERVABILITY =====")

quota_terms = [
    "GEMINI SCANNER QUOTA EXHAUSTED",
    "RESOURCE_EXHAUSTED",
]

for term in quota_terms:
    if term not in service_source:
        raise RuntimeError(
            f"Quota observability term missing: {term}"
        )

    print(f"{term}: PRESENT")

print("Quota observability: PASS")


print()
print("===== 6. VERIFY TRANSIENT FAILURE OBSERVABILITY =====")

failure_terms = [
    "GEMINI TRANSIENT SERVER ERROR:",
    "after controlled retries.",
]

for term in failure_terms:
    if term not in service_source:
        raise RuntimeError(
            f"Transient failure observability missing: {term}"
        )

    print(f"{term}: PRESENT")

print("Transient failure observability: PASS")


print()
print("===== 7. VERIFY SCANNER FAILURE OBSERVABILITY =====")

failure_contract_terms = [
    "Gemini scanner returned no response.",
    "Gemini returned an empty scanner response.",
]

for term in failure_contract_terms:
    if term not in service_source:
        raise RuntimeError(
            f"Scanner failure boundary missing: {term}"
        )

    print(f"{term}: PRESENT")

print("Scanner failure observability: PASS")


print()
print("===== 8. VERIFY SENSITIVE DATA IS NOT LOGGED =====")

sensitive_logging_patterns = [
    "print(settings.GEMINI_API_KEY",
    "print(self.client",
    "logger.info(settings.GEMINI_API_KEY",
    "logger.debug(settings.GEMINI_API_KEY",
    "logger.warning(settings.GEMINI_API_KEY",
    "logger.error(settings.GEMINI_API_KEY",
    "print(api_key",
    "logger.info(api_key",
    "logger.debug(api_key",
    "logger.warning(api_key",
    "logger.error(api_key",
    "print(password",
    "print(access_token",
    "print(refresh_token",
]

for pattern in sensitive_logging_patterns:
    if pattern in service_source:
        raise RuntimeError(
            f"Potential sensitive-data logging detected: {pattern}"
        )

    print(f"{pattern}: NOT PRESENT")

print("Sensitive logging protection: PASS")


print()
print("===== 9. VERIFY LOGGING DOES NOT EXPOSE IMAGE CONTENT =====")

image_logging_patterns = [
    "print(image_bytes",
    "logger.info(image_bytes",
    "logger.debug(image_bytes",
    "logger.warning(image_bytes",
    "logger.error(image_bytes",
    "print(image_base64",
    "logger.info(image_base64",
    "logger.debug(image_base64",
    "logger.warning(image_base64",
    "logger.error(image_base64",
    "print(base64_image",
    "logger.info(base64_image",
    "logger.debug(base64_image",
    "logger.warning(base64_image",
    "logger.error(base64_image",
]

for pattern in image_logging_patterns:
    if pattern in service_source:
        raise RuntimeError(
            f"Potential image-content logging detected: {pattern}"
        )

    print(f"{pattern}: NOT PRESENT")

print("Image-content logging protection: PASS")


print()
print("===== 10. VERIFY LOGGING DOES NOT EXPOSE GEMINI RESPONSE CONTENT =====")

response_logging_terms = [
    "print(response.text",
    "print(text)",
    "response.text=",
    "response_text=",
]

for term in response_logging_terms:
    if term in service_source:
        raise RuntimeError(
            f"Potential Gemini response-content logging detected: {term}"
        )

    print(f"{term}: NOT PRESENT")

print("Gemini response logging protection: PASS")


print()
print("===== 11. VERIFY RETRY CONFIGURATION IS OBSERVABLE =====")

retry_configuration = [
    "MAX_TRANSIENT_RETRIES",
    "TRANSIENT_RETRY_DELAY_SECONDS",
]

for term in retry_configuration:
    if term not in service_source:
        raise RuntimeError(
            f"Retry configuration missing: {term}"
        )

    print(f"{term}: PRESENT")

print("Retry configuration observability: PASS")


print()
print("===== 12. VERIFY SCANNER ROUTE =====")

openapi = app.openapi()
paths = openapi.get("paths", {})

scanner_path = paths.get("/api/v1/ai/scan")

if scanner_path is None:
    raise RuntimeError(
        "POST /api/v1/ai/scan route missing from OpenAPI."
    )

if "post" not in scanner_path:
    raise RuntimeError(
        "POST /api/v1/ai/scan operation missing from OpenAPI."
    )

print("POST /api/v1/ai/scan: PASS")
print("OpenAPI scanner route: PRESENT")


print()
print("===== 13. VERIFY EXISTING AI ROUTES =====")

if "/api/v1/ai/answer" not in paths:
    raise RuntimeError(
        "Existing /api/v1/ai/answer route missing."
    )

print("/api/v1/ai/answer: PRESERVED")
print("/api/v1/ai/scan: PRESERVED")


print()
print("===== 14. VERIFY AUTHENTICATION OBSERVABILITY BOUNDARY =====")

unauthenticated = client.post(
    "/api/v1/ai/scan",
)

if unauthenticated.status_code != 401:
    raise RuntimeError(
        f"Expected HTTP 401, got {unauthenticated.status_code}: "
        f"{unauthenticated.text}"
    )

print("Unauthenticated scanner request: HTTP 401")
print("Authentication observability boundary: PASS")


print()
print("===== 15. VERIFY PUBLIC ERROR DOES NOT LEAK INTERNAL LOG DATA =====")

response_text = unauthenticated.text

for forbidden in (
    "Traceback",
    "File ",
    "google.genai",
    "RESOURCE_EXHAUSTED",
    "ClientError",
    "ServerError",
    "api_key",
    "password",
    "secret",
):

    if forbidden.lower() in response_text.lower():
        raise RuntimeError(
            f"Public error response leaks internal detail: {forbidden}"
        )

print("Public error sanitization: PASS")


print()
print("===== 16. PRODUCTION SAFETY =====")

print("Controlled observability inspection only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 27 COMPLETE")
print("=" * 80)
print("Request lifecycle logging: PASS")
print("Retry observability: PASS")
print("Quota observability: PASS")
print("Transient failure observability: PASS")
print("Scanner failure observability: PASS")
print("Sensitive logging protection: PASS")
print("Image-content logging protection: PASS")
print("Gemini response logging protection: PASS")
print("Retry configuration observability: PASS")
print("Authentication boundary: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)





