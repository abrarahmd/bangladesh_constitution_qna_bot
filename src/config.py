from dotenv import load_dotenv
import os

load_dotenv()

CHUNK_SIZE = 2000
CHUNK_OVERLAP = 300
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
VECTOR_COLLECTION_NAME = "constitution"
RETRIEVER_TOP_K = 10
VECTOR_STORE_PATH = "./data/vector_store"

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA_MODEL_NAME = "llama3-8b-8192"