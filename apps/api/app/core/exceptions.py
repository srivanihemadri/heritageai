from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.common import APIErrorResponse


class HeritageAIException(Exception):
    """Base exception for all application-level errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(message)


class ResourceNotFoundException(HeritageAIException):
    """Raised when a requested resource does not exist."""

    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str = "RESOURCE_NOT_FOUND",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=error_code,
        )


class ResourceConflictException(HeritageAIException):
    """Raised when a resource conflicts with an existing resource."""

    def __init__(
        self,
        message: str = "Resource already exists",
        error_code: str = "RESOURCE_CONFLICT",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code=error_code,
        )


class UnauthorizedException(HeritageAIException):
    """Raised when authentication is required or invalid."""

    def __init__(
        self,
        message: str = "Authentication required",
        error_code: str = "UNAUTHORIZED",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=error_code,
        )


class ForbiddenException(HeritageAIException):
    """Raised when the authenticated user lacks permission."""

    def __init__(
        self,
        message: str = "Access forbidden",
        error_code: str = "FORBIDDEN",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=error_code,
        )


async def heritageai_exception_handler(
    request: Request,
    exc: HeritageAIException,
) -> JSONResponse:
    """Handle application-level exceptions."""

    response = APIErrorResponse(
        success=False,
        error={
            "code": exc.error_code,
            "message": exc.message,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle FastAPI/Pydantic request validation errors."""

    validation_details = []

    for error in exc.errors():
        validation_details.append(
            {
                "field": ".".join(
                    str(location)
                    for location in error.get("loc", [])
                    if location != "body"
                ),
                "message": error.get(
                    "msg",
                    "Invalid value.",
                ),
                "type": error.get(
                    "type",
                    "validation_error",
                ),
            }
        )

    response = APIErrorResponse(
        success=False,
        error={
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed.",
        },
    )

    response_content = response.model_dump()

    response_content["error"]["details"] = validation_details

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_content,
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle unexpected application errors."""

    response = APIErrorResponse(
        success=False,
        error={
            "code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred.",
        },
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(),
    )