#!/usr/bin/env python3
"""
Investigate the difference between requirement folders and actual requirements.

The UI shows requirements in a table, but we're only creating folders.
Let's check what an actual requirement looks like vs a folder.
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
folder_id = 698  # The folder we created
subfolder_id = 699  # The subfolder we created

print("=" * 80)
print("INVESTIGATING REQUIREMENT STRUCTURE")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"Folder ID: {folder_id}")
print(f"Subfolder ID: {subfolder_id}")
print()

# Get the requirement tree to see structure
print("1. Getting requirement tree structure...")
tree_url = f"{full_url}/requirementtree/project/{test_project_id}"
try:
    tree_response = requests.get(tree_url, headers=headers, timeout=10)
    if tree_response.status_code == 200:
        tree_data = tree_response.json()
        print(f"   Tree structure retrieved")
        print(f"\n   Full tree (first 500 chars):")
        print(json.dumps(tree_data, indent=2)[:500])
        
        # Look for our folder and subfolder
        def find_node(nodes, target_id, path=""):
            if isinstance(nodes, list):
                for node in nodes:
                    result = find_node(node, target_id, path)
                    if result:
                        return result
            elif isinstance(nodes, dict):
                if nodes.get("id") == target_id:
                    return path, nodes
                if "children" in nodes:
                    result = find_node(nodes["children"], target_id, f"{path}/{nodes.get('name', 'unknown')}")
                    if result:
                        return result
            return None
        
        print(f"\n   Looking for folder {folder_id}...")
        folder_info = find_node(tree_data, folder_id)
        if folder_info:
            print(f"   Found folder: {folder_info[0]}")
            print(f"   Folder data: {json.dumps(folder_info[1], indent=2)}")
        
        print(f"\n   Looking for subfolder {subfolder_id}...")
        subfolder_info = find_node(tree_data, subfolder_id)
        if subfolder_info:
            print(f"   Found subfolder: {subfolder_info[0]}")
            print(f"   Subfolder data: {json.dumps(subfolder_info[1], indent=2)}")
    else:
        print(f"   GET failed: {tree_response.status_code} - {tree_response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

# Try to get individual requirement details
print(f"\n2. Getting details for folder {folder_id}...")
detail_url = f"{full_url}/requirement/{folder_id}"
try:
    detail_response = requests.get(detail_url, headers=headers, timeout=10)
    if detail_response.status_code == 200:
        folder_detail = detail_response.json()
        print(f"   Folder details:")
        print(json.dumps(folder_detail, indent=2))
    else:
        print(f"   GET failed: {detail_response.status_code} - {detail_response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

print(f"\n3. Getting details for subfolder {subfolder_id}...")
detail_url = f"{full_url}/requirement/{subfolder_id}"
try:
    detail_response = requests.get(detail_url, headers=headers, timeout=10)
    if detail_response.status_code == 200:
        subfolder_detail = detail_response.json()
        print(f"   Subfolder details:")
        print(json.dumps(subfolder_detail, indent=2))
    else:
        print(f"   GET failed: {detail_response.status_code} - {detail_response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

# Check if there's a different endpoint for listing actual requirements (not tree)
print(f"\n4. Checking for requirements list endpoint...")
list_endpoints = [
    f"/requirement/project/{test_project_id}",
    f"/requirement/project/{test_project_id}/list",
    f"/requirement/list",
    f"/requirementtree/{folder_id}/requirements"
]

for endpoint in list_endpoints:
    url = f"{full_url}{endpoint}"
    print(f"   Trying: {endpoint}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   SUCCESS: {endpoint}")
            print(f"   Response structure: {type(data)}")
            if isinstance(data, list):
                print(f"   Found {len(data)} item(s)")
                if data:
                    print(f"   Sample item:")
                    print(json.dumps(data[0], indent=2))
            else:
                print(f"   Response: {json.dumps(data, indent=2)[:500]}")
            break
        else:
            print(f"   HTTP {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")

print(f"\n" + "=" * 80)
print("ANALYSIS")
print("=" * 80)
print("\nBased on the investigation, we need to determine:")
print("  1. What makes a requirement appear in the table vs just the tree?")
print("  2. Is there a different endpoint for creating requirements?")
print("  3. Do requirements need to be linked to testcases to appear?")
print("  4. Is there a 'type' or 'isFolder' field that distinguishes them?")

