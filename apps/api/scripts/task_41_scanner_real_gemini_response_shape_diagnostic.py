from __future__ import annotations

import json
from io import BytesIO
import sys
from pathlib import Path

from PIL import Image
from google import genai
from google.genai import types

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings


print("=" * 80)
print("STEP 8C-003 — TASK 41 — REAL GEMINI RESPONSE SHAPE DIAGNOSTIC")
print("=" * 80)

if not settings.GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

print()
print("===== 1. BUILD CONTROLLED IMAGE =====")

image = Image.new("RGB", (32, 32), (120, 80, 40))
buffer = BytesIO()
image.save(buffer, format="PNG")
image_bytes = buffer.getvalue()

print(f"PNG bytes: {len(image_bytes)}")
print("Controlled image: PASS")


print()
print("===== 2. INITIALIZE GEMINI CLIENT =====")

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

print("Gemini client: PASS")


print()
print("===== 3. BUILD CONTROLLED JSON REQUEST =====")

prompt = """
Return ONLY one JSON object.

Use exactly these fields:

identified_name: string or null
category: string or null
location: string or null
country: string or null
confidence: number between 0 and 1
confidence_level: LOW, MEDIUM, or HIGH
description: string or null
architectural_style: string or null
historical_period: string or null
historical_significance: string or null
visual_evidence: array of strings
alternative_matches: array of strings
grounding_status: GROUNDED, PARTIALLY_GROUNDED, or UNVERIFIED
identification_status: IDENTIFIED, POSSIBLE_MATCH, INSUFFICIENT_EVIDENCE, NOT_HERITAGE, or AMBIGUOUS
evidence_quality: STRONG, MODERATE, WEAK, or NONE

Return JSON only.
"""

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part.from_text(text=prompt),
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/png",
            ),
        ],
    )
]

config = types.GenerateContentConfig(
    temperature=0.1,
    response_mime_type="application/json",
)

print("Multimodal request: PASS")


print()
print("===== 4. EXECUTE ONE REAL GEMINI REQUEST =====")

response = client.models.generate_content(
    model=settings.GEMINI_GENERATION_MODEL,
    contents=contents,
    config=config,
)

print("Gemini request: COMPLETED")
print(f"Response type: {type(response).__name__}")


print()
print("===== 5. READ RESPONSE TEXT =====")

response_text = response.text

if not response_text:
    raise RuntimeError(
        "Gemini returned empty response.text."
    )

print("response.text: PRESENT")
print(f"Response length: {len(response_text)}")
print("Response content: NOT PRINTED")


print()
print("===== 6. PARSE RESPONSE JSON =====")

try:
    payload = json.loads(response_text)
except json.JSONDecodeError as exc:
    print("JSON parsing: FAILED")
    print(f"Boundary: {type(exc).__name__}")
    raise

print("JSON parsing: PASS")
print(f"Decoded type: {type(payload).__name__}")

if not isinstance(payload, dict):
    raise RuntimeError(
        f"Expected JSON object, got {type(payload).__name__}."
    )

print("JSON object boundary: PASS")


print()
print("===== 7. INSPECT RESPONSE FIELD PRESENCE =====")

expected_fields = [
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

for field in expected_fields:
    if field in payload:
        print(f"{field}: PRESENT")
    else:
        print(f"{field}: MISSING")

print("Field presence inspection: COMPLETE")


print()
print("===== 8. INSPECT RESPONSE FIELD TYPES =====")

for field in expected_fields:
    if field not in payload:
        continue

    value = payload[field]

    if value is None:
        value_type = "NoneType"
    else:
        value_type = type(value).__name__

    print(f"{field}: {value_type}")


print("Field type inspection: COMPLETE")


print()
print("===== 9. FOCUS ON PREVIOUSLY OBSERVED FAILURE FIELDS =====")

if "confidence_level" in payload:
    print(
        "confidence_level type:",
        type(payload["confidence_level"]).__name__,
    )
    print(
        "confidence_level value present: YES"
        if payload["confidence_level"] is not None
        else "confidence_level value present: NO"
    )
else:
    print("confidence_level: MISSING")

if "visual_evidence" in payload:
    visual_value = payload["visual_evidence"]

    print(
        "visual_evidence type:",
        type(visual_value).__name__,
    )

    if isinstance(visual_value, list):
        print(
            f"visual_evidence item count: {len(visual_value)}"
        )
    else:
        print(
            "visual_evidence item count: NOT-A-LIST"
        )
else:
    print("visual_evidence: MISSING")


print()
print("===== 10. VERIFY JSON STRUCTURE ONLY =====")

for field in [
    "confidence_level",
    "visual_evidence",
    "identification_status",
    "evidence_quality",
    "grounding_status",
]:
    if field not in payload:
        print(f"{field}: STRUCTURE UNKNOWN")
        continue

    value = payload[field]

    if field == "visual_evidence":
        valid_shape = isinstance(value, list)
    else:
        valid_shape = (
            value is None
            or isinstance(value, str)
        )

    print(
        f"{field}: "
        + ("EXPECTED SHAPE" if valid_shape else "UNEXPECTED SHAPE")
    )


print()
print("===== 11. PRODUCTION SAFETY =====")

print("Real Gemini request: ONE CONTROLLED REQUEST")
print("Response content printed: NO")
print("Image content printed: NO")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 41 COMPLETE")
print("=" * 80)
print("Real response obtained: PASS")
print("JSON parsing: PASS")
print("Response structure inspected: PASS")
print("Field types inspected: PASS")
print("Failure fields inspected: PASS")
print("Response content not exposed: PASS")
print("=" * 80)
