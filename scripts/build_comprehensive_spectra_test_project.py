"""Build comprehensive SpectraTestProject with synthetic data for schema discovery.

Purpose:
- Create entities with ALL fields populated
- Test enum variations
- Discover data structures (scalar, record, array)
- Capture API responses for schema analysis

Strategy:
1. Create comprehensive entities (releases, cycles, folders, testcases, executions)
2. Capture all API responses
3. Store responses for schema discovery
4. Document what works vs what triggers validation errors
"""
import requests
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
import time
from typing import Dict, List, Optional, Any

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

base_url = "https://velonetic.yourzephyr.com"
base_path = "/flex/services/rest/latest"
full_url = f"{base_url}{base_path}"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Get TEST_PROJECT_ID from Variable Library
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
    test_project_id = 45

print(f"Using TEST_PROJECT_ID: {test_project_id}")
print(f"API Base: {full_url}\n")

# Verify project exists
print("=" * 80)
print("VERIFYING PROJECT ACCESS")
print("=" * 80)

projects_response = requests.get(f"{full_url}/project/details", headers=headers, timeout=10)
projects_response.raise_for_status()
projects = projects_response.json()

spectra_test_project = None
for project in projects:
    if project.get("id") == test_project_id:
        spectra_test_project = project
        break

if not spectra_test_project:
    print(f"ERROR: Project ID {test_project_id} not found or not accessible")
    exit(1)

print(f"OK: Project found: {spectra_test_project.get('name', 'Unknown')} (ID: {test_project_id})\n")

# Load test data templates
data_dir = Path(__file__).parent / "data"
template_file = data_dir / "comprehensive_test_data.yaml"

if not template_file.exists():
    print(f"ERROR: Template file not found: {template_file}")
    exit(1)

try:
    with open(template_file, "r") as f:
        templates = yaml.safe_load(f)
except Exception as e:
    print(f"ERROR: Could not load template file: {e}")
    print(f"   Please ensure PyYAML is installed: pip install pyyaml")
    exit(1)

# Output directory for captured responses
output_dir = Path(__file__).parent.parent / "docs" / "schemas" / "discovered" / "comprehensive"
output_dir.mkdir(parents=True, exist_ok=True)

# Track created entities
created_entities = {
    "project_id": test_project_id,
    "releases": [],
    "cycles": [],
    "folders": [],
    "testcases": [],
    "executions": [],
    "requirements": []
}

