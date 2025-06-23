"""
Physics Rules Embedding Manager with singleton pattern.
"""

import os
import json
import pickle
import asyncio
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

from .data_loader import load_physics_rules
from ..kb.embeddings import get_embedding

logger = logging.getLogger(__name__)


class RulesEmbeddingManager:
    """
    Singleton manager for physics rules embeddings.
    
    This class manages the generation, caching, and persistence of embeddings
    for physics rules used in validation.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize instance variables
            cls._instance.physics_rules = []
            cls._instance.embeddings_cache = {}
            cls._instance.model_name = "models/text-embedding-004"
            cls._instance.is_initialized = False
            cls._instance._lock = asyncio.Lock()
        return cls._instance
    
    @property
    def cache_dir(self) -> Path:
        """Get the cache directory for storing embeddings."""
        # Navigate from tools/physics to data/embeddings
        current_dir = Path(__file__).parent
        cache_dir = current_dir.parent.parent / "data" / "embeddings"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
    
    @property
    def cache_file(self) -> Path:
        """Get the cache file path."""
        return self.cache_dir / "rules_embeddings.pkl"
    
    def reset(self):
        """Reset the manager state. Useful for testing."""
        self.physics_rules = []
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
                
            logger.info("Initializing Physics Rules Embedding Manager...")
            
            # Load physics rules
            self.physics_rules = load_physics_rules()
            logger.info(f"Loaded {len(self.physics_rules)} physics rules")
            
            # Try to load cached embeddings
            if not force_regenerate and self.load_embeddings():
                self.is_initialized = True
                return
                
            # Generate embeddings
            await self.generate_embeddings()
            
            # Save to cache
            self.save_embeddings()
            
            self.is_initialized = True
            logger.info("Physics Rules Embedding Manager initialized successfully")
    
    async def generate_embeddings(self):
        """Generate embeddings for all physics rules."""
        logger.info("Generating embeddings for physics rules...")
        self.embeddings_cache = {}
        
        # Create tasks for parallel embedding generation
        tasks = []
        for rule in self.physics_rules:
            rule_number = rule.get("rule_number")
            content = rule.get("content", "")
            if rule_number and content:
                tasks.append(self._generate_single_embedding(rule_number, content))
        
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
                rule_number, embedding = result
                if embedding:
                    self.embeddings_cache[rule_number] = embedding
                    success_count += 1
            elif isinstance(result, Exception):
                logger.error(f"Error generating embedding: {result}")
                
        logger.info(f"Generated {success_count}/{len(tasks)} rule embeddings successfully")
    
    async def _generate_single_embedding(self, rule_number: Any, content: str) -> tuple:
        """Generate embedding for a single rule."""
        try:
            embedding = await asyncio.to_thread(get_embedding, content, self.model_name)
            return (rule_number, embedding)
        except Exception as e:
            logger.error(f"Failed to generate embedding for rule {rule_number}: {e}")
            return (rule_number, None)
    
    def get_embedding(self, rule_number: Any) -> Optional[List[float]]:
        """
        Get embedding for a specific physics rule by rule number.
        
        Args:
            rule_number: Rule number
            
        Returns:
            Embedding vector or None if not found
        """
        return self.embeddings_cache.get(rule_number)
    
    def get_all_embeddings(self) -> Dict[Any, List[float]]:
        """Get all cached rule embeddings."""
        return self.embeddings_cache.copy()
    
    def get_rule_by_number(self, rule_number: Any) -> Optional[Dict[str, Any]]:
        """
        Get a rule by its number.
        
        Args:
            rule_number: Rule number to find
            
        Returns:
            Rule dictionary or None if not found
        """
        for rule in self.physics_rules:
            if rule.get("rule_number") == rule_number:
                return rule
        return None
    
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
                'num_rules': len(self.physics_rules)
            }
            
            with open(self.cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
                
            logger.info(f"Saved rule embeddings to {self.cache_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save rule embeddings: {e}")
            return False
    
    def load_embeddings(self) -> bool:
        """
        Load embeddings from disk.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.cache_file.exists():
            logger.info("No rule embeddings cache file found")
            return False
            
        try:
            with open(self.cache_file, 'rb') as f:
                cache_data = pickle.load(f)
                
            # Validate cache
            if cache_data.get('num_rules') != len(self.physics_rules):
                logger.warning("Rules cache size mismatch, regenerating embeddings")
                return False
                
            if cache_data.get('model_name') != self.model_name:
                logger.warning("Model name mismatch, regenerating embeddings")
                return False
                
            self.embeddings_cache = cache_data['embeddings']
            logger.info(f"Loaded {len(self.embeddings_cache)} rule embeddings from cache")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load rule embeddings: {e}")
            return False
    
    def clear_cache(self):
        """Clear the embeddings cache from memory and disk."""
        self.embeddings_cache = {}
        self.is_initialized = False
        
        if self.cache_file.exists():
            try:
                self.cache_file.unlink()
                logger.info("Deleted rule embeddings cache file")
            except Exception as e:
                logger.error(f"Failed to delete cache file: {e}")
    
    def get_rules_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all rules in a specific category.
        
        Args:
            category: Category name (case-insensitive)
            
        Returns:
            List of rules in the category
        """
        category_lower = category.lower()
        return [
            rule for rule in self.physics_rules
            if category_lower in rule.get("category", "").lower()
        ]
    
    def search_rules_by_content(self, query: str) -> List[Dict[str, Any]]:
        """
        Search rules by content using simple text matching.
        
        Args:
            query: Search query
            
        Returns:
            List of matching rules
        """
        query_lower = query.lower()
        matching_rules = []
        
        for rule in self.physics_rules:
            content = rule.get("content", "").lower()
            description = rule.get("description", "").lower()
            
            if query_lower in content or query_lower in description:
                matching_rules.append(rule)
                
        return matching_rules


# Convenience functions for backward compatibility
_manager = RulesEmbeddingManager()


async def embed_and_cache_rules(force_regenerate: bool = False):
    """
    Generate and cache embeddings for all physics rules.
    
    Args:
        force_regenerate: If True, regenerate embeddings even if cache exists
    """
    await _manager.initialize(force_regenerate)


def get_rules_manager() -> RulesEmbeddingManager:
    """Get the singleton rules embedding manager instance."""
    return _manager