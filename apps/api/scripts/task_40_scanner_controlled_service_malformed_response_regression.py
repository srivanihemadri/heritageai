from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image
from io import BytesIO

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.service import HeritageScannerService
from app.services.ai.scanner.contract import HeritageScannerResult


print("=" * 80)
print("STEP 8C-003 — TASK 40 — SCANNER CONTROLLED SERVICE MALFORMED RESPONSE REGRESSION")
print("=" * 80)


print()
print("===== 1. BUILD CONTROLLED IMAGE =====")

buffer = BytesIO()
Image.new("RGB", (1, 1), "white").save(buffer, format="PNG")
png_bytes = buffer.getvalue()

print(f"PNG bytes: {len(png_bytes)}")
print("Controlled image: PASS")


print()
print("===== 2. BUILD VALID CONTROLLED GEMINI PAYLOAD =====")

valid_payload = {
    "identified_name": "Konark Sun Temple",
    "identification_status": "IDENTIFIED",
    "evidence_quality": "STRONG",
    "category": "Temple",
    "location": "Konark",
    "country": "India",
    "confidence": 0.96,
    "confidence_level": "HIGH",
    "description": "Controlled heritage monument.",
    "architectural_style": "Kalinga architecture",
    "historical_period": "13th century",
    "historical_significance": "Controlled historical significance.",
    "visual_evidence": [
        "Stone architectural structure",
        "Distinctive temple features",
    ],
    "alternative_matches": [],
    "grounding_status": "GROUNDED",
}

valid_json = json.dumps(valid_payload)

print("Controlled Gemini JSON: PASS")


print()
print("===== 3. CREATE CONTROLLED GEMINI RESPONSE =====")


class FakeResponse:
    def __init__(self, text: str):
        self.text = text


class FakeModels:
    def __init__(self, response: FakeResponse):
        self.response = response

    def generate_content(self, **kwargs):
        return self.response


class FakeClient:
    def __init__(self, response: FakeResponse):
        self.models = FakeModels(response)


print("Fake Gemini response: PRESENT")
print("Fake Gemini client: PRESENT")


print()
print("===== 4. CREATE SCANNER SERVICE WITHOUT REAL CLIENT =====")

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
print("===== 5. VALID RESPONSE RUNTIME =====")

try:
    response = service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except Exception as exc:
    raise RuntimeError(
        f"Valid controlled scan failed: "
        f"{type(exc).__name__}: {exc}"
    )

if not response.success:
    raise RuntimeError(
        "Controlled scanner response success flag is false."
    )

if response.result.identified_name != "Konark Sun Temple":
    raise RuntimeError(
        "Controlled identified_name was not preserved."
    )

print("Valid controlled scan: PASS")
print("Extraction → validation → public response: PASS")


print()
print("===== 6. INVALID JSON RUNTIME =====")

service.client = FakeClient(
    FakeResponse("This is not valid JSON.")
)

try:
    service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except ValueError as exc:
    print("Invalid JSON: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "Invalid JSON unexpectedly passed."
    )


print()
print("===== 7. JSON ARRAY RUNTIME =====")

service.client = FakeClient(
    FakeResponse('[{"identified_name":"test"}]')
)

try:
    service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except ValueError as exc:
    print("JSON array: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "JSON array unexpectedly passed."
    )


print()
print("===== 8. INVALID CONFIDENCE LEVEL RUNTIME =====")

invalid_confidence = dict(valid_payload)
invalid_confidence["confidence_level"] = "NONE"

service.client = FakeClient(
    FakeResponse(
        json.dumps(invalid_confidence)
    )
)

try:
    service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except Exception as exc:
    print("Invalid confidence_level: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "Invalid confidence_level unexpectedly passed."
    )


print()
print("===== 9. INVALID VISUAL EVIDENCE TYPE RUNTIME =====")

invalid_visual = dict(valid_payload)
invalid_visual["visual_evidence"] = (
    "single string instead of list"
)

service.client = FakeClient(
    FakeResponse(
        json.dumps(invalid_visual)
    )
)

try:
    service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except Exception as exc:
    print("Invalid visual_evidence: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "Invalid visual_evidence unexpectedly passed."
    )


print()
print("===== 10. EMPTY RESPONSE RUNTIME =====")

service.client = FakeClient(
    FakeResponse("")
)

try:
    service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except RuntimeError as exc:
    print("Empty response: REJECTED")
    print(f"Boundary: {type(exc).__name__}")
else:
    raise RuntimeError(
        "Empty response unexpectedly passed."
    )


print()
print("===== 11. VERIFY PRODUCTION CONTRACT REMAINS STRICT =====")

if HeritageScannerResult.model_fields[
    "visual_evidence"
].annotation != list[str]:
    raise RuntimeError(
        "visual_evidence production type changed unexpectedly."
    )

print("Production visual_evidence type: list[str]")
print("Strict production contract: PASS")


print()
print("===== 12. PRODUCTION SAFETY =====")

print("Controlled fake Gemini client only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 40 COMPLETE")
print("=" * 80)
print("Valid service pipeline: PASS")
print("Invalid JSON rejection: PASS")
print("JSON array rejection: PASS")
print("Invalid confidence rejection: PASS")
print("Invalid visual evidence rejection: PASS")
print("Empty response rejection: PASS")
print("Strict production contract: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
