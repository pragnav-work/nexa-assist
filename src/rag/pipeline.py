from src.rag.retriever import PolicyRetriever
from src.rag.citation import format_retrieved_context
from google import genai

from src.config.settings import (
    GOOGLE_API_KEY,
    GEMINI_MODEL,
)


class RAGPipeline:
    """High-level interface for retrieving company policy information."""

    def __init__(self):
        # Create the policy retriever.
        self.retriever = PolicyRetriever()

        # Load the saved FAISS index and chunk metadata.
        self.retriever.load()

        # Gemini client
        self.client = genai.Client(api_key=GOOGLE_API_KEY)

    def retrieve(self, query, top_k=3):
        """Retrieve relevant policy chunks for a user query."""

        return self.retriever.retrieve(
            query,
            top_k=top_k
        )

    def retrieve_with_context(self, query, top_k=3):
        """Retrieve policy chunks and format them as grounded context."""

        results = self.retrieve(
            query,
            top_k=top_k
        )

        context = format_retrieved_context(results)

        return {
            "results": results,
            "context": context,
        }

    def answer_query(self, query: str):

        data = self.retrieve_with_context(query)

        context = data["context"]

        prompt = f"""
        You are NexaAssist, an internal HR assistant.

        Answer the user's question ONLY using the policy information below.

        If the answer is not present, say:
        "I couldn't find this information in the company policies."

        Policy Context:
        {context}

        User Question:
        {query}
        """

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

        except Exception as e:
            print("Gemini Exception:", repr(e))
            raise

        return {
            "answer": response.text,
            "citations": data["results"],
        }