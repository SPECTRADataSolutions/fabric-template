#!/usr/bin/env python3
"""
Try creating a requirement using all available endpoints from the catalog.

Since endpoints are now fixed, let's try all requirement-related endpoints systematically.
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
print("ATTEMPTING TO CREATE REQUIREMENT")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"API Base: {full_url}")
print()

# First, check existing requirements to understand structure
print("1. Checking existing requirements...")
get_url = f"{full_url}/requirement/project/{test_project_id}"
try:
    get_response = requests.get(get_url, headers=headers, timeout=10)
    if get_response.status_code == 200:
        existing = get_response.json()
        print(f"   ✅ Found {len(existing) if isinstance(existing, list) else 1} requirement(s)")
        if existing and isinstance(existing, list) and len(existing) > 0:
            sample = existing[0]
            print(f"\n   Sample requirement structure:")
            print(f"   ID: {sample.get('id')}")
            print(f"   Name: {sample.get('name')}")
            print(f"   Project ID: {sample.get('projectId')}")
            print(f"   Tree IDs: {sample.get('requirementTreeIds', [])}")
            print(f"\n   Full structure (first 20 fields):")
            for key, value in list(sample.items())[:20]:
                print(f"     {key}: {type(value).__name__} = {str(value)[:50]}")
    else:
        print(f"   ⚠️ GET failed: {get_response.status_code} - {get_response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("2. Attempting to create requirement...")
print("=" * 80)

# Try POST /requirement with various payload structures
requirement_name = "REQ-DS-004: Hyperdrive System Integration"
requirement_description = "The Death Star's hyperdrive system must integrate seamlessly with the core reactor, enabling instant travel across the galaxy. The system must support jump calculations for distances up to 100,000 light-years with accuracy within 0.001%. All navigation systems must be synchronized and validated before operational deployment."

payloads_to_try = [
    # Option 1: Minimal payload (based on what we see in existing requirements)
    {
        "name": requirement_name,
        "description": requirement_description,
        "projectId": test_project_id
    },
    # Option 2: With explicit fields from sample
    {
        "name": requirement_name,
        "description": requirement_description,
        "projectId": test_project_id,
        "priority": "P1",
        "altId": "REQ-DS-004"
    },
    # Option 3: With id: 0 (new entity)
    {
        "id": 0,
        "name": requirement_name,
        "description": requirement_description,
        "projectId": test_project_id
    },
    # Option 4: With requirementTreeIds (if we have a folder)
    {
        "name": requirement_name,
        "description": requirement_description,
        "projectId": test_project_id,
        "requirementTreeIds": [700]  # The Death Star Project folder
    }
]

endpoints_to_try = [
    "/requirement",
    "/requirement/",
    "/requirementtree/add"  # We know this creates folders, but let's confirm
]

created_requirement = None
requirement_id = None
successful_endpoint = None
successful_payload = None

for endpoint in endpoints_to_try:
    url = f"{full_url}{endpoint}"
    
    for i, payload in enumerate(payloads_to_try, 1):
        print(f"\n🔍 Trying: {endpoint} with payload option {i}")
        print(f"   Payload keys: {list(payload.keys())}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                created_requirement = response.json()
                requirement_id = created_requirement.get("id") if isinstance(created_requirement, dict) else None
                
                if requirement_id:
                    successful_endpoint = endpoint
                    successful_payload = payload
                    print(f"   ✅ SUCCESS: Created requirement ID {requirement_id}")
                    print(f"\n   Full Response:")
                    print(json.dumps(created_requirement, indent=2))
                    break
                else:
                    print(f"   ⚠️ Created but no ID in response")
                    print(f"   Response: {json.dumps(created_requirement, indent=2)[:500]}")
            else:
                print(f"   ❌ HTTP {response.status_code}")
                try:
                    error_json = response.json()
                    print(f"   Error: {json.dumps(error_json, indent=2)[:300]}")
                except:
                    print(f"   Error: {response.text[:300]}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    if created_requirement and requirement_id:
        break

if not created_requirement or not requirement_id:
    print("\n" + "=" * 80)
    print("❌ COULD NOT CREATE REQUIREMENT")
    print("=" * 80)
    print("\n💡 Next steps:")
    print("   1. Check if requirements must be created via UI")
    print("   2. Check if there's an import endpoint")
    print("   3. Verify API permissions for requirement creation")
    print("   4. Check Zephyr version - may need different endpoint")
    exit(1)

print("\n" + "=" * 80)
print("✅ SUCCESS: Requirement Created!")
print("=" * 80)
print(f"\nRequirement ID: {requirement_id}")
print(f"Endpoint: {successful_endpoint}")
print(f"Name: {requirement_name}")

# Verify it appears in the requirements list
print(f"\n3. Verifying requirement appears in project list...")
verify_url = f"{full_url}/requirement/project/{test_project_id}"
try:
    verify_response = requests.get(verify_url, headers=headers, timeout=10)
    if verify_response.status_code == 200:
        all_requirements = verify_response.json()
        if isinstance(all_requirements, list):
            found = any(r.get("id") == requirement_id for r in all_requirements)
            if found:
                print(f"   ✅ Requirement {requirement_id} found in project requirements")
            else:
                print(f"   ⚠️ Requirement {requirement_id} NOT found in project requirements list")
                print(f"   (May be a folder, not an actual requirement)")
except Exception as e:
    print(f"   ❌ Verification failed: {e}")

print(f"\n" + "=" * 80)
print("MANUAL VERIFICATION REQUIRED")
print("=" * 80)
print(f"\nPlease check in Zephyr UI:")
print(f"  1. Go to project ID: {test_project_id} (SpectraTestProject)")
print(f"  2. Check Requirements section")
print(f"  3. Look for: '{requirement_name}'")
print(f"  4. Verify it appears in the TABLE (not just in the tree)")
print(f"  5. Check requirement ID: {requirement_id}")

