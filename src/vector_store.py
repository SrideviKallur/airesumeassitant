
from pathlib import Path
import json

import faiss
import numpy as np

from text_chunker import split_text_into_chunks
from resume_parser import extract_resume_text
from embedding_service import generate_embedding


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESUME_PATH = PROJECT_ROOT / "resume.pdf"

DATA_DIR = PROJECT_ROOT / "data"
INDEX_PATH = DATA_DIR / "resume.index"
CHUNKS_PATH = DATA_DIR / "resume_chunks.json"

EMBEDDING_DIMENSION = 1024


def build_vector_store():

    # Step 1: Extract resume text
    print("\nExtracting resume text...")

    resume_text = extract_resume_text(RESUME_PATH)

    # Step 2: Split resume into chunks
    chunks = split_text_into_chunks(
        resume_text,
        chunk_size=100,
        overlap=20
    )

    print("Total chunks:", len(chunks))

    if not chunks:
        print("No resume chunks found.")
        return

    # Step 3: Generate embeddings for every chunk
    embeddings = []

    for index, chunk in enumerate(chunks, start=1):

        print("Generating embedding for chunk", index)

        embedding = generate_embedding(chunk)

        embeddings.append(embedding)

    # Step 4: Convert embeddings into NumPy float32 array
    embedding_matrix = np.array(
        embeddings,
        dtype=np.float32
    )

    # Step 5: Create FAISS index
    vector_index = faiss.IndexFlatIP(
        EMBEDDING_DIMENSION
    )

    # Step 6: Add embeddings to FAISS
    vector_index.add(embedding_matrix)

    # Step 7: Create data directory
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Step 8: Save FAISS index
    faiss.write_index(
        vector_index,
        str(INDEX_PATH)
    )

    # Step 9: Save original text chunks
    with open(CHUNKS_PATH, "w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=4)

    print("\nVector store created successfully!")
    print("Total vectors:", vector_index.ntotal)
    print("Embedding dimensions:", EMBEDDING_DIMENSION)
    print("Index saved at:", INDEX_PATH)
    print("Chunks saved at:", CHUNKS_PATH)


def search_similar_chunks(question, top_k=3):

    # Step 1: Load FAISS index
    vector_index = faiss.read_index(
        str(INDEX_PATH)
    )

    # Step 2: Load original text chunks
    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    # Step 3: Generate embedding for the question
    question_embedding = generate_embedding(question)

    # Step 4: Convert query embedding to NumPy array
    query_vector = np.array(
        [question_embedding],
        dtype=np.float32
    )

    # Step 5: Search FAISS
    scores, indices = vector_index.search(
        query_vector,
        min(top_k, len(chunks))
    )

    print("\nMost relevant resume chunks:\n")

    # Step 6: Display matching chunks
    for score, chunk_index in zip(scores[0], indices[0]):

        if chunk_index == -1:
            continue

        print("=" * 60)
        print("Similarity score:", float(score))
        print("Chunk number:", int(chunk_index) + 1)
        print("=" * 60)
        print(chunks[chunk_index])
        print()


if __name__ == "__main__":

    build_vector_store()

    search_question = "What experience does the candidate have with Kafka?"

    search_similar_chunks(search_question, top_k=3)
