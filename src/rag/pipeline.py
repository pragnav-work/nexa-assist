from src.rag.retriever import PolicyRetriever
from src.rag.citation import format_retrieved_context


class RAGPipeline:
    '''High-level interface for retrieving company policy information.'''

    def __init__(self):
        # Create the policy retriever.
        self.retriever = PolicyRetriever()

        # Load the saved FAISS index and chunk metadata.
        self.retriever.load()

    def retrieve(self, query, top_k=3):
        '''Retrieve relevant policy chunks for a user query.'''

        return self.retriever.retrieve(
            query,
            top_k=top_k
        )

    def retrieve_with_context(self, query, top_k=3):
        '''Retrieve policy chunks and format them as grounded context.'''

        results = self.retrieve(
            query,
            top_k=top_k
        )

        context = format_retrieved_context(results)

        return {
            'results': results,
            'context': context
        }