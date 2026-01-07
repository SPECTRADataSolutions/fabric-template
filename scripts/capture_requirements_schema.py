#!/usr/bin/env python3
"""
Capture requirement schemas from Zephyr API after UI creation.

We created 3 requirements in the UI:
- REQ-DS-001: Planet Destruction Capability (ID: 6455)
- REQ-DS-002: Thermal Exhaust Port Security (ID: unknown)
- REQ-DS-003: Core Reactor Stability (ID: unknown)

Let's try to retrieve them via API to document the schema.
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
known_requirement_id = 6455  # REQ-DS-001

print("=" * 80)
print("CAPTURING REQUIREMENT SCHEMAS")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"Known Requirement ID: {known_requirement_id} (REQ-DS-001)")
print()

# Create output directory
output_dir = Path(__file__).parent.parent / "docs" / "schemas" / "discovered" / "requirements"
output_dir.mkdir(parents=True, exist_ok=True)

# Try to get requirement by ID
print("1. Trying to get requirement by ID...")
endpoints_to_try = [
    f"/requirement/{known_requirement_id}",
    f"/requirement/{known_requirement_id}/",
    f"/requirementtree/{known_requirement_id}",
    f"/requirementtree/{known_requirement_id}/"
]

requirement_data = None
for endpoint in endpoints_to_try:
    url = f"{full_url}{endpoint}"
    print(f"   Trying: {endpoint}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            requirement_data = response.json()
            print(f"   ✅ SUCCESS: Retrieved requirement")
            print(f"   Response structure: {type(requirement_data)}")
            break
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if requirement_data:
    output_file = output_dir / f"requirement_{known_requirement_id}_schema.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(requirement_data, f, indent=2)
    print(f"\n   💾 Saved to: {output_file}")
    print(f"\n   Full Schema:")
    print(json.dumps(requirement_data, indent=2))

# Try to get all requirements for project
print(f"\n2. Trying to get all requirements for project...")
endpoints_to_try = [
    f"/requirement/project/{test_project_id}",
    f"/requirement/project/{test_project_id}/",
    f"/requirementtree/project/{test_project_id}",
    f"/requirementtree/project/{test_project_id}/"
]

all_requirements = None
for endpoint in endpoints_to_try:
    url = f"{full_url}{endpoint}"
    print(f"   Trying: {endpoint}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            all_requirements = response.json()
            print(f"   ✅ SUCCESS: Retrieved requirements list")
            print(f"   Response type: {type(all_requirements)}")
            if isinstance(all_requirements, list):
                print(f"   Found {len(all_requirements)} requirement(s)")
            break
        else:
            print(f"   ❌ HTTP {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if all_requirements:
    output_file = output_dir / f"all_requirements_project_{test_project_id}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_requirements, f, indent=2)
    print(f"\n   💾 Saved to: {output_file}")
    
    if isinstance(all_requirements, list) and all_requirements:
        print(f"\n   Sample requirement (first one):")
        print(json.dumps(all_requirements[0], indent=2))
        
        # Find our Star Wars requirements
        print(f"\n   Looking for Star Wars requirements...")
        for req in all_requirements:
            name = req.get("name", "")
            if "REQ-DS" in name or "Planet Destruction" in name or "Exhaust Port" in name or "Core Reactor" in name:
                req_id = req.get("id")
                print(f"   ✅ Found: {name} (ID: {req_id})")
                req_file = output_dir / f"requirement_{req_id}_{name.replace(':', '_').replace(' ', '_')}.json"
                with open(req_file, "w", encoding="utf-8") as f:
                    json.dump(req, f, indent=2)
                print(f"      💾 Saved to: {req_file}")

print(f"\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
if requirement_data or all_requirements:
    print("✅ Successfully captured requirement schema(s)")
    print(f"   Output directory: {output_dir}")
    print("\n   Next steps:")
    print("   1. Review captured schemas")
    print("   2. Document in ZEPHYR-API-DISCOVERIES.md")
    print("   3. Proceed to testcases (if folders work) or investigate folders further")
else:
    print("❌ Could not capture requirements via API")
    print("   Requirements may need to be accessed differently")
    print("   Or API endpoints for requirements are still broken")