# Helper function to create entity and capture response
def create_entity(
    endpoint: str,
    payload: Dict[str, Any],
    entity_name: str,
    save_response: bool = True
) -> tuple[Optional[Dict], Optional[int]]:
    """Create entity via POST and capture full response."""
    url = f"{full_url}{endpoint}"
    
    print(f"Creating {entity_name}...")
    print(f"   Endpoint: POST {endpoint}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        created_entity = response.json()
        
        # Extract entity ID (handle wrapped responses)
        entity_data = created_entity
        entity_id = None
        
        if isinstance(created_entity, dict):
            # Check for wrapper keys
            for key in ["projectDto", "releaseDto", "cycleDto", "testcaseDto", "executionDto", "requirementDto", "dto"]:
                if key in created_entity:
                    entity_data = created_entity[key]
                    break
            
            entity_id = entity_data.get("id") if isinstance(entity_data, dict) else None
        
        if save_response:
            # Save raw response
            response_file = output_dir / f"{entity_name.lower().replace(' ', '_')}_response.json"
            with open(response_file, "w") as f:
                json.dump(created_entity, f, indent=2)
            print(f"   Saved response to: {response_file}")
        
        print(f"   OK: Created successfully! ID: {entity_id}\n")
        return entity_data, entity_id
        
    except requests.exceptions.HTTPError as e:
        print(f"   ERROR: HTTP Error: {e.response.status_code}")
        print(f"   Response: {e.response.text[:500]}\n")
        
        # Save error response for analysis
        error_file = output_dir / f"{entity_name.lower().replace(' ', '_')}_error_{e.response.status_code}.json"
        try:
            error_data = {
                "status_code": e.response.status_code,
                "payload": payload,
                "error": e.response.text
            }
            with open(error_file, "w") as f:
                json.dump(error_data, f, indent=2)
            print(f"   Saved error to: {error_file}\n")
        except:
            pass
        
        return None, None
    except Exception as e:
        print(f"   ERROR: Error: {e}\n")
        return None, None

# ============================================================================
# 1. CREATE FOLDERS (Test Repository - MUST BE FIRST)
# ============================================================================
# Correct Zephyr hierarchy: Project → Test Repository (Folders) → Testcases
# Folders must be created before testcases (testcases require tcrCatalogTreeId)

print("=" * 80)
print("1. CREATING FOLDERS (Test Repository - Required for testcases)")
print("=" * 80)

# First, get existing folder tree to understand structure
print("   Getting existing folder tree...")
folder_tree_response = requests.get(
    f"{full_url}/testcasetree/projectrepository/{test_project_id}",
    headers=headers,
    timeout=10
)

folder_tree_file = output_dir / "existing_folder_tree.json"
if folder_tree_response.status_code == 200:
    folder_tree = folder_tree_response.json()
    with open(folder_tree_file, "w") as f:
        json.dump(folder_tree, f, indent=2)
    print(f"   OK: Folder tree retrieved")
    print(f"   Saved to: {folder_tree_file}")
    
    # Analyze structure to find root folder ID
    # Structure varies - may be list or dict
    if isinstance(folder_tree, list) and folder_tree:
        # If list, first item might be root or we need to find root
        # Root typically has no parentId or parentId is null/0
        root_folder_id = None
        for node in folder_tree:
            if isinstance(node, dict):
                parent_id = node.get("parentId") or node.get("parent")
                if not parent_id or parent_id == 0:
                    root_folder_id = node.get("id") or node.get("tcrCatalogTreeId")
                    print(f"   Found root folder ID: {root_folder_id}")
                    break
    elif isinstance(folder_tree, dict):
        # If dict, might have root key or id field
        root_folder_id = folder_tree.get("id") or folder_tree.get("tcrCatalogTreeId")
        print(f"   📁 Found root folder ID: {root_folder_id}")
    else:
        root_folder_id = None
        print(f"   WARNING: Could not determine root folder ID from structure")
else:
    folder_tree = []
    root_folder_id = None
    print(f"   WARNING: Could not retrieve folder tree: {folder_tree_response.status_code}")

# Create folders using /testcasetree endpoint (exploratory)
# Note: Folder creation may require POST /testcasetree with parentId
folder_id_map = {"ROOT": root_folder_id}

for folder_template in templates.get("folders", []):
    folder_name = folder_template["name"]
    parent_id_placeholder = folder_template.get("parentId")
    
    # Skip if parent not yet created
    if parent_id_placeholder and parent_id_placeholder not in folder_id_map and parent_id_placeholder != "ROOT" and parent_id_placeholder is not None:
        print(f"   Skipping {folder_name} - parent {parent_id_placeholder} not yet created")
        continue
    
    # Add timestamp to name for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    folder_payload = {
        "name": f"{folder_name} {timestamp}",
        "description": folder_template.get("description", ""),
        "projectId": test_project_id
    }
    
    # Set parentId if specified - handle null/None correctly (omit field, don't send "null" string)
    # Research shows: API rejects parentId: null - must omit field entirely
    if parent_id_placeholder is None:
        # Root folder - omit parentId field entirely (don't add it at all)
        pass
    elif parent_id_placeholder == "ROOT":
        if root_folder_id:
            folder_payload["parentId"] = root_folder_id
        # If no root folder ID, omit parentId (creates root folder)
    else:
        # Parent is a placeholder string (e.g., "SUB1")
        actual_parent_id = folder_id_map.get(parent_id_placeholder)
        if actual_parent_id:
            folder_payload["parentId"] = actual_parent_id
        # If parent not found, omit parentId (will create at root level)
    
    # Remove order field if present (may cause issues) - Zephyr may auto-assign order
    if "order" in folder_payload:
        del folder_payload["order"]
    
    # Try creating folder - test both wrapped and unwrapped formats
    # Some Zephyr endpoints require wrapper objects
    folder_data, folder_id = create_entity(
        endpoint="/testcasetree",
        payload=folder_payload,
        entity_name=f"Folder: {folder_name}",
        save_response=True
    )
    
    # If direct fails, try wrapped format
    if not folder_id:
        wrapped_folder_payload = {"testcasetree": folder_payload}
        folder_data, folder_id = create_entity(
            endpoint="/testcasetree",
            payload=wrapped_folder_payload,
            entity_name=f"Folder (wrapped): {folder_name}",
            save_response=True
        )
    
    if folder_id:
        created_entities["folders"].append({
            "id": folder_id,
            "name": folder_name,
            "tcrCatalogTreeId": folder_id,  # May be same as id
            "parentId": folder_payload.get("parentId"),
            "template": folder_template
        })
        # Map for child folders
        folder_id_map[folder_name.replace(" ", "_").upper()] = folder_id
        time.sleep(1)

