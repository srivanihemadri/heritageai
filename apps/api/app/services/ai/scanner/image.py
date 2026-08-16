"""Image validation primitives for the AI Heritage Scanner."""

from __future__ import annotations

from io import BytesIO

from PIL import Image, UnidentifiedImageError


SUPPORTED_IMAGE_FORMATS = {
    "JPEG",
    "PNG",
    "WEBP",
}

SUPPORTED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024


class ScannerImageValidationError(ValueError):
    """Raised when an uploaded scanner image is invalid."""


def validate_image_bytes(
    image_bytes: bytes,
    content_type: str | None = None,
) -> Image.Image:
    """Validate and decode an uploaded image."""

    if not image_bytes:
        raise ScannerImageValidationError(
            "Image file is empty."
        )

    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        raise ScannerImageValidationError(
            "Image file exceeds the maximum allowed size."
        )

    if content_type and content_type.lower() not in SUPPORTED_CONTENT_TYPES:
        raise ScannerImageValidationError(
            "Unsupported image content type."
        )

    try:
        image = Image.open(BytesIO(image_bytes))
        image.verify()

        decoded = Image.open(BytesIO(image_bytes))

    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
    ) as exc:
        raise ScannerImageValidationError(
            "Uploaded file is not a valid image."
        ) from exc

    image_format = (decoded.format or "").upper()

    if image_format not in SUPPORTED_IMAGE_FORMATS:
        raise ScannerImageValidationError(
            "Unsupported image format."
        )

    if content_type:
        expected_type = {
            "JPEG": "image/jpeg",
            "PNG": "image/png",
            "WEBP": "image/webp",
        }[image_format]

        if content_type.lower() != expected_type:
            raise ScannerImageValidationError(
                "Image content type does not match the actual image format."
            )

    return decoded
