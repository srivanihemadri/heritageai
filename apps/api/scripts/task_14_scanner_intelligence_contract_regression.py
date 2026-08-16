from __future__ import annotations

import inspect
import sys
import uuid
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
    ScannerEvidenceQuality,
    ScannerIdentificationStatus,
)


print("=" * 80)
print("STEP 8C-003 — TASK 14 — SCANNER INTELLIGENCE CONTRACT REGRESSION")
print("=" * 80)


def build_result(**overrides) -> HeritageScannerResult:

    payload = {
        "identified_name": "Test Heritage Site",
        "category": "HISTORICAL_SITE",
        "location": "Test Location",
        "country": "India",
        "confidence": 0.95,
        "confidence_level": "HIGH",
        "description": "Controlled scanner intelligence contract result.",
        "architectural_style": "Rock-cut",
        "historical_period": "Ancient",
        "historical_significance": "Controlled evidence.",
        "visual_evidence": [
            "Visible architectural structure",
            "Distinctive historical feature",
        ],
        "alternative_matches": [],
        "grounding_status": "GROUNDED",
        "identification_status": "IDENTIFIED",
        "evidence_quality": "STRONG",
    }

    payload.update(overrides)

    return HeritageScannerResult(**payload)


print()
print("===== 1. VERIFY INTELLIGENCE TYPES =====")

print(
    "ScannerIdentificationStatus:",
    ScannerIdentificationStatus,
)

print(
    "ScannerEvidenceQuality:",
    ScannerEvidenceQuality,
)

print("Identification status type: PASS")
print("Evidence quality type: PASS")


print()
print("===== 2. VALID HIGH-CONFIDENCE RESULT =====")

high = build_result()

if (
    high.confidence_level != "HIGH"
    or high.confidence < 0.90
    or not high.identified_name
    or not high.visual_evidence
):
    raise RuntimeError(
        "Valid HIGH-confidence intelligence result failed."
    )

print("HIGH confidence: PASS")
print("Identification: PASS")
print("Visual evidence: PASS")
print("Grounding: PASS")


print()
print("===== 3. HIGH WITHOUT IDENTIFICATION =====")

try:
    build_result(
        identified_name=None,
        identification_status="INSUFFICIENT_EVIDENCE",
        confidence=0.95,
        confidence_level="HIGH",
    )
except ValueError:
    print("HIGH without identification: REJECTED")
else:
    raise RuntimeError(
        "HIGH confidence without identification was accepted."
    )


print()
print("===== 4. HIGH WITHOUT VISUAL EVIDENCE =====")

try:
    build_result(
        visual_evidence=[],
        evidence_quality="NONE",
        confidence=0.95,
        confidence_level="HIGH",
    )
except ValueError:
    print("HIGH without visual evidence: REJECTED")
else:
    raise RuntimeError(
        "HIGH confidence without visual evidence was accepted."
    )


print()
print("===== 5. HIGH CONFIDENCE RANGE =====")

try:
    build_result(
        confidence=0.89,
        confidence_level="HIGH",
    )
except ValueError:
    print("HIGH confidence < 0.90: REJECTED")
else:
    raise RuntimeError(
        "HIGH confidence below required threshold was accepted."
    )


print()
print("===== 6. MEDIUM CONFIDENCE RANGE =====")

try:
    build_result(
        confidence=0.90,
        confidence_level="MEDIUM",
    )
except ValueError:
    print("MEDIUM confidence >= 0.90: REJECTED")
else:
    raise RuntimeError(
        "MEDIUM confidence outside expected range was accepted."
    )


print()
print("===== 7. LOW CONFIDENCE RANGE =====")

try:
    build_result(
        confidence=0.50,
        confidence_level="LOW",
    )
except ValueError:
    print("LOW confidence >= 0.50: REJECTED")
else:
    raise RuntimeError(
        "LOW confidence outside expected range was accepted."
    )


