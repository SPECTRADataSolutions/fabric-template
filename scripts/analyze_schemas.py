"""Analyze Zephyr API schemas by fetching real examples."""
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
    print("❌ API token not found")
    exit(1)

base_url = "https://velonetic.yourzephyr.com"
base_path = "/flex/services/rest/latest"
full_url = f"{base_url}{base_path}"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

output_dir = Path(__file__).parent.parent / "docs" / "schemas"
output_dir.mkdir(parents=True, exist_ok=True)

print("🔍 Analyzing Zephyr API schemas...\n")

# 1. Get a project with releases
print("1️⃣ Fetching projects to find one with releases...")
projects_response = requests.get(f"{full_url}/project/details", headers=headers, timeout=10)
projects_response.raise_for_status()
projects = projects_response.json()

if not projects:
    print("❌ No projects found")
    exit(1)

# Use first project
sample_project_id = projects[0]["id"]
print(f"   Using project ID: {sample_project_id} ({projects[0]['name']})")

# 2. Get releases for this project
print("\n2️⃣ Fetching releases for this project...")
releases_response = requests.get(
    f"{full_url}/release/project/{sample_project_id}",
    headers=headers,
    timeout=10
)
releases_response.raise_for_status()
releases = releases_response.json()

if releases:
    sample_release_id = releases[0]["id"]
    print(f"   Found {len(releases)} releases, using ID: {sample_release_id} ({releases[0].get('name', 'Unknown')})")
    
    # Save release schema
    with open(output_dir / "release_schema.json", "w") as f:
        json.dump(releases[0], f, indent=2)
    print(f"   💾 Saved release schema to: {output_dir / 'release_schema.json'}")
    
    # 3. Get cycles for this release
    print("\n3️⃣ Fetching cycles for this release...")
    cycles_response = requests.get(
        f"{full_url}/cycle/release/{sample_release_id}",
        headers=headers,
        timeout=10
    )
    cycles_response.raise_for_status()
    cycles = cycles_response.json()
    
    if cycles:
        sample_cycle_id = cycles[0]["id"]
        print(f"   Found {len(cycles)} cycles, using ID: {sample_cycle_id} ({cycles[0].get('name', 'Unknown')})")
        
        # Save cycle schema
        with open(output_dir / "cycle_schema.json", "w") as f:
            json.dump(cycles[0], f, indent=2)
        print(f"   💾 Saved cycle schema to: {output_dir / 'cycle_schema.json'}")
        
        # 4. Get testcases - try multiple endpoints
        print("\n4️⃣ Fetching testcases...")
        
        # Try getting testcases via tree ID from cycle phase
        if cycles[0].get("cyclePhases") and cycles[0]["cyclePhases"][0].get("tcrCatalogTreeId"):
            tree_id = cycles[0]["cyclePhases"][0]["tcrCatalogTreeId"]
            print(f"   Trying testcases via tree ID: {tree_id}...")
            testcases_response = requests.get(
                f"{full_url}/testcase/nodes?treeIds={tree_id}",
                headers=headers,
                timeout=10
            )
            if testcases_response.status_code == 200:
                testcases = testcases_response.json()
                if testcases:
                    print(f"   Found {len(testcases)} testcases, analyzing first one...")
                    with open(output_dir / "testcase_schema.json", "w") as f:
                        json.dump(testcases[0], f, indent=2)
                    print(f"   💾 Saved testcase schema to: {output_dir / 'testcase_schema.json'}")
                    
                    # 5. Try to get executions from cycle phase
                    if cycles[0].get("cyclePhases"):
                        sample_phase_id = cycles[0]["cyclePhases"][0]["id"]
                        print(f"\n5️⃣ Trying to fetch executions from cycle phase ID: {sample_phase_id}...")
                        
                        # Try different endpoint patterns
                        for endpoint_pattern in [
                            f"/execution/cyclephase/{sample_phase_id}",
                            f"/execution?cyclePhaseId={sample_phase_id}",
                            f"/execution/phase/{sample_phase_id}",
                        ]:
                            try:
                                executions_response = requests.get(
                                    f"{full_url}{endpoint_pattern}",
                                    headers=headers,
                                    timeout=10
                                )
                                if executions_response.status_code == 200:
                                    executions = executions_response.json()
                                    if executions and len(executions) > 0:
                                        print(f"   ✅ Found {len(executions)} executions via {endpoint_pattern}!")
                                        with open(output_dir / "execution_schema.json", "w") as f:
                                            json.dump(executions[0], f, indent=2)
                                        print(f"   💾 Saved execution schema to: {output_dir / 'execution_schema.json'}")
                                        break
                            except:
                                pass
                else:
                    print("   ⚠️ No testcases found in tree")
            else:
                print(f"   ⚠️ Could not fetch testcases (status: {testcases_response.status_code})")
    else:
        print("   ⚠️ No cycles found for this release")
        
        # Try to get testcases directly from project
        print("\n   Trying to fetch testcases from project...")
        testcases_response = requests.get(
            f"{full_url}/testcase/project/{sample_project_id}",
            headers=headers,
            timeout=10
        )
        if testcases_response.status_code == 200:
            testcases = testcases_response.json()
            if testcases:
                print(f"   Found {len(testcases)} testcases, analyzing first one...")
                with open(output_dir / "testcase_schema.json", "w") as f:
                    json.dump(testcases[0], f, indent=2)
                print(f"   💾 Saved testcase schema to: {output_dir / 'testcase_schema.json'}")
else:
    print("   ⚠️ No releases found for this project")
    print("   Trying a different project...")
    
    # Try projects 2-5
    for i in range(1, min(5, len(projects))):
        test_project_id = projects[i]["id"]
        print(f"\n   Trying project ID: {test_project_id} ({projects[i]['name']})...")
        releases_response = requests.get(
            f"{full_url}/release/project/{test_project_id}",
            headers=headers,
            timeout=10
        )
        if releases_response.status_code == 200:
            releases = releases_response.json()
            if releases:
                print(f"   ✅ Found {len(releases)} releases in this project!")
                sample_release_id = releases[0]["id"]
                with open(output_dir / "release_schema.json", "w") as f:
                    json.dump(releases[0], f, indent=2)
                print(f"   💾 Saved release schema")
                break

# Save project schema (we already have it)
with open(output_dir / "project_schema.json", "w") as f:
    json.dump(projects[0], f, indent=2)
print(f"\n💾 Saved project schema to: {output_dir / 'project_schema.json'}")

print("\n✅ Schema analysis complete!")
print(f"\n📁 All schemas saved to: {output_dir}")

