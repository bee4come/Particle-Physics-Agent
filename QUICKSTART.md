# FeynmanCraft ADK Quick Start Guide

**Enhanced Multi-Agent System - Integrated with MCP Physics Validation Tools**

## 🚀 5-Minute Quick Start

### 1. Clone the Project
```bash
git clone <repository-url>
cd Particle-Physics-Agent
```

### 2. Environment Setup
```bash
# Create Conda environment
conda create --name fey python=3.11 -y
conda activate fey

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
# Copy example configuration
cp .env.example .env

# Edit .env file, at least set:
# GOOGLE_API_KEY=your-api-key-here
```

### 4. Set Up Knowledge Base

#### Build Local Index (Recommended)
```bash
# Build vector index for semantic search
python feynmancraft_adk/scripts/build_local_index.py

# Set in .env (optional)
KB_MODE=local
```

#### Hybrid Mode (Default)
```bash
# Set in .env
KB_MODE=hybrid
# System will automatically combine vector search and keyword matching
```

### 5. Run the System
```bash
# Navigate to agent directory
cd feynmancraft_adk

# Start ADK Web UI
adk web . --port 8000

# Browser will open http://localhost:8000
# If port 8000 is busy, try port 8001, 8002, etc.
```

### 6. Test Examples

Enter in ADK Web UI:
- "Generate Feynman diagram for electron-positron annihilation"
- "Draw a Z boson decay to lepton pair diagram"
- "Show Compton scattering process"
- "muon decay diagram" (test MCP tools)
- "two up quarks and one down quark" (test natural language parsing)

## 🔧 Troubleshooting

### Issue: adk command not found
```bash
# Ensure google-adk is installed
pip install google-adk
```

### Issue: API authentication failed
```bash
# Check API key
echo $GOOGLE_API_KEY

# For other Google AI services, run:
gcloud auth application-default login
```

### Issue: No search results
```bash
# Check knowledge base file
ls feynmancraft_adk/data/feynman_kb.json

# Rebuild local index
python feynmancraft_adk/scripts/build_local_index.py
```

### Issue: Port conflict
```bash
# Try different ports
adk web . --port 8001
adk web . --port 8002
# etc.
```

## 📊 System Status Check
```bash
# Navigate to project root directory
cd ..

# Run quick test
python quick_test.py

# Run full test
python test_system.py
```

## 🎯 Next Steps

1. Read [README.md](README.md) for complete feature overview
2. Run `python feynmancraft_adk/scripts/build_local_index.py` to build vector index
3. Explore `feynmancraft_adk/sub_agents/` to understand agent functionalities
4. Try modifying prompts to optimize generation results

## 💡 Tips and New Features

### 🔬 MCP Physics Validation
- **Auto-trigger**: MCP tools are automatically used for every physics validation
- **Dual validation**: Internal tools + MCP tools cross-validation
- **Detailed analysis**: Professional physics data for 150+ particles
- **Smart diagnostics**: Automatic correction suggestions for particle lookup errors

### 🗃️ Knowledge Base Modes
- **Local mode**: Annoy vector index + JSON keyword search
- **Hybrid mode**: Automatically combines semantic search and exact match for best retrieval results
- **Environment control**: Use `KB_MODE` environment variable to switch modes

### 🤖 Workflow
- **Complete sequence**: Six agents execute in order, ensuring comprehensive validation
- **Natural language**: Supports Chinese and English physics process descriptions
- **Educational mode**: Provides educational explanations for processes that cannot be diagrammed

### 🎨 Six-Agent System
1. **PlannerAgent**: Natural language parsing and task planning
2. **KBRetrieverAgent**: Hybrid knowledge base search
3. **PhysicsValidatorAgent**: MCP-enhanced physics validation
4. **DiagramGeneratorAgent**: TikZ code generation
5. **TikZValidatorAgent**: LaTeX compilation validation
6. **FeedbackAgent**: Final response synthesis

---

Having issues? Check [GitHub Issues](https://github.com/your-username/Particle-Physics-Agent/issues) or create a new issue.