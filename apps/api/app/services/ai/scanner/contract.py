"""Contracts for the AI Heritage Scanner."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


ScannerConfidence = Literal["LOW", "MEDIUM", "HIGH"]

ScannerIdentificationStatus = Literal[
    "IDENTIFIED",
    "POSSIBLE_MATCH",
    "INSUFFICIENT_EVIDENCE",
    "NOT_HERITAGE",
    "AMBIGUOUS",
]

ScannerEvidenceQuality = Literal[
    "STRONG",
    "MODERATE",
    "WEAK",
    "NONE",
]

ScannerGroundingStatus = Literal[
    "GROUNDED",
    "PARTIALLY_GROUNDED",
    "UNVERIFIED",
]


class HeritageScannerResult(BaseModel):
    """Structured multimodal heritage identification result."""

    identified_name: str | None = None

    identification_status: ScannerIdentificationStatus = (
        "INSUFFICIENT_EVIDENCE"
    )

    evidence_quality: ScannerEvidenceQuality = "NONE"

    category: str | None = None

    location: str | None = None

    country: str | None = None

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    confidence_level: ScannerConfidence = "LOW"

    description: str | None = None

    architectural_style: str | None = None

    historical_period: str | None = None

    historical_significance: str | None = None

    visual_evidence: list[str] = Field(
        default_factory=list,
    )

    alternative_matches: list[str] = Field(
        default_factory=list,
    )

    grounding_status: ScannerGroundingStatus = "UNVERIFIED"

    @model_validator(mode="after")
    def validate_semantic_consistency(self) -> "HeritageScannerResult":
        """Enforce semantic consistency between scanner confidence and evidence."""

        if self.identified_name is not None:
            normalized_name = self.identified_name.strip()

            if not normalized_name:
                raise ValueError(
                    "identified_name cannot be empty when provided."
                )

            self.identified_name = normalized_name

        if self.identification_status == "IDENTIFIED":

            if not self.identified_name:
                raise ValueError(
                    "IDENTIFIED status requires an identified_name."
                )

            if not self.visual_evidence:
                raise ValueError(
                    "IDENTIFIED status requires visual_evidence."
                )

        if self.identification_status == "POSSIBLE_MATCH":

            if not self.visual_evidence:
                raise ValueError(
                    "POSSIBLE_MATCH status requires visual_evidence."
                )

            if self.confidence_level == "HIGH":
                raise ValueError(
                    "POSSIBLE_MATCH cannot use HIGH confidence."
                )

        if self.identification_status == "AMBIGUOUS":

            if len(self.alternative_matches) < 2:
                raise ValueError(
                    "AMBIGUOUS status requires at least two alternative_matches."
                )

        if self.identification_status == "INSUFFICIENT_EVIDENCE":

            if self.confidence_level == "HIGH":
                raise ValueError(
                    "INSUFFICIENT_EVIDENCE cannot use HIGH confidence."
                )

        if self.identification_status == "NOT_HERITAGE":

            if self.identified_name:
                raise ValueError(
                    "NOT_HERITAGE cannot contain an identified_name."
                )

        if self.evidence_quality == "STRONG":

            if not self.visual_evidence:
                raise ValueError(
                    "STRONG evidence quality requires visual_evidence."
                )

        if self.evidence_quality == "NONE":

            if self.visual_evidence:
                raise ValueError(
                    "NONE evidence quality cannot contain visual_evidence."
                )

        if self.confidence_level == "HIGH":

            if self.confidence < 0.90:
                raise ValueError(
                    "HIGH confidence requires confidence >= 0.90."
                )

            if not self.identified_name:
                raise ValueError(
                    "HIGH confidence requires an identified_name."
                )

            if not self.visual_evidence:
                raise ValueError(
                    "HIGH confidence requires visual_evidence."
                )

        elif self.confidence_level == "MEDIUM":

            if self.confidence < 0.50 or self.confidence >= 0.90:
                raise ValueError(
                    "MEDIUM confidence requires confidence >= 0.50 and < 0.90."
                )

        elif self.confidence_level == "LOW":

            if self.confidence >= 0.50:
                raise ValueError(
                    "LOW confidence requires confidence < 0.50."
                )

        if self.grounding_status == "GROUNDED":

            if not self.visual_evidence:
                raise ValueError(
                    "GROUNDED results require visual_evidence."
                )

        return self


class HeritageScannerResponse(BaseModel):
    """Public scanner response."""

    success: bool = True

    scan_id: str

    result: HeritageScannerResult
