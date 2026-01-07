#!/usr/bin/env python3
"""
Create a Star Wars-themed cycle for "The Death Star Project - Phase 1" release.

Cycle Name: "Death Star Core Reactor Testing"
This cycle tests the critical core reactor systems of the Death Star.
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
release_id = 131  # "The Death Star Project - Phase 1"

print("=" * 80)
print("CREATING STAR WARS CYCLE")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"Release ID: {release_id}")
print(f"API Base: {full_url}")
print()

# Star Wars Cycle: "Death Star Core Reactor Testing"
# Testing the critical core reactor systems
cycle_payload = {
    "name": "Death Star Core Reactor Testing",
    "description": "Comprehensive testing cycle for the Death Star's core reactor systems. This cycle validates reactor stability, power output, thermal management, and safety protocols for the moon-sized battle station's primary energy source.",
    "environment": "Production",
    "build": "DS-1.0.0",
    "revision": 1,
    "status": 0,  # Draft
    "startDate": 1733529600000,  # 2025-01-06 00:00:00 UTC
    "endDate": 1765065600000,    # 2025-12-06 00:00:00 UTC
    "releaseId": release_id,
    # No cyclePhases for now - we'll add phases later once we understand treePhaseId
}

print("Cycle Payload:")
print(json.dumps(cycle_payload, indent=2))
print()

# Create cycle
url = f"{full_url}/cycle"
try:
    response = requests.post(url, headers=headers, json=cycle_payload, timeout=30)
    
    if response.status_code in [200, 201]:
        created_cycle = response.json()
        
        # Extract cycle ID (handle wrapped responses)
        cycle_id = None
        cycle_data = created_cycle
        
        if isinstance(created_cycle, dict):
            # Check for wrapper keys
            for key in ["cycleDto", "dto", "cycle"]:
                if key in created_cycle:
                    cycle_data = created_cycle[key]
                    break
            
            cycle_id = cycle_data.get("id") if isinstance(cycle_data, dict) else None
        
        print("=" * 80)
        print("SUCCESS: Cycle Created!")
        print("=" * 80)
        print(f"\nCycle ID: {cycle_id}")
        print(f"Cycle Name: {cycle_data.get('name') if isinstance(cycle_data, dict) else 'N/A'}")
        print(f"Release ID: {cycle_data.get('releaseId') if isinstance(cycle_data, dict) else 'N/A'}")
        print(f"Status: {cycle_data.get('status') if isinstance(cycle_data, dict) else 'N/A'}")
        print(f"\nFull Response:")
        print(json.dumps(created_cycle, indent=2))
        
        # Verify it's accessible
        print(f"\nVerifying cycle access...")
        verify_url = f"{full_url}/cycle/release/{release_id}"
        verify_response = requests.get(verify_url, headers=headers, timeout=10)
        if verify_response.status_code == 200:
            all_cycles = verify_response.json()
            found = any(c.get("id") == cycle_id for c in all_cycles)
            if found:
                print(f"OK: Cycle {cycle_id} found in release cycles list")
            else:
                print(f"WARNING: Cycle {cycle_id} not found in release cycles list")
        
        print(f"\n" + "=" * 80)
        print("METADATA CHECK")
        print("=" * 80)
        print("\nChecking cycle metadata fields:")
        if isinstance(cycle_data, dict):
            required_fields = ["id", "name", "releaseId", "startDate", "endDate", "status"]
            optional_fields = ["description", "environment", "build", "revision", "createdDate", "cyclePhases"]
            
            print("\nRequired fields:")
            for field in required_fields:
                if field in cycle_data:
                    print(f"  OK: {field} = {cycle_data[field]}")
                else:
                    print(f"  MISSING: {field}")
            
            print("\nOptional fields present:")
            for field in optional_fields:
                if field in cycle_data:
                    value = cycle_data[field]
                    if field == "cyclePhases" and isinstance(value, list):
                        print(f"  - {field} = [{len(value)} phase(s)]")
                    else:
                        print(f"  - {field} = {value}")
        
        print(f"\n" + "=" * 80)
        print("MANUAL VERIFICATION")
        print("=" * 80)
        print(f"\nPlease check in Zephyr UI:")
        print(f"  1. Go to project ID: {test_project_id} (SpectraTestProject)")
        print(f"  2. Open release ID: {release_id} ('The Death Star Project - Phase 1')")
        print(f"  3. Check Cycles section")
        print(f"  4. Look for: 'Death Star Core Reactor Testing'")
        print(f"  5. Verify cycle ID: {cycle_id}")
        print(f"  6. Check all metadata fields are present")
        print(f"  7. Try opening the cycle to verify it's accessible")
        
    else:
        print(f"\nERROR: HTTP {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        try:
            error_data = response.json()
            print(f"\nError Details:")
            print(json.dumps(error_data, indent=2))
        except:
            pass
        
        exit(1)
        
except requests.exceptions.RequestException as e:
    print(f"\nERROR: Request failed: {e}")
    exit(1)
except Exception as e:
    print(f"\nERROR: {e}")
    exit(1)

