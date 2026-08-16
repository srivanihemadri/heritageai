from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.prompts import (
    SCANNER_INTELLIGENCE_RULES,
    build_scanner_prompt,
)
from app.services.ai.scanner.contract import HeritageScannerResult


print("=" * 80)
print("STEP 8C-003 — TASK 38 — SCANNER CONTROLLED PROMPT/RESPONSE SCHEMA REGRESSION")
print("=" * 80)

print()
print("===== 1. VERIFY PRODUCTION CONTRACT =====")

fields = HeritageScannerResult.model_fields

required_fields = [
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

for field in required_fields:
    if field not in fields:
        raise RuntimeError(
            f"Production response field missing: {field}"
        )
    print(f"{field}: PRESENT")

print("Production response contract: PASS")


print()
print("===== 2. BUILD PRODUCTION PROMPT =====")

prompt = build_scanner_prompt()

if not isinstance(prompt, str) or not prompt.strip():
    raise RuntimeError(
        "Production scanner prompt is empty."
    )

print(f"Prompt length: {len(prompt)}")
print("Prompt construction: PASS")


print()
print("===== 3. VERIFY INTELLIGENCE RULE INTEGRATION =====")

if SCANNER_INTELLIGENCE_RULES.strip() not in prompt:
    raise RuntimeError(
        "SCANNER_INTELLIGENCE_RULES is not integrated."
    )

print("SCANNER_INTELLIGENCE_RULES: PRESENT")
print("Intelligence rule integration: PASS")


print()
print("===== 4. VERIFY IDENTIFICATION STATES =====")

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
            f"Identification state missing from prompt: {state}"
        )
    print(f"{state}: PRESENT")

print("Identification state prompt contract: PASS")


print()
print("===== 5. VERIFY EVIDENCE QUALITY STATES =====")

evidence_states = [
    "STRONG",
    "MODERATE",
    "WEAK",
    "NONE",
]

for state in evidence_states:
    if state not in prompt:
        raise RuntimeError(
            f"Evidence state missing from prompt: {state}"
        )
    print(f"{state}: PRESENT")

print("Evidence quality prompt contract: PASS")


print()
print("===== 6. VERIFY GROUNDING STATES =====")

grounding_states = [
    "GROUNDED",
    "PARTIALLY_GROUNDED",
    "UNVERIFIED",
]

for state in grounding_states:
    if state not in prompt:
        raise RuntimeError(
            f"Grounding state missing from prompt: {state}"
        )
    print(f"{state}: PRESENT")

print("Grounding state prompt contract: PASS")


print()
print("===== 7. VERIFY CONFIDENCE LEVEL CONTRACT =====")

confidence_levels = [
    "LOW",
    "MEDIUM",
    "HIGH",
]

if "confidence_level" not in prompt:
    raise RuntimeError(
        "confidence_level missing from production prompt."
    )

for level in confidence_levels:
    if level not in prompt:
        raise RuntimeError(
            f"Confidence level missing from prompt: {level}"
        )
    print(f"{level}: PRESENT")

print("Confidence-level prompt contract: PASS")


print()
print("===== 8. VERIFY VISUAL EVIDENCE CONTRACT =====")

if "visual_evidence" not in prompt:
    raise RuntimeError(
        "visual_evidence missing from production prompt."
    )

visual_guidance_terms = ["visual evidence", "evidence"]

for term in visual_guidance_terms:
    if term.lower() not in prompt.lower():
        raise RuntimeError(
            f"Visual evidence guidance missing: {term}"
        )
    print(f"{term}: PRESENT")

print("Visual evidence prompt contract: PASS")


print()
print("===== 9. VERIFY JSON RESPONSE CONTRACT =====")

json_terms = [
    "Return JSON only.",
    '"identified_name"',
    '"category"',
    '"location"',
    '"country"',
    '"confidence"',
    '"confidence_level"',
    '"description"',
    '"architectural_style"',
    '"historical_period"',
    '"historical_significance"',
    '"visual_evidence"',
    '"alternative_matches"',
    '"grounding_status"',
    '"identification_status"',
    '"evidence_quality"',
]

for term in json_terms:
    if term not in prompt:
        raise RuntimeError(
            f"JSON response contract term missing: {term}"
        )
    print(f"{term}: PRESENT")

print("JSON response contract: PASS")


print()
print("===== 10. VERIFY ANTI-HALLUCINATION GUIDANCE =====")

anti_hallucination_terms = [
    "Never invent",
    "Do not claim certainty",
    "Visual similarity alone does not constitute historical grounding",
]

for term in anti_hallucination_terms:
    if term not in prompt:
        raise RuntimeError(
            f"Anti-hallucination guidance missing: {term}"
        )
    print(f"{term}: PRESENT")

print("Anti-hallucination guidance: PASS")


print()
print("===== 11. VERIFY PRODUCTION SCHEMA ALIGNMENT =====")

schema_prompt_fields = [
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

for field in schema_prompt_fields:
    if field not in prompt:
        raise RuntimeError(
            f"Prompt/schema alignment failure: {field}"
        )

print("All production fields represented in prompt: PASS")


print()
print("===== 12. PRODUCTION SAFETY =====")

print("Controlled prompt/schema inspection only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 38 COMPLETE")
print("=" * 80)
print("Production response contract: PASS")
print("Prompt construction: PASS")
print("Intelligence rules: PASS")
print("Identification states: PASS")
print("Evidence states: PASS")
print("Grounding states: PASS")
print("Confidence-level contract: PASS")
print("Visual-evidence contract: PASS")
print("JSON response contract: PASS")
print("Anti-hallucination guidance: PASS")
print("Schema alignment: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)



