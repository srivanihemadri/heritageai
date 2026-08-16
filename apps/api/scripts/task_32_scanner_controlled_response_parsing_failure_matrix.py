from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.service import HeritageScannerService
from app.services.ai.scanner.contract import HeritageScannerResult


print("=" * 80)
print("STEP 8C-003 — TASK 32 — SCANNER CONTROLLED RESPONSE PARSING FAILURE MATRIX")
print("=" * 80)


service = HeritageScannerService.__new__(
    HeritageScannerService
)


print()
print("===== 1. VERIFY SCANNER EXTRACTION BOUNDARY =====")

if not hasattr(
    HeritageScannerService,
    "_extract_json",
):
    raise RuntimeError(
        "_extract_json() not found."
    )

print("_extract_json(): PRESENT")
print("Extraction boundary: PASS")


print()
print("===== 2. BUILD CONTROLLED VALID PAYLOAD =====")

valid_payload = {
    "identified_name": "Konark Sun Temple",
    "category": "Temple",
    "location": "Konark",
    "country": "India",
    "confidence": 0.96,
    "confidence_level": "HIGH",
    "description": "Controlled heritage test result.",
    "architectural_style": "Kalinga architecture",
    "historical_period": "13th century",
    "historical_significance": "Controlled historical significance.",
    "visual_evidence": [
        "Stone temple structure",
        "Distinctive architectural elements",
    ],
    "alternative_matches": [],
    "grounding_status": "GROUNDED",
    "identification_status": "IDENTIFIED",
    "evidence_quality": "STRONG",
}

import json

valid_json = json.dumps(
    valid_payload
)

print("Controlled payload: PASS")
print(f"JSON length: {len(valid_json)}")


print()
print("===== 3. VALID JSON OBJECT =====")

try:
    extracted = service._extract_json(
        valid_json
    )
except Exception as exc:
    raise RuntimeError(
        f"Valid JSON unexpectedly failed: "
        f"{type(exc).__name__}: {exc}"
    )

if extracted != valid_payload:
    raise RuntimeError(
        "Valid JSON object was not preserved."
    )

print("Valid JSON object: PASS")


print()
print("===== 4. JSON FENCED RESPONSE =====")

fenced_json = (
    "```json\n"
    + valid_json
    + "\n```"
)

try:
    extracted = service._extract_json(
        fenced_json
    )
except Exception as exc:
    raise RuntimeError(
        f"Fenced JSON unexpectedly failed: "
        f"{type(exc).__name__}: {exc}"
    )

if extracted != valid_payload:
    raise RuntimeError(
        "Fenced JSON was not preserved."
    )

print("```json fenced response: PASS")


print()
print("===== 5. JSON WITH SURROUNDING TEXT =====")

surrounded_json = (
    "Here is the scanner result:\n"
    + valid_json
    + "\nEnd of response."
)

try:
    extracted = service._extract_json(
        surrounded_json
    )
except Exception as exc:
    raise RuntimeError(
        f"Surrounded JSON unexpectedly failed: "
        f"{type(exc).__name__}: {exc}"
    )

if extracted != valid_payload:
    raise RuntimeError(
        "JSON extraction from surrounding text failed."
    )

print("JSON surrounded by text: PASS")


print()
print("===== 6. INVALID JSON =====")

try:
    service._extract_json(
        '{"identified_name": "broken"'
    )
except ValueError as exc:
    print(
        "Invalid JSON: REJECTED"
    )
    print(
        f"ValueError message: {exc}"
    )
else:
    raise RuntimeError(
        "Invalid JSON was accepted."
    )


print()
print("===== 7. JSON ARRAY =====")

try:
    service._extract_json(
        '[{"identified_name": "test"}]'
    )
except ValueError as exc:
    print(
        "JSON array: REJECTED"
    )
    print(
        f"ValueError message: {exc}"
    )
else:
    raise RuntimeError(
        "JSON array was accepted as scanner object."
    )


print()
print("===== 8. EMPTY RESPONSE =====")

try:
    service._extract_json("")
except ValueError as exc:
    print(
        "Empty response: REJECTED"
    )
    print(
        f"ValueError message: {exc}"
    )
else:
    raise RuntimeError(
        "Empty response was accepted."
    )


print()
print("===== 9. NON-JSON RESPONSE =====")

try:
    service._extract_json(
        "The building appears to be a temple."
    )
except ValueError as exc:
    print(
        "Non-JSON response: REJECTED"
    )
    print(
        f"ValueError message: {exc}"
    )
else:
    raise RuntimeError(
        "Non-JSON response was accepted."
    )


print()
print("===== 10. VALID JSON → PRODUCTION RESULT =====")

try:
    result = HeritageScannerResult.model_validate(
        valid_payload
    )
except Exception as exc:
    raise RuntimeError(
        f"Controlled valid payload failed production "
        f"validation: {type(exc).__name__}: {exc}"
    )

print("HeritageScannerResult validation: PASS")
print(
    f"Identification status: "
    f"{result.identification_status}"
)
print(
    f"Evidence quality: "
    f"{result.evidence_quality}"
)
print(
    f"Grounding status: "
    f"{result.grounding_status}"
)


print()
print("===== 11. INVALID PRODUCTION RESULT =====")

invalid_payload = dict(
    valid_payload
)

invalid_payload.pop(
    "identification_status"
)

try:
    HeritageScannerResult.model_validate(
        invalid_payload
    )
except Exception as exc:
    print(
        "Invalid production payload: REJECTED"
    )
    print(
        f"Validation exception: "
        f"{type(exc).__name__}"
    )
else:
    raise RuntimeError(
        "Invalid production payload was accepted."
    )


print()
print("===== 12. DETERMINE PARSING BOUNDARY =====")

print(
    "Valid JSON extraction: PASS"
)
print(
    "Fenced JSON extraction: PASS"
)
print(
    "Surrounded JSON extraction: PASS"
)
print(
    "Invalid JSON rejection: PASS"
)
print(
    "Non-object rejection: PASS"
)
print(
    "Empty response rejection: PASS"
)
print(
    "Pydantic validation boundary: PASS"
)


print()
print("===== 13. PRODUCTION SAFETY =====")

print(
    "Controlled response parsing only: PASS"
)
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
print("TASK 32 COMPLETE")
print("=" * 80)
print("JSON extraction: PASS")
print("Invalid JSON rejection: PASS")
print("Non-object rejection: PASS")
print("Empty response rejection: PASS")
print("Pydantic validation boundary: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
