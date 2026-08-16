import os
import sys
from getpass import getpass

from app.crud.user import get_user_by_email
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.security import hash_password

ADMIN_NAME = "HeritageAI Admin"
ADMIN_EMAIL = os.getenv(
    "HERITAGEAI_ADMIN_EMAIL",
    "admin@heritageai.dev",
)


def resolve_admin_password() -> str:
    password = os.getenv("HERITAGEAI_ADMIN_PASSWORD")

    if password:
        return password

    if not sys.stdin.isatty():
        raise RuntimeError(
            "HERITAGEAI_ADMIN_PASSWORD must be set when running non-interactively."
        )

    password = getpass("HeritageAI administrator password: ")

    if not password:
        raise RuntimeError("Administrator password cannot be empty.")

    return password


def main() -> None:
    db = SessionLocal()

    try:
        existing_user = get_user_by_email(
            db,
            ADMIN_EMAIL,
        )

        if existing_user:
            if existing_user.role != UserRole.ADMIN:
                existing_user.role = UserRole.ADMIN

            if not existing_user.is_active:
                existing_user.is_active = True

            db.commit()

            print("Existing admin account updated.")
            print(f"Email: {ADMIN_EMAIL}")
            return

        admin_password = resolve_admin_password()

        admin = User(
            full_name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password_hash=hash_password(admin_password),
            role=UserRole.ADMIN,
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Admin account created successfully.")
        print(f"ID: {admin.id}")
        print(f"Email: {ADMIN_EMAIL}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
