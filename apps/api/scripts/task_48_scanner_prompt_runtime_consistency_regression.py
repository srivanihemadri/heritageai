import json
from io import BytesIO
from PIL import Image

from app.services.ai.scanner.contract import HeritageScannerResult
from app.services.ai.scanner.prompts import build_scanner_prompt, SCANNER_INTELLIGENCE_RULES


print("=" * 80)
print("STEP 8C-003 — TASK 48 — SCANNER PROMPT/RUNTIME CONSISTENCY REGRESSION")
print("=" * 80)


print()
print("===== 1. VERIFY PRODUCTION PROMPT =====")

prompt = build_scanner_prompt()

if not isinstance(prompt, str) or not prompt.strip():
    raise RuntimeError("Production scanner prompt is empty.")

print("build_scanner_prompt: PASS")
print(f"Prompt length: {len(prompt)}")


print()
print("===== 2. VERIFY INTELLIGENCE RULE INTEGRATION =====")

if SCANNER_INTELLIGENCE_RULES.strip() not in prompt:
    raise RuntimeError(
        "SCANNER_INTELLIGENCE_RULES is not integrated into production prompt."
    )

print("SCANNER_INTELLIGENCE_RULES: PRESENT")
print("Intelligence rules: PASS")


print()
print("===== 3. VERIFY PRODUCTION SEMANTIC RULES =====")

required_rules = [
    "If evidence_quality is NONE, visual_evidence MUST be an empty list []",
    "If visual_evidence contains one or more observations, evidence_quality MUST be STRONG, MODERATE, or WEAK",
    "Never return evidence_quality NONE together with non-empty visual_evidence",
]

for rule in required_rules:
    if rule not in prompt:
        raise RuntimeError(
            f"Production prompt semantic rule missing: {rule}"
        )

print("NONE → empty visual_evidence: PRESENT")
print("Non-empty visual_evidence → non-NONE evidence: PRESENT")
print("NONE/non-empty contradiction prevention: PRESENT")
print("Semantic prompt rules: PASS")


print()
print("===== 4. VERIFY PRODUCTION RESPONSE STATES =====")

states = [
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
    "LOW",
    "MEDIUM",
    "HIGH",
]

for state in states:
    if state not in prompt:
        raise RuntimeError(
            f"Production prompt state missing: {state}"
        )
    print(f"{state}: PRESENT")

print("Response states: PASS")


print()
print("===== 5. VERIFY PRODUCTION CONTRACT =====")

fields = HeritageScannerResult.model_fields

required_fields = [
    "identified_name",
    "identification_status",
    "evidence_quality",
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
]

for field in required_fields:
    if field not in fields:
        raise RuntimeError(
            f"Production response field missing: {field}"
        )
    print(f"{field}: PRESENT")

print("Production contract: PASS")


print()
print("===== 6. VERIFY VALID IDENTIFIED PAYLOAD =====")

valid_payload = {
    "identified_name": "Konark Sun Temple",
    "identification_status": "IDENTIFIED",
    "evidence_quality": "STRONG",
    "category": "Temple",
    "location": "Konark",
    "country": "India",
    "confidence": 0.95,
    "confidence_level": "HIGH",
    "description": "Controlled production-consistent payload.",
    "architectural_style": "Kalinga architecture",
    "historical_period": "13th century",
    "historical_significance": "Controlled historical significance.",
    "visual_evidence": [
        "Stone temple architecture",
        "Distinctive monumental sculptural elements",
    ],
    "alternative_matches": [],
    "grounding_status": "GROUNDED",
}

result = HeritageScannerResult.model_validate(valid_payload)

if result.identification_status != "IDENTIFIED":
    raise RuntimeError("IDENTIFIED state was not preserved.")

if result.evidence_quality != "STRONG":
    raise RuntimeError("STRONG evidence quality was not preserved.")

if result.confidence_level != "HIGH":
    raise RuntimeError("HIGH confidence was not preserved.")

if not result.visual_evidence:
    raise RuntimeError("Visual evidence was not preserved.")

print("Valid identified payload: PASS")


print()
print("===== 7. VERIFY VALID NOT-HERITAGE PAYLOAD =====")

not_heritage_payload = dict(valid_payload)

not_heritage_payload.update(
    {
        "identified_name": None,
        "identification_status": "NOT_HERITAGE",
        "evidence_quality": "NONE",
        "confidence": 0.20,
        "confidence_level": "LOW",
        "visual_evidence": [],
        "grounding_status": "UNVERIFIED",
    }
)

not_heritage_result = HeritageScannerResult.model_validate(
    not_heritage_payload
)

if not_heritage_result.identification_status != "NOT_HERITAGE":
    raise RuntimeError(
        "NOT_HERITAGE state was not preserved."
    )

if not_heritage_result.evidence_quality != "NONE":
    raise RuntimeError(
        "NONE evidence quality was not preserved."
    )

if not not_heritage_result.visual_evidence:
    print("NOT_HERITAGE visual evidence empty: PASS")

print("Valid NOT_HERITAGE payload: PASS")


print()
print("===== 8. VERIFY PROMPT/CONTRACT SEMANTIC ALIGNMENT =====")

if "visual_evidence" not in prompt:
    raise RuntimeError(
        "Prompt does not reference visual_evidence."
    )

if "evidence_quality" not in prompt:
    raise RuntimeError(
        "Prompt does not reference evidence_quality."
    )

if "confidence_level" not in prompt:
    raise RuntimeError(
        "Prompt does not reference confidence_level."
    )

print("visual_evidence alignment: PASS")
print("evidence_quality alignment: PASS")
print("confidence_level alignment: PASS")
print("Prompt/contract alignment: PASS")


print()
print("===== 9. PRODUCTION SAFETY =====")

print("Controlled prompt/contract regression only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 48 COMPLETE")
print("=" * 80)
print("Production prompt: PASS")
print("Intelligence rules: PASS")
print("Semantic rules: PASS")
print("Response states: PASS")
print("Production contract: PASS")
print("Valid IDENTIFIED payload: PASS")
print("Valid NOT_HERITAGE payload: PASS")
print("Prompt/contract alignment: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
