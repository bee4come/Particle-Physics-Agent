"""
KB search tools for TikZ examples.
"""

import asyncio
from typing import List, Dict, Any, Optional
import logging

from .embedding_manager import get_kb_manager
from .embeddings import get_embedding, cosine_similarity

logger = logging.getLogger(__name__)


async def search_local_tikz_examples(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Perform semantic search for TikZ examples in local KB.
    
    Args:
        query: Natural language query about the Feynman diagram
        top_k: Number of top results to return
        
    Returns:
        List of relevant TikZ examples sorted by similarity
    """
    try:
        # Get KB manager and ensure it's initialized
        manager = get_kb_manager()
        await manager.initialize()
        
        if not manager.kb_examples or not manager.embeddings_cache:
            return [{"error": "KB examples or embeddings are not available."}]
        
        # Get query embedding
        query_embedding = await asyncio.to_thread(
            get_embedding, 
            query, 
            manager.model_name
        )
        
        if not query_embedding:
            return [{"error": "Failed to get query embedding"}]
        
        # Calculate similarities
        similarities = []
        for i, example in enumerate(manager.kb_examples):
            if i in manager.embeddings_cache:
                example_embedding = manager.embeddings_cache[i]
                similarity = cosine_similarity(query_embedding, example_embedding)
                similarities.append((similarity, i, example))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for similarity, idx, example in similarities[:top_k]:
            result = example.copy()
            result["similarity_score"] = similarity
            result["source_type"] = "local"
            results.append(result)
            
        logger.info(f"Found {len(results)} local KB results for query: {query[:50]}...")
        return results
        
    except Exception as e:
        logger.error(f"Error in local TikZ search: {e}")
        return [{"error": f"Search failed: {str(e)}"}]


def search_tikz_examples(query: str, use_bigquery: bool = False, k: int = 5) -> List[Dict[str, Any]]:
    """
    Search interface for TikZ examples using local KB only.
    
    Args:
        query: Natural language query about the Feynman diagram
        use_bigquery: Deprecated parameter, ignored (BigQuery removed)
        k: Number of results to return
        
    Returns:
        List of relevant TikZ examples from local KB
    """
    results = []
    
    # Use local search only
    try:
        from . import LocalKBTool
        
        logger.info("Using local KB search...")
        local_tool = LocalKBTool()
        
        # Try hybrid search first
        results = local_tool.hybrid_search(query, k=k)
        
        if results:
            logger.info(f"Found {len(results)} results from local KB tool")
            # Add source type
            for result in results:
                result["source_type"] = "local"
            return results
        else:
            logger.warning("No results found in local KB tool, trying semantic search...")
            
    except Exception as e:
        logger.error(f"Local KB tool search failed: {e}")
    
    # Try our own local semantic search as fallback
    try:
        import asyncio
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create a new task
            task = asyncio.create_task(search_local_tikz_examples(query, k))
            # Note: This won't work well in practice, consider making this function async
            logger.warning("Cannot run async search in sync context")
            return []
        else:
            results = loop.run_until_complete(search_local_tikz_examples(query, k))
            if results and not (len(results) == 1 and "error" in results[0]):
                return results
    except Exception as e:
        logger.error(f"Fallback semantic search failed: {e}")
    
    # If all searches fail, return empty list
    logger.error("All search methods failed")
    return []


async def search_tikz_examples_async(query: str, use_bigquery: bool = False, k: int = 5) -> List[Dict[str, Any]]:
    """
    Async search interface for TikZ examples using local KB only.
    
    Args:
        query: Natural language query about the Feynman diagram
        use_bigquery: Deprecated parameter, ignored (BigQuery removed)
        k: Number of results to return
        
    Returns:
        List of relevant TikZ examples from local KB
    """
    results = []
    
    # Use local search only
    try:
        from . import LocalKBTool
        
        logger.info("Using local KB search...")
        
        def local_kb_search():
            local_tool = LocalKBTool()
            return local_tool.hybrid_search(query, k=k)
        
        results = await asyncio.to_thread(local_kb_search)
        
        if results:
            logger.info(f"Found {len(results)} results from local KB tool")
            # Add source type
            for result in results:
                result["source_type"] = "local"
            return results
        else:
            logger.warning("No results found in local KB tool, trying semantic search...")
            
    except Exception as e:
        logger.error(f"Local KB tool search failed: {e}")
    
    # Try our own local semantic search as fallback
    try:
        results = await search_local_tikz_examples(query, k)
        if results and not (len(results) == 1 and "error" in results[0]):
            return results
    except Exception as e:
        logger.error(f"Fallback semantic search failed: {e}")
    
    # If all searches fail, return empty list
    logger.error("All search methods failed")
    return []


def rank_results(results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Re-rank search results based on additional criteria.
    
    Args:
        results: List of search results
        query: Original query
        
    Returns:
        Re-ranked results
    """
    query_lower = query.lower()
    
    for result in results:
        score = result.get("similarity_score", 0.0)
        
        # Boost results with exact topic matches
        topic = result.get("topic", "").lower()
        if query_lower in topic:
            score += 0.1
            
        # Boost results with particle name matches
        particles = result.get("particles", [])
        for particle in particles:
            if particle.lower() in query_lower:
                score += 0.05
                
        # Boost results with reaction matches
        reaction = result.get("reaction", "").lower()
        if any(word in reaction for word in query_lower.split()):
            score += 0.05
            
        result["final_score"] = score
    
    # Sort by final score
    results.sort(key=lambda x: x.get("final_score", 0), reverse=True)
    return results


def filter_results_by_confidence(results: List[Dict[str, Any]], min_confidence: float = 0.5) -> List[Dict[str, Any]]:
    """
    Filter results by minimum confidence/similarity score.
    
    Args:
        results: List of search results
        min_confidence: Minimum confidence threshold
        
    Returns:
        Filtered results
    """
    return [
        result for result in results
        if result.get("similarity_score", 0) >= min_confidence or
           result.get("final_score", 0) >= min_confidence
    ]