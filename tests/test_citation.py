from src.rag.citation import format_retrieved_context


def test_format_retrieved_context():

    # Create sample retrieval results.
    results = [
        {
            'text': 'Employees may take up to 8 WFH days per calendar month.',
            'source': 'wfh_policy.pdf',
            'chunk_id': 0,
            'distance': 0.25
        },
        {
            'text': 'WFH requests should be submitted in advance.',
            'source': 'wfh_policy.pdf',
            'chunk_id': 1,
            'distance': 0.31
        }
    ]

    # Format the retrieved results into agent-ready context.
    context = format_retrieved_context(results)

    assert 'wfh_policy.pdf' in context
    assert 'Employees may take up to 8 WFH days' in context
    assert 'Chunk: 0' in context
    assert 'Chunk: 1' in context