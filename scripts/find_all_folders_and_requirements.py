#!/usr/bin/env python3
"""
Find all folders and their IDs, and check which folder "The Death Star Project" is.

The UI shows folders that the API might not be returning correctly.
Let's try different approaches to find the folder structure.
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

print("=" * 80)
print("FINDING ALL FOLDERS AND REQUIREMENTS")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print()

# Known folder IDs from our work
known_folders = {
    698: "REQ-001: Core Reactor Stability",
    699: "REQ-001: Core Reactor Stability (subfolder)",
    700: "The Death Star Project (created by script)"
}

print("1. Checking known folders...")
print("=" * 80)
for folder_id, expected_name in known_folders.items():
    folder_url = f"{full_url}/requirementtree/{folder_id}"
    try:
        response = requests.get(folder_url, headers=headers, timeout=10)
        if response.status_code == 200:
            folder_data = response.json()
            actual_name = folder_data.get("name", "Unknown")
            print(f"\nFolder ID {folder_id}:")
            print(f"   Expected: {expected_name}")
            print(f"   Actual: {actual_name}")
            print(f"   Full data: {json.dumps(folder_data, indent=2)[:300]}")
        else:
            print(f"\nFolder ID {folder_id}: HTTP {response.status_code}")
    except Exception as e:
        print(f"\nFolder ID {folder_id}: Error - {e}")

# Try to get all requirements and see their folder assignments
print(f"\n2. Getting all requirements to see folder structure...")
print("=" * 80)

# Try different endpoints to list requirements
list_endpoints = [
    f"/requirement/project/{test_project_id}",
    f"/requirementtree/project/{test_project_id}",
    f"/requirementtree/{test_project_id}",
]

all_requirements_data = None
for endpoint in list_endpoints:
    url = f"{full_url}{endpoint}"
    print(f"\n   Trying: {endpoint}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS: Got data (type: {type(data)})")
            if isinstance(data, list):
                print(f"   Found {len(data)} item(s)")
                all_requirements_data = data
                break
            elif isinstance(data, dict):
                print(f"   Got dict structure")
                all_requirements_data = data
                break
        else:
            print(f"   ❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# If we got data, analyze it
if all_requirements_data:
    print(f"\n3. Analyzing folder structure from requirements...")
    print("=" * 80)
    
    # Collect all unique folder IDs
    folder_ids = set()
    folder_to_requirements = {}
    
    if isinstance(all_requirements_data, list):
        items = all_requirements_data
    elif isinstance(all_requirements_data, dict):
        # Try to extract list from dict
        items = all_requirements_data.get("requirements", []) or all_requirements_data.get("children", []) or [all_requirements_data]
    else:
        items = []
    
    for item in items:
        if isinstance(item, dict):
            req_id = item.get("id")
            req_name = item.get("name", "Unknown")
            tree_ids = item.get("requirementTreeIds", [])
            
            for tree_id in tree_ids:
                folder_ids.add(tree_id)
                if tree_id not in folder_to_requirements:
                    folder_to_requirements[tree_id] = []
                folder_to_requirements[tree_id].append({"id": req_id, "name": req_name})
    
    print(f"\n   Found {len(folder_ids)} unique folder ID(s): {sorted(folder_ids)}")
    
    # Get folder names
    print(f"\n   Folder Structure:")
    for folder_id in sorted(folder_ids):
        folder_url = f"{full_url}/requirementtree/{folder_id}"
        try:
            response = requests.get(folder_url, headers=headers, timeout=10)
            if response.status_code == 200:
                folder_data = response.json()
                folder_name = folder_data.get("name", "Unknown")
                req_count = len(folder_to_requirements.get(folder_id, []))
                print(f"\n   Folder ID {folder_id}: '{folder_name}'")
                print(f"      Contains {req_count} requirement(s):")
                for req in folder_to_requirements.get(folder_id, []):
                    print(f"        - {req['name']} (ID: {req['id']})")
            else:
                print(f"\n   Folder ID {folder_id}: (Could not retrieve)")
        except Exception as e:
            print(f"\n   Folder ID {folder_id}: Error - {e}")

print(f"\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("\nThis should show:")
print("  1. All folders that exist")
print("  2. Which requirements are in which folders")
print("  3. The correct folder ID for 'The Death Star Project'")

