from __future__ import annotations

import sys
import uuid
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from pydantic import ValidationError

from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)


print("=" * 80)
print("STEP 8C-003 — TASK 12C — SCANNER RESPONSE CONTRACT HARDENING")
print("=" * 80)


def valid_result() -> HeritageScannerResult:
    return HeritageScannerResult(
        identified_name="Ajanta Caves",
        category="HISTORICAL_SITE",
        location="Maharashtra",
        country="India",
        confidence=0.96,
        confidence_level="HIGH",
        description="Rock-cut Buddhist cave complex.",
        architectural_style="Rock-cut architecture",
        historical_period="Ancient India",
        historical_significance="Major Buddhist heritage complex.",
        visual_evidence=[
            "Rock-cut cave facade",
            "Stone-carved architectural features",
        ],
        alternative_matches=[],
        grounding_status="UNVERIFIED",
    )


print()
print("===== 1. VALID RESULT CONTRACT =====")

result = valid_result()

print("HeritageScannerResult: PASS")

response = HeritageScannerResponse(
    scan_id=str(uuid.uuid4()),
    result=result,
)

print("HeritageScannerResponse: PASS")


print()
print("===== 2. CONFIDENCE LOWER BOUND =====")

try:
    HeritageScannerResult(
        **{
            **result.model_dump(),
            "confidence": -0.01,
        }
    )

except ValidationError:
    print("Confidence < 0 rejection: PASS")

else:
    raise RuntimeError(
        "Confidence below zero was accepted."
    )


print()
print("===== 3. CONFIDENCE UPPER BOUND =====")

try:
    HeritageScannerResult(
        **{
            **result.model_dump(),
            "confidence": 1.01,
        }
    )

except ValidationError:
    print("Confidence > 1 rejection: PASS")

else:
    raise RuntimeError(
        "Confidence above one was accepted."
    )


print()
print("===== 4. INVALID CONFIDENCE LEVEL =====")

try:
    HeritageScannerResult(
        **{
            **result.model_dump(),
            "confidence_level": "INVALID",
        }
    )

except ValidationError:
    print("Invalid confidence level rejection: PASS")

else:
    raise RuntimeError(
        "Invalid confidence level was accepted."
    )


print()
print("===== 5. INVALID GROUNDING STATUS =====")

try:
    HeritageScannerResult(
        **{
            **result.model_dump(),
            "grounding_status": "INVALID",
        }
    )

except ValidationError:
    print("Invalid grounding status rejection: PASS")

else:
    raise RuntimeError(
        "Invalid grounding status was accepted."
    )


print()
print("===== 6. VISUAL EVIDENCE CONTRACT =====")

if not isinstance(
    result.visual_evidence,
    list,
):
    raise RuntimeError(
        "Visual evidence is not a list."
    )

if len(result.visual_evidence) == 0:
    raise RuntimeError(
        "Valid scanner result contains no visual evidence."
    )

print("Visual evidence structure: PASS")


print()
print("===== 7. ALTERNATIVE MATCHES CONTRACT =====")

if not isinstance(
    result.alternative_matches,
    list,
):
    raise RuntimeError(
        "Alternative matches is not a list."
    )

print("Alternative matches structure: PASS")


print()
print("===== 8. SCAN ID CONTRACT =====")

if not response.scan_id:
    raise RuntimeError(
        "Scanner response has no scan_id."
    )

print("scan_id presence: PASS")


print()
print("===== 9. RESPONSE SERIALIZATION =====")

payload = response.model_dump()

if "scan_id" not in payload:
    raise RuntimeError(
        "Serialized response missing scan_id."
    )

if "result" not in payload:
    raise RuntimeError(
        "Serialized response missing result."
    )

print("Serialization: PASS")


print()
print("===== 10. PRODUCTION SAFETY =====")

print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 12C COMPLETE")
print("=" * 80)

print("Valid scanner response: PASS")
print("Confidence bounds: PASS")
print("Confidence level validation: PASS")
print("Grounding status validation: PASS")
print("Visual evidence contract: PASS")
print("Alternative matches contract: PASS")
print("Scan ID contract: PASS")
print("Serialization: PASS")
print("NO GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO PRODUCTION SOURCE CHANGES.")
print("SEND THE COMPLETE OUTPUT.")
