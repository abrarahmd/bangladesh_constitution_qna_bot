import chromadb
from tqdm import tqdm
from chromadb.config import Settings
from config import VECTOR_COLLECTION_NAME, VECTOR_STORE_PATH

def get_chroma_db():
    return chromadb.PersistentClient(path=VECTOR_STORE_PATH)

def create_collection(client: chromadb.Client, name: str = VECTOR_COLLECTION_NAME):
    """Returns a collection, creating it if needed."""
    return client.get_or_create_collection(name)

def index_chunks(
    chunks: list[dict],
    embedder,
    collection,
    batch_size: int = 50
) -> None:

    if not chunks:
        raise ValueError("No chunks provided for indexing.")

    for i in tqdm(range(0, len(chunks), batch_size), desc="Indexing chunks"):
        batch = chunks[i:i+batch_size]
        contents = [c["content"] for c in batch]
        metadatas = [{"source": c["source"]} for c in batch]
        embeddings = embedder.encode(contents).tolist()

        try:
            collection.add(
                ids=[f"doc_{i+j}" for j in range(len(batch))],
                documents=contents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        except Exception as e:
            tqdm.write(f"[Error] Failed to add batch starting at index {i}: {e}")
