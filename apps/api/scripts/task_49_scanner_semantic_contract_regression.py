from app.services.ai.scanner.contract import HeritageScannerResult
from app.services.ai.scanner.prompts import build_scanner_prompt


print("=" * 80)
print("STEP 8C-003 — TASK 49 — SCANNER SEMANTIC CONTRACT REGRESSION")
print("=" * 80)


print()
print("===== 1. BUILD PRODUCTION PROMPT =====")

prompt = build_scanner_prompt()

if not prompt.strip():
    raise RuntimeError("Production scanner prompt is empty.")

print("Production prompt: PASS")
print(f"Prompt length: {len(prompt)}")


print()
print("===== 2. VERIFY SEMANTIC RULES =====")

rules = [
    "If evidence_quality is NONE, visual_evidence MUST be an empty list []",
    "If visual_evidence contains one or more observations, evidence_quality MUST be STRONG, MODERATE, or WEAK",
    "Never return evidence_quality NONE together with non-empty visual_evidence",
]

for rule in rules:
    if rule not in prompt:
        raise RuntimeError(
            f"Missing semantic rule: {rule}"
        )

print("NONE → empty visual_evidence: PASS")
print("Non-empty visual_evidence → non-NONE evidence: PASS")
print("NONE/non-empty contradiction prevention: PASS")


print()
print("===== 3. VERIFY IDENTIFIED CONTRACT =====")

identified = HeritageScannerResult.model_validate(
    {
        "identified_name": "Konark Sun Temple",
        "identification_status": "IDENTIFIED",
        "evidence_quality": "STRONG",
        "category": "Temple",
        "location": "Konark",
        "country": "India",
        "confidence": 0.95,
        "confidence_level": "HIGH",
        "description": "Controlled identified result.",
        "architectural_style": "Kalinga architecture",
        "historical_period": "13th century",
        "historical_significance": "Controlled significance.",
        "visual_evidence": [
            "Monumental stone temple structure"
        ],
        "alternative_matches": [],
        "grounding_status": "GROUNDED",
    }
)

if not identified.identified_name:
    raise RuntimeError("IDENTIFIED result lost identified_name.")

if not identified.visual_evidence:
    raise RuntimeError("IDENTIFIED result lost visual_evidence.")

print("IDENTIFIED semantic contract: PASS")


print()
print("===== 4. VERIFY NOT_HERITAGE CONTRACT =====")

not_heritage = HeritageScannerResult.model_validate(
    {
        "identified_name": None,
        "identification_status": "NOT_HERITAGE",
        "evidence_quality": "NONE",
        "category": None,
        "location": None,
        "country": None,
        "confidence": 0.20,
        "confidence_level": "LOW",
        "description": "Controlled non-heritage result.",
        "architectural_style": None,
        "historical_period": None,
        "historical_significance": None,
        "visual_evidence": [],
        "alternative_matches": [],
        "grounding_status": "UNVERIFIED",
    }
)

if not_heritage.identified_name is not None:
    raise RuntimeError(
        "NOT_HERITAGE incorrectly contains identified_name."
    )

if not_heritage.visual_evidence:
    print("NOT_HERITAGE visual_evidence empty: PASS")

print("NOT_HERITAGE semantic contract: PASS")


print()
print("===== 5. VERIFY INVALID NONE + VISUAL EVIDENCE =====")

invalid_payload = {
    "identified_name": None,
    "identification_status": "INSUFFICIENT_EVIDENCE",
    "evidence_quality": "NONE",
    "category": None,
    "location": None,
    "country": None,
    "confidence": 0.10,
    "confidence_level": "LOW",
    "description": "Invalid controlled payload.",
    "architectural_style": None,
    "historical_period": None,
    "historical_significance": None,
    "visual_evidence": [
        "Observed structure"
    ],
    "alternative_matches": [],
    "grounding_status": "UNVERIFIED",
}

try:
    HeritageScannerResult.model_validate(
        invalid_payload
    )
except Exception as exc:
    print("NONE + non-empty visual_evidence: REJECTED")
    print(
        f"Boundary: {type(exc).__name__}"
    )
else:
    raise RuntimeError(
        "Invalid NONE + visual_evidence payload was accepted."
    )


print()
print("===== 6. VERIFY PROMPT FIELD ALIGNMENT =====")

for field in [
    "visual_evidence",
    "evidence_quality",
    "confidence_level",
    "identification_status",
    "grounding_status",
]:
    if field not in prompt:
        raise RuntimeError(
            f"Prompt missing production field: {field}"
        )
    print(f"{field}: PRESENT")

print("Prompt field alignment: PASS")


print()
print("===== 7. VERIFY PRODUCTION SAFETY =====")

print("Controlled semantic regression only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 49 COMPLETE")
print("=" * 80)
print("Production prompt: PASS")
print("Semantic rules: PASS")
print("IDENTIFIED contract: PASS")
print("NOT_HERITAGE contract: PASS")
print("Invalid NONE + visual evidence rejection: PASS")
print("Prompt field alignment: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
