#!/usr/bin/env python
"""
Clean up all test entities from SpectraTestProject.

Delete in reverse dependency order:
1. Allocations
2. Executions
3. Cycles
4. Testcases
5. Requirements (tree nodes)
6. Releases (keep existing ones, delete test ones)
"""

import requests
import json
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

deleted = {
    "allocations": 0,
    "executions": 0,
    "cycles": 0,
    "testcases": 0,
    "requirements": 0,
    "releases": 0,
    "folders": 0
}

print("="*80)
print("CLEANUP TEST PROJECT - Delete All Test Entities")
print("="*80)
print(f"\nProject ID: {PROJECT_ID}")
print(f"Timestamp: {datetime.now().isoformat()}\n")

# 1. Delete Allocations
print("="*80)
print("1. DELETING ALLOCATIONS")
print("="*80)

response = requests.get(f"{BASE_URL}/allocation/project/{PROJECT_ID}", headers=headers, timeout=10)
if response.status_code == 200:
    allocations = response.json()
    print(f"Found {len(allocations)} allocations")
    
    for alloc in allocations:
        alloc_id = alloc.get("id")
        print(f"  Deleting allocation {alloc_id}...")
        del_response = requests.delete(f"{BASE_URL}/allocation/{alloc_id}", headers=headers, timeout=10)
        if del_response.status_code == 200:
            deleted["allocations"] += 1
            print(f"    OK")
        else:
            print(f"    FAIL - HTTP {del_response.status_code}")
else:
    print(f"Could not fetch allocations - HTTP {response.status_code}")

# 2. Delete Executions
print("\n" + "="*80)
print("2. DELETING EXECUTIONS")
print("="*80)

response = requests.get(f"{BASE_URL}/execution/project/{PROJECT_ID}", headers=headers, timeout=10)
if response.status_code == 200:
    executions = response.json()
    print(f"Found {len(executions)} executions")
    
    for execution in executions:
        exec_id = execution.get("id")
        print(f"  Deleting execution {exec_id}...")
        del_response = requests.delete(f"{BASE_URL}/execution/{exec_id}", headers=headers, timeout=10)
        if del_response.status_code == 200:
            deleted["executions"] += 1
            print(f"    OK")
        else:
            print(f"    FAIL - HTTP {del_response.status_code}")
else:
    print(f"Could not fetch executions - HTTP {response.status_code}")

# 3. Delete Cycles
print("\n" + "="*80)
print("3. DELETING CYCLES")
print("="*80)

response = requests.get(f"{BASE_URL}/cycle/project/{PROJECT_ID}", headers=headers, timeout=10)
if response.status_code == 200:
    cycles = response.json()
    print(f"Found {len(cycles)} cycles")
    
    for cycle in cycles:
        cycle_id = cycle.get("id")
        cycle_name = cycle.get("name")
        print(f"  Deleting cycle {cycle_id}: {cycle_name}...")
        del_response = requests.delete(f"{BASE_URL}/cycle/{cycle_id}", headers=headers, timeout=10)
        if del_response.status_code == 200:
            deleted["cycles"] += 1
            print(f"    OK")
        else:
            print(f"    FAIL - HTTP {del_response.status_code}")
else:
    print(f"Could not fetch cycles - HTTP {response.status_code}")

# 4. Delete Testcases
print("\n" + "="*80)
print("4. DELETING TESTCASES")
print("="*80)

response = requests.get(f"{BASE_URL}/testcase/project/{PROJECT_ID}", headers=headers, timeout=10)
if response.status_code == 200:
    testcases = response.json()
    print(f"Found {len(testcases)} testcases")
    
    for testcase in testcases:
        tc_id = testcase.get("id")
        tc_name = testcase.get("name")
        print(f"  Deleting testcase {tc_id}: {tc_name}...")
        del_response = requests.delete(f"{BASE_URL}/testcase/{tc_id}", headers=headers, timeout=10)
        if del_response.status_code == 200:
            deleted["testcases"] += 1
            print(f"    OK")
        else:
            print(f"    FAIL - HTTP {del_response.status_code}")
