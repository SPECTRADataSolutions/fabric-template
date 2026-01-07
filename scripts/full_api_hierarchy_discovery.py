#!/usr/bin/env python
"""
Full API Hierarchy Discovery - Autonomous Experimentation

Purpose:
- Test EVERY entity type with EVERY possible dependency combination
- Try multiple delays (10s, 20s, 30s, 60s)
- Try wrapped and unwrapped payloads
- Try different field variations
- Build complete dependency graph
- Determine canonical creation order

Runs autonomously until complete hierarchy is discovered.
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sys

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
    "creation_order": [],
    "blockers": []
}

created_entities = {}

def test_create(entity_type: str, endpoint: str, payload: Dict, wrapped_key: Optional[str] = None, delay_before: int = 0, notes: str = "") -> Tuple[bool, Optional[int], str, Dict]:
    """Test entity creation with optional delay and wrapping."""
    if delay_before > 0:
        print(f"   Waiting {delay_before} seconds... {notes}")
        time.sleep(delay_before)
    
    test_payload = {wrapped_key: payload} if wrapped_key else payload
    
    try:
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            headers=headers,
            json=test_payload,
            timeout=15
        )
        
        if 200 <= response.status_code < 300:
            data = response.json()
            entity_id = data.get("id")
            return True, entity_id, "SUCCESS", data
        else:
            try:
                error_json = response.json()
                error_msg = error_json.get("errorMsg", error_json.get("errorCode", response.text))
            except:
                error_msg = response.text
            
            return False, None, f"HTTP {response.status_code}: {error_msg[:300]}", {}
            
    except Exception as e:
        return False, None, f"Exception: {str(e)}", {}


print("="*80)
print("FULL API HIERARCHY DISCOVERY - AUTONOMOUS EXPERIMENTATION")
print("="*80)
print(f"\nProject ID: {PROJECT_ID}")
print(f"Started: {datetime.now().isoformat()}")
print(f"\nRunning until complete hierarchy is mapped...\n")

# ============================================================================
# PHASE 1: Test independent entities (Level 0)
# ============================================================================

print("="*80)
print("PHASE 1: INDEPENDENT ENTITIES (Level 0 - No Dependencies)")
print("="*80)

# Test 1: Releases
print(f"\n{'─'*80}")
print("EXPERIMENT 1: RELEASE")

ts = datetime.now().strftime('%Y%m%d-%H%M%S')
release_payload = {
    "projectId": PROJECT_ID,
    "name": f"Discovery Test Release {ts}",
    "description": "Hierarchy discovery experiment",
    "startDate": "2025-12-08",
    "globalRelease": True,
    "projectRelease": False
}

success, release_id, error, data = test_create("release", "/release", release_payload)
results["experiments"]["release"] = {"success": success, "id": release_id, "error": error, "level": 0, "dependencies": []}

if success:
    print(f"✅ PASS - Release ID: {release_id}")
    created_entities["release"] = {"id": release_id, "data": data}
    results["creation_order"].append("release")
else:
    print(f"❌ FAIL - {error}")
    results["blockers"].append({"entity": "release", "error": error})

time.sleep(2)

# Test 2: Requirement Folders
print(f"\n{'─'*80}")
print("EXPERIMENT 2: REQUIREMENT FOLDER")

ts = datetime.now().strftime('%Y%m%d-%H%M%S')
req_folder_payload = {
    "projectId": PROJECT_ID,
    "name": f"Discovery Test Req Folder {ts}",
    "description": "Hierarchy discovery experiment"
}

success, req_folder_id, error, data = test_create("requirement_folder", "/requirementtree/add", req_folder_payload)
results["experiments"]["requirement_folder"] = {"success": success, "id": req_folder_id, "error": error, "level": 0, "dependencies": []}

if success:
    print(f"✅ PASS - Requirement Folder ID: {req_folder_id}")
    created_entities["requirement_folder"] = {"id": req_folder_id, "data": data}
    results["creation_order"].append("requirement_folder")
else:
    print(f"❌ FAIL - {error}")
    results["blockers"].append({"entity": "requirement_folder", "error": error})

time.sleep(2)

# Test 3: Testcase Folders (Known blocker, but try variations)
print(f"\n{'─'*80}")
print("EXPERIMENT 3: TESTCASE FOLDER (Multiple Attempts)")

ts = datetime.now().strftime('%Y%m%d-%H%M%S')

# Attempt 3.1: Direct payload (no parentId)
print("\n   Attempt 3.1: Direct payload (omit parentId)")
folder_payload_v1 = {
    "projectId": PROJECT_ID,
    "name": f"Discovery Folder v1 {ts}",
    "description": "Test folder creation"
}

success_v1, folder_id_v1, error_v1, data_v1 = test_create("testcase_folder_v1", "/testcasetree", folder_payload_v1)
print(f"      Result: {'PASS' if success_v1 else 'FAIL'} - {error_v1}")

# Attempt 3.2: With parentId: 0
print("\n   Attempt 3.2: With parentId: 0")
folder_payload_v2 = {
    "projectId": PROJECT_ID,
    "name": f"Discovery Folder v2 {ts}",
    "description": "Test folder creation",
    "parentId": 0
}

success_v2, folder_id_v2, error_v2, data_v2 = test_create("testcase_folder_v2", "/testcasetree", folder_payload_v2)
print(f"      Result: {'PASS' if success_v2 else 'FAIL'} - {error_v2}")

# Attempt 3.3: Wrapped payload
print("\n   Attempt 3.3: Wrapped payload")
success_v3, folder_id_v3, error_v3, data_v3 = test_create("testcase_folder_v3", "/testcasetree", folder_payload_v1, wrapped_key="folder")
print(f"      Result: {'PASS' if success_v3 else 'FAIL'} - {error_v3}")

# Attempt 3.4: Different endpoint /testcasetree/add
print("\n   Attempt 3.4: Try /testcasetree/add endpoint")
success_v4, folder_id_v4, error_v4, data_v4 = test_create("testcase_folder_v4", "/testcasetree/add", folder_payload_v1)
print(f"      Result: {'PASS' if success_v4 else 'FAIL'} - {error_v4}")

testcase_folder_id = folder_id_v1 or folder_id_v2 or folder_id_v3 or folder_id_v4

if testcase_folder_id:
    print(f"\n✅ SUCCESS - Testcase Folder ID: {testcase_folder_id}")
    created_entities["testcase_folder"] = {"id": testcase_folder_id, "data": data_v1 or data_v2 or data_v3 or data_v4}
    results["creation_order"].append("testcase_folder")
    results["experiments"]["testcase_folder"] = {"success": True, "id": testcase_folder_id, "level": 0, "dependencies": []}
else:
    print(f"\n❌ ALL FAILED - Testcase folders blocked (BLOCKER-002)")
    results["experiments"]["testcase_folder"] = {"success": False, "id": None, "error": error_v1, "level": 0, "dependencies": []}
    results["blockers"].append({"entity": "testcase_folder", "error": "All attempts failed - API broken"})

time.sleep(2)

# ============================================================================
# PHASE 2: Test dependent entities (Level 1)
# ============================================================================

print("\n" + "="*80)
print("PHASE 2: DEPENDENT ENTITIES (Level 1)")
print("="*80)

# Test 4: Cycles (depend on releases) - Try multiple delays
print(f"\n{'─'*80}")
print("EXPERIMENT 4: CYCLE (depends on release) - Multiple Delay Tests")

if "release" in created_entities:
    release_id = created_entities["release"]["id"]
    
    for delay in [15, 30, 60]:
        print(f"\n   Attempt 4.{delay//15}: {delay}-second delay")
        print(f"   Using release ID: {release_id}")
        
        ts = datetime.now().strftime('%Y%m%d-%H%M%S')
        cycle_payload = {
            "projectId": PROJECT_ID,
            "releaseId": release_id,
            "name": f"Discovery Cycle {ts}",
            "description": "Hierarchy discovery experiment",
            "environment": "Test",
            "build": "1.0.0",
            "status": 0,
            "startDate": int(datetime.now().timestamp() * 1000),
            "endDate": int(datetime(2025, 12, 31).timestamp() * 1000)
        }
        
        success, cycle_id, error, data = test_create("cycle", "/cycle", cycle_payload, delay_before=delay, notes="(waiting for release unlock)")
        
        if success:
            print(f"      ✅ SUCCESS with {delay}s delay - Cycle ID: {cycle_id}")
            created_entities["cycle"] = {"id": cycle_id, "data": data}
            results["creation_order"].append("cycle")
            results["dependency_graph"]["cycle"] = ["release"]
            results["experiments"]["cycle"] = {"success": True, "id": cycle_id, "level": 1, "dependencies": ["release"], "delay_required": delay}
            break
        else:
            print(f"      ❌ FAIL with {delay}s delay - {error[:150]}")
            if delay == 60:
                results["experiments"]["cycle"] = {"success": False, "id": None, "error": error, "level": 1, "dependencies": ["release"], "note": "Failed even with 60s delay"}
        
        time.sleep(2)
else:
    print("   SKIPPED - No release created")

# Test 5: Testcases (depend on folders)
print(f"\n{'─'*80}")
print("EXPERIMENT 5: TESTCASE (depends on testcase_folder)")

if "testcase_folder" in created_entities:
    folder_id = created_entities["testcase_folder"]["id"]
    print(f"   Using folder ID: {folder_id}")
    
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # Attempt 5.1: Wrapped payload (research says this is required)
    print("\n   Attempt 5.1: Wrapped payload")
    testcase_payload = {
        "testcase": {
            "projectId": PROJECT_ID,
            "tcrCatalogTreeId": folder_id,
            "name": f"Discovery Testcase {ts}",
            "description": "Hierarchy discovery experiment",
            "priority": "Critical"
        }
    }
    
    response = requests.post(f"{BASE_URL}/testcase", headers=headers, json=testcase_payload, timeout=15)
    
    if 200 <= response.status_code < 300:
        data = response.json()
        testcase_id = data.get("id")
        print(f"      ✅ SUCCESS - Testcase ID: {testcase_id}")
        created_entities["testcase"] = {"id": testcase_id, "data": data}
        results["creation_order"].append("testcase")
        results["dependency_graph"]["testcase"] = ["testcase_folder"]
        results["experiments"]["testcase"] = {"success": True, "id": testcase_id, "level": 1, "dependencies": ["testcase_folder"]}
    else:
        try:
            error_json = response.json()
            error = f"HTTP {response.status_code}: {error_json.get('errorMsg', response.text[:200])}"
        except:
            error = f"HTTP {response.status_code}: {response.text[:200]}"
        print(f"      ❌ FAIL - {error}")
        results["experiments"]["testcase"] = {"success": False, "id": None, "error": error, "level": 1, "dependencies": ["testcase_folder"]}
    
    time.sleep(2)
else:
    print("   SKIPPED - No testcase folder created (blocked by BLOCKER-002)")
    results["experiments"]["testcase"] = {"success": False, "id": None, "error": "Blocked by testcase_folder failure", "level": 1, "dependencies": ["testcase_folder"]}

# Test 6: Requirements (actual requirements, not folders)
print(f"\n{'─'*80}")
print("EXPERIMENT 6: REQUIREMENT (actual requirement)")

if "requirement_folder" in created_entities:
    req_folder_id = created_entities["requirement_folder"]["id"]
    print(f"   Using requirement folder ID: {req_folder_id}")
    
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # Attempt 6.1: POST /requirement (documented but known broken)
    print("\n   Attempt 6.1: POST /requirement (documented endpoint)")
    req_payload_v1 = {
        "projectId": PROJECT_ID,
        "name": f"Discovery Requirement {ts}",
        "description": "Test requirement creation",
        "priority": "P1"
    }
    
    success_v1, req_id_v1, error_v1, data_v1 = test_create("requirement_v1", "/requirement", req_payload_v1)
    print(f"      Result: {'PASS' if success_v1 else 'FAIL'} - {error_v1[:150]}")
    
    # Attempt 6.2: POST /requirementtree/add WITH parentId (creates subfolder/requirement)
    print("\n   Attempt 6.2: POST /requirementtree/add with parentId")
    req_payload_v2 = {
        "projectId": PROJECT_ID,
        "name": f"Discovery Requirement v2 {ts}",
        "description": "Test requirement as tree node",
        "parentId": req_folder_id
    }
    
    success_v2, req_id_v2, error_v2, data_v2 = test_create("requirement_v2", "/requirementtree/add", req_payload_v2)
    print(f"      Result: {'PASS' if success_v2 else 'FAIL'} - {error_v2[:150]}")
    
    requirement_id = req_id_v1 or req_id_v2
    
    if requirement_id:
        print(f"\n✅ SUCCESS - Requirement ID: {requirement_id}")
        created_entities["requirement"] = {"id": requirement_id, "data": data_v1 or data_v2}
        results["creation_order"].append("requirement")
        results["dependency_graph"]["requirement"] = ["requirement_folder"]
        results["experiments"]["requirement"] = {"success": True, "id": requirement_id, "level": 1, "dependencies": ["requirement_folder"]}
    else:
        print(f"\n❌ ALL FAILED - Requirements blocked")
        results["experiments"]["requirement"] = {"success": False, "id": None, "error": error_v1, "level": 1, "dependencies": ["requirement_folder"]}
        results["blockers"].append({"entity": "requirement", "error": "POST /requirement broken, /requirementtree/add creates folders"})
else:
    print("   SKIPPED - No requirement folder created")

time.sleep(2)

# ============================================================================
# PHASE 3: Test Level 2 dependencies
# ============================================================================

print("\n" + "="*80)
print("PHASE 3: LEVEL 2 DEPENDENCIES")
print("="*80)

# Test 7: Executions (depend on cycle + testcase)
print(f"\n{'─'*80}")
print("EXPERIMENT 7: EXECUTION (depends on cycle + testcase)")

if "cycle" in created_entities and "testcase" in created_entities:
    cycle_id = created_entities["cycle"]["id"]
    testcase_id = created_entities["testcase"]["id"]
    print(f"   Using cycle ID: {cycle_id}, testcase ID: {testcase_id}")
    
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # Attempt 7.1: Direct payload
    print("\n   Attempt 7.1: Direct payload")
    execution_payload = {
        "cycleId": cycle_id,
        "testcaseId": testcase_id,
        "projectId": PROJECT_ID,
        "status": 1,
        "executedBy": "mark@spectradatasolutions.com"
    }
    
    success_v1, exec_id_v1, error_v1, data_v1 = test_create("execution_v1", "/execution", execution_payload)
    print(f"      Result: {'PASS' if success_v1 else 'FAIL'} - {error_v1[:150]}")
    
    # Attempt 7.2: Wrapped payload
    if not success_v1:
        print("\n   Attempt 7.2: Wrapped payload")
        success_v2, exec_id_v2, error_v2, data_v2 = test_create("execution_v2", "/execution", execution_payload, wrapped_key="execution")
        print(f"      Result: {'PASS' if success_v2 else 'FAIL'} - {error_v2[:150]}")
    else:
        success_v2 = False
        exec_id_v2 = None
    
    execution_id = exec_id_v1 or exec_id_v2
    
    if execution_id:
        print(f"\n✅ SUCCESS - Execution ID: {execution_id}")
        created_entities["execution"] = {"id": execution_id, "data": data_v1 or data_v2}
        results["creation_order"].append("execution")
        results["dependency_graph"]["execution"] = ["cycle", "testcase"]
        results["experiments"]["execution"] = {"success": True, "id": execution_id, "level": 2, "dependencies": ["cycle", "testcase"]}
    else:
        print(f"\n❌ ALL FAILED - Executions blocked")
        results["experiments"]["execution"] = {"success": False, "id": None, "error": error_v1, "level": 2, "dependencies": ["cycle", "testcase"]}
else:
    print("   SKIPPED - Missing cycle or testcase")
    results["experiments"]["execution"] = {"success": False, "id": None, "error": "Missing dependencies", "level": 2, "dependencies": ["cycle", "testcase"]}

time.sleep(2)

# ============================================================================
# PHASE 4: Test allocation (links requirements to testcases)
# ============================================================================

print("\n" + "="*80)
print("PHASE 4: RELATIONSHIPS (Allocations)")
print("="*80)

# Test 8: Allocate testcase to requirement
print(f"\n{'─'*80}")
print("EXPERIMENT 8: ALLOCATION (links requirement to testcase)")

if "requirement" in created_entities and "testcase" in created_entities:
    req_id = created_entities["requirement"]["id"]
    testcase_id = created_entities["testcase"]["id"]
    print(f"   Using requirement ID: {req_id}, testcase ID: {testcase_id}")
    
    allocation_payload = {
        "requirementId": req_id,
        "testcaseId": testcase_id
    }
    
    success, alloc_id, error, data = test_create("allocation", "/allocation", allocation_payload)
    
    if success:
        print(f"✅ SUCCESS - Allocation ID: {alloc_id}")
        results["creation_order"].append("allocation")
        results["dependency_graph"]["allocation"] = ["requirement", "testcase"]
        results["experiments"]["allocation"] = {"success": True, "id": alloc_id, "level": 2, "dependencies": ["requirement", "testcase"]}
    else:
        print(f"❌ FAIL - {error[:150]}")
        results["experiments"]["allocation"] = {"success": False, "id": None, "error": error, "level": 2, "dependencies": ["requirement", "testcase"]}
else:
    print("   SKIPPED - Missing requirement or testcase")
    results["experiments"]["allocation"] = {"success": False, "id": None, "error": "Missing dependencies", "level": 2, "dependencies": ["requirement", "testcase"]}

# ============================================================================
# RESULTS & ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("DISCOVERY RESULTS & ANALYSIS")
print("="*80)

successful = [k for k, v in results["experiments"].items() if v.get("success")]
failed = [k for k, v in results["experiments"].items() if not v.get("success")]

print(f"\n📊 Success Rate: {len(successful)}/{len(results['experiments'])} ({len(successful)/len(results['experiments'])*100:.1f}%)")

print(f"\n✅ SUCCESSFUL ({len(successful)}):")
for entity in successful:
    exp = results["experiments"][entity]
    level = exp.get("level", "?")
    deps = exp.get("dependencies", [])
    entity_id = exp.get("id")
    delay_info = f" (requires {exp.get('delay_required')}s delay)" if exp.get('delay_required') else ""
    
    if deps:
        print(f"   Level {level}: {entity} (ID: {entity_id}) → depends on: {', '.join(deps)}{delay_info}")
    else:
        print(f"   Level {level}: {entity} (ID: {entity_id}) → no dependencies{delay_info}")

print(f"\n❌ FAILED ({len(failed)}):")
for entity in failed:
    exp = results["experiments"][entity]
    error = exp.get("error", "Unknown error")
    deps = exp.get("dependencies", [])
    
    if deps and isinstance(deps, list):
        print(f"   {entity} (expected deps: {', '.join(deps)}) → {error[:150]}")
    else:
        print(f"   {entity} → {error[:150]}")

print("\n📋 CANONICAL CREATION ORDER (Discovered):")
for i, entity in enumerate(results["creation_order"], 1):
    deps = results["dependency_graph"].get(entity, [])
    exp = results["experiments"][entity]
    delay_info = f" + {exp.get('delay_required')}s delay" if exp.get('delay_required') else ""
    
    if deps:
        print(f"   {i}. {entity} (after: {', '.join(deps)}{delay_info})")
    else:
        print(f"   {i}. {entity} (independent{delay_info})")

print("\n🌳 DEPENDENCY TREE:")
for entity, deps in results["dependency_graph"].items():
    print(f"   {entity} ← {deps}")

print("\n🔴 BLOCKERS:")
for blocker in results["blockers"]:
    print(f"   - {blocker['entity']}: {blocker['error']}")

# Save results
output_dir = Path(__file__).parent.parent / "validation-reports"
output_dir.mkdir(parents=True, exist_ok=True)

report_file = output_dir / f"hierarchy-discovery-full-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
with open(report_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n💾 Full report: {report_file}")

# Generate markdown summary
summary_file = output_dir / "canonical-creation-order.md"
with open(summary_file, "w", encoding="utf-8") as f:
    f.write("# Canonical API Creation Order - Experimentally Discovered\n\n")
    f.write(f"> **Discovered:** {datetime.now().isoformat()}  \n")
    f.write(f"> **Method:** Systematic experimentation with minimal payloads  \n")
    f.write(f"> **Success Rate:** {len(successful)}/{len(results['experiments'])} ({len(successful)/len(results['experiments'])*100:.1f}%)  \n\n")
    f.write("---\n\n")
    
    f.write("## ✅ Working Creation Order\n\n")
    for i, entity in enumerate(results["creation_order"], 1):
        deps = results["dependency_graph"].get(entity, [])
        exp = results["experiments"][entity]
        entity_id = exp.get("id")
        delay_info = f" (wait {exp.get('delay_required')}s after)" if exp.get('delay_required') else ""
        
        if deps:
            f.write(f"{i}. **{entity}** (ID: {entity_id}) → depends on: {', '.join(deps)}{delay_info}\n")
        else:
            f.write(f"{i}. **{entity}** (ID: {entity_id}) → independent{delay_info}\n")
    
    f.write("\n## ❌ Blockers\n\n")
    for blocker in results["blockers"]:
        f.write(f"- **{blocker['entity']}:** {blocker['error']}\n")
    
    f.write("\n## 🌳 Dependency Graph\n\n")
    f.write("```\n")
    for entity in results["creation_order"]:
        deps = results["dependency_graph"].get(entity, [])
        if deps:
            for dep in deps:
                f.write(f"{dep} → {entity}\n")
        else:
            f.write(f"[independent] → {entity}\n")
    f.write("```\n")

print(f"📄 Summary: {summary_file}")

print("\n" + "="*80)
print("DISCOVERY COMPLETE")
print("="*80)
print(f"\nCreated Entities: {len(created_entities)}")
print(f"Blocked Entities: {len(results['blockers'])}")
print(f"Canonical Order: {' → '.join(results['creation_order'])}")

