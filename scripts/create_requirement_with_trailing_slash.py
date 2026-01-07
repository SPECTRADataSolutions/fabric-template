#!/usr/bin/env python3
"""
Try creating requirement with /requirement/ (trailing slash) endpoint.

From endpoints.json line 616: "Create new requirement [/requirement/]"
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
print("CREATING REQUIREMENT WITH TRAILING SLASH")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"Endpoint: /requirement/ (with trailing slash)")
print()

# Try /requirement/ with trailing slash
url = f"{full_url}/requirement/"

payloads_to_try = [
    # Option 1: Direct payload
    {
        "name": "REQ-001: Core Reactor Stability",
        "description": "The Death Star's core reactor must maintain stable power output",
        "projectId": test_project_id
    },
    # Option 2: With requirementDto wrapper
    {
        "requirementDto": {
            "name": "REQ-001: Core Reactor Stability",
            "description": "The Death Star's core reactor must maintain stable power output",
            "projectId": test_project_id
        }
    }
]

for i, payload in enumerate(payloads_to_try, 1):
    print(f"Attempt {i}: {json.dumps(payload, indent=2)[:200]}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ SUCCESS! Status: {response.status_code}")
            print(f"Response: {json.dumps(result, indent=2)}")
            print(f"\n✅ FOUND WORKING ENDPOINT: /requirement/ (with trailing slash)")
            print(f"✅ WORKING PAYLOAD: Option {i}")
            exit(0)
        else:
            print(f"❌ HTTP {response.status_code}: {response.text[:300]}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("Still not working. Checking if endpoint needs different structure...")
print("=" * 80)

