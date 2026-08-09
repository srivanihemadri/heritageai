from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.db.session import get_db
from app.models.user import User, UserRole


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    # No Authorization header / no token
    if not token:
        raise UnauthorizedException(
            message="Not authenticated",
            error_code="UNAUTHORIZED",
        )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if not user_id:
            raise UnauthorizedException(
                message="Invalid authentication token",
                error_code="INVALID_TOKEN",
            )

    except JWTError:
        raise UnauthorizedException(
            message="Invalid authentication token",
            error_code="INVALID_TOKEN",
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise UnauthorizedException(
            message="User not found",
            error_code="USER_NOT_FOUND",
        )

    if not user.is_active:
        raise UnauthorizedException(
            message="User account is inactive",
            error_code="INACTIVE_ACCOUNT",
        )

    return user


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:

    if current_user.role != UserRole.ADMIN:
        raise ForbiddenException(
            message="Administrator access required",
            error_code="ADMIN_ACCESS_REQUIRED",
        )

    return current_user
