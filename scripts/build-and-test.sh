#!/bin/bash
# FeynmanCraft ADK Build and Test Script with TikZ Validation

set -e

echo "🚀 FeynmanCraft ADK Build and Test Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose is not installed${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found, copying from env.template${NC}"
    cp env.template .env
    echo -e "${YELLOW}📝 Please edit .env file with your Google API key${NC}"
fi

echo -e "${GREEN}🔨 Building Docker images...${NC}"
docker-compose build --no-cache

echo -e "${GREEN}🧪 Testing TeX Live installation...${NC}"
docker-compose run --rm feynmancraft pdflatex --version

echo -e "${GREEN}🎯 Testing TikZ packages...${NC}"
docker-compose run --rm feynmancraft python3 -c "
import subprocess
result = subprocess.run(['pdflatex', '--version'], capture_output=True, text=True)
print('✅ pdflatex available:', result.returncode == 0)

# Test basic TikZ compilation
tex_content = '''
\\documentclass{article}
\\usepackage{tikz}
\\usepackage{tikz-feynman}
\\usepackage{physics}
\\begin{document}
\\begin{tikzpicture}
\\node{Test};
\\end{tikzpicture}
\\end{document}
'''

import tempfile
import os
with tempfile.TemporaryDirectory() as tmpdir:
    tex_file = os.path.join(tmpdir, 'test.tex')
    with open(tex_file, 'w') as f:
        f.write(tex_content)
    
    result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file], 
                          cwd=tmpdir, capture_output=True)
    print('✅ TikZ compilation test:', 'PASSED' if result.returncode == 0 else 'FAILED')
    if result.returncode != 0:
        print('Error output:', result.stderr.decode())
"

echo -e "${GREEN}🧪 Testing FeynmanCraft ADK LaTeX compiler...${NC}"
docker-compose run --rm feynmancraft python3 -c "
try:
    from feynmancraft_adk.tools import validate_tikz_compilation
    result = validate_tikz_compilation('\\\\begin{tikzpicture}\\\\node{test};\\\\end{tikzpicture}')
    print('✅ LaTeX compiler tool test:', 'PASSED' if result['success'] else 'FAILED')
    if not result['success']:
        print('Error details:', result.get('error', 'Unknown error'))
except Exception as e:
    print('❌ LaTeX compiler tool test: FAILED')
    print('Error:', str(e))
"

echo -e "${GREEN}🎯 Testing Feynman diagram compilation...${NC}"
docker-compose run --rm feynmancraft python3 -c "
try:
    from feynmancraft_adk.tools import validate_tikz_compilation
    
    feynman_code = '''
\\\\begin{tikzpicture}
\\\\begin{feynman}
\\\\vertex (a) {\\\\(e^+\\\\)};
\\\\vertex [right=of a] (b);
\\\\vertex [right=of b] (c) {\\\\(e^-\\\\)};
\\\\diagram* {
(a) -- [fermion] (b) -- [fermion] (c),
};
\\\\end{feynman}
\\\\end{tikzpicture}
'''
    
    result = validate_tikz_compilation(feynman_code)
    print('✅ Feynman diagram test:', 'PASSED' if result['success'] else 'FAILED')
    if result['success']:
        print('   Quality score:', result['analysis']['quality_score'])
    else:
        print('Error details:', result.get('error', 'Unknown error'))
        if 'analysis' in result and 'suggestions' in result['analysis']:
            print('Suggestions:')
            for suggestion in result['analysis']['suggestions']:
                print('  -', suggestion)
except Exception as e:
    print('❌ Feynman diagram test: FAILED')
    print('Error:', str(e))
"

echo -e "${GREEN}🚀 Starting services for integration test...${NC}"
docker-compose up -d feynmancraft

# Wait for service to be ready
echo -e "${YELLOW}⏳ Waiting for service to be ready...${NC}"
sleep 30

# Health check
if docker-compose exec feynmancraft curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
    docker-compose logs feynmancraft
fi

echo -e "${GREEN}🧹 Cleaning up...${NC}"
docker-compose down

echo -e "${GREEN}✅ All tests completed!${NC}"
echo ""
echo "🎯 Next steps:"
echo "  1. Edit .env file with your Google API key"
echo "  2. Run: docker-compose up -d feynmancraft"
echo "  3. Visit: http://localhost:8080"
echo ""
echo "🛠️  Development mode:"
echo "  docker-compose --profile dev up -d feynmancraft-dev"
echo "  Visit: http://localhost:40000" 