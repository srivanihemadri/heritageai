"""Google ID-token verification for HeritageAI."""

from __future__ import annotations

from google.auth.exceptions import GoogleAuthError
from google.oauth2 import id_token
from google.auth.transport import requests

from app.core.config import settings
from app.core.exceptions import UnauthorizedException


class GoogleAuthService:
    """Verify Google ID tokens and return trusted identity claims."""

    def __init__(self) -> None:
        self._request = requests.Request()

    def verify_id_token(
        self,
        token: str,
    ) -> dict[str, object]:
        """Verify a Google ID token."""

        normalized = token.strip()

        if not normalized:
            raise UnauthorizedException(
                message="Google ID token is required.",
                error_code="GOOGLE_TOKEN_REQUIRED",
            )

        audience = getattr(
            settings,
            "GOOGLE_OAUTH_CLIENT_IDS",
            None,
        )

        if not audience:
            raise RuntimeError(
                "GOOGLE_OAUTH_CLIENT_IDS is not configured."
            )

        if isinstance(audience, str):
            audiences = [
                value.strip()
                for value in audience.split(",")
                if value.strip()
            ]
        else:
            audiences = list(audience)

        if not audiences:
            raise RuntimeError(
                "GOOGLE_OAUTH_CLIENT_IDS is empty."
            )

        last_error: Exception | None = None

        for client_id in audiences:
            try:
                claims = id_token.verify_oauth2_token(
                    normalized,
                    self._request,
                    client_id,
                )

                if claims.get("iss") not in {
                    "accounts.google.com",
                    "https://accounts.google.com",
                }:
                    raise UnauthorizedException(
                        message="Invalid Google token issuer.",
                        error_code="INVALID_GOOGLE_TOKEN",
                    )

                subject = claims.get("sub")
                email = claims.get("email")

                if not subject or not email:
                    raise UnauthorizedException(
                        message="Google token is missing required identity claims.",
                        error_code="INVALID_GOOGLE_TOKEN",
                    )

                if claims.get("email_verified") is not True:
                    raise UnauthorizedException(
                        message="Google email address is not verified.",
                        error_code="GOOGLE_EMAIL_NOT_VERIFIED",
                    )

                return claims

            except UnauthorizedException:
                raise

            except (ValueError, GoogleAuthError) as exc:
                last_error = exc

        raise UnauthorizedException(
            message="Invalid Google ID token.",
            error_code="INVALID_GOOGLE_TOKEN",
        ) from last_error
