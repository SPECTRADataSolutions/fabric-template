"""Create SpectraTestProject in Zephyr."""
import requests
import json
import os
from datetime import datetime
from pathlib import Path

# Get credentials from .env file (SPECTRA root)
spectra_root = Path(__file__).parent.parent.parent.parent
env_file = spectra_root / ".env"

# Read .env for API token
api_token = None
if env_file.exists():
    with open(env_file, "r") as f:
        for line in f:
            if line.startswith("ZEPHYR_API_TOKEN=") or line.startswith("SPECTRA_ZEPHYR_API_TOKEN="):
                api_token = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

# Fallback to Variable Library value if not in .env
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

# Base URL
base_url = "https://velonetic.yourzephyr.com"
base_path = "/flex/services/rest/latest"
full_url = f"{base_url}{base_path}"

# Project data
project_name = "SpectraTestProject"
project_description = "Comprehensive test project for SPECTRA pipeline validation and integration testing. Created via API."

# Get current date in milliseconds (timestamp format used by Zephyr)
current_timestamp = int(datetime.now().timestamp() * 1000)

project_data = {
    "name": project_name,
    "description": project_description,
    "startDate": current_timestamp,
    "active": True,
    "status": "2"  # Based on existing projects, "2" seems to be active status
}

# Make API call
endpoint = "/project"
url = f"{full_url}{endpoint}"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

print(f"🚀 Creating project: {project_name}")
print(f"📍 URL: {url}")
print(f"📦 Payload: {json.dumps(project_data, indent=2)}")

try:
    response = requests.post(url, headers=headers, json=project_data, timeout=10)
    response.raise_for_status()
    
    created_project = response.json()
    
    print(f"\n✅ Success! Project created:")
    print(f"   Name: {created_project.get('name', 'Unknown')}")
    print(f"   ID: {created_project.get('id', 'N/A')}")
    print(f"   Version: {created_project.get('version', 'N/A')}")
    print(f"   Active: {created_project.get('active', 'N/A')}")
    
    # Save to file for reference
    output_file = Path(__file__).parent.parent / "docs" / "spectra_test_project_created.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(created_project, f, indent=2)
    
    print(f"\n💾 Saved response to: {output_file}")
    
except requests.exceptions.HTTPError as e:
    print(f"\n❌ HTTP Error: {e}")
    print(f"   Status Code: {e.response.status_code}")
    print(f"   Response: {e.response.text[:500] if e.response else 'No response'}")
except requests.exceptions.RequestException as e:
    print(f"\n❌ Request Error: {e}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

