"""Local knowledge base tool with vector search using Annoy index."""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from annoy import AnnoyIndex
import google.generativeai as genai
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Configuration
EMB_DIM = 768  # Dimension for text-embedding-004
DEFAULT_EMBEDDING_MODEL = "text-embedding-004"
KB_JSON_PATH = Path(__file__).parent.parent / "data" / "feynman_kb.json"
ANN_INDEX_PATH = Path(__file__).parent.parent / "data" / "feynman_kb.ann"
ID_MAPPING_PATH = Path(__file__).parent.parent / "data" / "feynman_kb_id_map.json"

# Global cache
_kb_data_cache: Optional[List[Dict[str, Any]]] = None
_annoy_index_cache: Optional[AnnoyIndex] = None
_id_map_cache: Optional[List[str]] = None
_embeddings_cache: Optional[Dict[str, List[float]]] = None


class LocalKBTool:
    """Local knowledge base tool with vector search capabilities."""
    
    def __init__(self):
        """Initialize the local KB tool."""
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self._load_kb_data()
    
    def _load_kb_data(self):
        """Load knowledge base data from JSON file."""
        global _kb_data_cache
        
        if _kb_data_cache is not None:
            return
        
        try:
            with open(KB_JSON_PATH, 'r', encoding='utf-8') as f:
                _kb_data_cache = json.load(f)
            logger.info(f"Loaded {len(_kb_data_cache)} records from {KB_JSON_PATH}")
        except Exception as e:
            logger.error(f"Failed to load KB data: {e}")
            _kb_data_cache = []
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text using Gemini API."""
        if not self.api_key:
            logger.warning("No API key available for embeddings")
            return None
        
        try:
            model_name = f"models/{DEFAULT_EMBEDDING_MODEL}"
            response = genai.embed_content(
                model=model_name,
                content=text,
                task_type="RETRIEVAL_DOCUMENT"
            )
            
            embedding = response.get("embedding")
            if embedding and len(embedding) == EMB_DIM:
                return embedding
            else:
                logger.warning(f"Unexpected embedding dimension: {len(embedding) if embedding else 0}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return None
    
    def build_index(self, force_rebuild: bool = False):
        """Build Annoy index for vector search."""
        global _annoy_index_cache, _id_map_cache, _embeddings_cache
        
        if not force_rebuild and ANN_INDEX_PATH.exists() and ID_MAPPING_PATH.exists():
            logger.info("Index already exists. Use force_rebuild=True to rebuild.")
            return
        
        if not _kb_data_cache:
            logger.error("No KB data loaded")
            return
        
        logger.info("Building Annoy index...")
        
        # Create index
        index = AnnoyIndex(EMB_DIM, 'angular')
        id_map = []
        embeddings = {}
        
        for i, record in enumerate(_kb_data_cache):
            # Generate text for embedding
            text = f"{record.get('topic', '')}: {record.get('description', '')} {record.get('reaction', '')}"
            
            # Get embedding
            embedding = self.get_embedding(text)
            if embedding:
                index.add_item(i, embedding)
                reaction_id = record.get('reaction', f'item_{i}')
                id_map.append(reaction_id)
                embeddings[reaction_id] = embedding
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(_kb_data_cache)} records")
        
        # Build and save index
        logger.info("Building index tree...")
        index.build(10)  # 10 trees
        
        # Save index and mappings
        index.save(str(ANN_INDEX_PATH))
        
        with open(ID_MAPPING_PATH, 'w') as f:
            json.dump(id_map, f)
        
        # Cache results
        _annoy_index_cache = index
        _id_map_cache = id_map
        _embeddings_cache = embeddings
        
        logger.info(f"Index built and saved. Indexed {len(id_map)} items.")
    
    def _load_index(self) -> Tuple[Optional[AnnoyIndex], Optional[List[str]]]:
        """Load Annoy index and ID mapping."""
        global _annoy_index_cache, _id_map_cache
        
        if _annoy_index_cache is not None and _id_map_cache is not None:
            return _annoy_index_cache, _id_map_cache
        
        if not ANN_INDEX_PATH.exists() or not ID_MAPPING_PATH.exists():
            logger.warning("Index not found. Building it now...")
            self.build_index()
            return _annoy_index_cache, _id_map_cache
        
        try:
            # Load index
            index = AnnoyIndex(EMB_DIM, 'angular')
            index.load(str(ANN_INDEX_PATH))
            _annoy_index_cache = index
            
            # Load ID mapping
            with open(ID_MAPPING_PATH, 'r') as f:
                _id_map_cache = json.load(f)
            
            return _annoy_index_cache, _id_map_cache
            
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            return None, None
    
    def vector_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Perform vector similarity search."""
        index, id_map = self._load_index()
        if not index or not id_map:
            return []
        
        # Get query embedding
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            logger.warning("Could not generate query embedding")
            return []
        
        try:
            # Search
            indices, distances = index.get_nns_by_vector(
                query_embedding, k, include_distances=True
            )
            
            # Get results
            results = []
            for idx, dist in zip(indices, distances):
                reaction_id = id_map[idx]
                
                # Find the record
                for record in _kb_data_cache:
                    if record.get('reaction') == reaction_id:
                        result = record.copy()
                        result['similarity_score'] = 1 - dist  # Convert distance to similarity
                        results.append(result)
                        break
            
            return results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
    
    def keyword_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Perform simple keyword search as fallback."""
        if not _kb_data_cache:
            return []
        
        query_lower = query.lower()
        results = []
        
        for record in _kb_data_cache:
            score = 0
            
            # Check different fields
            if query_lower in record.get('reaction', '').lower():
                score += 3
            if query_lower in record.get('topic', '').lower():
                score += 2
            if query_lower in record.get('description', '').lower():
                score += 1
            
            # Check particles
            particles = record.get('particles', [])
            for particle in particles:
                if query_lower in particle.lower():
                    score += 2
            
            if score > 0:
                result = record.copy()
                result['keyword_score'] = score
                results.append(result)
        
        # Sort by score and return top k
        results.sort(key=lambda x: x['keyword_score'], reverse=True)
        return results[:k]
    
    def hybrid_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Perform hybrid search combining vector and keyword search."""
        # Try vector search first
        vector_results = self.vector_search(query, k)
        
        # If vector search fails or returns few results, use keyword search
        if len(vector_results) < k:
            keyword_results = self.keyword_search(query, k)
            
            # Merge results, avoiding duplicates
            seen_reactions = {r['reaction'] for r in vector_results}
            for kr in keyword_results:
                if kr['reaction'] not in seen_reactions:
                    vector_results.append(kr)
                    if len(vector_results) >= k:
                        break
        
        return vector_results[:k]
    
    def search_by_particles(self, particles: List[str], k: int = 5) -> List[Dict[str, Any]]:
        """Search for diagrams containing specific particles."""
        if not _kb_data_cache:
            return []
        
        results = []
        particles_lower = [p.lower() for p in particles]
        
        for record in _kb_data_cache:
            record_particles = [p.lower() for p in record.get('particles', [])]
            
            # Count matching particles
            matches = sum(1 for p in particles_lower if any(p in rp for rp in record_particles))
            
            if matches > 0:
                result = record.copy()
                result['particle_match_score'] = matches / len(particles)
                results.append(result)
        
        # Sort by match score
        results.sort(key=lambda x: x['particle_match_score'], reverse=True)
        return results[:k]
    
    def search_by_process_type(self, process_type: str) -> List[Dict[str, Any]]:
        """Search for diagrams by process type."""
        if not _kb_data_cache:
            return []
        
        process_type_lower = process_type.lower()
        results = []
        
        for record in _kb_data_cache:
            if record.get('process_type', '').lower() == process_type_lower:
                results.append(record.copy())
        
        return results


