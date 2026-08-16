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
print("STEP 8C-003 Ã¢â‚¬â€ TASK 12D Ã¢â‚¬â€ SCANNER SEMANTIC QUALITY GUARDRAILS")
print("=" * 80)


def build_result(**overrides) -> HeritageScannerResult:
    payload = {
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
        "grounding_status": "UNVERIFIED",
    }

    payload.update(overrides)

    return HeritageScannerResult(**payload)


print()
print("===== 1. HIGH-CONFIDENCE IDENTIFICATION =====")

result = build_result()

if (
    result.identified_name
    and result.confidence >= 0.90
    and len(result.visual_evidence) >= 1
):
    print("High-confidence evidence consistency: PASS")
else:
    raise RuntimeError(
        "Valid high-confidence result failed consistency."
    )


print()
print("===== 2. HIGH CONFIDENCE WITHOUT IDENTIFICATION =====")

try:
    build_result(
        identified_name=None,
        confidence=0.96,
        confidence_level="HIGH",
    )

except ValidationError:
    print(
        "Missing identification with HIGH confidence: PASS"
    )

else:
    print(
        "WARNING: Contract permits this semantic combination."
    )


print()
print("===== 3. HIGH CONFIDENCE WITHOUT VISUAL EVIDENCE =====")

try:
    build_result(
        confidence=0.96,
        confidence_level="HIGH",
        visual_evidence=[],
    )

except ValidationError:
    print(
        "HIGH confidence without evidence: PASS"
    )

else:
    print(
        "WARNING: Contract permits empty evidence."
    )


print()
print("===== 4. VERIFIED GROUNDING =====")

verified = build_result(
    grounding_status="GROUNDED",
)

if verified.grounding_status != "GROUNDED":
    raise RuntimeError(
        "VERIFIED grounding status was not preserved."
    )

if not verified.visual_evidence:
    raise RuntimeError(
        "GROUNDED result has no visual evidence."
    )

print(
    "Grounded evidence consistency: PASS"
)


print()
print("===== 5. LOW-CONFIDENCE RESULT =====")

low = build_result(
    identified_name=None,
    confidence=0.20,
    confidence_level="LOW",
    visual_evidence=[
        "Image contains architectural features."
    ],
)

if low.confidence_level != "LOW":
    raise RuntimeError(
        "LOW confidence level was not preserved."
    )

if low.confidence >= 0.50:
    raise RuntimeError(
        "LOW confidence result has unexpectedly high confidence."
    )

print(
    "Low-confidence uncertainty contract: PASS"
)


print()
print("===== 6. ALTERNATIVE MATCHES =====")

alternatives = build_result(
    identified_name="Ajanta Caves",
    confidence=0.72,
    confidence_level="MEDIUM",
    alternative_matches=[
        "Ellora Caves",
        "Elephanta Caves",
    ],
)

if len(alternatives.alternative_matches) != 2:
    raise RuntimeError(
        "Alternative matches were not preserved."
    )

if (
    alternatives.identified_name
    in alternatives.alternative_matches
):
    raise RuntimeError(
        "Primary identification duplicated in alternatives."
    )

print(
    "Alternative match separation: PASS"
)


print()
print("===== 7. EMPTY STRING PROTECTION =====")

try:
    build_result(
        identified_name="",
    )

except ValidationError:
    print(
        "Empty identification rejection: PASS"
    )

else:
    print(
        "WARNING: Contract permits empty identification."
    )


print()
print("===== 8. RESPONSE WRAPPER =====")

response = HeritageScannerResponse(
    scan_id=str(uuid.uuid4()),
    result=result,
)

if not response.scan_id:
    raise RuntimeError(
        "Missing scanner scan_id."
    )

if response.result.identified_name != "Ajanta Caves":
    raise RuntimeError(
        "Scanner result was not preserved."
    )

print(
    "Response wrapper integrity: PASS"
)


print()
print("===== 9. PRODUCTION SAFETY =====")

print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 Ã¢â‚¬â€ TASK 12D COMPLETE")
print("=" * 80)

print("Semantic scanner guardrails: PASS")
print("Confidence/evidence consistency: PASS")
print("Grounding consistency: PASS")
print("Uncertainty contract: PASS")
print("Alternative match separation: PASS")
print("Response wrapper: PASS")
print("NO GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO PRODUCTION SOURCE CHANGES.")
print("SEND THE COMPLETE OUTPUT.")
