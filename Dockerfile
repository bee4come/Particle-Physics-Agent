# FeynmanCraft ADK Production Container
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including Python 3.11 and TeX Live for TikZ compilation
RUN apt-get update && apt-get install -y \
    # Python 3.11 and pip
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3-pip \
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
    wget \
    # Ruby, TCL, TK dependencies (installed by texlive packages)
    && rm -rf /var/lib/apt/lists/* \
    # Update TeX Live package database
    && mktexlsr \
    # Create symlinks for python (only if they don't exist)
    && ln -sf /usr/bin/python3.11 /usr/bin/python \
    && ln -sf /usr/bin/python3.11 /usr/bin/python3

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN python3.11 -m pip install --upgrade pip \
    && python3.11 -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY feynmancraft_adk/ ./feynmancraft_adk/
# COPY feynmancraft_adk/scripts/ ./feynmancraft_adk/scripts/
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
ENV OTEL_SDK_DISABLED=true
# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["adk", "web", ".", "--host", "0.0.0.0", "--port", "8080"] 