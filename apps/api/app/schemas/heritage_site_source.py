from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models.heritage_site_source import SourceType


class HeritageSiteSourceCreate(BaseModel):
    source_type: SourceType
    title: str = Field(
        min_length=2,
        max_length=300,
    )
    author: str | None = Field(
        default=None,
        max_length=300,
    )
    organization: str | None = Field(
        default=None,
        max_length=300,
    )
    publisher: str | None = Field(
        default=None,
        max_length=300,
    )
    publication_date: date | None = None
    url: str | None = Field(
        default=None,
        max_length=1000,
    )
    citation_text: str | None = None
    language: str = Field(
        default="en",
        min_length=2,
        max_length=20,
    )


class HeritageSiteSourceUpdate(BaseModel):
    source_type: SourceType | None = None
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=300,
    )
    author: str | None = Field(
        default=None,
        max_length=300,
    )
    organization: str | None = Field(
        default=None,
        max_length=300,
    )
    publisher: str | None = Field(
        default=None,
        max_length=300,
    )
    publication_date: date | None = None
    url: str | None = Field(
        default=None,
        max_length=1000,
    )
    citation_text: str | None = None
    language: str | None = Field(
        default=None,
        min_length=2,
        max_length=20,
    )


class HeritageSiteSourceResponse(BaseModel):
    id: str
    site_id: str
    source_type: SourceType
    title: str
    author: str | None
    organization: str | None
    publisher: str | None
    publication_date: date | None
    url: str | None
    citation_text: str | None
    language: str
    display_order: int
    is_verified: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class HeritageSiteSourceListResponse(BaseModel):
    sources: list[HeritageSiteSourceResponse]
    total: int
