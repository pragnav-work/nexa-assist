import os

SYSTEM_CA = "/etc/ssl/certs/ca-certificates.crt"

os.environ["REQUESTS_CA_BUNDLE"] = SYSTEM_CA
os.environ["SSL_CERT_FILE"] = SYSTEM_CA
os.environ["CURL_CA_BUNDLE"] = SYSTEM_CA

print("Using certificate bundle:", SYSTEM_CA)
from sentence_transformers import SentenceTransformer

from src.rag.config import EMBEDDING_MODEL


class EmbeddingModel:
    '''Generate embeddings for documents and user queries.'''

    def __init__(self):
        # Load the pretrained embedding model once.
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def encode_documents(self, texts):
        '''Convert document chunks into numerical vectors.'''

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

    def encode_query(self, query):
        '''Convert a user query into a numerical vector.'''

        return self.model.encode(
            [query],
            convert_to_numpy=True
        )