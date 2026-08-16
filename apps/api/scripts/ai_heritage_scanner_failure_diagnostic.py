from __future__ import annotations

import sys
import traceback
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

print("=" * 80)
print("STEP 8C-003 — TASK 5-DIAGNOSTIC — SCANNER FAILURE ROOT-CAUSE ANALYSIS")
print("=" * 80)

IMAGE_PATH = (
    Path(__file__).resolve().parent
    / "ai_heritage_scanner_controlled_test.png"
)

print()
print("===== 1. VERIFY CONTROLLED IMAGE =====")

if not IMAGE_PATH.exists():
    raise RuntimeError(f"Controlled image not found: {IMAGE_PATH}")

image_bytes = IMAGE_PATH.read_bytes()

print(f"Image: {IMAGE_PATH}")
print(f"Image bytes: {len(image_bytes)}")

if not image_bytes:
    raise RuntimeError("Controlled image is empty.")

print("Image: PASS")

print()
print("===== 2. IMPORT SCANNER SERVICE =====")

try:
    from app.services.ai.scanner.service import HeritageScannerService
    from app.services.ai.scanner.contract import (
        HeritageScannerResponse,
        HeritageScannerResult,
    )

    print("HeritageScannerService import: PASS")
    print("HeritageScannerResponse import: PASS")
    print("HeritageScannerResult import: PASS")

except Exception:
    print("Scanner service import: FAIL")
    traceback.print_exc()
    raise

print()
print("===== 3. INITIALIZE SCANNER SERVICE =====")

service = None

try:
    service = HeritageScannerService()

    print("Scanner service initialization: PASS")
    print(
        "Configured model:",
        getattr(service, "model", "<model attribute unavailable>"),
    )

except Exception:
    print("Scanner service initialization: FAIL")
    traceback.print_exc()
    raise

print()
print("===== 4. INSPECT SCAN METHOD =====")

scan_method = getattr(service, "scan", None)

if scan_method is None:
    raise RuntimeError("HeritageScannerService.scan() not found.")

print("scan method: PRESENT")

try:
    import inspect

    print("scan signature:", inspect.signature(scan_method))

except Exception:
    print("Could not inspect scan signature.")

print()
print("===== 5. EXECUTE DIRECT REAL GEMINI SCANNER CALL =====")

print("This executes the production scanner service directly.")
print("No database writes are expected.")

try:
    result = service.scan(
        image_bytes=image_bytes,
        content_type="image/png",
    )

    print()
    print("===== 6. DIRECT SCANNER RESULT =====")

    print("Result type:", type(result).__name__)

    if isinstance(result, HeritageScannerResponse):
        print("HeritageScannerResponse: PASS")
    else:
        print(
            "WARNING: Unexpected response type:",
            type(result),
        )

    print("Result:", result)

except Exception as exc:
    print()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("DIRECT SCANNER SERVICE FAILURE")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print()
    print("Exception type:", type(exc).__name__)
    print("Exception message:", str(exc))
    print()
    print("FULL TRACEBACK:")
    traceback.print_exc()
    print()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    raise

finally:
    try:
        if service is not None and hasattr(service, "close"):
            service.close()
            print()
            print("Scanner service cleanup: PASS")
    except Exception:
        print()
        print("Scanner service cleanup warning:")
        traceback.print_exc()

print()
print("===== 7. DIAGNOSTIC RESULT =====")
print("Direct scanner service: PASS")
print("Root cause not reproduced.")

print()
print("=" * 80)
print("STEP 8C-003 — TASK 5-DIAGNOSTIC COMPLETE")
print("=" * 80)
print("DO NOT MODIFY PRODUCTION CODE.")
print("SEND THE COMPLETE OUTPUT.")
