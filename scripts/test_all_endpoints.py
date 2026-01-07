#!/usr/bin/env python3
"""
Test all relevant Zephyr API endpoints for Source stage health checks.
Tests GET endpoints that are used for data extraction.

Usage:
    python scripts/test_all_endpoints.py [--category <category>] [--endpoint <path>]

Categories:
    - core: Core 4 endpoints (projects, releases, cycles, executions)
    - testcase: Test case related endpoints
    - requirement: Requirement related endpoints
    - execution: Execution/test step related endpoints
    - user: User/team related endpoints
    - all: All GET endpoints (default)
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter, Retry

# Add parent directory to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

try:
    from spectra.modules.shared.logging import initialise_logger
except ImportError:
    import logging
    def initialise_logger(name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        logger.addHandler(handler)
        return logger

log = initialise_logger("testAllEndpoints")

# Active projects from discovery
ACTIVE_PROJECTS = [40, 44]


def load_endpoints() -> list[dict[str, Any]]:
    """Load endpoints from endpoints.json."""
    endpoints_file = repo_root / "docs" / "endpoints.json"
    with open(endpoints_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("endpoints", [])


def extract_path(resource: str) -> str:
    """Extract path from resource description."""
    if "[" in resource and "]" in resource:
        path_start = resource.find("[")
        path_end = resource.find("]")
        if path_start != -1 and path_end != -1:
            path = resource[path_start + 1:path_end]
            # Remove query parameters for now
            if "?" in path:
                path = path.split("?")[0]
            return path
    return ""


def categorize_endpoints(endpoints: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Categorize endpoints for testing."""
    categories = {
        "core": [],
        "testcase": [],
        "requirement": [],
        "execution": [],
        "user": [],
        "attachment": [],
        "other": []
    }
    
    for ep in endpoints:
        method = ep.get("method", "").upper()
        if method != "GET":
            continue  # Only test GET endpoints for Source stage
        
        resource = ep.get("resource", "").lower()
        path = extract_path(ep.get("resource", ""))
        
        if not path:
            continue
        
        # Categorize
        if path in ["/project", "/release", "/cycle", "/execution"]:
            categories["core"].append({**ep, "path": path})
        elif "/testcase" in path:
            categories["testcase"].append({**ep, "path": path})
        elif "/requirement" in path:
            categories["requirement"].append({**ep, "path": path})
        elif "/execution" in path or "/teststep" in path:
            categories["execution"].append({**ep, "path": path})
        elif "/user" in path or "/group" in path or "/team" in path:
            categories["user"].append({**ep, "path": path})
        elif "/attachment" in path:
            categories["attachment"].append({**ep, "path": path})
        else:
            categories["other"].append({**ep, "path": path})
    
    return categories


def create_session(api_token: str) -> requests.Session:
    """Create HTTP session with retry logic."""
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.headers.update({
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    })
    return session


def test_endpoint(
    session: requests.Session,
    base_url: str,
    endpoint: dict[str, Any],
    project_id: int | None = None
) -> tuple[bool, dict[str, Any]]:
    """Test a single endpoint."""
    path = endpoint.get("path", "")
    method = endpoint.get("method", "GET").upper()
    resource = endpoint.get("resource", "")
    
    # Build URL
    url = f"{base_url}{path}"
    
    # Handle path parameters (basic substitution)
    if "{id}" in path or "{projectid}" in path or "{releaseid}" in path:
        # Skip endpoints that require specific IDs for now
        # We'll test these with actual IDs later
        if project_id:
            url = url.replace("{projectid}", str(project_id))
            url = url.replace("{projectId}", str(project_id))
        else:
            return False, {"skipped": True, "reason": "Requires ID parameter"}
    
    # Build params
    params = {}
    if project_id and "projectid" in path.lower():
        params["projectId"] = project_id
    
    try:
        start = time.time()
        resp = session.get(url, params=params, timeout=10)
        duration = time.time() - start
        
        if resp.status_code == 200:
            data = resp.json()
            count = len(data) if isinstance(data, list) else 1
            return True, {
                "status_code": 200,
                "count": count,
                "duration": duration,
                "path": path
            }
        elif resp.status_code == 401:
            return False, {"status_code": 401, "error": "Unauthorized", "path": path}
        elif resp.status_code == 404:
            return False, {"status_code": 404, "error": "Not found", "path": path}
        else:
            return False, {
                "status_code": resp.status_code,
                "error": resp.text[:200],
                "path": path
            }
    except Exception as e:
        return False, {"error": str(e), "path": path}