# Get actual tcrCatalogTreeId values (may differ from folder id)
print("\n   Refreshing folder tree to get tcrCatalogTreeId values...")
folder_tree_refresh = requests.get(
    f"{full_url}/testcasetree/projectrepository/{test_project_id}",
    headers=headers,
    timeout=10
)
if folder_tree_refresh.status_code == 200:
    updated_tree = folder_tree_refresh.json()
    # Match created folders to tree nodes to get tcrCatalogTreeId
    for folder in created_entities["folders"]:
        folder_name = folder["name"]
        # Search tree for matching folder name
        def find_folder_in_tree(tree, name):
            if isinstance(tree, list):
                for node in tree:
                    result = find_folder_in_tree(node, name)
                    if result:
                        return result
            elif isinstance(tree, dict):
                if tree.get("name") == name:
                    return tree.get("id") or tree.get("tcrCatalogTreeId")
                # Recursively search children
                children = tree.get("children") or tree.get("nodes") or []
                for child in children:
                    result = find_folder_in_tree(child, name)
                    if result:
                        return result
            return None
        
        tcr_id = find_folder_in_tree(updated_tree, folder_name)
        if tcr_id:
            folder["tcrCatalogTreeId"] = tcr_id

# ============================================================================
# 2. CREATE TESTCASES (Require folder IDs)
# ============================================================================

print("=" * 80)
print("2. CREATING TESTCASES (All types and priorities)")
print("=" * 80)

# Use first folder as default (or root if available)
default_folder_id = None
if created_entities["folders"]:
    default_folder_id = created_entities["folders"][0].get("tcrCatalogTreeId") or created_entities["folders"][0].get("id")
elif root_folder_id:
    default_folder_id = root_folder_id

if not default_folder_id:
    print("   WARNING: No folder available for testcase creation. Skipping testcases.")
