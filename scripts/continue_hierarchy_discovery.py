#!/usr/bin/env python
"""
Continue hierarchy discovery using EXISTING releases (no lock issues).

Now that we know:
- Level 0: release, requirement_folder (independent)
- Level 1: requirement (depends on requirement_folder)
- Level 1: cycle (depends on release - use existing!)

Continue testing:
- testcase (needs folder - try manual workaround)
- execution (needs cycle + testcase)
- allocation (needs requirement + testcase)
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime

# Get API token
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

BASE_URL = "https://velonetic.yourzephyr.com/flex/services/rest/latest"
PROJECT_ID = 45

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

created_entities = {}
results = {
    "timestamp": datetime.now().isoformat(),
    "experiments": {},
    "creation_order": [],
    "dependency_graph": {}
}

print("="*80)
print("CONTINUE HIERARCHY DISCOVERY - Using Existing Entities")
print("="*80)

# Use existing release (The Death Star Project)
RELEASE_ID = 131
print(f"\nUsing existing release ID: {RELEASE_ID} (The Death Star Project)")

# Create cycle with existing release
print(f"\n{'─'*80}")
print("EXPERIMENT: CYCLE (with existing release)")

ts = datetime.now().strftime('%Y%m%d-%H%M%S')
cycle_payload = {
    "projectId": PROJECT_ID,
    "releaseId": RELEASE_ID,
    "name": f"Discovery Cycle {ts}",
    "description": "Hierarchy discovery with existing release",
    "environment": "Production",
    "build": "1.0.0",
    "revision": 1,
    "status": 0,
    "startDate": int(datetime.now().timestamp() * 1000),
    "endDate": int(datetime(2025, 12, 31).timestamp() * 1000)
}

response = requests.post(f"{BASE_URL}/cycle", headers=headers, json=cycle_payload, timeout=15)

if 200 <= response.status_code < 300:
    data = response.json()
    cycle_id = data.get("id")
    print(f"✅ SUCCESS - Cycle ID: {cycle_id}")
    created_entities["cycle"] = {"id": cycle_id, "data": data}
    results["creation_order"].append("cycle")
    results["dependency_graph"]["cycle"] = ["release"]
    results["experiments"]["cycle"] = {"success": True, "id": cycle_id, "level": 1, "dependencies": ["release"]}
else:
    print(f"❌ FAIL - HTTP {response.status_code}: {response.text[:200]}")
    cycle_id = None

time.sleep(2)

# Get existing folder tree to find a folder ID
print(f"\n{'─'*80}")
print("EXPERIMENT: Get existing folder tree")

response = requests.get(
    f"{BASE_URL}/testcasetree/projectrepository/{PROJECT_ID}",
    headers=headers,
    timeout=10
)

folder_id = None
if response.status_code == 200:
    folder_tree = response.json()
    print(f"Found folder tree with {len(folder_tree)} nodes")
    
    # Try to find any folder with an ID
    for node in folder_tree:
        if isinstance(node, dict) and node.get("id"):
            folder_id = node.get("id")
            print(f"Found folder ID: {folder_id} - {node.get('name', 'Unknown')}")
            break
    
    if not folder_id:
        print("WARNING: No folders found in tree")
else:
    print(f"ERROR: HTTP {response.status_code}")

# If we have a folder, test testcase creation
if folder_id:
    print(f"\n{'─'*80}")
    print(f"EXPERIMENT: TESTCASE (with existing folder ID: {folder_id})")
    
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    testcase_payload = {
        "testcase": {
            "projectId": PROJECT_ID,
            "tcrCatalogTreeId": folder_id,
            "name": f"Discovery Testcase {ts}",
            "description": "Hierarchy discovery with existing folder",
            "priority": "Critical",
            "status": "Draft"
        }
    }
    
    response = requests.post(f"{BASE_URL}/testcase", headers=headers, json=testcase_payload, timeout=15)
    
    if 200 <= response.status_code < 300:
        data = response.json()
        testcase_id = data.get("id")
        print(f"✅ SUCCESS - Testcase ID: {testcase_id}")
        created_entities["testcase"] = {"id": testcase_id, "data": data}
        results["creation_order"].append("testcase")
        results["dependency_graph"]["testcase"] = ["testcase_folder"]
        results["experiments"]["testcase"] = {"success": True, "id": testcase_id, "level": 1, "dependencies": ["testcase_folder"]}
    else:
        print(f"❌ FAIL - HTTP {response.status_code}: {response.text[:300]}")
        testcase_id = None
    
    time.sleep(2)
else:
    print("\nSKIPPED testcase - no folder available")
    testcase_id = None

# If we have cycle + testcase, test execution
if cycle_id and testcase_id:
    print(f"\n{'─'*80}")
    print(f"EXPERIMENT: EXECUTION (cycle {cycle_id} + testcase {testcase_id})")
    
    execution_payload = {
        "cycleId": cycle_id,
        "testcaseId": testcase_id,
        "projectId": PROJECT_ID,
        "status": 1,
        "executedBy": "mark@spectradatasolutions.com"
    }
    
    response = requests.post(f"{BASE_URL}/execution", headers=headers, json=execution_payload, timeout=15)
    
    if 200 <= response.status_code < 300:
        data = response.json()
        execution_id = data.get("id")
        print(f"✅ SUCCESS - Execution ID: {execution_id}")
        created_entities["execution"] = {"id": execution_id, "data": data}
        results["creation_order"].append("execution")
        results["dependency_graph"]["execution"] = ["cycle", "testcase"]
        results["experiments"]["execution"] = {"success": True, "id": execution_id, "level": 2, "dependencies": ["cycle", "testcase"]}
    else:
        print(f"❌ FAIL - HTTP {response.status_code}: {response.text[:300]}")
else:
    print("\nSKIPPED execution - missing cycle or testcase")

# ============================================================================
# FINAL RESULTS
# ============================================================================

print("\n" + "="*80)
print("DISCOVERY RESULTS")
print("="*80)

print(f"\n📋 Canonical Creation Order:")
for i, entity in enumerate(results["creation_order"], 1):
    deps = results["dependency_graph"].get(entity, [])
    exp = results["experiments"][entity]
    entity_id = exp.get("id")
    
    if deps:
        print(f"   {i}. {entity} (ID: {entity_id}) → depends on: {', '.join(deps)}")
    else:
        print(f"   {i}. {entity} (ID: {entity_id}) → independent")

print(f"\n✅ Created Entities: {len(created_entities)}")
for entity, info in created_entities.items():
    print(f"   - {entity}: ID {info['id']}")

# Save results
output_dir = Path(__file__).parent.parent / "validation-reports"
output_dir.mkdir(parents=True, exist_ok=True)

report_file = output_dir / f"hierarchy-with-existing-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
with open(report_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"\n💾 Report: {report_file}")

print("\n" + "="*80)
print("COMPLETE")
print("="*80)

