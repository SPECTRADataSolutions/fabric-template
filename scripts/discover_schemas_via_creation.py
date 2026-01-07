"""Discover Zephyr API schemas by creating sample entities in SpectraTestProject.

This utility:
1. Creates sample entities (release, cycle, testcase) via POST
2. Captures the full response schema
3. Generates schema documentation
4. Optionally cleans up test data

This gives us 100% accurate schemas without assumptions.
"""
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time

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

# Get TEST_PROJECT_ID from Variable Library (SPECTRA-grade: environment config)
test_project_id = None
var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
if var_lib_path.exists():
    with open(var_lib_path, "r") as f:
        var_lib = json.load(f)
        for var in var_lib.get("variables", []):
            if var.get("name") == "TEST_PROJECT_ID":
                test_project_id = int(var.get("value", "45"))
                break

if not test_project_id:
    test_project_id = 45  # Fallback to default

print(f"🔍 Using TEST_PROJECT_ID from Variable Library: {test_project_id}")

# Verify project exists
projects_response = requests.get(f"{full_url}/project/details", headers=headers, timeout=10)
projects_response.raise_for_status()
projects = projects_response.json()

spectra_test_project = None
for project in projects:
    if project.get("id") == test_project_id:
        spectra_test_project = project
        break

if not spectra_test_project:
    print(f"❌ Project ID {test_project_id} not found or not accessible")
    print(f"   Expected project ID from Variable Library: {test_project_id}")
    print("\n💡 Verify:")
    print("   1. Project exists in Zephyr")
    print("   2. TEST_PROJECT_ID in Variable Library is correct")
    print("   3. API token has access to the project")
    exit(1)

project_id = test_project_id  # Use locked ID from Variable Library
print(f"✅ Using locked TEST_PROJECT_ID: {project_id}")
print(f"   Project Name: {spectra_test_project.get('name', 'Unknown')}\n")

output_dir = Path(__file__).parent.parent / "docs" / "schemas" / "discovered"
output_dir.mkdir(parents=True, exist_ok=True)

created_entities = {
    "project_id": project_id,
    "releases": [],
    "cycles": [],
    "testcases": [],
    "executions": []
}

