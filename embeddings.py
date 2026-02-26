"""
Embeddings module - handles model loading and embedding generation
"""
from sentence_transformers import SentenceTransformer
from typing import List
import os

# Use a lightweight, free model from HuggingFace
MODEL_NAME = "all-MiniLM-L6-v2"
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", ".models")

class EmbeddingsManager:
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._model is None:
            print(f"Loading embedding model: {MODEL_NAME}...")
            # Models will be cached locally
            os.makedirs(MODELS_DIR, exist_ok=True)
            self._model = SentenceTransformer(
                MODEL_NAME,
                cache_folder=MODELS_DIR
            )
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        if isinstance(texts, str):
            texts = [texts]
        return self._model.encode(texts, convert_to_numpy=True).tolist()
    
    def embed_single(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        return self.embed([text])[0]

# Singleton instance
embeddings_manager = EmbeddingsManager()
