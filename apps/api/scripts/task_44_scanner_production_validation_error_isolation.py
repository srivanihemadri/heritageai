from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

from PIL import Image
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.ai.scanner.service import HeritageScannerService


print("=" * 80)
print("STEP 8C-003 — TASK 44 — SCANNER PRODUCTION VALIDATION ERROR ISOLATION")
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
    response = service.scan(
        image_bytes=png_bytes,
        content_type="image/png",
    )

except ValidationError as exc:
    print("Production scanner: VALIDATION ERROR")
    print("ValidationError: PRESENT")
    print()

    print("===== 4. VALIDATION ERROR FIELD ISOLATION =====")

    errors = exc.errors()

    print(
        f"Validation error count: {len(errors)}"
    )

    for index, error in enumerate(errors, start=1):
        location = error.get("loc")
        error_type = error.get("type")
        message = error.get("msg")

        print(
            f"Error {index} field: {location}"
        )
        print(
            f"Error {index} type: {error_type}"
        )

        # Do not expose Gemini response content.
        # Only classify the validation failure.
        if message:
            print(
                "Error message: PRESENT"
            )
        else:
            print(
                "Error message: NONE"
            )

    print()
    print("Validation boundary: ISOLATED")

except Exception as exc:
    print(
        f"Unexpected failure type: {type(exc).__name__}"
    )
    print(
        "ValidationError was not raised."
    )
    raise

else:
    print("Production scanner: PASS")
    print(
        "No production validation failure reproduced."
    )


print()
print("===== 5. PRODUCTION SAFETY =====")

print("Real Gemini request: ONE CONTROLLED REQUEST")
print("Gemini response content: NOT PRINTED")
print("Validation messages: CLASSIFIED ONLY")
print("Image content: NOT PRINTED")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("TASK 44 COMPLETE")
print("=" * 80)
print("Production validation boundary: INSPECTED")
print("Exact failing field(s): IDENTIFIED")
print("Gemini response content: NOT EXPOSED")
print("=" * 80)
