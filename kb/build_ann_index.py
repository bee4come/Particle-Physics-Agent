# kb/build_ann_index.py
import os
import duckdb
import json
from pathlib import Path
from annoy import AnnoyIndex
from tqdm import tqdm

# Assuming these modules are in the same 'kb' package or accessible
from .db import DB_FILE_PATH as DUCKDB_PATH, _deserialize_embedding # Use existing DB path and deserializer
from .embedding import EMB_DIM # Use existing EMB_DIM

# Define paths for Annoy index and its ID mapping
ANN_INDEX_PATH = Path("data/feynman_kb.ann")
ID_MAPPING_PATH = Path("data/feynman_kb_id_map.json")
NUM_TREES = 10 # Default number of trees for Annoy index

def build_annoy_index():
    if not DUCKDB_PATH.exists():
        print(f"Error: DuckDB database not found at {DUCKDB_PATH}. Please run migration first.")
        return

    print(f"Connecting to database: {DUCKDB_PATH}")
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)

    print("Fetching records with embeddings from the database...")
    # Fetch reaction (as ID) and embedding for records where embedding is not NULL
    try:
        records_with_embeddings = con.execute(
            "SELECT reaction, embedding FROM feynman WHERE embedding IS NOT NULL"
        ).fetchall()
    except Exception as e:
        print(f"Error fetching records from database: {e}")
        con.close()
        return
    
    con.close()

    if not records_with_embeddings:
        print("No records with embeddings found in the database. Annoy index will not be built.")
        # Optionally, delete old index files if they exist
        if ANN_INDEX_PATH.exists():
            ANN_INDEX_PATH.unlink()
            print(f"Deleted old Annoy index: {ANN_INDEX_PATH}")
        if ID_MAPPING_PATH.exists():
            ID_MAPPING_PATH.unlink()
            print(f"Deleted old ID mapping: {ID_MAPPING_PATH}")
        return

    print(f"Found {len(records_with_embeddings)} records with embeddings to index.")

    # Initialize Annoy index
    # EMB_DIM should be consistent with the embeddings (e.g., 768)
    # 'angular' is common for cosine similarity with sentence embeddings
    annoy_index = AnnoyIndex(EMB_DIM, 'angular')
    
    id_map = [] # List to store reaction IDs corresponding to Annoy's integer index

    print("Adding items to Annoy index...")
    # Corrected tqdm usage: if 'from tqdm import tqdm' is used, then call is tqdm(...)
    for i, (reaction_id, embedding_blob) in enumerate(tqdm(records_with_embeddings, desc="Indexing embeddings")):
        embedding_vector = _deserialize_embedding(embedding_blob)
        if embedding_vector and len(embedding_vector) == EMB_DIM:
            annoy_index.add_item(i, embedding_vector)
            id_map.append(reaction_id)
        else:
            print(f"Warning: Skipping record with reaction ID '{reaction_id}' due to invalid or missing embedding (expected dim {EMB_DIM}).")

    if not id_map: # Check if any valid items were added
        print("No valid embeddings were added to the index. Annoy index will not be built.")
        return

    print(f"Building Annoy index with {NUM_TREES} trees... (This may take a moment)")
    annoy_index.build(NUM_TREES)
    
    # Ensure data directory exists for Annoy files
    ANN_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Saving Annoy index to: {ANN_INDEX_PATH}")
    annoy_index.save(str(ANN_INDEX_PATH))
    
    print(f"Saving ID mapping to: {ID_MAPPING_PATH}")
    with open(ID_MAPPING_PATH, 'w', encoding='utf-8') as f:
        json.dump(id_map, f)

    print("Annoy index and ID mapping built and saved successfully.")
    print(f"Total items indexed: {annoy_index.get_n_items()}")

if __name__ == "__main__":
    # Ensure .env is loaded if any underlying db/embedding ops need it (though not directly here)
    # from dotenv import load_dotenv
    # load_dotenv()
    build_annoy_index()
