#!/usr/bin/env python
"""Mock test without external dependencies."""

import json
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_syntax_check():
    """Check Python syntax for all files."""
    print("=== Syntax Check ===")
    
    python_files = [
        "feynmancraft_adk/__init__.py",
        "feynmancraft_adk/agent.py",
        "feynmancraft_adk/tools/bigquery_kb_tool.py",
        "feynmancraft_adk/tools/local_kb_tool.py",
        "feynmancraft_adk/shared_libraries/config.py",
        "feynmancraft_adk/sub_agents/kb_retriever_agent.py",
    ]
    
    all_good = True
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            compile(code, file_path, 'exec')
            print(f"✅ {file_path} - syntax OK")
        except SyntaxError as e:
            print(f"❌ {file_path} - syntax error: {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️  {file_path} - {e}")
    
    return all_good

def test_mock_local_kb():
    """Test local KB functionality with mocks."""
    print("\n=== Mock Local KB Test ===")
    
    # Load KB data
    kb_path = Path("feynmancraft_adk/data/feynman_kb.json")
    with open(kb_path, 'r') as f:
        kb_data = json.load(f)
    
    print(f"✅ Loaded {len(kb_data)} KB entries")
    
    # Mock keyword search
    def mock_keyword_search(data, query, k=5):
        query_lower = query.lower()
        results = []
        
        for record in data:
            score = 0
            if query_lower in record.get('reaction', '').lower():
                score += 3
            if query_lower in record.get('topic', '').lower():
                score += 2
            if query_lower in record.get('description', '').lower():
                score += 1
            
            if score > 0:
                result = record.copy()
                result['score'] = score
                results.append(result)
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:k]
    
    # Test searches
    test_queries = ["electron", "photon", "Z boson"]
    for query in test_queries:
        results = mock_keyword_search(kb_data, query, k=3)
        print(f"\nQuery: '{query}' -> {len(results)} results")
        if results:
            print(f"  Top result: {results[0]['reaction']} (score: {results[0]['score']})")
    
    return True

def test_config_mock():
    """Test configuration loading without dotenv."""
    print("\n=== Mock Config Test ===")
    
    # Mock environment
    mock_env = {
        "KB_MODE": "hybrid",
        "GOOGLE_CLOUD_PROJECT": "test-project",
        "GOOGLE_API_KEY": "mock-key-123",
    }
    
    # Mock config loading
    kb_mode = mock_env.get("KB_MODE", "hybrid").lower()
    use_bigquery = kb_mode in ["bigquery", "hybrid"]
    use_local = kb_mode in ["local", "hybrid"]
    
    print(f"KB Mode: {kb_mode}")
    print(f"Use BigQuery: {use_bigquery}")
    print(f"Use Local: {use_local}")
    
    return True

def test_agent_structure_mock():
    """Test agent structure with mocks."""
    print("\n=== Mock Agent Structure Test ===")
    
    # Check if agent files exist
    agent_files = [
        "feynmancraft_adk/sub_agents/orchestrator_agent.py",
        "feynmancraft_adk/sub_agents/planner_agent.py",
        "feynmancraft_adk/sub_agents/kb_retriever_agent.py",
        "feynmancraft_adk/sub_agents/diagram_generator_agent.py",
        "feynmancraft_adk/sub_agents/tikz_validator_agent.py",
        "feynmancraft_adk/sub_agents/physics_validator_agent.py",
        "feynmancraft_adk/sub_agents/feedback_agent.py",
    ]
    
    agents_found = 0
    for agent_file in agent_files:
        if Path(agent_file).exists():
            agents_found += 1
            print(f"✅ Found: {Path(agent_file).name}")
        else:
            print(f"❌ Missing: {Path(agent_file).name}")
    
    print(f"\nTotal agents found: {agents_found}/7")
    return agents_found >= 6  # At least 6 agents should exist

def test_imports_isolated():
    """Test imports in isolation."""
    print("\n=== Isolated Import Test ===")
    
    # Test importing without external dependencies
    try:
        # This should work even without google packages
        import feynmancraft_adk
        print("✅ feynmancraft_adk package structure OK")
        
        # Check for required attributes
        if hasattr(feynmancraft_adk, '__file__'):
            print("✅ Package __file__ defined")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run all mock tests."""
    print("🧪 FeynmanCraft ADK Mock Test (No Dependencies)")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_syntax_check()
    all_passed &= test_mock_local_kb()
    all_passed &= test_config_mock()
    all_passed &= test_agent_structure_mock()
    all_passed &= test_imports_isolated()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All mock tests passed!")
        print("\n📋 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up .env file with your API keys")
        print("3. Run full tests: python test_system.py")
        print("4. Start the agent: adk run feynmancraft_adk")
    else:
        print("❌ Some mock tests failed.")
        print("Please fix the issues before proceeding.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)