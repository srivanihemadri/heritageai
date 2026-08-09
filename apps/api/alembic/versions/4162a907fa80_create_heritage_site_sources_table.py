"""create heritage site sources table

Revision ID: 4162a907fa80
Revises: 3d9f59bbafd3
Create Date: 2026-08-09 15:56:05.940109

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4162a907fa80"
down_revision: Union[str, Sequence[str], None] = "3d9f59bbafd3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "heritage_site_sources",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("site_id", sa.String(length=36), nullable=False),
        sa.Column(
            "source_type",
            sa.Enum(
                "GOVERNMENT",
                "UNESCO",
                "ACADEMIC",
                "BOOK",
                "MUSEUM",
                "ARCHIVE",
                "WEBSITE",
                "OTHER",
                name="sourcetype",
            ),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=300), nullable=False),
        sa.Column("author", sa.String(length=300), nullable=True),
        sa.Column("organization", sa.String(length=300), nullable=True),
        sa.Column("publisher", sa.String(length=300), nullable=True),
        sa.Column("publication_date", sa.Date(), nullable=True),
        sa.Column("url", sa.String(length=1000), nullable=True),
        sa.Column("citation_text", sa.Text(), nullable=True),
        sa.Column("language", sa.String(length=20), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["site_id"],
            ["heritage_sites.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_heritage_site_sources_site_id"),
        "heritage_site_sources",
        ["site_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_heritage_site_sources_source_type"),
        "heritage_site_sources",
        ["source_type"],
        unique=False,
    )

    op.create_index(
        op.f("ix_heritage_site_sources_language"),
        "heritage_site_sources",
        ["language"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_heritage_site_sources_language"),
        table_name="heritage_site_sources",
    )

    op.drop_index(
        op.f("ix_heritage_site_sources_source_type"),
        table_name="heritage_site_sources",
    )

    op.drop_index(
        op.f("ix_heritage_site_sources_site_id"),
        table_name="heritage_site_sources",
    )

    op.drop_table("heritage_site_sources")
