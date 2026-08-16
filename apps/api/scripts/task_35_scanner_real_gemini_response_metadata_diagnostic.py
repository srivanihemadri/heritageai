from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from google import genai
from google.genai import types

from app.core.config import settings


print("=" * 80)
print("STEP 8C-003 — TASK 35 — REAL GEMINI RESPONSE METADATA DIAGNOSTIC")
print("=" * 80)


print()
print("===== 1. VERIFY GEMINI CONFIGURATION =====")

if not settings.GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )

model = settings.GEMINI_GENERATION_MODEL

print("GEMINI_API_KEY: CONFIGURED")
print(f"Gemini model configured: {model}")
print("Configuration boundary: PASS")


print()
print("===== 2. BUILD CONTROLLED TEST IMAGE =====")

image = Image.new(
    "RGB",
    (32, 32),
    (120, 80, 40),
)

buffer = BytesIO()
image.save(buffer, format="PNG")
image_bytes = buffer.getvalue()

print(f"PNG bytes: {len(image_bytes)}")
print("Controlled image: PASS")


print()
print("===== 3. INITIALIZE REAL GEMINI CLIENT =====")

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

print("Gemini client: PASS")


print()
print("===== 4. BUILD CONTROLLED MULTIMODAL REQUEST =====")

prompt = """
Return ONLY a JSON object matching this structure:

{
  "identified_name": "Test Heritage Site",
  "category": "Temple",
  "location": "Konark",
  "country": "India",
  "confidence": 0.95,
  "confidence_level": "HIGH",
  "description": "Controlled diagnostic response.",
  "architectural_style": "Kalinga architecture",
  "historical_period": "13th century",
  "historical_significance": "Controlled diagnostic significance.",
  "visual_evidence": [
    "Controlled visual observation"
  ],
  "alternative_matches": [],
  "grounding_status": "GROUNDED",
  "identification_status": "IDENTIFIED",
  "evidence_quality": "STRONG"
}
"""

image_part = types.Part.from_bytes(
    data=image_bytes,
    mime_type="image/png",
)

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=prompt
            ),
            image_part,
        ],
    )
]

config = types.GenerateContentConfig(
    temperature=0.1,
    response_mime_type="application/json",
)

print("Multimodal request: PASS")


print()
print("===== 5. EXECUTE ONE REAL GEMINI REQUEST =====")

try:
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )
except Exception as exc:
    print(
        "Gemini request failed."
    )
    print(
        f"Exception type: {type(exc).__name__}"
    )
    print(
        "Exception message available: YES"
    )
    raise RuntimeError(
        "Real Gemini request failed before a response "
        f"was returned: {type(exc).__name__}"
    ) from exc

print("Gemini request: COMPLETED")
print(
    f"Response Python type: {type(response).__name__}"
)


print()
print("===== 6. INSPECT RESPONSE OBJECT METADATA =====")

candidates = getattr(
    response,
    "candidates",
    None,
)

if candidates is None:
    print("candidates attribute: NONE")
    candidate_count = 0
else:
    try:
        candidate_count = len(candidates)
    except Exception:
        candidate_count = -1

    print(
        f"candidates count: {candidate_count}"
    )

print("Response metadata inspection: PASS")


print()
print("===== 7. INSPECT FIRST CANDIDATE METADATA =====")

if candidate_count > 0:

    candidate = candidates[0]

    finish_reason = getattr(
        candidate,
        "finish_reason",
        None,
    )

    print(
        f"finish_reason: {finish_reason}"
    )

    content = getattr(
        candidate,
        "content",
        None,
    )

    print(
        "candidate.content present: "
        + ("YES" if content is not None else "NO")
    )

    if content is not None:

        parts = getattr(
            content,
            "parts",
            None,
        )

        if parts is None:
            print("candidate.parts: NONE")
        else:
            try:
                print(
                    f"candidate.parts count: {len(parts)}"
                )
            except Exception:
                print(
                    "candidate.parts count: UNKNOWN"
                )

else:
    print(
        "No candidates returned."
    )

print("Candidate metadata inspection: PASS")


print()
print("===== 8. VERIFY RESPONSE TEXT ACCESS =====")

try:
    response_text = response.text
except Exception as exc:
    print("response.text access: FAILED")
    print(
        f"response.text exception type: "
        f"{type(exc).__name__}"
    )
    print(
        "response.text exception message: AVAILABLE"
    )

    print()
    print("===== 9. DIAGNOSTIC CONCLUSION =====")
    print(
        "Failure boundary: response.text access"
    )
    print(
        "JSON extraction reached: NO"
    )
    print(
        "Pydantic validation reached: NO"
    )

    raise RuntimeError(
        "Task 35 isolated failure at response.text access."
    ) from exc

print("response.text access: PASS")

if not response_text:
    print(
        "response.text empty: YES"
    )
else:
    print(
        "response.text empty: NO"
    )

print(
    "Response content itself: NOT PRINTED"
)


print()
print("===== 10. VERIFY RESPONSE TEXT TYPE =====")

print(
    f"response.text type: {type(response_text).__name__}"
)

print(
    f"response.text length: {len(response_text)}"
)

print(
    "Response text content: NOT PRINTED"
)


print()
print("===== 11. PRODUCTION SAFETY =====")

print(
    "Real Gemini request: ONE CONTROLLED REQUEST"
)
print(
    "Gemini response content printed: NO"
)
print(
    "Image content printed: NO"
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
print("TASK 35 DIAGNOSTIC COMPLETE")
print("=" * 80)
print("Gemini response metadata: INSPECTED")
print("Candidate metadata: INSPECTED")
print("Response text boundary: INSPECTED")
print("Response content: NOT EXPOSED")
print("=" * 80)