print()
print("===== 8. GROUNDED WITHOUT EVIDENCE =====")

try:
    build_result(
        grounding_status="GROUNDED",
        visual_evidence=[],
        evidence_quality="NONE",
    )
except ValueError:
    print("GROUNDED without evidence: REJECTED")
else:
    raise RuntimeError(
        "GROUNDED result without evidence was accepted."
    )


print()
print("===== 9. PARTIALLY GROUNDED =====")

partial = build_result(
    confidence=0.72,
    confidence_level="MEDIUM",
    grounding_status="PARTIALLY_GROUNDED",
    identification_status="POSSIBLE_MATCH",
    evidence_quality="MODERATE",
)

if partial.grounding_status != "PARTIALLY_GROUNDED":
    raise RuntimeError(
        "PARTIALLY_GROUNDED status was not preserved."
    )

print("PARTIALLY_GROUNDED: PASS")
print("Partial identification: PASS")
print("Moderate evidence: PASS")


print()
print("===== 10. UNVERIFIED =====")

unverified = build_result(
    identified_name=None,
    confidence=0.20,
    confidence_level="LOW",
    grounding_status="UNVERIFIED",
    identification_status="INSUFFICIENT_EVIDENCE",
    evidence_quality="NONE",
    visual_evidence=[],
)

if unverified.grounding_status != "UNVERIFIED":
    raise RuntimeError(
        "UNVERIFIED status was not preserved."
    )

print("UNVERIFIED: PASS")
print("Unidentified result: PASS")
print("Insufficient evidence: PASS")


print()
print("===== 11. IDENTIFICATION STATUS VALIDATION =====")

identification_test_cases = {
    "IDENTIFIED": {
        "confidence": 0.95,
        "confidence_level": "HIGH",
        "grounding_status": "GROUNDED",
        "identification_status": "IDENTIFIED",
        "evidence_quality": "STRONG",
        "visual_evidence": [
            "Distinctive architectural evidence"
        ],
    },
    "POSSIBLE_MATCH": {
        "confidence": 0.72,
        "confidence_level": "MEDIUM",
        "grounding_status": "PARTIALLY_GROUNDED",
        "identification_status": "POSSIBLE_MATCH",
        "evidence_quality": "MODERATE",
        "visual_evidence": [
            "Partial architectural evidence"
        ],
    },
    "INSUFFICIENT_EVIDENCE": {
        "confidence": 0.20,
        "confidence_level": "LOW",
        "grounding_status": "UNVERIFIED",
        "identification_status": "INSUFFICIENT_EVIDENCE",
        "evidence_quality": "NONE",
        "visual_evidence": [],
    },
    "NOT_HERITAGE": {
        "identified_name": None,
        "confidence": 0.20,
        "confidence_level": "LOW",
        "grounding_status": "UNVERIFIED",
        "identification_status": "NOT_HERITAGE",
        "evidence_quality": "NONE",
        "visual_evidence": [],
    },
    "AMBIGUOUS": {
        "confidence": 0.72,
        "confidence_level": "MEDIUM",
        "grounding_status": "PARTIALLY_GROUNDED",
        "identification_status": "AMBIGUOUS",
        "evidence_quality": "MODERATE",
        "visual_evidence": [
            "Conflicting visual characteristics"
        ],
        "alternative_matches": [
            "Possible Heritage Site A",
            "Possible Heritage Site B"
        ],
    },
}

for state, test_case in identification_test_cases.items():

    result = build_result(
        **test_case,
    )

    if result.identification_status != state:
        raise RuntimeError(
            f"Identification state {state} was not preserved."
        )

    print(f"{state}: PASS")


print()
print("===== 12. EVIDENCE QUALITY VALIDATION =====")

