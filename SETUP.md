# Getting Started

## Installation

1. **Create virtual environment** (already done):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### CLI Usage

**Index documents:**
```bash
python cli.py index ./your_documents_folder
```

**Search:**
```bash
python cli.py search "your query here"
```

**Search with filter:**
```bash
python cli.py search "query" --filter filename.md
```

**View statistics:**
```bash
python cli.py stats
```

**Clear index:**
```bash
python cli.py clear
```

### API Usage

**Start the server:**
```bash
python main.py
```

Server will be available at `http://localhost:8000`

**Interactive API docs:** http://localhost:8000/docs

**Example requests:**

Index documents:
```bash
curl -X POST "http://localhost:8000/index" \
  -H "Content-Type: application/json" \
  -d '{"directory_path": "./sample_docs"}'
```

Search:
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "your search query", "top_k": 5}'
```

Get stats:
```bash
curl "http://localhost:8000/stats"
```

## How It Works

1. **Document Parsing**: Reads markdown, text, and PDF files
2. **Chunking**: Splits documents into overlapping chunks for better search
3. **Embeddings**: Uses `all-MiniLM-L6-v2` from HuggingFace (lightweight, free)
4. **Vector Storage**: Stores embeddings in Chroma (local vector database)
5. **Semantic Search**: Matches query meaning against document embeddings

## Architecture

```
CLI/API Input
     ↓
Document Parser (utils/file_handler.py)
     ↓
Text Chunker
     ↓
Embeddings Manager (core/embeddings.py)
     ↓
Vector Database (Chroma)
     ↓
Search Engine (core/search.py)
     ↓
Results
```

## Customization

### Change Embedding Model
Edit `core/embeddings.py`:
```python
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # Change this
```

Other lightweight models:
- `all-MiniLM-L6-v2` (current, ~80MB)
- `all-MiniLM-L12-v2` (more accurate, ~120MB)
- `distiluse-base-multilingual-cased-v2` (multilingual)

### Adjust Chunk Size
In `utils/file_handler.py`, modify:
```python
chunk_size: int = 512,  # Characters per chunk
overlap: int = 100      # Overlap between chunks
```

### Change Database Location
In `core/indexer.py` or when initializing:
```python
search_engine = SemanticSearch(db_path="./my_custom_path")
```

## Performance Tips

- **First run**: Model download may take a few minutes (~90MB)
- **Indexing**: Faster on SSD drives
- **Search**: Typically <100ms per query
- **Memory**: ~500MB for embeddings + indices

## Troubleshooting

### SSL Warning
This is harmless. Your system's OpenSSL version doesn't match urllib3's expectations, but everything works fine.

### Out of Memory
Reduce `chunk_size` or process fewer documents at once.

### Slow Indexing
This is normal for the first run. Subsequent searches are fast.

## Next Steps

- Add a web UI with Streamlit
- Support more file formats (DOCX, HTML, etc.)
- Add metadata filtering
- Implement batch processing
- Deploy as a microservice

## License

MIT