else:
    print(f"Could not fetch testcases - HTTP {response.status_code}")

# 5. Delete Requirements (tree nodes)
print("\n" + "="*80)
print("5. DELETING REQUIREMENTS")
print("="*80)

response = requests.get(f"{BASE_URL}/requirementtree/project/{PROJECT_ID}", headers=headers, timeout=10)
if response.status_code == 200:
    requirements = response.json()
    print(f"Found {len(requirements)} requirement tree nodes")
    
    for req in requirements:
        req_id = req.get("id")
        req_name = req.get("name")
        print(f"  Deleting requirement {req_id}: {req_name}...")
        del_response = requests.delete(f"{BASE_URL}/requirementtree/{req_id}", headers=headers, timeout=10)
        if del_response.status_code == 200:
            deleted["requirements"] += 1
            print(f"    OK")
        else:
            print(f"    FAIL - HTTP {del_response.status_code}")
else:
    print(f"Could not fetch requirements - HTTP {response.status_code}")

# 6. Delete Test Releases (keep existing project releases)
print("\n" + "="*80)
print("6. DELETING TEST RELEASES")
print("="*80)

response = requests.get(f"{BASE_URL}/release/project/{PROJECT_ID}", headers=headers, timeout=10)
if response.status_code == 200:
    releases = response.json()
    print(f"Found {len(releases)} releases")
    
    # Keep these releases (pre-existing, useful)
    keep_ids = [131, 132, 133, 134]  # The Death Star Project, Draft, Active, Completed
    keep_names = ["The Death Star Project - Phase 1", "Release 1 - Draft Status", "Release 2 - Active Status", "Release 3 - Completed Status"]
    
    for release in releases:
        rel_id = release.get("id")
        rel_name = release.get("name")
        
        # Skip if in keep list
        if rel_id in keep_ids or any(keep_name in rel_name for keep_name in keep_names):
            print(f"  KEEPING release {rel_id}: {rel_name}")
            continue
        
        # Delete test releases
        if "Test" in rel_name or "Discovery" in rel_name or "API Validation" in rel_name:
            print(f"  Deleting test release {rel_id}: {rel_name}...")
            del_response = requests.delete(f"{BASE_URL}/release/{rel_id}", headers=headers, timeout=10)
            if del_response.status_code == 200:
                deleted["releases"] += 1
                print(f"    OK")
            elif del_response.status_code == 400 and "cannot be deleted" in del_response.text:
                print(f"    SKIP - Last active release (cannot delete)")
            else:
                print(f"    FAIL - HTTP {del_response.status_code}")
        else:
            print(f"  KEEPING release {rel_id}: {rel_name}")
else:
    print(f"Could not fetch releases - HTTP {response.status_code}")

# 7. Delete Folders (if any exist)
print("\n" + "="*80)
print("7. DELETING FOLDERS")
print("="*80)

response = requests.get(f"{BASE_URL}/testcasetree/projectrepository/{PROJECT_ID}", headers=headers, timeout=10)
if response.status_code == 200:
    folders = response.json()
    print(f"Found {len(folders)} folders")
    
    for folder in folders:
        if isinstance(folder, dict):
            folder_id = folder.get("id")
            folder_name = folder.get("name", "Unknown")
            print(f"  Deleting folder {folder_id}: {folder_name}...")
            del_response = requests.delete(f"{BASE_URL}/testcasetree/{folder_id}", headers=headers, timeout=10)
            if del_response.status_code == 200:
                deleted["folders"] += 1
                print(f"    OK")
            else:
                print(f"    FAIL - HTTP {del_response.status_code}")
else:
    print(f"Could not fetch folders - HTTP {response.status_code}")

# Summary
print("\n" + "="*80)
print("CLEANUP SUMMARY")
print("="*80)

total_deleted = sum(deleted.values())

print(f"\nTotal deleted: {total_deleted}")
for entity_type, count in deleted.items():
    if count > 0:
        print(f"  - {entity_type}: {count}")

print("\n" + "="*80)
print("CLEANUP COMPLETE - Project is now clean!")
print("="*80)
print("\nReady for fresh test data creation using discovered hierarchy.")

