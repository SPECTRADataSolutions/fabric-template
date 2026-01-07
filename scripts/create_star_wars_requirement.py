#!/usr/bin/env python3
"""
Create a Star Wars-themed requirement for "The Death Star Project - Phase 1".

Requirement Name: "REQ-001: Core Reactor Stability"
This requirement tracks the critical core reactor stability requirements for the Death Star.
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
print("CREATING STAR WARS REQUIREMENT")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"API Base: {full_url}")
print()

# Star Wars Requirement: "REQ-001: Core Reactor Stability"
# This requirement tracks the critical core reactor stability requirements
requirement_payload = {
    "name": "REQ-001: Core Reactor Stability",
    "description": "The Death Star's core reactor must maintain stable power output of 1.08 x 10^32 watts without thermal fluctuations exceeding 0.1%. The reactor must sustain continuous operation for a minimum of 72 standard hours at full capacity. All safety protocols must be validated before operational deployment.",
    "projectId": test_project_id
}

print("Requirement Payload:")
print(json.dumps(requirement_payload, indent=2))
print()

# Try different requirement endpoints
endpoints_to_try = [
    "/requirement",
    "/requirementtree/add",
    "/requirement/project"
]

created_requirement = None
requirement_id = None

for endpoint in endpoints_to_try:
    url = f"{full_url}{endpoint}"
    
    # Adjust payload based on endpoint
    if endpoint == "/requirement/project":
        # This might be GET only, but try POST
        url = f"{full_url}/requirement"
    elif endpoint == "/requirementtree/add":
        # Tree endpoint might need different structure
        pass
    
    print(f"Trying endpoint: {endpoint}...")
    
    try:
        response = requests.post(url, headers=headers, json=requirement_payload, timeout=30)
        
        if response.status_code in [200, 201]:
            created_requirement = response.json()
            
            # Extract requirement ID (handle wrapped responses)
            if isinstance(created_requirement, dict):
                # Check for wrapper keys
                for key in ["requirementDto", "dto", "requirement"]:
                    if key in created_requirement:
                        requirement_data = created_requirement[key]
                        requirement_id = requirement_data.get("id") if isinstance(requirement_data, dict) else None
                        break
                
                if not requirement_id:
                    requirement_id = created_requirement.get("id")
            
            print(f"SUCCESS: Created via {endpoint}")
            break
        else:
            print(f"  HTTP {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")

if not created_requirement:
    print("\nERROR: Could not create requirement with any endpoint")
    print("Trying GET to see existing requirements structure...")
    
    # Try GET to understand structure
    get_url = f"{full_url}/requirement/project/{test_project_id}"
    try:
        get_response = requests.get(get_url, headers=headers, timeout=10)
        if get_response.status_code == 200:
            existing = get_response.json()
            print(f"\nExisting requirements structure:")
            print(json.dumps(existing[:1] if isinstance(existing, list) and existing else existing, indent=2))
    except Exception as e:
        print(f"GET also failed: {e}")
    
    exit(1)

print("\n" + "=" * 80)
print("SUCCESS: Requirement Created!")
print("=" * 80)
print(f"\nRequirement ID: {requirement_id}")
print(f"Requirement Name: {requirement_payload['name']}")
print(f"Project ID: {test_project_id}")
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
        else:
            found = all_requirements.get("id") == requirement_id if isinstance(all_requirements, dict) else False
        
        if found:
            print(f"OK: Requirement {requirement_id} found in project requirements list")
        else:
            print(f"WARNING: Requirement {requirement_id} not found in project requirements list")
except Exception as e:
    print(f"Verification failed: {e}")

print(f"\n" + "=" * 80)
print("METADATA CHECK")
print("=" * 80)
print("\nChecking requirement metadata fields:")
if isinstance(created_requirement, dict):
    requirement_data = created_requirement
    for key in ["requirementDto", "dto", "requirement"]:
        if key in created_requirement:
            requirement_data = created_requirement[key]
            break
    
    if isinstance(requirement_data, dict):
        required_fields = ["id", "name", "projectId"]
        optional_fields = ["description", "createdDate", "orderId", "hasChild"]
        
        print("\nRequired fields:")
        for field in required_fields:
            if field in requirement_data:
                print(f"  OK: {field} = {requirement_data[field]}")
            else:
                print(f"  MISSING: {field}")
        
        print("\nOptional fields present:")
        for field in optional_fields:
            if field in requirement_data:
                print(f"  - {field} = {requirement_data[field]}")

print(f"\n" + "=" * 80)
print("MANUAL VERIFICATION")
print("=" * 80)
print(f"\nPlease check in Zephyr UI:")
print(f"  1. Go to project ID: {test_project_id} (SpectraTestProject)")
print(f"  2. Check Requirements section (should be at top of page)")
print(f"  3. Look for: 'REQ-001: Core Reactor Stability'")
print(f"  4. Verify requirement ID: {requirement_id}")
print(f"  5. Check all metadata fields are present")
print(f"  6. Try opening the requirement to verify it's accessible")

