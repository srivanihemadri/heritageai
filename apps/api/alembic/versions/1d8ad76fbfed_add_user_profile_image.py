"""add user profile image

Revision ID: 1d8ad76fbfed
Revises: 6283772c4771
Create Date: 2026-08-18

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1d8ad76fbfed"
down_revision: Union[str, Sequence[str], None] = "6283772c4771"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add optional Google profile image URL."""

    op.add_column(
        "users",
        sa.Column(
            "profile_image_url",
            sa.String(length=1000),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Remove profile image URL."""

    op.drop_column(
        "users",
        "profile_image_url",
    )
