from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.contract import HeritageScannerResult


print("=" * 80)
print("STEP 8C-003 — TASK 39 — SCANNER CONTROLLED MALFORMED GEMINI RESPONSE REGRESSION")
print("=" * 80)

base_payload = {
    "identified_name": "Konark Sun Temple",
    "identification_status": "IDENTIFIED",
    "evidence_quality": "STRONG",
    "category": "Temple",
    "location": "Konark",
    "country": "India",
    "confidence": 0.96,
    "confidence_level": "HIGH",
    "description": "Controlled test heritage monument.",
    "architectural_style": "Kalinga architecture",
    "historical_period": "13th century",
    "historical_significance": "Controlled historical significance.",
    "visual_evidence": [
        "Stone architectural structure",
        "Distinctive temple features",
    ],
    "alternative_matches": [],
    "grounding_status": "GROUNDED",
}

print()
print("===== 1. VERIFY VALID PRODUCTION PAYLOAD =====")

try:
    valid_result = HeritageScannerResult.model_validate(
        base_payload
    )
except Exception as exc:
    raise RuntimeError(
        f"Valid production payload rejected: "
        f"{type(exc).__name__}: {exc}"
    )

print("Valid production payload: PASS")


print()
print("===== 2. INVALID CONFIDENCE LEVEL =====")

invalid_confidence = dict(base_payload)
invalid_confidence["confidence_level"] = "NONE"

try:
    HeritageScannerResult.model_validate(
        invalid_confidence
    )
except Exception as exc:
    print("Invalid confidence_level: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "Invalid confidence_level was accepted."
    )


print()
print("===== 3. INVALID VISUAL EVIDENCE TYPE =====")

invalid_visual = dict(base_payload)
invalid_visual["visual_evidence"] = (
    "single string instead of list"
)

try:
    HeritageScannerResult.model_validate(
        invalid_visual
    )
except Exception as exc:
    print("Invalid visual_evidence type: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "Invalid visual_evidence type was accepted."
    )


print()
print("===== 4. INVALID IDENTIFIED RESULT WITHOUT VISUAL EVIDENCE =====")

missing_visual = dict(base_payload)
missing_visual["visual_evidence"] = []

try:
    HeritageScannerResult.model_validate(
        missing_visual
    )
except Exception as exc:
    print("IDENTIFIED without visual evidence: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "IDENTIFIED result without visual evidence was accepted."
    )


print()
print("===== 5. INVALID HIGH CONFIDENCE WITHOUT IDENTIFICATION =====")

no_identification = dict(base_payload)
no_identification["identified_name"] = None

try:
    HeritageScannerResult.model_validate(
        no_identification
    )
except Exception as exc:
    print("HIGH without identification: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "HIGH confidence without identification was accepted."
    )


print()
print("===== 6. INVALID NONE EVIDENCE WITH VISUAL EVIDENCE =====")

invalid_none_evidence = dict(base_payload)
invalid_none_evidence["evidence_quality"] = "NONE"

try:
    HeritageScannerResult.model_validate(
        invalid_none_evidence
    )
except Exception as exc:
    print("NONE evidence with visual evidence: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "NONE evidence with visual evidence was accepted."
    )


print()
print("===== 7. INVALID GROUNDED WITHOUT VISUAL EVIDENCE =====")

invalid_grounding = dict(base_payload)
invalid_grounding["visual_evidence"] = []

try:
    HeritageScannerResult.model_validate(
        invalid_grounding
    )
except Exception as exc:
    print("GROUNDED without visual evidence: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "GROUNDED without visual evidence was accepted."
    )


print()
print("===== 8. VERIFY CONTROLLED JSON BOUNDARY =====")

controlled_json = json.dumps(
    base_payload
)

decoded = json.loads(controlled_json)

if not isinstance(decoded, dict):
    raise RuntimeError(
        "Controlled JSON did not decode to an object."
    )

print("Controlled JSON object: PASS")


print()
print("===== 9. VERIFY PRODUCTION RESULT AFTER JSON ROUND TRIP =====")

try:
    round_trip_result = HeritageScannerResult.model_validate(
        decoded
    )
except Exception as exc:
    raise RuntimeError(
        f"Round-trip production validation failed: "
        f"{type(exc).__name__}: {exc}"
    )

if round_trip_result != valid_result:
    raise RuntimeError(
        "Round-trip result does not equal original result."
    )

print("JSON → Pydantic round trip: PASS")


print()
print("===== 10. PRODUCTION SAFETY =====")

print("Controlled malformed-response validation only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 39 COMPLETE")
print("=" * 80)
print("Valid production payload: PASS")
print("Invalid confidence_level rejection: PASS")
print("Invalid visual_evidence rejection: PASS")
print("Semantic validation boundaries: PASS")
print("JSON round trip: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
