"""
Embedding utilities for KB search and similarity operations.
"""

import google.generativeai as genai
from typing import List, Optional, Dict, Any
import numpy as np
from functools import lru_cache
import hashlib


def _hash_text(text: str) -> str:
    """Create a hash of text for caching purposes."""
    return hashlib.md5(text.encode()).hexdigest()


@lru_cache(maxsize=1000)
def get_embedding(text: str, model_name: str = "models/text-embedding-004") -> List[float]:
    """
    Get embedding for text using Gemini embedding model.
    
    Args:
        text: Text to embed
        model_name: Name of the embedding model to use
        
    Returns:
        List of float values representing the embedding
    """
    try:
        result = genai.embed_content(
            model=model_name,
            content=text,
            task_type="retrieval_query",
        )
        return result['embedding']
    except Exception as e:
        print(f"Error getting embedding: {str(e)}")
        return []


def embed_and_cache(texts: List[str], model_name: str = "models/text-embedding-004") -> Dict[str, List[float]]:
    """
    Get embeddings for multiple texts with caching.
    
    Args:
        texts: List of texts to embed
        model_name: Name of the embedding model to use
        
    Returns:
        Dictionary mapping text to embedding
    """
    embeddings = {}
    for text in texts:
        embedding = get_embedding(text, model_name)
        if embedding:
            embeddings[text] = embedding
    return embeddings


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity score between -1 and 1
    """
    if not vec1 or not vec2:
        return 0.0
        
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)
    
    dot_product = np.dot(vec1_np, vec2_np)
    norm1 = np.linalg.norm(vec1_np)
    norm2 = np.linalg.norm(vec2_np)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
        
    return dot_product / (norm1 * norm2)


def find_similar_texts(
    query: str,
    candidates: List[Dict[str, Any]],
    text_field: str = "description",
    embedding_field: Optional[str] = None,
    top_k: int = 5,
    threshold: float = 0.7
) -> List[Dict[str, Any]]:
    """
    Find similar texts from candidates based on query.
    
    Args:
        query: Query text
        candidates: List of candidate dictionaries
        text_field: Field name containing text to match
        embedding_field: Field name containing pre-computed embeddings (optional)
        top_k: Number of top results to return
        threshold: Minimum similarity threshold
        
    Returns:
        List of similar candidates sorted by similarity
    """
    query_embedding = get_embedding(query)
    if not query_embedding:
        return []
    
    scored_candidates = []
    
    for candidate in candidates:
        # Get candidate embedding
        if embedding_field and embedding_field in candidate:
            candidate_embedding = candidate[embedding_field]
        else:
            text = candidate.get(text_field, "")
            candidate_embedding = get_embedding(text)
            
        if not candidate_embedding:
            continue
            
        # Calculate similarity
        similarity = cosine_similarity(query_embedding, candidate_embedding)
        
        if similarity >= threshold:
            scored_candidates.append({
                **candidate,
                "similarity_score": similarity
            })
    
    # Sort by similarity score
    scored_candidates.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return scored_candidates[:top_k]