
from pathlib import Path
import json

import faiss
import numpy as np

from embedding_service import generate_embedding
from app import ask_bedrock


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
INDEX_PATH = DATA_DIR / "resume.index"
CHUNKS_PATH = DATA_DIR / "resume_chunks.json"


def retrieve_relevant_chunks(question, top_k=3):

    # Load FAISS index
    vector_index = faiss.read_index(str(INDEX_PATH))

    # Load original text chunks
    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    # Generate question embedding
    question_embedding = generate_embedding(question)

    query_vector = np.array(
        [question_embedding],
        dtype=np.float32
    )

    # Search for relevant chunks
    scores, indices = vector_index.search(
        query_vector,
        min(top_k, len(chunks))
    )

    retrieved_chunks = []

    for score, chunk_index in zip(scores[0], indices[0]):

        if chunk_index != -1:
            retrieved_chunks.append({
                "text": chunks[chunk_index],
                "score": float(score)
            })

    return retrieved_chunks



def answer_question(question):

    # Step 1: Retrieve relevant resume information
    retrieved_chunks = retrieve_relevant_chunks(question)

    if not retrieved_chunks:
        print("No relevant resume information found.")
        return

    # Step 2: Display retrieved source information
    print("\nRETRIEVED SOURCES:\n")

    for index, item in enumerate(retrieved_chunks, start=1):

        print("=" * 60)
        print("Source:", index)
        print("Similarity score:", round(item["score"], 4))
        print("Retrieved text:")
        print(item["text"])
        print()

    # Step 3: Build context from retrieved chunks
    context = "\n\n".join(
        item["text"] for item in retrieved_chunks
    )

    # Step 4: Build RAG prompt
    prompt = f"""
    You are a professional technical recruitment assistant.

    Answer the user's question using ONLY the resume context below.

    Rules:
    1. Do not invent experience or skills.
    2. Distinguish explicit resume evidence from interpretation.
    3. If the context does not contain the answer, say
       "The resume does not provide enough evidence to answer this."
    4. Explain your answer clearly.
    5. Mention relevant projects and technologies where available.

    RESUME CONTEXT:
    {context}

    USER QUESTION:
    {question}
    """

    # Step 5: Generate answer
    print("\nGenerating answer using retrieved resume context...\n")

    answer = ask_bedrock(prompt)

    if answer:
        print("\nANSWER:\n")
        print(answer)

if __name__ == "__main__":

    while True:

        question = input(
            "\nAsk a question about your resume (or type EXIT): "
        )

        if question.strip().upper() == "EXIT":
            break

        if not question.strip():
            continue

        answer_question(question)
