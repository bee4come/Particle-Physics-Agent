# kb/annoy_index.py
import os
import json
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from annoy import AnnoyIndex

from .schema import FeynmanRecord
from .embedding import get_embedding, EMB_DIM
from .db import get_record_by_id # To fetch full record if needed, or ensure ID exists

# Define paths using Path objects for consistency
DATA_DIR = Path("data")
ANN_INDEX_PATH = DATA_DIR / "feynman_kb.ann"
ID_MAPPING_PATH = DATA_DIR / "feynman_kb_id_map.json" # Maps Annoy int index to reaction_id string
NUM_TREES = 10  # Default number of trees for Annoy index, consistent with build_ann_index

# Global cache for Annoy index and ID map
_annoy_index: Optional[AnnoyIndex] = None
_id_map: Optional[List[str]] = None # List of reaction_ids, index is Annoy's int ID
_reaction_to_annoy_id: Optional[Dict[str, int]] = None # Reverse map for quick lookups

def _initialize_index_and_map_from_files() -> None:
    """
    Initializes the Annoy index and ID map from files.
    If files don't exist, initializes empty structures.
    """
    global _annoy_index, _id_map, _reaction_to_annoy_id
    
    _annoy_index = AnnoyIndex(EMB_DIM, 'angular')
    
    if ANN_INDEX_PATH.exists():
        print(f"Loading Annoy index from {ANN_INDEX_PATH}...")
        _annoy_index.load(str(ANN_INDEX_PATH))
        print(f"Annoy index loaded with {_annoy_index.get_n_items()} items.")
    else:
        print(f"Annoy index file not found at {ANN_INDEX_PATH}. Initializing new index.")
        # Index is already initialized as empty

    if ID_MAPPING_PATH.exists():
        print(f"Loading ID map from {ID_MAPPING_PATH}...")
        with open(ID_MAPPING_PATH, 'r', encoding='utf-8') as f:
            _id_map = json.load(f)
        print(f"ID map loaded with {len(_id_map)} entries.")
    else:
        print(f"ID map file not found at {ID_MAPPING_PATH}. Initializing new empty map.")
        _id_map = []
    
    # Build reverse map
    _reaction_to_annoy_id = {reaction_id: i for i, reaction_id in enumerate(_id_map)}

    # Sanity check
    if _annoy_index.get_n_items() != len(_id_map):
        # This could happen if one file was updated and the other not, or corruption.
        # Forcing a rebuild or providing a warning might be necessary in a production system.
        print(f"Warning: Annoy index item count ({_annoy_index.get_n_items()}) "
              f"does not match ID map length ({len(_id_map)}). "
              "This may indicate inconsistency. Consider rebuilding the index.")
        # As a quick fix, we might trust the ID map's length if index is larger,
        # or rebuild. For now, just a warning.
        # If _id_map is shorter, Annoy items beyond len(_id_map) are unaddressable by reaction_id.

def get_index_and_map() -> Tuple[AnnoyIndex, List[str], Dict[str, int]]:
    """
    Returns the cached Annoy index, ID map (list), and reaction_id to Annoy_id map (dict).
    Initializes them from files if not already loaded.
    """
    global _annoy_index, _id_map, _reaction_to_annoy_id
    if _annoy_index is None or _id_map is None or _reaction_to_annoy_id is None:
        _initialize_index_and_map_from_files()
    return _annoy_index, _id_map, _reaction_to_annoy_id

