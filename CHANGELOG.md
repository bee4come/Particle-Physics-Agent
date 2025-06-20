# Changelog

All notable changes to FeynmanCraft ADK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.4] - Docker Deployment & Build Infrastructure

### Added
- **Docker Support**: Complete containerization with comprehensive build and test infrastructure
  - Full TeX Live 2022 installation with TikZ-Feynman support
  - Multi-stage Docker build with optimized caching
  - Production-ready Docker Compose configuration
  - Automated health checks and service validation
- **Build & Test Script**: Comprehensive validation pipeline (`scripts/build-and-test.sh`)
  - Docker image build verification
  - TeX Live installation testing
  - TikZ packages compilation validation
  - FeynmanCraft LaTeX compiler testing
  - Feynman diagram compilation with quality scoring
  - Service integration testing with health checks

### Fixed
- **Dependencies**: Resolved package version conflicts and build issues
  - Fixed PDG package version from `>=0.3.0` to `>=0.2.0` (actual available version)
  - Added build dependencies (`build-essential`, `gcc`, `g++`) for C++ package compilation
  - Resolved Annoy package compilation issues in Docker environment
- **ADK Command**: Corrected Docker startup command from `adk serve` to `adk web`
- **String Escaping**: Fixed LaTeX content escaping in Python test scripts
- **Documentation**: Removed emojis from all scripts per user preference

### Enhanced
- **Architecture Cleanup**: Streamlined MCP integration layer
  - Removed unnecessary `tools/integrations/mcp.py` wrapper
  - Updated import paths for direct MCP client usage
  - Cleaned project structure and updated documentation
- **Documentation Accuracy**: Comprehensive fact-checking and corrections
  - Removed misleading BigQuery production claims
  - Updated to accurately reflect local-only implementation
  - Corrected knowledge base descriptions (Annoy vector search + JSON keyword matching)
  - Simplified deployment documentation to remove non-functional components

### Technical Details
- Docker image: Python 3.11-slim with full TeX Live 2022
- Build time: ~4 minutes with comprehensive dependency installation
- All LaTeX compilation tests pass with quality validation
- Production-ready containerized deployment
- Clean MCP integration architecture without wrapper layers

## [0.3.3] - Workflow Enhancement & Documentation Update

### Changed
- **Branch Management**: Renamed `hackathon` branch to `main` and cleaned up repository
  - Consolidated all development into single `main` branch
  - Removed multiple feature branches for cleaner repository structure
  - Updated upstream tracking to `origin/main`
- **Documentation**: Updated README.md project structure diagram
  - Corrected project name from `feynmancraft-adk/` to `Particle-Physics-Agent/`
  - Added missing directories: `data/`, `tools/kb/`, `tools/physics/`, `tools/integrations/`
  - Removed non-existent directories: `feyncore/`, duplicate entries
  - Added detailed sub-structures for MCP integration and LaTeX compilation
  - Updated root-level file listings for accuracy

### Fixed
- **Workflow Orchestration**: Identified and documented incomplete agent workflow execution
  - Root agent stopping prematurely after `DiagramGeneratorAgent`
  - Missing `TikZValidatorAgent` execution for code compilation validation
  - Missing `FeedbackAgent` execution for final response synthesis
- **MCP Tools**: Investigated PDG package dependency issues
  - Confirmed PDG package installation
  - Identified transient MCP connection issues as cause of validation errors
  - System properly falls back to internal tools when MCP unavailable

### Enhanced
- **Web Interface**: Improved ADK web server deployment
  - Multiple port configurations (8002, 8003, 8004, 8005) for testing
  - Proper directory-based agent serving
  - Better agent detection and loading in web UI

### Technical Details
- Repository now uses single-branch development model
- Documentation accurately reflects current codebase structure
- Web ADK properly serves FeynmanCraft agent interface
- Workflow orchestration issues documented for future improvement

## [0.3.2] - Project Restructuring

### Changed
- **Project Structure**: Moved `docs/` and `scripts/` directories inside `feynmancraft_adk/` for better organization
  - All documentation now under `feynmancraft_adk/docs/`
  - All scripts now under `feynmancraft_adk/scripts/`
  - Updated all references in documentation and configuration files
