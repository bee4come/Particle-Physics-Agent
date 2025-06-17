# Changelog

All notable changes to FeynmanCraft ADK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-01-17 (Hotfix)

### Fixed
- **Import Error**: Fixed `ImportError: cannot import name 'language_models'` in physics_validator_agent.py and kb_retriever_agent.py
- **Embedding Generation**: Updated embedding functions to use `google.generativeai` API instead of deprecated `google.cloud.aiplatform.preview.language_models`
- **Package Import**: Added graceful fallback in `__init__.py` to allow package import without Google dependencies

### Changed
- Unified embedding API usage across all components
- Improved error handling for missing dependencies

## [0.2.0] - 2025-01-17

### Added
- **Dual Knowledge Base System**: Support for both BigQuery and local storage
  - BigQuery integration for production environments
  - Local vector search using Annoy index for development
  - Intelligent fallback mechanism
- **Vector Search**: Implemented semantic search using text-embedding-004
- **Configuration System**: Flexible configuration via environment variables
- **Scripts**:
  - `scripts/upload_to_bigquery.py`: Upload knowledge base to BigQuery
  - `scripts/build_local_index.py`: Build local vector search index
- **Tools**:
  - `bigquery_kb_tool.py`: BigQuery operations and queries
  - `local_kb_tool.py`: Local KB with vector and keyword search
- **Documentation**:
  - BigQuery setup guide
  - Updated CLAUDE.md for better AI assistance
  - Enhanced .env.example with all configuration options

### Changed
- Updated `KBRetrieverAgent` to support both BigQuery and local search
- Improved knowledge base search with hybrid approach
- Enhanced requirements.txt with all necessary dependencies

### Technical Details
- Vector embeddings: 768-dimensional using Gemini text-embedding-004
- Search modes: `bigquery`, `local`, `hybrid` (configurable)
- Supports multiple search strategies: semantic, keyword, particle-based

## [0.1.0] - 2025-01-12

### Initial Release
- Basic ADK agent structure
- 7 specialized sub-agents for Feynman diagram generation
- Local JSON knowledge base
- Core physics validation
- TikZ compilation validation
- Basic test runner