"""Real multimodal Gemini service for HeritageAI image scanning."""

from __future__ import annotations

import json
import re
import time
from uuid import uuid4

from google import genai
from google.genai import errors, types

from app.core.config import settings
from app.services.ai.scanner.contract import (
    HeritageScannerResponse,
    HeritageScannerResult,
)
from app.services.ai.scanner.image import (
    validate_image_bytes,
)
from app.services.ai.scanner.prompts import (
    SCANNER_INTELLIGENCE_RULES,
    build_scanner_prompt,
)


class ScannerQuotaExceededError(RuntimeError):
    """Raised when the Gemini scanner project quota is exhausted."""


class HeritageScannerService:
    """Performs multimodal heritage image analysis with Gemini."""

    MAX_TRANSIENT_RETRIES = 3
    TRANSIENT_RETRY_DELAY_SECONDS = 3

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.GEMINI_GENERATION_MODEL

    def create_scan_id(self) -> str:
        """Create a unique scanner request identifier."""

        return str(uuid4())

    @staticmethod
    def _extract_json(text: str) -> dict:
        """Extract a JSON object from a Gemini response."""

        cleaned = text.strip()

        cleaned = re.sub(
            r"^```json\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"^```\s*",
            "",
            cleaned,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
        )

        try:
            payload = json.loads(cleaned)

        except json.JSONDecodeError as exc:
            start = cleaned.find("{")
            end = cleaned.rfind("}")

            if start < 0 or end <= start:
                raise ValueError(
                    "Gemini returned invalid scanner JSON."
                ) from exc

            try:
                payload = json.loads(
                    cleaned[start : end + 1]
                )
            except json.JSONDecodeError as nested_exc:
                raise ValueError(
                    "Gemini returned invalid scanner JSON."
                ) from nested_exc

        if not isinstance(payload, dict):
            raise ValueError(
                "Gemini scanner response must be a JSON object."
            )

        return payload

    def scan(
        self,
        image_bytes: bytes,
        content_type: str,
    ) -> HeritageScannerResponse:
        """Validate an image and perform one real Gemini scan."""

        validate_image_bytes(
            image_bytes,
            content_type,
        )

        scan_id = self.create_scan_id()

        prompt = build_scanner_prompt()

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=content_type,
        )

        print("REAL GEMINI SCANNER REQUEST: START")

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=prompt,
                    ),
                    image_part,
                ],
            )
        ]

        config = types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
        )

        response = None
        last_error = None

        for attempt in range(
            1,
            self.MAX_TRANSIENT_RETRIES + 1,
        ):
            try:
                print(
                    f"GEMINI SCANNER ATTEMPT: "
                    f"{attempt}/{self.MAX_TRANSIENT_RETRIES}"
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config,
                )

                print(
                    "REAL GEMINI SCANNER REQUEST: COMPLETED"
                )

                break

            except errors.ClientError as exc:

                status_code = getattr(
                    exc,
                    "status_code",
                    None,
                )

                error_text = str(exc)

                if (
                    status_code == 429
                    or "RESOURCE_EXHAUSTED" in error_text
                ):

                    print(
                        "GEMINI SCANNER QUOTA EXHAUSTED"
                    )

                    raise ScannerQuotaExceededError(
                        "Gemini scanner quota has been exhausted. "
                        "Please try again later."
                    ) from exc

                raise

            except errors.ServerError as exc:
                last_error = exc

                print(
                    f"GEMINI TRANSIENT SERVER ERROR: "
                    f"{getattr(exc, 'status_code', 'UNKNOWN')}"
                )

                if attempt >= self.MAX_TRANSIENT_RETRIES:
                    raise RuntimeError(
                        "Gemini scanner temporarily unavailable "
                        "after controlled retries."
                    ) from exc

                print(
                    "Waiting before controlled retry..."
                )

                time.sleep(
                    self.TRANSIENT_RETRY_DELAY_SECONDS
                )

        if response is None:
            raise RuntimeError(
                "Gemini scanner returned no response."
            ) from last_error

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError(
                "Gemini returned an empty scanner response."
            )

        payload = self._extract_json(text)

        result = HeritageScannerResult.model_validate(
            payload
        )

        # Gemini performs visual analysis only.
        # Historical grounding is controlled by trusted
        # HeritageAI application knowledge and retrieval.
        result.grounding_status = "UNVERIFIED"

        return HeritageScannerResponse(
            success=True,
            scan_id=scan_id,
            result=result,
        )

