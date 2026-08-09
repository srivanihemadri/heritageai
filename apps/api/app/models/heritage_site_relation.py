import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RelationType(str, Enum):
    RELATED_TO = "RELATED_TO"
    PART_OF = "PART_OF"
    ASSOCIATED_WITH = "ASSOCIATED_WITH"
    LOCATED_NEAR = "LOCATED_NEAR"
    HISTORICALLY_CONNECTED = "HISTORICALLY_CONNECTED"


class HeritageSiteRelation(Base):
    __tablename__ = "heritage_site_relations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    source_site_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("heritage_sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    target_site_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("heritage_sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    relation_type: Mapped[RelationType] = mapped_column(
        SqlEnum(RelationType),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
