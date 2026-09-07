def format_retrieved_context(results):
    '''Format retrieved chunks into context with source citations.'''

    context_parts = []

    for result in results:
        # Include the source so the agent can cite the policy document.
        context_parts.append(
            f"Source: {result['source']}\n"
            f"Chunk: {result['chunk_id']}\n"
            f"Content: {result['text']}"
        )

    return '\n\n'.join(context_parts)