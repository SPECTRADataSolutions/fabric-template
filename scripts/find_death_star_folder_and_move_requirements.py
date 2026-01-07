#!/usr/bin/env python3
"""
Find "The Death Star Project" folder ID and move requirements to it.

Current issue:
- Requirements are under "REQ-001: Core Reactor Stabilit..." (Folder ID: 698)
- Should be under "The Death Star Project" folder

Steps:
1. Get requirement tree to find "The Death Star Project" folder ID
2. Update requirements to move them to correct folder
"""
import requests
import json
from pathlib import Path

# Get API credentials
spectra_root = Path(__file__).parent.parent.parent.parent
env_file = spectra_root / ".env"

api_token = None
if env_file.exists():
    with open(env_file, "r") as f:
        for line in f:
            if line.startswith("ZEPHYR_API_TOKEN=") or line.startswith("SPECTRA_ZEPHYR_API_TOKEN="):
                api_token = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

if not api_token:
    var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
    if var_lib_path.exists():
        with open(var_lib_path, "r") as f:
            var_lib = json.load(f)
            for var in var_lib.get("variables", []):
                if var.get("name") == "API_TOKEN":
                    api_token = var.get("value")
                    break

if not api_token:
    print("ERROR: API token not found")
    exit(1)

base_url = "https://velonetic.yourzephyr.com"
base_path = "/flex/services/rest/latest"
full_url = f"{base_url}{base_path}"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

test_project_id = 45
requirement_ids = [6455, 6456, 6457]  # REQ-DS-001, REQ-DS-002, REQ-DS-003
current_folder_id = 698  # "REQ-001: Core Reactor Stabilit..."

print("=" * 80)
print("FINDING DEATH STAR FOLDER AND MOVING REQUIREMENTS")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"Current folder ID: {current_folder_id} (REQ-001: Core Reactor Stabilit...)")
print(f"Requirements to move: {requirement_ids}")
print()

# Step 1: Get requirement tree to find "The Death Star Project" folder
print("1. Getting requirement tree to find 'The Death Star Project' folder...")
tree_endpoints = [
    f"/requirementtree/project/{test_project_id}",
    f"/requirementtree/project/{test_project_id}/",
    f"/requirementtree/{test_project_id}",
]

death_star_folder_id = None
tree_data = None

for endpoint in tree_endpoints:
    url = f"{full_url}{endpoint}"
    print(f"   Trying: {endpoint}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            tree_data = response.json()
            print(f"   ✅ SUCCESS: Retrieved requirement tree")
            
            # Search for "Death Star" in tree
            def find_folder(nodes, target_name):
                if isinstance(nodes, list):
                    for node in nodes:
                        result = find_folder(node, target_name)
                        if result:
                            return result
                elif isinstance(nodes, dict):
                    name = nodes.get("name", "")
                    if target_name.lower() in name.lower():
                        return nodes.get("id"), nodes
                    if "children" in nodes:
                        result = find_folder(nodes["children"], target_name)
                        if result:
                            return result
                return None
            
            result = find_folder(tree_data, "Death Star")
            if result:
                death_star_folder_id, folder_data = result
                print(f"   ✅ Found: '{folder_data.get('name')}' (ID: {death_star_folder_id})")
                break
            else:
                print(f"   ⚠️ 'Death Star' folder not found in tree")
                print(f"   Tree structure (first 500 chars):")
                print(json.dumps(tree_data, indent=2)[:500])
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if not death_star_folder_id:
    print("\n⚠️ Could not find 'The Death Star Project' folder")
    print("   Options:")
    print("   1. Create the folder via UI first")
    print("   2. Use existing folder ID if you know it")
    print("   3. Keep requirements where they are for now")
    exit(1)

print(f"\n2. Moving requirements to folder ID: {death_star_folder_id}...")

# Step 2: Update each requirement to move to correct folder
for req_id in requirement_ids:
    print(f"\n   Updating requirement {req_id}...")
    
    # First, get current requirement
    get_url = f"{full_url}/requirement/{req_id}"
    try:
        get_response = requests.get(get_url, headers=headers, timeout=10)
        if get_response.status_code == 200:
            current_req = get_response.json()
            req_name = current_req.get("name", "Unknown")
            print(f"   Current: {req_name}")
            print(f"   Current requirementTreeIds: {current_req.get('requirementTreeIds', [])}")
            
            # Update requirementTreeIds to point to Death Star folder
            updated_req = current_req.copy()
            updated_req["requirementTreeIds"] = [death_star_folder_id]
            
            # Try PUT to update
            put_url = f"{full_url}/requirement/{req_id}"
            print(f"   Updating requirementTreeIds to: [{death_star_folder_id}]...")
            
            put_response = requests.put(put_url, headers=headers, json=updated_req, timeout=10)
            if put_response.status_code in [200, 204]:
                print(f"   ✅ SUCCESS: Requirement moved to Death Star folder")
            else:
                print(f"   ❌ HTTP {put_response.status_code}: {put_response.text[:200]}")
        else:
            print(f"   ❌ Could not get requirement: {get_response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print(f"\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"✅ Found Death Star folder ID: {death_star_folder_id}")
print(f"✅ Attempted to move {len(requirement_ids)} requirement(s)")
print(f"\nPlease verify in Zephyr UI that requirements are now under 'The Death Star Project' folder")

