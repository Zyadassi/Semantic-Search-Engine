"""
File handler - parse different document formats
"""
from pathlib import Path
from typing import List, Dict
import re

def parse_document(file_path: str, chunk_size: int = 512, overlap: int = 100) -> List[Dict]:
    """
    Parse a document and split into chunks
    
    Args:
        file_path: Path to document
        chunk_size: Approximate chunk size in characters
        overlap: Character overlap between chunks
    
    Returns:
        List of chunks with metadata
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Read file based on extension
    if file_path.suffix.lower() == ".pdf":
        content = _parse_pdf(str(file_path))
    elif file_path.suffix.lower() in [".md", ".txt"]:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    # Split into chunks
    chunks = _chunk_text(content, chunk_size, overlap)
    
    return [{"text": chunk, "file": str(file_path)} for chunk in chunks]

def _parse_pdf(file_path: str) -> str:
    """Parse PDF files"""
    try:
        import PyPDF2 # pyright: ignore[reportMissingImports]
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text
    except ImportError:
        raise ImportError("PyPDF2 not installed. For PDF support, run: pip install PyPDF2")

def _chunk_text(text: str, chunk_size: int = 512, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks"""
    # Clean up text
    text = re.sub(r'\s+', ' ', text).strip()
    
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            last_period = text.rfind('.', start, end)
            if last_period > start + chunk_size // 2:
                end = last_period + 1
        
        chunks.append(text[start:end])
        start = end - overlap
    
    return [chunk.strip() for chunk in chunks if chunk.strip()]
