from pathlib import Path
import traceback

from app.services.ai.scanner.service import HeritageScannerService

IMAGE = Path(
    "scripts/ai_heritage_scanner_controlled_test.png"
)

print("=" * 80)
print("TASK 129 — EXACT SCANNER VALUEERROR DIAGNOSTIC")
print("=" * 80)

image_bytes = IMAGE.read_bytes()

print()
print("Image bytes:", len(image_bytes))
print("Image: PASS")

service = HeritageScannerService()

try:
    print()
    print("REAL GEMINI REQUEST: START")

    result = service.scan(
        image_bytes=image_bytes,
        content_type="image/png",
    )

    print()
    print("Scanner result: PASS")
    print(result.model_dump_json(indent=2))

except Exception as exc:
    print()
    print("=" * 80)
    print("EXACT FAILURE")
    print("=" * 80)
    print("Exception type:", type(exc).__name__)
    print("Exception message:", str(exc))
    print()
    print("FULL TRACEBACK:")
    traceback.print_exc()
    print()
    print("=" * 80)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 80)
    raise

finally:
    client = getattr(service, "client", None)
    close_method = getattr(client, "close", None)

    if callable(close_method):
        try:
            close_method()
        except Exception:
            pass

print()
print("NO DATABASE MUTATION")
print("NO QDRANT CHANGES")
print("NO EMBEDDINGS CREATED")
