"""Quick script to list all projects."""
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

print("🔍 Fetching all projects...\n")
projects_response = requests.get(f"{full_url}/project/details", headers=headers, timeout=10)
projects_response.raise_for_status()
projects = projects_response.json()

print(f"Found {len(projects)} projects:\n")
for project in projects:
    name = project.get("name", "Unknown")
    project_id = project.get("id", "Unknown")
    members = project.get("members", [])
    print(f"  - {name} (ID: {project_id}) - Members: {len(members)}")

print("\n🔍 Looking for 'SpectraTestProject' or similar...")
spectra_projects = [p for p in projects if "spectra" in p.get("name", "").lower() or "test" in p.get("name", "").lower()]
if spectra_projects:
    print(f"\n✅ Found {len(spectra_projects)} matching project(s):")
    for p in spectra_projects:
        print(f"  - {p.get('name')} (ID: {p.get('id')})")
else:
    print("\n⚠️  No project found with 'spectra' or 'test' in the name")