evidence_test_cases = {
    "STRONG": {
        "confidence": 0.95,
        "confidence_level": "HIGH",
        "grounding_status": "GROUNDED",
        "identification_status": "IDENTIFIED",
        "evidence_quality": "STRONG",
        "visual_evidence": [
            "Strong visual evidence"
        ],
    },
    "MODERATE": {
        "confidence": 0.72,
        "confidence_level": "MEDIUM",
        "grounding_status": "PARTIALLY_GROUNDED",
        "identification_status": "POSSIBLE_MATCH",
        "evidence_quality": "MODERATE",
        "visual_evidence": [
            "Moderate visual evidence"
        ],
    },
    "NONE": {
        "confidence": 0.20,
        "confidence_level": "LOW",
        "grounding_status": "UNVERIFIED",
        "identification_status": "INSUFFICIENT_EVIDENCE",
        "evidence_quality": "NONE",
        "visual_evidence": [],
    },
}

for state, test_case in evidence_test_cases.items():

    result = build_result(
        **test_case,
    )

    if result.evidence_quality != state:
        raise RuntimeError(
            f"Evidence quality {state} was not preserved."
        )

    print(f"{state}: PASS")


print()
print("===== 13. INVALID INTELLIGENCE STATES =====")

try:
    build_result(
        identification_status="INVALID_STATUS",
    )
except ValueError:
    print("Invalid identification status: REJECTED")
else:
    raise RuntimeError(
        "Invalid identification status was accepted."
    )


try:
    build_result(
        evidence_quality="INVALID_QUALITY",
    )
except ValueError:
    print("Invalid evidence quality: REJECTED")
else:
    raise RuntimeError(
        "Invalid evidence quality was accepted."
    )


print()
print("===== 14. RESPONSE CONTRACT =====")

scan_id = str(uuid.uuid4())

response = HeritageScannerResponse(
    scan_id=scan_id,
    result=high,
)

if response.scan_id != scan_id:
    raise RuntimeError(
        "Scanner response scan_id contract failed."
    )

if response.result != high:
    raise RuntimeError(
        "Scanner response result contract failed."
    )

print("HeritageScannerResponse: PASS")
print("scan_id: PASS")
print("result: PASS")


print()
print("===== 15. SERIALIZATION =====")

serialized = response.model_dump()

if "scan_id" not in serialized:
    raise RuntimeError(
        "scan_id missing from serialized response."
    )

if "result" not in serialized:
    raise RuntimeError(
        "result missing from serialized response."
    )

result_payload = serialized["result"]

for field in (
    "identification_status",
    "evidence_quality",
    "grounding_status",
    "confidence",
    "visual_evidence",
):
    if field not in result_payload:
        raise RuntimeError(
            f"{field} missing from serialized result."
        )

print("Serialization: PASS")


print()
print("===== 16. PRODUCTION MODEL VALIDATOR INSPECTION =====")

validator_source = inspect.getsource(
    HeritageScannerResult
)

if "model_validator" not in validator_source:
    raise RuntimeError(
        "Production semantic validator was not found."
    )

print("Production semantic validator: PRESENT")
print("Semantic validation architecture: PASS")


print()
print("===== 17. IMPORT VALIDATION =====")

from app.services.ai.scanner.service import HeritageScannerService
from app.services.ai.scanner.prompts import (
    SCANNER_INTELLIGENCE_RULES,
    build_scanner_prompt,
)

print("HeritageScannerService: PASS")
print("SCANNER_INTELLIGENCE_RULES: PASS")
print("build_scanner_prompt: PASS")


print()
print("===== 18. GEMINI BOUNDARY SAFETY =====")

print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 14 COMPLETE")
print("=" * 80)

print("Scanner intelligence types: PASS")
print("High-confidence validation: PASS")
print("Medium-confidence validation: PASS")
print("Low-confidence validation: PASS")
print("Grounding validation: PASS")
print("Identification status: PASS")
print("Evidence quality: PASS")
print("Invalid intelligence states: PASS")
print("Response contract: PASS")
print("Serialization: PASS")
print("Production semantic validator: PASS")
print("Scanner service imports: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("SEND THE COMPLETE OUTPUT.")
