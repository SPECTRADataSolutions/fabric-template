"""Discover Zephyr Test Repository folder tree structure.

Understanding the folder tree is critical for:
1. Creating testcases (requires tcrCatalogTreeId)
2. Organizing testcases in SpectraTestProject
3. Understanding the browser UI structure
"""
import requests
import json
import sys
from pathlib import Path

# Add scripts directory to path for imports
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir.parent))

from scripts.zephyr_utils import get_test_project_id, get_api_credentials

# Get credentials and project ID
api_token, base_url, base_path, full_url = get_api_credentials()
project_id = get_test_project_id()

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

output_dir = Path(__file__).parent.parent / "docs" / "schemas" / "discovered"
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("🌲 DISCOVERING TEST REPOSITORY FOLDER TREE")
print("=" * 80)
print(f"Project ID: {project_id}\n")

# Get the complete Test Repository tree for the project
print("1️⃣ Getting Project Repository Testcase Tree...")
print(f"   GET /testcasetree/projectrepository/{project_id}")

try:
    tree_response = requests.get(
        f"{full_url}/testcasetree/projectrepository/{project_id}",
        headers=headers,
        timeout=10
    )
    tree_response.raise_for_status()
    
    tree_data = tree_response.json()
    
    # Save raw response
    tree_file = output_dir / "test_repository_tree.json"
    with open(tree_file, "w") as f:
        json.dump(tree_data, f, indent=2)
    
    print(f"   ✅ Tree retrieved")
    print(f"   💾 Saved to: {tree_file}\n")
    
    # Analyze structure
    if isinstance(tree_data, list) and tree_data:
        print(f"   📊 Tree contains {len(tree_data)} root nodes")
        print(f"   Sample structure preview:")
        print(json.dumps(tree_data[0] if len(tree_data) > 0 else tree_data, indent=2)[:500])
    elif isinstance(tree_data, dict):
        print(f"   📊 Tree structure:")
        print(json.dumps(tree_data, indent=2)[:500])
    
except requests.exceptions.HTTPError as e:
    print(f"   ❌ HTTP Error: {e.response.status_code}")
    print(f"   Response: {e.response.text[:300]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Get TCR hierarchy
print("\n2️⃣ Getting TCR Hierarchy...")
print(f"   GET /testcasetree/hierarchy")

try:
    hierarchy_response = requests.get(
        f"{full_url}/testcasetree/hierarchy",
        headers=headers,
        timeout=10
    )
    hierarchy_response.raise_for_status()
    
    hierarchy_data = hierarchy_response.json()
    
    # Save raw response
    hierarchy_file = output_dir / "tcr_hierarchy.json"
    with open(hierarchy_file, "w") as f:
        json.dump(hierarchy_data, f, indent=2)
    
    print(f"   ✅ Hierarchy retrieved")
    print(f"   💾 Saved to: {hierarchy_file}\n")
    print(json.dumps(hierarchy_data, indent=2)[:500])
    
except requests.exceptions.HTTPError as e:
    print(f"   ❌ HTTP Error: {e.response.status_code}")
    print(f"   Response: {e.response.text[:300]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Try to get requirements to understand the top-level structure
print("\n3️⃣ Getting Requirements (for context)...")
print(f"   GET /requirement/project/{project_id}")

try:
    req_response = requests.get(
        f"{full_url}/requirement/project/{project_id}",
        headers=headers,
        timeout=10
    )
    if req_response.status_code == 200:
        req_data = req_response.json()
        
        req_file = output_dir / "requirements_sample.json"
        with open(req_file, "w") as f:
            json.dump(req_data, f, indent=2)
        
        print(f"   ✅ Requirements retrieved")
        if isinstance(req_data, list):
            print(f"   📊 Found {len(req_data)} requirements")
        print(f"   💾 Saved to: {req_file}\n")
    else:
        print(f"   ⚠️ Status: {req_response.status_code}")
        print(f"   Response: {req_response.text[:300]}\n")
        
except Exception as e:
    print(f"   ⚠️ Error: {e}\n")

print("=" * 80)
print("✅ Folder Tree Discovery Complete")
print("=" * 80)
print(f"📁 All schemas saved to: {output_dir}\n")

