"""Validation boundary for AI image enhancement."""

from __future__ import annotations

from io import BytesIO

from PIL import Image


MAX_IMAGE_BYTES = 10 * 1024 * 1024

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


def validate_image(
    image_bytes: bytes,
    content_type: str,
) -> tuple[int, int]:

    if not image_bytes:
        raise ValueError("Image is empty.")

    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise ValueError(
            "Image exceeds the 10 MB safety limit."
        )

    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(
            "Unsupported image format."
        )

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()

        with Image.open(BytesIO(image_bytes)) as image:
            width, height = image.size

    except Exception as exc:
        raise ValueError(
            "Invalid image data."
        ) from exc

    if width < 1 or height < 1:
        raise ValueError(
            "Invalid image dimensions."
        )

    return width, height
