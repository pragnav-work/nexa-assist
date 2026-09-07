from pathlib import Path


# Get the project root directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define project-level paths.
DOCUMENTS_PATH = PROJECT_ROOT / 'data' / 'documents'
VECTORSTORE_PATH = PROJECT_ROOT / 'vectorstore'

# RAG configuration.
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

TOP_K = 3
# DOCUMENTS_PATH
#     Location of the company policy PDFs.

# VECTORSTORE_PATH
#     Location where the generated FAISS index is stored.

# CHUNK_SIZE
#     Maximum approximate size of each searchable text chunk.

# CHUNK_OVERLAP
#     Amount of text shared between neighboring chunks.

# EMBEDDING_MODEL
#     Model used to convert text into numerical vectors.

# TOP_K
#     Number of relevant chunks returned for a query.

