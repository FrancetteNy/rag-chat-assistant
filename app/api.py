from fastapi import FastAPI
from pydantic import BaseModel
from app.retrieval import retrieve
from app.generation import generate

app = FastAPI(title="RAG Chat Assistant")


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    chunks = retrieve(request.question)
    answer = generate(request.question, chunks)
    sources = list(set(c["source"] for c in chunks))
    return ChatResponse(answer=answer, sources=sources)