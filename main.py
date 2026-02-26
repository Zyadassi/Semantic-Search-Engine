"""
FastAPI server for semantic search
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List

from models.schemas import (
    SearchRequest, SearchResponse, SearchResult,
    IndexRequest, IndexResponse, StatsResponse
)
from core.search import SemanticSearch
from core.indexer import DocumentIndexer
from utils.logger import logger

# Global search instance
search_engine: SemanticSearch = None
indexer: DocumentIndexer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global search_engine, indexer
    logger.info("Initializing search engine...")
    search_engine = SemanticSearch()
    indexer = search_engine.indexer
    logger.info("Search engine ready!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Semantic Search Engine",
    description="Search your documents using AI embeddings",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Semantic Search Engine API",
        "docs": "/docs",
        "health": "ok"
    }

@app.post("/search", response_model=SearchResponse, tags=["Search"])
async def search(request: SearchRequest):
    """Search indexed documents using semantic similarity"""
    if not search_engine:
        raise HTTPException(status_code=503, detail="Search engine not initialized")
    
    results = search_engine.search(
        query=request.query,
        top_k=request.top_k,
        threshold=request.threshold
    )
    
    search_results = [
        SearchResult(
            text=r["text"],
            similarity=r["similarity"],
            metadata=r["metadata"]
        )
        for r in results
    ]
    
    return SearchResponse(
        query=request.query,
        results=search_results,
        count=len(search_results)
    )

@app.post("/index", response_model=IndexResponse, tags=["Indexing"])
async def index(request: IndexRequest):
    """Index all documents in a directory"""
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    try:
        results = indexer.index_directory(request.directory_path)
        return IndexResponse(**results)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=StatsResponse, tags=["Stats"])
async def stats():
    """Get indexing statistics"""
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    stats_data = indexer.get_stats()
    return StatsResponse(**stats_data)

@app.delete("/clear", tags=["Indexing"])
async def clear_index():
    """Clear all indexed documents"""
    if not indexer:
        raise HTTPException(status_code=503, detail="Indexer not initialized")
    
    indexer.clear_index()
    return {"message": "Index cleared successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
