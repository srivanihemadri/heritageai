from sqlalchemy.orm import Session

from app.models.heritage_site_relation import HeritageSiteRelation
from app.schemas.heritage_site_relation import (
    HeritageSiteRelationCreate,
    HeritageSiteRelationUpdate,
)


def create_heritage_site_relation(
    db: Session,
    source_site_id: str,
    data: HeritageSiteRelationCreate,
) -> HeritageSiteRelation:
    relation = HeritageSiteRelation(
        source_site_id=source_site_id,
        target_site_id=data.target_site_id,
        relation_type=data.relation_type,
        description=data.description,
    )

    db.add(relation)
    db.commit()
    db.refresh(relation)

    return relation


def get_heritage_site_relation_by_id(
    db: Session,
    relation_id: str,
) -> HeritageSiteRelation | None:
    return (
        db.query(HeritageSiteRelation)
        .filter(HeritageSiteRelation.id == relation_id)
        .first()
    )


def get_heritage_site_relations_by_site_id(
    db: Session,
    site_id: str,
) -> list[HeritageSiteRelation]:
    return (
        db.query(HeritageSiteRelation)
        .filter(
            HeritageSiteRelation.source_site_id == site_id,
            HeritageSiteRelation.is_active.is_(True),
        )
        .order_by(
            HeritageSiteRelation.display_order,
            HeritageSiteRelation.created_at,
        )
        .all()
    )


def update_heritage_site_relation(
    db: Session,
    relation: HeritageSiteRelation,
    data: HeritageSiteRelationUpdate,
) -> HeritageSiteRelation:
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(relation, field, value)

    db.commit()
    db.refresh(relation)

    return relation


def delete_heritage_site_relation(
    db: Session,
    relation: HeritageSiteRelation,
) -> None:
    relation.is_active = False

    db.commit()
