#!/usr/bin/env python
"""
Experimental API Hierarchy Discovery

Purpose:
- Systematically test EVERY endpoint to discover true dependencies
- Start with simplest possible payloads
- Record what succeeds (no dependencies) vs fails (has dependencies)
- Build dependency graph from results
- Determine canonical order for data creation

Method:
1. Test each entity type with minimal payload
2. If SUCCESS → no dependencies (can create independently)
3. If FAIL → analyze error to understand what's missing
4. Build dependency tree
5. Output canonical creation order

This gives us SCIENTIFIC understanding of the API hierarchy.
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

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

BASE_URL = "https://velonetic.yourzephyr.com/flex/services/rest/latest"
PROJECT_ID = 45

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Results tracking
results = {
    "timestamp": datetime.now().isoformat(),
    "project_id": PROJECT_ID,
    "experiments": {},
    "dependency_graph": {},
    "creation_order": []
}

created_entities = {}

def test_endpoint(entity_type: str, endpoint: str, payload: Dict, wrapped: bool = False) -> Tuple[bool, Optional[int], str, Dict]:
    """
    Test an endpoint to see if it works.
    
    Returns:
        (success, entity_id, error_message, response_data)
    """
    if wrapped:
        test_payload = {entity_type: payload}
    else:
        test_payload = payload
    
    try:
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        if 200 <= response.status_code < 300:
            data = response.json()
            entity_id = data.get("id")
            return True, entity_id, "SUCCESS", data
        else:
            error_data = response.text
            try:
                error_json = response.json()
                error_msg = error_json.get("errorMsg", error_json.get("errorCode", error_data))
            except:
                error_msg = error_data
            
            return False, None, f"HTTP {response.status_code}: {error_msg[:200]}", {}
            
    except Exception as e:
        return False, None, f"Exception: {str(e)}", {}


print("="*80)
print("EXPERIMENTAL API HIERARCHY DISCOVERY")
print("="*80)
print(f"\nProject ID: {PROJECT_ID}")
print(f"Timestamp: {datetime.now().isoformat()}")
print(f"\nStrategy: Test each entity type with minimal payload to discover dependencies\n")

# ============================================================================
# EXPERIMENT 1: Test each entity type independently (no dependencies)
# ============================================================================

print("="*80)
print("PHASE 1: INDEPENDENT ENTITY TESTS (No Dependencies)")
print("="*80)

experiments = [
    {
        "entity": "release",
        "endpoint": "/release",
        "payload": {
            "projectId": PROJECT_ID,
            "name": f"Test Release {datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "description": "Minimal test release",
            "startDate": "2025-12-08",
            "globalRelease": True,
            "projectRelease": False
        },
        "wrapped": False
    },
    {
        "entity": "requirement_folder",
        "endpoint": "/requirementtree/add",
        "payload": {
            "projectId": PROJECT_ID,
            "name": f"Test Requirement Folder {datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "description": "Minimal test requirement folder"
        },
        "wrapped": False
    },
    {
        "entity": "testcase_folder",
        "endpoint": "/testcasetree",
        "payload": {
            "projectId": PROJECT_ID,
            "name": f"Test Folder {datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "description": "Minimal test folder"
        },
        "wrapped": False
    },
]

for exp in experiments:
    entity = exp["entity"]
    print(f"\n{'─'*80}")
    print(f"Testing: {entity.upper()}")
    print(f"Endpoint: POST {exp['endpoint']}")
    print(f"Payload: {json.dumps(exp['payload'], indent=2)}")
    
    success, entity_id, error, data = test_endpoint(
        entity, exp["endpoint"], exp["payload"], exp["wrapped"]
    )
    
    results["experiments"][entity] = {
        "endpoint": exp["endpoint"],
        "payload": exp["payload"],
        "success": success,
        "entity_id": entity_id,
        "error": error,
        "dependencies": "none" if success else "unknown"
    }
    
    if success:
        print(f"✅ SUCCESS - Created ID: {entity_id}")
        print(f"   → {entity} can be created independently (no dependencies)")
        created_entities[entity] = {"id": entity_id, "data": data}
        
        # Add to creation order
        if entity not in results["creation_order"]:
            results["creation_order"].append(entity)
    else:
        print(f"❌ FAILED - {error}")
        print(f"   → {entity} may have dependencies or requires different payload")
    
    time.sleep(2)  # Rate limiting

# ============================================================================
# EXPERIMENT 2: Test entities that require dependencies
# ============================================================================

print("\n" + "="*80)
print("PHASE 2: DEPENDENT ENTITY TESTS (Require Other Entities)")
print("="*80)

# Now test entities that we expect to have dependencies

if "release" in created_entities:
    release_id = created_entities["release"]["id"]
    print(f"\n{'─'*80}")
    print(f"Testing: CYCLE (depends on release)")
    print(f"Using release ID: {release_id}")
    
    # Wait for release to unlock
    print("Waiting 10 seconds for release to unlock...")
    time.sleep(10)
    
    cycle_payload = {
        "projectId": PROJECT_ID,
        "releaseId": release_id,
        "name": f"Test Cycle {datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "description": "Minimal test cycle",
        "environment": "Test",
        "build": "1.0.0",
        "status": 0,
        "startDate": int(datetime.now().timestamp() * 1000),
        "endDate": int(datetime(2025, 12, 31).timestamp() * 1000)
    }
    
    print(f"Endpoint: POST /cycle")
    print(f"Payload: {json.dumps(cycle_payload, indent=2)}")
    
    success, cycle_id, error, data = test_endpoint("cycle", "/cycle", cycle_payload, False)
    
    results["experiments"]["cycle"] = {
        "endpoint": "/cycle",
        "payload": cycle_payload,
        "success": success,
        "entity_id": cycle_id,
        "error": error,
        "dependencies": ["release"] if success else "release (but still failed)"
    }
    
    if success:
        print(f"✅ SUCCESS - Created ID: {cycle_id}")
        print(f"   → cycle depends on: release")
        created_entities["cycle"] = {"id": cycle_id, "data": data}
        results["creation_order"].append("cycle")
        results["dependency_graph"]["cycle"] = ["release"]
    else:
        print(f"❌ FAILED - {error}")
    
    time.sleep(2)

if "testcase_folder" in created_entities:
    folder_id = created_entities["testcase_folder"]["id"]
    print(f"\n{'─'*80}")
    print(f"Testing: TESTCASE (depends on folder)")
    print(f"Using folder ID: {folder_id}")
    
    testcase_payload = {
        "testcase": {  # Wrapped format
            "projectId": PROJECT_ID,
            "tcrCatalogTreeId": folder_id,
            "name": f"Test Testcase {datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "description": "Minimal test testcase",
            "priority": "Critical"
        }
    }
    
    print(f"Endpoint: POST /testcase")
    print(f"Payload: {json.dumps(testcase_payload, indent=2)}")
    
    # Testcase uses wrapped format
    response = requests.post(
        f"{BASE_URL}/testcase",
        headers=headers,
        json=testcase_payload,
        timeout=10
    )
    
    if 200 <= response.status_code < 300:
        data = response.json()
        testcase_id = data.get("id")
        success = True
        error = "SUCCESS"
        print(f"✅ SUCCESS - Created ID: {testcase_id}")
        print(f"   → testcase depends on: testcase_folder")
        created_entities["testcase"] = {"id": testcase_id, "data": data}
        results["creation_order"].append("testcase")
        results["dependency_graph"]["testcase"] = ["testcase_folder"]
    else:
        testcase_id = None
        success = False
        try:
            error_json = response.json()
            error = f"HTTP {response.status_code}: {error_json.get('errorMsg', response.text[:200])}"
        except:
            error = f"HTTP {response.status_code}: {response.text[:200]}"
        print(f"❌ FAILED - {error}")
    
    results["experiments"]["testcase"] = {
        "endpoint": "/testcase",
        "payload": testcase_payload,
        "success": success,
        "entity_id": testcase_id,
        "error": error,
        "dependencies": ["testcase_folder"] if success else "testcase_folder (but still failed)"
    }
    
    time.sleep(2)

if "cycle" in created_entities and "testcase" in created_entities:
    cycle_id = created_entities["cycle"]["id"]
    testcase_id = created_entities["testcase"]["id"]
    print(f"\n{'─'*80}")
    print(f"Testing: EXECUTION (depends on cycle + testcase)")
    print(f"Using cycle ID: {cycle_id}, testcase ID: {testcase_id}")
    
    execution_payload = {
        "cycleId": cycle_id,
        "testcaseId": testcase_id,
        "projectId": PROJECT_ID,
        "status": 1,  # Pass
        "executedBy": "mark@spectradatasolutions.com"
    }
    
    print(f"Endpoint: POST /execution")
    print(f"Payload: {json.dumps(execution_payload, indent=2)}")
    
    success, execution_id, error, data = test_endpoint("execution", "/execution", execution_payload, False)
    
    results["experiments"]["execution"] = {
        "endpoint": "/execution",
        "payload": execution_payload,
        "success": success,
        "entity_id": execution_id,
        "error": error,
        "dependencies": ["cycle", "testcase"] if success else "cycle + testcase (but still failed)"
    }
    
    if success:
        print(f"✅ SUCCESS - Created ID: {execution_id}")
        print(f"   → execution depends on: cycle, testcase")
        created_entities["execution"] = {"id": execution_id, "data": data}
        results["creation_order"].append("execution")
        results["dependency_graph"]["execution"] = ["cycle", "testcase"]
    else:
        print(f"❌ FAILED - {error}")
    
    time.sleep(2)

# ============================================================================
# RESULTS SUMMARY
# ============================================================================

print("\n" + "="*80)
print("DISCOVERY RESULTS")
print("="*80)

print("\n📊 Success Summary:")
successful = [k for k, v in results["experiments"].items() if v["success"]]
failed = [k for k, v in results["experiments"].items() if not v["success"]]

print(f"   ✅ Successful: {len(successful)}/{len(results['experiments'])}")
for entity in successful:
    print(f"      - {entity} (ID: {results['experiments'][entity]['entity_id']})")

print(f"\n   ❌ Failed: {len(failed)}/{len(results['experiments'])}")
for entity in failed:
    print(f"      - {entity}")
    print(f"        Error: {results['experiments'][entity]['error'][:100]}")

print("\n📋 Discovered Canonical Creation Order:")
for i, entity in enumerate(results["creation_order"], 1):
    deps = results["dependency_graph"].get(entity, [])
    if deps:
        print(f"   {i}. {entity} (depends on: {', '.join(deps)})")
    else:
        print(f"   {i}. {entity} (no dependencies)")

print("\n🌳 Dependency Tree:")
for entity, deps in results["dependency_graph"].items():
    print(f"   {entity} → {deps}")

# Save results
output_dir = Path(__file__).parent.parent / "validation-reports"
output_dir.mkdir(parents=True, exist_ok=True)

report_file = output_dir / f"hierarchy-discovery-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
with open(report_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n💾 Full report saved: {report_file}")

print("\n" + "="*80)
print("DISCOVERY COMPLETE")
print("="*80)

