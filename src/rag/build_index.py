import os

# SSL certificate configuration:
# Uses the Linux system's trusted CA certificates for HTTPS connections.
# This is required in our corporate network because the default Python
# certificate bundle does not trust the network's certificate chain.
os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/ca-certificates.crt'
os.environ['SSL_CERT_FILE'] = '/etc/ssl/certs/ca-certificates.crt'

from src.rag.config import DOCUMENTS_PATH
from src.rag.document_loader import load_documents
from src.rag.chunker import create_chunks
from src.rag.embeddings import EmbeddingModel
from src.rag.vector_store import VectorStore


def build_policy_index():
    '''Build and save the FAISS index for company policies.'''

    documents = load_documents(DOCUMENTS_PATH)

    print(f'Loaded documents: {len(documents)}')

    chunks = create_chunks(documents)

    print(f'Created chunks: {len(chunks)}')

    embedding_model = EmbeddingModel()

    embeddings = embedding_model.encode_documents(
        [chunk['text'] for chunk in chunks]
    )

    print(f'Embedding shape: {embeddings.shape}')

    vector_store = VectorStore()

    vector_store.build(
        embeddings,
        chunks
    )

    vector_store.save()

    print('FAISS index created successfully.')


if __name__ == '__main__':
    build_policy_index()