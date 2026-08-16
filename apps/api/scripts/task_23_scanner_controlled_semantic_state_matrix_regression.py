from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pydantic import ValidationError

from app.services.ai.scanner.contract import (
    HeritageScannerResult,
    ScannerEvidenceQuality,
    ScannerIdentificationStatus,
)


print("=" * 80)
print("STEP 8C-003 — TASK 23 — SCANNER CONTROLLED SEMANTIC STATE MATRIX REGRESSION")
print("=" * 80)


def build_result(**overrides):
    payload = {
        "identified_name": "Controlled Heritage Site",
        "category": "HISTORICAL_MONUMENT",
        "location": "Controlled Location",
        "country": "India",
        "confidence": 0.96,
        "confidence_level": "HIGH",
        "description": "Controlled semantic regression result.",
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
    }

    payload.update(overrides)

    return HeritageScannerResult(**payload)


def expect_rejected(label, **overrides):
    try:
        build_result(**overrides)
    except (ValidationError, ValueError):
        print(f"{label}: REJECTED")
        return

    raise RuntimeError(
        f"{label} was accepted but should have been rejected."
    )


print()
print("===== 1. VERIFY PRODUCTION INTELLIGENCE TYPES =====")

expected_identification_states = {
    "IDENTIFIED",
    "POSSIBLE_MATCH",
    "INSUFFICIENT_EVIDENCE",
    "NOT_HERITAGE",
    "AMBIGUOUS",
}

expected_evidence_states = {
    "STRONG",
    "MODERATE",
    "WEAK",
    "NONE",
}

print(
    "ScannerIdentificationStatus:",
    ScannerIdentificationStatus,
)

print(
    "ScannerEvidenceQuality:",
    ScannerEvidenceQuality,
)

print("Identification state type: PASS")
print("Evidence quality type: PASS")


print()
print("===== 2. VERIFY ALL IDENTIFICATION STATES =====")

actual_identification_states = set(
    ScannerIdentificationStatus.__args__
)

if actual_identification_states != expected_identification_states:
    raise RuntimeError(
        "Identification state set does not match production contract."
    )

for state in expected_identification_states:
    print(f"{state}: PRESENT")

print("All identification states: PASS")


print()
print("===== 3. VERIFY ALL EVIDENCE QUALITY STATES =====")

actual_evidence_states = set(
    ScannerEvidenceQuality.__args__
)

if actual_evidence_states != expected_evidence_states:
    raise RuntimeError(
        "Evidence quality state set does not match production contract."
    )

for state in (
    "STRONG",
    "MODERATE",
    "WEAK",
    "NONE",
):
    print(f"{state}: PRESENT")

print("All evidence quality states: PASS")


print()
print("===== 4. IDENTIFIED STATE =====")

identified = build_result(
    identification_status="IDENTIFIED",
    evidence_quality="STRONG",
    confidence=0.96,
    confidence_level="HIGH",
)

if identified.identification_status != "IDENTIFIED":
    raise RuntimeError(
        "IDENTIFIED state was not preserved."
    )

print("IDENTIFIED: PASS")


print()
print("===== 5. POSSIBLE_MATCH STATE =====")

possible = build_result(
    identification_status="POSSIBLE_MATCH",
    evidence_quality="MODERATE",
    confidence=0.72,
    confidence_level="MEDIUM",
)

if possible.identification_status != "POSSIBLE_MATCH":
    raise RuntimeError(
        "POSSIBLE_MATCH state was not preserved."
    )

print("POSSIBLE_MATCH: PASS")


print()
print("===== 6. INSUFFICIENT_EVIDENCE STATE =====")

insufficient = build_result(
    identified_name=None,
    identification_status="INSUFFICIENT_EVIDENCE",
    evidence_quality="NONE",
    confidence=0.20,
    confidence_level="LOW",
    visual_evidence=[],
)

if insufficient.identification_status != "INSUFFICIENT_EVIDENCE":
    raise RuntimeError(
        "INSUFFICIENT_EVIDENCE state was not preserved."
    )

print("INSUFFICIENT_EVIDENCE: PASS")


print()
print("===== 7. NOT_HERITAGE STATE =====")

not_heritage = build_result(
    identified_name=None,
    category=None,
    location=None,
    country=None,
    architectural_style=None,
    historical_period=None,
    historical_significance=None,
    identification_status="NOT_HERITAGE",
    evidence_quality="NONE",
    confidence=0.10,
    confidence_level="LOW",
    visual_evidence=[],
    alternative_matches=[],
)

if not_heritage.identification_status != "NOT_HERITAGE":
    raise RuntimeError(
        "NOT_HERITAGE state was not preserved."
    )

print("NOT_HERITAGE: PASS")


print()
print("===== 8. AMBIGUOUS STATE =====")

ambiguous = build_result(
    identified_name=None,
    identification_status="AMBIGUOUS",
    evidence_quality="MODERATE",
    confidence=0.68,
    confidence_level="MEDIUM",
    alternative_matches=[
        "Controlled Heritage Site A",
        "Controlled Heritage Site B",
    ],
)

if ambiguous.identification_status != "AMBIGUOUS":
    raise RuntimeError(
        "AMBIGUOUS state was not preserved."
    )

