"""Application SQLAlchemy model registry.

Importing this package registers every ORM model with Base.metadata.
The declarative Base itself remains dependency-free to avoid circular imports.
"""

from app.models.user import User
from app.models.heritage_site import HeritageSite
from app.models.heritage_site_historical_event import HeritageSiteHistoricalEvent
from app.models.heritage_site_media import HeritageSiteMedia
from app.models.heritage_site_metadata import HeritageSiteMetadata
from app.models.heritage_site_relation import HeritageSiteRelation
from app.models.heritage_site_source import HeritageSiteSource

from app.models.ai.knowledge_document import AIKnowledgeDocument
from app.models.ai.knowledge_chunk import AIKnowledgeChunk
from app.models.ai.embedding import AIEmbedding

from app.models.scan import Scan

__all__ = [
    "User",
    "HeritageSite",
    "HeritageSiteHistoricalEvent",
    "HeritageSiteMedia",
    "HeritageSiteMetadata",
    "HeritageSiteRelation",
    "HeritageSiteSource",
    "AIKnowledgeDocument",
    "AIKnowledgeChunk",
    "AIEmbedding",
    "Scan",
]
