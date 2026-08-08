from fastapi import APIRouter, Depends, status
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


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


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