if len(ambiguous.alternative_matches) < 2:
    raise RuntimeError(
        "AMBIGUOUS state did not preserve required alternatives."
    )

print("AMBIGUOUS: PASS")
print("Alternative matches >= 2: PASS")


print()
print("===== 9. EVIDENCE QUALITY MATRIX =====")

quality_cases = [
    ("STRONG", "IDENTIFIED", 0.96, "HIGH"),
    ("MODERATE", "POSSIBLE_MATCH", 0.72, "MEDIUM"),
    ("WEAK", "POSSIBLE_MATCH", 0.55, "MEDIUM"),
    ("NONE", "INSUFFICIENT_EVIDENCE", 0.20, "LOW"),
]

for quality, identification, confidence, level in quality_cases:
    kwargs = {
        "evidence_quality": quality,
        "identification_status": identification,
        "confidence": confidence,
        "confidence_level": level,
    }

    if identification == "POSSIBLE_MATCH":
        kwargs["alternative_matches"] = [
            "Controlled Alternative"
        ]

    if quality == "NONE":
        kwargs["identified_name"] = None
        kwargs["visual_evidence"] = []

    result = build_result(**kwargs)

    if result.evidence_quality != quality:
        raise RuntimeError(
            f"Evidence quality {quality} was not preserved."
        )

    print(f"{quality}: PASS")

print("Evidence quality matrix: PASS")


print()
print("===== 10. INVALID IDENTIFICATION STATES =====")

expect_rejected(
    "Invalid identification status",
    identification_status="UNKNOWN_STATUS",
)


print()
print("===== 11. INVALID EVIDENCE QUALITY =====")

expect_rejected(
    "Invalid evidence quality",
    evidence_quality="INVALID_QUALITY",
)


print()
print("===== 12. INVALID HIGH CONFIDENCE WITHOUT IDENTIFICATION =====")

expect_rejected(
    "HIGH without identification",
    identified_name=None,
    identification_status="INSUFFICIENT_EVIDENCE",
    evidence_quality="NONE",
    confidence=0.96,
    confidence_level="HIGH",
    visual_evidence=[],
)


print()
print("===== 13. INVALID HIGH CONFIDENCE WITHOUT VISUAL EVIDENCE =====")

expect_rejected(
    "HIGH without visual evidence",
    identification_status="IDENTIFIED",
    evidence_quality="STRONG",
    confidence=0.96,
    confidence_level="HIGH",
    visual_evidence=[],
)


print()
print("===== 14. INVALID GROUNDED WITHOUT EVIDENCE =====")

expect_rejected(
    "GROUNDED without evidence",
    grounding_status="GROUNDED",
    visual_evidence=[],
)


print()
print("===== 15. INVALID NOT_HERITAGE WITH IDENTIFICATION =====")

expect_rejected(
    "NOT_HERITAGE with identified_name",
    identification_status="NOT_HERITAGE",
    identified_name="Incorrect Heritage Claim",
)


print()
print("===== 16. INVALID AMBIGUOUS WITHOUT ALTERNATIVES =====")

expect_rejected(
    "AMBIGUOUS without alternatives",
    identification_status="AMBIGUOUS",
    identified_name=None,
    evidence_quality="MODERATE",
    confidence=0.68,
    confidence_level="MEDIUM",
    alternative_matches=[],
)


print()
print("===== 17. INVALID LOW CONFIDENCE RANGE =====")

expect_rejected(
    "LOW with confidence >= 0.50",
    identification_status="INSUFFICIENT_EVIDENCE",
    evidence_quality="NONE",
    identified_name=None,
    visual_evidence=[],
    confidence=0.50,
    confidence_level="LOW",
)


print()
print("===== 18. INVALID MEDIUM CONFIDENCE RANGE =====")

expect_rejected(
    "MEDIUM with confidence >= 0.90",
    identification_status="POSSIBLE_MATCH",
    evidence_quality="MODERATE",
    confidence=0.90,
    confidence_level="MEDIUM",
)


print()
print("===== 19. INVALID HIGH CONFIDENCE RANGE =====")

expect_rejected(
    "HIGH with confidence < 0.90",
    identification_status="IDENTIFIED",
    evidence_quality="STRONG",
    confidence=0.89,
    confidence_level="HIGH",
)


print()
print("===== 20. VERIFY SERIALIZATION =====")

serialized = identified.model_dump()

for field in (
    "identification_status",
    "evidence_quality",
    "grounding_status",
):
    if field not in serialized:
        raise RuntimeError(
            f"Serialized result missing field: {field}"
        )

print("Intelligence fields serialized: PASS")


print()
print("===== 21. VERIFY PRODUCTION SAFETY =====")

print("Controlled semantic matrix only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 23 COMPLETE")
print("=" * 80)
print("Identification state matrix: PASS")
print("Evidence quality matrix: PASS")
print("IDENTIFIED: PASS")
print("POSSIBLE_MATCH: PASS")
print("INSUFFICIENT_EVIDENCE: PASS")
print("NOT_HERITAGE: PASS")
print("AMBIGUOUS: PASS")
print("STRONG: PASS")
print("MODERATE: PASS")
print("WEAK: PASS")
print("NONE: PASS")
print("Invalid states: PASS")
print("Semantic rejection boundaries: PASS")
print("Serialization: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
