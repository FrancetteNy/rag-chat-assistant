# RAG Chat Assistant

A document-aware chatbot powered by Retrieval-Augmented Generation (RAG). Ask questions about your PDF documents and get accurate, sourced answers — without hallucinations.

---

## How it works

```
PDF documents
      ↓
  Text extraction + chunking
      ↓
  Semantic embeddings (sentence-transformers)
      ↓
  ChromaDB vector store
      ↓
  User question → retrieve top-k chunks → augment prompt → LLM (Groq)
      ↓
  Answer + source citation
```

The system only answers based on the content of your documents. If the answer is not there, it says so.

---

## Tech stack

| Layer | Technology |
|---|---|
| LLM | Groq (Llama 3.1 — OpenAI-compatible API) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector database | ChromaDB |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Containerization | Docker + docker-compose |

---

## Features

- Upload any PDF document and query it instantly
- Semantic search — finds relevant passages even without exact keyword matches
- Source citations — every answer shows which document it came from
- REST API with auto-generated Swagger documentation (`/docs`)
- Fully containerized — runs anywhere with one command

---

## Project structure

```
rag-chat-assistant/
├── app/
│   ├── ingestion.py    # Load PDFs, chunk text, build ChromaDB index
│   ├── retrieval.py    # Semantic search over indexed documents
│   ├── generation.py   # Augmented prompt + LLM call
│   └── api.py          # FastAPI REST endpoint
├── documents/          # Place your PDF files here
├── streamlit_app.py    # Chat interface
├── Dockerfile          # API container
├── Dockerfile.frontend # Streamlit container
├── docker-compose.yml
└── requirements.txt
```

---

## Getting started

### Prerequisites

- Docker + docker-compose
- A [Groq API key](https://console.groq.com) (free)

### Run with Docker

```bash
git clone https://github.com/your-username/rag-chat-assistant.git
cd rag-chat-assistant

cp .env.example .env
# Add your Groq API key to .env

# Place your PDF files in the documents/ folder
# Then index them:
python3 app/ingestion.py

docker-compose up --build
```

Open `http://localhost:8501` and start asking questions.

### Run locally (without Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add your Groq API key

python3 app/ingestion.py
uvicorn app.api:app --reload &
streamlit run streamlit_app.py
```

---

## API

The FastAPI backend exposes a single endpoint:

```
POST /chat
Content-Type: application/json

{ "question": "What is the main contribution of this paper?" }
```

Response:
```json
{
  "answer": "The authors propose an adaptive RAG approach...",
  "sources": ["2025.acl-long.440.pdf"]
}
```

Interactive API documentation available at `http://localhost:8000/docs`.

---

## Roadmap

- [ ] Document upload via the UI (drag & drop)
- [ ] Multi-document support with source filtering
- [ ] Conversational memory (multi-turn chat)
- [ ] Evaluation metrics (faithfulness, relevance)
