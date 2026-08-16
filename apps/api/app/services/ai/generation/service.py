from google import genai
from google.genai import types
from google.genai import errors


from app.core.config import settings
from app.services.ai.generation.contract import (
    AnswerSource,
    GroundedAnswer,
)
from app.services.ai.retrieval import (
    RAGRetrievalService,
)
from app.services.ai.retrieval.relevance_gate import (
    RetrievalRelevanceGate,
)


class GeminiQuotaExceededError(RuntimeError):
    """Raised when Gemini rejects a request because quota is exhausted."""


class GeminiProviderTimeoutError(RuntimeError):
    """Raised when Gemini generation times out."""


class GeminiProviderError(RuntimeError):
    """Raised when Gemini returns a non-quota provider error."""


class GroundedAnswerService:

    MAX_TRANSIENT_RETRIES = 3
    TRANSIENT_RETRY_DELAY_SECONDS = 3

    def __init__(
        self,
        retrieval_service: RAGRetrievalService | None = None,
    ) -> None:

        if not settings.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = getattr(
            settings,
            "GEMINI_GENERATION_MODEL",
            "gemini-2.5-flash",
        )

        self.retrieval = (
            retrieval_service
            or RAGRetrievalService()
        )

        self.relevance_gate = RetrievalRelevanceGate()


    def answer(
        self,
        query: str,
        top_k: int = 5,
    ) -> GroundedAnswer:

        normalized_query = query.strip()

        if not normalized_query:
            raise ValueError(
                "Question cannot be empty."
            )


        retrieval = self.retrieval.retrieve(
            query=normalized_query,
            top_k=top_k,
        )


        if not retrieval.results:

            return GroundedAnswer(
                query=normalized_query,
                answer=(
                    "I don't have enough verified "
                    "HeritageAI knowledge to answer "
                    "that question."
                ),
                sources=[],
                grounded=False,
            )


        relevance_decision = self.relevance_gate.evaluate(
            query=normalized_query,
            evidence=retrieval.results,
        )


        if not relevance_decision.allowed:

            return GroundedAnswer(
                query=normalized_query,
                answer=(
                    "I don't have enough verified "
                    "HeritageAI evidence to answer "
                    "that question."
                ),
                sources=[],
                grounded=False,
            )


        evidence_blocks = []


        for evidence in retrieval.results:

            evidence_blocks.append(
                (
                    f"[Evidence {evidence.rank}]\n"
                    f"Title: {evidence.title}\n"
                    f"Document Type: {evidence.document_type}\n"
                    f"Similarity: "
                    f"{evidence.similarity_score:.6f}\n"
                    f"Provenance: "
                    f"{evidence.provenance_level}\n"
                    f"Verified: "
                    f"{evidence.is_verified}\n"
                    f"Content:\n"
                    f"{evidence.content}"
                )
            )


        evidence_context = "\n\n".join(
            evidence_blocks
        )


        prompt = f"""
You are the HeritageAI historical knowledge assistant.

Answer the user's question using ONLY the supplied
HeritageAI evidence.

USER QUESTION:
{normalized_query}

SUPPLIED HERITAGEAI EVIDENCE:
{evidence_context}

GROUNDING RULES:

1. Use only facts supported by the supplied evidence.
2. Do not introduce outside historical facts.
3. Do not invent dates, names, locations, events,
   relationships, or sources.
4. If the evidence is insufficient, explicitly say
   that the available HeritageAI evidence is
   insufficient.
5. Do not mention similarity scores in the answer.
6. Do not fabricate citations.
7. Keep the answer directly relevant to the question.
8. Do not claim certainty beyond the evidence.
9. Prefer verified evidence when forming factual claims.
10. Produce a concise, informative answer.

Return only the answer text.
"""


        response = None
        last_error = None

        for attempt in range(
            1,
            self.MAX_TRANSIENT_RETRIES + 1,
        ):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                    ),
                )

                break

            except errors.ClientError as exc:
                status_code = getattr(
                    exc,
                    "status_code",
                    None,
                )

                if status_code == 429:
                    raise GeminiQuotaExceededError(
                        "Gemini generation quota has been exhausted."
                    ) from exc

                raise GeminiProviderError(
                    "Gemini provider returned an error."
                ) from exc

            except errors.ServerError as exc:
                last_error = exc

                if attempt >= self.MAX_TRANSIENT_RETRIES:
                    raise GeminiProviderError(
                        "Gemini provider temporarily unavailable "
                        "after controlled retries."
                    ) from exc

                import time

                time.sleep(
                    self.TRANSIENT_RETRY_DELAY_SECONDS
                )

            except TimeoutError as exc:
                last_error = exc

                if attempt >= self.MAX_TRANSIENT_RETRIES:
                    raise GeminiProviderTimeoutError(
                        "Gemini generation timed out "
                        "after controlled retries."
                    ) from exc

                import time

                time.sleep(
                    self.TRANSIENT_RETRY_DELAY_SECONDS
                )

        if response is None:
            raise GeminiProviderError(
                "Gemini generation returned no response."
            ) from last_error


        answer_text = (
            response.text.strip()
            if response.text
            else ""
        )


        if not answer_text:

            raise RuntimeError(
                "Gemini returned an empty answer."
            )


        sources = [
            AnswerSource(
                rank=evidence.rank,
                chunk_id=evidence.chunk_id,
                document_id=evidence.document_id,
                title=evidence.title,
                similarity_score=evidence.similarity_score,
                provenance_level=evidence.provenance_level,
                is_verified=evidence.is_verified,
            )
            for evidence in retrieval.results
        ]


        return GroundedAnswer(
            query=normalized_query,
            answer=answer_text,
            sources=sources,
            grounded=True,
        )


    def close(self) -> None:

        self.retrieval.close()
