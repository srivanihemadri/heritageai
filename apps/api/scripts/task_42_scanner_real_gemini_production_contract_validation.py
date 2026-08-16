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
from app.services.ai.scanner.contract import HeritageScannerResult


print("=" * 80)
print("STEP 8C-003 — TASK 42 — REAL GEMINI → PRODUCTION CONTRACT VALIDATION")
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
print("===== 3. BUILD PRODUCTION-ALIGNED REQUEST =====")

prompt = """
Return ONLY a JSON object.

The response MUST satisfy this production schema exactly.

Fields:
- identified_name: string or null
- identification_status: one of IDENTIFIED, POSSIBLE_MATCH, INSUFFICIENT_EVIDENCE, NOT_HERITAGE, AMBIGUOUS
- evidence_quality: one of STRONG, MODERATE, WEAK, NONE
- category: string or null
- location: string or null
- country: string or null
- confidence: number from 0.0 to 1.0
- confidence_level: one of LOW, MEDIUM, HIGH
- description: string or null
- architectural_style: string or null
- historical_period: string or null
- historical_significance: string or null
- visual_evidence: array of strings
- alternative_matches: array of strings
- grounding_status: one of GROUNDED, PARTIALLY_GROUNDED, UNVERIFIED

Semantic rules:
- IDENTIFIED requires identified_name and non-empty visual_evidence.
- POSSIBLE_MATCH requires non-empty visual_evidence and cannot use HIGH confidence.
- AMBIGUOUS requires at least two alternative_matches.
- NOT_HERITAGE must not contain identified_name.
- STRONG evidence requires non-empty visual_evidence.
- NONE evidence must contain no visual_evidence.
- HIGH confidence requires identified_name, confidence >= 0.90, and non-empty visual_evidence.
- MEDIUM confidence requires confidence >= 0.50 and < 0.90.
- LOW confidence requires confidence < 0.50.
- GROUNDED requires non-empty visual_evidence.

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

print("Production-aligned prompt: PASS")


print()
print("===== 4. EXECUTE ONE REAL GEMINI REQUEST =====")

response = client.models.generate_content(
    model=settings.GEMINI_GENERATION_MODEL,
    contents=contents,
    config=config,
)

print("Gemini request: COMPLETED")
print("Response content: NOT PRINTED")


print()
print("===== 5. EXTRACT JSON =====")

response_text = response.text

if not response_text:
    raise RuntimeError(
        "Gemini returned empty response.text."
    )

try:
    payload = json.loads(response_text)
except json.JSONDecodeError as exc:
    raise RuntimeError(
        f"Gemini response was not valid JSON: "
        f"{type(exc).__name__}"
    ) from exc

if not isinstance(payload, dict):
    raise RuntimeError(
        "Gemini response was not a JSON object."
    )

print("JSON extraction: PASS")
print("JSON object: PASS")


print()
print("===== 6. INSPECT SEMANTIC STATE SUMMARY =====")

for field in [
    "identification_status",
    "evidence_quality",
    "grounding_status",
    "confidence_level",
]:
    value = payload.get(field)
    print(
        f"{field}: PRESENT"
        if field in payload
        else f"{field}: MISSING"
    )
    if field in payload:
        print(
            f"{field} type: {type(value).__name__}"
        )

visual_evidence = payload.get(
    "visual_evidence"
)

if isinstance(visual_evidence, list):
    print(
        f"visual_evidence count: {len(visual_evidence)}"
    )
else:
    print(
        "visual_evidence count: INVALID-TYPE"
    )


print()
print("===== 7. VALIDATE AGAINST PRODUCTION PYDANTIC CONTRACT =====")

try:
    result = HeritageScannerResult.model_validate(
        payload
    )
except Exception as exc:
    print("Production contract validation: REJECTED")
    print(
        f"Validation boundary: {type(exc).__name__}"
    )
    print(
        "Real Gemini response is semantically incompatible "
        "with the production contract."
    )
else:
    print("Production contract validation: PASS")
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
    print(
        f"Confidence level: "
        f"{result.confidence_level}"
    )


print()
print("===== 8. PRODUCTION SAFETY =====")

print("Real Gemini request: ONE CONTROLLED REQUEST")
print("Gemini response content printed: NO")
print("Image content printed: NO")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 42 COMPLETE")
print("=" * 80)
print("Real response obtained: PASS")
print("JSON extraction: PASS")
print("Production contract boundary: INSPECTED")
print("Response content not exposed: PASS")
print("=" * 80)
