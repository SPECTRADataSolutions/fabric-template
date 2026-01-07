"""
Test Zephyr API intelligence locally before running in Fabric.

Tests all the API endpoints we use in prepareZephyr to verify:
1. Releases endpoint works
2. Cycles endpoint works (with release filter)
3. Cycles endpoint works (direct, no filter)
4. Testcases endpoint works
5. Response structure is correct
"""

import os
import sys
import requests
import json
from pathlib import Path

# Add parent directory to path to access .env
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def load_env_file():
    """Load .env file from workspace root."""
    env_path = Path(__file__).parent.parent.parent.parent / ".env"
    env_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

def load_variable_library():
    """Load Variable Library JSON file."""
    var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
    if var_lib_path.exists():
        with open(var_lib_path, 'r') as f:
            return json.load(f)
    return None

def test_zephyr_api():
    """Test Zephyr API endpoints."""
    print("=" * 80)
    print("Testing Zephyr API Intelligence")
    print("=" * 80)
    
    # Load credentials from .env and Variable Library
    env = load_env_file()
    var_lib = load_variable_library()
    
    # Get API credentials (try multiple sources)
    base_url = env.get("ZEPHYR_BASE_URL", "https://velonetic.yourzephyr.com/flex/services/rest/latest")
    api_token = None
    
    # Try .env first
    api_token = env.get("ZEPHYR_API_TOKEN") or env.get("SPECTRA_ZEPHYR_API_TOKEN")
    
    # Try Variable Library if not in .env
    if not api_token and var_lib:
        for var in var_lib.get("variables", []):
            if var.get("name") == "API_TOKEN":
                api_token = var.get("value")
                break
    
    # Try base_url and base_path from Variable Library
    base_path = "/flex/services/rest/latest"
    if var_lib:
        for var in var_lib.get("variables", []):
            if var.get("name") == "BASE_URL":
                base_url = var.get("value", base_url)
            elif var.get("name") == "BASE_PATH":
                base_path = var.get("value", base_path)
    
    # Combine base_url and base_path
    if base_path and not base_url.endswith(base_path):
        base_url = f"{base_url.rstrip('/')}{base_path}"
    
    production_project_id = 44
    
    if not api_token:
        print("ERROR: API_TOKEN not found")
        print("Please add one of the following to .env file:")
        print("  - ZEPHYR_API_TOKEN=...")
        print("  - SPECTRA_ZEPHYR_API_TOKEN=...")
        print("Or ensure API_TOKEN is set in Variable Library (zephyrVariables.VariableLibrary/variables.json)")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    print(f"\nBase URL: {base_url}")
    print(f"Project ID: {production_project_id}")
    print(f"API Token: {'*' * 20}...{api_token[-4:] if len(api_token) > 4 else '****'}")
    
    # Test 1: Fetch releases
    print("\n" + "=" * 80)
    print("TEST 1: Fetch Releases")
    print("=" * 80)
    try:
        releases_url = f"{base_url.rstrip('/')}/release?projectId={production_project_id}"
        print(f"URL: {releases_url}")
        response = requests.get(releases_url, headers=headers, timeout=10)
        response.raise_for_status()
        releases = response.json()
        
        # Handle nested response
        if isinstance(releases, dict):
            print(f"Response is dict with keys: {list(releases.keys())}")
            if "data" in releases:
                releases = releases["data"]
            elif "items" in releases:
                releases = releases["items"]
            elif "results" in releases:
                releases = releases["results"]
        
        print(f"[OK] Found {len(releases)} releases")
        if releases:
            print(f"First release: ID={releases[0].get('id')}, Name={releases[0].get('name', 'N/A')}")
            print(f"First 5 release IDs: {[r.get('id') for r in releases[:5]]}")
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        return False
    
    # Test 2: Fetch cycles for releases (including release 1 from cycle 106)
    print("\n" + "=" * 80)
    print("TEST 2: Fetch Cycles for Release (Release-based endpoint)")
    print("=" * 80)
    release_id = releases[0].get("id") if releases else None
    if not release_id:
        print("[ERROR] No release ID available")
        return False
    
    print(f"Testing with release ID: {release_id}")
    print(f"NOTE: Project 44 has releases 112 and 106, each with cycles")
    cycles_found = False
    
    # Try releases 112 and 106 first (project 44's releases with cycles)
    test_releases = [112, 106] + [r.get("id") for r in releases[:10] if r.get("id") not in [112, 106]]
    
    for candidate_id in test_releases:
        if not candidate_id:
            continue
        
        try:
            cycles_url = f"{base_url.rstrip('/')}/cycle/release/{candidate_id}"
            print(f"  Trying release {candidate_id}: {cycles_url}")
            response = requests.get(cycles_url, headers=headers, timeout=10)
            response.raise_for_status()
            cycles = response.json()
            
            # Handle nested response
            if isinstance(cycles, dict):
                print(f"    Response is dict with keys: {list(cycles.keys())}")
                if "data" in cycles:
                    cycles = cycles["data"]
                elif "items" in cycles:
                    cycles = cycles["items"]
                elif "results" in cycles:
                    cycles = cycles["results"]
            
            if cycles and len(cycles) > 0:
                print(f"  [OK] Found {len(cycles)} cycles for release {candidate_id}")
                print(f"  First cycle keys: {list(cycles[0].keys()) if cycles else 'N/A'}")
                cycles_found = True
                release_id = candidate_id
                break
            else:
                print(f"  [WARN] No cycles for release {candidate_id}")
        except Exception as e:
            print(f"  [ERROR] Release {candidate_id} failed: {e}")
            continue
    
    if not cycles_found:
        print("[ERROR] No cycles found for any release")
    
    # Test 2b: Try fetching cycle 106 directly (from UI URL)
    print("\n" + "=" * 80)
    print("TEST 2b: Fetch Cycle 106 Directly (from UI)")
    print("=" * 80)
    try:
        cycle_106_url = f"{base_url.rstrip('/')}/cycle/106"
        print(f"URL: {cycle_106_url}")
        response = requests.get(cycle_106_url, headers=headers, timeout=10)
        response.raise_for_status()
        cycle_106 = response.json()
        print(f"[OK] Cycle 106 exists!")
        print(f"Cycle 106 keys: {list(cycle_106.keys()) if isinstance(cycle_106, dict) else 'N/A'}")
        if isinstance(cycle_106, dict):
            print(f"Cycle 106 sample: {json.dumps(cycle_106, indent=2)[:500]}...")
            cycles_found = True
            cycles = [cycle_106]
    except Exception as e:
        print(f"[ERROR] Failed to fetch cycle 106: {e}")
    
    # Test 2c: Try fetching cycles by tree ID (from UI URL: treeId=309)
    print("\n" + "=" * 80)
    print("TEST 2c: Fetch Cycles by Tree ID 309 (from UI)")
    print("=" * 80)
    try:
        # Try various tree-based cycle endpoints
        tree_309_urls = [
            f"{base_url.rstrip('/')}/cycle?treeId=309",
            f"{base_url.rstrip('/')}/cycle/tree/309",
            f"{base_url.rstrip('/')}/cyclephase/tree/309",
        ]
        for tree_url in tree_309_urls:
            try:
                print(f"  Trying: {tree_url}")
                response = requests.get(tree_url, headers=headers, timeout=10)
                response.raise_for_status()
                tree_cycles = response.json()
                # Handle nested response
                if isinstance(tree_cycles, dict):
                    if "data" in tree_cycles:
                        tree_cycles = tree_cycles["data"]
                    elif "items" in tree_cycles:
                        tree_cycles = tree_cycles["items"]
                    elif "results" in tree_cycles:
                        tree_cycles = tree_cycles["results"]
                if tree_cycles and len(tree_cycles) > 0:
                    print(f"  [OK] Found {len(tree_cycles)} cycles via tree endpoint")
                    print(f"  First cycle keys: {list(tree_cycles[0].keys())}")
                    cycles_found = True
                    cycles = tree_cycles
                    break
            except Exception as e:
                print(f"  [WARN] {tree_url} failed: {e}")
    except Exception as e:
        print(f"[ERROR] Tree-based cycle fetch failed: {e}")
    
    # Test 3: Fetch cycles directly (no release filter)
    print("\n" + "=" * 80)
    print("TEST 3: Fetch Cycles Directly (No Release Filter)")
    print("=" * 80)
    try:
        cycles_direct_url = f"{base_url.rstrip('/')}/cycle?projectId={production_project_id}"
        print(f"URL: {cycles_direct_url}")
        response = requests.get(cycles_direct_url, headers=headers, timeout=10)
        response.raise_for_status()
        cycles_direct = response.json()
        
        # Handle nested response
        if isinstance(cycles_direct, dict):
            print(f"Response is dict with keys: {list(cycles_direct.keys())}")
            if "data" in cycles_direct:
                cycles_direct = cycles_direct["data"]
            elif "items" in cycles_direct:
                cycles_direct = cycles_direct["items"]
            elif "results" in cycles_direct:
                cycles_direct = cycles_direct["results"]
        
        if cycles_direct and len(cycles_direct) > 0:
            print(f"[OK] Found {len(cycles_direct)} cycles via direct endpoint")
            print(f"First cycle keys: {list(cycles_direct[0].keys())}")
        else:
            print("[WARN] No cycles found via direct endpoint")
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        # Not a failure - endpoint might not support this
    
    # Test 4: Fetch testcases (try multiple endpoints)
    print("\n" + "=" * 80)
    print("TEST 4: Fetch Testcases")
    print("=" * 80)
    testcases = None
    
    # Try testcase tree endpoint first (project-based)
    try:
        testcases_tree_url = f"{base_url.rstrip('/')}/testcasetree/projectrepository/{production_project_id}"
        print(f"  Trying testcase tree endpoint: {testcases_tree_url}")
        response = requests.get(testcases_tree_url, headers=headers, timeout=10)
        response.raise_for_status()
        testcases_tree = response.json()
        print(f"  [OK] Testcase tree endpoint works")
        print(f"  Response type: {type(testcases_tree)}")
        if isinstance(testcases_tree, dict):
            print(f"  Keys: {list(testcases_tree.keys())}")
        elif isinstance(testcases_tree, list):
            print(f"  List length: {len(testcases_tree)}")
            if testcases_tree:
                print(f"  First tree node keys: {list(testcases_tree[0].keys())}")
                # Try to extract testcase IDs from tree
                testcase_ids = []
                def extract_ids(node):
                    if isinstance(node, dict):
                        if "id" in node and "type" in node and node.get("type") == "TESTCASE":
                            testcase_ids.append(node["id"])
                        for key, value in node.items():
                            if isinstance(value, (list, dict)):
                                extract_ids(value)
                    elif isinstance(node, list):
                        for item in node:
                            extract_ids(item)
                extract_ids(testcases_tree)
                if testcase_ids:
                    print(f"  Found {len(testcase_ids)} testcase IDs in tree: {testcase_ids[:5]}...")
                    # Try fetching one testcase by ID
                    if testcase_ids:
                        testcase_detail_url = f"{base_url.rstrip('/')}/testcase/detail/{testcase_ids[0]}"
                        print(f"  Fetching testcase detail: {testcase_detail_url}")
                        detail_response = requests.get(testcase_detail_url, headers=headers, timeout=10)
                        detail_response.raise_for_status()
                        testcase_detail = detail_response.json()
                        print(f"  [OK] Testcase detail endpoint works")
                        print(f"  Testcase keys: {list(testcase_detail.keys())}")
                        testcases = [testcase_detail]  # Use this as sample
                else:
                    # Try fetching testcases by tree ID (if tree has treeid)
                    if testcases_tree and isinstance(testcases_tree, list) and len(testcases_tree) > 0:
                        first_tree_node = testcases_tree[0]
                        tree_id = first_tree_node.get("id")
                        if tree_id:
                            print(f"  Trying to fetch testcases by tree ID: {tree_id}")
                            try:
                                testcases_by_tree_url = f"{base_url.rstrip('/')}/testcase/tree/{tree_id}"
                                print(f"  URL: {testcases_by_tree_url}")
                                tree_response = requests.get(testcases_by_tree_url, headers=headers, timeout=10)
                                tree_response.raise_for_status()
                                testcases_by_tree = tree_response.json()
                                # Handle nested response
                                if isinstance(testcases_by_tree, dict):
                                    if "data" in testcases_by_tree:
                                        testcases_by_tree = testcases_by_tree["data"]
                                    elif "items" in testcases_by_tree:
                                        testcases_by_tree = testcases_by_tree["items"]
                                    elif "results" in testcases_by_tree:
                                        testcases_by_tree = testcases_by_tree["results"]
                                if testcases_by_tree and len(testcases_by_tree) > 0:
                                    print(f"  [OK] Found {len(testcases_by_tree)} testcases via tree endpoint")
                                    print(f"  First testcase keys: {list(testcases_by_tree[0].keys())}")
                                    testcases = testcases_by_tree
                            except Exception as e:
                                print(f"  [ERROR] Tree endpoint failed: {e}")
    except Exception as e:
            print(f"  [ERROR] Testcase tree endpoint failed: {e}")
    
    # Try testcase by criteria (needs releaseid)
    if release_id:
        try:
            testcases_url = f"{base_url.rstrip('/')}/testcase?releaseid={release_id}"
            print(f"  Trying testcase by criteria: {testcases_url}")
            response = requests.get(testcases_url, headers=headers, timeout=10)
            response.raise_for_status()
            testcases = response.json()
            
            # Handle nested response
            if isinstance(testcases, dict):
                print(f"    Response is dict with keys: {list(testcases.keys())}")
                if "data" in testcases:
                    testcases = testcases["data"]
                elif "items" in testcases:
                    testcases = testcases["items"]
                elif "results" in testcases:
                    testcases = testcases["results"]
            
            if testcases and len(testcases) > 0:
                print(f"  [OK] Found {len(testcases)} testcases via criteria endpoint")
                print(f"  First testcase keys: {list(testcases[0].keys())}")
                print(f"  First testcase sample: {json.dumps(testcases[0], indent=2)[:500]}...")
            else:
                print("  [WARN] No testcases found via criteria endpoint")
        except Exception as e:
            print(f"  [ERROR] Testcase criteria endpoint failed: {e}")
    
    if not testcases or len(testcases) == 0:
        print("[WARN] No testcases found via any endpoint")
        return False
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"[OK] Releases: {len(releases)} found")
    print(f"{'[OK]' if cycles_found else '[ERROR]'} Cycles: {'Found' if cycles_found else 'Not found'}")
    print(f"{'[OK]' if testcases and len(testcases) > 0 else '[ERROR]'} Testcases: {len(testcases) if testcases else 0} found")
    
    if testcases and len(testcases) > 0:
        print("\n[OK] RECOMMENDATION: Use testcases for schema discovery")
        return True
    elif cycles_found:
        print("\n[OK] RECOMMENDATION: Use cycles for schema discovery")
        return True
    else:
        print("\n[ERROR] RECOMMENDATION: No data available for schema discovery")
        return False

if __name__ == "__main__":
    success = test_zephyr_api()
    sys.exit(0 if success else 1)

