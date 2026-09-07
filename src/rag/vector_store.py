from pathlib import Path
import pickle

import faiss

from src.rag.config import VECTORSTORE_PATH


class VectorStore:
    '''Store and search document embeddings using FAISS.'''

    def __init__(self):
        self.index = None
        self.chunks = []

    def build(self, embeddings, chunks):
        '''Create a FAISS index from document embeddings.'''

        # Get the number of dimensions in each embedding vector.
        dimension = embeddings.shape[1]

        # IndexFlatL2 uses Euclidean distance for similarity search.
        self.index = faiss.IndexFlatL2(dimension)

        # FAISS expects float32 vectors.
        self.index.add(embeddings.astype('float32'))

        # Keep the original chunks so search results can be mapped back to text.
        self.chunks = chunks

    def save(self):
        '''Save the FAISS index and chunk metadata.'''

        path = Path(VECTORSTORE_PATH)
        path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(
            self.index,
            str(path / 'policy.index')
        )

        with open(path / 'chunks.pkl', 'wb') as file:
            pickle.dump(self.chunks, file)

    def load(self):
        '''Load the FAISS index and chunk metadata.'''

        path = Path(VECTORSTORE_PATH)

        self.index = faiss.read_index(
            str(path / 'policy.index')
        )

        with open(path / 'chunks.pkl', 'rb') as file:
            self.chunks = pickle.load(file)

    def search(self, query_embedding, top_k):
        '''Search for the most similar document chunks.'''

        distances, indices = self.index.search(
            query_embedding.astype('float32'),
            top_k
        )

        results = []

        for distance, index in zip(distances[0], indices[0]):

            if index != -1:
                results.append({
                    'text': self.chunks[index]['text'],
                    'source': self.chunks[index]['source'],
                    'chunk_id': self.chunks[index]['chunk_id'],
                    'distance': float(distance)
                })

        return results