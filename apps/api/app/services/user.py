from sqlalchemy.orm import Session

from app.core.exceptions import ResourceConflictException, ResourceNotFoundException
from app.crud.user import get_user_by_email, get_user_by_id
from app.models.user import User, UserRole
from app.schemas.user import UserAdminUpdate, UserUpdate


def update_user(
    db: Session,
    user: User,
    data: UserUpdate,
) -> User:
    updates = data.model_dump(exclude_unset=True)

    if "email" in updates:
        existing_user = get_user_by_email(db, updates["email"])
        if existing_user and existing_user.id != user.id:
            raise ResourceConflictException(
                message="Email already registered",
                error_code="EMAIL_ALREADY_REGISTERED",
            )

    for field, value in updates.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def admin_update_user(
    db: Session,
    user: User,
    data: UserAdminUpdate,
) -> User:
    updates = data.model_dump(exclude_unset=True)

    if "email" in updates:
        existing_user = get_user_by_email(db, updates["email"])
        if existing_user and existing_user.id != user.id:
            raise ResourceConflictException(
                message="Email already registered",
                error_code="EMAIL_ALREADY_REGISTERED",
            )

    if "role" in updates:
        try:
            updates["role"] = UserRole(updates["role"])
        except ValueError:
            raise ResourceConflictException(
                message="Invalid user role",
                error_code="INVALID_USER_ROLE",
            )

    for field, value in updates.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User,
) -> None:
    db.delete(user)
    db.commit()


def get_user_or_404(
    db: Session,
    user_id: str,
) -> User:
    user = get_user_by_id(db, user_id)

    if not user:
        raise ResourceNotFoundException(
            message="User not found",
            error_code="USER_NOT_FOUND",
        )

    return user
