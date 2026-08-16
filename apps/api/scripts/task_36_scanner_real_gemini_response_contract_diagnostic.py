from __future__ import annotations

import json
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image
from google import genai
from google.genai import types

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings
from app.services.ai.scanner.service import HeritageScannerService
from app.services.ai.scanner.contract import HeritageScannerResult


print("=" * 80)
print("STEP 8C-003 — TASK 36 — REAL GEMINI RESPONSE → PRODUCTION CONTRACT DIAGNOSTIC")
print("=" * 80)


print()
print("===== 1. VERIFY CONFIGURATION =====")

if not settings.GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

print("GEMINI_API_KEY: CONFIGURED")
print(f"Gemini model: {settings.GEMINI_GENERATION_MODEL}")
print("Configuration: PASS")


print()
print("===== 2. BUILD CONTROLLED IMAGE =====")

image = Image.new(
    "RGB",
    (32, 32),
    (120, 80, 40),
)

buffer = BytesIO()
image.save(buffer, format="PNG")
image_bytes = buffer.getvalue()

print(f"PNG bytes: {len(image_bytes)}")
print("Image construction: PASS")


print()
print("===== 3. INITIALIZE REAL GEMINI CLIENT =====")

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

print("Gemini client: PASS")


print()
print("===== 4. BUILD CONTROLLED SCANNER PROMPT =====")

prompt = """
Analyze this image as a heritage-image scanner.

Return ONLY one JSON object.

Required fields:
identified_name
category
location
country
confidence
confidence_level
description
architectural_style
historical_period
historical_significance
visual_evidence
alternative_matches
grounding_status
identification_status
evidence_quality

Use these exact semantic states where applicable:

identification_status:
IDENTIFIED, POSSIBLE_MATCH, INSUFFICIENT_EVIDENCE, NOT_HERITAGE, AMBIGUOUS

evidence_quality:
STRONG, MODERATE, WEAK, NONE

grounding_status:
GROUNDED, PARTIALLY_GROUNDED, UNVERIFIED

Do not return markdown fences.
Do not return explanatory text outside the JSON object.
"""

image_part = types.Part.from_bytes(
    data=image_bytes,
    mime_type="image/png",
)

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part.from_text(text=prompt),
            image_part,
        ],
    )
]

config = types.GenerateContentConfig(
    temperature=0.1,
    response_mime_type="application/json",
)

print("Prompt: PASS")
print("Multimodal contents: PASS")
print("JSON response configuration: PASS")


print()
print("===== 5. EXECUTE ONE REAL GEMINI REQUEST =====")

try:
    response = client.models.generate_content(
        model=settings.GEMINI_GENERATION_MODEL,
        contents=contents,
        config=config,
    )
except Exception as exc:
    raise RuntimeError(
        "Gemini request failed before response processing: "
        f"{type(exc).__name__}"
    ) from exc

print("Gemini request: COMPLETED")
print(f"Response type: {type(response).__name__}")


print()
print("===== 6. VERIFY RESPONSE METADATA =====")

candidates = getattr(response, "candidates", None)

if candidates is None:
    raise RuntimeError("Gemini response has no candidates.")

print(f"Candidate count: {len(candidates)}")

if len(candidates) == 0:
    raise RuntimeError("Gemini returned zero candidates.")

candidate = candidates[0]

print(
    "Finish reason: "
    f"{getattr(candidate, 'finish_reason', None)}"
)

content = getattr(candidate, "content", None)

if content is None:
    raise RuntimeError(
        "Gemini candidate content is missing."
    )

parts = getattr(content, "parts", None)

if parts is None:
    raise RuntimeError(
        "Gemini candidate parts are missing."
    )

print(f"Candidate parts: {len(parts)}")
print("Response metadata: PASS")


print()
print("===== 7. ACCESS REAL RESPONSE TEXT =====")

try:
    response_text = response.text
except Exception as exc:
    print("response.text: FAILED")
    print(
        f"Exception type: {type(exc).__name__}"
    )
    raise RuntimeError(
        "Failure boundary: response.text"
    ) from exc

if not response_text:
    raise RuntimeError(
        "Failure boundary: empty response.text"
    )

print("response.text: PASS")
print(f"Response text length: {len(response_text)}")
print("Response content: NOT PRINTED")


print()
print("===== 8. RUN PRODUCTION JSON EXTRACTION =====")

try:
    extracted = HeritageScannerService._extract_json(
        response_text
    )
except Exception as exc:
    print("Production _extract_json(): FAILED")
    print(
        f"Exception type: {type(exc).__name__}"
    )
    print(
        f"Exception message: {str(exc)}"
    )
    print(
        "FAILURE BOUNDARY: JSON EXTRACTION"
    )
    raise RuntimeError(
        "Task 36 isolated failure at _extract_json()."
    ) from exc

print("Production _extract_json(): PASS")
print(f"Extracted object type: {type(extracted).__name__}")
print(f"Extracted field count: {len(extracted)}")
print(
    "Extracted field names: "
    + ", ".join(sorted(extracted.keys()))
)
print("Gemini JSON → Python object: PASS")


print()
print("===== 9. RUN PRODUCTION PYDANTIC VALIDATION =====")

try:
    result = HeritageScannerResult.model_validate(
        extracted
    )
except Exception as exc:
    print("HeritageScannerResult validation: FAILED")
    print(
        f"Exception type: {type(exc).__name__}"
    )
    print(
        f"Exception message: {str(exc)}"
    )
    print(
        "FAILURE BOUNDARY: PYDANTIC VALIDATION"
    )
    raise RuntimeError(
        "Task 36 isolated failure at HeritageScannerResult.model_validate()."
    ) from exc

print("HeritageScannerResult validation: PASS")
print(
    f"identification_status: "
    f"{result.identification_status}"
)
print(
    f"evidence_quality: "
    f"{result.evidence_quality}"
)
print(
    f"grounding_status: "
    f"{result.grounding_status}"
)
print("Production result contract: PASS")


print()
print("===== 10. BUILD PUBLIC RESPONSE =====")

try:
    from app.services.ai.scanner.contract import (
        HeritageScannerResponse,
    )

    public_response = HeritageScannerResponse(
        success=True,
        scan_id="TASK36-CONTROLLED",
        result=result,
    )
except Exception as exc:
    print("Public response construction: FAILED")
    print(
        f"Exception type: {type(exc).__name__}"
    )
    print(
        f"Exception message: {str(exc)}"
    )
    print(
        "FAILURE BOUNDARY: PUBLIC RESPONSE"
    )
    raise

print("HeritageScannerResponse: PASS")
print("Public response contract: PASS")


print()
print("===== 11. DETERMINE EXACT PIPELINE RESULT =====")

print("REAL GEMINI REQUEST: PASS")
print("response.text: PASS")
print("_extract_json(): PASS")
print("HeritageScannerResult.model_validate(): PASS")
print("HeritageScannerResponse: PASS")
print("Exact production contract pipeline: PASS")


print()
print("===== 12. PRODUCTION SAFETY =====")

print("Real Gemini request: ONE CONTROLLED REQUEST")
print("Gemini response content printed: NONE")
print("Image content printed: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 36 COMPLETE")
print("=" * 80)
print("Real Gemini response acquisition: PASS")
print("Response metadata: PASS")
print("response.text: PASS")
print("JSON extraction: PASS")
print("Production result validation: PASS")
print("Public response construction: PASS")
print("=" * 80)
