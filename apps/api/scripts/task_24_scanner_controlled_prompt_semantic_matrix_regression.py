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
from app.services.ai.scanner.prompts import (
    SCANNER_INTELLIGENCE_RULES,
    build_scanner_prompt,
)


print("=" * 80)
print("STEP 8C-003 — TASK 24 — SCANNER CONTROLLED PROMPT/SEMANTIC MATRIX REGRESSION")
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


print()
print("===== 1. BUILD PRODUCTION PROMPT =====")

prompt = build_scanner_prompt()

if not isinstance(prompt, str):
    raise RuntimeError(
        "Production scanner prompt is not a string."
    )

if not prompt.strip():
    raise RuntimeError(
        "Production scanner prompt is empty."
    )

print("Prompt type: str")
print("Prompt length:", len(prompt))
print("Prompt construction: PASS")


print()
print("===== 2. VERIFY INTELLIGENCE RULE INTEGRATION =====")

if not SCANNER_INTELLIGENCE_RULES.strip():
    raise RuntimeError(
        "SCANNER_INTELLIGENCE_RULES is empty."
    )

if SCANNER_INTELLIGENCE_RULES not in prompt:
    raise RuntimeError(
        "SCANNER_INTELLIGENCE_RULES is not integrated into "
        "the generated scanner prompt."
    )

print("SCANNER_INTELLIGENCE_RULES integration: PASS")


print()
print("===== 3. VERIFY IDENTIFICATION STATES IN PROMPT =====")

identification_states = [
    "IDENTIFIED",
    "POSSIBLE_MATCH",
    "INSUFFICIENT_EVIDENCE",
    "NOT_HERITAGE",
    "AMBIGUOUS",
]

for state in identification_states:
    if state not in prompt:
        raise RuntimeError(
            f"Prompt missing identification state: {state}"
        )

    if state not in SCANNER_INTELLIGENCE_RULES:
        raise RuntimeError(
            f"Intelligence rules missing identification state: {state}"
        )

    print(f"{state}: PASS")

print("Identification prompt matrix: PASS")


print()
print("===== 4. VERIFY EVIDENCE STATES IN PROMPT =====")

evidence_states = [
    "STRONG",
    "MODERATE",
    "WEAK",
    "NONE",
]

for state in evidence_states:
    if state not in prompt:
        raise RuntimeError(
            f"Prompt missing evidence quality state: {state}"
        )

    if state not in SCANNER_INTELLIGENCE_RULES:
        raise RuntimeError(
            f"Intelligence rules missing evidence quality state: {state}"
        )

    print(f"{state}: PASS")

print("Evidence prompt matrix: PASS")


print()
print("===== 5. VERIFY GROUNDING STATES IN PROMPT =====")

grounding_states = [
    "GROUNDED",
    "PARTIALLY_GROUNDED",
    "UNVERIFIED",
]

for state in grounding_states:
    if state not in prompt:
        raise RuntimeError(
            f"Prompt missing grounding state: {state}"
        )

    if state not in SCANNER_INTELLIGENCE_RULES:
        raise RuntimeError(
            f"Intelligence rules missing grounding state: {state}"
        )

    print(f"{state}: PASS")

print("Grounding prompt matrix: PASS")


print()
print("===== 6. VERIFY PRODUCTION IDENTIFICATION CONTRACT =====")

production_identification = set(
    ScannerIdentificationStatus.__args__
)

expected_identification = set(
    identification_states
)

if production_identification != expected_identification:
    raise RuntimeError(
        "Prompt identification states do not match "
        "production identification contract."
    )

print("Prompt ↔ production identification alignment: PASS")


print()
print("===== 7. VERIFY PRODUCTION EVIDENCE CONTRACT =====")

production_evidence = set(
    ScannerEvidenceQuality.__args__
)

expected_evidence = set(
    evidence_states
)

if production_evidence != expected_evidence:
    raise RuntimeError(
        "Prompt evidence states do not match "
        "production evidence contract."
    )

print("Prompt ↔ production evidence alignment: PASS")


print()
print("===== 8. IDENTIFIED PROMPT/CONTRACT CASE =====")

identified = build_result(
    identification_status="IDENTIFIED",
    evidence_quality="STRONG",
    confidence=0.96,
    confidence_level="HIGH",
)

if identified.identification_status != "IDENTIFIED":
    raise RuntimeError(
        "IDENTIFIED contract case failed."
    )

if identified.evidence_quality != "STRONG":
    raise RuntimeError(
        "IDENTIFIED evidence case failed."
    )

print("IDENTIFIED + STRONG: PASS")


print()
print("===== 9. POSSIBLE_MATCH PROMPT/CONTRACT CASE =====")

possible = build_result(
    identification_status="POSSIBLE_MATCH",
    evidence_quality="MODERATE",
    confidence=0.72,
    confidence_level="MEDIUM",
    alternative_matches=[
        "Controlled Alternative"
    ],
)

