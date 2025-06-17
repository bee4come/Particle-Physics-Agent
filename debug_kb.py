#!/usr/bin/env python3
"""
Debug script for KB Retriever Agent issues.
"""

import sys
import os
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_environment():
    """Test environment setup."""
    print("=== Environment Test ===")
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"✓ GOOGLE_API_KEY found (length: {len(api_key)})")
        # Don't print full key for security
        print(f"  Starts with: {api_key[:10]}...")
    else:
        print("✗ GOOGLE_API_KEY not found")
        return False
    
    # Check data files
    data_dir = project_root / "feynmancraft_adk" / "data"
    kb_file = data_dir / "feynman_kb.json"
    
    if kb_file.exists():
        print(f"✓ KB file found: {kb_file}")
        # Check file size
        size = kb_file.stat().st_size
        print(f"  Size: {size} bytes")
    else:
        print(f"✗ KB file not found: {kb_file}")
        return False
    
    return True

def test_local_kb_tool():
    """Test LocalKBTool functionality."""
    print("\n=== LocalKBTool Test ===")
    
    try:
        from feynmancraft_adk.tools.local_kb_tool import LocalKBTool
        
        # Initialize tool
        print("Initializing LocalKBTool...")
        tool = LocalKBTool()
        
        # Test API connection
        print("Testing embedding generation...")
        test_text = "electron positron annihilation"
        embedding = tool.get_embedding(test_text)
        
        if embedding:
            print(f"✓ Embedding generated (dimension: {len(embedding)})")
        else:
            print("✗ Failed to generate embedding")
            return False
        
        # Test keyword search (no embedding required)
        print("Testing keyword search...")
        results = tool.keyword_search("electron", k=3)
        print(f"✓ Keyword search returned {len(results)} results")
        
        for i, result in enumerate(results[:2]):
            print(f"  {i+1}. {result.get('reaction', 'N/A')}")
        
        # Test hybrid search
        print("Testing hybrid search...")
        results = tool.hybrid_search("Z boson decay", k=3)
        print(f"✓ Hybrid search returned {len(results)} results")
        
        return True
        
    except Exception as e:
        print(f"✗ LocalKBTool test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_bigquery_tool():
    """Test BigQueryKBTool functionality."""
    print("\n=== BigQueryKBTool Test ===")
    
    try:
        from feynmancraft_adk.tools.bigquery_kb_tool import BigQueryKBTool
        
        print("Initializing BigQueryKBTool...")
        tool = BigQueryKBTool()
        
        # This will likely fail due to credentials, but let's see
        print("Testing semantic search...")
        results = tool.semantic_search("gluon")
        print(f"BigQuery search returned {len(results)} results")
        
        return True
        
    except Exception as e:
        print(f"✗ BigQuery test failed (expected): {e}")
        return False

def test_kb_retriever_agent():
    """Test KB Retriever Agent directly."""
    print("\n=== KB Retriever Agent Test ===")
    
    try:
        from feynmancraft_adk.sub_agents.kb_retriever_agent import search_tikz_examples
        
        print("Testing search_tikz_examples function...")
        
        # Test with BigQuery disabled (should use local)
        results = search_tikz_examples("gluon splitting", use_bigquery=False, k=3)
        print(f"✓ Local search returned {len(results)} results")
        
        for i, result in enumerate(results[:2]):
            print(f"  {i+1}. {result.get('reaction', 'N/A')} ({result.get('source_type', 'unknown')})")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"✗ KB Retriever Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic tests."""
    print("KB Retriever Agent Diagnostic Tool")
    print("=" * 40)
    
    tests = [
        ("Environment", test_environment),
        ("LocalKBTool", test_local_kb_tool),
        ("BigQueryKBTool", test_bigquery_tool),
        ("KB Retriever Agent", test_kb_retriever_agent),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results[test_name] = False
    
    print("\n=== Summary ===")
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    if not any(results.values()):
        print("\nAll tests failed. Check the error messages above.")
        return 1
    elif results.get("KB Retriever Agent", False):
        print("\nKB Retriever Agent is working!")
        return 0
    else:
        print("\nSome tests failed, but core functionality may still work.")
        return 0

if __name__ == "__main__":
    sys.exit(main())