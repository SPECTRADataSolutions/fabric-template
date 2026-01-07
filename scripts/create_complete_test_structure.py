"""Create complete test structure in SpectraTestProject.

This utility demonstrates the complete workflow:
1. Create folder in Test Repository
2. Create requirement
3. Create testcase (in folder)
4. Allocate testcase to requirement
5. Create execution (testcase in cycle)
6. Update execution status

This gives us complete schema understanding and validates the workflow.
"""
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time
import sys

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir.parent))

from scripts.zephyr_utils import get_test_project_id, get_api_credentials

# Get credentials and project ID
api_token, base_url, base_path, full_url = get_api_credentials()
project_id = get_test_project_id()

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

output_dir = Path(__file__).parent.parent / "docs" / "schemas" / "discovered"
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("CREATING COMPLETE TEST STRUCTURE")
print("=" * 80)
print(f"Project ID: {project_id}\n")

created_entities = {}

# Get existing release and cycle (from previous discovery)
print("[INFO] Checking for existing release and cycle...")
releases_response = requests.get(f"{full_url}/release/project/{project_id}", headers=headers, timeout=10)
if releases_response.status_code == 200:
    releases = releases_response.json()
    if isinstance(releases, list) and releases:
        release = releases[-1]  # Use most recent
        release_id = release.get("id")
        print(f"   [OK] Using existing Release ID: {release_id}")
        
        # Get cycles for this release
        cycles_response = requests.get(f"{full_url}/cycle/release/{release_id}", headers=headers, timeout=10)
        if cycles_response.status_code == 200:
            cycles_data = cycles_response.json()
            cycles = cycles_data if isinstance(cycles_data, list) else [cycles_data]
            if cycles:
                cycle = cycles[-1]
                cycle_id = cycle.get("id")
                print(f"   [OK] Using existing Cycle ID: {cycle_id}")
                created_entities["release_id"] = release_id
                created_entities["cycle_id"] = cycle_id
            else:
                print(f"   [WARN] No cycles found, will create one")
                created_entities["release_id"] = release_id
        else:
            print(f"   [WARN] Could not fetch cycles")
    else:
        print(f"   [WARN] No releases found, will create one")
else:
    print(f"   [WARN] Could not fetch releases")

# Step 1: Create Folder in Test Repository
print("\n" + "=" * 80)
print("1. CREATING FOLDER IN TEST REPOSITORY")
print("=" * 80)

# Try different payloads for folder creation
# Option 1: Omit parentId entirely (might be required)
folder_payload = {
    "name": "SPECTRA Test Folder",
    "projectId": project_id
}

print(f"   POST /testcasetree")
print(f"   Payload: {json.dumps(folder_payload, indent=2)}")

try:
    folder_response = requests.post(f"{full_url}/testcasetree", headers=headers, json=folder_payload, timeout=10)
    folder_response.raise_for_status()
    
    folder_data = folder_response.json()
    folder_id = folder_data.get("id") if isinstance(folder_data, dict) else None
    
    # Save schema
    folder_file = output_dir / "folder_created_response.json"
    with open(folder_file, "w") as f:
        json.dump(folder_data, f, indent=2)
    
    print(f"   [OK] Folder created: ID {folder_id}")
    print(f"   [SAVED] Saved to: {folder_file}")
    created_entities["folder_id"] = folder_id
    created_entities["tcrCatalogTreeId"] = folder_id
    
except requests.exceptions.HTTPError as e:
    print(f"   [ERROR] HTTP Error: {e.response.status_code}")
    print(f"   Response: {e.response.text[:500]}")
    created_entities["folder_id"] = None
except Exception as e:
    print(f"   [ERROR] Error: {e}")
    created_entities["folder_id"] = None

