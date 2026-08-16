from __future__ import annotations

import json
import sys
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image

from app.services.ai.scanner.service import HeritageScannerService


print("=" * 80)
print("STEP 8C-003 — TASK 34 — SCANNER CONTROLLED RUNTIME FAILURE ISOLATION")
print("=" * 80)


print()
print("===== 1. BUILD CONTROLLED VALID IMAGE =====")

image = Image.new(
    "RGB",
    (2, 2),
    (120, 80, 40),
)

buffer = BytesIO()
image.save(buffer, format="PNG")
png_bytes = buffer.getvalue()

print(f"PNG bytes: {len(png_bytes)}")
print("Controlled image: PASS")


print()
print("===== 2. BUILD CONTROLLED VALID GEMINI PAYLOAD =====")

valid_payload = {
    "identified_name": "Konark Sun Temple",
    "category": "Temple",
    "location": "Konark",
    "country": "India",
    "confidence": 0.96,
    "confidence_level": "HIGH",
    "description": "Controlled scanner runtime result.",
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

valid_json = json.dumps(valid_payload)

print("Controlled Gemini JSON: PASS")


print()
print("===== 3. CREATE CONTROLLED GEMINI RESPONSE OBJECT =====")


class FakeResponse:
    def __init__(self, text):
        self.text = text


class FakeModels:
    def __init__(self, response):
        self.response = response

    def generate_content(
        self,
        *,
        model,
        contents,
        config,
    ):
        return self.response


class FakeClient:
    def __init__(self, response):
        self.models = FakeModels(response)


print("Fake Gemini response: PRESENT")
print("Fake Gemini client: PRESENT")
print("No real Gemini client: PASS")


print()
print("===== 4. CREATE CONTROLLED SCANNER SERVICE =====")

service = HeritageScannerService.__new__(
    HeritageScannerService
)

service.model = "controlled-test-model"
service.client = FakeClient(
    FakeResponse(valid_json)
)

print("HeritageScannerService: PASS")
print("Controlled client injection: PASS")


print()
print("===== 5. EXECUTE ACTUAL SCAN PIPELINE =====")

try:
    response = service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except Exception as exc:
    raise RuntimeError(
        "Valid controlled Gemini response failed during "
        f"the actual scan pipeline: "
        f"{type(exc).__name__}: {exc}"
    )

print("scan(): PASS")
print("Controlled Gemini → extraction → validation: PASS")


print()
print("===== 6. VERIFY PUBLIC RESPONSE =====")

if not response.success:
    raise RuntimeError(
        "Scanner response success flag is false."
    )

if not response.scan_id:
    raise RuntimeError(
        "Scanner response scan_id is missing."
    )

if response.result.identification_status != "IDENTIFIED":
    raise RuntimeError(
        "Identification status was not preserved."
    )

if response.result.evidence_quality != "STRONG":
    raise RuntimeError(
        "Evidence quality was not preserved."
    )

if response.result.grounding_status != "GROUNDED":
    raise RuntimeError(
        "Grounding status was not preserved."
    )

print("success: PASS")
print("scan_id: PASS")
print("result: PASS")
print("Intelligence fields: PASS")


print()
print("===== 7. CONTROLLED INVALID JSON RUNTIME =====")

service.client = FakeClient(
    FakeResponse(
        "This is not valid JSON."
    )
)

try:
    service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except ValueError as exc:
    print("Invalid JSON runtime: REJECTED")
    print(
        f"Failure boundary: ValueError"
    )
else:
    raise RuntimeError(
        "Invalid JSON unexpectedly passed runtime pipeline."
    )


print()
print("===== 8. CONTROLLED JSON ARRAY RUNTIME =====")

service.client = FakeClient(
    FakeResponse(
        '[{"identified_name":"test"}]'
    )
)

try:
    service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except ValueError as exc:
    print("JSON array runtime: REJECTED")
    print(
        "Failure boundary: ValueError"
    )
else:
    raise RuntimeError(
        "JSON array unexpectedly passed runtime pipeline."
    )


print()
print("===== 9. CONTROLLED EMPTY RESPONSE RUNTIME =====")

service.client = FakeClient(
    FakeResponse("")
)

try:
    service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except RuntimeError as exc:
    print("Empty response runtime: REJECTED")
    print(
        "Failure boundary: RuntimeError"
    )
else:
    raise RuntimeError(
        "Empty response unexpectedly passed runtime pipeline."
    )


print()
print("===== 10. CONTROLLED SCHEMA FAILURE RUNTIME =====")

invalid_schema_payload = dict(
    valid_payload
)

invalid_schema_payload.pop(
    "identification_status"
)

service.client = FakeClient(
    FakeResponse(
        json.dumps(
            invalid_schema_payload
        )
    )
)

try:
    service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except Exception as exc:
    print(
        "Invalid schema runtime: REJECTED"
    )
    print(
        f"Failure boundary: {type(exc).__name__}"
    )
else:
    raise RuntimeError(
        "Invalid schema unexpectedly passed runtime pipeline."
    )


print()
print("===== 11. DETERMINE RUNTIME PIPELINE BOUNDARY =====")

service.client = FakeClient(
    FakeResponse(valid_json)
)

try:
    final_response = service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except Exception as exc:
    raise RuntimeError(
        "Final controlled runtime verification failed: "
        f"{type(exc).__name__}: {exc}"
    )

if final_response.result.identified_name != (
    "Konark Sun Temple"
):
    raise RuntimeError(
        "Final identified_name was not preserved."
    )

print("Gemini response simulation: PASS")
print("response.text boundary: PASS")
print("_extract_json boundary: PASS")
print("Pydantic validation boundary: PASS")
print("HeritageScannerResponse boundary: PASS")


print()
print("===== 12. PRODUCTION SAFETY =====")

print("Actual Gemini SDK request: NONE")
print("Controlled fake Gemini response: ONLY")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 34 COMPLETE")
print("=" * 80)
print("Actual scan pipeline: PASS")
print("Controlled valid response: PASS")
print("Invalid JSON boundary: PASS")
print("JSON array boundary: PASS")
print("Empty response boundary: PASS")
print("Schema validation boundary: PASS")
print("Public response boundary: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
