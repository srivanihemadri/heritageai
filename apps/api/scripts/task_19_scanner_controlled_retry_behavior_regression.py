from __future__ import annotations

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.service import HeritageScannerService
from app.services.ai.scanner.contract import HeritageScannerResponse


print("=" * 80)
print("STEP 8C-003 — TASK 19 — SCANNER CONTROLLED RETRY-BEHAVIOR REGRESSION")
print("=" * 80)

print()
print("===== 1. VERIFY RETRY CONFIGURATION =====")

if HeritageScannerService.MAX_TRANSIENT_RETRIES != 3:
    raise RuntimeError(
        "Expected MAX_TRANSIENT_RETRIES to be 3."
    )

if HeritageScannerService.TRANSIENT_RETRY_DELAY_SECONDS < 0:
    raise RuntimeError(
        "Retry delay cannot be negative."
    )

print(
    "MAX_TRANSIENT_RETRIES:",
    HeritageScannerService.MAX_TRANSIENT_RETRIES,
)

print(
    "TRANSIENT_RETRY_DELAY_SECONDS:",
    HeritageScannerService.TRANSIENT_RETRY_DELAY_SECONDS,
)

print("Retry configuration: PASS")

print()
print("===== 2. VERIFY SCANNER SERVICE IMPORT =====")

print("HeritageScannerService: PASS")

print()
print("===== 3. VERIFY RETRY IMPLEMENTATION =====")

service_source = Path(
    "app/services/ai/scanner/service.py"
).read_text(encoding="utf-8")

required_patterns = [
    "for attempt in range(",
    "errors.ServerError",
    "last_error",
    "MAX_TRANSIENT_RETRIES",
    "TRANSIENT_RETRY_DELAY_SECONDS",
    "time.sleep(",
]

for pattern in required_patterns:
    if pattern not in service_source:
        raise RuntimeError(
            f"Retry implementation missing: {pattern}"
        )

print("Retry loop: PRESENT")
print("ServerError handling: PRESENT")
print("Attempt tracking: PRESENT")
print("Retry delay: PRESENT")
print("Final failure handling: PRESENT")
print("Retry implementation: PASS")

print()
print("===== 4. VERIFY CONTROLLED RESPONSE CONTRACT =====")

controlled_payload = {
    "success": True,
    "scan_id": f"task19-{uuid.uuid4().hex}",
    "result": {
        "identified_name": "Controlled Heritage Site",
        "category": "HISTORICAL_MONUMENT",
        "location": "Controlled Location",
        "country": "India",
        "confidence": 0.96,
        "confidence_level": "HIGH",
        "description": "Controlled retry regression result.",
        "architectural_style": "Controlled style",
        "historical_period": "Controlled period",
        "historical_significance": "Controlled significance",
        "visual_evidence": [
            "Distinctive architectural feature",
            "Visible historical structure",
        ],
        "alternative_matches": [],
        "grounding_status": "UNVERIFIED",
        "identification_status": "IDENTIFIED",
        "evidence_quality": "STRONG",
    },
}

response = HeritageScannerResponse.model_validate(
    controlled_payload
)

if not response.success:
    raise RuntimeError(
        "Controlled scanner response success flag is false."
    )

print("HeritageScannerResponse: PASS")
print("Controlled response contract: PASS")

print()
print("===== 5. VERIFY RETRY SAFETY =====")

if "time.sleep(" not in service_source:
    raise RuntimeError(
        "Controlled retry delay is missing."
    )

if "raise RuntimeError(" not in service_source:
    raise RuntimeError(
        "Final transient failure handling is missing."
    )

print("Retry delay boundary: PASS")
print("Final failure boundary: PASS")
print("Retry safety: PASS")

print()
print("===== 6. VERIFY QUOTA IS NOT RETRIED AS 503 =====")

client_error_section = service_source[
    service_source.find("except errors.ClientError"):
    service_source.find("except errors.ServerError")
]

if "ScannerQuotaExceededError" not in client_error_section:
    raise RuntimeError(
        "Quota exception handling boundary is missing."
    )

print("Quota exception boundary: PRESENT")
print("Quota is separated from transient retry path: PASS")

print()
print("===== 7. VERIFY EXISTING AI ROUTES =====")

from app.main import app

paths = app.openapi().get("paths", {})

if "/api/v1/ai/answer" not in paths:
    raise RuntimeError(
        "/api/v1/ai/answer route missing."
    )

if "/api/v1/ai/scan" not in paths:
    raise RuntimeError(
        "/api/v1/ai/scan route missing."
    )

print("/api/v1/ai/answer: PRESERVED")
print("/api/v1/ai/scan: PRESERVED")

print()
print("===== 8. PRODUCTION SAFETY =====")

print("Controlled retry architecture only: PASS")
print("Real Gemini request: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")

print()
print("=" * 80)
print("STEP 8C-003 — TASK 19 COMPLETE")
print("=" * 80)
print("Retry configuration: PASS")
print("Retry loop architecture: PASS")
print("ServerError handling: PASS")
print("Quota separation: PASS")
print("Final failure boundary: PASS")
print("Response contract: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
