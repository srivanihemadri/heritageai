from pathlib import Path
import json
import re

from app.services.ai.scanner.service import HeritageScannerService


print("=" * 80)
print("STEP 8C-006 — TASK 112 — SCANNER JSON BOUNDARY DIAGNOSTIC")
print("=" * 80)

image_path = Path(
    "scripts/ai_heritage_scanner_controlled_test.png"
)

if not image_path.exists():
    raise RuntimeError(
        f"Controlled scanner image missing: {image_path}"
    )

image_bytes = image_path.read_bytes()

print()
print("===== 1. CONTROLLED IMAGE =====")
print("Image bytes:", len(image_bytes))
print("Controlled image: PASS")

original_extract_json = HeritageScannerService._extract_json


def diagnostic_extract_json(text: str) -> dict:
    print()
    print("===== 2. GEMINI RESPONSE BOUNDARY =====")
    print("Gemini response text received: PASS")
    print("Response length:", len(text))

    cleaned = text.strip()

    cleaned = re.sub(
        r"^```json\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    print("Cleaned JSON candidate length:", len(cleaned))

    try:
        payload = json.loads(cleaned)

        print("JSON parse: PASS")
        return payload

    except json.JSONDecodeError as exc:

        print()
        print("===== 3. JSON PARSE FAILURE =====")
        print("JSON parse: FAIL")
        print("Error:", exc.msg)
        print("Line:", exc.lineno)
        print("Column:", exc.colno)
        print("Character:", exc.pos)

        start = max(0, exc.pos - 200)
        end = min(len(cleaned), exc.pos + 200)

        print()
        print("===== 4. BOUNDED RESPONSE WINDOW =====")
        print(
            "Showing only 200 characters before/after "
            "the failure position."
        )
        print()

        print(cleaned[start:end])

        print()
        print("===== 5. CHARACTER-LEVEL INSPECTION =====")

        local_start = max(0, exc.pos - 30)
        local_end = min(len(cleaned), exc.pos + 30)

        for index in range(local_start, local_end):
            print(
                f"{index}: {repr(cleaned[index])}"
            )

        print()
        print("===== 6. JSON STRUCTURE CHECK =====")

        opening = cleaned[:exc.pos].count("{")
        closing = cleaned[:exc.pos].count("}")

        print("Opening braces before failure:", opening)
        print("Closing braces before failure:", closing)

        print()
        print("===== 7. SAFETY GATE =====")
        print("Gemini transport: PASS")
        print("Gemini response received: PASS")
        print("JSON extraction: FAIL")
        print("Pydantic validation: NOT REACHED")
        print("Database persistence: NOT REACHED")
        print("Qdrant mutation: NONE")
        print("Embeddings created: NONE")

        print()
        print("TASK 112 DIAGNOSTIC: FAILURE LOCATED")
        print("NO SOURCE CHANGE APPLIED.")
        print("NO DATABASE MUTATION.")

        raise ValueError(
            "TASK 112 diagnostic intentionally stopped "
            "after locating malformed Gemini JSON."
        ) from exc


HeritageScannerService._extract_json = staticmethod(
    diagnostic_extract_json
)

service = None

try:

    print()
    print("===== 8. REAL SCANNER REQUEST =====")
    print("REAL GEMINI REQUEST: START")

    service = HeritageScannerService()

    try:
        service.scan(
            image_bytes=image_bytes,
            content_type="image/png",
        )

        print("Scanner returned successfully.")
        print("JSON parse: PASS")

    except ValueError as exc:

        if "TASK 112 diagnostic intentionally stopped" in str(exc):
            pass
        else:
            raise

finally:

    HeritageScannerService._extract_json = (
        original_extract_json
    )

    if service is not None:

        client = getattr(
            service,
            "client",
            None,
        )

        close_method = getattr(
            client,
            "close",
            None,
        )

        if callable(close_method):

            try:
                close_method()
            except Exception:
                pass

print()
print("=" * 80)
print("TASK 112 DIAGNOSTIC COMPLETE")
print("=" * 80)
print("Temporary instrumentation removed.")
print("No application source changed.")
print("No database mutation.")
print("No Qdrant changes.")
print("No embeddings created.")
print("=" * 80)
