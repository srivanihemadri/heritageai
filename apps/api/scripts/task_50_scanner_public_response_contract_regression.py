from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)


print("=" * 80)
print("STEP 8C-003 — TASK 50 — SCANNER PUBLIC RESPONSE CONTRACT REGRESSION")
print("=" * 80)


print()
print("===== 1. VERIFY PUBLIC RESPONSE MODEL =====")

response_fields = HeritageScannerResponse.model_fields

for field in [
    "success",
    "scan_id",
    "result",
]:
    if field not in response_fields:
        raise RuntimeError(
            f"Public response field missing: {field}"
        )
    print(f"{field}: PRESENT")

print("Public response model: PASS")


print()
print("===== 2. BUILD CONTROLLED SCANNER RESULT =====")

result = HeritageScannerResult.model_validate(
    {
        "identified_name": "Konark Sun Temple",
        "identification_status": "IDENTIFIED",
        "evidence_quality": "STRONG",
        "category": "Temple",
        "location": "Konark",
        "country": "India",
        "confidence": 0.95,
        "confidence_level": "HIGH",
        "description": "Controlled public-response result.",
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

print("HeritageScannerResult: PASS")


print()
print("===== 3. BUILD PUBLIC RESPONSE =====")

response = HeritageScannerResponse(
    success=True,
    scan_id="task50-controlled-scan",
    result=result,
)

if response.success is not True:
    raise RuntimeError(
        "Public response success flag is incorrect."
    )

if response.scan_id != "task50-controlled-scan":
    raise RuntimeError(
        "Public response scan_id was not preserved."
    )

if not isinstance(response.result, HeritageScannerResult):
    raise RuntimeError(
        "Public response result is not HeritageScannerResult."
    )

print("success: PASS")
print("scan_id: PASS")
print("result: PASS")


print()
print("===== 4. VERIFY INTELLIGENCE FIELDS =====")

for field in [
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
]:
    if not hasattr(response.result, field):
        raise RuntimeError(
            f"Public intelligence field missing: {field}"
        )
    print(f"{field}: PRESENT")

print("Intelligence response contract: PASS")


print()
print("===== 5. VERIFY PUBLIC RESPONSE SERIALIZATION =====")

payload = response.model_dump()

if not isinstance(payload, dict):
    raise RuntimeError(
        "Public response did not serialize to dict."
    )

if payload["success"] is not True:
    raise RuntimeError(
        "Serialized success flag is incorrect."
    )

if payload["scan_id"] != "task50-controlled-scan":
    raise RuntimeError(
        "Serialized scan_id was not preserved."
    )

if not isinstance(payload["result"], dict):
    raise RuntimeError(
        "Serialized result is not an object."
    )

for field in [
    "identified_name",
    "identification_status",
    "evidence_quality",
    "visual_evidence",
    "confidence_level",
    "grounding_status",
]:
    if field not in payload["result"]:
        raise RuntimeError(
            f"Serialized result field missing: {field}"
        )

print("Public serialization: PASS")


print()
print("===== 6. VERIFY JSON ROUND TRIP =====")

json_payload = response.model_dump_json()

round_trip = HeritageScannerResponse.model_validate_json(
    json_payload
)

if round_trip.success != response.success:
    raise RuntimeError(
        "Round-trip success mismatch."
    )

if round_trip.scan_id != response.scan_id:
    raise RuntimeError(
        "Round-trip scan_id mismatch."
    )

if round_trip.result.identification_status != (
    response.result.identification_status
):
    raise RuntimeError(
        "Round-trip identification_status mismatch."
    )

if round_trip.result.evidence_quality != (
    response.result.evidence_quality
):
    raise RuntimeError(
        "Round-trip evidence_quality mismatch."
    )

if round_trip.result.confidence_level != (
    response.result.confidence_level
):
    raise RuntimeError(
        "Round-trip confidence_level mismatch."
    )

print("Pydantic JSON round trip: PASS")


print()
print("===== 7. VERIFY NO INTERNAL CLIENT DATA =====")

serialized = json_payload.lower()

for forbidden in [
    "api_key",
    "gemini_api_key",
    "access_token",
    "password",
]:
    if forbidden in serialized:
        raise RuntimeError(
            f"Sensitive field leaked into public response: {forbidden}"
        )

print("Sensitive-field boundary: PASS")


print()
print("===== 8. PRODUCTION SAFETY =====")

print("Controlled public-response regression only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 50 COMPLETE")
print("=" * 80)
print("Public response model: PASS")
print("Scanner result contract: PASS")
print("Public response envelope: PASS")
print("Intelligence fields: PASS")
print("Public serialization: PASS")
print("JSON round trip: PASS")
print("Sensitive-field boundary: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
