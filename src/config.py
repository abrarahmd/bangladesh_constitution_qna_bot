import os
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Project & Environment Setup
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / '.env')

# === Paths ===
DATA_DIR = PROJECT_ROOT / 'data'
MARKDOWN_PATH = DATA_DIR / 'pdf_markdown' / 'constitution.md'
PERSIST_DIRECTORY = str(PROJECT_ROOT / 'chroma_db')  # Chroma DB persistence

# RAG Configuration
CHUNK_SIZE = 1000                  # Max tokens per chunk
CHUNK_OVERLAP = 200                # Overlap between chunks
RETRIEVER_TOP_K = 3                # Number of top documents to retrieve
VECTOR_COLLECTION_NAME = "constitution"
VECTOR_STORE_PATH = str(PROJECT_ROOT / 'data' / 'vector_store')


# Embedding Model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# LLM API Configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

LLAMA_MODEL_NAME = "llama3-8b-8192"



DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Debug Prints
print(f"MARKDOWN_PATH → {MARKDOWN_PATH}")
print(f"Using Embedder → {EMBEDDING_MODEL_NAME}")
print(f"Using LLM Model → {LLAMA_MODEL_NAME}")
if DEBUG:
    print(f"PERSIST_DIRECTORY → {PERSIST_DIRECTORY}")

__all__ = [
    "MARKDOWN_PATH",
    "PERSIST_DIRECTORY",
    "CHUNK_SIZE",
    "CHUNK_OVERLAP",
    "RETRIEVER_TOP_K",
    "VECTOR_COLLECTION_NAME",
    "EMBEDDING_MODEL_NAME",
    "GROQ_API_URL",
    "GROQ_API_KEY",
    "LLAMA_MODEL_NAME",
    "SECRET_KEY",
    "DEBUG"
]