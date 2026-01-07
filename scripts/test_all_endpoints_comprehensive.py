#!/usr/bin/env python3
"""
Comprehensive endpoint testing with proper parameters and diagnostics.
Goal: Get ALL endpoints green by using actual IDs and fixing issues.
"""

import os
import json
import time
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter, Retry

# Configuration
base_url = os.environ.get("DXC_ZEPHYR_BASE_URL", "https://velonetic.yourzephyr.com")
base_path = os.environ.get("DXC_ZEPHYR_BASE_PATH", "/flex/services/rest/latest")
api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN")

if not all([base_url, base_path, api_token]):
    print("ERROR: Missing required environment variables")
    print("  DXC_ZEPHYR_BASE_URL")
    print("  DXC_ZEPHYR_BASE_PATH")
    print("  DXC_ZEPHYR_API_TOKEN")
    exit(1)

full_base = f"{base_url}{base_path}"
repo_root = Path(__file__).parent.parent

# Load sample data for actual IDs
sample_data_dir = repo_root / "docs" / "api-discovery" / "sample-100-extraction"
actual_ids = {
    'project': [],
    'release': [],
    'cycle': [],
    'execution': [],
    'testcase': []
}

# Load ALL IDs from comprehensive extraction
try:
    all_ids_file = repo_root / "docs" / "api-discovery" / "all_identifiers.json"
    
    if all_ids_file.exists():
        with open(all_ids_file, 'r') as f:
            all_extracted_ids = json.load(f)
        
        print(f"Loaded {len(all_extracted_ids)} ID types from all_identifiers.json:")
        
        # Map extracted IDs to actual_ids dictionary
        actual_ids = {
            'project': all_extracted_ids.get('projectId', [])[:5],
            'release': all_extracted_ids.get('releaseId', [])[:5],
            'cycle': all_extracted_ids.get('cycleId', [])[:5],
            'execution': all_extracted_ids.get('executionId', [])[:5],
            'testcase': all_extracted_ids.get('testCaseId', all_extracted_ids.get('testcaseId', []))[:5],
            'testcaseversion': all_extracted_ids.get('testcaseVersionId', [])[:5],
            'tester': all_extracted_ids.get('testerId', [])[:5],
            'user': all_extracted_ids.get('createdById', [])[:5],
            'tree': all_extracted_ids.get('tcrCatalogTreeId', all_extracted_ids.get('testCaseTreeId', []))[:5],
            'field': all_extracted_ids.get('fieldId', [])[:5],
            'requirement': all_extracted_ids.get('requirementId', [])[:5],
            'defect': all_extracted_ids.get('bugId', [])[:5],  # bugId is defectId!
            'cyclephase': all_extracted_ids.get('cyclePhaseId', [])[:5],
            'entity': all_extracted_ids.get('entityId', [])[:5],
            'external': all_extracted_ids.get('externalId', [])[:5]
        }
        
        print(f"  Projects: {actual_ids['project']}")
        print(f"  Releases: {actual_ids['release']}")
        print(f"  Cycles: {actual_ids['cycle']}")
        print(f"  Defects (bugId): {actual_ids['defect']}")
        print(f"  Requirements: {actual_ids['requirement']}")
        print(f"  Trees: {actual_ids['tree']}")
        print(f"  Fields: {actual_ids['field']}")
        print()
    else:
        raise FileNotFoundError("all_identifiers.json not found - run extract_all_identifiers.py first")
        
except Exception as e:
    print(f"⚠️ Could not load all identifiers: {e}")
    print("Using fallback IDs...")
    actual_ids = {
        'project': [40, 44],
        'release': [90, 106],
        'cycle': [133, 164],
        'execution': [33023],
        'testcase': [80360]
    }

def create_session(api_token: str, timeout: int = 30) -> requests.Session:
    """Create HTTP session with retry logic and longer timeout."""
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.headers.update({
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    })
    return session

def fix_path(path: str) -> str:
    """Fix malformed paths (remove trailing {)."""
    if path.endswith('{'):
        path = path[:-1]
    return path

