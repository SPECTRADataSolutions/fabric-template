#!/usr/bin/env python3
"""
Create "The Death Star Project" requirement folder and move requirements to it.

Since "The Death Star Project" folder doesn't exist in the API response,
we'll create it first, then move the requirements.
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

print("=" * 80)
print("CREATE DEATH STAR FOLDER AND MOVE REQUIREMENTS")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"Requirements to move: {requirement_ids}")
print()

# Step 1: Create "The Death Star Project" folder
print("1. Creating 'The Death Star Project' requirement folder...")
folder_payload = {
    "name": "The Death Star Project",
    "description": "Galactic Empire's ultimate weapon development project - Phase 1",
    "projectId": test_project_id
    # No parentId = top-level folder
}

url = f"{full_url}/requirementtree/add"
try:
    response = requests.post(url, headers=headers, json=folder_payload, timeout=30)
    if response.status_code in [200, 201]:
        folder_data = response.json()
        death_star_folder_id = folder_data.get("id")
        print(f"   ✅ SUCCESS: Created folder (ID: {death_star_folder_id})")
    else:
        print(f"   ❌ HTTP {response.status_code}: {response.text[:200]}")
        print(f"   ⚠️ Folder may already exist - trying to find it...")
        death_star_folder_id = None
except Exception as e:
    print(f"   ❌ Error: {e}")
    death_star_folder_id = None

# If creation failed, try to find existing folder
if not death_star_folder_id:
    print("\n2. Searching for existing 'Death Star' folder...")
    # Try getting requirement tree again with different endpoint
    tree_url = f"{full_url}/requirementtree/{test_project_id}"
    try:
        tree_response = requests.get(tree_url, headers=headers, timeout=10)
        if tree_response.status_code == 200:
            tree_data = tree_response.json()
            
            # Recursive search function
            def find_death_star_folder(nodes):
                if isinstance(nodes, list):
                    for node in nodes:
                        result = find_death_star_folder(node)
                        if result:
                            return result
                elif isinstance(nodes, dict):
                    name = nodes.get("name", "")
                    if "death star" in name.lower():
                        return nodes.get("id"), nodes
                    if "children" in nodes:
                        result = find_death_star_folder(nodes["children"])
                        if result:
                            return result
                return None
            
            result = find_death_star_folder(tree_data)
            if result:
                death_star_folder_id, folder_data = result
                print(f"   ✅ Found: '{folder_data.get('name')}' (ID: {death_star_folder_id})")
            else:
                print(f"   ❌ 'Death Star' folder not found")
                print(f"   Please create 'The Death Star Project' folder in UI first")
                exit(1)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        exit(1)

# Step 2: Move requirements to Death Star folder
print(f"\n3. Moving requirements to folder ID: {death_star_folder_id}...")

for req_id in requirement_ids:
    print(f"\n   Updating requirement {req_id}...")
    
    # Get current requirement
    get_url = f"{full_url}/requirement/{req_id}"
    try:
        get_response = requests.get(get_url, headers=headers, timeout=10)
        if get_response.status_code == 200:
            current_req = get_response.json()
            req_name = current_req.get("name", "Unknown")
            print(f"   Requirement: {req_name}")
            print(f"   Current requirementTreeIds: {current_req.get('requirementTreeIds', [])}")
            
            # Update requirementTreeIds
            updated_req = current_req.copy()
            updated_req["requirementTreeIds"] = [death_star_folder_id]
            
            # Try PUT to update
            put_url = f"{full_url}/requirement/{req_id}"
            print(f"   Updating requirementTreeIds to: [{death_star_folder_id}]...")
            
            put_response = requests.put(put_url, headers=headers, json=updated_req, timeout=10)
            if put_response.status_code in [200, 204]:
                print(f"   ✅ SUCCESS: Requirement moved")
            else:
                print(f"   ❌ HTTP {put_response.status_code}: {put_response.text[:300]}")
        else:
            print(f"   ❌ Could not get requirement: {get_response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print(f"\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
if death_star_folder_id:
    print(f"✅ Death Star folder ID: {death_star_folder_id}")
    print(f"✅ Attempted to move {len(requirement_ids)} requirement(s)")
    print(f"\nPlease verify in Zephyr UI:")
    print(f"   1. Requirements should now be under 'The Death Star Project' folder")
    print(f"   2. If not, you may need to move them manually in UI")
else:
    print("❌ Could not find or create Death Star folder")
    print("   Please create 'The Death Star Project' folder in UI first")