def main():
    """Run endpoint health checks."""
    parser = argparse.ArgumentParser(description="Test Zephyr API endpoints")
    parser.add_argument("--category", choices=["core", "testcase", "requirement", "execution", "user", "attachment", "all"], 
                       default="all", help="Category of endpoints to test")
    parser.add_argument("--endpoint", help="Test specific endpoint path")
    parser.add_argument("--project", type=int, help="Project ID to use for testing")
    args = parser.parse_args()
    
    # Load environment variables
    base_url = os.environ.get("DXC_ZEPHYR_BASE_URL", "")
    base_path = os.environ.get("DXC_ZEPHYR_BASE_PATH", "")
    api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN", "")
    
    if not base_url or not base_path or not api_token:
        log.error("Missing required environment variables")
        sys.exit(1)
    
    full_base_url = f"{base_url.rstrip('/')}{base_path}"
    session = create_session(api_token)
    
    # Load and categorize endpoints
    log.info("Loading endpoints from endpoints.json...")
    all_endpoints = load_endpoints()
    categories = categorize_endpoints(all_endpoints)
    
    # Select endpoints to test
    if args.endpoint:
        # Test specific endpoint
        endpoints_to_test = [ep for ep in all_endpoints if args.endpoint in extract_path(ep.get("resource", ""))]
        if not endpoints_to_test:
            log.error(f"Endpoint '{args.endpoint}' not found")
            sys.exit(1)
    elif args.category == "all":
        # Test all GET endpoints
        endpoints_to_test = [ep for cat in categories.values() for ep in cat]
    else:
        endpoints_to_test = categories.get(args.category, [])
    
    # Filter to GET only
    endpoints_to_test = [ep for ep in endpoints_to_test if ep.get("method", "").upper() == "GET"]
    
    log.info("=" * 60)
    log.info(f"Testing {len(endpoints_to_test)} endpoints")
    log.info(f"Category: {args.category}")
    log.info(f"Base URL: {full_base_url}")
    log.info("=" * 60)
    log.info("")
    
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base_url": full_base_url,
        "category": args.category,
        "total_tested": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "results": []
    }
    
    # Test each endpoint
    for i, endpoint in enumerate(endpoints_to_test, 1):
        path = endpoint.get("path", extract_path(endpoint.get("resource", "")))
        resource = endpoint.get("resource", "")
        
        log.info(f"[{i}/{len(endpoints_to_test)}] {path}")
        
        # Test with project ID if provided
        project_id = args.project or (ACTIVE_PROJECTS[0] if ACTIVE_PROJECTS else None)
        success, data = test_endpoint(session, full_base_url, endpoint, project_id)
        
        results["total_tested"] += 1
        
        if data.get("skipped"):
            results["skipped"] += 1
            log.info(f"  ⏭️  Skipped: {data.get('reason', 'Unknown')}")
        elif success:
            results["passed"] += 1
            count = data.get("count", 0)
            duration = data.get("duration", 0)
            log.info(f"  ✅ Success: {count} records in {duration:.2f}s")
        else:
            results["failed"] += 1
            error = data.get("error", "Unknown error")
            status = data.get("status_code", "?")
            log.info(f"  ❌ Failed: HTTP {status} - {error[:100]}")
        
        results["results"].append({
            "path": path,
            "resource": resource,
            "success": success,
            "data": data
        })
        
        # Small delay to avoid rate limiting
        time.sleep(0.1)
    
    # Summary
    log.info("")
    log.info("=" * 60)
    log.info("Summary")
    log.info("=" * 60)
    log.info(f"Total tested: {results['total_tested']}")
    log.info(f"Passed: {results['passed']}")
    log.info(f"Failed: {results['failed']}")
    log.info(f"Skipped: {results['skipped']}")
    
    # Save results
    results_file = repo_root / "docs" / "api-discovery" / f"endpoint-test-results-{int(time.time())}.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    log.info(f"\nResults saved to: {results_file}")
    
    if results["failed"] == 0:
        log.info("✅ All tests passed!")
        return 0
    else:
        log.error("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())





