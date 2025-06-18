"""BigQuery knowledge base tool for FeynmanCraft agents."""

import os
from typing import List, Dict, Any, Optional
from google.cloud import bigquery
from google.oauth2 import service_account
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
DATASET_ID = "feynmancraft"
TABLE_ID = "feynman_diagrams"


class BigQueryKBTool:
    """Tool for querying Feynman diagram knowledge base in BigQuery."""
    
    def __init__(self):
        """Initialize BigQuery client."""
        self.client = self._init_client()
        self.table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    def _init_client(self) -> bigquery.Client:
        """Initialize BigQuery client with proper credentials."""
        try:
            # Try to use service account if available
            service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if service_account_path and Path(service_account_path).exists():
                credentials = service_account.Credentials.from_service_account_file(
                    service_account_path
                )
                return bigquery.Client(project=PROJECT_ID, credentials=credentials)
            else:
                # Fall back to default credentials
                return bigquery.Client(project=PROJECT_ID)
        except Exception as e:
            logger.error(f"Failed to initialize BigQuery client: {e}")
            raise
    
    def search_by_reaction(self, reaction: str) -> List[Dict[str, Any]]:
        """Search for diagrams by reaction formula."""
        query = f"""
        SELECT *
        FROM `{self.table_ref}`
        WHERE LOWER(reaction) LIKE LOWER(@reaction)
        ORDER BY created_at DESC
        LIMIT 10
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("reaction", "STRING", f"%{reaction}%")
            ]
        )
        
        try:
            query_job = self.client.query(query, job_config=job_config)
            results = list(query_job)
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Error searching by reaction: {e}")
            return []
    
    def search_by_particles(self, particles: List[str]) -> List[Dict[str, Any]]:
        """Search for diagrams containing specific particles."""
        # Create conditions for each particle
        particle_conditions = []
        for particle in particles:
            particle_conditions.append(
                f"EXISTS(SELECT 1 FROM UNNEST(particles) AS p WHERE LOWER(p) LIKE LOWER('%{particle}%'))"
            )
        
        where_clause = " AND ".join(particle_conditions)
        
        query = f"""
        SELECT *
        FROM `{self.table_ref}`
        WHERE {where_clause}
        ORDER BY created_at DESC
        LIMIT 10
        """
        
        try:
            query_job = self.client.query(query)
            results = list(query_job)
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Error searching by particles: {e}")
            return []
    
    def search_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Search for diagrams by topic."""
        query = f"""
        SELECT *
        FROM `{self.table_ref}`
        WHERE LOWER(topic) LIKE LOWER(@topic)
           OR LOWER(description) LIKE LOWER(@topic)
        ORDER BY created_at DESC
        LIMIT 10
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("topic", "STRING", f"%{topic}%")
            ]
        )
        
        try:
            query_job = self.client.query(query, job_config=job_config)
            results = list(query_job)
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Error searching by topic: {e}")
            return []
    
    def search_by_process_type(self, process_type: str) -> List[Dict[str, Any]]:
        """Search for diagrams by process type (decay, scattering, etc.)."""
        query = f"""
        SELECT *
        FROM `{self.table_ref}`
        WHERE LOWER(process_type) = LOWER(@process_type)
        ORDER BY created_at DESC
        LIMIT 10
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("process_type", "STRING", process_type)
            ]
        )
        
        try:
            query_job = self.client.query(query, job_config=job_config)
            results = list(query_job)
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Error searching by process type: {e}")
            return []
    
    def get_by_id(self, diagram_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific diagram by ID."""
        query = f"""
        SELECT *
        FROM `{self.table_ref}`
        WHERE id = @id
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("id", "STRING", diagram_id)
            ]
        )
        
        try:
            query_job = self.client.query(query, job_config=job_config)
            results = list(query_job)
            return dict(results[0]) if results else None
        except Exception as e:
            logger.error(f"Error getting diagram by ID: {e}")
            return None
    
    def semantic_search(self, query: str) -> List[Dict[str, Any]]:
        """Perform semantic search across all text fields."""
        sql_query = f"""
        SELECT *,
            (
                CASE WHEN LOWER(reaction) LIKE LOWER(@query) THEN 3 ELSE 0 END +
                CASE WHEN LOWER(topic) LIKE LOWER(@query) THEN 2 ELSE 0 END +
                CASE WHEN LOWER(description) LIKE LOWER(@query) THEN 1 ELSE 0 END
            ) AS relevance_score
        FROM `{self.table_ref}`
        WHERE LOWER(reaction) LIKE LOWER(@query)
           OR LOWER(topic) LIKE LOWER(@query)
           OR LOWER(description) LIKE LOWER(@query)
           OR EXISTS(SELECT 1 FROM UNNEST(particles) AS p WHERE LOWER(p) LIKE LOWER(@query))
        ORDER BY relevance_score DESC, created_at DESC
        LIMIT 10
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("query", "STRING", f"%{query}%")
            ]
        )
        
        try:
            query_job = self.client.query(sql_query, job_config=job_config)
            results = list(query_job)
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
    
    def add_diagram(self, diagram_data: Dict[str, Any]) -> bool:
        """Add a new diagram to the knowledge base."""
        from datetime import datetime
        
        # Add timestamps
        diagram_data["created_at"] = datetime.utcnow().isoformat()
        diagram_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Generate ID if not provided
        if "id" not in diagram_data:
            diagram_data["id"] = f"feynman_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        try:
            table = self.client.get_table(self.table_ref)
            errors = self.client.insert_rows_json(table, [diagram_data])
            
            if errors:
                logger.error(f"Failed to insert diagram: {errors}")
                return False
            return True
        except Exception as e:
            logger.error(f"Error adding diagram: {e}")
            return False


# Convenience functions for agent use
def search_kb_by_reaction(reaction: str) -> List[Dict[str, Any]]:
    """Search knowledge base by reaction."""
    tool = BigQueryKBTool()
    return tool.search_by_reaction(reaction)


def search_kb_by_particles(particles: List[str]) -> List[Dict[str, Any]]:
    """Search knowledge base by particles."""
    tool = BigQueryKBTool()
    return tool.search_by_particles(particles)


def search_kb_semantic(query: str) -> List[Dict[str, Any]]:
    """Perform semantic search on knowledge base."""
    tool = BigQueryKBTool()
    return tool.semantic_search(query)