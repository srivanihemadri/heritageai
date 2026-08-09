from pydantic import BaseModel, ConfigDict, Field


class HeritageSiteCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=200,
    )
    slug: str = Field(
        min_length=2,
        max_length=220,
    )
    short_description: str | None = Field(
        default=None,
        max_length=500,
    )
    description: str | None = None
    category: str = Field(
        min_length=2,
        max_length=100,
    )
    country: str = Field(
        min_length=2,
        max_length=100,
    )
    state: str | None = Field(
        default=None,
        max_length=100,
    )
    city: str | None = Field(
        default=None,
        max_length=100,
    )
    latitude: float | None = None
    longitude: float | None = None
    established_year: int | None = None
    architectural_style: str | None = Field(
        default=None,
        max_length=150,
    )
    historical_period: str | None = Field(
        default=None,
        max_length=150,
    )
    significance: str | None = None
    preservation_status: str | None = Field(
        default=None,
        max_length=100,
    )


class HeritageSiteUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )
    slug: str | None = Field(
        default=None,
        min_length=2,
        max_length=220,
    )
    short_description: str | None = Field(
        default=None,
        max_length=500,
    )
    description: str | None = None
    category: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    country: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    state: str | None = Field(
        default=None,
        max_length=100,
    )
    city: str | None = Field(
        default=None,
        max_length=100,
    )
    latitude: float | None = None
    longitude: float | None = None
    established_year: int | None = None
    architectural_style: str | None = Field(
        default=None,
        max_length=150,
    )
    historical_period: str | None = Field(
        default=None,
        max_length=150,
    )
    significance: str | None = None
    preservation_status: str | None = Field(
        default=None,
        max_length=100,
    )


class HeritageSiteResponse(BaseModel):
    id: str
    name: str
    slug: str
    short_description: str | None
    description: str | None
    category: str
    country: str
    state: str | None
    city: str | None
    latitude: float | None
    longitude: float | None
    established_year: int | None
    architectural_style: str | None
    historical_period: str | None
    significance: str | None
    preservation_status: str | None
    is_verified: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class HeritageSiteListResponse(BaseModel):
    sites: list[HeritageSiteResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
