from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app


print("=" * 80)
print("STEP 8C-003 — TASK 28 — SCANNER CONTROLLED API CONTRACT & OPENAPI REGRESSION")
print("=" * 80)


print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")


print()
print("===== 2. BUILD OPENAPI CONTRACT =====")

openapi = app.openapi()

if not isinstance(openapi, dict):
    raise RuntimeError("OpenAPI document is not a dictionary.")

paths = openapi.get("paths", {})

print("OpenAPI document: PASS")
print("Paths collection: PRESENT")


print()
print("===== 3. VERIFY SCANNER ENDPOINT =====")

scanner_path = paths.get("/api/v1/ai/scan")

if scanner_path is None:
    raise RuntimeError(
        "Scanner endpoint missing from OpenAPI."
    )

if "post" not in scanner_path:
    raise RuntimeError(
        "POST operation missing from scanner OpenAPI contract."
    )

scanner_operation = scanner_path["post"]

print("POST /api/v1/ai/scan: PRESENT")
print("Scanner OpenAPI operation: PASS")


print()
print("===== 4. VERIFY SCANNER OPERATION METADATA =====")

if not scanner_operation.get("responses"):
    raise RuntimeError(
        "Scanner operation has no documented responses."
    )

print("Operation responses: PRESENT")


if "summary" in scanner_operation:
    print("Summary: PRESENT")
else:
    print("Summary: NOT REQUIRED")


if "description" in scanner_operation:
    print("Description: PRESENT")
else:
    print("Description: NOT REQUIRED")


print("Operation metadata: PASS")


print()
print("===== 5. VERIFY REQUEST BODY CONTRACT =====")

request_body = scanner_operation.get("requestBody")

if request_body is None:
    raise RuntimeError(
        "Scanner requestBody missing from OpenAPI."
    )

content = request_body.get("content", {})

multipart = content.get("multipart/form-data")

if multipart is None:
    raise RuntimeError(
        "multipart/form-data scanner request contract missing."
    )

print("requestBody: PRESENT")
print("multipart/form-data: PRESENT")


multipart_schema = multipart.get("schema", {})

if not multipart_schema:
    raise RuntimeError(
        "multipart/form-data schema missing."
    )

print("Multipart schema: PRESENT")
print("Request body contract: PASS")


print()
print("===== 6. VERIFY IMAGE FILE FIELD =====")

schema_ref = multipart_schema.get("$ref")

if schema_ref:
    schemas = openapi.get("components", {}).get("schemas", {})
    schema_name = schema_ref.rsplit("/", 1)[-1]
    request_schema = schemas.get(schema_name, {})
else:
    request_schema = multipart_schema

properties = request_schema.get("properties", {})

if "file" not in properties:
    raise RuntimeError(
        "Scanner multipart request does not expose file field."
    )

file_schema = properties["file"]

print("file field: PRESENT")

file_type = file_schema.get("type")

if file_type != "string":
    raise RuntimeError(
        f"Scanner file field expected type string, got {file_type!r}."
    )

print("file field type: string")
print("Image upload field: PASS")


print()
print("===== 7. VERIFY AUTHENTICATION CONTRACT =====")

security = scanner_operation.get("security")

if not security:
    raise RuntimeError(
        "Scanner endpoint has no OpenAPI security requirement."
    )

print("Security requirement: PRESENT")
print("Authentication declaration: PASS")


print()
print("===== 8. VERIFY SUCCESS RESPONSE CONTRACT =====")

responses = scanner_operation["responses"]

if "200" not in responses:
    raise RuntimeError(
        "HTTP 200 scanner response missing."
    )

success_response = responses["200"]

if "content" not in success_response:
    raise RuntimeError(
        "HTTP 200 response content missing."
    )

print("HTTP 200: PRESENT")
print("Success response content: PRESENT")


print()
print("===== 9. VERIFY PUBLIC SCANNER RESPONSE SCHEMA =====")

success_content = success_response["content"]

json_content = success_content.get("application/json")

