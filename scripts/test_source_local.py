#!/usr/bin/env python3
"""
Local test script for Zephyr Source stage.
Tests all endpoints without requiring Fabric pipeline execution.

Usage:
    python scripts/test_source_local.py

Requires:
    - .env file with DXC_ZEPHYR_BASE_URL, DXC_ZEPHYR_BASE_PATH, DXC_ZEPHYR_API_TOKEN
    - Or set environment variables directly
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter, Retry

# Add parent directory to path for imports
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

try:
    from spectra.modules.shared.logging import initialise_logger
except ImportError:
    # Fallback if SDK not installed
    import logging
    def initialise_logger(name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        logger.addHandler(handler)
        return logger

log = initialise_logger("testSourceLocal")

# Active projects from discovery
ACTIVE_PROJECTS = [40, 44]  # Project 40: "Vendor Testing POC", Project 44: "BP2 Test Management"


def create_session(api_token: str) -> requests.Session:
    """Create HTTP session with retry logic."""
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
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
    endpoint: str,
    method: str = "GET",
    params: dict[str, Any] | None = None,
    description: str = ""
) -> tuple[bool, dict[str, Any]]:
    """Test an endpoint and return success status and response data."""
    url = f"{base_url}{endpoint}"
    
    try:
        log.info(f"Testing {endpoint}...")
        start = time.time()
        
        if method == "GET":
            resp = session.get(url, params=params, timeout=30)
        else:
            resp = session.request(method, url, json=params, timeout=30)
        
        duration = time.time() - start
        
        if resp.status_code != 200:
            log.error(f"  ❌ HTTP {resp.status_code}: {resp.text[:200]}")
            return False, {"status_code": resp.status_code, "error": resp.text[:200]}
        
        data = resp.json()
        
        if isinstance(data, list):
            count = len(data)
            log.info(f"  ✅ Success: {count} records in {duration:.2f}s")
            return True, {"count": count, "duration": duration, "sample": data[0] if data else None}
        elif isinstance(data, dict):
            log.info(f"  ✅ Success: Response received in {duration:.2f}s")
            return True, {"data": data, "duration": duration}
        else:
            log.warning(f"  ⚠️  Unexpected response type: {type(data)}")
            return True, {"data": data, "duration": duration}
            
    except Exception as e:
        log.error(f"  ❌ Error: {e}")
        return False, {"error": str(e)}


def test_pagination(
    session: requests.Session,
    base_url: str,
    endpoint: str,
    page_size: int = 100
) -> tuple[bool, dict[str, Any]]:
    """Test pagination with firstresult/maxresults."""
    log.info(f"Testing pagination on {endpoint} with page_size={page_size}...")
    
    # First page
    params = {"firstresult": 0, "maxresults": page_size}
    success, result1 = test_endpoint(session, base_url, endpoint, params=params)
    
    if not success:
        return False, result1
    
    count1 = result1.get("count", 0)
    
    # If we got fewer than page_size, no need to test next page
    if count1 < page_size:
        log.info(f"  ✅ Pagination test: Only {count1} records, single page sufficient")
        return True, {"page1_count": count1, "total_pages": 1}
    
    # Second page
    params = {"firstresult": page_size, "maxresults": page_size}
    success, result2 = test_endpoint(session, base_url, endpoint, params=params)
    
    if not success:
        return False, result2
    
    count2 = result2.get("count", 0)
    log.info(f"  ✅ Pagination test: Page 1={count1}, Page 2={count2}")
    
    return True, {"page1_count": count1, "page2_count": count2, "total_pages": 2}


def main():
    """Run all Source stage health checks."""
    
    # Load environment variables
    base_url = os.environ.get("DXC_ZEPHYR_BASE_URL", "")
    base_path = os.environ.get("DXC_ZEPHYR_BASE_PATH", "")
    api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN", "")
    
    if not base_url or not base_path or not api_token:
        log.error("Missing required environment variables:")
        log.error("  - DXC_ZEPHYR_BASE_URL")
        log.error("  - DXC_ZEPHYR_BASE_PATH")
        log.error("  - DXC_ZEPHYR_API_TOKEN")
        log.error("\nSet these in .env file or environment variables")
        sys.exit(1)
    
    full_base_url = f"{base_url.rstrip('/')}{base_path}"
    session = create_session(api_token)
    
    log.info("=" * 60)
    log.info("Zephyr Source Stage Health Checks")
    log.info("=" * 60)
    log.info(f"Base URL: {full_base_url}")
    log.info(f"Active Projects: {ACTIVE_PROJECTS}")
    log.info("")
    log.info("NOTE: This tests the 4 core endpoints.")
    log.info("      For full endpoint testing, use: python scripts/test_all_endpoints.py")
    log.info("")
    
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base_url": full_base_url,
        "tests": {}
    }
    
    # Test 1: Projects endpoint
    log.info("1. Testing /project endpoint...")
    success, data = test_endpoint(session, full_base_url, "/project")
    results["tests"]["projects"] = {"success": success, "data": data}
    
    if success and "sample" in data:
        log.info(f"   Sample project: {data['sample'].get('name', 'N/A')} (ID: {data['sample'].get('id', 'N/A')})")
    
    log.info("")
    
    # Test 2: Releases endpoint (for each active project)
    log.info("2. Testing /release endpoint...")
    for project_id in ACTIVE_PROJECTS:
        log.info(f"   Project {project_id}:")
        params = {"projectId": project_id}
        success, data = test_endpoint(session, full_base_url, "/release", params=params)
        results["tests"][f"releases_project_{project_id}"] = {"success": success, "data": data}
    log.info("")
    
    # Test 3: Cycles endpoint (for each active project)
    log.info("3. Testing /cycle endpoint...")
    for project_id in ACTIVE_PROJECTS:
        log.info(f"   Project {project_id}:")
        params = {"projectId": project_id}
        success, data = test_endpoint(session, full_base_url, "/cycle", params=params)
        results["tests"][f"cycles_project_{project_id}"] = {"success": success, "data": data}
    log.info("")
    
    # Test 4: Executions endpoint (for each active project)
    log.info("4. Testing /execution endpoint...")
    for project_id in ACTIVE_PROJECTS:
        log.info(f"   Project {project_id}:")
        params = {"projectId": project_id}
        success, data = test_endpoint(session, full_base_url, "/execution", params=params)
        results["tests"][f"executions_project_{project_id}"] = {"success": success, "data": data}
    log.info("")
    
    # Test 5: Pagination (on projects endpoint)
    log.info("5. Testing pagination (firstresult/maxresults)...")
    success, data = test_pagination(session, full_base_url, "/project", page_size=100)
    results["tests"]["pagination"] = {"success": success, "data": data}
    log.info("")
    
    # Summary
    log.info("=" * 60)
    log.info("Summary")
    log.info("=" * 60)
    
    total_tests = len(results["tests"])
    passed_tests = sum(1 for t in results["tests"].values() if t["success"])
    
    log.info(f"Tests run: {total_tests}")
    log.info(f"Passed: {passed_tests}")
    log.info(f"Failed: {total_tests - passed_tests}")
    log.info("")
    log.info("For comprehensive endpoint testing:")
    log.info("  python scripts/test_all_endpoints.py --category all")
    
    if passed_tests == total_tests:
        log.info("✅ All health checks passed!")
        return 0
    else:
        log.error("❌ Some health checks failed - see details above")
        return 1


if __name__ == "__main__":
    sys.exit(main())

