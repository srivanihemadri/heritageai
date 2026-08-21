from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Scan(Base):
    """Persisted result of an anonymous heritage-image scan."""

    __tablename__ = "scans"

    __table_args__ = ()

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    identification_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    evidence_quality: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )

    identified_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence_level: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    architectural_style: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    historical_period: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    historical_significance: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    visual_evidence: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    alternative_matches: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    grounding_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )




