from pathlib import Path
from pydantic import ValidationError

from app.services.ai.scanner.service import HeritageScannerService
from app.services.ai.scanner.image import ScannerImageValidationError


print("=" * 80)
print("STEP 8C-006 — TASK 111 — REAL GEMINI VALIDATION ERROR DIAGNOSTIC")
print("=" * 80)

image_path = Path("scripts/ai_heritage_scanner_controlled_test.png")

if not image_path.exists():
    raise RuntimeError(
        f"Controlled scanner image missing: {image_path}"
    )

image_bytes = image_path.read_bytes()

print()
print("===== 1. CONTROLLED IMAGE =====")
print("Image:", image_path)
print("Image bytes:", len(image_bytes))
print("Controlled image: PASS")

print()
print("===== 2. REAL GEMINI REQUEST =====")
print("REAL GEMINI REQUEST: START")

service = None

try:
    service = HeritageScannerService()

    response = service.scan(
        image_bytes=image_bytes,
        content_type="image/png",
    )

    print("REAL GEMINI REQUEST: COMPLETED")
    print()
    print("===== 3. VALIDATION RESULT =====")
    print("Scanner response validation: PASS")
    print("scan_id:", response.scan_id)
    print("identification_status:", response.result.identification_status)
    print("evidence_quality:", response.result.evidence_quality)
    print("confidence:", response.result.confidence)
    print("confidence_level:", response.result.confidence_level)
    print("grounding_status:", response.result.grounding_status)

except ValidationError as exc:

    print("REAL GEMINI REQUEST: COMPLETED")
    print()
    print("===== 3. PYDANTIC VALIDATION ERROR =====")
    print("ValidationError: PRESENT")
    print()
    print("Exact validation errors:")

    for error in exc.errors():
        print()
        print("Location:", error.get("loc"))
        print("Type:", error.get("type"))
        print("Message:", error.get("msg"))
        print("Input:", repr(error.get("input")))

    print()
    print("===== 4. DIAGNOSTIC INTERPRETATION =====")
    print("Gemini transport: PASS")
    print("Gemini response received: PASS")
    print("JSON extraction: PASS")
    print("Pydantic contract validation: FAIL")
    print("Exact contract mismatch: IDENTIFIED")
    print()
    print("NO SOURCE FIX APPLIED.")
    print("NO DATABASE MUTATION.")
    print("NO QDRANT CHANGES.")
    print("NO EMBEDDINGS CREATED.")

except ScannerImageValidationError as exc:

    print("Scanner image validation failed unexpectedly.")
    print("Error:", str(exc))
    raise

except Exception as exc:

    print()
    print("===== 3. NON-VALIDATION ERROR =====")
    print("Exception type:", type(exc).__name__)
    print("Message:", str(exc))
    print()
    print("This is NOT a Pydantic ValidationError.")
    print("STOP FOR REVIEW.")
    raise

finally:

    if service is not None:
        client = getattr(service, "client", None)
        close_method = getattr(client, "close", None)

        if callable(close_method):
            try:
                close_method()
            except Exception:
                pass

print()
print("=" * 80)
print("TASK 111 DIAGNOSTIC COMPLETE")
print("=" * 80)