else:
    print(f"   Using folder ID: {default_folder_id} for testcase creation\n")

    for testcase_template in templates.get("testcases", []):
        # Build testcase payload
        testcase_payload = {
            "name": testcase_template["name"],
            "description": testcase_template.get("description", ""),
            "projectId": test_project_id,
            "tcrCatalogTreeId": default_folder_id  # Required field
        }
        
        # Add optional fields if present
        if "testcaseType" in testcase_template:
            testcase_payload["testcaseType"] = testcase_template["testcaseType"]
        if "priority" in testcase_template:
            testcase_payload["priority"] = testcase_template["priority"]
        if "estimatedTime" in testcase_template:
            testcase_payload["estimatedTime"] = testcase_template["estimatedTime"]
        if "preconditions" in testcase_template:
            testcase_payload["preconditions"] = testcase_template["preconditions"]
        if "steps" in testcase_template:
            testcase_payload["steps"] = testcase_template["steps"]
        if "tags" in testcase_template:
            testcase_payload["tags"] = testcase_template["tags"]
        if "customFields" in testcase_template:
            testcase_payload["customFields"] = testcase_template["customFields"]
        if "assignedTo" in testcase_template:
            testcase_payload["assignedTo"] = testcase_template["assignedTo"]
        
        # Zephyr API requires testcase payload to be wrapped in "testcase" object
        wrapped_payload = {"testcase": testcase_payload}
        testcase_data, testcase_id = create_entity(
            endpoint="/testcase",
            payload=wrapped_payload,  # Use wrapped format (required by API)
            entity_name=f"Testcase: {testcase_template['name']}",
            save_response=True
        )
        
        if testcase_id:
            created_entities["testcases"].append({
                "id": testcase_id,
                "name": testcase_template["name"],
                "tcrCatalogTreeId": default_folder_id,
                "template": testcase_template
            })
            time.sleep(1)

# ============================================================================
# 3. CREATE RELEASES (Time-bounded containers)
# ============================================================================

print("=" * 80)
print("3. CREATING RELEASES (Multiple variations for enum testing)")
print("=" * 80)

# Always use globalRelease: true to avoid "Project Release creation not allowed" error
# The API blocks project-level releases if one already exists (even if flag isn't set)
# Using globalRelease is safer and works consistently
print(f"   INFO: Using globalRelease: true for all releases (avoids project-level release conflict)")

for release_template in templates.get("releases", []):
    release_payload = release_template.copy()
    release_payload["projectId"] = test_project_id
    
    # Add timestamp to name for uniqueness (avoid duplicate errors)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    release_payload["name"] = f"{release_template['name']} {timestamp}"
    
    # Always use globalRelease to avoid conflicts
    release_payload["globalRelease"] = True
    release_payload["projectRelease"] = False
    
    release_data, release_id = create_entity(
        endpoint="/release",
        payload=release_payload,
        entity_name=f"Release: {release_payload['name']}",
        save_response=True
    )
    
    if release_id:
        created_entities["releases"].append({
            "id": release_id,
            "name": release_payload["name"],
            "template": release_template
        })
        # CRITICAL: Wait for release to unlock before creating cycles
        # Validation discovered: Zephyr locks releases briefly after creation
        print(f"   Waiting 10 seconds for release {release_id} to unlock...")
        time.sleep(10)

# ============================================================================
# 4. CREATE CYCLES (Require release IDs)
# ============================================================================

print("=" * 80)
print("4. CREATING CYCLES (Test phase arrays and variations)")
print("=" * 80)

if not created_entities["releases"]:
    print("   WARNING: No releases created. Cannot proceed with cycles.")
else:
    for release in created_entities["releases"]:
        release_id = release["id"]
        
        for cycle_template in templates.get("cycles", []):
            cycle_payload = cycle_template.copy()
            cycle_payload["releaseId"] = release_id
            
            # Add timestamp to name for uniqueness
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            cycle_payload["name"] = f"{cycle_template['name']} {timestamp}"
            
            # Fix cycle phases - add startDate and endDate to each phase if missing
            # API requires both startDate and endDate for phases
            if "cyclePhases" in cycle_payload and cycle_payload["cyclePhases"]:
                cycle_start_date = cycle_payload.get("startDate", 1733529600000)
                cycle_end_date = cycle_payload.get("endDate", 1765065600000)
                for phase in cycle_payload["cyclePhases"]:
                    if "startDate" not in phase:
                        # Use cycle startDate as default
                        phase["startDate"] = cycle_start_date
                    if "endDate" not in phase:
                        # Use cycle endDate as default
                        phase["endDate"] = cycle_end_date
            
            cycle_data, cycle_id = create_entity(
                endpoint="/cycle",
                payload=cycle_payload,
                entity_name=f"Cycle: {cycle_template['name']} (Release {release_id})",
                save_response=True
            )
            
            if cycle_id:
                created_entities["cycles"].append({
                    "id": cycle_id,
                    "name": cycle_template["name"],
                    "releaseId": release_id,
                    "template": cycle_template
                })
                time.sleep(1)

