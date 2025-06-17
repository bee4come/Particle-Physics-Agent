"""Configuration settings for FeynmanCraft ADK."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Knowledge Base Configuration
KB_MODE = os.getenv("KB_MODE", "hybrid").lower()  # Options: "bigquery", "local", "hybrid"
USE_BIGQUERY = KB_MODE in ["bigquery", "hybrid"]
USE_LOCAL_KB = KB_MODE in ["local", "hybrid"]

# BigQuery Configuration
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET", "feynmancraft")
BIGQUERY_TABLE = os.getenv("BIGQUERY_TABLE", "feynman_diagrams")

# Local KB Configuration
LOCAL_KB_PATH = Path(__file__).parent.parent / "data" / "feynman_kb.json"
LOCAL_INDEX_PATH = Path(__file__).parent.parent / "data" / "feynman_kb.ann"
LOCAL_ID_MAP_PATH = Path(__file__).parent.parent / "data" / "feynman_kb_id_map.json"

# Embedding Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-004")
EMBEDDING_DIM = 768

# Search Configuration
DEFAULT_SEARCH_K = int(os.getenv("DEFAULT_SEARCH_K", "5"))
SEARCH_TIMEOUT = int(os.getenv("SEARCH_TIMEOUT", "30"))  # seconds

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def get_kb_config():
    """Get current knowledge base configuration."""
    return {
        "mode": KB_MODE,
        "use_bigquery": USE_BIGQUERY,
        "use_local": USE_LOCAL_KB,
        "bigquery": {
            "project": GOOGLE_CLOUD_PROJECT,
            "dataset": BIGQUERY_DATASET,
            "table": BIGQUERY_TABLE,
        },
        "local": {
            "kb_path": str(LOCAL_KB_PATH),
            "index_path": str(LOCAL_INDEX_PATH),
            "has_index": LOCAL_INDEX_PATH.exists(),
        },
    }


def validate_config():
    """Validate configuration settings."""
    issues = []
    
    if USE_BIGQUERY and not GOOGLE_CLOUD_PROJECT:
        issues.append("BigQuery enabled but GOOGLE_CLOUD_PROJECT not set")
    
    if USE_LOCAL_KB and not LOCAL_KB_PATH.exists():
        issues.append(f"Local KB enabled but file not found: {LOCAL_KB_PATH}")
    
    if not GOOGLE_API_KEY:
        issues.append("GOOGLE_API_KEY not set - some features may not work")
    
    return issues