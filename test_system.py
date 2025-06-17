#!/usr/bin/env python
"""System test for FeynmanCraft ADK."""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_imports():
    """Test that all modules can be imported."""
    print("=== Testing Imports ===")
    try:
        from feynmancraft_adk import agent
        print("✅ Main agent module imported successfully")
        
        from feynmancraft_adk.tools.local_kb_tool import LocalKBTool
        print("✅ Local KB tool imported successfully")
        
        from feynmancraft_adk.tools.bigquery_kb_tool import BigQueryKBTool
        print("✅ BigQuery KB tool imported successfully")
        
        from feynmancraft_adk.shared_libraries.config import get_kb_config
        print("✅ Config module imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("\n=== Testing Configuration ===")
    try:
        from feynmancraft_adk.shared_libraries.config import get_kb_config, validate_config
        
        config = get_kb_config()
        print(f"KB Mode: {config['mode']}")
        print(f"Use BigQuery: {config['use_bigquery']}")
        print(f"Use Local: {config['use_local']}")
        
        issues = validate_config()
        if issues:
            print("⚠️  Configuration issues:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("✅ Configuration valid")
        
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_local_kb():
    """Test local knowledge base functionality."""
    print("\n=== Testing Local KB ===")
    try:
        from feynmancraft_adk.tools.local_kb_tool import LocalKBTool
        
        tool = LocalKBTool()
        
        # Test keyword search
        print("Testing keyword search...")
        results = tool.keyword_search("electron", k=3)
        print(f"Found {len(results)} results")
        if results:
            print(f"First result: {results[0].get('reaction', 'N/A')}")
        
        # Check if index exists
        from feynmancraft_adk.shared_libraries.config import LOCAL_INDEX_PATH
        if LOCAL_INDEX_PATH.exists():
            print("✅ Vector index exists")
            
            # Test vector search if API key is available
            if tool.api_key:
                print("Testing vector search...")
                results = tool.vector_search("electron positron annihilation", k=3)
                print(f"Found {len(results)} results via vector search")
            else:
                print("⚠️  No API key for vector search")
        else:
            print("⚠️  Vector index not built yet")
            print("   Run: python scripts/build_local_index.py")
        
        return True
    except Exception as e:
        print(f"❌ Local KB error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_structure():
    """Test agent structure and sub-agents."""
    print("\n=== Testing Agent Structure ===")
    try:
        from feynmancraft_adk.agent import root_agent
        
        print(f"Root agent name: {root_agent.name}")
        print(f"Root agent model: {root_agent.model}")
        print(f"Number of sub-agents: {len(root_agent.sub_agents)}")
        
        for sub_agent in root_agent.sub_agents:
            print(f"  - {sub_agent.name}")
        
        print("✅ Agent structure looks good")
        return True
    except Exception as e:
        print(f"❌ Agent structure error: {e}")
        return False

def test_kb_retriever():
    """Test KB retriever agent functionality."""
    print("\n=== Testing KB Retriever ===")
    try:
        from feynmancraft_adk.sub_agents.kb_retriever_agent import search_tikz_examples
        
        # Test with local search only (to avoid BigQuery auth issues)
        print("Testing unified search (local mode)...")
        results = search_tikz_examples("electron positron", use_bigquery=False, k=3)
        
        if results:
            print(f"✅ Found {len(results)} results")
            print(f"First result: {results[0].get('reaction', 'N/A')}")
        else:
            print("⚠️  No results found (this might be normal)")
        
        return True
    except Exception as e:
        print(f"❌ KB Retriever error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 FeynmanCraft ADK System Test")
    print("=" * 50)
    
    # Check environment
    print("\n=== Environment Check ===")
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"✅ GOOGLE_API_KEY is set ({len(api_key)} chars)")
    else:
        print("⚠️  GOOGLE_API_KEY not set")
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        print(f"✅ GOOGLE_CLOUD_PROJECT: {project_id}")
    else:
        print("⚠️  GOOGLE_CLOUD_PROJECT not set")
    
    # Run tests
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_config()
    all_passed &= test_local_kb()
    all_passed &= test_agent_structure()
    all_passed &= test_kb_retriever()
    
    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed!")
        print("\nNext steps:")
        print("1. Build local index: python scripts/build_local_index.py")
        print("2. Upload to BigQuery: python scripts/upload_to_bigquery.py")
        print("3. Run the agent: adk run feynmancraft_adk")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()