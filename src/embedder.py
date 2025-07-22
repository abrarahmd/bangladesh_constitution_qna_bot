from sentence_transformers import SentenceTransformer
from typing import Optional
from config import EMBEDDING_MODEL_NAME

def get_embedder(model_name=EMBEDDING_MODEL_NAME):
    return SentenceTransformer(model_name, device="cpu")


def embed_texts(
    model: SentenceTransformer,
    texts: list[str],
    batch_size: int = 32
) -> list[list[float]]:

    return model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True
    ).tolist()
