from src.rag.config import DOCUMENTS_PATH
from src.rag.document_loader import load_documents
from src.rag.chunker import create_chunks


def test_documents_are_split_into_chunks():

    documents = load_documents(DOCUMENTS_PATH)
    chunks = create_chunks(documents)

    # Four PDFs should produce multiple searchable chunks.
    assert len(chunks) > 4

    # Every chunk should contain the required metadata.
    for chunk in chunks:
        assert chunk['text']
        assert chunk['source']
        assert isinstance(chunk['chunk_id'], int)