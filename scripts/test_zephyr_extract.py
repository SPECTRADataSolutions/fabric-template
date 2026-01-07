#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Zephyr API extraction in Cursor.
Extracts data from Zephyr API endpoints to test connectivity and response structure.

This script:
1. Loads credentials from .env or Variable Library
2. Tests the /project endpoint (first in the hierarchy)
3. Displays response structure and sample data
4. Can be extended to test other endpoints
"""

import json
import sys
import io
from pathlib import Path
from typing import Dict, Any, Optional

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import requests
except ImportError:
    print("❌ Missing dependency: requests")
    print("   Install with: pip install requests")
    sys.exit(1)


def load_credentials() -> tuple[str, str, str]:
    """
    Load Zephyr API credentials from .env or Variable Library.
    
    Returns:
        tuple: (api_token, base_url, base_path)
    
    Raises:
        ValueError: If credentials not found
    """
    spectra_root = Path(__file__).parent.parent.parent.parent
    env_file = spectra_root / ".env"
    
    api_token = None
    base_url = "https://velonetic.yourzephyr.com"
    base_path = "/flex/services/rest/latest"
    
    # Try .env first
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("ZEPHYR_API_TOKEN=") or line.startswith("SPECTRA_ZEPHYR_API_TOKEN="):
                    api_token = line.split("=", 1)[1].strip().strip('"').strip("'")
                elif line.startswith("ZEPHYR_BASE_URL="):
                    base_url = line.split("=", 1)[1].strip().strip('"').strip("'")
    
    # Fallback to Variable Library
    if not api_token:
        var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
        if var_lib_path.exists():
            with open(var_lib_path, "r") as f:
                var_lib = json.load(f)
                for var in var_lib.get("variables", []):
                    name = var.get("name", "")
                    value = var.get("value", "")
                    if name == "API_TOKEN":
                        api_token = value
                    elif name == "BASE_URL":
                        base_url = value
                    elif name == "BASE_PATH":
                        base_path = value
    
    if not api_token:
        raise ValueError(
            "API token not found. "
            "Set ZEPHYR_API_TOKEN in .env or API_TOKEN in Variable Library"
        )
    
    return api_token, base_url, base_path


def get_api_headers(api_token: str) -> Dict[str, str]:
    """Build API request headers."""
    return {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def test_project_endpoint(base_url: str, base_path: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Test the /project endpoint (first in extraction hierarchy).
    
    According to source.plan.yaml, the endpoint is /project.
    Some scripts use /project/details for detailed project info.
    We'll try both.
    """
    full_url = f"{base_url}{base_path}"
    results = {}
    
    # Test 1: /project (as per source.plan.yaml)
    print("[*] Testing endpoint: GET /project")
    try:
        response = requests.get(
            f"{full_url}/project",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        results["/project"] = {
            "status": "success",
            "status_code": response.status_code,
            "data_type": type(data).__name__,
            "data_count": len(data) if isinstance(data, list) else 1,
            "sample": data[0] if isinstance(data, list) and len(data) > 0 else data
        }
        print(f"   [OK] Success: {response.status_code}")
        print(f"   [*] Response type: {results['/project']['data_type']}")
        print(f"   [*] Count: {results['/project']['data_count']}")
    except requests.exceptions.HTTPError as e:
        results["/project"] = {
            "status": "error",
            "status_code": e.response.status_code if e.response else None,
            "error": str(e)
        }
        print(f"   [ERROR] Error: {e}")
    except Exception as e:
        results["/project"] = {
            "status": "error",
            "error": str(e)
        }
        print(f"   [ERROR] Unexpected error: {e}")
    
    print()
    
    # Test 2: /project/details (used in existing scripts)
    print("[*] Testing endpoint: GET /project/details")
    try:
        response = requests.get(
            f"{full_url}/project/details",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        results["/project/details"] = {
            "status": "success",
            "status_code": response.status_code,
            "data_type": type(data).__name__,
            "data_count": len(data) if isinstance(data, list) else 1,
            "sample": data[0] if isinstance(data, list) and len(data) > 0 else data
        }
        print(f"   [OK] Success: {response.status_code}")
        print(f"   [*] Response type: {results['/project/details']['data_type']}")
        print(f"   [*] Count: {results['/project/details']['data_count']}")
    except requests.exceptions.HTTPError as e:
        results["/project/details"] = {
            "status": "error",
            "status_code": e.response.status_code if e.response else None,
            "error": str(e)
        }
        print(f"   [ERROR] Error: {e}")
    except Exception as e:
        results["/project/details"] = {
            "status": "error",
            "error": str(e)
        }
        print(f"   [ERROR] Unexpected error: {e}")
    
    return results


def print_sample_data(results: Dict[str, Any], endpoint: str):
    """Print formatted sample data from endpoint response."""
    if endpoint not in results:
        return
    
    result = results[endpoint]
    if result.get("status") != "success":
        return
    
    sample = result.get("sample")
    if not sample:
        return
    
    print(f"\n[*] Sample data from {endpoint}:")
    print("=" * 80)
    print(json.dumps(sample, indent=2, default=str))
    print("=" * 80)


def analyze_schema(data: Any, prefix: str = "") -> Dict[str, str]:
    """
    Analyze the schema/structure of the API response.
    
    Returns:
        Dict mapping field paths to their types
    """
    schema = {}
    
    if isinstance(data, dict):
        for key, value in data.items():
            field_path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                schema[field_path] = "object"
                schema.update(analyze_schema(value, field_path))
            elif isinstance(value, list):
                schema[field_path] = "array"
                if len(value) > 0:
                    schema[field_path] = f"array[{type(value[0]).__name__}]"
                    if isinstance(value[0], dict):
                        schema.update(analyze_schema(value[0], field_path))
            else:
                schema[field_path] = type(value).__name__
    elif isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            schema.update(analyze_schema(data[0], prefix))
    
    return schema


def print_schema(results: Dict[str, Any], endpoint: str):
    """Print schema analysis for endpoint response."""
    if endpoint not in results:
        return
    
    result = results[endpoint]
    if result.get("status") != "success":
        return
    
    sample = result.get("sample")
    if not sample:
        return
    
    schema = analyze_schema(sample)
    
    print(f"\n[*] Schema structure for {endpoint}:")
    print("=" * 80)
    for field_path, field_type in sorted(schema.items()):
        print(f"  {field_path}: {field_type}")
    print("=" * 80)


def main():
    """Main test function."""
    print("Zephyr API Extraction Test")
    print("=" * 80)
    print()
    
    # Load credentials
    try:
        print("[*] Loading credentials...")
        api_token, base_url, base_path = load_credentials()
        print(f"   [OK] Base URL: {base_url}")
        print(f"   [OK] Base Path: {base_path}")
        print(f"   [OK] API Token: {'*' * 20}...{api_token[-4:] if len(api_token) > 4 else '****'}")
        print()
    except ValueError as e:
        print(f"[ERROR] {e}")
        return 1
    
    # Build headers
    headers = get_api_headers(api_token)
    
    # Test project endpoint
    print("[*] Testing Project Endpoint (first in extraction hierarchy)")
    print("-" * 80)
    print()
    
    results = test_project_endpoint(base_url, base_path, headers)
    
    # Display results
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    
    for endpoint, result in results.items():
        status_icon = "[OK]" if result.get("status") == "success" else "[ERROR]"
        print(f"\n{status_icon} {endpoint}")
        print(f"   Status: {result.get('status')}")
        if result.get("status_code"):
            print(f"   HTTP Status: {result.get('status_code')}")
        if result.get("data_count"):
            print(f"   Records: {result.get('data_count')}")
        if result.get("error"):
            print(f"   Error: {result.get('error')}")
    
    # Show sample data and schema for successful endpoints
    print("\n" + "=" * 80)
    print("DETAILED ANALYSIS")
    print("=" * 80)
    
    for endpoint in results.keys():
        if results[endpoint].get("status") == "success":
            print_sample_data(results, endpoint)
            print_schema(results, endpoint)
    
    print("\n" + "=" * 80)
    print("[OK] Test complete!")
    print("=" * 80)
    print("\n[*] Next steps:")
    print("   1. Review the schema structure above")
    print("   2. Use this to build the Prepare stage schema")
    print("   3. Test additional endpoints (releases, cycles, executions)")
    print("   4. Extend this script to extract full datasets")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

