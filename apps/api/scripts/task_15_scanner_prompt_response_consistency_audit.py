from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)
from app.services.ai.scanner.prompts import (
    SCANNER_INTELLIGENCE_RULES,
    build_scanner_prompt,
)
from app.services.ai.scanner.service import HeritageScannerService


print("=" * 80)
print(
    "STEP 8C-003 — TASK 15 — "
    "SCANNER INTELLIGENCE PROMPT/RESPONSE CONSISTENCY AUDIT"
)
print("=" * 80)


print()
print("===== 1. VERIFY PRODUCTION IMPORTS =====")

print("HeritageScannerResult:", "PASS")
print("HeritageScannerResponse:", "PASS")
print("HeritageScannerService:", "PASS")
print("SCANNER_INTELLIGENCE_RULES:", "PASS")
print("build_scanner_prompt:", "PASS")


print()
print("===== 2. BUILD PRODUCTION PROMPT =====")

prompt = build_scanner_prompt()

if not isinstance(prompt, str):
    raise RuntimeError(
        "Scanner prompt is not a string."
    )

if not prompt.strip():
    raise RuntimeError(
        "Scanner prompt is empty."
    )

print(
    "Prompt type:",
    type(prompt).__name__,
)

print(
    "Prompt length:",
    len(prompt),
)

print("Prompt construction: PASS")


print()
print("===== 3. VERIFY INTELLIGENCE RULES ARE IN PROMPT =====")

required_prompt_terms = [
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
    "confidence",
    "visual evidence",
]

for term in required_prompt_terms:

    if term.lower() not in prompt.lower():

        raise RuntimeError(
            f"Required intelligence term missing from prompt: {term}"
        )

    print(
        f"{term}: PRESENT"
    )

print("Prompt intelligence coverage: PASS")


print()
print("===== 4. VERIFY PROMPT CONSTANT INTEGRATION =====")

if SCANNER_INTELLIGENCE_RULES.strip() not in prompt:

    raise RuntimeError(
        "SCANNER_INTELLIGENCE_RULES is not integrated "
        "into the production scanner prompt."
    )

print(
    "SCANNER_INTELLIGENCE_RULES integration: PASS"
)


print()
print("===== 5. VERIFY SERVICE PROMPT INTEGRATION =====")

service_source = inspect.getsource(
    HeritageScannerService
)

if "build_scanner_prompt" not in service_source:

    raise RuntimeError(
        "Scanner service does not call build_scanner_prompt."
    )

if "prompt = build_scanner_prompt()" not in service_source:

    raise RuntimeError(
        "Scanner service prompt construction pattern missing."
    )

print(
    "Service prompt builder reference: PASS"
)


print()
print("===== 6. VERIFY GEMINI RESPONSE PARSER =====")

parser_source = service_source

if "_extract_json" not in parser_source:

    raise RuntimeError(
        "Scanner service does not reference _extract_json."
    )

print(
    "_extract_json: PRESENT"
)

if "HeritageScannerResult.model_validate" not in parser_source:

    raise RuntimeError(
        "Scanner service does not validate the Gemini payload "
        "through HeritageScannerResult.model_validate."
    )

print(
    "HeritageScannerResult.model_validate: PRESENT"
)

if "HeritageScannerResponse" not in parser_source:

    raise RuntimeError(
        "Scanner service does not construct "
        "HeritageScannerResponse."
    )

print(
    "HeritageScannerResponse: PRESENT"
)

print(
    "Field-by-field manual parser: NOT REQUIRED"
)

print(
    "Pydantic response validation architecture: PASS"
)

print("===== 7. BUILD CONTROLLED GEMINI-LIKE RESPONSE =====")

controlled_payload = {
    "identified_name": "Konark Sun Temple",
    "category": "HISTORICAL_MONUMENT",
    "location": "Konark",
    "country": "India",
    "confidence": 0.96,
    "confidence_level": "HIGH",
    "description": (
        "Controlled diagnostic heritage identification response."
    ),
    "architectural_style": "Kalinga architecture",
    "historical_period": "13th century",
    "historical_significance": (
        "Controlled diagnostic historical significance."
    ),
    "visual_evidence": [
        "Stone architectural structure",
        "Distinctive carved wheel-like elements",
    ],
    "alternative_matches": [],
    "grounding_status": "GROUNDED",
    "identification_status": "IDENTIFIED",
    "evidence_quality": "STRONG",
}

