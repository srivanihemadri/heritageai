from typing import Generic, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class APIError(BaseModel):
    """Standard API error details."""

    code: str = Field(
        ...,
        description="Machine-readable error code.",
        examples=["RESOURCE_NOT_FOUND"],
    )

    message: str = Field(
        ...,
        description="Human-readable error message.",
        examples=["Resource not found"],
    )


class APIResponse(BaseModel, Generic[T]):
    """Standard successful API response."""

    success: bool = Field(
        default=True,
        description="Whether the request was successful.",
    )

    data: T | None = Field(
        default=None,
        description="Response payload.",
    )

    message: str | None = Field(
        default=None,
        description="Optional human-readable message.",
    )


class APIErrorResponse(BaseModel):
    """Standard API error response."""

    success: bool = Field(
        default=False,
        description="Whether the request was successful.",
    )

    error: APIError = Field(
        ...,
        description="Structured error information.",
    )