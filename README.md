# Semantic Search Engine for Your Docs

A fast, lightweight semantic search engine for indexing and searching your documents using AI embeddings. No API costs, runs entirely locally.

## Features

- 📄 **Multi-format support**: Index markdown, text, and PDF files
- 🔍 **Semantic search**: Find documents by meaning, not just keywords
- 🚀 **Fast & lightweight**: Runs on your machine, no cloud dependencies
- 💾 **Persistent storage**: Indexes are saved locally with Chroma
- 🎯 **Flexible querying**: Search with natural language queries
- 🌐 **API & CLI**: Use via FastAPI web interface or command-line


## How I Built It

- Parsed documents into chunks for better semantic accuracy
- Converted text into embeddings using HuggingFace all-MiniLM-L6-v2
- Stored embeddings in a local Chroma vector database
- Built a CLI using Click to index documents and search easily
- Built a FastAPI server with interactive /docs for API testing
- Added logging, error handling, and persistence for robustness


## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Usage

#### CLI
```bash
# Index documents
python cli.py index ./docs

# Search documents
python cli.py search "your query here"
```

#### API Server
```bash
python main.py
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
.
├── main.py              # FastAPI server
├── cli.py              # CLI interface
├── core/
│   ├── embeddings.py   # Embedding model handling
│   ├── indexer.py      # Document indexing logic
│   └── search.py       # Search functionality
├── models/
│   └── schemas.py      # Pydantic schemas
├── utils/
│   ├── file_handler.py # File parsing
│   └── logger.py       # Logging setup
└── requirements.txt
```

## Stack

- **FastAPI**: Web framework
- **Sentence-Transformers**: Free embeddings from HuggingFace
- **Chroma**: Vector database for embeddings
- **Click**: CLI framework

## Roadmap

- [ ] Web UI (Streamlit)
- [ ] Multi-language support
- [ ] Batch search operations
- [ ] Document metadata filtering
- [ ] Export search results

## License

MIT
