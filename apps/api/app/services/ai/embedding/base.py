from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Provider-agnostic contract for text embedding."""

    @abstractmethod
    def embed_document(self, text: str) -> list[float]:
        """Generate a document embedding."""
        raise NotImplementedError
