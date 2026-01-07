#!/usr/bin/env python3
"""
Verify if requirement ID 701 is an actual requirement or just a folder.
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

requirement_id = 701

print("=" * 80)
print("VERIFYING REQUIREMENT 701")
print("=" * 80)
print(f"\nRequirement ID: {requirement_id}")
print()

# Try GET /requirement/{id}
print("1. Checking GET /requirement/{id}...")
get_url = f"{full_url}/requirement/{requirement_id}"
try:
    response = requests.get(get_url, headers=headers, timeout=10)
    if response.status_code == 200:
        requirement = response.json()
        print(f"   ✅ SUCCESS: Retrieved requirement")
        print(f"\n   Key Fields:")
        print(f"     ID: {requirement.get('id')}")
        print(f"     Name: {requirement.get('name')}")
        print(f"     Priority: {requirement.get('priority')}")
        print(f"     External ID: {requirement.get('externalId')}")
        print(f"     Details: {requirement.get('details', requirement.get('description', ''))[:100]}...")
        print(f"     Requirement Tree IDs: {requirement.get('requirementTreeIds', [])}")
        print(f"     Testcase IDs: {requirement.get('testcaseIds', [])}")
        print(f"     Requirement Type: {requirement.get('requirementType')}")
        
        # Check if it has fields that indicate it's a real requirement
        has_priority = requirement.get('priority') is not None
        has_external_id = requirement.get('externalId') is not None
        has_details = requirement.get('details') is not None or requirement.get('description') is not None
        
        print(f"\n   Analysis:")
        if has_priority and has_external_id and has_details:
            print(f"     ✅ Looks like a REAL REQUIREMENT (has priority, externalId, details)")
        else:
            print(f"     ⚠️ May be a FOLDER (missing priority/externalId/details)")
        
        print(f"\n   Full Response:")
        print(json.dumps(requirement, indent=2))
    elif response.status_code == 404:
        print(f"   ❌ NOT FOUND: Requirement {requirement_id} does not exist")
    else:
        print(f"   ⚠️ HTTP {response.status_code}: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Compare with known requirement (6455)
print(f"\n2. Comparing with known requirement (6455)...")
known_url = f"{full_url}/requirement/6455"
try:
    response = requests.get(known_url, headers=headers, timeout=10)
    if response.status_code == 200:
        known = response.json()
        print(f"   ✅ Retrieved known requirement 6455")
        print(f"\n   Known requirement fields:")
        print(f"     Priority: {known.get('priority')}")
        print(f"     External ID: {known.get('externalId')}")
        print(f"     Details: {known.get('details', '')[:50]}...")
        print(f"     Requirement Type: {known.get('requirementType')}")
        
        print(f"\n   Comparison:")
        print(f"     Both have ID: ✅")
        print(f"     Both have name: ✅")
        if known.get('priority') and requirement.get('priority'):
            print(f"     Both have priority: ✅")
        else:
            print(f"     Priority match: ⚠️ (known: {known.get('priority')}, new: {requirement.get('priority')})")
except Exception as e:
    print(f"   ⚠️ Could not compare: {e}")

print(f"\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)
print(f"\nPlease check in Zephyr UI:")
print(f"  1. Go to Requirements section")
print(f"  2. Look for ID: {requirement_id}")
print(f"  3. Check if it appears in the TABLE view (not just tree)")
print(f"  4. Compare with requirement 6455 (known real requirement)")

