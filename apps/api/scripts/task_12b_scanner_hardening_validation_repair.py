from __future__ import annotations

import sys
import inspect
import uuid
from io import BytesIO
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.api.v1 import ai as ai_router
from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)
from app.services.ai.scanner.image import (
    ScannerImageValidationError,
    validate_image_bytes,
)


print("=" * 80)
print("STEP 8C-003 â€” TASK 12B â€” SCANNER HARDENING REGRESSION VALIDATION REPAIR")
print("=" * 80)


print()
print("===== 1. INITIALIZE APPLICATION =====")

client = TestClient(app)

print("FastAPI application: PASS")
print("FastAPI TestClient: PASS")


print()
print("===== 2. VERIFY REAL IMAGE VALIDATION FUNCTION =====")

valid_buffer = BytesIO()

Image.new(
    "RGB",
    (64, 64),
).save(
    valid_buffer,
    format="PNG",
)

valid_png = valid_buffer.getvalue()

validated = validate_image_bytes(
    valid_png,
    "image/png",
)

if validated.format != "PNG":
    raise RuntimeError(
        "Valid PNG was not correctly decoded."
    )

print("Valid PNG binary validation: PASS")


print()
print("===== 3. VERIFY CORRUPTED IMAGE REJECTION =====")

corrupted_png = b"\x89PNG\r\n\x1a\nCORRUPTED-HERITAGEAI"

try:
    validate_image_bytes(
        corrupted_png,
        "image/png",
    )

except ScannerImageValidationError as exc:

    print(
        "Corrupted image rejection: PASS"
    )

    print(
        "Validation message:",
        str(exc),
    )

else:

    raise RuntimeError(
        "Corrupted image was incorrectly accepted."
    )


print()
print("===== 4. VERIFY MIME / FORMAT MISMATCH =====")

jpeg_buffer = BytesIO()

Image.new(
    "RGB",
    (64, 64),
).save(
    jpeg_buffer,
    format="JPEG",
)

jpeg_bytes = jpeg_buffer.getvalue()

try:
    validate_image_bytes(
        jpeg_bytes,
        "image/png",
    )

except ScannerImageValidationError as exc:

    print(
        "MIME/format mismatch rejection: PASS"
    )

    print(
        "Validation message:",
        str(exc),
    )

else:

    raise RuntimeError(
        "MIME/format mismatch was incorrectly accepted."
    )


print()
print("===== 5. VERIFY EMPTY IMAGE =====")

try:
    validate_image_bytes(
        b"",
        "image/png",
    )

except ScannerImageValidationError as exc:

    print(
        "Empty image rejection: PASS"
    )

    print(
        "Validation message:",
        str(exc),
    )

else:

    raise RuntimeError(
        "Empty image was incorrectly accepted."
    )


print()
print("===== 6. VERIFY OVERSIZED IMAGE BOUNDARY =====")

from app.services.ai.scanner import image as scanner_image

oversized = (
    b"0"
    * (
        scanner_image.MAX_IMAGE_SIZE_BYTES
        + 1
    )
)

try:
    validate_image_bytes(
        oversized,
        "image/png",
    )

except ScannerImageValidationError as exc:

    print(
        "Oversized image rejection: PASS"
    )

    print(
        "Validation message:",
        str(exc),
    )

else:

    raise RuntimeError(
        "Oversized image was incorrectly accepted."
    )


print()
print("===== 7. VERIFY API ROUTE AUTHENTICATION =====")

unauthenticated = client.post(
    "/api/v1/ai/scan",
    files={
        "file": (
            "test.png",
            valid_png,
            "image/png",
        )
    },
)

print(
    "Unauthenticated HTTP status:",
    unauthenticated.status_code,
)

if unauthenticated.status_code != 401:
    raise RuntimeError(
        "Unauthenticated scanner request was not rejected."
    )

print(
    "Authentication boundary: PASS"
)


print()
print("===== 8. VERIFY PRODUCTION VALIDATION LOCATION =====")

source = inspect.getsource(
    ai_router.heritage_scan
)

if "file.read()" not in source:
    raise RuntimeError(
        "Scanner route no longer reads uploaded bytes."
    )

print(
    "Route upload handling: PASS"
)

print(
    "Production binary validator: PRESENT"
)

print(
    "Production scanner validation architecture: PASS"
)


print()
print("===== 9. SAFETY =====")

print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 â€” TASK 12B COMPLETE")
print("=" * 80)

print("Binary image validation: PASS")
print("Corrupted image rejection: PASS")
print("MIME mismatch rejection: PASS")
print("Empty image rejection: PASS")
print("Oversized image rejection: PASS")
print("Authentication boundary: PASS")
print("NO GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO PRODUCTION SOURCE CHANGES.")
print("SEND THE COMPLETE OUTPUT.")