def add_record_to_index(record: FeynmanRecord, build_immediately: bool = True) -> bool:
    """
    Adds a single record to the Annoy index and updates the ID map.
    The record's embedding must be available or generatable.
    The record's 'reaction' field is used as its unique ID in the map.
    Assumes that if a reaction_id already exists, its vector is being updated.
    """
    index, id_map, reaction_to_annoy_id_map = get_index_and_map()

    if not record.reaction:
        print("Error: Record must have a 'reaction' (ID) to be added to the index.")
        return False

    embedding_vector = record.embedding
    if not embedding_vector:
        print(f"Embedding not found in record '{record.reaction}'. Generating...")
        desc_for_embedding = record.description or record.reaction # Fallback to reaction if no description
        embedding_vector = get_embedding(desc_for_embedding)

    if not embedding_vector or len(embedding_vector) != EMB_DIM:
        print(f"Error: Could not get a valid embedding for record '{record.reaction}'. Cannot add to index.")
        return False

    annoy_item_id: Optional[int] = None
    if record.reaction in reaction_to_annoy_id_map:
        # This reaction ID already exists. Annoy does not support updating items directly.
        # The strategy here is to treat it as a new item if we must, or log a warning.
        # For true "upsert" behavior in Annoy, one typically rebuilds the index.
        # Given the "add_item; build; save" approach, we are essentially rebuilding.
        # However, Annoy's add_item takes an integer ID. If we reuse an existing Annoy int ID
        # with a new vector, it's an update. But we need to manage our id_map carefully.
        
        # Simplest for now: if ID exists, we can't "add" it again with add_item to get a *new* Annoy ID.
        # Annoy's `add_item(i, vector)` adds or updates vector for integer index `i`.
        # So, if reaction_id exists, we get its current Annoy int ID and update that vector.
        print(f"Reaction ID '{record.reaction}' already exists in Annoy map. Updating its vector.")
        annoy_item_id = reaction_to_annoy_id_map[record.reaction]
        # No change to id_map list itself or reaction_to_annoy_id_map needed for an update.
    else:
        # New reaction ID, get a new Annoy integer ID.
        annoy_item_id = len(id_map) # Next available Annoy integer ID
        id_map.append(record.reaction)
        reaction_to_annoy_id_map[record.reaction] = annoy_item_id
        print(f"Adding new reaction ID '{record.reaction}' to Annoy map with Annoy ID {annoy_item_id}.")

    try:
        # index.unbuild() # Necessary if index was already built and we want to add items
                        # However, if we load an index, it's ready for querying.
                        # To add items, it's often better to build a new index or manage carefully.
                        # The user's suggestion: add_item, build, save implies rebuilding.
        
        # If the index was loaded from a file, it's in a queryable state.
        # To add items and make them searchable, Annoy typically requires a rebuild.
        # If `index.build()` was called after loading, `add_item` might not be allowed without `unbuild()`.
        # Let's assume `_initialize_index_and_map_from_files` loads it, and we might need to `unbuild` if it's built.
        # However, `AnnoyIndex.load()` prepares it for querying. `add_item` can be called on an empty or partially filled index
        # *before* the first `build()`. If it's loaded and built, `add_item` is not allowed.
        # This implies we might need to rebuild from scratch or use a temporary index.

        # For simplicity, following user's "add_item; build; save" implies that `index` object
        # is either fresh or `unbuild()` has been called.
        # Let's ensure the index is "unbuilt" before adding if it's not empty.
        # This is tricky. A simpler model for "incremental" is to add to a list, then periodically rebuild ALL.
        # User's model: index.add_item(new_id, vec); index.build(10); index.save()
        # This means `index` object is THE live index.
        
        # If index has items and is "built" (i.e., loaded from a saved file),
        # we cannot simply add_item. We would need to unbuild, add, then build.
        # Unbuilding clears the index. So this means we'd have to re-add ALL items.
        # This is not incremental for Annoy's C++ object in memory.

        # Alternative: The user's `index.build(10)` after `add_item` suggests they expect
        # `add_item` to work on a loaded index, and then `build` finalizes it.
        # This is how you'd do it if you were building from scratch.
        # If `_annoy_index` was loaded, it's already "built".
        # `add_item` to a built index is an error.

        # Let's re-evaluate:
        # 1. Load existing index (it's built).
        # 2. To add an item:
        #    a. Create a NEW AnnoyIndex.
        #    b. Copy all items from old index to new index.
        #    c. Add the new item to the new index.
        #    d. Build the new index.
        #    e. Save the new index, replacing the old one.
        # This is effectively a full rebuild but managed here. This is safest.

        current_n_items = index.get_n_items()
        all_items_to_reindex = []
        for i in range(current_n_items):
            # Check if this item is the one being updated. If so, use the new vector.
            # Otherwise, use the old vector.
            existing_reaction_id = id_map[i]
            if existing_reaction_id == record.reaction: # This is the item being "updated"
                all_items_to_reindex.append(embedding_vector)
            else:
                all_items_to_reindex.append(index.get_item_vector(i))
        
        # If it's a truly new item (not an update of an existing one by reaction_id)
        if record.reaction not in reaction_to_annoy_id_map or reaction_to_annoy_id_map[record.reaction] >= current_n_items : # new item
             all_items_to_reindex.append(embedding_vector)
        
        # Now, rebuild the index from scratch with all_items_to_reindex
        index.unbuild() # Clear the current index structure
        
        # The id_map should now reflect the final list of reaction_ids to be indexed
        # If we added a new reaction to id_map, its length is now current_n_items + 1
        # If we updated, length is current_n_items.
        
        # Re-populate the index object
        for i, vector in enumerate(all_items_to_reindex):
            index.add_item(i, vector)
            # id_map should already be correct here based on previous logic.
            # If it was an update, id_map[i] is the reaction_id for vector.
            # If it was an add, id_map now includes the new reaction_id at the end.

        if build_immediately:
            print(f"Rebuilding Annoy index with {NUM_TREES} trees...")
            index.build(NUM_TREES)
            print("Annoy index rebuilt.")
            
            # Save immediately
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            index.save(str(ANN_INDEX_PATH))
            with open(ID_MAPPING_PATH, 'w', encoding='utf-8') as f:
                json.dump(id_map, f) # id_map has been updated in place
            print(f"Annoy index and ID map saved. Total items: {index.get_n_items()}")
        else:
            print("Record vector prepared for Annoy. Index will be built and saved later.")
        
        return True

    except Exception as e:
        print(f"Error adding record '{record.reaction}' to Annoy index: {e}")
        # Rollback id_map changes if it was a new item? Complex.
        # For now, if error, state might be inconsistent.
        return False

