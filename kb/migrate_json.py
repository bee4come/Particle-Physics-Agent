# One-time script for migrating JSON data to the database
import json
import tqdm # For progress bar
from pathlib import Path

# Relative imports for modules within the 'kb' package
from .db import init_db, upsert_record # Corrected to upsert_record
from .schema import FeynmanRecord
from .embedding import enrich_record_with_embedding # Corrected to enrich_record_with_embedding

# Define the path to the JSON data file
# User confirmed feynman_kb_enhanced.json is in the project root.
JSON_DATA_FILE = Path("feynman_kb_enhanced.json")

def main():
    if not JSON_DATA_FILE.exists():
        print(f"Error: JSON data file not found at {JSON_DATA_FILE}")
        print("Please ensure 'feynman_kb_enhanced.json' is in the project root directory.")
        return

    print("Initializing database...")
    init_db()
    print("Database initialized.")

    print(f"Loading data from {JSON_DATA_FILE}...")
    try:
        with open(JSON_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading or parsing JSON data: {e}")
        return
    
    print(f"Found {len(data)} records in JSON file.")
    print("Starting migration and embedding process (this may take some time)...")

    # Using tqdm for a progress bar
    for item in tqdm.tqdm(data, desc="Migrating records"):
        try:
            # Ensure all fields required by FeynmanRecord are present or have defaults
            # Pydantic will raise a ValidationError if fields are missing and not Optional/defaulted
            record_data = {
                'topic': item.get('topic', 'N/A'), # Provide default if not present
                'reaction': item.get('reaction'),
                'particles': item.get('particles', []),
                'description': item.get('description', ''),
                'tikz': item.get('tikz', ''),
                'process_type': item.get('process_type', 'N/A'),
                'source': item.get('source'), # Optional, defaults to None in schema
                'embedding': item.get('embedding') # Optional, defaults to None
            }
            if not record_data['reaction']: # reaction is primary key, must exist
                print(f"Skipping item due to missing 'reaction': {item}")
                continue

            rec = FeynmanRecord(**record_data)
            enriched_rec = enrich_record_with_embedding(rec) # Embedding is generated here if None
            upsert_record(enriched_rec)
        except Exception as e:
            print(f"Error processing item {item.get('reaction', 'Unknown reaction')}: {e}")
            # Optionally, decide whether to continue or stop on error
            # continue 

    print("Data migration and embedding complete.")

if __name__ == "__main__":
    # This allows running the script directly using `python -m kb.migrate_json`
    # Ensure .env is loaded if GOOGLE_API_KEY is needed by embedding functions
    from dotenv import load_dotenv
    load_dotenv()
    main()
