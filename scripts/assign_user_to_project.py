"""Assign current user to SpectraTestProject.

Attempts to add the API token user to the project using PUT /project endpoint.
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
    print("❌ API token not found")
    exit(1)

base_url = "https://velonetic.yourzephyr.com"
base_path = "/flex/services/rest/latest"
full_url = f"{base_url}{base_path}"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Get SpectraTestProject
print("🔍 Finding SpectraTestProject...")
projects_response = requests.get(f"{full_url}/project/details", headers=headers, timeout=10)
projects_response.raise_for_status()
projects = projects_response.json()

spectra_test_project = None
for project in projects:
    if project.get("name") == "SpectraTestProject":
        spectra_test_project = project
        break

if not spectra_test_project:
    print("❌ SpectraTestProject not found")
    exit(1)

project_id = spectra_test_project["id"]
print(f"✅ Found SpectraTestProject (ID: {project_id})")
print(f"   Current members: {spectra_test_project.get('members', [])}\n")

# Try to assign user - test different payload formats
print("🔧 Attempting to assign user to project...")
print("   Endpoint: PUT /project")

# Approach 1: Just project ID (might auto-assign current user)
print("\n   Approach 1: Minimal payload (project ID only)...")
payload1 = {
    "id": project_id
}

try:
    response = requests.put(f"{full_url}/project", headers=headers, json=payload1, timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Success!")
        print(f"   Response: {json.dumps(response.json(), indent=2)[:500]}")
    else:
        print(f"   Response: {response.text[:300]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Approach 2: Project with empty members array (might trigger assignment)
print("\n   Approach 2: Project with members array...")
payload2 = {
    "id": project_id,
    "members": []
}

try:
    response = requests.put(f"{full_url}/project", headers=headers, json=payload2, timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Success!")
        print(f"   Response: {json.dumps(response.json(), indent=2)[:500]}")
    else:
        print(f"   Response: {response.text[:300]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Approach 3: Try with userId (if we can infer it)
# The API might use the token to identify the user
print("\n   Approach 3: Check if we can get current user info...")

# Try getting projects for current user to see if there's a pattern
user_projects_response = requests.get(f"{full_url}/project/user", headers=headers, timeout=10)
if user_projects_response.status_code == 200:
    user_projects = user_projects_response.json()
    print(f"   ✅ Found {len(user_projects)} projects for current user")
    if user_projects:
        print(f"   Sample project structure: {json.dumps(user_projects[0] if isinstance(user_projects, list) else user_projects, indent=2)[:300]}")
else:
    print(f"   Could not fetch user projects (status: {user_projects_response.status_code})")

print("\n📝 Note: Check Zephyr API docs at: https://zephyrenterprisev3.docs.apiary.io")
print("   Look for 'Assign User to Project' endpoint documentation")

