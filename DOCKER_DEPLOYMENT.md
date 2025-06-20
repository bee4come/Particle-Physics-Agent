# FeynmanCraft ADK Docker Deployment Guide

This guide explains how to deploy FeynmanCraft ADK with full TikZ compilation and validation support using Docker.

## 🚀 Quick Start

### Basic Production Deployment

```bash
# Clone the repository
git clone <repository-url>
cd feynmancraft-adk

# Set up environment variables
cp .env.example .env
# Edit .env with your Google API key

# Build and run
docker-compose up -d feynmancraft
```

### Development Mode

```bash
# Run in development mode with hot reload
docker-compose --profile dev up -d feynmancraft-dev
```

### TikZ-Only Validation Service

```bash
# Run standalone TikZ validation service
docker-compose --profile tikz-only up -d tikz-validator
```

## 📦 Services Overview

### `feynmancraft` (Production)
- **Port**: 8080
- **Purpose**: Full FeynmanCraft ADK application
- **Features**: Complete physics diagram generation with TikZ validation
- **Resources**: Optimized for production use

### `feynmancraft-dev` (Development)
- **Port**: 40000
- **Purpose**: Development environment with hot reload
- **Features**: Live code reloading, debug logging
- **Profile**: `dev`

### `tikz-validator` (Standalone)
- **Purpose**: Isolated TikZ compilation and validation
- **Features**: Pure LaTeX/TikZ validation service
- **Profile**: `tikz-only`

## 🎯 Environment Variables

### Core Settings
```env
# Google AI Configuration
GOOGLE_API_KEY=your_api_key_here

# Knowledge Base
KB_MODE=local

# Application Settings
MODEL_TEMPERATURE=0.7
DEFAULT_SEARCH_K=5
LOG_LEVEL=INFO
```

### TikZ Validation Settings
```env
# TeX Live Configuration
TEXLIVE_ENABLED=true
TIKZ_VALIDATION_ENABLED=true
LATEX_COMPILER=pdflatex
TEX_MAX_COMPILATION_TIME=30
```

## 🛠 Installed TeX Live Packages

The Docker image includes the following TeX Live packages:

### Core Packages
- `texlive-latex-base` - Basic LaTeX functionality
- `texlive-latex-extra` - Extended LaTeX packages
- `texlive-fonts-recommended` - Recommended fonts
- `texlive-fonts-extra` - Additional fonts

### TikZ and Diagram Packages
- `texlive-pictures` - **TikZ, tikz-feynman, PGF graphics**
  - Enables Feynman diagram generation
  - Includes TikZ libraries for scientific diagrams

### Physics and Science Packages
- `texlive-science` - **Physics package and scientific symbols**
  - Mathematical physics notation
  - Scientific computation packages

### Additional Support
- `texlive-lang-greek` - Greek language support for physics symbols

## 🔧 Volume Mounts

### Production (`feynmancraft`)
```yaml
volumes:
  - ./data:/app/data:ro          # Knowledge base data (read-only)
  - ./logs:/app/logs             # Application logs
  - ./tmp:/app/tmp               # Temporary files
  - tikz-compile-cache:/tmp/tikz-compile  # TikZ compilation cache
```

### Development (`feynmancraft-dev`)
```yaml
volumes:
  - .:/app                       # Live code mounting
  - ./logs:/app/logs             # Application logs
  - tikz-compile-cache:/tmp/tikz-compile  # TikZ compilation cache
```

## 🚨 Health Checks

The production service includes health checks:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## 📁 Directory Structure

```
feynmancraft-adk/
├── docker-compose.yml          # Multi-service orchestration
├── Dockerfile                  # Container definition with TeX Live
├── .env.example               # Environment template
├── data/                      # Knowledge base data
├── logs/                      # Application logs
├── tmp/                       # Temporary files
└── feynmancraft_adk/          # Application code
    ├── tools/
    │   └── latex_compiler.py   # TikZ validation engine
    └── sub_agents/
        └── tikz_validator_agent.py  # Validation agent
```

## 🔍 Testing TikZ Validation

### Verify TeX Live Installation

```bash
# Check if TeX Live is properly installed
docker-compose exec feynmancraft pdflatex --version

# Test TikZ compilation
docker-compose exec feynmancraft python -c "
from feynmancraft_adk.tools import validate_tikz_compilation
result = validate_tikz_compilation('\\\\begin{tikzpicture}\\\\node{test};\\\\end{tikzpicture}')
print('Success:', result['success'])
"
```

### Manual TikZ Test

```bash
# Run a manual TikZ validation test
docker-compose exec feynmancraft python -m feynmancraft_adk.tools.latex_compiler
```

## 🐛 Troubleshooting

### Common Issues

1. **TeX Live packages missing**
   ```bash
   # Rebuild with clean cache
   docker-compose build --no-cache feynmancraft
   ```

2. **Permission issues with volumes**
   ```bash
   # Fix permissions
   sudo chown -R $(id -u):$(id -g) ./logs ./tmp
   ```

3. **Memory issues during TeX compilation**
   ```yaml
   # Add to docker-compose.yml service
   deploy:
     resources:
       limits:
         memory: 2G
   ```

### Debug Commands

```bash
# View logs
docker-compose logs feynmancraft

# Shell access
docker-compose exec feynmancraft bash

# Check TeX Live installation
docker-compose exec feynmancraft tlmgr --version
```

## 🚀 Production Deployment Tips

1. **Resource Allocation**: Allocate at least 1GB RAM for TeX compilation
2. **Volume Persistence**: Use named volumes for better performance
3. **Monitoring**: Monitor `/tmp/tikz-compile` volume usage
4. **Scaling**: Use multiple replicas with shared volumes for load balancing

## 📈 Performance Optimization

### TeX Compilation Cache
The `tikz-compile-cache` volume stores compiled artifacts to speed up repeated operations.

### Environment Tuning
```env
# Optimize for your workload
TEX_MAX_COMPILATION_TIME=60     # Increase for complex diagrams
LOG_LEVEL=WARNING               # Reduce logging in production
```

This deployment setup ensures that FeynmanCraft ADK has full TikZ compilation capabilities with the validation-correction loop system for robust diagram generation. 