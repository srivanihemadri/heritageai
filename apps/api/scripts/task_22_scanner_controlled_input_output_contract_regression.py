from __future__ import annotations

import json
import sys
import uuid
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image

from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)
from app.services.ai.scanner.image import validate_image_bytes
from app.services.ai.scanner.service import HeritageScannerService


print("=" * 80)
print("STEP 8C-003 — TASK 22 — SCANNER CONTROLLED INPUT/OUTPUT CONTRACT REGRESSION")
print("=" * 80)

print()
print("===== 1. VERIFY PRODUCTION IMPORTS =====")

print("HeritageScannerResult: PASS")
print("HeritageScannerResponse: PASS")
print("HeritageScannerService: PASS")
print("validate_image_bytes: PASS")

print()
print("===== 2. BUILD CONTROLLED IMAGE INPUT =====")

image_buffer = BytesIO()

image = Image.new(
    "RGB",
    (8, 8),
    (120, 120, 120),
)

image.save(
    image_buffer,
    format="PNG",
)

image_bytes = image_buffer.getvalue()

if not image_bytes:
    raise RuntimeError(
        "Controlled image bytes are empty."
    )

print("Controlled PNG bytes:", len(image_bytes))
print("Controlled image construction: PASS")

print()
print("===== 3. VALIDATE IMAGE INPUT =====")

decoded_image = validate_image_bytes(
    image_bytes,
    "image/png",
)

if decoded_image.format != "PNG":
    raise RuntimeError(
        f"Expected PNG image, got {decoded_image.format}"
    )

print("Image validation: PASS")
print("Image format: PNG")
print("Input boundary: PASS")

print()
print("===== 4. BUILD CONTROLLED GEMINI JSON =====")

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
    "grounding_status": "UNVERIFIED",
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
print("===== 5. VERIFY JSON EXTRACTION =====")

service = object.__new__(
    HeritageScannerService
)

extracted = service._extract_json(
    controlled_json
)

if not isinstance(extracted, dict):
    raise RuntimeError(
        "Extracted scanner payload is not a dictionary."
    )

if extracted["identified_name"] != "Konark Sun Temple":
    raise RuntimeError(
        "identified_name was not preserved."
    )

print("_extract_json(): PASS")
print("JSON object preservation: PASS")

print()
print("===== 6. BUILD PRODUCTION RESULT =====")

result = HeritageScannerResult.model_validate(
    extracted
)

if result.identified_name != "Konark Sun Temple":
    raise RuntimeError(
        "Production result lost identified_name."
    )

if result.identification_status != "IDENTIFIED":
    raise RuntimeError(
        "Production result lost identification_status."
    )

if result.evidence_quality != "STRONG":
    raise RuntimeError(
        "Production result lost evidence_quality."
    )

if result.grounding_status != "UNVERIFIED":
    raise RuntimeError(
        "Production result changed grounding_status unexpectedly."
    )

print("HeritageScannerResult: PASS")
print("Identification field preservation: PASS")
print("Evidence field preservation: PASS")
print("Grounding field preservation: PASS")

print()
print("===== 7. BUILD PUBLIC RESPONSE =====")

scan_id = f"task22-{uuid.uuid4().hex}"

response = HeritageScannerResponse(
    success=True,
    scan_id=scan_id,
    result=result,
)

if response.scan_id != scan_id:
    raise RuntimeError(
        "scan_id was not preserved."
    )

if response.result.identification_status != "IDENTIFIED":
    raise RuntimeError(
        "Public response lost identification_status."
    )

if response.result.evidence_quality != "STRONG":
    raise RuntimeError(
        "Public response lost evidence_quality."
    )

print("HeritageScannerResponse: PASS")
print("scan_id preservation: PASS")
print("Public result preservation: PASS")

print()
print("===== 8. VERIFY PUBLIC SERIALIZATION =====")

serialized = response.model_dump()

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

for field in required_fields:
    if field not in serialized["result"]:
        raise RuntimeError(
            f"Public response missing field: {field}"
        )

print("All scanner result fields: PRESENT")
print("Public serialization: PASS")

print()
print("===== 9. VERIFY INTELLIGENCE FIELD VALUES =====")

if serialized["result"]["identification_status"] != "IDENTIFIED":
    raise RuntimeError(
        "Serialized identification_status mismatch."
    )

if serialized["result"]["evidence_quality"] != "STRONG":
    raise RuntimeError(
        "Serialized evidence_quality mismatch."
    )

if serialized["result"]["grounding_status"] != "UNVERIFIED":
    raise RuntimeError(
        "Serialized grounding_status mismatch."
    )

print("identification_status: PASS")
print("evidence_quality: PASS")
print("grounding_status: PASS")

print()
print("===== 10. VERIFY RESPONSE JSON ROUND TRIP =====")

serialized_json = json.dumps(
    serialized
)

round_trip = json.loads(
    serialized_json
)

if round_trip["scan_id"] != scan_id:
    raise RuntimeError(
        "scan_id failed JSON round trip."
    )

if (
    round_trip["result"]["identified_name"]
    != "Konark Sun Temple"
):
    raise RuntimeError(
        "identified_name failed JSON round trip."
    )

if (
    round_trip["result"]["identification_status"]
    != "IDENTIFIED"
):
    raise RuntimeError(
        "identification_status failed JSON round trip."
    )

if (
    round_trip["result"]["evidence_quality"]
    != "STRONG"
):
    raise RuntimeError(
        "evidence_quality failed JSON round trip."
    )

print("JSON round trip: PASS")

print()
print("===== 11. VERIFY SERVICE GEMINI BOUNDARY =====")

service_source = Path(
    "app/services/ai/scanner/service.py"
).read_text(
    encoding="utf-8"
)

if "generate_content" not in service_source:
    raise RuntimeError(
        "Gemini generation boundary is missing."
    )

if "types.Part.from_bytes" not in service_source:
    raise RuntimeError(
        "Image byte boundary is missing."
    )

if "mime_type=content_type" not in service_source:
    raise RuntimeError(
        "Content type boundary is missing."
    )

print("Gemini generation boundary: PRESENT")
print("Image bytes boundary: PRESENT")
print("Content type boundary: PRESENT")
print("Multimodal boundary: PASS")

print()
print("===== 12. VERIFY EXISTING AI ROUTES =====")

from app.main import app

paths = app.openapi().get("paths", {})

if "/api/v1/ai/answer" not in paths:
    raise RuntimeError(
        "/api/v1/ai/answer route is missing."
    )

if "/api/v1/ai/scan" not in paths:
    raise RuntimeError(
        "/api/v1/ai/scan route is missing."
    )

print("/api/v1/ai/answer: PRESERVED")
print("/api/v1/ai/scan: PRESERVED")

print()
print("===== 13. PRODUCTION SAFETY =====")

print("Controlled input/output path only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")

print()
print("=" * 80)
print("STEP 8C-003 — TASK 22 COMPLETE")
print("=" * 80)
print("Controlled image input: PASS")
print("Image validation: PASS")
print("Controlled Gemini JSON: PASS")
print("JSON extraction: PASS")
print("Production result contract: PASS")
print("Public response contract: PASS")
print("Intelligence field preservation: PASS")
print("Serialization: PASS")
print("JSON round trip: PASS")
print("Multimodal boundary: PASS")
print("Existing AI routes: PRESERVED")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
