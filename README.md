# DocuQuery — Document Q&A RAG

Upload a PDF, ask questions about it in plain English, and get answers grounded in the document — with page-number citations so you can verify the source.

**Live demo:** [document-qna-rag-app.streamlit.app](https://document-qna-rag-app.streamlit.app)

## How it works

1. **Ingest** — `ingest.py` opens the PDF with PyMuPDF, extracts text page by page, cleans it up, and splits it into ~1000-character chunks (200-character overlap) using LangChain's `RecursiveCharacterTextSplitter`.
2. **Index** — `retriever.py` stores each chunk in a local ChromaDB collection (one collection per uploaded file, persisted to `./my_local_db`), along with its source page number.
3. **Retrieve** — when you ask a question, ChromaDB's built-in embedding search pulls back the top-k most relevant chunks.
4. **Generate** — `generate.py` packs the retrieved chunks into a context block and sends it to Groq (`openai/gpt-oss-120b`) with a system prompt that keeps the model grounded in the document and citing page numbers.
5. **Serve** — `app.py` wraps the whole thing in a one-page Streamlit UI: upload a file, type a question, get an answer.

## Tech stack

- **UI:** Streamlit
- **PDF parsing:** PyMuPDF
- **Chunking:** LangChain text splitters
- **Vector store:** ChromaDB (persistent, local)
- **LLM:** Groq API (`openai/gpt-oss-120b`)

## Running locally

```bash
git clone https://github.com/ateebkhan96/document-qa-rag.git
cd document-qa-rag
pip install -r requirements.txt
```

Add your Groq API key as a Streamlit secret:

```bash
mkdir -p .streamlit
echo 'GROQ_API_KEY = "your-key-here"' > .streamlit/secrets.toml
```

Then run:

```bash
streamlit run app.py
```

Open the local URL Streamlit prints, upload a PDF, and start asking questions.

## Project structure

```
.
├── app.py          # Streamlit UI
├── ingest.py        # PDF parsing + chunking
├── retriever.py     # ChromaDB indexing + retrieval
├── generate.py       # Context assembly + Groq call
└── requirements.txt
```

## Notes

- Each uploaded PDF gets its own ChromaDB collection, so re-uploading the same file skips re-indexing.
- This was built as a from-scratch RAG project to learn the pipeline end to end — chunking strategy, vector storage, and retrieval-augmented generation — rather than relying on a pre-built RAG framework.
