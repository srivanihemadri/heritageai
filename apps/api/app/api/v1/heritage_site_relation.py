from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_admin
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.heritage_site_relation import (
    HeritageSiteRelationCreate,
    HeritageSiteRelationListResponse,
    HeritageSiteRelationResponse,
    HeritageSiteRelationUpdate,
)
from app.services.heritage_site_relation import (
    create_relation,
    delete_relation,
    get_relation_or_404,
    list_relations,
    update_relation,
)

router = APIRouter(
    prefix="/heritage-sites/{site_id}/relations",
    tags=["Heritage Site Relations"],
)


@router.get(
    "",
    response_model=APIResponse[HeritageSiteRelationListResponse],
)
def list_heritage_site_relations(
    site_id: str,
    db: Session = Depends(get_db),
):
    relations = list_relations(
        db,
        site_id,
    )

    return APIResponse(
        success=True,
        data=HeritageSiteRelationListResponse(
            relations=relations,
            total=len(relations),
        ),
        message="Heritage site relations retrieved successfully",
    )


@router.get(
    "/{relation_id}",
    response_model=APIResponse[HeritageSiteRelationResponse],
)
def get_heritage_site_relation(
    site_id: str,
    relation_id: str,
    db: Session = Depends(get_db),
):
    relation = get_relation_or_404(
        db,
        relation_id,
    )

    if relation.source_site_id != site_id:
        from app.core.exceptions import ResourceNotFoundException

        raise ResourceNotFoundException(
            message="Heritage site relation not found",
            error_code="HERITAGE_SITE_RELATION_NOT_FOUND",
        )

    return APIResponse(
        success=True,
        data=relation,
        message="Heritage site relation retrieved successfully",
    )


@router.post(
    "",
    response_model=APIResponse[HeritageSiteRelationResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_heritage_site_relation(
    site_id: str,
    data: HeritageSiteRelationCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    relation = create_relation(
        db,
        site_id,
        data,
    )

    return APIResponse(
        success=True,
        data=relation,
        message="Heritage site relation created successfully",
    )


@router.patch(
    "/{relation_id}",
    response_model=APIResponse[HeritageSiteRelationResponse],
)
def update_heritage_site_relation(
    site_id: str,
    relation_id: str,
    data: HeritageSiteRelationUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    relation = get_relation_or_404(
        db,
        relation_id,
    )

    if relation.source_site_id != site_id:
        from app.core.exceptions import ResourceNotFoundException

        raise ResourceNotFoundException(
            message="Heritage site relation not found",
            error_code="HERITAGE_SITE_RELATION_NOT_FOUND",
        )

    relation = update_relation(
        db,
        relation_id,
        data,
    )

    return APIResponse(
        success=True,
        data=relation,
        message="Heritage site relation updated successfully",
    )


@router.delete(
    "/{relation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_heritage_site_relation(
    site_id: str,
    relation_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    relation = get_relation_or_404(
        db,
        relation_id,
    )

    if relation.source_site_id != site_id:
        from app.core.exceptions import ResourceNotFoundException

        raise ResourceNotFoundException(
            message="Heritage site relation not found",
            error_code="HERITAGE_SITE_RELATION_NOT_FOUND",
        )

    delete_relation(
        db,
        relation_id,
    )

    return None
