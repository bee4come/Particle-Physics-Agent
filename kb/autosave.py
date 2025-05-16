# kb/autosave.py
import json
import threading
import time
import atexit
from pathlib import Path
from typing import List, Dict, Any
from .schema import FeynmanRecord # Assuming FeynmanRecord has a model_dump() method like Pydantic

DATA_DIR = Path("data")
USER_KB_DELTA_FILE = DATA_DIR / "feynman_kb_user.json"
AUTOSAVE_INTERVAL_SECONDS = 600  # 10 minutes

_pending_records: List[FeynmanRecord] = []
_lock = threading.Lock() # To protect access to _pending_records

def queue_record_for_autosave(record: FeynmanRecord) -> None:
    """Adds a record to the pending list for the next autosave."""
    with _lock:
        _pending_records.append(record)
    print(f"Record '{record.reaction}' queued for autosave. Pending count: {len(_pending_records)}")

def _flush_pending_records_to_json() -> None:
    """
    Writes all pending records to the feynman_kb_user.json file.
    This function is intended to be called by the autosave thread or at exit.
    """
    with _lock:
        if not _pending_records:
            # print("Autosave: No pending records to flush.")
            return

        print(f"Autosave: Flushing {len(_pending_records)} pending records to {USER_KB_DELTA_FILE}...")
        
        DATA_DIR.mkdir(parents=True, exist_ok=True) # Ensure data directory exists
        
        existing_records_data: List[Dict[str, Any]] = []
        if USER_KB_DELTA_FILE.exists():
            try:
                with open(USER_KB_DELTA_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip(): # Ensure file is not empty or just whitespace
                        existing_records_data = json.loads(content)
                    if not isinstance(existing_records_data, list):
                        print(f"Warning: Content of {USER_KB_DELTA_FILE} is not a list. Initializing as empty list.")
                        existing_records_data = []
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {USER_KB_DELTA_FILE}. File might be corrupted. Initializing as empty list.")
                existing_records_data = []
            except Exception as e:
                print(f"Error reading {USER_KB_DELTA_FILE}: {e}. Initializing as empty list.")
                existing_records_data = []
        
        # Convert pending FeynmanRecord objects to dictionaries for JSON serialization
        # Using model_dump if it's a Pydantic model, otherwise assuming asdict or similar.
        new_records_data = []
        for rec in _pending_records:
            if hasattr(rec, 'model_dump'):
                new_records_data.append(rec.model_dump(exclude_none=True, mode='json'))
            else:
                # Fallback if not a Pydantic model, this might need adjustment
                new_records_data.append(vars(rec)) 

        all_records_data = existing_records_data + new_records_data
        
        try:
            with open(USER_KB_DELTA_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_records_data, f, ensure_ascii=False, indent=2)
            print(f"Autosave: Successfully flushed {len(new_records_data)} new records. Total records in {USER_KB_DELTA_FILE}: {len(all_records_data)}.")
            _pending_records.clear()
        except Exception as e:
            print(f"Autosave: Error writing to {USER_KB_DELTA_FILE}: {e}")
            # Do not clear pending records if write failed, so they can be retried.

def _autosave_daemon_loop():
    """Periodically calls _flush_pending_records_to_json."""
    while True:
        time.sleep(AUTOSAVE_INTERVAL_SECONDS)
        print(f"Autosave daemon: Interval reached. Attempting to flush records...")
        _flush_pending_records_to_json()

# Register flush at exit
atexit.register(_flush_pending_records_to_json)
print("Autosave: _flush_pending_records_to_json registered with atexit.")

# Start the autosave daemon thread
# It's a daemon so it won't prevent the program from exiting if it's the only thread left.
_daemon_thread = threading.Thread(target=_autosave_daemon_loop, daemon=True)
_daemon_thread.start()
print(f"Autosave: Background daemon thread started. Interval: {AUTOSAVE_INTERVAL_SECONDS}s.")

if __name__ == '__main__':
    # Test autosave functionality
    print("Testing autosave module...")
    print(f"Records will be saved to: {USER_KB_DELTA_FILE}")
    print(f"Autosave interval: {AUTOSAVE_INTERVAL_SECONDS} seconds (for daemon). Manual flush on exit.")

    # Create some dummy records for testing
    # Ensure FeynmanRecord can be instantiated correctly
    try:
        test_rec1 = FeynmanRecord(reaction="test_reaction_autosave_1", description="Test desc 1", tikz="tikz1", particles=["e-"], topic="test", process_type="vertex")
        test_rec2 = FeynmanRecord(reaction="test_reaction_autosave_2", description="Test desc 2", tikz="tikz2", particles=["p"], topic="test", process_type="decay")
        
        queue_record_for_autosave(test_rec1)
        queue_record_for_autosave(test_rec2)
        
        print("Queued 2 test records. They should be flushed on exit, or by the daemon if it runs long enough.")
        # To test daemon, you might need to let this script run for AUTOSAVE_INTERVAL_SECONDS
        # For a quick test, rely on atexit.
        # time.sleep(AUTOSAVE_INTERVAL_SECONDS + 5) # Uncomment to test daemon during script run

    except Exception as e:
        print(f"Error during autosave test setup: {e}")
        print("Please ensure FeynmanRecord schema is correctly defined and importable.")
    
    print("Autosave test script finished. Check console for flush messages on exit.")
