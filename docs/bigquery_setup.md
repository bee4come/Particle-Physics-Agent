# BigQuery Setup Guide for FeynmanCraft ADK

## Overview

FeynmanCraft ADK uses Google BigQuery as its production knowledge base for storing and retrieving Feynman diagram examples. This guide explains how to set up and use BigQuery with the project.

## Prerequisites

1. **Google Cloud Project**: You need a Google Cloud Project with billing enabled
2. **Google Cloud CLI**: Install `gcloud` CLI tool
3. **Authentication**: Set up authentication for your project
4. **APIs**: Enable BigQuery API in your project

## Setup Steps

### 1. Configure Environment Variables

Add the following to your `.env` file:

```bash
# Google Cloud Project ID
GOOGLE_CLOUD_PROJECT="your-project-id"

# Optional: Service Account Key Path
GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### 2. Authentication Options

You have two options for authentication:

#### Option A: Using gcloud CLI (Recommended for Development)
```bash
gcloud auth application-default login
gcloud config set project your-project-id
```

#### Option B: Using Service Account (Recommended for Production)
1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. Set `GOOGLE_APPLICATION_CREDENTIALS` in your `.env` file

### 3. Upload Data to BigQuery

Run the upload script to create the dataset, table, and populate it with data:

```bash
cd feynmancraft-adk
python scripts/upload_to_bigquery.py
```

The script will:
- Create a dataset named `feynmancraft`
- Create a table named `feynman_diagrams`
- Upload all examples from `feynmancraft_adk/data/feynman_kb.json`

### 4. Verify the Upload

You can verify the data was uploaded correctly:

```bash
# Using bq CLI
bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM `your-project-id.feynmancraft.feynman_diagrams`'

# Or in BigQuery Console
# Navigate to: https://console.cloud.google.com/bigquery
```

## BigQuery Schema

The `feynman_diagrams` table has the following schema:

| Field | Type | Description |
|-------|------|-------------|
| id | STRING | Unique identifier |
| topic | STRING | Topic of the diagram |
| reaction | STRING | Physics reaction formula |
| particles | STRING[] | Array of particles involved |
| description | STRING | Description of the process |
| tikz | STRING | TikZ code for the diagram |
| source | STRING | Source URL or reference |
| process_type | STRING | Type of process (decay, scattering, etc.) |
| source_type | STRING | Type of source (web, pdf, etc.) |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

## Using BigQuery in the Agent

The `KBRetrieverAgent` automatically uses BigQuery when available. It falls back to the local JSON file if BigQuery is not configured.

### Query Examples

The BigQuery tool supports various search methods:

```python
from feynmancraft_adk.tools.bigquery_kb_tool import BigQueryKBTool

# Initialize the tool
kb_tool = BigQueryKBTool()

# Search by reaction
results = kb_tool.search_by_reaction("e+ e- -> gamma gamma")

# Search by particles
results = kb_tool.search_by_particles(["electron", "photon"])

# Semantic search
results = kb_tool.semantic_search("electron positron annihilation")
```

## Cost Considerations

BigQuery charges for:
- **Storage**: ~$0.02 per GB per month
- **Queries**: ~$5 per TB of data processed

For this project:
- Storage cost is negligible (< 1 MB of data)
- Query costs are minimal due to small dataset size
- First 1 TB of queries per month is free

## Troubleshooting

### Common Issues

1. **Authentication Error**
   - Ensure you've run `gcloud auth application-default login`
   - Check that `GOOGLE_CLOUD_PROJECT` is set correctly

2. **Permission Denied**
   - Ensure your account has BigQuery Admin role
   - Check project billing is enabled

3. **Table Not Found**
   - Run the upload script first
   - Verify the project ID matches your configuration

### Debug Mode

To enable debug logging for BigQuery operations:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Features

### Adding New Diagrams

You can add new diagrams programmatically:

```python
from feynmancraft_adk.tools.bigquery_kb_tool import BigQueryKBTool

kb_tool = BigQueryKBTool()
new_diagram = {
    "topic": "Higgs decay",
    "reaction": "H -> gamma gamma",
    "particles": ["H", "gamma", "gamma"],
    "description": "Higgs boson decay to two photons",
    "tikz": "\\begin{tikzpicture}...",
    "source": "manual_entry",
    "process_type": "decay",
    "source_type": "manual"
}
kb_tool.add_diagram(new_diagram)
```

### Batch Operations

For bulk updates, use the BigQuery client directly:

```python
from google.cloud import bigquery

client = bigquery.Client()
# Perform batch operations...
```

## Next Steps

1. Set up automated backups of your BigQuery data
2. Implement vector embeddings for improved semantic search
3. Add data validation and quality checks
4. Set up monitoring and alerting for query performance