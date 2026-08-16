"""Gemini-backed AI image enhancement service."""

from __future__ import annotations

import base64
import io

from app.core.config import settings

from .contract import ImageEnhancementResult
from .image import validate_image


class ImageEnhancementService:
    """Improve visual quality and resolution of heritage images."""

    def __init__(self) -> None:

        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "Gemini SDK is not available."
            ) from exc

        api_key = getattr(
            settings,
            "GEMINI_API_KEY",
            None,
        )

        if not api_key:
            raise RuntimeError(
                "Gemini API key is not configured."
            )

        self.client = genai.Client(
            api_key=api_key,
        )

        self.model = getattr(
            settings,
            "GEMINI_IMAGE_MODEL",
            "gemini-3.1-flash-image",
        )

    def enhance(
        self,
        image_bytes: bytes,
        content_type: str,
        resolution: str = "2K",
    ) -> ImageEnhancementResult:

        width, height = validate_image(
            image_bytes=image_bytes,
            content_type=content_type,
        )

        resolution = resolution.upper()

        if resolution not in {"1K", "2K", "4K"}:
            raise ValueError(
                "Resolution must be 1K, 2K, or 4K."
            )

        from google import genai

        import base64

        prompt = (
            "Enhance the supplied heritage image while preserving "
            "the exact identity, architecture, composition, geometry, "
            "historical characteristics, colors, and important visual "
            "details of the original image. "
            "Improve clarity, fine detail, sharpness, lighting balance, "
            "and apparent image quality. "
            "Do not invent architectural structures, remove historical "
            "features, alter inscriptions, or change the identity of "
            "the heritage site. "
            f"Return the enhanced image at {resolution} resolution."
        )

        interaction = self.client.interactions.create(
            model=self.model,
            input=[
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image",
                    "data": base64.b64encode(
                        image_bytes
                    ).decode("utf-8"),
                    "mime_type": content_type,
                },
            ],
            response_format={
                "type": "image",
                "mime_type": "image/jpeg",
                "image_size": resolution,
            },
        )

        output_image = getattr(
            interaction,
            "output_image",
            None,
        )

        if output_image is None:
            raise ValueError(
                "Gemini returned no enhanced image."
            )

        encoded = getattr(
            output_image,
            "data",
            None,
        )

        if not encoded:
            raise ValueError(
                "Gemini returned empty enhanced image data."
            )

        enhanced_bytes = base64.b64decode(
            encoded
        )

        if not enhanced_bytes:
            raise ValueError(
                "Enhanced image is empty."
            )

        from PIL import Image

        try:
            with Image.open(
                io.BytesIO(enhanced_bytes)
            ) as enhanced:
                output_width, output_height = enhanced.size
        except Exception as exc:
            raise ValueError(
                "Gemini returned invalid image data."
            ) from exc

        return ImageEnhancementResult(
            mime_type=content_type,
            image_bytes=enhanced_bytes,
            width=output_width,
            height=output_height,
            resolution=resolution,
        )

    def close(self) -> None:

        client = getattr(
            self,
            "client",
            None,
        )

        if client is None:
            return

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
