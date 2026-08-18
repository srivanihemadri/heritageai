"""add google authentication identity

Revision ID: 6283772c4771
Revises: 1604f8627652
Create Date: 2026-08-18 14:23:39.212746

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6283772c4771"
down_revision: Union[str, Sequence[str], None] = "1604f8627652"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add Google identity support without altering existing passwords."""

    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        nullable=True,
    )

    op.add_column(
        "users",
        sa.Column(
            "google_sub",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_users_google_sub",
        "users",
        ["google_sub"],
        unique=True,
    )


def downgrade() -> None:
    """Remove Google identity support."""

    op.drop_index(
        "ix_users_google_sub",
        table_name="users",
    )

    op.drop_column(
        "users",
        "google_sub",
    )

    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        nullable=False,
    )
