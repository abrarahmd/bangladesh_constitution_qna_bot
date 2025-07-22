from pdf_parser import extract_text
from chunker import chunk_text
from embedder import get_embedder
from vector_store import get_chroma_db, create_collection, index_chunks
from rag_pipeline import retrieve, build_prompt, generate_answer
import os

PDF_PATH = os.getenv("PDF_PATH", "data/raw_pdfs/bangladesh_constitution.pdf")
EXIT_COMMAND = "exit"

def run_pipeline():
    # Step 1: Parse & chunk
    text = extract_text(PDF_PATH)
    chunks = chunk_text(text)

    # Step 2: Embed & index
    embedder = get_embedder()
    db = get_chroma_db()
    collection = create_collection(db)

    # Index if needed
    should_index = input("Re-index chunks? (y/n): ").lower()
    if should_index == 'y':
        index_chunks(chunks, embedder, collection)

    # Step 3: RAG
    while True:
        query = input(f"\nAsk your question (or '{EXIT_COMMAND}'): ").strip()
        if query.lower() == EXIT_COMMAND:
            print("Goodbye!")
            break

        try:
            context = retrieve(collection, embedder, query)
            prompt = build_prompt(context, query)
            answer = generate_answer(prompt)
            print(f"\nAnswer: {answer}\n")
        except Exception as e:
            print(f"[Error] {e}")
            print(f"[Error] {e}")

def main():
    run_pipeline()

if __name__ == "__main__":
    main()
