from types import SimpleNamespace

from app.services.ai.retrieval.relevance_gate import (
    RetrievalRelevanceGate,
)


def test_heritage_intent_keywords_are_recognized():
    gate = RetrievalRelevanceGate()

    heritage_queries = [
        "What is the history of Angkor Wat?",
        "Where is Machu Picchu located?",
        "What architectural style does the Acropolis have?",
    ]

    for query in heritage_queries:
        assert gate._is_heritage_intent(query) is True


def test_canonical_site_name_matches_query():
    gate = RetrievalRelevanceGate()

    evidence = [
        SimpleNamespace(
            site_name="Taj Mahal",
            title="Taj Mahal — Heritage Profile",
            content="The Taj Mahal is a monumental Mughal complex.",
            document_type="SITE_PROFILE",
        )
    ]

    assert gate._site_entity_supported(
        "Tell me about the Taj Mahal.",
        evidence,
    ) is True


def test_canonical_site_name_matches_case_insensitively():
    gate = RetrievalRelevanceGate()

    evidence = [
        SimpleNamespace(
            site_name="Taj Mahal",
            title="Taj Mahal — Heritage Profile",
            content="The Taj Mahal is a monumental Mughal complex.",
            document_type="SITE_PROFILE",
        )
    ]

    assert gate._site_entity_supported(
        "tell me about TAJ MAHAL",
        evidence,
    ) is True


def test_unrelated_entity_does_not_match_heritage_evidence():
    gate = RetrievalRelevanceGate()

    evidence = [
        SimpleNamespace(
            site_name="Taj Mahal",
            title="Taj Mahal — Heritage Profile",
            content="The Taj Mahal is a monumental Mughal complex.",
            document_type="SITE_PROFILE",
        )
    ]

    assert gate._site_entity_supported(
        "What is the capital of Brazil?",
        evidence,
    ) is False


def test_unrelated_queries_are_not_recognized_as_heritage():
    gate = RetrievalRelevanceGate()

    unrelated_queries = [
        "What is the capital of Brazil?",
        "What is quantum mechanics?",
        "What is the weather today?",
        "Who won yesterday's cricket match?",
    ]

    for query in unrelated_queries:
        assert gate._is_heritage_intent(query) is False


def test_heritage_attribute_queries_are_recognized():
    gate = RetrievalRelevanceGate()

    queries = [
        "What is the cost?",
        "Where is it located?",
        "What architectural style is it?",
        "What is its historical significance?",
        "When was it established?",
    ]

    for query in queries:
        assert gate._is_heritage_intent(query) is True


def test_heritage_claim_queries_are_recognized():
    gate = RetrievalRelevanceGate()

    queries = [
        "Was the monument built by the Mughal Empire?",
        "Is the Taj Mahal a UNESCO site?",
        "Who built the monument?",
        "Was it designed by a famous architect?",
    ]

    for query in queries:
        assert gate._is_heritage_intent(query) is True


def test_existing_unrelated_markers_remain_unrelated():
    gate = RetrievalRelevanceGate()

    assert gate._is_heritage_intent("What is the capital of Japan?") is False
    assert gate._is_heritage_intent("Explain quantum mechanics.") is False


def _make_evidence(
    site_name: str,
    *,
    score: float = 0.90,
    verified: bool = True,
):
    return SimpleNamespace(
        site_name=site_name,
        title=f"{site_name} — Heritage Profile",
        content=f"{site_name} is a protected heritage monument.",
        document_type="SITE_PROFILE",
        similarity_score=score,
        is_verified=verified,
    )


def test_explicit_heritage_entity_allows_matching_evidence():
    gate = RetrievalRelevanceGate()

    evidence = [
        _make_evidence("Taj Mahal"),
    ]

    decision = gate.evaluate(
        "Tell me about the Taj Mahal.",
        evidence,
    )

    assert decision.allowed is True


def test_explicit_heritage_entity_rejects_mismatched_evidence():
    gate = RetrievalRelevanceGate()

    evidence = [
        _make_evidence("Angkor Wat"),
    ]

    decision = gate.evaluate(
        "Tell me about the Taj Mahal.",
        evidence,
    )

    assert decision.allowed is False


def test_contextual_attribute_query_remains_supported_without_entity_name():
    gate = RetrievalRelevanceGate()

    evidence = [
        _make_evidence(
            "Taj Mahal",
        )
    ]

    decision = gate.evaluate(
        "Where is it located?",
        evidence,
    )

    assert decision.allowed is True

def test_explicit_site_entity_can_be_extracted_from_query():
    gate = RetrievalRelevanceGate()

    assert gate._extract_explicit_site_entity(
        "Tell me about the Taj Mahal."
    ) == "taj mahal"


def test_explicit_site_entity_extraction_is_case_insensitive():
    gate = RetrievalRelevanceGate()

    assert gate._extract_explicit_site_entity(
        "Tell me about TAJ MAHAL."
    ) == "taj mahal"


def test_contextual_query_has_no_explicit_site_entity():
    gate = RetrievalRelevanceGate()

    assert gate._extract_explicit_site_entity(
        "Where is it located?"
    ) is None


def test_unrelated_query_has_no_explicit_site_entity():
    gate = RetrievalRelevanceGate()

    assert gate._extract_explicit_site_entity(
        "What is the capital of Brazil?"
    ) is None
