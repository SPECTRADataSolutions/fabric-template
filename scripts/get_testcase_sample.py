"""Get a sample testcase via GET to understand the schema structure."""
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

# Get a sample testcase from an existing project
print("🔍 Fetching sample testcases from existing projects...\n")

# Get projects
projects_response = requests.get(f"{full_url}/project/details", headers=headers, timeout=10)
projects_response.raise_for_status()
projects = projects_response.json()

# Try to get testcases from first project
if projects:
    first_project = projects[0]
    project_id = first_project["id"]
    project_name = first_project["name"]
    
    print(f"📋 Checking project: {project_name} (ID: {project_id})")
    
    # Try GET /testcase endpoint
    testcases_url = f"{full_url}/testcase/project/{project_id}"
    print(f"   GET {testcases_url}")
    
    try:
        response = requests.get(testcases_url, headers=headers, params={"maxresults": 1}, timeout=10)
        if response.status_code == 200:
            testcases = response.json()
            print(f"   ✅ Found testcases")
            
            # Save sample
            output_file = Path(__file__).parent.parent / "docs" / "schemas" / "discovered" / "testcase_sample_from_get.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                json.dump(testcases, f, indent=2)
            
            print(f"   💾 Saved to: {output_file}")
            
            # Display structure
            if isinstance(testcases, list) and testcases:
                print(f"\n   Sample testcase structure:")
                print(json.dumps(testcases[0], indent=2)[:1000])
            elif isinstance(testcases, dict):
                print(f"\n   Testcase structure:")
                print(json.dumps(testcases, indent=2)[:1000])
                
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

