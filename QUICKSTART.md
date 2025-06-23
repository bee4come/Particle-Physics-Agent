# FeynmanCraft ADK Quick Start Guide

**AI-Powered Multi-Agent Feynman Diagram Generation**

## 🚀 3-Minute Hackathon Setup

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

### 3. Configure API Key
```bash
# Copy example configuration
cp .env.example .env

# Edit .env file and set:
# GOOGLE_API_KEY=your-api-key-here
```

### 4. Run the System
```bash
# Start ADK Web UI
adk web . --port 8000

# Browser will open http://localhost:8000
```

### 5. Test Examples

Enter in ADK Web UI:
- "Generate Feynman diagram for electron-positron annihilation"
- "Draw a Z boson decay to lepton pair diagram"
- "Show Compton scattering process"
- "muon decay diagram"

## 🔧 Quick Troubleshooting

### Common Issues
- **adk command not found**: Run `pip install google-adk`
- **API authentication failed**: Check your GOOGLE_API_KEY in .env file
- **Port conflict**: Try different port with `--port 8001`

That's it! The system should now be running and ready for demonstration.

## 🎯 What You Get

### Six-Agent AI System
1. **PlannerAgent**: Natural language parsing
2. **KBRetrieverAgent**: Knowledge base search
3. **PhysicsValidatorAgent**: AI physics validation
4. **DiagramGeneratorAgent**: TikZ code generation
5. **TikZValidatorAgent**: AI syntax validation
6. **FeedbackAgent**: Response synthesis

Perfect for hackathon demonstrations! 🚀