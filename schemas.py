"""
Pydantic schemas for API requests/responses
"""
from pydantic import BaseModel
from typing import List, Dict, Optional

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    threshold: float = 0.0

class SearchResult(BaseModel):
    text: str
    similarity: float
    metadata: Dict

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    count: int

class IndexRequest(BaseModel):
    directory_path: str

class IndexResponse(BaseModel):
    indexed: int
    failed: int
    files: List[str]

class StatsResponse(BaseModel):
    total_chunks: int
    collection_name: str
