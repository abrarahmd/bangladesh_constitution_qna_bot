import requests
from config import RETRIEVER_TOP_K, GROQ_API_URL, GROQ_API_KEY, LLAMA_MODEL_NAME

QA_PROMPT = """
Context:
{context}

Question: {question}
You are a helpful legal assistant. Answer the question based on the provided context.
If the answer is not in the context, reply: "I could not find the answer in the provided laws or constitution."
"""

def build_prompt(context: str, question: str) -> str:
    return QA_PROMPT.format(context=context, question=question)

def retrieve(collection, embedder, query: str, top_k: int = RETRIEVER_TOP_K) -> str:
    q_emb = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[q_emb], n_results=top_k)
    docs = results.get("documents", [[]])[0]
    if not docs:
        return ""
    return "\n".join(docs)

def generate_answer(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": LLAMA_MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.2
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()