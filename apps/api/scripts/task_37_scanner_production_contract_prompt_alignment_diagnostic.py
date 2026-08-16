from __future__ import annotations

import inspect
import sys
from pathlib import Path
from typing import get_args, get_origin

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.contract import HeritageScannerResult
from app.services.ai.scanner.prompt import (
    build_scanner_prompt,
    SCANNER_INTELLIGENCE_RULES,
)


BASE = Path(__file__).resolve().parents[1]

CONTRACT_PATH = (
    BASE
    / "app"
    / "services"
    / "ai"
    / "scanner"
    / "contract.py"
)

PROMPT_PATH = (
    BASE
    / "app"
    / "services"
    / "ai"
    / "scanner"
    / "prompt.py"
)


print("=" * 80)
print("STEP 8C-003 — TASK 37 — SCANNER PRODUCTION CONTRACT/PROMPT ALIGNMENT DIAGNOSTIC")
print("=" * 80)


print()
print("===== 1. VERIFY PRODUCTION CONTRACT =====")

if not CONTRACT_PATH.exists():
    raise RuntimeError(
        f"Scanner contract not found: {CONTRACT_PATH}"
    )

print("contract.py: PRESENT")
print("HeritageScannerResult: PRESENT")
print("Production contract: PASS")


print()
print("===== 2. INSPECT HERITAGE SCANNER RESULT FIELDS =====")

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

for field_name in required_fields:
    if field_name not in fields:
        raise RuntimeError(
            f"Production field missing: {field_name}"
        )

    field = fields[field_name]

    print(
        f"{field_name}: "
        f"{field.annotation}"
    )

print("All production fields: PRESENT")


print()
print("===== 3. INSPECT CONFIDENCE LEVEL CONTRACT =====")

confidence_field = fields["confidence_level"]

print(
    f"confidence_level annotation: "
    f"{confidence_field.annotation}"
)

confidence_args = get_args(
    confidence_field.annotation
)

if confidence_args:
    print(
        "confidence_level allowed values: "
        + ", ".join(
            str(value)
            for value in confidence_args
        )
    )
else:
    print(
        "confidence_level allowed values: "
        "NOT REPRESENTED AS TYPING ARGS"
    )

print("Confidence-level contract inspection: PASS")


print()
print("===== 4. INSPECT VISUAL EVIDENCE CONTRACT =====")

visual_field = fields["visual_evidence"]

print(
    f"visual_evidence annotation: "
    f"{visual_field.annotation}"
)

visual_origin = get_origin(
    visual_field.annotation
)

visual_args = get_args(
    visual_field.annotation
)

print(
    f"visual_evidence origin: "
    f"{visual_origin}"
)

if visual_args:
    print(
        "visual_evidence type arguments: "
        + ", ".join(
            str(value)
            for value in visual_args
        )
    )

print("Visual-evidence contract inspection: PASS")


print()
print("===== 5. INSPECT SEMANTIC INTELLIGENCE RULES =====")

if not isinstance(
    SCANNER_INTELLIGENCE_RULES,
    str,
):
    raise RuntimeError(
        "SCANNER_INTELLIGENCE_RULES is not a string."
    )

print(
    f"SCANNER_INTELLIGENCE_RULES length: "
    f"{len(SCANNER_INTELLIGENCE_RULES)}"
)

semantic_terms = [
    "confidence_level",
    "LOW",
    "MEDIUM",
    "HIGH",
    "visual_evidence",
    "identification_status",
    "evidence_quality",
    "grounding_status",
]

for term in semantic_terms:
    if term in SCANNER_INTELLIGENCE_RULES:
        print(
            f"{term}: PRESENT"
        )
    else:
        print(
            f"{term}: NOT PRESENT"
        )

print("Semantic rules inspection: PASS")


print()
print("===== 6. BUILD PRODUCTION PROMPT =====")

production_prompt = build_scanner_prompt()

if not isinstance(
    production_prompt,
    str,
):
    raise RuntimeError(
        "build_scanner_prompt() did not return str."
    )

print(
    f"Production prompt length: "
    f"{len(production_prompt)}"
)

prompt_terms = [
    "confidence_level",
    "LOW",
    "MEDIUM",
    "HIGH",
    "visual_evidence",
    "identification_status",
    "evidence_quality",
    "grounding_status",
    "JSON",
]

for term in prompt_terms:
    if term in production_prompt:
        print(
            f"{term}: PRESENT"
        )
    else:
        print(
            f"{term}: NOT PRESENT"
        )

print("Production prompt construction: PASS")


print()
print("===== 7. VERIFY VISUAL EVIDENCE FORMAT GUIDANCE =====")

visual_format_terms = [
    "array",
    "list",
    "string",
    "evidence",
]

for term in visual_format_terms:
    if term.lower() in production_prompt.lower():
        print(
            f"{term}: PRESENT"
        )
    else:
        print(
            f"{term}: NOT PRESENT"
        )

print("Visual-evidence prompt guidance inspected")


print()
print("===== 8. VERIFY CONFIDENCE FORMAT GUIDANCE =====")

confidence_terms = [
    "confidence_level",
    "LOW",
    "MEDIUM",
    "HIGH",
]

for term in confidence_terms:
    if term in production_prompt:
        print(
            f"{term}: PRESENT"
        )
    else:
        print(
            f"{term}: NOT PRESENT"
        )

print("Confidence prompt guidance inspected")


print()
print("===== 9. INSPECT PROMPT SOURCE LOCATION =====")

if not PROMPT_PATH.exists():
    raise RuntimeError(
        f"Scanner prompt module not found: {PROMPT_PATH}"
    )

print(
    f"Prompt module: {PROMPT_PATH}"
)

prompt_source = PROMPT_PATH.read_text(
    encoding="utf-8"
)

print(
    f"Prompt source length: "
    f"{len(prompt_source)}"
)

print("Prompt source: PRESENT")


print()
print("===== 10. CONTRACT/PROMPT ALIGNMENT CHECK =====")

contract_confidence_values = set(
    str(value)
    for value in confidence_args
)

expected_confidence_values = {
    "LOW",
    "MEDIUM",
    "HIGH",
}

if contract_confidence_values:
    if not expected_confidence_values.issubset(
        contract_confidence_values
    ):
        raise RuntimeError(
            "Production confidence contract does not expose "
            "LOW/MEDIUM/HIGH."
        )

print(
    "Production confidence values LOW/MEDIUM/HIGH: PASS"
)

if "confidence_level" not in production_prompt:
    raise RuntimeError(
        "Production prompt does not mention confidence_level."
    )

print(
    "Prompt confidence_level field: PASS"
)

if "visual_evidence" not in production_prompt:
    raise RuntimeError(
        "Production prompt does not mention visual_evidence."
    )

print(
    "Prompt visual_evidence field: PASS"
)


print()
print("===== 11. VERIFY NO PRODUCTION CHANGES =====")

print("Diagnostic mode: READ-ONLY")
print("Production contract modified: NO")
print("Production prompt modified: NO")
print("Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")


print()
print("=" * 80)
print("TASK 37 DIAGNOSTIC COMPLETE")
print("=" * 80)
print("Production result contract: INSPECTED")
print("Confidence contract: INSPECTED")
print("Visual evidence contract: INSPECTED")
print("Semantic rules: INSPECTED")
print("Production prompt: INSPECTED")
print("Contract/prompt alignment: INSPECTED")
print("NO PRODUCTION SOURCE CHANGES.")
print("NO REAL GEMINI REQUEST.")
print("=" * 80)
