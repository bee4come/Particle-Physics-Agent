# scripts/ci_check_embeddings.py
import duckdb
from pathlib import Path
import sys

DB_FILE_PATH = Path("data/feynman_kb.duckdb")
MIN_EMBEDDING_COVERAGE_RATIO = 0.9 # At least 90% of records should have embeddings

def check_embedding_coverage():
    if not DB_FILE_PATH.exists():
        print(f"Error: Database file not found at {DB_FILE_PATH}")
        sys.exit(1)

    con = None
    try:
        con = duckdb.connect(str(DB_FILE_PATH), read_only=True)
        
        total_records_result = con.execute("SELECT COUNT(*) FROM feynman").fetchone()
        if total_records_result is None or total_records_result[0] is None:
            print("Error: Could not get total record count from database.")
            sys.exit(1)
        total_records = total_records_result[0]

        if total_records == 0:
            print("Warning: Database contains no records. Skipping embedding coverage check.")
            # Depending on CI requirements, this might be an error or a pass.
            # For now, let's consider it a pass if the migration ran but produced no records from an empty JSON.
            # However, our feynman_kb_enhanced.json has 48 records. So this should be an error.
            print("Error: Database is empty after migration, expected records.")
            sys.exit(1)

        embedded_records_result = con.execute("SELECT COUNT(*) FROM feynman WHERE embedding IS NOT NULL").fetchone()
        if embedded_records_result is None or embedded_records_result[0] is None:
            print("Error: Could not get embedded record count from database.")
            sys.exit(1)
        embedded_records = embedded_records_result[0]

        coverage = embedded_records / total_records
        print(f"Total records: {total_records}")
        print(f"Records with embeddings: {embedded_records}")
        print(f"Embedding coverage: {coverage:.2%}")

        if coverage < MIN_EMBEDDING_COVERAGE_RATIO:
            print(f"Error: Embedding coverage ({coverage:.2%}) is below the threshold of {MIN_EMBEDDING_COVERAGE_RATIO:.0%}.")
            sys.exit(1)
        else:
            print(f"Success: Embedding coverage ({coverage:.2%}) meets or exceeds the threshold.")
            sys.exit(0)

    except Exception as e:
        print(f"An error occurred during embedding check: {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    check_embedding_coverage()
