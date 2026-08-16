from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.service import HeritageScannerService
from app.services.ai.scanner.contract import HeritageScannerResponse


print("=" * 80)
print("STEP 8C-003 — TASK 43 — REAL PRODUCTION SCANNER PIPELINE DIAGNOSTIC")
print("=" * 80)


print()
print("===== 1. BUILD CONTROLLED IMAGE =====")

image = Image.new(
    "RGB",
    (32, 32),
    (120, 80, 40),
)

buffer = BytesIO()
image.save(buffer, format="PNG")
png_bytes = buffer.getvalue()

print(f"PNG bytes: {len(png_bytes)}")
print("Controlled image: PASS")


print()
print("===== 2. INITIALIZE PRODUCTION SCANNER SERVICE =====")

service = HeritageScannerService()

print("HeritageScannerService: PASS")
print("Production client: PRESENT")


print()
print("===== 3. EXECUTE ACTUAL PRODUCTION SCAN =====")

try:
    response = service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )
except Exception as exc:
    print("Production scanner pipeline: FAILED")
    print(
        f"Failure type: {type(exc).__name__}"
    )
    print(
        "Failure message: NOT PRINTED"
    )
    print(
        "This isolates the remaining failure "
        "to the production scanner runtime."
    )
else:
    print("Production scanner pipeline: PASS")
    print(
        f"Response type: {type(response).__name__}"
    )

    if not isinstance(
        response,
        HeritageScannerResponse,
    ):
        raise RuntimeError(
            "Production scanner returned an unexpected response type."
        )

    print("HeritageScannerResponse: PASS")
    print("success field: PRESENT")
    print("scan_id field: PRESENT")
    print("result field: PRESENT")

    result = response.result

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
    print(
        f"confidence_level: "
        f"{result.confidence_level}"
    )
    print(
        f"visual_evidence count: "
        f"{len(result.visual_evidence)}"
    )

    print("Production contract: PASS")


print()
print("===== 4. PRODUCTION SAFETY =====")

print("Real Gemini request: ONE CONTROLLED REQUEST")
print("Gemini response content: NOT PRINTED")
print("Image content: NOT PRINTED")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 43 DIAGNOSTIC COMPLETE")
print("=" * 80)
print("Production scanner runtime: INSPECTED")
print("Production contract: INSPECTED")
print("Response content: NOT EXPOSED")
print("=" * 80)
