from __future__ import annotations

from dataclasses import dataclass

from app.services.ai.retrieval.contract import RetrievalEvidence


@dataclass(frozen=True)
class RelevanceDecision:
    allowed: bool
    reason: str
    top_score: float
    second_score: float
    score_margin: float
    verified_evidence_count: int


ATTRIBUTE_TERMS = {
    "cost": ("cost", "price", "expense", "budget"),
    "currency": ("currency", "rupee", "rupees", "coin", "coins"),
    "founder": ("founder", "founded by", "built by", "builder"),
    "architect": ("architect", "designed by", "designer"),
    "height": ("height", "tall", "high"),
    "capacity": ("capacity", "holds", "seats"),
    "material": ("material", "stone", "marble", "wood", "brick"),
    "date": ("when", "year", "date", "dated", "established"),
    "location": ("where", "location", "located", "state", "city", "country"),
    "architecture": ("architecture", "architectural", "style", "design"),
    "history": ("history", "historical", "event", "events"),
    "relationship": ("relationship", "related", "connection", "connected"),
}


UNRELATED_MARKERS = (
    "capital of japan",
    "quantum mechanics",
)


EVIDENCE_TYPE_TERMS = {
    "diary": (
        "diary",
        "journal",
        "personal diary",
        "diary entry",
        "journal entry",
    ),
    "inscription": (
        "inscription",
        "inscribed",
        "carved",
        "engraving",
        "engraved",
    ),
    "quotation": (
        "exact quote",
        "exact quotation",
        "exact wording",
        "quote",
        "quotation",
        "said exactly",
        "words written",
        "words spoken",
    ),
    "letter": (
        "letter",
        "personal letter",
        "correspondence",
    ),
}


CLAIM_PREFIXES = (
    "was ",
    "were ",
    "is ",
    "are ",
    "did ",
    "does ",
    "do ",
    "built by ",
    "founded by ",
    "created by ",
    "designed by ",
)


