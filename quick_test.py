#!/usr/bin/env python
"""Quick test without external dependencies."""

import json
from pathlib import Path

def test_project_structure():
    """Test basic project structure."""
    print("=== Testing Project Structure ===")
    
    required_files = [
        "feynmancraft_adk/__init__.py",
        "feynmancraft_adk/agent.py",
        "feynmancraft_adk/data/feynman_kb.json",
        "feynmancraft_adk/tools/bigquery_kb_tool.py",
        "feynmancraft_adk/tools/local_kb_tool.py",
        "feynmancraft_adk/shared_libraries/config.py",
        "scripts/upload_to_bigquery.py",
        "scripts/build_local_index.py",
        "requirements.txt",
        ".env.example",
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_kb_data():
    """Test knowledge base data file."""
    print("\n=== Testing KB Data ===")
    
    kb_path = Path("feynmancraft_adk/data/feynman_kb.json")
    if not kb_path.exists():
        print("❌ KB data file not found")
        return False
    
    try:
        with open(kb_path, 'r') as f:
            data = json.load(f)
        
        print(f"✅ KB data loaded: {len(data)} entries")
        
        # Check first entry structure
        if data:
            first = data[0]
            required_fields = ["topic", "reaction", "particles", "description", "tikz"]
            for field in required_fields:
                if field in first:
                    print(f"  ✅ Field '{field}' present")
                else:
                    print(f"  ❌ Field '{field}' missing")
        
        return True
    except Exception as e:
        print(f"❌ Error loading KB data: {e}")
        return False

def test_imports_basic():
    """Test basic Python imports."""
    print("\n=== Testing Basic Imports ===")
    
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        
        # Test importing main module
        import feynmancraft_adk
        print("✅ feynmancraft_adk package imported")
        
        # Check MODEL is defined
        if hasattr(feynmancraft_adk, 'MODEL'):
            print(f"✅ MODEL defined: {feynmancraft_adk.MODEL}")
        else:
            print("⚠️  MODEL not defined in __init__.py")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run quick tests."""
    print("🚀 FeynmanCraft ADK Quick Test")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_project_structure()
    all_passed &= test_kb_data()
    all_passed &= test_imports_basic()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ Basic structure tests passed!")
    else:
        print("❌ Some tests failed.")
    
    print("\n📋 Requirements to install:")
    print("pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    main()