"""
Search module - handles semantic search queries
"""
from typing import List, Dict, Optional
from core.embeddings import embeddings_manager
from core.indexer import DocumentIndexer
from utils.logger import logger

class SemanticSearch:
    def __init__(self, db_path: str = ".db"):
        self.indexer = DocumentIndexer(db_path)
        self.collection = self.indexer.collection
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = 0.0
    ) -> List[Dict]:
        """
        Perform semantic search on indexed documents
        
        Args:
            query: Search query
            top_k: Number of results to return
            threshold: Minimum similarity score (0-1)
        
        Returns:
            List of search results with scores
        """
        # Generate query embedding
        query_embedding = embeddings_manager.embed_single(query)
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        if not results["documents"][0]:
            logger.warning(f"No results found for query: {query}")
            return []
        
        # Format results
        formatted_results = []
        for i, doc in enumerate(results["documents"][0]):
            distance = results["distances"][0][i]
            # Convert distance to similarity (for cosine, similarity = 1 - distance)
            similarity = 1 - distance
            
            if similarity >= threshold:
                formatted_results.append({
                    "text": doc,
                    "similarity": round(similarity, 4),
                    "metadata": results["metadatas"][0][i]
                })
        
        logger.info(f"Found {len(formatted_results)} results for: {query}")
        return formatted_results
    
    def search_with_filter(
        self,
        query: str,
        filename_filter: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """Search with optional filename filtering"""
        results = self.search(query, top_k * 2)  # Get more results before filtering
        
        if filename_filter:
            results = [
                r for r in results
                if filename_filter.lower() in r["metadata"]["filename"].lower()
            ][:top_k]
        
        return results