if possible.identification_status != "POSSIBLE_MATCH":
    raise RuntimeError(
        "POSSIBLE_MATCH contract case failed."
    )

print("POSSIBLE_MATCH + MODERATE: PASS")


print()
print("===== 10. INSUFFICIENT_EVIDENCE CASE =====")

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
        "INSUFFICIENT_EVIDENCE contract case failed."
    )

print("INSUFFICIENT_EVIDENCE + NONE: PASS")


print()
print("===== 11. NOT_HERITAGE CASE =====")

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
        "NOT_HERITAGE contract case failed."
    )

print("NOT_HERITAGE + NONE: PASS")


print()
print("===== 12. AMBIGUOUS CASE =====")

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
        "AMBIGUOUS contract case failed."
    )

if len(ambiguous.alternative_matches) < 2:
    raise RuntimeError(
        "AMBIGUOUS case does not contain two alternatives."
    )

print("AMBIGUOUS + MODERATE: PASS")
print("Alternative matches >= 2: PASS")


print()
print("===== 13. PROMPT RESPONSE FIELD ALIGNMENT =====")

required_response_fields = [
    "identified_name",
    "category",
    "location",
    "country",
    "confidence",
    "confidence_level",
    "description",
    "architectural_style",
    "historical_period",
    "historical_significance",
    "visual_evidence",
    "alternative_matches",
    "grounding_status",
    "identification_status",
    "evidence_quality",
]

for field in required_response_fields:
    if field not in prompt:
        raise RuntimeError(
            f"Prompt missing response field: {field}"
        )

    print(f"{field}: PRESENT")

print("Prompt response field alignment: PASS")


print()
print("===== 14. VERIFY ANTI-HALLUCINATION GUIDANCE =====")

anti_hallucination_terms = [
    "Never invent",
    "Do not claim certainty",
    "Visual similarity alone does not constitute historical grounding",
]

for term in anti_hallucination_terms:
    if term not in prompt:
        raise RuntimeError(
            f"Prompt missing safety guidance: {term}"
        )

    print(f"{term}: PRESENT")

print("Anti-hallucination guidance: PASS")


print()
print("===== 15. VERIFY INVALID CONTRACT STATES ARE REJECTED =====")


def expect_rejected(label, **overrides):
    try:
        build_result(**overrides)
    except (ValidationError, ValueError):
        print(f"{label}: REJECTED")
        return

    raise RuntimeError(
        f"{label} was accepted but should have been rejected."
    )


expect_rejected(
    "Invalid identification status",
    identification_status="INVALID_STATUS",
)

expect_rejected(
    "Invalid evidence quality",
    evidence_quality="INVALID_QUALITY",
)

expect_rejected(
    "HIGH without identification",
    identified_name=None,
    identification_status="INSUFFICIENT_EVIDENCE",
    evidence_quality="NONE",
    confidence=0.96,
    confidence_level="HIGH",
    visual_evidence=[],
)

expect_rejected(
    "HIGH without visual evidence",
    identification_status="IDENTIFIED",
    evidence_quality="STRONG",
    confidence=0.96,
    confidence_level="HIGH",
    visual_evidence=[],
)

expect_rejected(
    "GROUNDED without evidence",
    grounding_status="GROUNDED",
    visual_evidence=[],
)

expect_rejected(
    "NOT_HERITAGE with identified_name",
    identification_status="NOT_HERITAGE",
    identified_name="Incorrect Heritage Claim",
)

expect_rejected(
    "AMBIGUOUS without alternatives",
    identification_status="AMBIGUOUS",
    identified_name=None,
    evidence_quality="MODERATE",
    confidence=0.68,
    confidence_level="MEDIUM",
    alternative_matches=[],
)

print("Prompt semantic rejection alignment: PASS")


print()
print("===== 16. VERIFY PROMPT IS JSON-OUTPUT ORIENTED =====")

required_json_terms = [
    "Return JSON only",
    '"identification_status"',
    '"evidence_quality"',
    '"grounding_status"',
]

for term in required_json_terms:
    if term not in prompt:
        raise RuntimeError(
            f"Prompt missing JSON contract term: {term}"
        )

    print(f"{term}: PRESENT")

print("JSON response contract guidance: PASS")


print()
print("===== 17. PRODUCTION SAFETY =====")

print("Controlled prompt/semantic matrix only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 24 COMPLETE")
print("=" * 80)
print("Prompt construction: PASS")
print("Intelligence rule integration: PASS")
print("Identification state alignment: PASS")
print("Evidence quality alignment: PASS")
print("Grounding state alignment: PASS")
print("Response field alignment: PASS")
print("Anti-hallucination guidance: PASS")
print("Semantic rejection alignment: PASS")
print("JSON response contract: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
