#!/usr/bin/env python
"""Build local vector search index for FeynmanCraft knowledge base."""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from feynmancraft_adk.tools.local_kb_tool import LocalKBTool


def main():
    """Build the local vector search index."""
    print("=== FeynmanCraft Local Index Builder ===")
    print()
    
    # Initialize tool
    tool = LocalKBTool()
    
    # Check if we have API key for embeddings
    if not tool.api_key:
        print("WARNING: No GOOGLE_API_KEY found in environment.")
        print("Vector search will not be available without embeddings.")
        print("Please set GOOGLE_API_KEY in your .env file.")
        return
    
    # Build index
    print("Building vector search index...")
    print("This may take a few minutes depending on the size of your knowledge base.")
    print()
    
    try:
        tool.build_index(force_rebuild=True)
        print("\n✅ Index built successfully!")
        print("\nYou can now use vector search in the KBRetrieverAgent.")
        
    except Exception as e:
        print(f"\n❌ Error building index: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()