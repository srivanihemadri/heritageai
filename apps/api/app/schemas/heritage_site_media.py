from pydantic import BaseModel, ConfigDict, Field

from app.models.heritage_site_media import MediaType


class HeritageSiteMediaCreate(BaseModel):
    media_type: MediaType

    storage_key: str = Field(
        min_length=1,
        max_length=500,
    )

    url: str = Field(
        min_length=1,
        max_length=1000,
    )

    title: str | None = Field(
        default=None,
        max_length=200,
    )

    alt_text: str | None = Field(
        default=None,
        max_length=500,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_primary: bool = False


class HeritageSiteMediaUpdate(BaseModel):
    media_type: MediaType | None = None

    storage_key: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )

    url: str | None = Field(
        default=None,
        min_length=1,
        max_length=1000,
    )

    title: str | None = Field(
        default=None,
        max_length=200,
    )

    alt_text: str | None = Field(
        default=None,
        max_length=500,
    )

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_primary: bool | None = None
    is_active: bool | None = None


class HeritageSiteMediaResponse(BaseModel):
    id: str
    site_id: str
    media_type: MediaType
    storage_key: str
    url: str
    title: str | None
    alt_text: str | None
    display_order: int
    is_primary: bool
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class HeritageSiteMediaListResponse(BaseModel):
    media: list[HeritageSiteMediaResponse]
    total: int