# ============================================================================
# 5. CREATE EXECUTIONS (Require cycle ID + testcase ID)
# ============================================================================

print("=" * 80)
print("5. CREATING EXECUTIONS (All status types)")
print("=" * 80)

# Executions require cycleId and testcaseId
if not created_entities["cycles"]:
    print("   WARNING: No cycles created. Cannot create executions.")
elif not created_entities["testcases"]:
    print("   WARNING: No testcases created. Cannot create executions.")
else:
    # Use first cycle and create executions for each testcase
    first_cycle = created_entities["cycles"][0]
    cycle_id = first_cycle["id"]
    
    for testcase in created_entities["testcases"]:
        testcase_id = testcase["id"]
        
        for execution_template in templates.get("executions", []):
            execution_payload = {
                "cycleId": cycle_id,
                "testcaseId": testcase_id,
                "status": execution_template.get("status", 0)
            }
            
            # Add optional fields
            if "executedOn" in execution_template and execution_template["executedOn"]:
                execution_payload["executedOn"] = execution_template["executedOn"]
            if "executedBy" in execution_template and execution_template["executedBy"]:
                execution_payload["executedBy"] = execution_template["executedBy"]
            if "comment" in execution_template:
                execution_payload["comment"] = execution_template["comment"]
            if "defectIds" in execution_template:
                execution_payload["defectIds"] = execution_template["defectIds"]
            
            # Try wrapped and unwrapped payloads for execution
            execution_data, execution_id = create_entity(
                endpoint="/execution",
                payload=execution_payload,
                entity_name=f"Execution: {execution_template['name']} (Testcase {testcase_id})",
                save_response=True
            )
            
            # If direct fails, try wrapped format
            if not execution_id:
                wrapped_execution_payload = {"execution": execution_payload}
                execution_data, execution_id = create_entity(
                    endpoint="/execution",
                    payload=wrapped_execution_payload,
                    entity_name=f"Execution (wrapped): {execution_template['name']} (Testcase {testcase_id})",
                    save_response=True
                )
            
            if execution_id:
                created_entities["executions"].append({
                    "id": execution_id,
                    "cycleId": cycle_id,
                    "testcaseId": testcase_id,
                    "status": execution_template.get("status"),
                    "template": execution_template
                })
                time.sleep(1)
            
            # Limit executions per testcase to avoid too many
            if len([e for e in created_entities["executions"] if e["testcaseId"] == testcase_id]) >= len(templates.get("executions", [])):
                break

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("COMPREHENSIVE TEST DATA CREATION SUMMARY")
print("=" * 80)

print(f"OK: Project ID: {test_project_id}")
print(f"OK: Releases created: {len(created_entities['releases'])}")
print(f"OK: Cycles created: {len(created_entities['cycles'])}")
print(f"OK: Folders created: {len(created_entities['folders'])}")
print(f"OK: Testcases created: {len(created_entities['testcases'])}")
print(f"OK: Executions created: {len(created_entities['executions'])}")

print(f"\nAll responses saved to: {output_dir}")
print(f"\nNext steps:")
print(f"   1. Explore folder tree API to understand structure")
print(f"   2. Create folders and capture structure")
print(f"   3. Create testcases with folder node IDs")
print(f"   4. Create executions with cycle and testcase IDs")
print(f"   5. Analyze all captured responses for schema discovery")

# Save creation summary
summary_file = output_dir / "creation_summary.json"
with open(summary_file, "w") as f:
    json.dump(created_entities, f, indent=2)
print(f"\nCreation summary saved to: {summary_file}")

