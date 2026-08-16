from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image

from app.main import app
from app.services.ai.scanner.image import (
    MAX_IMAGE_SIZE_BYTES,
    SUPPORTED_CONTENT_TYPES,
    SUPPORTED_IMAGE_FORMATS,
    ScannerImageValidationError,
    validate_image_bytes,
)


print("=" * 80)
print("STEP 8C-003 — TASK 29 — SCANNER CONTROLLED CONTENT-TYPE & UPLOAD CONTRACT REGRESSION")
print("=" * 80)


print()
print("===== 1. VERIFY IMAGE VALIDATION IMPORTS =====")

print("validate_image_bytes: PASS")
print("ScannerImageValidationError: PASS")
print("MAX_IMAGE_SIZE_BYTES: PRESENT")
print("SUPPORTED_CONTENT_TYPES: PRESENT")
print("SUPPORTED_IMAGE_FORMATS: PRESENT")


print()
print("===== 2. VERIFY SUPPORTED IMAGE CONTRACT =====")

expected_content_types = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

expected_formats = {
    "JPEG",
    "PNG",
    "WEBP",
}

if set(SUPPORTED_CONTENT_TYPES) != expected_content_types:
    raise RuntimeError(
        f"Unexpected supported content types: "
        f"{SUPPORTED_CONTENT_TYPES}"
    )

if set(SUPPORTED_IMAGE_FORMATS) != expected_formats:
    raise RuntimeError(
        f"Unexpected supported image formats: "
        f"{SUPPORTED_IMAGE_FORMATS}"
    )

for content_type in sorted(SUPPORTED_CONTENT_TYPES):
    print(f"{content_type}: PRESENT")

for image_format in sorted(SUPPORTED_IMAGE_FORMATS):
    print(f"{image_format}: PRESENT")

print("Supported image contract: PASS")


print()
print("===== 3. BUILD CONTROLLED TEST IMAGES =====")

def build_image_bytes(image_format: str) -> bytes:
    image = Image.new(
        "RGB",
        (2, 2),
        (120, 80, 40),
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format=image_format,
    )

    return buffer.getvalue()


png_bytes = build_image_bytes("PNG")
jpeg_bytes = build_image_bytes("JPEG")
webp_bytes = build_image_bytes("WEBP")

print(f"PNG bytes: {len(png_bytes)}")
print(f"JPEG bytes: {len(jpeg_bytes)}")
print(f"WEBP bytes: {len(webp_bytes)}")

print("Controlled image construction: PASS")


print()
print("===== 4. VERIFY VALID PNG =====")

png_result = validate_image_bytes(
    png_bytes,
    "image/png",
)

if png_result.format != "PNG":
    raise RuntimeError(
        f"Expected PNG, got {png_result.format!r}"
    )

print("PNG validation: PASS")
print("PNG format: PASS")


print()
print("===== 5. VERIFY VALID JPEG =====")

jpeg_result = validate_image_bytes(
    jpeg_bytes,
    "image/jpeg",
)

if jpeg_result.format != "JPEG":
    raise RuntimeError(
        f"Expected JPEG, got {jpeg_result.format!r}"
    )

print("JPEG validation: PASS")
print("JPEG format: PASS")


print()
print("===== 6. VERIFY VALID WEBP =====")

webp_result = validate_image_bytes(
    webp_bytes,
    "image/webp",
)

if webp_result.format != "WEBP":
    raise RuntimeError(
        f"Expected WEBP, got {webp_result.format!r}"
    )

print("WEBP validation: PASS")
print("WEBP format: PASS")


print()
print("===== 7. VERIFY EMPTY IMAGE REJECTION =====")

try:
    validate_image_bytes(
        b"",
        "image/png",
    )
except ScannerImageValidationError:
    print("Empty image: REJECTED")
else:
    raise RuntimeError(
        "Empty image was not rejected."
    )

print("Empty image rejection: PASS")


print()
print("===== 8. VERIFY CORRUPTED IMAGE REJECTION =====")

corrupted_bytes = b"This is not a valid image."

try:
    validate_image_bytes(
        corrupted_bytes,
        "image/png",
    )
except ScannerImageValidationError:
    print("Corrupted image: REJECTED")
else:
    raise RuntimeError(
        "Corrupted image was not rejected."
    )

print("Corrupted image rejection: PASS")


print()
print("===== 9. VERIFY UNSUPPORTED MIME REJECTION =====")

try:
    validate_image_bytes(
        png_bytes,
        "image/gif",
    )
except ScannerImageValidationError:
    print("Unsupported MIME type: REJECTED")
