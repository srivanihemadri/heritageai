from types import SimpleNamespace

from app.services.ai.retrieval.relevance_gate import (
    RetrievalRelevanceGate,
)


def _evidence(site_name: str):
    return [
        SimpleNamespace(
            rank=1,
            chunk_id="chunk-1",
            document_id="doc-1",
            document_type="SITE_PROFILE",
            title=f"{site_name} Heritage Profile",
            content=f"{site_name} is a protected heritage site.",
            similarity_score=0.716,
            provenance_level="INTERNAL_DATABASE",
            language="en",
            is_verified=True,
            site_id="site-1",
            site_name=site_name,
            source_id=None,
        )
    ]


def test_explicit_mismatched_site_is_rejected():
    gate = RetrievalRelevanceGate()

    decision = gate.evaluate(
        "Tell me about the Taj Mahal.",
        _evidence("Angkor Wat"),
    )

    assert decision.allowed is False


def test_explicit_matching_site_is_allowed():
    gate = RetrievalRelevanceGate()

    decision = gate.evaluate(
        "Tell me about the Taj Mahal.",
        _evidence("Taj Mahal"),
    )

    assert decision.allowed is True


def test_unrelated_country_capital_is_rejected():
    gate = RetrievalRelevanceGate()

    decision = gate.evaluate(
        "What is the capital of Brazil?",
        _evidence("Acropolis of Athens"),
    )

    assert decision.allowed is False


def test_contextual_query_without_entity_remains_allowed():
    gate = RetrievalRelevanceGate()

    decision = gate.evaluate(
        "Where is it located?",
        _evidence("Taj Mahal"),
    )

    assert decision.allowed is True
