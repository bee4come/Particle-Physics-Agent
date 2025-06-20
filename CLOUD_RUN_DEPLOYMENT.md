# FeynmanCraft ADK Cloud Run Deployment Guide

Deploy your FeynmanCraft ADK agent with full TeX Live 2022 support to Google Cloud Run for scalable, serverless Feynman diagram generation.

## Overview

This deployment provides:
- **Complete TeX Live 2022** environment with TikZ-Feynman 1.1.0
- **ADK Web UI** for interactive diagram generation
- **REST API** endpoints for programmatic access
- **Auto-scaling** from 0 to 5 instances based on demand
- **4GB memory, 2 CPU** configuration optimized for LaTeX compilation

## Prerequisites

### 1. Google Cloud Setup

```bash
# Install Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate with Google Cloud
gcloud auth login

# Set your project (replace with your project ID)
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Enable billing for your project
# https://cloud.google.com/billing/docs/how-to/modify-project
```

### 2. Environment Variables

```bash
# Required environment variables
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"  # or your preferred region
export GOOGLE_API_KEY="your-gemini-api-key"  # Get from https://ai.google.dev/

# Optional customization
export SERVICE_NAME="feynmancraft-adk-service"
export APP_NAME="feynmancraft-adk"
```

### 3. Verify Local Build (Recommended)

```bash
# Test local Docker build first
docker build -f Dockerfile.cloudrun -t feynmancraft-cloudrun-test .
docker run -p 8080:8080 -e GOOGLE_API_KEY=$GOOGLE_API_KEY feynmancraft-cloudrun-test
```

## Deployment Methods

### Method 1: Automated Script (Recommended)

Use our comprehensive deployment script that handles all setup:

```bash
# Deploy with automatic configuration
./scripts/deploy-cloud-run.sh

# Or deploy using ADK CLI instead of gcloud
./scripts/deploy-cloud-run.sh adk

# Test existing deployment
./scripts/deploy-cloud-run.sh test
```

### Method 2: Manual gcloud Deployment

Following the [ADK Cloud Run documentation](https://google.github.io/adk-docs/deploy/cloud-run/#ui-testing):

```bash
# Enable required APIs
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com

# Deploy with gcloud (recommended for Docker containers)
gcloud run deploy feynmancraft-adk-service \
    --source . \
    --dockerfile Dockerfile.cloudrun \
    --region $GOOGLE_CLOUD_LOCATION \
    --project $GOOGLE_CLOUD_PROJECT \
    --allow-unauthenticated \
    --platform managed \
    --memory 4Gi \
    --cpu 2 \
    --timeout 3600 \
    --concurrency 10 \
    --min-instances 0 \
    --max-instances 5 \
    --port 8080 \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_API_KEY=$GOOGLE_API_KEY,KB_MODE=local,TEXLIVE_ENABLED=true,TIKZ_VALIDATION_ENABLED=true,LOG_LEVEL=INFO"
```

### Method 3: ADK CLI Deployment

If you prefer the ADK CLI approach:

```bash
# Install ADK CLI (if not already installed)
pip install google-adk

# Deploy using ADK CLI
adk deploy cloud_run \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_LOCATION \
    --service_name=feynmancraft-adk-service \
    --app_name=feynmancraft-adk \
    --with_ui \
    .
```

## Configuration Details

### Cloud Run Settings

- **Memory**: 4GiB (required for TeX Live and large LaTeX compilations)
- **CPU**: 2 vCPU (optimized for TikZ-Feynman rendering)
- **Timeout**: 3600 seconds (1 hour for complex diagrams)
- **Concurrency**: 10 (balance between resource usage and responsiveness)
- **Auto-scaling**: 0-5 instances (cost-effective with demand scaling)

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_CLOUD_PROJECT` | Your GCP project ID | Required |
| `GOOGLE_CLOUD_LOCATION` | Deployment region | Required |
| `GOOGLE_API_KEY` | Gemini API key | Required |
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI | `True` |
| `KB_MODE` | Knowledge base mode | `local` |
| `TEXLIVE_ENABLED` | Enable TeX Live | `true` |
| `TIKZ_VALIDATION_ENABLED` | Enable TikZ validation | `true` |
| `LOG_LEVEL` | Logging level | `INFO` |

### TeX Live 2022 Components

Your deployed service includes:
- **TikZ-Feynman 1.1.0** - Latest stable Feynman diagram package
- **TikZ 3.0+** - Modern graphics and positioning
- **Physics packages** - Complete LaTeX physics notation
- **Font libraries** - Comprehensive mathematics fonts
- **pdflatex** - High-quality PDF compilation

## Testing Your Deployment

### 1. Web UI Testing

Access the deployed service URL in your browser:
```
https://your-service-name-hash.a.run.app
```

The [ADK Web UI](https://google.github.io/adk-docs/deploy/cloud-run/#ui-testing) provides:
- Interactive agent selection
- Real-time conversation interface
- Session management
- Execution event viewing

### 2. API Testing

#### Health Check
```bash
# Get your service URL
SERVICE_URL=$(gcloud run services describe feynmancraft-adk-service \
    --region=$GOOGLE_CLOUD_LOCATION \
    --format="value(status.url)")

# Test health endpoint
curl -f $SERVICE_URL/health
```

#### List Available Apps
```bash
curl -X GET $SERVICE_URL/list-apps
```

#### Generate Feynman Diagram
```bash
curl -X POST $SERVICE_URL/run_sse \
    -H "Content-Type: application/json" \
    -d '{
        "app_name": "feynmancraft-adk",
        "user_id": "test_user",
        "session_id": "test_session",
        "new_message": {
            "role": "user",
            "parts": [{
                "text": "Generate a Feynman diagram for electron-positron annihilation"
            }]
        },
        "streaming": false
    }'
