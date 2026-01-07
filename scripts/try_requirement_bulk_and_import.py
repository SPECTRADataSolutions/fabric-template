#!/usr/bin/env python3
"""
Try creating requirement using bulk endpoint and import endpoint.
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
print("TRYING BULK AND IMPORT ENDPOINTS")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print()

# Try POST /requirement/bulk
print("1. Trying POST /requirement/bulk...")
bulk_url = f"{full_url}/requirement/bulk"

# Bulk payload - array of requirements
bulk_payloads = [
    # Option 1: Array of requirement objects
    [
        {
            "name": "REQ-DS-005: Shield Generator Integration",
            "description": "The Death Star's shield generator must integrate with the hyperdrive and core reactor systems, providing protection during hyperspace jumps. Shield strength must be maintained at 100% during all operational phases.",
            "projectId": test_project_id,
            "priority": "1",
            "externalId": "REQ-DS-005"
        }
    ],
    # Option 2: Wrapped array
    {
        "requirements": [
            {
                "name": "REQ-DS-005: Shield Generator Integration",
                "description": "The Death Star's shield generator must integrate with the hyperdrive and core reactor systems, providing protection during hyperspace jumps. Shield strength must be maintained at 100% during all operational phases.",
                "projectId": test_project_id,
                "priority": "1",
                "externalId": "REQ-DS-005"
            }
        ]
    }
]

for i, payload in enumerate(bulk_payloads, 1):
    print(f"\n   Trying bulk payload option {i}...")
    print(f"   Payload type: {type(payload).__name__}")
    try:
        response = requests.post(bulk_url, headers=headers, json=payload, timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"   ✅ SUCCESS!")
            print(f"   Response: {json.dumps(result, indent=2)[:500]}")
            break
        else:
            print(f"   ❌ HTTP {response.status_code}")
            try:
                error = response.json()
                print(f"   Error: {json.dumps(error, indent=2)[:300]}")
            except:
                print(f"   Error: {response.text[:300]}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")

# Try GET /externalrequirement/importall (check what it needs)
print(f"\n2. Checking /externalrequirement/importall endpoint...")
import_url = f"{full_url}/externalrequirement/importall?projectId={test_project_id}"
try:
    # First try GET to see what it expects
    response = requests.get(import_url, headers=headers, timeout=10)
    print(f"   GET Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ GET works - Response: {response.text[:200]}")
    else:
        print(f"   ⚠️ GET Status {response.status_code}: {response.text[:200]}")
    
    # Try POST with minimal payload
    print(f"\n   Trying POST /externalrequirement/importall...")
    import_payload = {
        "projectId": test_project_id,
        "filter": "project = SPECTRA"  # Example filter
    }
    response = requests.post(import_url, headers=headers, json=import_payload, timeout=30)
    print(f"   POST Status: {response.status_code}")
    if response.status_code in [200, 201]:
        result = response.json()
        print(f"   ✅ SUCCESS!")
        print(f"   Response: {json.dumps(result, indent=2)[:500]}")
    else:
        print(f"   ❌ HTTP {response.status_code}")
        try:
            error = response.json()
            print(f"   Error: {json.dumps(error, indent=2)[:300]}")
        except:
            print(f"   Error: {response.text[:300]}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

print(f"\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nIf none of these worked, requirements may need to be created via:")
print(f"   1. UI (manual creation)")
print(f"   2. Import from external system (Jira, etc.)")
print(f"   3. Different Zephyr version/configuration")
print(f"   4. Different API endpoint not in catalog")

