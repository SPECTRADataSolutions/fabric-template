#!/usr/bin/env python
"""
Manual workaround: Create folder in UI, then use its ID.

Since POST /testcasetree is broken, we'll:
1. Prompt user to create folder in UI
2. Fetch folder tree to get ID
3. Continue with testcase creation
"""

import requests
import json
from pathlib import Path

# Get API token
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

BASE_URL = "https://velonetic.yourzephyr.com/flex/services/rest/latest"
PROJECT_ID = 45

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

print("="*80)
print("MANUAL WORKAROUND: Get Folder ID from UI")
print("="*80)

print("\n📋 INSTRUCTIONS:")
print("1. Go to Zephyr UI")
print("2. Navigate to Test Repository")
print("3. Create a folder called 'Discovery Test Folder'")
print("4. Press Enter when done...")

input()

print("\nFetching folder tree...")

# Try multiple endpoints to get folder tree
endpoints_to_try = [
    f"/testcasetree/projectrepository/{PROJECT_ID}",
    f"/testcasetree/project/{PROJECT_ID}",
    f"/testcasetree/{PROJECT_ID}",
]

folder_id = None
folder_name = None

for endpoint in endpoints_to_try:
    print(f"\nTrying: GET {endpoint}")
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=headers,
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response type: {type(data)}")
        print(f"Response length: {len(data) if isinstance(data, list) else 'N/A'}")
        
        if isinstance(data, list) and len(data) > 0:
            print(f"\nFound {len(data)} nodes:")
            for node in data[:5]:  # Show first 5
                if isinstance(node, dict):
                    node_id = node.get("id")
                    node_name = node.get("name", "Unknown")
                    node_type = node.get("type", "Unknown")
                    print(f"  - ID: {node_id}, Name: {node_name}, Type: {node_type}")
                    
                    if not folder_id:
                        folder_id = node_id
                        folder_name = node_name
            
            if folder_id:
                break
        else:
            print("  (empty or non-list response)")

if folder_id:
    print(f"\n✅ Found folder ID: {folder_id} - {folder_name}")
    print(f"\nYou can now use this ID for testcase creation:")
    print(f"  folder_id = {folder_id}")
else:
    print(f"\n❌ No folders found")
    print("\nPossible reasons:")
    print("1. Folder not created yet")
    print("2. Different API endpoint needed")
    print("3. Permissions issue")

