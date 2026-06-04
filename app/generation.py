import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.1-8b-instant"
def generate(query: str, chunks: list[dict]) -> str:
    """Generate an answer based on retrieved chunks."""
    context = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['content']}" for c in chunks
    )

    system_prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided context.
If the answer is not in the context, say so clearly. Do not make up information.

CONTEXT:
{context}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    from retrieval import retrieve

    query = "How does RAG improve mental health screening?"
    chunks = retrieve(query)
    answer = generate(query, chunks)
    print(f"Question: {query}\n")
    print(f"Answer: {answer}")