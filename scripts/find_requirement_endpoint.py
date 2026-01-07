#!/usr/bin/env python3
"""
Find the correct endpoint for creating actual requirements (not tree folders).

Hypothesis: Anything with "tree" creates folders. We need the non-tree endpoint.
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
print("FINDING ACTUAL REQUIREMENT ENDPOINT")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"Hypothesis: /requirementtree/* creates folders, /requirement/* creates requirements")
print()

# Try /requirement endpoint with different payload structures
print("1. Trying /requirement endpoint (POST)...")
print("   (Previous attempts returned HTTP 500: 'id is null')")
print()

requirement_payloads = [
    # Option 1: Direct payload with projectId
    {
        "name": "REQ-001: Core Reactor Stability",
        "description": "Test requirement - direct payload",
        "projectId": test_project_id
    },
    # Option 2: With requirementDto wrapper
    {
        "requirementDto": {
            "name": "REQ-001: Core Reactor Stability",
            "description": "Test requirement - wrapped",
            "projectId": test_project_id
        }
    },
    # Option 3: With id field (maybe it needs an ID?)
    {
        "id": 0,  # Maybe 0 means "new"?
        "name": "REQ-001: Core Reactor Stability",
        "description": "Test requirement - with id: 0",
        "projectId": test_project_id
    },
    # Option 4: With parentId reference to existing folder
    {
        "name": "REQ-001: Core Reactor Stability",
        "description": "Test requirement - with parentId",
        "projectId": test_project_id,
        "parentId": 698  # Existing folder
    }
]

url = f"{full_url}/requirement"
for i, payload in enumerate(requirement_payloads, 1):
    print(f"   Attempt {i}: {json.dumps(payload, indent=2)[:200]}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"   ✅ SUCCESS! Status: {response.status_code}")
            print(f"   Response: {json.dumps(result, indent=2)[:500]}")
            print(f"\n   ✅ FOUND WORKING ENDPOINT: /requirement")
            print(f"   ✅ WORKING PAYLOAD: Option {i}")
            exit(0)
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("2. Checking SDK for other requirement endpoints...")
print("=" * 80)

# Check what other requirement endpoints exist in SDK
sdk_path = Path(__file__).parent.parent / "spectraSDK.Notebook" / "notebook_content.py"
if sdk_path.exists():
    with open(sdk_path, "r", encoding="utf-8") as f:
        content = f.read()
        # Find all requirement endpoints
        import re
        endpoints = re.findall(r'"endpoint_path":\s*"(/requirement[^"]*)"', content)
        print(f"   Found {len(set(endpoints))} unique requirement endpoints:")
        for endpoint in sorted(set(endpoints)):
            print(f"   - {endpoint}")

print("\n" + "=" * 80)
print("3. Trying alternative endpoints...")
print("=" * 80)

# Try other endpoints from SDK
alternative_endpoints = [
    "/requirement/bulk",  # Bulk operations
    # Maybe requirements are created differently?
]

for endpoint in alternative_endpoints:
    url = f"{full_url}{endpoint}"
    print(f"\n   Trying: {endpoint}...")
    payload = {
        "name": "REQ-001: Core Reactor Stability",
        "description": "Test requirement",
        "projectId": test_project_id
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code in [200, 201]:
            print(f"   ✅ SUCCESS! Status: {response.status_code}")
            print(f"   Response: {json.dumps(response.json(), indent=2)[:500]}")
            exit(0)
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)
print("\nIf all endpoints failed, requirements might be:")
print("  1. Created through the UI only (no API endpoint)")
print("  2. Created via a different workflow (e.g., import)")
print("  3. Created by linking testcases to requirement folders")
print("  4. Created via a different endpoint we haven't found yet")
print("\nNext steps:")
print("  - Check Zephyr API documentation")
print("  - Check if requirements are created by allocating testcases")
print("  - Check if there's an import endpoint")

