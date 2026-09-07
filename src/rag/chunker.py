from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.config import CHUNK_SIZE, CHUNK_OVERLAP


def create_chunks(documents):
    '''Split policy documents into smaller overlapping chunks.'''

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=['\n\n', '\n', '. ', ' ', '']
    )

    chunks = []

    for document in documents:

        # Split the document text while keeping its source information.
        split_texts = splitter.split_text(document['text'])

        for chunk_id, text in enumerate(split_texts):

            chunks.append({
                'text': text,
                'source': document['source'],
                'chunk_id': chunk_id
            })

    return chunks