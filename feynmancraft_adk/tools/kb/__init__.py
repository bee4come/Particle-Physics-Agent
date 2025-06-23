"""
Knowledge Base tools for FeynmanCraft ADK.
"""

from .embeddings import (
    get_embedding,
    embed_and_cache,
    cosine_similarity,
    find_similar_texts
)

from .data_loader import (
    load_kb_examples,
    get_kb_data_path,
    validate_kb_data,
    filter_kb_by_topic,
    filter_kb_by_particles,
    get_kb_stats,
)

from .embedding_manager import (
    KBEmbeddingManager,
    embed_and_cache_kb,
    get_kb_manager,
)

from .search import (
    search_local_tikz_examples,
    search_tikz_examples,
    search_tikz_examples_async,
    rank_results,
    filter_results_by_confidence,
)

# Import KB tool classes
try:
    from .local import LocalKBTool
except ImportError:
    LocalKBTool = None

__all__ = [
    # Embedding utilities
    "get_embedding",
    "embed_and_cache",
    "cosine_similarity",
    "find_similar_texts",
    
    # Data loading
    "load_kb_examples",
    "get_kb_data_path",
    "validate_kb_data",
    "filter_kb_by_topic",
    "filter_kb_by_particles",
    "get_kb_stats",
    
    # Embedding management
    "KBEmbeddingManager",
    "embed_and_cache_kb",
    "get_kb_manager",
    
    # Search tools
    "search_local_tikz_examples",
    "search_tikz_examples",
    "search_tikz_examples_async",
    "rank_results",
    "filter_results_by_confidence",
    
    # Tool classes
    "LocalKBTool",
]