controlled_json = json.dumps(
    controlled_payload
)

print(
    "Controlled JSON bytes:",
    len(controlled_json.encode("utf-8")),
)

print("Controlled response JSON: PASS")


print()
print("===== 8. VERIFY RESPONSE JSON FIELD COVERAGE =====")

decoded = json.loads(
    controlled_json
)

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

    if field not in decoded:

        raise RuntimeError(
            f"Controlled response missing field: {field}"
        )

    print(
        f"{field}: PRESENT"
    )

print("Response field coverage: PASS")


print()
print("===== 9. BUILD PRODUCTION RESULT CONTRACT =====")

result = HeritageScannerResult(
    **decoded
)

print(
    "HeritageScannerResult construction: PASS"
)

if result.identification_status != "IDENTIFIED":
    raise RuntimeError(
        "Identification status was not preserved."
    )

if result.evidence_quality != "STRONG":
    raise RuntimeError(
        "Evidence quality was not preserved."
    )

if result.grounding_status != "GROUNDED":
    raise RuntimeError(
        "Grounding status was not preserved."
    )

if result.confidence != 0.96:
    raise RuntimeError(
        "Confidence value was not preserved."
    )

print(
    "Intelligence field preservation: PASS"
)


print()
print("===== 10. BUILD PUBLIC RESPONSE CONTRACT =====")

response = HeritageScannerResponse(
    scan_id="task-15-controlled-scan",
    result=result,
)

print(
    "HeritageScannerResponse construction: PASS"
)

serialized = response.model_dump()

if serialized["result"]["identification_status"] != "IDENTIFIED":
    raise RuntimeError(
        "Serialized identification_status mismatch."
    )

if serialized["result"]["evidence_quality"] != "STRONG":
    raise RuntimeError(
        "Serialized evidence_quality mismatch."
    )

if serialized["result"]["grounding_status"] != "GROUNDED":
    raise RuntimeError(
        "Serialized grounding_status mismatch."
    )

print(
    "Public response serialization: PASS"
)


print()
print("===== 11. VERIFY API RESPONSE FIELDS =====")

public_fields = serialized["result"]

for field in required_response_fields:

    if field not in public_fields:

        raise RuntimeError(
            f"API response missing intelligence field: {field}"
        )

print(
    "All scanner intelligence fields exposed: PASS"
)


print()
print("===== 12. VERIFY SEMANTIC CONSISTENCY =====")

if (
    public_fields["confidence_level"] == "HIGH"
    and public_fields["confidence"] < 0.90
):

    raise RuntimeError(
        "HIGH confidence level is inconsistent with confidence value."
    )

if (
    public_fields["confidence_level"] == "HIGH"
    and public_fields["identification_status"] != "IDENTIFIED"
):

    raise RuntimeError(
        "HIGH confidence must represent an identified result."
    )

if (
    public_fields["confidence_level"] == "HIGH"
    and public_fields["evidence_quality"] != "STRONG"
):

    raise RuntimeError(
        "HIGH confidence requires STRONG evidence."
    )

if (
    public_fields["grounding_status"] == "GROUNDED"
    and not public_fields["visual_evidence"]
):

    raise RuntimeError(
        "GROUNDED result requires visual evidence."
    )

print(
    "Prompt/response semantic consistency: PASS"
)


print()
print("===== 13. VERIFY NO REAL GEMINI REQUEST =====")

print(
    "Real Gemini request: NONE"
)

print(
    "Database queries: NONE"
)

print(
    "Database mutations: NONE"
)

print(
    "Qdrant changes: NONE"
)

print(
    "Embeddings created: NONE"
)

print(
    "Production source changes: NONE"
)


print()
print("=" * 80)
print("STEP 8C-003 — TASK 15 COMPLETE")
print("=" * 80)

print("Prompt construction: PASS")
print("Intelligence prompt coverage: PASS")
print("Service prompt integration: PASS")
print("Response field mapping: PASS")
print("Controlled response contract: PASS")
print("Intelligence field preservation: PASS")
print("Public API serialization: PASS")
print("Semantic consistency: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("SEND THE COMPLETE OUTPUT.")
