from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)
from app.services.ai.scanner.service import HeritageScannerService


print("=" * 80)
print("STEP 8C-003 — TASK 25 — SCANNER CONTROLLED RESPONSE DESERIALIZATION & ROUND-TRIP REGRESSION")
print("=" * 80)


print()
print("===== 1. BUILD CONTROLLED GEMINI RESPONSE =====")

controlled_payload = {
    "identified_name": "Controlled Heritage Site",
    "category": "HISTORICAL_MONUMENT",
    "location": "Controlled Location",
    "country": "India",
    "confidence": 0.96,
    "confidence_level": "HIGH",
    "description": "Controlled heritage identification result.",
    "architectural_style": "Controlled architectural style",
    "historical_period": "Controlled historical period",
    "historical_significance": "Controlled historical significance",
    "visual_evidence": [
        "Distinctive architectural feature",
        "Visible historical structure",
    ],
    "alternative_matches": [],
    "grounding_status": "GROUNDED",
    "identification_status": "IDENTIFIED",
    "evidence_quality": "STRONG",
}

controlled_json = json.dumps(
    controlled_payload
)

print("Controlled Gemini JSON: PASS")
print(
    "Controlled JSON bytes:",
    len(controlled_json.encode("utf-8")),
)


print()
print("===== 2. VERIFY JSON EXTRACTION =====")

service_extract = HeritageScannerService._extract_json

extracted = service_extract(
    controlled_json,
)

if not isinstance(extracted, dict):
    raise RuntimeError(
        "Extracted JSON is not a dictionary."
    )

if extracted != controlled_payload:
    raise RuntimeError(
        "Extracted JSON does not match controlled payload."
    )

print("_extract_json(): PASS")
print("JSON object preservation: PASS")


print()
print("===== 3. BUILD PRODUCTION RESULT =====")

result = HeritageScannerResult.model_validate(
    extracted
)

if not isinstance(result, HeritageScannerResult):
    raise RuntimeError(
        "Production result is not HeritageScannerResult."
    )

print("HeritageScannerResult: PASS")
print("Production validation: PASS")


print()
print("===== 4. VERIFY INTELLIGENCE FIELDS =====")

if result.identification_status != "IDENTIFIED":
    raise RuntimeError(
        "identification_status was not preserved."
    )

if result.evidence_quality != "STRONG":
    raise RuntimeError(
        "evidence_quality was not preserved."
    )

if result.grounding_status != "GROUNDED":
    raise RuntimeError(
        "grounding_status was not preserved."
    )

print("identification_status: PASS")
print("evidence_quality: PASS")
print("grounding_status: PASS")


print()
print("===== 5. VERIFY ALL RESPONSE FIELDS =====")

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

result_dict = result.model_dump()

for field in required_fields:
    if field not in result_dict:
        raise RuntimeError(
            f"Production result missing field: {field}"
        )

    print(f"{field}: PRESENT")

print("Production field preservation: PASS")


print()
print("===== 6. BUILD PUBLIC RESPONSE =====")

response = HeritageScannerResponse(
    success=True,
    scan_id="task-25-controlled-scan",
    result=result,
)

if not isinstance(response, HeritageScannerResponse):
    raise RuntimeError(
        "Public response is not HeritageScannerResponse."
    )

print("HeritageScannerResponse: PASS")
print("scan_id: PASS")
print("Public result: PASS")


print()
print("===== 7. SERIALIZE PUBLIC RESPONSE =====")

serialized = response.model_dump()

if serialized["success"] is not True:
    raise RuntimeError(
        "success field was not preserved."
    )

if serialized["scan_id"] != "task-25-controlled-scan":
    raise RuntimeError(
        "scan_id was not preserved."
    )

for field in required_fields:
    if field not in serialized["result"]:
        raise RuntimeError(
            f"Serialized response missing field: {field}"
        )

print("Public serialization: PASS")
print("scan_id preservation: PASS")
print("All result fields preserved: PASS")


print()
print("===== 8. JSON SERIALIZATION =====")

serialized_json = json.dumps(
    serialized
)

if not serialized_json:
    raise RuntimeError(
        "Serialized JSON is empty."
    )

print("JSON serialization: PASS")
print(
    "Serialized JSON bytes:",
    len(serialized_json.encode("utf-8")),
)


print()
print("===== 9. JSON DESERIALIZATION =====")

decoded = json.loads(
    serialized_json
)

if not isinstance(decoded, dict):
    raise RuntimeError(
        "Decoded response is not a dictionary."
    )

print("JSON deserialization: PASS")


print()
print("===== 10. REBUILD RESULT FROM DESERIALIZED JSON =====")

round_trip_result = HeritageScannerResult.model_validate(
    decoded["result"]
)

if not isinstance(
    round_trip_result,
    HeritageScannerResult,
):
    raise RuntimeError(
        "Round-trip result is not HeritageScannerResult."
    )

print("Round-trip HeritageScannerResult: PASS")


print()
print("===== 11. REBUILD PUBLIC RESPONSE =====")

round_trip_response = HeritageScannerResponse(
    success=decoded["success"],
    scan_id=decoded["scan_id"],
    result=round_trip_result,
)

if round_trip_response.scan_id != response.scan_id:
    raise RuntimeError(
        "scan_id changed during round trip."
    )

print("Round-trip HeritageScannerResponse: PASS")


print()
print("===== 12. VERIFY EXACT ROUND TRIP =====")

original_result = response.result.model_dump()
round_trip_result_dict = (
    round_trip_response.result.model_dump()
)

if original_result != round_trip_result_dict:
    raise RuntimeError(
        "Result changed during JSON round trip."
    )

if response.model_dump() != round_trip_response.model_dump():
    raise RuntimeError(
        "Public response changed during JSON round trip."
    )

print("Result equality: PASS")
print("Response equality: PASS")
print("Exact JSON round trip: PASS")


print()
print("===== 13. VERIFY INTELLIGENCE FIELD ROUND TRIP =====")

for field in (
    "identification_status",
    "evidence_quality",
    "grounding_status",
):
    original_value = getattr(
        response.result,
        field,
    )

    round_trip_value = getattr(
        round_trip_response.result,
        field,
    )

    if original_value != round_trip_value:
        raise RuntimeError(
            f"{field} changed during round trip."
        )

    print(f"{field}: PASS")


print()
print("===== 14. VERIFY SERVICE EXTRACTION BOUNDARY =====")

if "_extract_json" not in dir(
    HeritageScannerService
):
    raise RuntimeError(
        "HeritageScannerService._extract_json missing."
    )

print("_extract_json boundary: PASS")
print("Pydantic validation boundary: PASS")
print("Public response boundary: PASS")


print()
print("===== 15. PRODUCTION SAFETY =====")

print("Controlled response round trip only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 25 COMPLETE")
print("=" * 80)
print("Controlled Gemini JSON: PASS")
print("JSON extraction: PASS")
print("Production result validation: PASS")
print("Public response construction: PASS")
print("Serialization: PASS")
print("Deserialization: PASS")
print("Result round trip: PASS")
print("Response round trip: PASS")
print("Intelligence field preservation: PASS")
print("Exact round-trip equality: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)

