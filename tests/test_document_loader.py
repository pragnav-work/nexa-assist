from src.rag.document_loader import load_documents


def test_documents_are_loaded():

    documents = load_documents('data/documents')

    assert len(documents) == 4

    sources = {
        document['source']
        for document in documents
    }

    assert 'leave_policy.pdf' in sources
    assert 'wfh_policy.pdf' in sources
    assert 'travel_policy.pdf' in sources
    assert 'reimbursement_policy.pdf' in sources