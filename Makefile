# FeynmanCraft ADK Docker Makefile
# Simplified commands for Docker deployment with TikZ validation

.PHONY: help build test dev prod clean logs shell tikz-test

# Default target
help: ## Show this help message
	@echo "FeynmanCraft ADK Docker Commands"
	@echo "==============================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	@echo "🔨 Building FeynmanCraft ADK with TeX Live..."
	docker-compose build --no-cache

test: ## Run comprehensive tests including TikZ validation
	@echo "🧪 Running build and test suite..."
	./scripts/build-and-test.sh

dev: ## Start development environment with hot reload
	@echo "🚀 Starting development environment..."
	docker-compose --profile dev up -d feynmancraft-dev
	@echo "✅ Development server running at http://localhost:40000"

prod: ## Start production environment
	@echo "🚀 Starting production environment..."
	docker-compose up -d feynmancraft
	@echo "✅ Production server running at http://localhost:8080"

tikz-only: ## Start standalone TikZ validation service
	@echo "🎯 Starting TikZ validation service..."
	docker-compose --profile tikz-only up -d tikz-validator
	@echo "✅ TikZ validator service started"

stop: ## Stop all services
	@echo "🛑 Stopping all services..."
	docker-compose down

clean: ## Clean up containers, images, and volumes
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down -v --rmi all
	docker system prune -f

logs: ## View logs from production service
	@echo "📋 Viewing FeynmanCraft logs..."
	docker-compose logs -f feynmancraft

logs-dev: ## View logs from development service
	@echo "📋 Viewing development logs..."
	docker-compose logs -f feynmancraft-dev

shell: ## Open shell in running production container
	@echo "🐚 Opening shell in production container..."
	docker-compose exec feynmancraft bash

shell-dev: ## Open shell in running development container
	@echo "🐚 Opening shell in development container..."
	docker-compose exec feynmancraft-dev bash

tikz-test: ## Test TikZ compilation manually
	@echo "🧪 Testing TikZ compilation..."
	docker-compose run --rm feynmancraft python3 -c "\
	from feynmancraft_adk.tools import validate_tikz_compilation; \
	result = validate_tikz_compilation('\\\\begin{tikzpicture}\\\\node{test};\\\\end{tikzpicture}'); \
	print('Success:', result['success']); \
	print('Details:', result.get('analysis', {}))"

health: ## Check service health
	@echo "🔍 Checking service health..."
	@if curl -f http://localhost:8080/health > /dev/null 2>&1; then \
		echo "✅ Production service is healthy"; \
	else \
		echo "❌ Production service is not responding"; \
	fi
	@if curl -f http://localhost:40000/health > /dev/null 2>&1; then \
		echo "✅ Development service is healthy"; \
	else \
		echo "❌ Development service is not responding"; \
	fi

restart: ## Restart production services
	@echo "🔄 Restarting production services..."
	docker-compose restart feynmancraft

restart-dev: ## Restart development services
	@echo "🔄 Restarting development services..."
	docker-compose restart feynmancraft-dev

env: ## Create .env file from template
	@echo "📝 Creating .env file..."
	@if [ ! -f .env ]; then \
		cp env.template .env; \
		echo "✅ .env file created from template"; \
		echo "📝 Please edit .env file with your configuration"; \
	else \
		echo "⚠️  .env file already exists"; \
	fi

status: ## Show status of all services
	@echo "📊 Service Status:"
	@echo "=================="
	docker-compose ps

# Advanced targets
rebuild: clean build ## Clean rebuild everything

full-test: build test ## Build and run full test suite

deploy: env build prod ## Complete deployment (env + build + production)

# Monitoring targets
monitor: ## Monitor resource usage
	@echo "📈 Monitoring Docker resources..."
	docker stats

volumes: ## Show volume information
	@echo "💾 Docker volumes:"
	docker volume ls | grep tikz

# Development helpers
format: ## Format Python code in development container
	@echo "🎨 Formatting Python code..."
	docker-compose run --rm feynmancraft-dev python -m black feynmancraft_adk/

lint: ## Lint Python code in development container
	@echo "🔍 Linting Python code..."
	docker-compose run --rm feynmancraft-dev python -m flake8 feynmancraft_adk/

# Documentation
docs: ## Generate documentation
	@echo "📚 Opening documentation..."
	@echo "📖 Docker Deployment Guide: DOCKER_DEPLOYMENT.md"
	@echo "📖 Quick Start: README.md" 