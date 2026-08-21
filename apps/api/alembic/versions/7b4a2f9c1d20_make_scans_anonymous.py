"""make scans anonymous

Revision ID: 7b4a2f9c1d20
Revises: 1d8ad76fbfed
Create Date: 2026-08-21

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7b4a2f9c1d20"
down_revision: Union[str, Sequence[str], None] = "1d8ad76fbfed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove user ownership from scanner results."""

    bind = op.get_bind()
    inspector = sa.inspect(bind)

    foreign_keys = inspector.get_foreign_keys("scans")

    for foreign_key in foreign_keys:
        if foreign_key.get("constrained_columns") == ["user_id"]:
            constraint_name = foreign_key.get("name")
            if constraint_name:
                op.drop_constraint(
                    constraint_name,
                    "scans",
                    type_="foreignkey",
                )

    indexes = inspector.get_indexes("scans")

    for index in indexes:
        if index["name"] in {
            "ix_scans_user_id",
            "ix_scans_user_id_created_at",
        }:
            op.drop_index(index["name"], table_name="scans")

    columns = {
        column["name"]
        for column in inspector.get_columns("scans")
    }

    if "user_id" in columns:
        op.drop_column("scans", "user_id")


def downgrade() -> None:
    """Restore user ownership to scanner results."""

    op.add_column(
        "scans",
        sa.Column(
            "user_id",
            sa.String(length=36),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_scans_user_id",
        "scans",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        "ix_scans_user_id_created_at",
        "scans",
        ["user_id", "created_at"],
        unique=False,
    )
