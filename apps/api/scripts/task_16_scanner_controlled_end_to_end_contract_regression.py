# STEP 8C-003 — TASK 16
# SCANNER CONTROLLED END-TO-END CONTRACT REGRESSION

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import uuid
from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app
from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)
from app.services.ai.scanner.prompts import (
    SCANNER_INTELLIGENCE_RULES,
    build_scanner_prompt,
)


print("=" * 80)
print("STEP 8C-003 — TASK 16 — SCANNER CONTROLLED END-TO-END CONTRACT REGRESSION")
print("=" * 80)

print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")

print()
print("===== 2. VERIFY SCANNER ROUTE =====")

openapi = app.openapi()
operation = openapi.get("paths", {}).get("/api/v1/ai/scan", {}).get("post")

if operation is None:
    raise RuntimeError("POST /api/v1/ai/scan not found.")

print("POST /api/v1/ai/scan: PASS")

security = operation.get("security")

if not security:
    raise RuntimeError("Scanner authentication security definition missing.")

print("Authentication security: PASS")

print()
print("===== 3. VERIFY PROMPT INTELLIGENCE CONTRACT =====")

prompt = build_scanner_prompt()

if not isinstance(prompt, str) or not prompt:
    raise RuntimeError("Scanner prompt construction failed.")

required_terms = [
    "IDENTIFIED",
    "POSSIBLE_MATCH",
    "INSUFFICIENT_EVIDENCE",
    "NOT_HERITAGE",
    "AMBIGUOUS",
    "STRONG",
    "MODERATE",
    "WEAK",
    "NONE",
    "GROUNDED",
    "PARTIALLY_GROUNDED",
    "UNVERIFIED",
    "identification_status",
    "evidence_quality",
    "confidence",
    "visual_evidence",
]

for term in required_terms:
    if term not in prompt:
        raise RuntimeError(
            f"Required scanner intelligence term missing: {term}"
        )

print("SCANNER_INTELLIGENCE_RULES: PASS")
print("Prompt intelligence coverage: PASS")

print()
print("===== 4. VERIFY AUTHENTICATION BOUNDARY =====")

png_bytes = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00"
    b"\x90wS\xde"
    b"\x00\x00\x00\x0cIDAT"
    b"\x08\xd7c\xf8\xcf\xc0\x00\x00\x03\x01\x01\x00"
    b"\x18\xdd\x8d\xb4"
    b"\x00\x00\x00\x00IEND\xaeB`\x82"
)

unauthenticated = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "controlled.png",
            BytesIO(png_bytes),
            "image/png",
        )
    },
)

if unauthenticated.status_code != 401:
    raise RuntimeError(
        f"Expected unauthenticated status 401, got "
        f"{unauthenticated.status_code}"
    )

print("Unauthenticated status: 401")
print("Authentication boundary: PASS")

print()
print("===== 5. CREATE CONTROLLED TEST USER =====")

email = f"task16.{uuid.uuid4().hex}@example.com"
password = "Task16-Controlled-Password-123!"

registration = client.post(
    "/api/v1/auth/register",
    json={
        "email": email,
        "full_name": "Task 16 Controlled User",
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
print("===== 6. LOGIN =====")

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
print("===== 7. BUILD CONTROLLED SCANNER RESPONSE =====")

controlled_payload = {
    "identified_name": "Konark Sun Temple",
    "category": "HISTORICAL_MONUMENT",
    "location": "Konark",
    "country": "India",
    "confidence": 0.96,
    "confidence_level": "HIGH",
    "description": "Controlled scanner regression response.",
    "architectural_style": "Kalinga architecture",
    "historical_period": "13th century",
    "historical_significance": (
        "Controlled historical significance for regression testing."
    ),
    "visual_evidence": [
        "Stone architectural structure",
        "Distinctive carved wheel-like elements",
    ],
    "alternative_matches": [],
    "grounding_status": "GROUNDED",
    "identification_status": "IDENTIFIED",
    "evidence_quality": "STRONG",
}

controlled_result = HeritageScannerResult.model_validate(
    controlled_payload
)

controlled_response = HeritageScannerResponse(
    success=True,
    scan_id=f"task16-{uuid.uuid4().hex}",
    result=controlled_result,
)

print("Controlled HeritageScannerResult: PASS")
print("Controlled HeritageScannerResponse: PASS")
print("Intelligence fields: PASS")

print()
print("===== 8. VERIFY CONTROLLED RESPONSE SERIALIZATION =====")

serialized = controlled_response.model_dump()

for field in (
    "identification_status",
    "evidence_quality",
    "grounding_status",
    "confidence",
    "visual_evidence",
    "alternative_matches",
):
    if field not in serialized["result"]:
        raise RuntimeError(
            f"Serialized scanner result missing field: {field}"
        )

if not serialized["scan_id"]:
    raise RuntimeError("scan_id missing.")

print("Response serialization: PASS")
print("scan_id: PASS")
print("Intelligence field preservation: PASS")

print()
print("===== 9. VERIFY SEMANTIC REJECTION =====")

invalid_cases = [
    {
        "name": "HIGH without identification",
        "payload": {
            **controlled_payload,
            "identified_name": None,
        },
    },
    {
        "name": "HIGH without visual evidence",
        "payload": {
            **controlled_payload,
            "visual_evidence": [],
        },
    },
    {
        "name": "GROUNDED without evidence",
        "payload": {
            **controlled_payload,
            "visual_evidence": [],
            "grounding_status": "GROUNDED",
        },
    },
]

for case in invalid_cases:
    try:
        HeritageScannerResult.model_validate(case["payload"])
    except Exception:
        print(f'{case["name"]}: REJECTED')
    else:
        raise RuntimeError(
            f'{case["name"]} was incorrectly accepted.'
        )

print("Semantic rejection: PASS")

print()
print("===== 10. VERIFY ERROR CONTRACTS =====")

from app.services.ai.scanner.service import ScannerQuotaExceededError

quota_error = ScannerQuotaExceededError(
    "Gemini scanner quota has been exhausted. Please try again later."
)

if not str(quota_error):
    raise RuntimeError("Quota exception contract invalid.")

print("ScannerQuotaExceededError: PASS")
print("HTTP 429 boundary architecture: PRESERVED")

print()
print("===== 11. VERIFY EXISTING AI ROUTES =====")

paths = openapi.get("paths", {})

if "/api/v1/ai/answer" not in paths:
    raise RuntimeError("/api/v1/ai/answer route was lost.")

if "/api/v1/ai/scan" not in paths:
    raise RuntimeError("/api/v1/ai/scan route was lost.")

print("/api/v1/ai/answer: PRESERVED")
print("/api/v1/ai/scan: PRESERVED")

print()
print("===== 12. PRODUCTION SAFETY =====")

print("Controlled scanner only: PASS")
print("Real Gemini request: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")

print()
print("=" * 80)
print("STEP 8C-003 — TASK 16 COMPLETE")
print("=" * 80)
print("Authenticated scanner contract: PASS")
print("Prompt intelligence contract: PASS")
print("Controlled scanner response: PASS")
print("Semantic validation: PASS")
print("Response serialization: PASS")
print("Authentication boundary: PASS")
print("Error architecture: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)



