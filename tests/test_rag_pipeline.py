from src.rag.pipeline import RAGPipeline


def test_rag_pipeline():

    # Initialize the complete RAG retrieval pipeline.
    rag = RAGPipeline()

    # Retrieve evidence for a policy question.
    results = rag.retrieve(
        'How many WFH days can I take per month?'
    )

    assert len(results) == 3
    assert all(result['text'] for result in results)
    assert all(result['source'] for result in results)

    # The WFH policy should be among the retrieved sources.
    assert any(
        'wfh' in result['source'].lower()
        for result in results
    )