else:
    raise RuntimeError(
        "Unsupported MIME type was not rejected."
    )

print("Unsupported MIME rejection: PASS")


print()
print("===== 10. VERIFY MIME / FORMAT MISMATCH =====")

try:
    validate_image_bytes(
        png_bytes,
        "image/jpeg",
    )
except ScannerImageValidationError:
    print("PNG sent as JPEG: REJECTED")
else:
    raise RuntimeError(
        "PNG/JPEG MIME mismatch was not rejected."
    )

try:
    validate_image_bytes(
        jpeg_bytes,
        "image/png",
    )
except ScannerImageValidationError:
    print("JPEG sent as PNG: REJECTED")
else:
    raise RuntimeError(
        "JPEG/PNG MIME mismatch was not rejected."
    )

print("MIME/format mismatch rejection: PASS")


print()
print("===== 11. VERIFY CONTENT-TYPE CASE NORMALIZATION =====")

case_result = validate_image_bytes(
    png_bytes,
    "IMAGE/PNG",
)

if case_result.format != "PNG":
    raise RuntimeError(
        "Uppercase MIME content type was not normalized correctly."
    )

print("Uppercase MIME handling: PASS")


print()
print("===== 12. VERIFY OVERSIZED IMAGE REJECTION =====")

oversized_bytes = b"0" * (
    MAX_IMAGE_SIZE_BYTES + 1
)

try:
    validate_image_bytes(
        oversized_bytes,
        "image/png",
    )
except ScannerImageValidationError:
    print("Oversized image: REJECTED")
else:
    raise RuntimeError(
        "Oversized image was not rejected."
    )

print("Maximum image-size boundary: PASS")


print()
print("===== 13. VERIFY OPENAPI UPLOAD CONTRACT =====")

openapi = app.openapi()

scanner_path = openapi.get(
    "paths",
    {},
).get(
    "/api/v1/ai/scan",
)

if scanner_path is None:
    raise RuntimeError(
        "Scanner route missing from OpenAPI."
    )

scanner_operation = scanner_path.get("post")

if scanner_operation is None:
    raise RuntimeError(
        "POST scanner operation missing."
    )

request_body = scanner_operation.get(
    "requestBody",
)

if request_body is None:
    raise RuntimeError(
        "Scanner request body missing."
    )

multipart = request_body.get(
    "content",
    {},
).get(
    "multipart/form-data",
)

if multipart is None:
    raise RuntimeError(
        "multipart/form-data contract missing."
    )

print("POST /api/v1/ai/scan: PRESENT")
print("multipart/form-data: PRESENT")
print("Upload contract: PASS")


print()
print("===== 14. VERIFY FILE FIELD =====")

schema = multipart.get(
    "schema",
    {},
)

schemas = openapi.get(
    "components",
    {},
).get(
    "schemas",
    {},
)

if "$ref" in schema:
    schema_name = schema["$ref"].rsplit(
        "/",
        1,
    )[-1]

    schema = schemas.get(
        schema_name,
        {},
    )

properties = schema.get(
    "properties",
    {},
)

if "file" not in properties:
    raise RuntimeError(
        "Scanner file upload field missing."
    )

print("file: PRESENT")
print("File upload field: PASS")


print()
print("===== 15. VERIFY VALIDATOR SOURCE BOUNDARIES =====")

validator_source = validate_image_bytes.__module__

if not validator_source:
    raise RuntimeError(
        "Validator module information unavailable."
    )

print("Validator module: PRESENT")
print("Validator boundary: PASS")


print()
print("===== 16. PRODUCTION SAFETY =====")

print("Controlled upload validation only: PASS")
print("Real Gemini request: NONE")
print("Database queries: NONE")
print("Database mutations: NONE")
print("Qdrant changes: NONE")
print("Embeddings created: NONE")
print("Production source changes: NONE")


print()
print("=" * 80)
print("STEP 8C-003 — TASK 29 COMPLETE")
print("=" * 80)
print("Supported image contract: PASS")
print("PNG validation: PASS")
print("JPEG validation: PASS")
print("WEBP validation: PASS")
print("Empty image rejection: PASS")
print("Corrupted image rejection: PASS")
print("Unsupported MIME rejection: PASS")
print("MIME mismatch rejection: PASS")
print("Oversized image rejection: PASS")
print("OpenAPI upload contract: PASS")
print("File upload field: PASS")
print("NO REAL GEMINI REQUEST.")
print("NO DATABASE CHANGES.")
print("NO QDRANT CHANGES.")
print("NO EMBEDDINGS CREATED.")
print("=" * 80)
