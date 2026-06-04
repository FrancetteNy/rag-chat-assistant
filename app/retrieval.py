import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


def get_collection() -> chromadb.Collection:
    """Connect to the existing ChromaDB collection."""
    ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="chroma_db")
    return client.get_collection("documents", embedding_function=ef)


def retrieve(query: str, k: int = 3) -> list[dict]:
    """Find the k most relevant chunks for a given query."""
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=k)

    chunks = []
    for content, metadata in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({
            "content": content,
            "source": metadata["source"]
        })
    return chunks


if __name__ == "__main__":
    query = "How does RAG improve mental health screening?"
    results = retrieve(query)
    for i, chunk in enumerate(results):
        print(f"\n--- Chunk {i+1} (source: {chunk['source']}) ---")
        print(chunk["content"])