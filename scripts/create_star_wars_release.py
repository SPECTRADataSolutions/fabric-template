#!/usr/bin/env python3
"""
Create a single Star Wars-themed release with comprehensive metadata.

Star Wars Release Name: "The Death Star Project - Phase 1"
This represents the Galactic Empire's ultimate weapon development project.
"""
import requests
import json
from pathlib import Path
from datetime import datetime

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
print("CREATING STAR WARS RELEASE")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"API Base: {full_url}")
print()

# Star Wars Release: "The Death Star Project - Phase 1"
# This represents the Galactic Empire's ultimate weapon development
release_payload = {
    "name": "The Death Star Project - Phase 1",
    "description": "Galactic Empire's ultimate weapon development project. Phase 1 focuses on core reactor design, superlaser integration, and structural framework. This release tracks all test execution for the moon-sized battle station's initial construction phase.",
    "projectId": test_project_id,
    "startDate": 1733529600000,  # 2025-01-06 00:00:00 UTC (milliseconds)
    "endDate": 1765065600000,    # 2025-12-06 00:00:00 UTC (milliseconds)
    "status": 0,  # Draft (will be activated later)
    "globalRelease": True,  # Use globalRelease to avoid conflicts
    "projectRelease": False,
    "syncEnabled": False
}

print("Release Payload:")
print(json.dumps(release_payload, indent=2))
print()

# Create release
url = f"{full_url}/release"
try:
    response = requests.post(url, headers=headers, json=release_payload, timeout=30)
    
    if response.status_code in [200, 201]:
        created_release = response.json()
        
        # Extract release ID (handle wrapped responses)
        release_id = None
        release_data = created_release
        
        if isinstance(created_release, dict):
            # Check for wrapper keys
            for key in ["releaseDto", "dto", "release"]:
                if key in created_release:
                    release_data = created_release[key]
                    break
            
            release_id = release_data.get("id") if isinstance(release_data, dict) else None
        
        print("=" * 80)
        print("SUCCESS: Release Created!")
        print("=" * 80)
        print(f"\nRelease ID: {release_id}")
        print(f"Release Name: {release_data.get('name') if isinstance(release_data, dict) else 'N/A'}")
        print(f"Project ID: {release_data.get('projectId') if isinstance(release_data, dict) else 'N/A'}")
        print(f"Status: {release_data.get('status') if isinstance(release_data, dict) else 'N/A'}")
        print(f"Global Release: {release_data.get('globalRelease') if isinstance(release_data, dict) else 'N/A'}")
        print(f"\nFull Response:")
        print(json.dumps(created_release, indent=2))
        
        # Verify it's accessible
        print(f"\nVerifying release access...")
        verify_url = f"{full_url}/release/project/{test_project_id}"
        verify_response = requests.get(verify_url, headers=headers, timeout=10)
        if verify_response.status_code == 200:
            all_releases = verify_response.json()
            found = any(r.get("id") == release_id for r in all_releases)
            if found:
                print(f"OK: Release {release_id} found in project releases list")
            else:
                print(f"WARNING: Release {release_id} not found in project releases list")
        
        print(f"\n" + "=" * 80)
        print("METADATA CHECK")
        print("=" * 80)
        print("\nChecking release metadata fields:")
        if isinstance(release_data, dict):
            required_fields = ["id", "name", "projectId", "startDate", "endDate", "status", "globalRelease"]
            optional_fields = ["description", "createdDate", "orderId", "hasChild", "syncEnabled"]
            
            print("\nRequired fields:")
            for field in required_fields:
                if field in release_data:
                    print(f"  OK: {field} = {release_data[field]}")
                else:
                    print(f"  MISSING: {field}")
            
            print("\nOptional fields present:")
            for field in optional_fields:
                if field in release_data:
                    print(f"  - {field} = {release_data[field]}")
        
        print(f"\n" + "=" * 80)
        print("MANUAL VERIFICATION")
        print("=" * 80)
        print(f"\nPlease check in Zephyr UI:")
        print(f"  1. Go to project ID: {test_project_id} (SpectraTestProject)")
        print(f"  2. Check Releases section")
        print(f"  3. Look for: 'The Death Star Project - Phase 1'")
        print(f"  4. Verify release ID: {release_id}")
        print(f"  5. Check all metadata fields are present")
        print(f"  6. Try opening the release to verify it's accessible")
        
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

