import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.retrieval import retrieve
from app.generation import generate
from app.ingestion import load_pdf, split_into_chunks, build_index

app = FastAPI(title="RAG Chat Assistant")

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "documents")
ALLOWED_EXTENSIONS = {".pdf"}


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


class UploadResponse(BaseModel):
    filename: str
    chunks_indexed: int
    message: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    chunks = retrieve(request.question)
    answer = generate(request.question, chunks)
    sources = list(set(c["source"] for c in chunks))
    return ChatResponse(answer=answer, sources=sources)


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}")

    os.makedirs(DOCS_DIR, exist_ok=True)
    dest_path = os.path.join(DOCS_DIR, file.filename)

    with open(dest_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = load_pdf(dest_path)
    chunks = split_into_chunks(text)
    build_index(chunks, source=file.filename)

    return UploadResponse(
        filename=file.filename,
        chunks_indexed=len(chunks),
        message=f"'{file.filename}' successfully indexed ({len(chunks)} chunks)."
    )