from src.rag.config import TOP_K
from src.rag.embeddings import EmbeddingModel
from src.rag.vector_store import VectorStore


class PolicyRetriever:
    '''Retrieve relevant company policy chunks for a user query.'''

    def __init__(self):
        # Load the embedding model and saved FAISS vector store.
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()

    def load(self):
        '''Load the saved FAISS index and chunk metadata.'''

        self.vector_store.load()

    def retrieve(self, query, top_k=TOP_K):
        '''Retrieve the most relevant policy chunks for a query.'''

        # Convert the user's question into an embedding vector.
        query_embedding = self.embedding_model.encode_query(query)

        # Search FAISS for the most similar policy chunks.
        results = self.vector_store.search(
            query_embedding,
            top_k
        )

        return results