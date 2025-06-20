#!/bin/bash

# FeynmanCraft ADK Cloud Run Deployment Script
# Based on: https://google.github.io/adk-docs/deploy/cloud-run/#ui-testing

set -e

echo "🚀 FeynmanCraft ADK Cloud Run Deployment Script"
echo "================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if required environment variables are set
check_env_vars() {
    local required_vars=("GOOGLE_CLOUD_PROJECT" "GOOGLE_CLOUD_LOCATION")
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo -e "${RED}Error: Missing required environment variables:${NC}"
        printf ' - %s\n' "${missing_vars[@]}"
        echo ""
        echo "Please set the required variables:"
        echo "export GOOGLE_CLOUD_PROJECT=\"your-gcp-project-id\""
        echo "export GOOGLE_CLOUD_LOCATION=\"us-central1\""
        echo "export GOOGLE_API_KEY=\"your-gemini-api-key\""
        exit 1
    fi
}

# Set default values for optional variables
set_defaults() {
    export SERVICE_NAME="${SERVICE_NAME:-feynmancraft-adk-service}"
    export APP_NAME="${APP_NAME:-feynmancraft-adk}"
    export AGENT_PATH="${AGENT_PATH:-.}"
    export DOCKER_FILE="${DOCKER_FILE:-Dockerfile.cloudrun}"
}

# Validate Google Cloud authentication
check_gcloud_auth() {
    echo -e "${BLUE}Checking Google Cloud authentication...${NC}"
    
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1 > /dev/null; then
        echo -e "${RED}Error: Not authenticated with Google Cloud${NC}"
        echo "Please run: gcloud auth login"
        exit 1
    fi
    
    # Set the project
    gcloud config set project "$GOOGLE_CLOUD_PROJECT"
    echo -e "${GREEN}✓ Authenticated with Google Cloud${NC}"
}

# Enable required APIs
enable_apis() {
    echo -e "${BLUE}Enabling required Google Cloud APIs...${NC}"
    
    gcloud services enable \
        cloudbuild.googleapis.com \
        run.googleapis.com \
        artifactregistry.googleapis.com \
        aiplatform.googleapis.com
        
    echo -e "${GREEN}✓ APIs enabled${NC}"
}

# Build and deploy using gcloud (recommended for Docker containers with TeX Live)
deploy_with_gcloud() {
    echo -e "${BLUE}Deploying FeynmanCraft ADK to Cloud Run...${NC}"
    echo "Service: $SERVICE_NAME"
    echo "Region: $GOOGLE_CLOUD_LOCATION"
    echo "Project: $GOOGLE_CLOUD_PROJECT"
    echo ""
    
    # Deploy using gcloud with our custom Dockerfile
    gcloud run deploy "$SERVICE_NAME" \
        --source . \
        --dockerfile "$DOCKER_FILE" \
        --region "$GOOGLE_CLOUD_LOCATION" \
        --project "$GOOGLE_CLOUD_PROJECT" \
        --allow-unauthenticated \
        --platform managed \
        --memory 4Gi \
        --cpu 2 \
        --timeout 3600 \
        --concurrency 10 \
        --min-instances 0 \
        --max-instances 5 \
        --port 8080 \
        --set-env-vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_API_KEY=$GOOGLE_API_KEY,KB_MODE=local,TEXLIVE_ENABLED=true,TIKZ_VALIDATION_ENABLED=true,LOG_LEVEL=INFO" \
        --tag="$SERVICE_NAME:$(cat VERSION)"
}

# Alternative: Deploy using ADK CLI (if preferred)
deploy_with_adk_cli() {
    echo -e "${BLUE}Deploying with ADK CLI...${NC}"
    
    adk deploy cloud_run \
        --project="$GOOGLE_CLOUD_PROJECT" \
        --region="$GOOGLE_CLOUD_LOCATION" \
        --service_name="$SERVICE_NAME" \
        --app_name="$APP_NAME" \
        --with_ui \
        "$AGENT_PATH"
}

# Test the deployed service
test_deployment() {
    echo -e "${BLUE}Testing deployed service...${NC}"
    
    # Get the service URL
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$GOOGLE_CLOUD_LOCATION" \
        --format="value(status.url)")
    
    if [ -z "$SERVICE_URL" ]; then
        echo -e "${RED}Error: Could not get service URL${NC}"
        exit 1
    fi
    
    echo "Service URL: $SERVICE_URL"
    
    # Test health endpoint
    echo "Testing health endpoint..."
    if curl -f "$SERVICE_URL/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Health check passed${NC}"
    else
        echo -e "${YELLOW}⚠ Health check failed (service may still be starting)${NC}"
    fi
    
    # Test list-apps endpoint
    echo "Testing list-apps endpoint..."
    if curl -f "$SERVICE_URL/list-apps" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ ADK API is responding${NC}"
    else
        echo -e "${YELLOW}⚠ ADK API test failed${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 Deployment completed!${NC}"
    echo ""
    echo "Access your FeynmanCraft ADK service at:"
    echo -e "${BLUE}$SERVICE_URL${NC}"
    echo ""
    echo "To test with curl:"
    echo "curl -X POST $SERVICE_URL/run_sse \\"
    echo "  -H \"Content-Type: application/json\" \\"
    echo "  -d '{\"app_name\": \"$APP_NAME\", \"user_id\": \"test_user\", \"session_id\": \"test_session\", \"new_message\": {\"role\": \"user\", \"parts\": [{\"text\": \"Generate a Feynman diagram for electron-positron annihilation\"}]}, \"streaming\": false}'"
}

# Main deployment function
main() {
    echo "Starting FeynmanCraft ADK Cloud Run deployment..."
    echo ""
    
    check_env_vars
    set_defaults
    check_gcloud_auth
    enable_apis
    
    # Use gcloud deployment for Docker containers with TeX Live
    deploy_with_gcloud
    
    # Test the deployment
    test_deployment
}

# Handle command line arguments
case "${1:-}" in
    "test")
        test_deployment
        ;;
    "adk")
        check_env_vars
        set_defaults
        check_gcloud_auth
        deploy_with_adk_cli
        test_deployment
        ;;
    *)
        main
        ;;
esac 