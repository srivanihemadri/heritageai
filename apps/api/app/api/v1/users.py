from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException
from app.db.session import get_db
from app.dependencies import get_current_admin, get_current_user
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.user import (
    UserAdminUpdate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from app.services.user import (
    admin_update_user,
    delete_user,
    get_user_or_404,
    update_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=APIResponse[UserResponse],
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return APIResponse(
        success=True,
        data=current_user,
        message="User profile retrieved successfully",
    )


@router.patch(
    "/me",
    response_model=APIResponse[UserResponse],
)
def update_my_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updated_user = update_user(
        db,
        current_user,
        data,
    )

    return APIResponse(
        success=True,
        data=updated_user,
        message="User profile updated successfully",
    )


@router.get(
    "",
    response_model=APIResponse[UserListResponse],
)
def list_users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    users = db.query(User).order_by(User.created_at.desc()).all()

    return APIResponse(
        success=True,
        data=UserListResponse(
            users=users,
            total=len(users),
        ),
        message="Users retrieved successfully",
    )


@router.get(
    "/{user_id}",
    response_model=APIResponse[UserResponse],
)
def get_user(
    user_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    user = get_user_or_404(
        db,
        user_id,
    )

    return APIResponse(
        success=True,
        data=user,
        message="User retrieved successfully",
    )


@router.patch(
    "/{user_id}",
    response_model=APIResponse[UserResponse],
)
def update_user_by_admin(
    user_id: str,
    data: UserAdminUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    user = get_user_or_404(
        db,
        user_id,
    )

    updated_user = admin_update_user(
        db,
        user,
        data,
    )

    return APIResponse(
        success=True,
        data=updated_user,
        message="User updated successfully",
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_by_admin(
    user_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    user = get_user_or_404(
        db,
        user_id,
    )

    if user.id == current_admin.id:
        raise ForbiddenException(
            message="Administrators cannot delete themselves",
            error_code="ADMIN_SELF_DELETE_FORBIDDEN",
        )

    delete_user(
        db,
        user,
    )

    return None