if created_entities.get("folder_id"):
    time.sleep(1)
    
    # Step 2: Create Requirement
    print("\n" + "=" * 80)
    print("2. CREATING REQUIREMENT")
    print("=" * 80)
    
    requirement_payload = {
        "name": "SPECTRA Test Requirement",
        "projectId": project_id,
        "description": "Test requirement for schema discovery and validation"
    }
    
    print(f"   POST /requirement")
    
    try:
        req_response = requests.post(f"{full_url}/requirement", headers=headers, json=requirement_payload, timeout=10)
        req_response.raise_for_status()
        
        req_data = req_response.json()
        req_id = req_data.get("id") if isinstance(req_data, dict) else None
        
        req_file = output_dir / "requirement_created_response.json"
        with open(req_file, "w") as f:
            json.dump(req_data, f, indent=2)
        
        print(f"   [OK] Requirement created: ID {req_id}")
        print(f"   [SAVED] Saved to: {req_file}")
        created_entities["requirement_id"] = req_id
        
    except requests.exceptions.HTTPError as e:
        print(f"   [ERROR] HTTP Error: {e.response.status_code}")
        print(f"   Response: {e.response.text[:500]}")
        created_entities["requirement_id"] = None
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        created_entities["requirement_id"] = None
    
    if created_entities.get("requirement_id"):
        time.sleep(1)
        
        # Step 3: Create Testcase (in folder)
        print("\n" + "=" * 80)
        print("3. CREATING TESTCASE IN FOLDER")
        print("=" * 80)
        
        testcase_payload = {
            "testcase": {
                "name": "SPECTRA Testcase",
                "projectId": project_id,
                "tcrCatalogTreeId": created_entities["folder_id"],
                "description": "Test testcase for schema discovery"
            }
        }
        
        print(f"   POST /testcase")
        print(f"   Using tcrCatalogTreeId: {created_entities['folder_id']}")
        
        try:
            tc_response = requests.post(f"{full_url}/testcase", headers=headers, json=testcase_payload, timeout=10)
            tc_response.raise_for_status()
            
            tc_data = tc_response.json()
            # Extract testcase from wrapper if needed
            if isinstance(tc_data, dict):
                if "testcaseDto" in tc_data:
                    tc_entity = tc_data["testcaseDto"]
                elif "id" in tc_data:
                    tc_entity = tc_data
                else:
                    tc_entity = tc_data
            else:
                tc_entity = tc_data
            
            tc_id = tc_entity.get("id") if isinstance(tc_entity, dict) else None
            
            tc_file = output_dir / "testcase_created_response.json"
            with open(tc_file, "w") as f:
                json.dump(tc_data, f, indent=2)
            
            print(f"   [OK] Testcase created: ID {tc_id}")
            print(f"   [SAVED] Saved to: {tc_file}")
            created_entities["testcase_id"] = tc_id
            
            if tc_id and created_entities.get("requirement_id"):
                time.sleep(1)
                
                # Step 4: Allocate Testcase to Requirement
                print("\n" + "=" * 80)
                print("4. ALLOCATING TESTCASE TO REQUIREMENT")
                print("=" * 80)
                
                allocate_payload = {
                    "testcaseId": tc_id,
                    "requirementId": created_entities["requirement_id"]
                }
                
                print(f"   POST /testcase/allocate/requirement")
                
                try:
                    alloc_response = requests.post(
                        f"{full_url}/testcase/allocate/requirement",
                        headers=headers,
                        json=allocate_payload,
                        timeout=10
                    )
                    alloc_response.raise_for_status()
                    
                    print(f"   [OK] Testcase allocated to requirement")
                    created_entities["allocation_success"] = True
                    
                except requests.exceptions.HTTPError as e:
                    print(f"   [ERROR] HTTP Error: {e.response.status_code}")
                    print(f"   Response: {e.response.text[:500]}")
                    created_entities["allocation_success"] = False
                except Exception as e:
                    print(f"   [ERROR] Error: {e}")
                    created_entities["allocation_success"] = False
                
                if tc_id and created_entities.get("cycle_id"):
                    time.sleep(1)
                    
                    # Step 5: Create Execution (schedule testcase in cycle)
                    print("\n" + "=" * 80)
                    print("5. CREATING EXECUTION (Schedule Testcase in Cycle)")
                    print("=" * 80)
                    
                    execution_payload = {
                        "cycleId": created_entities["cycle_id"],
                        "testcaseId": tc_id,
                        "status": 0  # Not Executed
                    }
                    
                    print(f"   POST /execution")
                    print(f"   Cycle ID: {created_entities['cycle_id']}")
                    print(f"   Testcase ID: {tc_id}")
                    
                    try:
                        exec_response = requests.post(
                            f"{full_url}/execution",
                            headers=headers,
                            json=execution_payload,
                            timeout=10
                        )
                        exec_response.raise_for_status()
                        
                        exec_data = exec_response.json()
                        exec_id = exec_data.get("id") if isinstance(exec_data, dict) else None
                        
                        exec_file = output_dir / "execution_created_response.json"
                        with open(exec_file, "w") as f:
                            json.dump(exec_data, f, indent=2)
                        
                        print(f"   [OK] Execution created: ID {exec_id}")
                        print(f"   [SAVED] Saved to: {exec_file}")
                        created_entities["execution_id"] = exec_id
                        
                    except requests.exceptions.HTTPError as e:
                        print(f"   [ERROR] HTTP Error: {e.response.status_code}")
                        print(f"   Response: {e.response.text[:500]}")
                        created_entities["execution_id"] = None
                    except Exception as e:
                        print(f"   [ERROR] Error: {e}")
                        created_entities["execution_id"] = None
        
        except requests.exceptions.HTTPError as e:
            print(f"   [ERROR] HTTP Error: {e.response.status_code}")
            print(f"   Response: {e.response.text[:500]}")
            created_entities["testcase_id"] = None
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
            created_entities["testcase_id"] = None

# Save complete workflow summary
summary = {
    "workflow_date": datetime.now().isoformat(),
    "project_id": project_id,
    "created_entities": created_entities,
    "schema_files": {
        "folder": "folder_created_response.json" if created_entities.get("folder_id") else None,
        "requirement": "requirement_created_response.json" if created_entities.get("requirement_id") else None,
        "testcase": "testcase_created_response.json" if created_entities.get("testcase_id") else None,
        "execution": "execution_created_response.json" if created_entities.get("execution_id") else None,
    }
}

summary_file = output_dir / "complete_workflow_summary.json"
with open(summary_file, "w") as f:
    json.dump(summary, f, indent=2)

print("\n" + "=" * 80)
print("WORKFLOW SUMMARY")
print("=" * 80)
print(f"Created entities: {json.dumps(created_entities, indent=2)}")
print(f"Summary: {summary_file}\n")

