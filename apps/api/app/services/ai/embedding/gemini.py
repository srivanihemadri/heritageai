import math

from google import genai
from google.genai import types

from app.core.config import settings

from .base import EmbeddingProvider


class GeminiEmbeddingService(EmbeddingProvider):
    """
    Gemini implementation of the HeritageAI embedding provider.

    The service performs embedding generation only.
    Persistence is handled by the vector repository / pipeline.
    """

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.GEMINI_EMBEDDING_MODEL
        self.dimensions = settings.GEMINI_EMBEDDING_DIMENSIONS

    def embed_document(
        self,
        text: str,
    ) -> list[float]:

        if not text or not text.strip():
            raise ValueError(
                "Cannot embed empty text."
            )

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=self.dimensions,
            ),
        )

        if not response.embeddings:
            raise RuntimeError(
                "Gemini returned no embedding."
            )

        vector = response.embeddings[0].values

        if len(vector) != self.dimensions:
            raise RuntimeError(
                "Gemini returned an unexpected vector dimension: "
                f"expected {self.dimensions}, "
                f"received {len(vector)}."
            )

        return normalize_vector(vector)


def normalize_vector(
    vector: list[float],
) -> list[float]:
    """
    L2-normalize a vector.

    Gemini embeddings are normalized here so the
    resulting vector is suitable for cosine similarity.
    """

    if not vector:
        raise ValueError(
            "Cannot normalize an empty vector."
        )

    magnitude = math.sqrt(
        sum(
            value * value
            for value in vector
        )
    )

    if magnitude == 0:
        raise ValueError(
            "Cannot normalize a zero vector."
        )

    return [
        value / magnitude
        for value in vector
    ]