- **License Files**: Merged dual licenses (MIT and Apache 2.0) into a single `LICENSE` file
  - Removed separate `LICENSE-MIT` and `LICENSE-APACHE` files
  - Clearer dual-license presentation in single file
  - Updated README.md license section

### Fixed
- **ADK Web UI**: Fixed agent detection in ADK web interface
  - Added `root_agent` export in `feynmancraft_adk/__init__.py`
  - Web UI now properly recognizes and loads the FeynmanCraft agent

### Updated
- **Documentation**: Updated all paths in:
  - README.md
  - QUICKSTART.md
  - CHANGELOG.md
  - Dockerfile
  - bigquery_setup.md

### Technical Details
- Better encapsulation with all project files under the main package
- Cleaner root directory structure
- Improved ADK compatibility with proper agent exports

## [0.3.1] - Project Optimization

### Removed
- **OrchestratorAgent**: Removed unused orchestration agent (root_agent handles orchestration directly)
- **HarvestAgent**: Removed stub implementation for offline knowledge harvesting
- **Unused Imports**: Cleaned up sub_agents module imports

### Changed
- **Agent System**: Streamlined to 6 core production agents only
- **Documentation**: Updated README and project structure to reflect optimized codebase
- **Codebase**: Removed unused code paths and simplified architecture

### Technical Details
- Focused architecture on the proven 6-agent workflow
- Eliminated confusion between different orchestration approaches
- Cleaner import structure in sub_agents module
- Updated documentation to accurately reflect current system

## [0.3.0] (MCP Integration & Workflow Enhancement)

### Added
- **MCP Integration**: Complete integration of Model Context Protocol physics tools into PhysicsValidatorAgent
  - 20+ advanced particle physics tools automatically triggered during validation
  - Enhanced particle search with comprehensive database (150+ particles)
  - Advanced quantum number validation and decay analysis
  - Intelligent unit conversion with physics context
  - Comprehensive particle property validation with diagnostics
- **Dual Validation System**: Internal tools + MCP tools cross-validation for enhanced accuracy
- **Workflow Optimization**: Ensured complete sequential execution through all 6 agents
- **Natural Language Enhancement**: Improved parsing of complex physics queries

### Fixed
- **Agent Routing**: Fixed workflow routing to prevent agents from bypassing sequential execution
- **Template Variables**: Resolved template variable parsing issues in diagram generation

### Changed
- **PhysicsValidatorAgent**: Enhanced with full MCP toolkit integration
- **Agent Prompts**: Updated all agent prompts to enforce sequential workflow execution
- **Validation Strategy**: Implemented dual validation approach using both internal and MCP tools

### Enhanced
- **Physics Validation**: Now provides comprehensive particle analysis using MCP tools
- **Error Diagnostics**: Intelligent particle lookup error diagnosis and suggestions
- **Educational Context**: Enhanced educational explanations for complex physics processes

## [0.2.1] -  (Hotfix)

### Fixed
- **Import Error**: Fixed `ImportError: cannot import name 'language_models'` in physics_validator_agent.py and kb_retriever_agent.py
- **Embedding Generation**: Updated embedding functions to use `google.generativeai` API instead of deprecated `google.cloud.aiplatform.preview.language_models`
- **Package Import**: Added graceful fallback in `__init__.py` to allow package import without Google dependencies

### Changed
- Unified embedding API usage across all components
- Improved error handling for missing dependencies

## [0.2.0] 

### Added
- **Dual Knowledge Base System**: Support for both BigQuery and local storage
  - BigQuery integration for production environments
  - Local vector search using Annoy index for development
  - Intelligent fallback mechanism
- **Vector Search**: Implemented semantic search using text-embedding-004
- **Configuration System**: Flexible configuration via environment variables
- **Scripts**:
  - `feynmancraft_adk/scripts/upload_to_bigquery.py`: Upload knowledge base to BigQuery
- `feynmancraft_adk/scripts/build_local_index.py`: Build local vector search index
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

## [0.1.0] 

### Initial Release
- Basic ADK agent structure
- 7 specialized sub-agents for Feynman diagram generation
- Local JSON knowledge base
- Core physics validation
- TikZ compilation validation
- Basic test runner