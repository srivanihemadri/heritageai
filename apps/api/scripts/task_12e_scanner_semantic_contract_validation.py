from __future__ import annotations

import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from pydantic import ValidationError

from app.services.ai.scanner.contract import (
    HeritageScannerResult,
)


def valid_payload() -> dict:
    return {
        "identified_name": "Ajanta Caves",
        "category": "HISTORICAL_SITE",
        "location": "Maharashtra",
        "country": "India",
        "confidence": 0.96,
        "confidence_level": "HIGH",
        "description": "Rock-cut Buddhist cave complex.",
        "architectural_style": "Rock-cut architecture",
        "historical_period": "Ancient India",
        "historical_significance": "Major Buddhist heritage complex.",
        "visual_evidence": [
            "Rock-cut cave facade",
            "Stone-carved architectural features",
        ],
        "alternative_matches": [],
        "grounding_status": "GROUNDED",
    }


print("=" * 80)
print("STEP 8C-003 — TASK 12E — PRODUCTION SCANNER SEMANTIC CONTRACT VALIDATION")
print("=" * 80)


print()
print("===== 1. VALID HIGH-CONFIDENCE RESULT =====")

result = HeritageScannerResult(
    **valid_payload()
)

print("Valid HIGH result: PASS")


print()
print("===== 2. HIGH WITHOUT IDENTIFICATION =====")

payload = valid_payload()

payload["identified_name"] = None

try:
    HeritageScannerResult(**payload)

except ValidationError:
    print("HIGH without identification: REJECTED")

else:
    raise RuntimeError(
        "HIGH confidence without identification was accepted."
    )


print()
print("===== 3. HIGH WITHOUT VISUAL EVIDENCE =====")

payload = valid_payload()

payload["visual_evidence"] = []

try:
    HeritageScannerResult(**payload)

except ValidationError:
    print("HIGH without visual evidence: REJECTED")

else:
    raise RuntimeError(
        "HIGH confidence without visual evidence was accepted."
    )


print()
print("===== 4. HIGH CONFIDENCE RANGE =====")

payload = valid_payload()

payload["confidence"] = 0.89

try:
    HeritageScannerResult(**payload)

except ValidationError:
    print("HIGH with confidence < 0.90: REJECTED")

else:
    raise RuntimeError(
        "HIGH confidence below 0.90 was accepted."
    )


print()
print("===== 5. MEDIUM CONFIDENCE RANGE =====")

payload = valid_payload()

payload["confidence"] = 0.95
payload["confidence_level"] = "MEDIUM"

try:
    HeritageScannerResult(**payload)

except ValidationError:
    print("MEDIUM with confidence >= 0.90: REJECTED")

else:
    raise RuntimeError(
        "MEDIUM confidence >= 0.90 was accepted."
    )


print()
print("===== 6. LOW CONFIDENCE RANGE =====")

payload = valid_payload()

payload["identified_name"] = None
payload["confidence"] = 0.70
payload["confidence_level"] = "LOW"

try:
    HeritageScannerResult(**payload)

except ValidationError:
    print("LOW with confidence >= 0.50: REJECTED")

else:
    raise RuntimeError(
        "LOW confidence >= 0.50 was accepted."
    )


print()
print("===== 7. GROUNDED WITHOUT EVIDENCE =====")

payload = valid_payload()

payload["visual_evidence"] = []
payload["grounding_status"] = "GROUNDED"

try:
    HeritageScannerResult(**payload)

except ValidationError:
    print("GROUNDED without evidence: REJECTED")

else:
    raise RuntimeError(
        "GROUNDED without evidence was accepted."
    )


print()
print("===== 8. EMPTY IDENTIFICATION =====")

payload = valid_payload()

payload["identified_name"] = ""

try:
    HeritageScannerResult(**payload)

except ValidationError:
    print("Empty identification: REJECTED")

else:
    raise RuntimeError(
        "Empty identification was accepted."
    )


print()
print("===== 9. VALID MEDIUM RESULT =====")

payload = valid_payload()

payload["confidence"] = 0.75
payload["confidence_level"] = "MEDIUM"

medium = HeritageScannerResult(
    **payload
)

print("Valid MEDIUM result: PASS")


print()
print("===== 10. VALID LOW RESULT =====")

payload = valid_payload()

payload["identified_name"] = None
payload["confidence"] = 0.20
payload["confidence_level"] = "LOW"
payload["grounding_status"] = "UNVERIFIED"

low = HeritageScannerResult(
    **payload
)

print("Valid LOW result: PASS")


print()
print("===== 11. PRODUCTION SAFETY =====")

print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")


print()
print("=" * 80)
print("TASK 12E VALIDATION COMPLETE")
print("=" * 80)

print("Production semantic contract validation: PASS")
print("NO GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("SEND THE COMPLETE OUTPUT.")
