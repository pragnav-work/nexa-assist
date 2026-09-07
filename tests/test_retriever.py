from src.rag.retriever import PolicyRetriever


def test_policy_retriever():

    retriever = PolicyRetriever()
    retriever.load()

    results = retriever.retrieve(
        'How many WFH days can I take per month?'
    )

    assert len(results) == 3

    # The retrieved chunks should contain actual policy text.
    assert all(result['text'] for result in results)

    # Every result should retain its source document.
    assert all(result['source'] for result in results)

    # WFH policy should be among the top retrieved sources.
    assert any(
        'wfh' in result['source'].lower()
        for result in results
    )