def substitute_path_params(path: str, ids: dict) -> tuple[str, bool]:
    """Substitute path parameters with actual IDs."""
    original = path
    substituted = False
    
    # Common substitutions using ALL extracted IDs
    replacements = {
        '{projectid}': ids.get('project', [None])[0],
        '{projectId}': ids.get('project', [None])[0],
        '{releaseid}': ids.get('release', [None])[0],
        '{releaseId}': ids.get('release', [None])[0],
        '{cycleid}': ids.get('cycle', [None])[0],
        '{cycleId}': ids.get('cycle', [None])[0],
        '{id}': ids.get('execution', [None])[0],  # Generic ID - try execution first
        '{testcaseId}': ids.get('testcase', [None])[0],
        '{testcaseid}': ids.get('testcase', [None])[0],
        '{testcaseVersionId}': ids.get('testcaseversion', [None])[0],
        '{treeId}': ids.get('tree', [None])[0],
        '{treeid}': ids.get('tree', [None])[0],
        '{tctId}': ids.get('tree', [None])[0],  # Test case catalog tree ID
        '{UserID}': ids.get('user', ids.get('tester', [None]))[0],
        '{userid}': ids.get('user', ids.get('tester', [None]))[0],
        '{pid}': ids.get('project', [None])[0],
        '{TemplateId}': 1,  # Parser template - need to find
        '{defectId}': ids.get('defect', [None])[0],  # Now we have actual bugId!
        '{dashboardId}': 1,  # Dashboard - need to find
        '{entityName}': 'testcase',  # Common entity
        '{entityname}': 'testcase',
        '{requirementid}': ids.get('requirement', [None])[0],
        '{altid}': ids.get('external', [None])[0],  # Alternative ID
        '{fieldId}': ids.get('field', [None])[0]
    }
    
    for placeholder, value in replacements.items():
        if placeholder in path and value is not None:
            path = path.replace(placeholder, str(value))
            substituted = True
    
    # If still has placeholders, we couldn't substitute
    if '{' in path and '}' in path:
        return original, False
    
    return path, substituted

def extract_query_params(resource: str, ids: dict) -> dict:
    """Extract query parameters from resource description."""
    params = {}
    
    # Common query patterns from resource description
    if '{?cycleid}' in resource.lower():
        params['cycleid'] = ids.get('cycle', [None])[0]
    if '{?releaseid}' in resource.lower():
        params['releaseid'] = ids.get('release', [None])[0]
    if '{?projectid}' in resource.lower():
        params['projectid'] = ids.get('project', [None])[0]
    if '{?testcaseid}' in resource.lower():
        params['testcaseid'] = ids.get('testcase', [None])[0]
    if '{?tcid}' in resource.lower():
        params['tcid'] = ids.get('testcase', [None])[0]
    if '{?requirementid}' in resource.lower():
        params['requirementid'] = ids.get('requirement', [None])[0]
    if '{?treeids}' in resource.lower():
        # Send as comma-separated
        tree_ids = ids.get('tree', [])[:3]
        if tree_ids:
            params['treeids'] = ','.join(map(str, tree_ids))
    if '{?ids}' in resource.lower():
        # Generic IDs - try execution IDs
        exec_ids = ids.get('execution', [])[:3]
        if exec_ids:
            params['ids'] = ','.join(map(str, exec_ids))
    if '{?altids}' in resource.lower():
        params['altids'] = ids.get('external', [None])[0]
    if '{?tctid}' in resource.lower():
        params['tctid'] = ids.get('tree', [None])[0]
    if '{?tctids}' in resource.lower():
        tree_ids = ids.get('tree', [])[:3]
        if tree_ids:
            params['tctids'] = ','.join(map(str, tree_ids))
    
    return params

def test_endpoint(
    session: requests.Session,
    base_url: str,
    endpoint: dict[str, Any],
    ids: dict
) -> tuple[bool, dict[str, Any]]:
    """Test a single endpoint with proper parameters."""
    resource = endpoint.get("resource", "")
    method = endpoint.get("method", "GET").upper()
    
    # Extract and fix path
    path = ""
    if "[" in resource and "]" in resource:
        start = resource.find("[")
        end = resource.find("]")
        if start != -1 and end != -1:
            path = resource[start + 1:end]
            # Remove query param indicators from path
            if "?" in path:
                path = path.split("?")[0]
    
    if not path:
        return False, {"error": "Could not extract path", "reason": "Path parsing failed"}
    
    # Fix malformed path
    path = fix_path(path)
    
    # Substitute path parameters
    path, substituted = substitute_path_params(path, ids)
    
    # If still has unresolved placeholders, skip
    if '{' in path:
        return False, {
            "skipped": True,
            "reason": f"Unresolved path parameter in {path}",
            "diagnosis": "Need additional ID types"
        }
    
    # Build URL
    url = f"{base_url}{path}"
    
    # Extract query parameters
    query_params = extract_query_params(resource, ids)
    
    # Test the endpoint
    try:
        start_time = time.time()
        response = session.get(url, params=query_params, timeout=10)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            try:
                data = response.json()
                count = len(data) if isinstance(data, list) else len(data.get('results', data.get('data', [])))
                return True, {
                    "status_code": 200,
                    "count": count,
                    "duration": duration,
                    "path": path,
                    "substituted": substituted,
                    "query_params": query_params
                }
            except:
                return True, {
                    "status_code": 200,
                    "count": "non-json",
                    "duration": duration,
                    "path": path
                }
        else:
            return False, {
                "status_code": response.status_code,
                "error": response.text[:200] if response.text else response.reason,
                "path": path,
                "substituted": substituted,
                "query_params": query_params,
                "diagnosis": diagnose_failure(response.status_code, response.text)
            }
    
    except requests.Timeout:
        return False, {
            "error": "Request timeout (>10s)",
            "path": path,
            "diagnosis": "Endpoint too slow or service issue"
        }
    except Exception as e:
        return False, {
            "error": str(e)[:200],
            "path": path,
            "diagnosis": f"Exception: {type(e).__name__}"
        }

