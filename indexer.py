"""
Indexer module - handles document parsing and indexing
"""
import os
import chromadb
from pathlib import Path
from typing import List, Dict, Optional
from utils.file_handler import parse_document
from core.embeddings import embeddings_manager
from utils.logger import logger

class DocumentIndexer:
    def __init__(self, db_path: str = ".db"):
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)
        
        # Initialize Chroma persistent client
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def index_directory(self, directory_path: str, extensions: Optional[List[str]] = None) -> Dict:
        """Index all documents in a directory"""
        if extensions is None:
            extensions = [".md", ".txt", ".pdf"]
        
        directory_path = Path(directory_path)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        results = {
            "indexed": 0,
            "failed": 0,
            "files": []
        }
        
        # Recursively find all matching files
        for file_path in directory_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                try:
                    self.index_file(str(file_path))
                    results["indexed"] += 1
                    results["files"].append(str(file_path))
                    logger.info(f"Indexed: {file_path}")
                except Exception as e:
                    results["failed"] += 1
                    logger.error(f"Failed to index {file_path}: {e}")
        
        return results
    
    def index_file(self, file_path: str) -> None:
        """Index a single file"""
        file_path = Path(file_path)
        
        # Parse document
        chunks = parse_document(str(file_path))
        
        if not chunks:
            logger.warning(f"No content extracted from {file_path}")
            return
        
        # Generate embeddings
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embeddings_manager.embed(texts)
        
        # Prepare data for Chroma
        ids = [
            f"{file_path.name}_{i}" 
            for i in range(len(chunks))
        ]
        
        metadatas = [
            {
                "file": str(file_path),
                "filename": file_path.name,
                "chunk_index": i,
                "file_type": file_path.suffix
            }
            for i in range(len(chunks))
        ]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        logger.info(f"Successfully indexed {len(chunks)} chunks from {file_path}")
    
    def clear_index(self) -> None:
        """Clear all indexed documents"""
        self.client.delete_collection(name="documents")
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Index cleared")
    
    def get_stats(self) -> Dict:
        """Get indexing statistics"""
        count = self.collection.count()
        return {
            "total_chunks": count,
            "collection_name": "documents"
        }