def search_vectors(query_embedding: List[float], k: int, search_k: int = -1) -> Optional[Tuple[List[str], List[float]]]:
    """
    Performs Annoy search and returns (list_of_reaction_ids, list_of_distances).
    """
    index, id_map, _ = get_index_and_map()
    if not index or index.get_n_items() == 0:
        print("Annoy index is not loaded or is empty.")
        return None

    if not query_embedding or len(query_embedding) != EMB_DIM:
        print(f"Invalid query embedding for Annoy search.")
        return None
    
    actual_k = min(k, index.get_n_items()) # Cannot get more items than exist

    try:
        neighbor_indices, distances = index.get_nns_by_vector(
            query_embedding, actual_k, search_k=search_k, include_distances=True
        )
        
        retrieved_reaction_ids = [id_map[i] for i in neighbor_indices]
        return retrieved_reaction_ids, distances
    except Exception as e:
        print(f"Error during Annoy vector search: {e}")
        return None

# For testing or direct use
if __name__ == '__main__':
    print("Testing Annoy Index utilities...")
    # This requires GOOGLE_API_KEY for get_embedding if records don't have embeddings.
    # Also requires existing feynman_kb.duckdb for get_record_by_id (if used).

    # Example: Create a dummy record
    # Ensure your schema and embedding functions are usable here
    try:
        # Initialize (loads or creates empty)
        idx, idm, r_to_a_idm = get_index_and_map()
        print(f"Initial index items: {idx.get_n_items()}, map size: {len(idm)}")

        # Test adding a record
        # For a real test, ensure FeynmanRecord can be instantiated and get_embedding works.
        # This part is highly dependent on your project structure being fully functional.
        print("\nAttempting to add a test record (requires working FeynmanRecord and get_embedding)...")
        # Placeholder: actual record creation would involve more details
        # from .embedding import get_embedding # Make sure this is callable
        # test_reaction_id = "test_reaction_001"
        # test_desc = "A test particle interaction"
        # test_embedding = get_embedding(test_desc)
        # if test_embedding:
        #     test_record = FeynmanRecord(
        #         reaction=test_reaction_id,
        #         description=test_desc,
        #         tikz="...", particles=[], topic="test", process_type="test",
        #         embedding=test_embedding # Store it if generated
        #     )
        #     if add_record_to_index(test_record):
        #         print(f"Record '{test_reaction_id}' added successfully.")
        #         idx, idm, r_to_a_idm = get_index_and_map() # Re-get to see changes
        #         print(f"New index items: {idx.get_n_items()}, new map size: {len(idm)}")
        #         
        #         # Test search
        #         search_results = search_vectors(test_embedding, k=1)
        #         if search_results:
        #             ids, dists = search_results
        #             print(f"Search found IDs: {ids} with distances: {dists}")
        #     else:
        #         print(f"Failed to add record '{test_reaction_id}'.")
        # else:
        #     print("Could not generate embedding for test record.")
        print("Skipping add/search test in __main__ as it requires full environment setup.")

    except Exception as e:
        print(f"Error in Annoy index test: {e}")

    print("\nAnnoy Index utilities test finished.")
