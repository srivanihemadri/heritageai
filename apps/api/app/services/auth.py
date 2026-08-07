from sqlalchemy.orm import Session

from app.crud.user import authenticate_user
from app.schemas.token import Token
from app.security import create_access_token


def login(
    db: Session,
    email: str,
    password: str,
) -> Token | None:

    user = authenticate_user(
        db,
        email,
        password,
    )

    if not user:
        return None

    access_token = create_access_token(
        subject=str(user.id),
    )

    return Token(
        access_token=access_token,
    )