```

#### Streaming Response
```bash
curl -X POST $SERVICE_URL/run_sse \
    -H "Content-Type: application/json" \
    -d '{
        "app_name": "feynmancraft-adk",
        "user_id": "test_user",
        "session_id": "test_session",
        "new_message": {
            "role": "user",
            "parts": [{
                "text": "Draw a muon decay diagram"
            }]
        },
        "streaming": true
    }'
```

## Monitoring and Maintenance

### View Logs
```bash
# Real-time logs
gcloud run services logs tail feynmancraft-adk-service --region=$GOOGLE_CLOUD_LOCATION

# Recent logs
gcloud run services logs read feynmancraft-adk-service --region=$GOOGLE_CLOUD_LOCATION --limit=50
```

### Update Deployment
```bash
# Redeploy with latest code
./scripts/deploy-cloud-run.sh

# Or manually update
gcloud run deploy feynmancraft-adk-service \
    --source . \
    --dockerfile Dockerfile.cloudrun \
    --region $GOOGLE_CLOUD_LOCATION
```

### Scale Configuration
```bash
# Update scaling settings
gcloud run services update feynmancraft-adk-service \
    --region=$GOOGLE_CLOUD_LOCATION \
    --min-instances=1 \
    --max-instances=10 \
    --concurrency=20
```

## Cost Optimization

### Pricing Factors
- **Request time**: Billed per 100ms increments
- **Memory usage**: 4GiB allocation
- **CPU time**: 2 vCPU allocation
- **Network egress**: PDF generation and API responses

### Cost Reduction Tips
1. **Use streaming**: Enable streaming for real-time feedback
2. **Session management**: Reuse sessions for multiple diagrams
3. **Batch requests**: Process multiple diagrams in single sessions
4. **Monitor usage**: Use Cloud Monitoring to track costs

## Security Considerations

### Authentication (Optional)
Remove `--allow-unauthenticated` for private services:
```bash
# Deploy with authentication required
gcloud run deploy feynmancraft-adk-service \
    --source . \
    --dockerfile Dockerfile.cloudrun \
    --region $GOOGLE_CLOUD_LOCATION \
    # Remove: --allow-unauthenticated

# Get identity token for requests
TOKEN=$(gcloud auth print-identity-token)
curl -H "Authorization: Bearer $TOKEN" $SERVICE_URL/health
```

### API Key Security
- Use **Secret Manager** for production API keys
- Rotate keys regularly
- Monitor API usage in Google AI Studio

## Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check build logs
gcloud builds list --limit=5
gcloud builds log <BUILD_ID>
```

#### Memory Issues
```bash
# Increase memory allocation
gcloud run services update feynmancraft-adk-service \
    --region=$GOOGLE_CLOUD_LOCATION \
    --memory=8Gi
```

#### Timeout Issues
```bash
# Increase timeout for complex diagrams
gcloud run services update feynmancraft-adk-service \
    --region=$GOOGLE_CLOUD_LOCATION \
    --timeout=3600
```

#### TeX Live Issues
```bash
# Debug TeX Live in container
docker run -it --entrypoint=/bin/bash feynmancraft-cloudrun-test
# Inside container:
pdflatex --version
kpsewhich tikz-feynman.sty
```

### Support Resources
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [TikZ-Feynman Manual](https://ctan.org/pkg/tikz-feynman)

## Next Steps

After successful deployment:
1. **Integrate with your applications** using the REST API
2. **Set up monitoring** with Cloud Monitoring and Alerting
3. **Configure CI/CD** for automated deployments
4. **Scale resources** based on usage patterns
5. **Consider Kubernetes** deployment for advanced orchestration

Your FeynmanCraft ADK agent is now running on Google Cloud Run with full TeX Live 2022 support! 