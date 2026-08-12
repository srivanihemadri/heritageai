import sys

from app.crud.user import get_user_by_email
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.security import hash_password


ADMIN_NAME = "HeritageAI Admin"
ADMIN_EMAIL = "admin@heritageai.local"
ADMIN_PASSWORD = "[REDACTED_REMOVED]"


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

        admin = User(
            full_name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
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
