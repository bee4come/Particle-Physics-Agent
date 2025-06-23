"""
KB Embedding Manager with singleton pattern for managing embeddings cache.
"""

import os
import json
import pickle
import asyncio
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

from .data_loader import load_kb_examples
from .embeddings import get_embedding

logger = logging.getLogger(__name__)


class KBEmbeddingManager:
    """
    Singleton manager for KB embeddings.
    
    This class manages the generation, caching, and persistence of embeddings
    for the knowledge base examples.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize instance variables
            cls._instance.kb_examples = []
            cls._instance.embeddings_cache = {}
            cls._instance.model_name = "models/text-embedding-004"
            cls._instance.is_initialized = False
            cls._instance._lock = asyncio.Lock()
        return cls._instance
    
    @property
    def cache_dir(self) -> Path:
        """Get the cache directory for storing embeddings."""
        # Navigate from tools/kb to data/embeddings
        current_dir = Path(__file__).parent
        cache_dir = current_dir.parent.parent / "data" / "embeddings"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
    
    @property
    def cache_file(self) -> Path:
        """Get the cache file path."""
        return self.cache_dir / "kb_embeddings.pkl"
    
    def reset(self):
        """Reset the manager state. Useful for testing."""
        self.kb_examples = []
        self.embeddings_cache = {}
        self.is_initialized = False
    
    async def initialize(self, force_regenerate: bool = False):
        """
        Initialize the embedding manager.
        
        Args:
            force_regenerate: If True, regenerate embeddings even if cache exists
        """
        async with self._lock:
            if self.is_initialized and not force_regenerate:
                return
                
            logger.info("Initializing KB Embedding Manager...")
            
            # Load KB examples
            self.kb_examples = load_kb_examples()
            logger.info(f"Loaded {len(self.kb_examples)} KB examples")
            
            # Try to load cached embeddings
            if not force_regenerate and self.load_embeddings():
                self.is_initialized = True
                return
                
            # Generate embeddings
            await self.generate_embeddings()
            
            # Save to cache
            self.save_embeddings()
            
            self.is_initialized = True
            logger.info("KB Embedding Manager initialized successfully")
    
    async def generate_embeddings(self):
        """Generate embeddings for all KB examples."""
        logger.info("Generating embeddings for KB examples...")
        self.embeddings_cache = {}
        
        # Create tasks for parallel embedding generation
        tasks = []
        for i, example in enumerate(self.kb_examples):
            text_to_embed = self._get_text_for_embedding(example)
            tasks.append(self._generate_single_embedding(i, text_to_embed))
        
        # Execute tasks with concurrency limit
        semaphore = asyncio.Semaphore(10)  # Limit concurrent API calls
        
        async def limited_task(task):
            async with semaphore:
                return await task
                
        limited_tasks = [limited_task(task) for task in tasks]
        results = await asyncio.gather(*limited_tasks, return_exceptions=True)
        
        # Process results
        success_count = 0
        for result in results:
            if isinstance(result, tuple) and not isinstance(result, Exception):
                idx, embedding = result
                if embedding:
                    self.embeddings_cache[idx] = embedding
                    success_count += 1
            elif isinstance(result, Exception):
                logger.error(f"Error generating embedding: {result}")
                
        logger.info(f"Generated {success_count}/{len(self.kb_examples)} embeddings successfully")
    
    async def _generate_single_embedding(self, index: int, text: str) -> tuple:
        """Generate embedding for a single text."""
        try:
            embedding = await asyncio.to_thread(get_embedding, text, self.model_name)
            return (index, embedding)
        except Exception as e:
            logger.error(f"Failed to generate embedding for index {index}: {e}")
            return (index, None)
    
    def _get_text_for_embedding(self, example: Dict[str, Any]) -> str:
        """Get the text representation of an example for embedding."""
        topic = example.get('topic', '')
        description = example.get('description', '')
        reaction = example.get('reaction', '')
        particles = ', '.join(example.get('particles', []))
        
        # Combine relevant fields
        text_parts = []
        if topic:
            text_parts.append(f"Topic: {topic}")
        if description:
            text_parts.append(f"Description: {description}")
        if reaction:
            text_parts.append(f"Reaction: {reaction}")
        if particles:
            text_parts.append(f"Particles: {particles}")
            
        return " | ".join(text_parts)
    
    def get_embedding(self, index: int) -> Optional[List[float]]:
        """
        Get embedding for a specific KB example by index.
        
        Args:
            index: Index of the KB example
            
        Returns:
            Embedding vector or None if not found
        """
        return self.embeddings_cache.get(index)
    
    def get_all_embeddings(self) -> Dict[int, List[float]]:
        """Get all cached embeddings."""
        return self.embeddings_cache.copy()
    
    def save_embeddings(self) -> bool:
        """
        Save embeddings to disk.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cache_data = {
                'embeddings': self.embeddings_cache,
                'model_name': self.model_name,
                'num_examples': len(self.kb_examples)
            }
            
            with open(self.cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
                
            logger.info(f"Saved embeddings to {self.cache_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save embeddings: {e}")
            return False
    
    def load_embeddings(self) -> bool:
        """
        Load embeddings from disk.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.cache_file.exists():
            logger.info("No embeddings cache file found")
            return False
            
        try:
            with open(self.cache_file, 'rb') as f:
                cache_data = pickle.load(f)
                
            # Validate cache
            if cache_data.get('num_examples') != len(self.kb_examples):
                logger.warning("Cache size mismatch, regenerating embeddings")
                return False
                
            if cache_data.get('model_name') != self.model_name:
                logger.warning("Model name mismatch, regenerating embeddings")
                return False
                
            self.embeddings_cache = cache_data['embeddings']
            logger.info(f"Loaded {len(self.embeddings_cache)} embeddings from cache")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load embeddings: {e}")
            return False
    
    def clear_cache(self):
        """Clear the embeddings cache from memory and disk."""
        self.embeddings_cache = {}
        self.is_initialized = False
        
        if self.cache_file.exists():
            try:
                self.cache_file.unlink()
                logger.info("Deleted embeddings cache file")
            except Exception as e:
                logger.error(f"Failed to delete cache file: {e}")


# Convenience functions for backward compatibility
_manager = KBEmbeddingManager()


async def embed_and_cache_kb(force_regenerate: bool = False):
    """
    Generate and cache embeddings for all KB examples.
    
    Args:
        force_regenerate: If True, regenerate embeddings even if cache exists
    """
    await _manager.initialize(force_regenerate)


def get_kb_manager() -> KBEmbeddingManager:
    """Get the singleton KB embedding manager instance."""
    return _manager