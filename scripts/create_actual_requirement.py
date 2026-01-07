#!/usr/bin/env python3
"""
Create an actual requirement (not a folder) in Zephyr.

The /requirementtree/add endpoint creates folders/categories.
We need to find the correct endpoint for creating actual requirements.
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
requirement_folder_id = 698  # The folder we created

print("=" * 80)
print("CREATING ACTUAL REQUIREMENT")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"Requirement Folder ID: {requirement_folder_id}")
print(f"API Base: {full_url}")
print()

# First, let's see what existing requirements look like
print("1. Checking existing requirements structure...")
get_url = f"{full_url}/requirement/project/{test_project_id}"
try:
    get_response = requests.get(get_url, headers=headers, timeout=10)
    if get_response.status_code == 200:
        existing = get_response.json()
        print(f"   Found {len(existing) if isinstance(existing, list) else 1} requirement(s)")
        if existing:
            print(f"\n   Sample requirement structure:")
            sample = existing[0] if isinstance(existing, list) else existing
            print(json.dumps(sample, indent=2))
    else:
        print(f"   GET failed: {get_response.status_code} - {get_response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 80)
print("2. Attempting to create actual requirement...")
print("=" * 80)

# Try different payload structures
payloads_to_try = [
    # Option 1: Direct requirement with folder reference
    {
        "name": "REQ-001: Core Reactor Stability",
        "description": "The Death Star's core reactor must maintain stable power output of 1.08 x 10^32 watts without thermal fluctuations exceeding 0.1%. The reactor must sustain continuous operation for a minimum of 72 standard hours at full capacity. All safety protocols must be validated before operational deployment.",
        "projectId": test_project_id,
        "parentId": requirement_folder_id
    },
    # Option 2: Requirement with treeId
    {
        "name": "REQ-001: Core Reactor Stability",
        "description": "The Death Star's core reactor must maintain stable power output of 1.08 x 10^32 watts without thermal fluctuations exceeding 0.1%. The reactor must sustain continuous operation for a minimum of 72 standard hours at full capacity. All safety protocols must be validated before operational deployment.",
        "projectId": test_project_id,
        "treeId": requirement_folder_id
    },
    # Option 3: Requirement without folder reference
    {
        "name": "REQ-001: Core Reactor Stability",
        "description": "The Death Star's core reactor must maintain stable power output of 1.08 x 10^32 watts without thermal fluctuations exceeding 0.1%. The reactor must sustain continuous operation for a minimum of 72 standard hours at full capacity. All safety protocols must be validated before operational deployment.",
        "projectId": test_project_id
    },
    # Option 4: Wrapped in requirementDto
    {
        "requirementDto": {
            "name": "REQ-001: Core Reactor Stability",
            "description": "The Death Star's core reactor must maintain stable power output of 1.08 x 10^32 watts without thermal fluctuations exceeding 0.1%. The reactor must sustain continuous operation for a minimum of 72 standard hours at full capacity. All safety protocols must be validated before operational deployment.",
            "projectId": test_project_id
        }
    }
]

endpoints_to_try = [
    "/requirement",
    "/requirementtree/add",
    f"/requirementtree/{requirement_folder_id}/add"
]

created_requirement = None
requirement_id = None
successful_endpoint = None
successful_payload = None

for endpoint in endpoints_to_try:
    url = f"{full_url}{endpoint}"
    
    for i, payload in enumerate(payloads_to_try, 1):
        print(f"\nTrying endpoint: {endpoint}, payload option {i}...")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code in [200, 201]:
                created_requirement = response.json()
                
                # Extract requirement ID
                if isinstance(created_requirement, dict):
                    for key in ["requirementDto", "dto", "requirement"]:
                        if key in created_requirement:
                            requirement_data = created_requirement[key]
                            requirement_id = requirement_data.get("id") if isinstance(requirement_data, dict) else None
                            break
                    
                    if not requirement_id:
                        requirement_id = created_requirement.get("id")
                
                if requirement_id:
                    successful_endpoint = endpoint
                    successful_payload = payload
                    print(f"   SUCCESS: Created requirement ID {requirement_id}")
                    break
            else:
                print(f"   HTTP {response.status_code}: {response.text[:300]}")
        except Exception as e:
            print(f"   Error: {e}")
    
    if created_requirement and requirement_id:
        break

if not created_requirement or not requirement_id:
    print("\n" + "=" * 80)
    print("ERROR: Could not create requirement with any endpoint/payload combination")
    print("=" * 80)
    print("\nPlease check Zephyr API documentation or UI to understand the correct structure.")
    exit(1)

print("\n" + "=" * 80)
print("SUCCESS: Actual Requirement Created!")
print("=" * 80)
print(f"\nRequirement ID: {requirement_id}")
print(f"Endpoint used: {successful_endpoint}")
print(f"\nFull Response:")
print(json.dumps(created_requirement, indent=2))

# Verify it's accessible
print(f"\nVerifying requirement access...")
verify_url = f"{full_url}/requirement/project/{test_project_id}"
try:
    verify_response = requests.get(verify_url, headers=headers, timeout=10)
    if verify_response.status_code == 200:
        all_requirements = verify_response.json()
        if isinstance(all_requirements, list):
            found = any(r.get("id") == requirement_id for r in all_requirements)
            if found:
                print(f"OK: Requirement {requirement_id} found in project requirements list")
            else:
                print(f"WARNING: Requirement {requirement_id} not found in project requirements list")
except Exception as e:
    print(f"Verification failed: {e}")

print(f"\n" + "=" * 80)
print("MANUAL VERIFICATION")
print("=" * 80)
print(f"\nPlease check in Zephyr UI:")
print(f"  1. Go to project ID: {test_project_id} (SpectraTestProject)")
print(f"  2. Check Requirements section")
print(f"  3. Open folder ID: {requirement_folder_id} (REQ-001: Core Reactor Stabilit...)")
print(f"  4. Look for actual requirement: 'REQ-001: Core Reactor Stability'")
print(f"  5. Verify requirement ID: {requirement_id}")
print(f"  6. Check it appears in the table (not just in the tree)")

