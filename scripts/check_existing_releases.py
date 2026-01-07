#!/usr/bin/env python
"""Check existing releases in SpectraTestProject."""
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

print("Fetching existing releases...")
response = requests.get(
    f"{BASE_URL}/release/project/{PROJECT_ID}",
    headers=headers,
    timeout=10
)

if response.status_code == 200:
    releases = response.json()
    print(f"\nFound {len(releases)} existing releases:\n")
    
    for r in releases:
        status_map = {0: "Draft", 1: "Active", 2: "Completed"}
        status = status_map.get(r.get("status"), "Unknown")
        locked = r.get("isLocked", "unknown")
        
        print(f"  ID {r['id']}: {r['name']}")
        print(f"     Status: {status}, Locked: {locked}")
        print(f"     Created: {r.get('createdDate')}")
        print()
else:
    print(f"ERROR: HTTP {response.status_code}")
    print(response.text)
