from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingService:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def generate_chunks_embedding(self, text: str, chunk_max_words: int = 150, chunk_overlap_words: int = 30) -> List[tuple]:
        """Split text into chunks using sentence-aware boundary matching and generate embeddings."""
        import re
        # Split by sentences (very basic split on period, question mark, exclamation mark)
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        
        chunks = []
        current_chunk_words = []
        current_word_count = 0
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            sentence_words = sentence.split()
            sentence_word_count = len(sentence_words)
            
            # If adding this sentence exceeds the max chunk size (and the chunk is not empty)
            if current_word_count + sentence_word_count > chunk_max_words and current_chunk_words:
                chunks.append(' '.join(current_chunk_words))
                # Keep the overlap: take the last `chunk_overlap_words` words from current chunk
                overlap_words = current_chunk_words[-chunk_overlap_words:] if chunk_overlap_words > 0 else []
                current_chunk_words = overlap_words + sentence_words
                current_word_count = len(current_chunk_words)
            else:
                current_chunk_words.extend(sentence_words)
                current_word_count += sentence_word_count
                
        # Add the final chunk if not empty
        if current_chunk_words:
            chunks.append(' '.join(current_chunk_words))
            
        if not chunks:
            return []
            
        embeddings = self.generate_embeddings(chunks)
        
        return list(zip(chunks, embeddings))


# Global embedding service instance
_embedding_service = None


def get_embedding_service():
    global _embedding_service
    if _embedding_service is None:
        from app.config import settings
        _embedding_service = EmbeddingService(settings.embedding_model)
    return _embedding_service
