from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.scan import Scan
from app.services.ai.scanner.contract import HeritageScannerResult


class ScanRepository:
    """Persistence boundary for authenticated heritage scanner results."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        user_id: str,
        result: HeritageScannerResult,
    ) -> Scan:
        scan = Scan(
            user_id=user_id,
            identification_status=result.identification_status,
            evidence_quality=result.evidence_quality,
            identified_name=result.identified_name,
            category=result.category,
            location=result.location,
            country=result.country,
            confidence=result.confidence,
            confidence_level=result.confidence_level,
            description=result.description,
            architectural_style=result.architectural_style,
            historical_period=result.historical_period,
            historical_significance=result.historical_significance,
            visual_evidence=result.visual_evidence,
            alternative_matches=result.alternative_matches,
            grounding_status=result.grounding_status,
        )

        self.db.add(scan)
        self.db.flush()

        return scan

    def get_by_id(
        self,
        *,
        scan_id: str,
        user_id: str,
    ) -> Scan | None:
        statement = (
            select(Scan)
            .where(
                Scan.id == scan_id,
                Scan.user_id == user_id,
            )
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def list_by_user(
        self,
        *,
        user_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Scan]:
        statement = (
            select(Scan)
            .where(
                Scan.user_id == user_id,
            )
            .order_by(
                Scan.created_at.desc(),
            )
            .limit(limit)
            .offset(offset)
        )

        return list(
            self.db.execute(
                statement
            ).scalars().all()
        )
