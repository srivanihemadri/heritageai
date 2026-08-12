from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models.heritage_site_historical_event import DatePrecision


class HeritageSiteHistoricalEventCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=300,
    )
    description: str | None = None
    event_date: date | None = None
    date_label: str | None = None
    date_precision: DatePrecision = DatePrecision.UNKNOWN
    display_order: int = Field(default=0, ge=0)
    significance: str | None = None


class HeritageSiteHistoricalEventUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=300,
    )
    description: str | None = None
    event_date: date | None = None
    date_label: str | None = None
    date_precision: DatePrecision | None = None
    display_order: int | None = Field(default=None, ge=0)
    significance: str | None = None


class HeritageSiteHistoricalEventResponse(BaseModel):
    id: str
    site_id: str
    title: str
    description: str | None
    event_date: date | None
    date_label: str | None
    date_precision: DatePrecision
    significance: str | None
    display_order: int
    is_verified: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class HeritageSiteHistoricalEventListResponse(BaseModel):
    events: list[HeritageSiteHistoricalEventResponse]
    total: int