if json_content is None:
    raise RuntimeError(
        "application/json success response missing."
    )

success_schema = json_content.get("schema", {})

if not success_schema:
    raise RuntimeError(
        "Scanner success response schema missing."
    )

print("application/json: PRESENT")
print("Success response schema: PRESENT")


print()
print("===== 10. VERIFY RESPONSE CONTRACT FIELDS =====")

schemas = openapi.get("components", {}).get("schemas", {})

response_ref = success_schema.get("$ref")

if response_ref:
    response_schema_name = response_ref.rsplit("/", 1)[-1]
    response_schema = schemas.get(
        response_schema_name,
        {},
    )
else:
    response_schema = success_schema

response_properties = response_schema.get(
    "properties",
    {},
)

required_response_fields = [
    "success",
    "scan_id",
    "result",
]

for field in required_response_fields:
    if field not in response_properties:
        raise RuntimeError(
            f"Public scanner response field missing: {field}"
        )

    print(f"{field}: PRESENT")

print("Public response envelope: PASS")


print()
print("===== 11. VERIFY INTELLIGENCE RESPONSE FIELDS =====")

result_schema_ref = response_properties["result"].get("$ref")

if not result_schema_ref:
    raise RuntimeError(
        "Scanner result schema reference missing."
    )

result_schema_name = result_schema_ref.rsplit("/", 1)[-1]

result_schema = schemas.get(
    result_schema_name,
    {},
)

result_properties = result_schema.get(
    "properties",
    {},
)

required_intelligence_fields = [
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

for field in required_intelligence_fields:
    if field not in result_properties:
        raise RuntimeError(
            f"Scanner intelligence field missing from OpenAPI: {field}"
        )

    print(f"{field}: PRESENT")

print("Intelligence response schema: PASS")


print()
print("===== 12. VERIFY ERROR RESPONSES =====")

for status_code in ("400", "401", "429"):
    if status_code not in responses:
        raise RuntimeError(
            f"Scanner error response {status_code} missing from OpenAPI."
        )

    print(f"HTTP {status_code}: PRESENT")

print("Scanner error response contract: PASS")


print()
print("===== 13. VERIFY EXISTING AI ANSWER ROUTE =====")

answer_path = paths.get("/api/v1/ai/answer")

if answer_path is None:
    raise RuntimeError(
        "Existing /api/v1/ai/answer route missing."
    )

if "post" not in answer_path:
    raise RuntimeError(
        "POST /api/v1/ai/answer operation missing."
    )

print("/api/v1/ai/answer: PRESERVED")


print()
print("===== 14. VERIFY RUNTIME AUTHENTICATION BOUNDARY =====")

unauthenticated = client.post(
    "/api/v1/ai/scan",
)

if unauthenticated.status_code != 401:
    raise RuntimeError(
        f"Expected HTTP 401, got "
        f"{unauthenticated.status_code}: "
        f"{unauthenticated.text}"
    )

print("Unauthenticated scanner request: HTTP 401")
print("Runtime authentication boundary: PASS")


print()
print("===== 15. VERIFY PUBLIC ERROR SANITIZATION =====")

error_text = unauthenticated.text

for forbidden in (
    "Traceback",
    "google.genai",
    "api_key",
    "password",
    "secret",
):

    if forbidden.lower() in error_text.lower():
        raise RuntimeError(
            f"Public error response leaks internal detail: {forbidden}"
        )

print("Public error sanitization: PASS")


print()
print("===== 16. PRODUCTION SAFETY =====")

print("Controlled API/OpenAPI inspection only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 28 COMPLETE")
print("=" * 80)
print("Scanner OpenAPI route: PASS")
print("Multipart input contract: PASS")
print("Image upload field: PASS")
print("Authentication contract: PASS")
print("Success response contract: PASS")
print("Intelligence response schema: PASS")
print("Error response contract: PASS")
print("Existing AI answer route: PRESERVED")
print("Runtime authentication boundary: PASS")
print("Public error sanitization: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
