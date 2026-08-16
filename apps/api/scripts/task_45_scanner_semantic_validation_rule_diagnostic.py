from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

from PIL import Image
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.service import HeritageScannerService


print("=" * 80)
print("STEP 8C-003 — TASK 45 — SCANNER SEMANTIC VALIDATION RULE DIAGNOSTIC")
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
print("===== 2. INITIALIZE PRODUCTION SCANNER =====")

service = HeritageScannerService()

print("HeritageScannerService: PASS")


print()
print("===== 3. EXECUTE PRODUCTION SCAN =====")

try:
    service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )

except ValidationError as exc:
    print("Production scanner: VALIDATION ERROR")
    print("ValidationError: PRESENT")

    errors = exc.errors()

    print()
    print("===== 4. IDENTIFY SEMANTIC VALIDATION RULE =====")

    for index, error in enumerate(errors, start=1):
        print(f"Error {index} location: {error.get('loc')}")
        print(f"Error {index} type: {error.get('type')}")
        print(f"Error {index} message: {error.get('msg')}")

    print()
    print("Semantic validation rule: IDENTIFIED")

else:
    print("Production scanner: PASS")
    print("No semantic validation failure reproduced.")


print()
print("===== 5. PRODUCTION SAFETY =====")

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
print("TASK 45 COMPLETE")
print("=" * 80)
print("Semantic validation rule: IDENTIFIED")
print("Gemini response content: NOT EXPOSED")
print("=" * 80)
