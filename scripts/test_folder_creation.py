"""Test folder creation with minimal payload to debug parentId: null issue."""
import requests
import json
from pathlib import Path
import sys

# Get API credentials
spectra_root = Path(__file__).parent.parent.parent.parent
env_file = spectra_root / ".env"

api_token = None
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "ZEPHYR" in line.upper() and "TOKEN" in line.upper():
                parts = line.split("=", 1)
                if len(parts) == 2:
                    api_token = parts[1].strip().strip('"').strip("'")
                    print(f"   Found token from: {parts[0]}")
                    break

# Fallback: Try Variable Library
if not api_token:
    var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
    if var_lib_path.exists():
        with open(var_lib_path, "r", encoding="utf-8") as f:
            var_lib = json.load(f)
            for var in var_lib.get("variables", []):
                if var.get("name") == "API_TOKEN":
                    api_token = var.get("value")
                    print(f"   Found token from Variable Library")
                    break

if not api_token:
    print("ERROR: API token not found")
    print(f"   Looking in: {env_file}")
    print(f"   File exists: {env_file.exists()}")
    sys.exit(1)

base_url = "https://velonetic.yourzephyr.com"
base_path = "/flex/services/rest/latest"
full_url = f"{base_url}{base_path}"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

test_project_id = 45

print("=" * 80)
print("TESTING FOLDER CREATION - MINIMAL PAYLOADS")
print("=" * 80)

# Test 1: Absolute minimal payload (name + projectId only)
print("\n1. Testing minimal payload (name + projectId only)...")
payload1 = {
    "name": "Test Folder Minimal",
    "projectId": test_project_id
}
print(f"   Payload: {json.dumps(payload1, indent=2)}")
response1 = requests.post(f"{full_url}/testcasetree", headers=headers, json=payload1, timeout=10)
print(f"   Status: {response1.status_code}")
if response1.status_code != 200:
    print(f"   Error: {response1.text}")
else:
    print(f"   Success: {response1.json()}")

# Test 2: With description (no parentId)
print("\n2. Testing with description (no parentId)...")
payload2 = {
    "name": "Test Folder With Description",
    "description": "Test folder description",
    "projectId": test_project_id
}
print(f"   Payload: {json.dumps(payload2, indent=2)}")
response2 = requests.post(f"{full_url}/testcasetree", headers=headers, json=payload2, timeout=10)
print(f"   Status: {response2.status_code}")
if response2.status_code != 200:
    print(f"   Error: {response2.text}")
else:
    print(f"   Success: {response2.json()}")

# Test 3: Check what the existing folder tree structure looks like
print("\n3. Checking existing folder tree structure...")
tree_response = requests.get(
    f"{full_url}/testcasetree/projectrepository/{test_project_id}",
    headers=headers,
    timeout=10
)
print(f"   Status: {tree_response.status_code}")
if tree_response.status_code == 200:
    tree = tree_response.json()
    print(f"   Tree structure: {json.dumps(tree, indent=2)}")
else:
    print(f"   Error: {tree_response.text}")

# Test 4: Try wrapped format
print("\n4. Testing wrapped format...")
payload4 = {
    "testcasetree": {
        "name": "Test Folder Wrapped",
        "projectId": test_project_id
    }
}
print(f"   Payload: {json.dumps(payload4, indent=2)}")
response4 = requests.post(f"{full_url}/testcasetree", headers=headers, json=payload4, timeout=10)
print(f"   Status: {response4.status_code}")
if response4.status_code != 200:
    print(f"   Error: {response4.text}")
else:
    print(f"   Success: {response4.json()}")

# Test 5: Check endpoint documentation - try different endpoint
print("\n5. Testing alternative endpoint: /testcasetree/add...")
payload5 = {
    "name": "Test Folder Add Endpoint",
    "projectId": test_project_id
}
print(f"   Payload: {json.dumps(payload5, indent=2)}")
response5 = requests.post(f"{full_url}/testcasetree/add", headers=headers, json=payload5, timeout=10)
print(f"   Status: {response5.status_code}")
if response5.status_code != 200:
    print(f"   Error: {response5.text}")
else:
    print(f"   Success: {response5.json()}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)

