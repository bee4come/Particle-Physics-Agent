#!/usr/bin/env python
"""Upload Feynman knowledge base to BigQuery."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
DATASET_ID = "feynmancraft"
TABLE_ID = "feynman_diagrams"
JSON_FILE = Path(__file__).parent.parent / "feynmancraft_adk" / "data" / "feynman_kb.json"

# BigQuery schema for the table
SCHEMA = [
    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("topic", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("reaction", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("particles", "STRING", mode="REPEATED"),
    bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("tikz", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("source", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("process_type", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("source_type", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("updated_at", "TIMESTAMP", mode="REQUIRED"),
]


def create_dataset_if_not_exists(client: bigquery.Client, dataset_id: str):
    """Create dataset if it doesn't exist."""
    dataset_ref = client.dataset(dataset_id)
    
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} already exists.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        dataset.description = "FeynmanCraft knowledge base for Feynman diagrams"
        
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"Created dataset {dataset.project}.{dataset.dataset_id}")


def create_table_if_not_exists(client: bigquery.Client, dataset_id: str, table_id: str):
    """Create table if it doesn't exist."""
    table_ref = client.dataset(dataset_id).table(table_id)
    
    try:
        client.get_table(table_ref)
        print(f"Table {table_id} already exists.")
        return False
    except Exception:
        table = bigquery.Table(table_ref, schema=SCHEMA)
        table.description = "Feynman diagram examples and templates"
        
        table = client.create_table(table)
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")
        return True


def load_json_data(json_file: Path):
    """Load and transform JSON data for BigQuery."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Transform data to match BigQuery schema
    rows = []
    for i, item in enumerate(data):
        row = {
            "id": f"feynman_{i+1:04d}",
            "topic": item.get("topic", ""),
            "reaction": item.get("reaction", ""),
            "particles": item.get("particles", []),
            "description": item.get("description", ""),
            "tikz": item.get("tikz", ""),
            "source": item.get("source", ""),
            "process_type": item.get("process_type", ""),
            "source_type": item.get("source_type", ""),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        rows.append(row)
    
    return rows


def upload_to_bigquery(client: bigquery.Client, dataset_id: str, table_id: str, rows: list):
    """Upload data to BigQuery table."""
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)
    
    errors = client.insert_rows_json(table, rows)
    
    if errors:
        print(f"Failed to insert rows: {errors}")
        return False
    else:
        print(f"Successfully inserted {len(rows)} rows into {dataset_id}.{table_id}")
        return True


def main():
    """Main function to upload data to BigQuery."""
    print("=== FeynmanCraft BigQuery Upload Script ===")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Dataset: {DATASET_ID}")
    print(f"Table: {TABLE_ID}")
    print(f"JSON file: {JSON_FILE}")
    print()
    
    # Check if JSON file exists
    if not JSON_FILE.exists():
        print(f"Error: JSON file not found at {JSON_FILE}")
        sys.exit(1)
    
    # Initialize BigQuery client
    try:
        # Try to use service account if available
        service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if service_account_path and Path(service_account_path).exists():
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path
            )
            client = bigquery.Client(project=PROJECT_ID, credentials=credentials)
        else:
            # Fall back to default credentials
            client = bigquery.Client(project=PROJECT_ID)
    except Exception as e:
        print(f"Error initializing BigQuery client: {e}")
        print("\nMake sure you have either:")
        print("1. Set GOOGLE_APPLICATION_CREDENTIALS to your service account key file")
        print("2. Run 'gcloud auth application-default login'")
        sys.exit(1)
    
    # Create dataset if needed
    create_dataset_if_not_exists(client, DATASET_ID)
    
    # Create table if needed
    table_created = create_table_if_not_exists(client, DATASET_ID, TABLE_ID)
    
    # Load JSON data
    print("\nLoading JSON data...")
    rows = load_json_data(JSON_FILE)
    print(f"Loaded {len(rows)} records from JSON file")
    
    # Upload to BigQuery
    if table_created or input("\nTable already exists. Upload data anyway? (y/n): ").lower() == 'y':
        print("\nUploading to BigQuery...")
        success = upload_to_bigquery(client, DATASET_ID, TABLE_ID, rows)
        
        if success:
            print("\n✅ Upload completed successfully!")
            print(f"\nYou can query the data with:")
            print(f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` LIMIT 10")
        else:
            print("\n❌ Upload failed!")
            sys.exit(1)


if __name__ == "__main__":
    main()