# Convenience functions for agent use
def search_local_kb(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """Search local knowledge base using hybrid search."""
    tool = LocalKBTool()
    return tool.hybrid_search(query, k)


def search_local_kb_by_particles(particles: List[str], k: int = 5) -> List[Dict[str, Any]]:
    """Search local knowledge base by particles."""
    tool = LocalKBTool()
    return tool.search_by_particles(particles, k)


def build_local_index():
    """Build the local vector search index."""
    tool = LocalKBTool()
    tool.build_index(force_rebuild=True)


if __name__ == "__main__":
    # Test the local KB tool
    print("Testing Local KB Tool...")
    
    tool = LocalKBTool()
    
    # Build index if needed
    print("\nBuilding index...")
    tool.build_index()
    
    # Test searches
    test_queries = [
        "electron positron annihilation",
        "Z boson decay",
        "photon",
    ]
    
    for query in test_queries:
        print(f"\n--- Searching for: '{query}' ---")
        
        # Vector search
        print("\nVector search results:")
        results = tool.vector_search(query, k=3)
        for i, r in enumerate(results):
            print(f"{i+1}. {r.get('reaction')} (similarity: {r.get('similarity_score', 0):.3f})")
        
        # Keyword search
        print("\nKeyword search results:")
        results = tool.keyword_search(query, k=3)
        for i, r in enumerate(results):
            print(f"{i+1}. {r.get('reaction')} (score: {r.get('keyword_score', 0)})")
        
        # Hybrid search
        print("\nHybrid search results:")
        results = tool.hybrid_search(query, k=3)
        for i, r in enumerate(results):
            print(f"{i+1}. {r.get('reaction')}")