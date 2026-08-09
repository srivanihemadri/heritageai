import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Date, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SourceType(str, Enum):
    GOVERNMENT = "GOVERNMENT"
    UNESCO = "UNESCO"
    ACADEMIC = "ACADEMIC"
    BOOK = "BOOK"
    MUSEUM = "MUSEUM"
    ARCHIVE = "ARCHIVE"
    WEBSITE = "WEBSITE"
    OTHER = "OTHER"


class HeritageSiteSource(Base):
    __tablename__ = "heritage_site_sources"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    site_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("heritage_sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    source_type: Mapped[SourceType] = mapped_column(
        SqlEnum(SourceType),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    author: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    organization: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    publisher: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    publication_date: Mapped[datetime | None] = mapped_column(
        Date,
        nullable=True,
    )

    url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    citation_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    language: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="en",
        index=True,
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