def diagnose_failure(status_code: int, response_text: str) -> str:
    """Provide diagnosis for failure."""
    if status_code == 404:
        return "Endpoint not found - may require specific parameters or deprecated"
    elif status_code == 403:
        return "Access denied - insufficient permissions for this endpoint"
    elif status_code == 400:
        return "Bad request - missing required parameters or invalid format"
    elif status_code == 401:
        return "Authentication failed - token invalid or expired"
    elif status_code == 429:
        return "Rate limited - too many requests"
    elif status_code >= 500:
        return "Server error - API service issue"
    else:
        return f"HTTP {status_code} - Unknown issue"

def main():
    # Load endpoints
    endpoints_file = repo_root / "docs" / "endpoints.json"
    with open(endpoints_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    endpoints = data.get("endpoints", [])
    
    # Filter to GET endpoints only
    get_endpoints = [ep for ep in endpoints if ep.get("method", "").upper() == "GET"]
    
    print("="*80)
    print("COMPREHENSIVE ENDPOINT DIAGNOSTIC TEST")
    print("="*80)
    print(f"Total GET endpoints to test: {len(get_endpoints)}")
    print(f"Base URL: {full_base}")
    print("="*80)
    print()
    
    # Create session
    session = create_session(api_token, timeout=10)
    
    # Results
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base_url": full_base,
        "total_tested": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "results": []
    }
    
    # Test each endpoint
    for i, endpoint in enumerate(get_endpoints, 1):
        resource = endpoint.get("resource", "")
        print(f"[{i}/{len(get_endpoints)}] Testing: {resource[:70]}...")
        
        success, data = test_endpoint(session, full_base, endpoint, actual_ids)
        
        results["total_tested"] += 1
        
        if data.get("skipped"):
            results["skipped"] += 1
            reason = data.get("reason", "Unknown")
            print(f"  [SKIP] {reason}")
        elif success:
            results["passed"] += 1
            count = data.get("count", 0)
            duration = data.get("duration", 0)
            was_substituted = data.get("substituted", False)
            sub_marker = " [SUBSTITUTED]" if was_substituted else ""
            print(f"  [PASS] {count} records in {duration:.2f}s{sub_marker}")
        else:
            results["failed"] += 1
            error = data.get("error", "Unknown")
            status = data.get("status_code", "?")
            diagnosis = data.get("diagnosis", "")
            print(f"  [FAIL] HTTP {status} - {diagnosis}")
            print(f"         {error[:100]}")
        
        results["results"].append({
            "resource": resource,
            "success": success,
            "data": data
        })
        
        # Small delay to avoid rate limiting
        time.sleep(0.1)
    
    # Summary
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total tested: {results['total_tested']}")
    print(f"[PASS] Passed:    {results['passed']} ({results['passed']/results['total_tested']*100:.1f}%)")
    print(f"[FAIL] Failed:    {results['failed']} ({results['failed']/results['total_tested']*100:.1f}%)")
    print(f"[SKIP] Skipped:   {results['skipped']} ({results['skipped']/results['total_tested']*100:.1f}%)")
    print()
    
    # Failure analysis
    failure_reasons = {}
    for result in results["results"]:
        if not result["success"] and not result["data"].get("skipped"):
            diagnosis = result["data"].get("diagnosis", "Unknown")
            failure_reasons[diagnosis] = failure_reasons.get(diagnosis, 0) + 1
    
    if failure_reasons:
        print("Failure Breakdown:")
        for reason, count in sorted(failure_reasons.items(), key=lambda x: -x[1]):
            print(f"  - {reason}: {count}")
    
    # Save results
    results_file = repo_root / "docs" / "api-discovery" / f"comprehensive-test-{int(time.time())}.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print(f"Results saved to: {results_file}")
    
    # Exit code
    if results["failed"] == 0 and results["skipped"] == 0:
        print()
        print("[SUCCESS] ALL ENDPOINTS GREEN!")
        return 0
    elif results["failed"] == 0:
        print()
        print(f"[SUCCESS] All testable endpoints passed ({results['skipped']} skipped due to missing params)")
        return 0
    else:
        print()
        print(f"[WARNING] {results['failed']} endpoints still failing - see diagnostics above")
        return 1

if __name__ == "__main__":
    exit(main())