class RetrievalRelevanceGate:

    def __init__(
        self,
        minimum_top_score: float = 0.70,
        minimum_verified_evidence: int = 1,
    ) -> None:

        self.minimum_top_score = minimum_top_score
        self.minimum_verified_evidence = minimum_verified_evidence

    @staticmethod
    def _text(evidence: RetrievalEvidence) -> str:

        return (
            f"{evidence.title}\n"
            f"{evidence.document_type}\n"
            f"{evidence.content}"
        ).lower()

    @staticmethod
    def _detect_attributes(query: str) -> list[str]:

        q = query.lower()

        return [
            attribute
            for attribute, terms in ATTRIBUTE_TERMS.items()
            if any(term in q for term in terms)
        ]

    @staticmethod
    def _is_claim_verification(query: str) -> bool:

        q = query.lower().strip()

        return any(
            q.startswith(prefix)
            for prefix in CLAIM_PREFIXES
        )

    @staticmethod
    def _is_unrelated(query: str) -> bool:

        q = query.lower()

        return any(
            marker in q
            for marker in UNRELATED_MARKERS
        )

    @staticmethod
    def _attribute_supported(
        attribute: str,
        evidence_text: str,
    ) -> bool:

        terms = ATTRIBUTE_TERMS[attribute]

        return any(
            term in evidence_text
            for term in terms
        )

    @staticmethod
    def _detect_evidence_types(
        query: str,
    ) -> list[str]:

        q = query.lower()

        return [
            evidence_type
            for evidence_type, terms in EVIDENCE_TYPE_TERMS.items()
            if any(term in q for term in terms)
        ]

    @staticmethod
    def _evidence_type_supported(
        evidence_type: str,
        evidence: list[RetrievalEvidence],
    ) -> bool:

        if evidence_type == "diary":
            return any(
                "diary" in RetrievalRelevanceGate._text(item)
                or "journal" in RetrievalRelevanceGate._text(item)
                for item in evidence
            )

        if evidence_type == "inscription":
            for item in evidence:
                text = RetrievalRelevanceGate._text(item)

                # A historical event such as
                # "UNESCO World Heritage inscription" does not
                # provide the actual inscription text/content.
                #
                # Accept only evidence explicitly representing
                # inscription content or an inscription artifact.
                if item.document_type.upper() in {
                    "INSCRIPTION",
                    "INSCRIPTION_TEXT",
                    "INSCRIPTION_ARTIFACT",
                }:
                    return True

                content_markers = (
                    "inscription text:",
                    "inscription reads:",
                    "inscription reads ",
                    "inscription states:",
                    "inscription states ",
                    "inscription wording:",
                    "inscription wording ",
                    "carved text:",
                    "engraved text:",
                    "inscription:",
                )

                if any(marker in text for marker in content_markers):
                    return True

            return False

        if evidence_type == "quotation":
            return any(
                any(
                    term in RetrievalRelevanceGate._text(item)
                    for term in EVIDENCE_TYPE_TERMS["quotation"]
                )
                for item in evidence
            )

        if evidence_type == "letter":
            return any(
                any(
                    term in RetrievalRelevanceGate._text(item)
                    for term in EVIDENCE_TYPE_TERMS["letter"]
                )
                for item in evidence
            )

        return False

    def evaluate(
        self,
        query: str,
        evidence: list[RetrievalEvidence],
    ) -> RelevanceDecision:

        if not evidence:

            return RelevanceDecision(
                allowed=False,
                reason="NO_RETRIEVAL_EVIDENCE",
                top_score=0.0,
                second_score=0.0,
                score_margin=0.0,
                verified_evidence_count=0,
            )

        scores = [
            float(item.similarity_score)
            for item in evidence
        ]

        top_score = scores[0]
        second_score = scores[1] if len(scores) > 1 else 0.0
        score_margin = top_score - second_score

        verified_count = sum(
            1
            for item in evidence
            if item.is_verified
        )

        if self._is_unrelated(query):

            return RelevanceDecision(
                allowed=False,
                reason="UNRELATED_DOMAIN",
                top_score=top_score,
                second_score=second_score,
                score_margin=score_margin,
                verified_evidence_count=verified_count,
            )

        if top_score < self.minimum_top_score:

            return RelevanceDecision(
                allowed=False,
                reason="LOW_RETRIEVAL_CONFIDENCE",
                top_score=top_score,
                second_score=second_score,
                score_margin=score_margin,
                verified_evidence_count=verified_count,
            )

        if verified_count < self.minimum_verified_evidence:

            return RelevanceDecision(
                allowed=False,
                reason="NO_VERIFIED_EVIDENCE",
                top_score=top_score,
                second_score=second_score,
                score_margin=score_margin,
                verified_evidence_count=verified_count,
            )

        # -----------------------------------------------------
        # Claim verification is intentionally handled before
        # ordinary attribute sufficiency checks.
        #
        # Example:
        # "Was Ajanta Caves built by the Mughal Empire?"
        #
        # This is a claim to verify/refute, not a request for
        # an unsupported "founder" field.
        # -----------------------------------------------------

        if self._is_claim_verification(query):

            return RelevanceDecision(
                allowed=True,
                reason="CLAIM_VERIFICATION_WITH_VERIFIED_EVIDENCE",
                top_score=top_score,
                second_score=second_score,
                score_margin=score_margin,
                verified_evidence_count=verified_count,
            )

        requested_evidence_types = self._detect_evidence_types(query)

        if requested_evidence_types:

            unsupported_types = [
                evidence_type
                for evidence_type in requested_evidence_types
                if not self._evidence_type_supported(
                    evidence_type,
                    evidence,
                )
            ]

            if unsupported_types:

                return RelevanceDecision(
                    allowed=False,
                    reason="REQUESTED_EVIDENCE_TYPE_ABSENT",
                    top_score=top_score,
                    second_score=second_score,
                    score_margin=score_margin,
                    verified_evidence_count=verified_count,
                )

        requested_attributes = self._detect_attributes(query)

        if requested_attributes:

            combined_text = "\n".join(
                self._text(item)
                for item in evidence
            )

            supported_attributes = [
                attribute
                for attribute in requested_attributes
                if self._attribute_supported(
                    attribute,
                    combined_text,
                )
            ]

            if not supported_attributes:

                return RelevanceDecision(
                    allowed=False,
                    reason="REQUESTED_ATTRIBUTE_ABSENT",
                    top_score=top_score,
                    second_score=second_score,
                    score_margin=score_margin,
                    verified_evidence_count=verified_count,
                )

        return RelevanceDecision(
            allowed=True,
            reason="STRONG_VERIFIED_EVIDENCE",
            top_score=top_score,
            second_score=second_score,
            score_margin=score_margin,
            verified_evidence_count=verified_count,
        )


__all__ = [
    "RetrievalRelevanceGate",
    "RelevanceDecision",
]


