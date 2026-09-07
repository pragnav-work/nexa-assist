from src.rag.pipeline import RAGPipeline

rag = RAGPipeline()

result = rag.answer_query(
    "How many WFH days can I take?"
)

print(result["answer"])