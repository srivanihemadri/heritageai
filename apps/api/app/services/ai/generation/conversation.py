from __future__ import annotations

import random
import re
from enum import StrEnum


class ConversationIntent(StrEnum):
    GREETING = "greeting"
    HOW_ARE_YOU = "how_are_you"
    THANKS = "thanks"
    GOODBYE = "goodbye"
    IDENTITY = "identity"
    NONE = "none"


class ConversationalIntentService:
    """
    Detects lightweight conversational messages that should not
    be sent through the heritage RAG pipeline.

    This layer is intentionally conservative:
    factual heritage questions continue through retrieval
    and the existing relevance gate.
    """

    _GREETING_PATTERNS = (
        r"^(hi|hello|hey|hiya|heya)(?:\s+(man|bro|buddy|there|dude))?[!.?,\s]*$",
        r"^(good\s+morning|good\s+afternoon|good\s+evening)[!.?,\s]*$",
        r"^namaste[!.?,\s]*$",
    )

    _HOW_ARE_YOU_PATTERNS = (
        r"^how\s+are\s+you[!.?,\s]*$",
        r"^how\s+r\s+u[!.?,\s]*$",
        r"^how\s+you\s+doing[!.?,\s]*$",
        r"^how\s+is\s+it\s+going[!.?,\s]*$",
        r"^how\s+are\s+things[!.?,\s]*$",
    )

    _THANKS_PATTERNS = (
        r"^(thanks|thank\s+you|thx|ty)(?:\s+(man|bro|buddy|dude))?[!.?,\s]*$",
        r"^(thanks|thank\s+you)\s+(a\s+lot|so\s+much)[!.?,\s]*$",
    )

    _GOODBYE_PATTERNS = (
        r"^(bye|goodbye|see\s+you|see\s+ya|talk\s+to\s+you\s+later)[!.?,\s]*$",
        r"^(good\s+night)[!.?,\s]*$",
    )

    _IDENTITY_PATTERNS = (
        r"^who\s+are\s+you[!.?,\s]*$",
        r"^what\s+are\s+you[!.?,\s]*$",
        r"^what\s+is\s+heritageai[!.?,\s]*$",
        r"^tell\s+me\s+about\s+yourself[!.?,\s]*$",
    )

    @staticmethod
    def _normalize(message: str) -> str:
        return re.sub(
            r"\s+",
            " ",
            message.strip().lower(),
        )

    @staticmethod
    def _matches(
        normalized: str,
        patterns: tuple[str, ...],
    ) -> bool:
        return any(
            re.fullmatch(pattern, normalized)
            for pattern in patterns
        )

    def detect(self, message: str) -> ConversationIntent:
        normalized = self._normalize(message)

        if not normalized:
            return ConversationIntent.NONE

        if self._matches(
            normalized,
            self._GREETING_PATTERNS,
        ):
            return ConversationIntent.GREETING

        if self._matches(
            normalized,
            self._HOW_ARE_YOU_PATTERNS,
        ):
            return ConversationIntent.HOW_ARE_YOU

        if self._matches(
            normalized,
            self._THANKS_PATTERNS,
        ):
            return ConversationIntent.THANKS

        if self._matches(
            normalized,
            self._GOODBYE_PATTERNS,
        ):
            return ConversationIntent.GOODBYE

        if self._matches(
            normalized,
            self._IDENTITY_PATTERNS,
        ):
            return ConversationIntent.IDENTITY

        return ConversationIntent.NONE

    def respond(
        self,
        intent: ConversationIntent,
    ) -> str:
        responses = {
            ConversationIntent.GREETING: (
                "Hey! 👋 Good to see you. "
                "What are we exploring today?"
            ),
            ConversationIntent.HOW_ARE_YOU: (
                "I'm doing great! 😄 "
                "Ready to explore India's heritage with you. "
                "What are you curious about?"
            ),
            ConversationIntent.THANKS: (
                "Anytime! 🙌 "
                "I'm always happy to help."
            ),
            ConversationIntent.GOODBYE: (
                "See you! 👋 "
                "Come back whenever you want to explore some history."
            ),
            ConversationIntent.IDENTITY: (
                "I'm HeritageAI 🤖 — your companion for exploring "
                "India's heritage, monuments, history, architecture, "
                "culture, and the stories behind the places you discover."
            ),
        }

        response = responses.get(intent)

        if response is None:
            raise ValueError(
                f"No conversational response for intent: {intent}"
            )

        return response
