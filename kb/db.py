# Database operations (CRUD)
import duckdb
import json
from pathlib import Path
from typing import List, Optional

# Relative import for the schema
from .schema import FeynmanRecord

# Define the database file path within the 'data' directory
# Ensure 'data' directory exists or is created before running.
DB_FILE_PATH = Path("data/feynman_kb.duckdb")

def init_db():
    """Initializes the DuckDB database and the 'feynman' table if they don't exist."""
    DB_FILE_PATH.parent.mkdir(parents=True, exist_ok=True) # Ensure data directory exists
    con = duckdb.connect(str(DB_FILE_PATH), read_only=False)
    con.sql("""
        CREATE TABLE IF NOT EXISTS feynman (
            topic TEXT,
            reaction TEXT PRIMARY KEY,
            particles TEXT,          -- JSON string array
            description TEXT,
            tikz TEXT,
            process_type TEXT,
            source TEXT,
            embedding BLOB           -- DuckDB can store VECTOR type, but BLOB is simpler for now if storing raw bytes of list.
                                     -- Or use LIST type if DuckDB version supports it well for this.
                                     -- For simplicity with sentence-transformers output (list of floats),
                                     -- storing as JSON string or converting to bytes might be needed if not using native VECTOR.
                                     -- User's schema had BLOB, let's stick to that. Embeddings will be List[float].
                                     -- We'll need to serialize List[float] to bytes (e.g., using struct or json+encode)
                                     -- or store as JSON string if BLOB is problematic for direct list storage.
                                     -- Given DuckDB's flexibility, let's try storing as a LIST of FLOATs directly if possible,
                                     -- or fallback to JSON string for the 'embedding' column.
                                     -- The user's schema used BLOB. For List[float], this usually means serializing.
                                     -- Let's try DuckDB's LIST type for embeddings.
                                     -- Rechecking user's DDL: embedding BLOB. This implies serialization.
                                     -- Simplest serialization for List[float] to BLOB is via JSON string then encode to bytes.
    );""")
    # Add a vector type if we want native vector operations later, for now BLOB as per user.
    # Example for vector type (requires vector extension usually):
    # con.sql("CREATE EXTENSION IF NOT EXISTS vector;")
    # con.sql("ALTER TABLE feynman ADD COLUMN embedding_vector FLOAT[768];")
    con.close()
    print(f"Database initialized at {DB_FILE_PATH}")

def _serialize_embedding(embedding: Optional[List[float]]) -> Optional[bytes]:
    """Serializes a list of floats (embedding) to bytes via JSON string."""
    if embedding is None:
        return None
    return json.dumps(embedding).encode('utf-8')

def _deserialize_embedding(embedding_blob: Optional[bytes]) -> Optional[List[float]]:
    """Deserializes bytes (from BLOB) back to a list of floats via JSON string."""
    if embedding_blob is None:
        return None
    return json.loads(embedding_blob.decode('utf-8'))

def upsert_record(record: FeynmanRecord):
    """Inserts or replaces a FeynmanRecord into the database."""
    con = duckdb.connect(str(DB_FILE_PATH), read_only=False)
    
    # Ensure particles list is stored as a JSON string
    particles_json = json.dumps(record.particles)
    embedding_blob = _serialize_embedding(record.embedding)

    con.execute(
        "INSERT OR REPLACE INTO feynman (topic, reaction, particles, description, tikz, process_type, source, embedding) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            record.topic,
            record.reaction,
            particles_json,
            record.description,
            record.tikz,
            record.process_type,
            record.source,
            embedding_blob, # Store serialized embedding
        ),
    )
    con.close()

def query_records_by_description(text: str, k: int = 5) -> List[FeynmanRecord]:
    """Queries records by description using ILIKE (case-insensitive LIKE)."""
    con = duckdb.connect(str(DB_FILE_PATH), read_only=True)
    # The query from user was: "SELECT * FROM feynman WHERE description ILIKE ? LIMIT ?"
    # Need to map table columns back to FeynmanRecord fields, especially 'particles' and 'embedding'.
    
    # Fetch all columns including the blob
    rows = con.sql(
        "SELECT topic, reaction, particles, description, tikz, process_type, source, embedding FROM feynman WHERE description ILIKE ? LIMIT ?", 
        params=["%" + text + "%", k] # Pass parameters as a named argument
    ).fetchall()
    con.close()

    results = []
    for row_data in rows:
        # Assuming column order matches select: topic, reaction, particles, description, tikz, process_type, source, embedding_blob
        record_dict = {
            "topic": row_data[0],
            "reaction": row_data[1],
            "particles": json.loads(row_data[2]), # particles stored as JSON string
            "description": row_data[3],
            "tikz": row_data[4],
            "process_type": row_data[5],
            "source": row_data[6],
            "embedding": _deserialize_embedding(row_data[7]) # Deserialize embedding from BLOB
        }
        results.append(FeynmanRecord(**record_dict))
    return results

if __name__ == '__main__':
    # Basic test for db operations
    print("Testing DB operations...")
    init_db()

    # Sample record
    sample_particles = ["e-", "gamma"]
    sample_embedding_data = [0.1] * 768 # Dummy embedding of correct dimension

    test_record = FeynmanRecord(
        topic="QED Test",
        reaction="e- -> e- gamma (test)",
        particles=sample_particles,
        description="Test electron emitting a photon.",
        tikz="\\feynmandiagram { test };",
        process_type="Emission Test",
        source="db.py test",
        embedding=sample_embedding_data
    )
    
    print(f"Upserting test record: {test_record.reaction}")
    upsert_record(test_record)
    print("Upsert complete.")

    print("\nQuerying for 'Test electron':")
    queried_records = query_records_by_description("Test electron", k=1)
    if queried_records:
        retrieved_record = queried_records[0]
        print(f"  Found record: {retrieved_record.reaction}")
        print(f"  Description: {retrieved_record.description}")
        print(f"  Particles: {retrieved_record.particles}")
        print(f"  Embedding (first 5 dims): {retrieved_record.embedding[:5] if retrieved_record.embedding else None}")
        assert retrieved_record.reaction == test_record.reaction
        assert retrieved_record.particles == sample_particles
        assert retrieved_record.embedding is not None and len(retrieved_record.embedding) == 768
    else:
        print("  No records found by query.")

    # Test with None embedding
    test_record_no_emb = FeynmanRecord(
        topic="QED Test No Emb",
        reaction="gamma -> e- e+ (test no emb)",
        particles=["gamma", "e-", "e+"],
        description="Test photon pair production no embedding.",
        tikz="\\feynmandiagram { test no emb };",
        process_type="Pair Production Test",
        source="db.py test no emb",
        embedding=None
    )
    print(f"\nUpserting test record with no embedding: {test_record_no_emb.reaction}")
    upsert_record(test_record_no_emb)
    queried_no_emb = query_records_by_description("photon pair production no embedding", k=1)
    if queried_no_emb:
        retrieved_no_emb = queried_no_emb[0]
        print(f"  Found record: {retrieved_no_emb.reaction}")
        print(f"  Embedding: {retrieved_no_emb.embedding}")
        assert retrieved_no_emb.embedding is None
    else:
        print("  No records found for no_emb test.")
        
    print("\nDB operations test complete.")
