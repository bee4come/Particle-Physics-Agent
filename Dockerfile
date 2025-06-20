# FeynmanCraft ADK Production Container
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including TeX Live for TikZ compilation
RUN apt-get update && apt-get install -y \
    # Build dependencies for Python packages
    build-essential \
    gcc \
    g++ \
    # Core TeX Live packages
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    # TikZ and Feynman diagram packages
    texlive-pictures \
    # Physics and science packages
    texlive-science \
    # Additional TeX Live packages for completeness
    texlive-lang-greek \
    # System utilities
    git \
    curl \
    # Ruby, TCL, TK dependencies (installed by texlive packages)
    && rm -rf /var/lib/apt/lists/* \
    # Update TeX Live package database
    && mktexlsr

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY feynmancraft_adk/ ./feynmancraft_adk/
COPY feynmancraft_adk/scripts/ ./feynmancraft_adk/scripts/
COPY VERSION ./
COPY .env.example ./.env

# Create necessary directories
RUN mkdir -p data logs tmp

# Set environment variables
ENV PYTHONPATH=/app
ENV KB_MODE=local
ENV LOG_LEVEL=INFO
ENV ADK_HOST=0.0.0.0
ENV ADK_PORT=8080

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["adk", "serve", "feynmancraft_adk", "--host", "0.0.0.0", "--port", "8080"] 