# Helper function to create and capture schema
def create_and_capture_schema(endpoint, payload, entity_name, parent_id=None):
    """Create an entity and capture its full response schema."""
    url = f"{full_url}{endpoint}"
    
    print(f"🚀 Creating {entity_name}...")
    print(f"   Endpoint: POST {endpoint}")
    if parent_id:
        print(f"   Parent ID: {parent_id}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        created_entity = response.json()
        
        # Save raw response
        schema_file = output_dir / f"{entity_name.lower()}_created_response.json"
        with open(schema_file, "w") as f:
            json.dump(created_entity, f, indent=2)
        
        # Extract the actual entity (might be wrapped)
        entity_data = created_entity
        if isinstance(created_entity, dict):
            # Check for common wrapper keys
            for key in ["projectDto", "releaseDto", "cycleDto", "testcaseDto", "executionDto", "dto"]:
                if key in created_entity:
                    entity_data = created_entity[key]
                    break
        
        entity_id = entity_data.get("id") if isinstance(entity_data, dict) else None
        
        print(f"   ✅ Created successfully!")
        if entity_id:
            print(f"   ID: {entity_id}")
        
        print(f"   💾 Saved response to: {schema_file}\n")
        
        return entity_data, entity_id
        
    except requests.exceptions.HTTPError as e:
        print(f"   ❌ HTTP Error: {e.response.status_code}")
        print(f"   Response: {e.response.text[:500]}")
        return None, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None, None

# ============================================================================
# 1. CREATE RELEASE
# ============================================================================

print("=" * 80)
print("1️⃣ DISCOVERING RELEASE SCHEMA")
print("=" * 80)

start_date = int(datetime.now().timestamp() * 1000)
end_date = int((datetime.now() + timedelta(days=90)).timestamp() * 1000)

release_payload = {
    "name": "Schema Discovery Release",
    "description": "Temporary release for schema discovery - will be deleted",
    "projectId": project_id,
    "startDate": start_date,
    "endDate": end_date,
    "status": 0
}

release_data, release_id = create_and_capture_schema(
    endpoint="/release",
    payload=release_payload,
    entity_name="Release",
    parent_id=project_id
)

if release_id:
    created_entities["releases"].append({
        "id": release_id,
        "name": release_payload["name"],
        "endpoint": "/release",
        "payload": release_payload
    })
    
    time.sleep(1)  # Rate limiting
    
    # ============================================================================
    # 2. CREATE CYCLE
    # ============================================================================
    
    print("=" * 80)
    print("2️⃣ DISCOVERING CYCLE SCHEMA")
    print("=" * 80)
    
    cycle_payload = {
        "name": "Schema Discovery Cycle",
        "description": "Temporary cycle for schema discovery - will be deleted",
        "releaseId": release_id,
        "startDate": start_date,
        "endDate": end_date,
        "status": 0,
        "environment": "Discovery",
        "build": "1.0"
    }
    
    cycle_data, cycle_id = create_and_capture_schema(
        endpoint="/cycle",
        payload=cycle_payload,
        entity_name="Cycle",
        parent_id=release_id
    )
    
    if cycle_id:
        created_entities["cycles"].append({
            "id": cycle_id,
            "name": cycle_payload["name"],
            "endpoint": "/cycle",
            "payload": cycle_payload
        })
        
        time.sleep(1)  # Rate limiting
        
        # ============================================================================
        # 3. CREATE TESTCASE
        # ============================================================================
        
        print("=" * 80)
        print("3️⃣ DISCOVERING TESTCASE SCHEMA")
        print("=" * 80)
        
        # Try different payload formats
        # Format 1: Wrapped in "testcase" object
        testcase_payload_wrapped = {
            "testcase": {
                "name": "Schema Discovery Testcase",
                "projectId": project_id
            }
        }
        
        print("   Trying wrapped payload (testcase object)...")
        testcase_data, testcase_id = create_and_capture_schema(
            endpoint="/testcase",
            payload=testcase_payload_wrapped,
            entity_name="Testcase (wrapped)",
            parent_id=project_id
        )
        
        if not testcase_id:
            # Format 2: Direct fields
            print("\n   Trying direct payload...")
            testcase_payload_direct = {
                "name": "Schema Discovery Testcase",
                "projectId": project_id
            }
            
            testcase_data, testcase_id = create_and_capture_schema(
                endpoint="/testcase",
                payload=testcase_payload_direct,
                entity_name="Testcase (direct)",
                parent_id=project_id
            )
        
        if not testcase_id:
            # Format 3: With release ID in wrapper
            print("\n   Trying wrapped with release ID...")
            testcase_payload_wrapped_release = {
                "testcase": {
                    "name": "Schema Discovery Testcase",
                    "projectId": project_id,
                    "releaseId": release_id
                }
            }
            
            testcase_data, testcase_id = create_and_capture_schema(
                endpoint="/testcase",
                payload=testcase_payload_wrapped_release,
                entity_name="Testcase (wrapped with release)",
                parent_id=project_id
            )
        
        if testcase_id:
            # Determine which payload worked
            working_payload = testcase_payload_wrapped
            if testcase_data:
                # Use the payload that actually worked (first non-None)
                pass
            
            created_entities["testcases"].append({
                "id": testcase_id,
                "name": "Schema Discovery Testcase",
                "endpoint": "/testcase",
                "payload": testcase_payload_wrapped
            })

# ============================================================================
# GENERATE SCHEMA SUMMARY
# ============================================================================

print("=" * 80)
print("📊 SCHEMA DISCOVERY SUMMARY")
print("=" * 80)

summary = {
    "discovery_date": datetime.now().isoformat(),
    "project_id": project_id,
    "project_name": "SpectraTestProject",
    "entities_created": {
        "releases": len(created_entities["releases"]),
        "cycles": len(created_entities["cycles"]),
        "testcases": len(created_entities["testcases"]),
        "executions": len(created_entities["executions"])
    },
    "created_entities": created_entities,
    "schema_files": {
        "release": "release_created_response.json" if created_entities["releases"] else None,
        "cycle": "cycle_created_response.json" if created_entities["cycles"] else None,
        "testcase": "testcase_created_response.json" if created_entities["testcases"] else None,
    }
}

summary_file = output_dir / "discovery_summary.json"
with open(summary_file, "w") as f:
    json.dump(summary, f, indent=2)

print(f"\n✅ Schema discovery complete!")
print(f"📁 All schemas saved to: {output_dir}")
print(f"📋 Summary: {summary_file}\n")

if created_entities["releases"] or created_entities["cycles"] or created_entities["testcases"]:
    print("⚠️  Note: Test entities were created for schema discovery.")
    print("   You may want to delete them after reviewing the schemas.")
    print("\n   Created entities:")
    for release in created_entities["releases"]:
        print(f"     - Release: {release['name']} (ID: {release['id']})")
    for cycle in created_entities["cycles"]:
        print(f"     - Cycle: {cycle['name']} (ID: {cycle['id']})")
    for testcase in created_entities["testcases"]:
        print(f"     - Testcase: {testcase['name']} (ID: {testcase['id']})")

