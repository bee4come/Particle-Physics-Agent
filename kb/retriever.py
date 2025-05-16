# kb/retriever.py
import os
import json
from pathlib import Path
from typing import List, Optional, Tuple

from annoy import AnnoyIndex

from .schema import FeynmanRecord
from .embedding import get_embedding, EMB_DIM # For query embedding and dimension
from .db import DB_FILE_PATH, _deserialize_embedding # Correctly import DB_FILE_PATH

ANN_INDEX_PATH = Path("data/feynman_kb.ann")
ID_MAPPING_PATH = Path("data/feynman_kb_id_map.json")

# Global cache for Annoy index and ID map to avoid reloading on every query
_annoy_index_cache: Optional[AnnoyIndex] = None
_id_map_cache: Optional[List[str]] = None

def _load_annoy_index_and_map() -> Tuple[Optional[AnnoyIndex], Optional[List[str]]]:
    """Loads the Annoy index and ID map from disk, caching them."""
    global _annoy_index_cache, _id_map_cache

    if _annoy_index_cache is not None and _id_map_cache is not None:
        return _annoy_index_cache, _id_map_cache

    if not ANN_INDEX_PATH.exists() or not ID_MAPPING_PATH.exists():
        print(f"Warning: Annoy index ({ANN_INDEX_PATH}) or ID map ({ID_MAPPING_PATH}) not found. Please build the index first.")
        return None, None
    
    try:
        print(f"Loading Annoy index from {ANN_INDEX_PATH}...")
        index = AnnoyIndex(EMB_DIM, 'angular')
        index.load(str(ANN_INDEX_PATH))
        _annoy_index_cache = index
        print("Annoy index loaded.")

        print(f"Loading ID map from {ID_MAPPING_PATH}...")
        with open(ID_MAPPING_PATH, 'r', encoding='utf-8') as f:
            _id_map_cache = json.load(f)
        print("ID map loaded.")
        
        return _annoy_index_cache, _id_map_cache
    except Exception as e:
        print(f"Error loading Annoy index or ID map: {e}")
        _annoy_index_cache = None # Invalidate cache on error
        _id_map_cache = None
        return None, None

def query_records_by_vector(query_text: str, k: int = 5, search_k: int = -1) -> List[FeynmanRecord]:
    """
    Queries records by vector similarity using Annoy.
    - query_text: The text to find similar records for.
    - k: Number of results to return.
    - search_k: Number of nodes to inspect during search. -1 means default (roughly n_trees * k).
    """
    index, id_map = _load_annoy_index_and_map()
    if not index or not id_map:
        return []

    query_embedding = get_embedding(query_text)
    if not query_embedding:
        print("Warning: Could not generate embedding for query text. Vector search cannot proceed.")
        return []

    if len(query_embedding) != EMB_DIM:
        print(f"Warning: Query embedding dimension ({len(query_embedding)}) does not match index dimension ({EMB_DIM}).")
        return []

    print(f"Performing Annoy search for query: \"{query_text[:50]}...\" (k={k}, search_k={search_k})")
    # Get k nearest neighbors. Returns a list of item indices.
    try:
        neighbor_indices, distances = index.get_nns_by_vector(query_embedding, k, search_k=search_k, include_distances=True)
    except Exception as e:
        print(f"Error during Annoy search: {e}")
        return []

    if not neighbor_indices:
        print("No similar items found by Annoy.")
        return []

    # Map Annoy indices back to reaction IDs
    retrieved_reaction_ids = [id_map[i] for i in neighbor_indices]
    print(f"Annoy retrieved reaction IDs: {retrieved_reaction_ids}")
    print(f"Distances: {distances}")


    # Fetch full records from DuckDB based on these reaction IDs
    # This requires a new DB function or direct querying here.
    # For now, let's implement a direct query.
    import duckdb # Import here to avoid circular dependency if db.py imports retriever.py
    
    records: List[FeynmanRecord] = []
    if not DB_FILE_PATH.exists(): # Use DB_FILE_PATH
        print(f"Error: DuckDB database not found at {DB_FILE_PATH} for fetching full records.")
        return []

    try:
        con = duckdb.connect(str(DB_FILE_PATH), read_only=True) # Use DB_FILE_PATH
        # Create a placeholder string for the IN clause
        placeholders = ', '.join(['?'] * len(retrieved_reaction_ids))
        sql_query = f"SELECT topic, reaction, particles, description, tikz, process_type, source, embedding FROM feynman WHERE reaction IN ({placeholders})"
        
        db_rows = con.execute(sql_query, retrieved_reaction_ids).fetchall()
        
        # Create a dictionary for quick lookup
        db_records_map = {}
        for row_data in db_rows:
            record_dict = {
                "topic": row_data[0], "reaction": row_data[1], "particles": json.loads(row_data[2]),
                "description": row_data[3], "tikz": row_data[4], "process_type": row_data[5],
                "source": row_data[6], "embedding": _deserialize_embedding(row_data[7])
            }
            db_records_map[row_data[1]] = FeynmanRecord(**record_dict)
        
        # Reconstruct records in the order Annoy returned them
        for reaction_id in retrieved_reaction_ids:
            if reaction_id in db_records_map:
                records.append(db_records_map[reaction_id])
            else:
                print(f"Warning: Reaction ID {reaction_id} from Annoy not found in DB.")

    except Exception as e:
        print(f"Error fetching records from DuckDB by reaction IDs: {e}")
    finally:
        if 'con' in locals() and con:
            con.close()
            
    return records

if __name__ == '__main__':
    # Basic test for retriever (requires .env, feynman_kb.duckdb, .ann, .json map)
    from dotenv import load_dotenv
    load_dotenv()

    print("Testing retriever functions...")
    if not ANN_INDEX_PATH.exists() or not ID_MAPPING_PATH.exists():
        print("Annoy index or ID map not found. Building them first...")
        from .build_ann_index import build_annoy_index
        build_annoy_index() # This will also initialize DB if needed via its imports
        print("--- Index build complete, proceeding with retriever test ---")


    test_query = "electron emitting a photon"
    print(f"\nQuerying for: \"{test_query}\" using vector search")
    
    # Ensure GOOGLE_API_KEY is set for get_embedding to work with Gemini
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not set. Vector search might fail or use only local model for query embedding.")

    results = query_records_by_vector(test_query, k=3)
    if results:
        print(f"\nFound {len(results)} records via vector search:")
        for i, record in enumerate(results):
            print(f"  Result {i+1}:")
            print(f"    Reaction: {record.reaction}")
            print(f"    Description: {record.description}")
            print(f"    TikZ (preview): {record.tikz.replace(os.linesep, ' ')[:80]}...")
            # print(f"    Embedding (first 3): {record.embedding[:3] if record.embedding else 'N/A'}")
    else:
        print("No records found by vector search.")
