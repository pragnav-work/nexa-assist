from src.rag.embeddings import EmbeddingModel


def test_document_embeddings():

    model = EmbeddingModel()

    texts = [
        'Employees can take up to 8 WFH days per month.',
        'Casual leave entitlement is 12 days per year.'
    ]

    embeddings = model.encode_documents(texts)

    # Two input texts should produce two embedding vectors.
    assert embeddings.shape[0] == 2

    # all-MiniLM-L6-v2 produces 384-dimensional embeddings.
    assert embeddings.shape[1] == 384


def test_query_embedding():

    model = EmbeddingModel()

    embedding = model.encode_query(
        'How many WFH days can I take?'
    )

    # A single query should produce one vector.
    assert embedding.shape == (1, 384)