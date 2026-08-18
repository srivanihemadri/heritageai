from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ResourceConflictException,
    UnauthorizedException,
)
from app.crud.user import (
    authenticate_user,
    create_user,
    get_user_by_email,
)
from app.db.session import get_db
from app.dependencies import get_current_user
from app.schemas.common import APIResponse
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.security import create_access_token
from app.services.google_auth import GoogleAuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


class GoogleAuthRequest(BaseModel):
    id_token: str


@router.post(
    "/register",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(
        db,
        user.email,
    )

    if existing_user:
        raise ResourceConflictException(
            message="Email already registered",
            error_code="EMAIL_ALREADY_REGISTERED",
        )

    created_user = create_user(
        db,
        user,
    )

    return APIResponse(
        success=True,
        data=created_user,
        message="User registered successfully",
    )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not user:
        raise UnauthorizedException(
            message="Invalid email or password",
            error_code="INVALID_CREDENTIALS",
        )

    # Synchronize the latest Google profile image for every Google login.
    if google_profile_image and user.profile_image_url != google_profile_image:
        user.profile_image_url = google_profile_image
        db.commit()
        db.refresh(user)

    if not user.is_active:
        raise UnauthorizedException(
            message="User account is inactive",
            error_code="INACTIVE_ACCOUNT",
        )

    access_token = create_access_token(
        subject=str(user.id),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post(
    "/google",
    response_model=Token,
)
def google_login(
    payload: GoogleAuthRequest,
    db: Session = Depends(get_db),
):
    """Authenticate with a verified Google ID token."""

    google_claims = GoogleAuthService().verify_id_token(
        payload.id_token,
    )

    google_sub = str(google_claims["sub"])
    google_email = str(google_claims["email"]).strip().lower()
    google_name = str(
        google_claims.get("name")
        or google_claims.get("given_name")
        or "HeritageAI User"
    ).strip()

    google_profile_image = google_claims.get("picture")

    if google_profile_image is not None:
        google_profile_image = str(google_profile_image).strip() or None

    user = (
        db.query(__import__("app.models.user", fromlist=["User"]).User)
        .filter(
            __import__("app.models.user", fromlist=["User"]).User.google_sub
            == google_sub
        )
        .first()
    )

    if user is None:
        user = get_user_by_email(
            db,
            google_email,
        )

        if user is not None:
            if user.google_sub not in (None, google_sub):
                raise ResourceConflictException(
                    message="Google account is already linked to another identity.",
                    error_code="GOOGLE_IDENTITY_CONFLICT",
                )

            user.google_sub = google_sub

            if not user.full_name.strip():
                user.full_name = google_name

            if google_profile_image:
                user.profile_image_url = google_profile_image

            db.commit()
            db.refresh(user)

        else:
            User = __import__(
                "app.models.user",
                fromlist=["User"],
            ).User

            user = User(
                full_name=google_name[:100],
                email=google_email,
                password_hash=None,
                google_sub=google_sub,
                profile_image_url=google_profile_image,
            )

            db.add(user)
            db.commit()
            db.refresh(user)

    if not user.is_active:
        raise UnauthorizedException(
            message="User account is inactive",
            error_code="INACTIVE_ACCOUNT",
        )

    access_token = create_access_token(
        subject=str(user.id),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=APIResponse[UserResponse],
)
def get_current_user_profile(
    current_user=Depends(get_current_user),
):
    return APIResponse(
        success=True,
        data=current_user,
        message="User profile retrieved successfully",
    )