"""Check existing projects to see member structure."""
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

# Get all projects
print("🔍 Fetching all projects to check member structures...\n")
projects_response = requests.get(f"{full_url}/project/details", headers=headers, timeout=10)
projects_response.raise_for_status()
projects = projects_response.json()

projects_with_members = []
for project in projects:
    members = project.get("members", [])
    if members:
        projects_with_members.append(project)
        print(f"✅ Project '{project.get('name')}' (ID: {project.get('id')}) has {len(members)} members:")
        print(f"   Members structure: {json.dumps(members, indent=2)[:500]}\n")

if not projects_with_members:
    print("⚠️  No projects found with members")
    print("   All projects have empty members arrays")
    print("\n💡 Suggestion: The API might handle membership differently.")
    print("   Try updating the project with a PUT request including all required fields.")

# Save to file for inspection
output_file = Path(__file__).parent.parent / "docs" / "projects_with_members.json"
output_file.parent.mkdir(parents=True, exist_ok=True)

if projects_with_members:
    with open(output_file, "w") as f:
        json.dump(projects_with_members, f, indent=2)
    print(f"💾 Saved projects with members to: {output_file}")
else:
    # Save all projects anyway for reference
    with open(output_file, "w") as f:
        json.dump(projects[:3] if len(projects) > 3 else projects, f, indent=2)
    print(f"💾 Saved sample projects to: {output_file}")

