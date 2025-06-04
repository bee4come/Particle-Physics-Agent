# Embedding generation logic using Gemini
import os
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

from .schema import FeynmanRecord # Relative import

# Unified Embedding Dimension
EMB_DIM = 768


# Default Gemini embedding model to be used if not overridden by .env
# User confirmed text-embedding-004 works and is 768d.
# User's patch also used "gemini-embedding-001" as a default in its example.
# Let's make it configurable via .env, defaulting to text-embedding-004.
DEFAULT_GEMINI_EMBEDDING_MODEL = "text-embedding-004" 

def embed_with_gemini(text: str, api_key: str, model_name: Optional[str] = None) -> Optional[List[float]]:
    """Generates embedding using Gemini API via google-generativeai SDK (>=0.5.0)."""
    
    eff_model_name = model_name or os.getenv("GEMINI_EMBEDDING_MODEL_NAME", DEFAULT_GEMINI_EMBEDDING_MODEL)
    
    # Ensure model name includes "models/" prefix if not already present, as required by genai.embed_content
    if not eff_model_name.startswith("models/"):
        api_model_name = f"models/{eff_model_name}"
    else:
        api_model_name = eff_model_name

    try:
        # Configure API key (ideally done once globally, but doing it here for encapsulation per call for now)
        genai.configure(api_key=api_key)
        
        print(f"Attempting Gemini embedding with model '{api_model_name}'...")
        response = genai.embed_content(
            model=api_model_name, 
            content=text, 
            task_type="RETRIEVAL_DOCUMENT" # A common task type; others include "similarity", "classification"
        )
        
        vec = response.get("embedding") # SDK >=0.5.0 returns a dict like {'embedding': [values]}
        if vec and isinstance(vec, list):
            if len(vec) == EMB_DIM:
                return vec
            else:
                print(f"[WARN] Gemini model '{api_model_name}' returned embedding of dimension {len(vec)}, expected {EMB_DIM}.")
                return None
        else:
            print(f"[WARN] Gemini embedding response for model '{api_model_name}' did not contain expected 'embedding' list. Response: {response}")
            return None
    except Exception as e:
        print(f"[WARN] Gemini embedding with model '{api_model_name}' failed: {e}")
        return None

def get_embedding(text: str) -> Optional[List[float]]:
    """Generates an embedding using Gemini API."""
    if not text:
        return None

    api_key = os.getenv("GOOGLE_API_KEY")
    model_to_use = os.getenv("GEMINI_EMBEDDING_MODEL_NAME", DEFAULT_GEMINI_EMBEDDING_MODEL)
    if not api_key:
        print("GOOGLE_API_KEY not found. Cannot generate embedding.")
        return None

    vec = embed_with_gemini(text, api_key, model_name=model_to_use)
    if vec is None:
        print(f"[ERROR] Gemini embedding failed for text: \"{text[:50]}...\"")
    return vec

def enrich_record_with_embedding(record: FeynmanRecord) -> FeynmanRecord:
    """
    Enriches a FeynmanRecord with an embedding if it doesn't already have one.
    The embedding is generated based on the record's description or reaction.
    """
    if record.embedding is None:
        text_to_embed = record.description or record.reaction # Prioritize description
        if text_to_embed:
            record.embedding = get_embedding(text_to_embed)
        else:
            print(f"Warning: No description or reaction found for record {record.reaction} to generate embedding.")
    return record

if __name__ == "__main__":
    load_dotenv() 
    print("Testing embedding functions with Gemini API...")
    
    sample_text_for_test = "An electron and a positron annihilate to produce two photons."
    
    api_key_present = os.getenv("GOOGLE_API_KEY")

    if api_key_present:
        print(f"\nTesting Gemini embedding (model from env or default '{DEFAULT_GEMINI_EMBEDDING_MODEL}'):")
        gemini_emb_test = get_embedding(sample_text_for_test)
        if gemini_emb_test:
            print(f"  Gemini Embedding (first 5 dims): {gemini_emb_test[:5]}")
            print(f"  Gemini Embedding dimension: {len(gemini_emb_test)}")
        else:
            print("  Gemini embedding test failed or API key not configured properly.")
    else:
        print("\nGOOGLE_API_KEY not found in .env. Skipping embedding test.")


    print("\nTesting enrich_record_with_embedding:")
    test_record_data_for_enrich = {
        "topic": "QED", "reaction": "e- e+ -> gamma gamma (enrich test)",
        "particles": ["e-", "e+", "gamma"], "description": sample_text_for_test,
        "tikz": "\\feynmandiagram {};", "process_type": "Annihilation"
    }
    record_to_enrich_test = FeynmanRecord(**test_record_data_for_enrich)
    print(f"  Record before enrichment (embedding): {record_to_enrich_test.embedding}")
    enriched_record_test = enrich_record_with_embedding(record_to_enrich_test)
    if enriched_record_test.embedding:
        print(f"  Record after enrichment (embedding first 5 dims): {enriched_record_test.embedding[:5]}")
        print(f"  Enriched embedding dimension: {len(enriched_record_test.embedding)}")
    else:
        print("  Enrichment resulted in no embedding.")
