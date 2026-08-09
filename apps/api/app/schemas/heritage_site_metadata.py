from pydantic import BaseModel, ConfigDict, Field


class HeritageSiteMetadataCreate(BaseModel):
    metadata_type: str = Field(
        min_length=2,
        max_length=100,
    )

    title: str = Field(
        min_length=2,
        max_length=200,
    )

    content: str = Field(
        min_length=1,
    )

    source: str | None = Field(
        default=None,
        max_length=300,
    )

    source_url: str | None = Field(
        default=None,
        max_length=1000,
    )

    language: str = Field(
        default="en",
        min_length=2,
        max_length=20,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )


class HeritageSiteMetadataUpdate(BaseModel):
    metadata_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    content: str | None = Field(
        default=None,
        min_length=1,
    )

    source: str | None = Field(
        default=None,
        max_length=300,
    )

    source_url: str | None = Field(
        default=None,
        max_length=1000,
    )

    language: str | None = Field(
        default=None,
        min_length=2,
        max_length=20,
    )

    display_order: int | None = Field(
        default=None,
        ge=0,
    )


class HeritageSiteMetadataResponse(BaseModel):
    id: str
    site_id: str
    metadata_type: str
    title: str
    content: str
    source: str | None
    source_url: str | None
    language: str
    display_order: int
    is_verified: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class HeritageSiteMetadataListResponse(BaseModel):
    metadata: list[HeritageSiteMetadataResponse]
    total: int
