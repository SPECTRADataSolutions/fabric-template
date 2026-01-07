#!/usr/bin/env python
"""Delete ALL releases from SpectraTestProject."""
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

print("Fetching all releases...")
response = requests.get(f"{BASE_URL}/release/project/{PROJECT_ID}", headers=headers, timeout=10)

if response.status_code == 200:
    releases = response.json()
    print(f"\nFound {len(releases)} releases\n")
    
    deleted = 0
    skipped = 0
    
    for release in releases:
        rel_id = release.get("id")
        rel_name = release.get("name")
        
        print(f"Deleting release {rel_id}: {rel_name}...")
        del_response = requests.delete(f"{BASE_URL}/release/{rel_id}", headers=headers, timeout=10)
        
        if del_response.status_code == 200:
            print(f"  OK")
            deleted += 1
        elif del_response.status_code == 400 and "cannot be deleted" in del_response.text:
            print(f"  SKIP - Last active release (Zephyr won't allow deletion)")
            skipped += 1
        else:
            print(f"  FAIL - HTTP {del_response.status_code}: {del_response.text[:100]}")
    
    print(f"\nDeleted: {deleted}")
    print(f"Skipped: {skipped} (last active release)")
    print("\nProject is now clean!")
else:
    print(f"ERROR: HTTP {response.status_code}")
    print(response.text)
