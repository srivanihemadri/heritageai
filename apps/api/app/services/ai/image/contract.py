"""Contracts for AI image enhancement."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ImageEnhancementResult(BaseModel):
    """Result returned after AI image enhancement."""

    success: bool = True

    mime_type: str = Field(
        min_length=1,
        max_length=100,
    )

    image_bytes: bytes = Field(
        min_length=1,
    )

    width: int = Field(
        ge=1,
    )

    height: int = Field(
        ge=1,
    )

    resolution: str = Field(
        min_length=1,
        max_length=20,
    )


class ImageEnhancementResponse(BaseModel):
    """Public response metadata for image enhancement."""

    success: bool = True
    mime_type: str
    width: int
    height: int
    resolution: str
