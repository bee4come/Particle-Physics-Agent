# Particle Physics Agent

**Intelligent Multi-Agent TikZ Feynman Diagram Generation System** - Based on Google Agent Development Kit (ADK) v1.0.0

![Version](https://img.shields.io/badge/version-0.3.4-brightgreen)
![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-blue)
![ADK](https://img.shields.io/badge/ADK-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-Beta-yellow)

## 🎯 Project Overview

Particle Physics Agent is an **autonomous learning intelligent research assistant** built on Google Agent Development Kit, capable of automatically generating high-quality TikZ Feynman diagram code from natural language descriptions. The project features an innovative **dual validation architecture** with MCP-enhanced physics validation capabilities.

### 🚀 Core Innovations

- 🧠 **Dual Validation Architecture**: Internal physics tools + MCP tools cross-validation
- 🔍 **MCP Tools Integration**: 20+ professional particle physics MCP tools auto-triggered
- 🤖 **6-Agent Collaboration System**: Streamlined specialized agent collaboration
- 📊 **Local Knowledge Base**: Annoy vector search + JSON keyword search hybrid retrieval
- 🔬 **Enhanced Physics Validation**: Detailed physics properties validation for 150+ particles
- 🌐 **Natural Language Processing**: Supports Chinese and English physics process descriptions
- ⚡ **Smart Routing Decisions**: Automatic path selection based on query quality
- 📐 **TikZ Code Generation**: Production-quality LaTeX Feynman diagram code

## 🏗️ System Architecture

### Intelligent Workflow

```
User Request → PlannerAgent → KBRetrieverAgent → PhysicsValidatorAgent (MCP) 
    ↓                              ↓                    ↓
Natural Language Parsing → Hybrid Knowledge Base Search → MCP-Enhanced Physics Validation
    ↓                              ↓                    ↓
DiagramGeneratorAgent → TikZValidatorAgent → FeedbackAgent
    ↓                              ↓                    ↓
TikZ Code Generation → LaTeX Compilation Validation → Final Response Synthesis
```

**MCP tools are automatically triggered during each physics validation phase**, providing:
- Dual validation: Internal tools + MCP tools cross-validation
- Enhanced data: Detailed physics properties for 150+ particles
- Smart diagnostics: Automatic diagnosis and suggestions for particle lookup errors

## 🤖 Agent System

### Core Agents (6)

1. **PlannerAgent** - Natural language parsing and task planning
2. **KBRetrieverAgent** - Local vector search and keyword retrieval
3. **PhysicsValidatorAgent** - MCP-enhanced physics correctness validation
4. **DiagramGeneratorAgent** - TikZ-Feynman code generation expert
5. **TikZValidatorAgent** - LaTeX compilation validation
6. **FeedbackAgent** - Result aggregation and user feedback

### MCP Tools Integration (20+ tools)

**PhysicsValidatorAgent** integrates the complete MCP particle physics toolkit:
- **Particle Search**: `search_particle_mcp` - Advanced particle database search
- **Property Retrieval**: `get_particle_properties_mcp` - Detailed particle properties
- **Quantum Number Validation**: `validate_quantum_numbers_mcp` - Advanced quantum number validation
- **Decay Analysis**: `get_branching_fractions_mcp` - Decay mode analysis
- **Particle Comparison**: `compare_particles_mcp` - Multi-particle property comparison
- **Unit Conversion**: `convert_units_mcp` - Intelligent physics unit conversion
- **Property Check**: `check_particle_properties_mcp` - Comprehensive property validation

## 🚀 Quick Start

### Requirements

- Python 3.9+
- Google ADK 1.0.0+
- Conda (recommended) or Docker
- LaTeX (optional, for local compilation validation)
- Google AI API Key
- Optional: Google Cloud Project (for deployment)

### Method 1: Google Cloud Run Deployment (Recommended for Production)

One-click deployment to Google Cloud Run for scalable serverless Feynman diagram generation:

```bash
# Set environment variables
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_API_KEY="your-gemini-api-key"

# One-click deployment
./scripts/deploy-cloud-run.sh
```

For detailed deployment guide, see [CLOUD_RUN_DEPLOYMENT.md](CLOUD_RUN_DEPLOYMENT.md)

### Method 2: Docker Local Deployment (Recommended for Development)

Use Docker to quickly deploy a complete TeX Live environment with all dependencies:

```bash
# 1. Clone the project
git clone <repository-url>
cd Particle-Physics-Agent

# 2. Configure environment variables
cp env.template .env
# Edit .env file, add your Google API Key

# 3. Run build and test script
./scripts/build-and-test.sh

# 4. Start the service
docker-compose up -d feynmancraft
```

Visit `http://localhost:8080` to start using!

### Development Mode (Docker)
```bash
# Start in development mode (supports hot reload)
docker-compose --profile dev up -d feynmancraft-dev
# Visit http://localhost:40000
```

### Local Installation Steps

If you choose to install locally without Docker:

1. **Clone the project**
   ```bash
   git clone <repository-url>
   cd Particle-Physics-Agent
   ```

2. **Create Conda environment**
   ```bash
   conda create --name fey python=3.11 -y
   conda activate fey
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file
   cat > .env << EOF
   GOOGLE_API_KEY="your_google_ai_api_key_here"
   GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   ADK_MODEL_NAME="gemini-2.0-flash"  # Optional, default value
   EOF
   ```

5. **Start Web interface**
   ```bash
   cd feynmancraft_adk
   adk web . --port 8000
   ```
   
   Open browser and visit `http://localhost:8000` to start using

### Usage Example

**Start Web interface**:
```bash
cd feynmancraft_adk
adk web . --port 8000
```

Enter in the Web interface:
```
Please generate a Feynman diagram for electron-positron annihilation producing two photons
```

**System Workflow**:
1. 📋 **PlannerAgent** - Parse natural language and create execution plan
2. 📚 **KBRetrieverAgent** - Search relevant TikZ examples
3. 🔬 **PhysicsValidatorAgent** - Validate physics correctness using MCP tools
4. 🎨 **DiagramGeneratorAgent** - Generate TikZ code
5. ✅ **TikZValidatorAgent** - LaTeX compilation validation
6. 📝 **FeedbackAgent** - Synthesize final response

## 📊 Project Structure

```
Particle-Physics-Agent/
├── feynmancraft_adk/           # Main package (ADK standard structure)
│   ├── __init__.py            # Model configuration and logging setup
│   ├── agent.py               # root_agent definition
│   ├── schemas.py             # Pydantic data models
│   ├── data/                  # Knowledge base data files
│   │   ├── feynman_kb.json        # Local knowledge base
│   │   ├── pprules.json           # Physics rules data
│   │   └── embeddings/            # Vector embedding cache
│   ├── sub_agents/            # 6 core agent implementations
│   │   ├── planner_agent.py           # Natural language parsing and planning
│   │   ├── kb_retriever_agent.py      # Knowledge base retrieval
│   │   ├── physics_validator_agent.py # MCP-enhanced physics validation
│   │   ├── diagram_generator_agent.py # TikZ code generation
│   │   ├── tikz_validator_agent.py    # LaTeX compilation validation
│   │   ├── feedback_agent.py          # Result aggregation and feedback
│   │   └── code_agent.py              # Utility functions
│   ├── shared_libraries/       # Shared utility libraries
│   │   ├── config.py              # Environment configuration
│   │   ├── prompt_utils.py        # Prompt utilities
│   │   └── physics/               # Physics data and tools
│   ├── integrations/           # External service integrations
│   │   └── mcp/                   # MCP tools integration
│   │       ├── mcp_client.py          # MCP client
│   │       ├── mcp_config.json        # MCP configuration
│   │       └── particle_name_mappings.py # Particle name mappings
│   ├── tools/                 # Tool functions
│   │   ├── kb/                    # Knowledge base tools
│   │   │   ├── bigquery.py            # BigQuery integration (unused)
│   │   │   ├── local.py               # Local vector search
│   │   │   ├── search.py              # Unified search interface
│   │   │   ├── data_loader.py         # Data loader
│   │   │   └── embedding_manager.py   # Embedding manager
│   │   ├── physics/               # Physics tools
│   │   │   ├── physics_tools.py       # MCP physics tools
│   │   │   ├── search.py              # Physics rules search
│   │   │   ├── data_loader.py         # Physics data loader
│   │   │   └── embedding_manager.py   # Physics embedding manager
│   │   ├── integrations/          # Integration tool interfaces (directly uses ../integrations/mcp)
│   │   └── latex_compiler.py      # LaTeX compiler
│   ├── docs/                  # Project documentation
│   │   ├── AGENT_TREE.md          # Agent architecture documentation
│   │   └── bigquery_setup.md      # BigQuery setup guide (unused)
│   └── scripts/               # Deployment and management scripts
│       ├── build_local_index.py   # Build local index
│       ├── upload_to_bigquery.py  # Upload to BigQuery (unused)
│       └── release.py             # Release script
├── requirements.txt           # Python dependencies
├── scripts/                   # Build and deployment scripts
│   └── build-and-test.sh         # Docker build and test pipeline
├── docker-compose.yml         # Docker orchestration configuration
├── Dockerfile                 # Docker image build
├── env.template               # Environment variable template
├── QUICKSTART.md             # Quick start guide
├── DEVELOPMENTplan.md        # Development plan
├── CHANGELOG.md              # Change log
├── VERSION                   # Version information
└── README.md                 # This document
```

## 🛠️ Tech Stack

### Core Frameworks
- **Google ADK 1.0.0** - Multi-agent orchestration framework
- **Google Gemini** - Language model (gemini-2.0-flash)
- **MCP (Model Context Protocol)** - Enhanced tool communication protocol
- **Pydantic** - Data validation and serialization

### Professional Tools
- **TikZ-Feynman** - Feynman diagram drawing
- **LaTeX** - Document compilation
- **MCP Particle Physics Tools** - 20+ professional particle physics tools
- **Annoy** - Local vector similarity search
- **Vertex AI** - Vector embedding generation

### Development Tools
- **Conda** - Environment management
- **pytest** - Testing framework
- **GitHub Actions** - CI/CD
- **Docker** - Containerized deployment
- **TeX Live 2022** - Complete LaTeX environment
- **Build Pipeline** - Automated build and test infrastructure

## 🎯 Project Milestones

### ✅ Completed Milestones
- **Phase 1**: Core ADK framework and 6-agent system ✅
- **Phase 2**: MCP tools integration and dual validation ✅
- **Phase 3**: Hybrid knowledge base and smart routing ✅
- **Phase 4**: Project optimization and code cleanup ✅
- **Phase 5**: Docker deployment and build infrastructure ✅

### 🎯 Next Steps
- **Cloud-Native Enhancement**: Kubernetes support and advanced auto-scaling
- **Monitoring and Observability**: Application performance monitoring, log aggregation, and distributed tracing
- **Performance Optimization**: Further improve response speed and resource efficiency
- **Extended Testing**: More physics processes and edge case coverage

## 📦 Latest Version

### v0.3.4 - Docker Deployment and Build Infrastructure Release
- 🐳 **Docker Support**: Complete containerized deployment with TeX Live 2022 and TikZ-Feynman support
- 🛠️ **Build and Test Pipeline**: Comprehensive validation pipeline (`scripts/build-and-test.sh`)
  - Docker image build validation
  - TeX Live installation test
  - TikZ package compilation validation
  - FeynmanCraft LaTeX compiler test
  - Feynman diagram compilation quality scoring
  - Service integration test and health checks
- 🔧 **Dependency Fixes**: Resolve package version conflicts and build issues
  - Fix PDG package version from `>=0.3.0` to `>=0.2.0`
  - Add build dependencies for C++ package compilation
  - Resolve Annoy package compilation issues in Docker environment
- 📁 **Architecture Cleanup**: Streamline MCP integration layer, remove unnecessary wrappers
- 📝 **Documentation Accuracy**: Comprehensive fact-checking and corrections, remove misleading BigQuery claims

### v0.3.3 - Workflow Enhancement Release
- 🔄 **Branch Management Optimization**: Renamed `hackathon` branch to `main`, cleaned up codebase structure
- 📝 **Documentation Improvements**: Updated README project structure diagram, corrected directory structure and file listings
- 🔧 **Workflow Analysis**: Identified and documented incomplete agent workflow execution issues
- 🌐 **Web Interface Improvements**: Improved ADK web server deployment and agent detection
- 🛠️ **MCP Tools Debugging**: Investigated and resolved PDG package dependencies and MCP connection issues

### v0.3.2 - Project Refactoring Release
- 📁 **Project Structure Optimization**: Moved `docs/` and `scripts/` into `feynmancraft_adk/` directory
- 📄 **License Consolidation**: Merged MIT and Apache 2.0 dual licenses into single LICENSE file
- 🔧 **ADK Compatibility Fix**: Fixed agent detection issues in ADK Web UI
- 📝 **Documentation Updates**: Updated path references in all documentation

### v0.3.1 - Project Optimization Release
- 🗑️ **Code Cleanup**: Removed unused OrchestratorAgent and HarvestAgent
- ⚡ **Architecture Streamlining**: Focused on production-grade workflow with 6 core agents
- 📝 **Documentation Updates**: Updated README and project structure to reflect optimized codebase
- 🔧 **Import Optimization**: Cleaned up sub_agents module import structure

See [CHANGELOG.md](CHANGELOG.md) for details

## 🏆 Innovation Highlights

### MCP-Enhanced Intelligent Validation System 🔬
1. **Dual Validation Mechanism**: Each physics validation automatically triggers internal tools + MCP tools dual validation
2. **Professional Particle Database**: Detailed physics properties, quantum numbers, decay modes for 150+ particles
3. **Smart Error Diagnostics**: Automatically provides suggestions and corrections when particle lookup fails
4. **Education-Friendly**: Provides in-depth educational explanations for complex physics processes

### Local Knowledge Architecture
1. **Vector Semantic Search**: Annoy index enables fast similarity search
2. **Keyword Exact Match**: Text and particle search in JSON data
3. **Hybrid Retrieval Strategy**: Automatically combines vector search and keyword matching
4. **Continuous Learning**: Knowledge base expansion based on user feedback

### Workflow Intelligence
1. **Natural Language Understanding**: Supports Chinese and English physics process descriptions
2. **Complete Agent Sequence**: Six-agent collaboration ensures comprehensive validation
3. **Quality Self-Monitoring**: Continuous evaluation and improvement of output quality
4. **Educational Mode**: Provides educational explanations for processes that cannot be diagrammed

## 🤝 Contributing Guidelines

We welcome community contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed information.

### Development Environment Setup
```bash
# Clone the project
git clone <repository-url>
cd feynmancraft-adk

# Set up development environment
conda create --name fey-dev python=3.9 -y
conda activate fey-dev
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black feynmancraft_adk/
isort feynmancraft_adk/
```

## 📄 License

This project is dual-licensed under MIT License and Apache License 2.0.

Please see the [LICENSE](LICENSE) file for details. You may choose either license when using this project.

## 🙏 Acknowledgments

- **Google ADK Team** - For providing the powerful multi-agent development framework
- **TikZ-Feynman Community** - For the excellent Feynman diagram drawing tools
- **Particle Data Group** - For authoritative particle physics data
- **Open Source Community** - For countless excellent open source tools and libraries

## 📞 Contact

- **Project Homepage**: [GitHub Repository](https://github.com/your-username/feynmancraft-adk)
- **Issue Tracker**: [GitHub Issues](https://github.com/your-username/feynmancraft-adk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/feynmancraft-adk/discussions)

---

**FeynmanCraft ADK - Making Physics Diagram Generation Intelligent and Simple** 🚀 