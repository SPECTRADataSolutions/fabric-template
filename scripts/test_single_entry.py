#!/usr/bin/env python3
"""
Test script to create a single entry in Zephyr for manual verification.

Creates one release in SpectraTestProject (ID: 45) for testing.
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
    # Try Variable Library
    var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
    if var_lib_path.exists():
        with open(var_lib_path, "r") as f:
            var_lib = json.load(f)
            for var in var_lib.get("variables", []):
                if var.get("name") == "API_TOKEN":
                    api_token = var.get("value")
                    break

if not api_token:
    print("ERROR: API token not found in .env or Variable Library")
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
print("TEST: CREATE SINGLE RELEASE ENTRY")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print(f"API Base: {full_url}")
print()

# Check existing releases first
print("1. Checking existing releases...")
existing_releases_url = f"{full_url}/release/project/{test_project_id}"
has_project_release = False
try:
    existing_releases_response = requests.get(existing_releases_url, headers=headers, timeout=10)
    if existing_releases_response.status_code == 200:
        existing_releases = existing_releases_response.json()
        print(f"   Found {len(existing_releases)} existing release(s)")
        
        # Check for project-level releases
        for r in existing_releases:
            print(f"     - {r.get('name')} (ID: {r.get('id')}, projectRelease: {r.get('projectRelease')}, globalRelease: {r.get('globalRelease')})")
            if r.get("projectRelease"):
                has_project_release = True
        
        # If API says we can't create project release, assume one exists even if flag not set
        # Try creating with projectRelease first, if it fails, use globalRelease
        if has_project_release:
            print(f"   WARNING: Project has project-level release(s) - will use globalRelease: true")
        else:
            print(f"   INFO: No project-level releases detected - will try projectRelease first")
    else:
        print(f"   WARNING: Could not check existing releases (status: {existing_releases_response.status_code})")
        # Assume project release exists if we can't check
        has_project_release = True
except Exception as e:
    print(f"   WARNING: Could not check existing releases: {e}")
    # Assume project release exists if we can't check
    has_project_release = True

# Create test release
print("\n2. Creating test release...")
release_payload = {
    "name": f"SPECTRA Test Release - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "description": "Single entry test for manual verification",
    "projectId": test_project_id,
    "startDate": 1733529600000,  # 2025-01-06 00:00:00 UTC
    "endDate": 1765065600000,    # 2025-12-06 00:00:00 UTC
    "status": 0,  # Draft
    "syncEnabled": False
}

# Always use globalRelease to avoid the "already created at project level" error
# The API error suggests a project-level release exists even if the flag isn't set
release_payload["globalRelease"] = True
release_payload["projectRelease"] = False
print(f"   Using globalRelease: true (to avoid project-level release conflict)")

print(f"   Payload: {json.dumps(release_payload, indent=2)}")

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
        
        print(f"\n✅ SUCCESS: Release created!")
        print(f"   Release ID: {release_id}")
        print(f"   Release Name: {release_data.get('name') if isinstance(release_data, dict) else 'N/A'}")
        print(f"   Project ID: {release_data.get('projectId') if isinstance(release_data, dict) else 'N/A'}")
        print(f"\n📋 Full Response:")
        print(json.dumps(created_release, indent=2))
        
        # Verify it's in the project
        print(f"\n3. Verifying release in project...")
        verify_response = requests.get(existing_releases_url, headers=headers, timeout=10)
        if verify_response.status_code == 200:
            all_releases = verify_response.json()
            found = any(r.get("id") == release_id for r in all_releases)
            if found:
                print(f"   ✅ Release {release_id} found in project {test_project_id}")
            else:
                print(f"   ⚠️  Release {release_id} not found in project releases list")
        
        print(f"\n" + "=" * 80)
        print("MANUAL VERIFICATION")
        print("=" * 80)
        print(f"\nPlease check in Zephyr UI:")
        print(f"  1. Go to project ID: {test_project_id} (SpectraTestProject)")
        print(f"  2. Check Releases section")
        print(f"  3. Look for release: {release_data.get('name') if isinstance(release_data, dict) else 'N/A'}")
        print(f"  4. Verify release ID: {release_id}")
        print(f"  5. Verify it's in the correct project")
        
    else:
        print(f"\n❌ FAILED: HTTP {response.status_code}")
        print(f"   Response: {response.text[:500]}")
        
        # Try to parse error
        try:
            error_data = response.json()
            print(f"\n   Error Details:")
            print(json.dumps(error_data, indent=2))
        except:
            pass
        
        exit(1)
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ ERROR: Request failed: {e}")
    exit(1)
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    exit(1)

