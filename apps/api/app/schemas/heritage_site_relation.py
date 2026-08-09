from pydantic import BaseModel, ConfigDict, Field

from app.models.heritage_site_relation import RelationType


class HeritageSiteRelationCreate(BaseModel):
    target_site_id: str = Field(min_length=36, max_length=36)
    relation_type: RelationType
    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class HeritageSiteRelationUpdate(BaseModel):
    relation_type: RelationType | None = None
    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class HeritageSiteRelationResponse(BaseModel):
    id: str
    source_site_id: str
    target_site_id: str
    relation_type: RelationType
    description: str | None
    display_order: int
    is_verified: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class HeritageSiteRelationListResponse(BaseModel):
    relations: list[HeritageSiteRelationResponse]
    total: int
