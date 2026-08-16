import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AIKnowledgeDocumentType(str, Enum):
    SITE_PROFILE = "SITE_PROFILE"
    HISTORICAL_EVENT = "HISTORICAL_EVENT"
    RELATIONSHIP = "RELATIONSHIP"
    MEDIA_CONTEXT = "MEDIA_CONTEXT"


class AIKnowledgeDocument(Base):
    __tablename__ = "ai_knowledge_documents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    site_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "heritage_sites.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    source_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey(
            "heritage_site_sources.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    document_type: Mapped[AIKnowledgeDocumentType] = mapped_column(
        SqlEnum(AIKnowledgeDocumentType),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="en",
        index=True,
    )

    provenance_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="INTERNAL_DATABASE",
        index=True,
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
