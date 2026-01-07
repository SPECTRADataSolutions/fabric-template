#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local test script for Zephyr data extraction.
Extracts samples from independent endpoints and saves as JSON files (simulating lakehouse writes).

This script tests extraction before committing to Fabric notebook.
"""

import json
import sys
import io
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

try:
    import requests
except ImportError:
    print("[ERROR] Missing dependency: requests")
    print("   Install with: pip install requests")
    sys.exit(1)


# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


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


def extract_projects(full_url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Extract all projects.
    Endpoint: GET /project or /project/details
    """
    print("[*] Extracting projects...")
    
    # Try /project/details first (used in existing scripts)
    try:
        response = requests.get(
            f"{full_url}/project/details",
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        projects = response.json()
        
        print(f"   [OK] Success: {len(projects)} projects retrieved")
        return {
            "status": "success",
            "endpoint": "/project/details",
            "data": projects,
            "count": len(projects) if isinstance(projects, list) else 1
        }
    except requests.exceptions.HTTPError as e:
        print(f"   [ERROR] HTTP Error: {e.response.status_code}")
        # Fallback to /project
        try:
            response = requests.get(
                f"{full_url}/project",
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            projects = response.json()
            print(f"   [OK] Fallback /project succeeded: {len(projects)} projects retrieved")
            return {
                "status": "success",
                "endpoint": "/project",
                "data": projects,
                "count": len(projects) if isinstance(projects, list) else 1
            }
        except Exception as e2:
            print(f"   [ERROR] Fallback also failed: {e2}")
            return {
                "status": "error",
                "error": str(e),
                "fallback_error": str(e2)
            }
    except Exception as e:
        print(f"   [ERROR] Unexpected error: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


def extract_releases(full_url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Extract all releases.
    Endpoint: GET /release
    """
    print("[*] Extracting releases...")
    
    try:
        response = requests.get(
            f"{full_url}/release",
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        releases = response.json()
        
        count = len(releases) if isinstance(releases, list) else 1
        print(f"   [OK] Success: {count} releases retrieved")
        
        return {
            "status": "success",
            "endpoint": "/release",
            "data": releases,
            "count": count
        }
    except requests.exceptions.HTTPError as e:
        print(f"   [ERROR] HTTP Error: {e.response.status_code} - {e}")
        return {
            "status": "error",
            "endpoint": "/release",
            "error": str(e),
            "status_code": e.response.status_code if e.response else None
        }
    except Exception as e:
        print(f"   [ERROR] Unexpected error: {e}")
        return {
            "status": "error",
            "endpoint": "/release",
            "error": str(e)
        }


def extract_requirement_folders(full_url: str, headers: Dict[str, str], project_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Extract requirement folders for a project.
    Endpoint: GET /requirementtree/project/{projectId}
    
    If project_id is None, tries to get TEST_PROJECT_ID from Variable Library or uses a default.
    """
    print("[*] Extracting requirement folders...")
    
    # Get project_id if not provided
    if project_id is None:
        var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
        if var_lib_path.exists():
            with open(var_lib_path, "r") as f:
                var_lib = json.load(f)
                for var in var_lib.get("variables", []):
                    if var.get("name") == "TEST_PROJECT_ID":
                        project_id = int(var.get("value", "45"))
                        break
        
        if project_id is None:
            project_id = 45  # Default fallback
    
    print(f"   [*] Using project_id: {project_id}")
    
    try:
        response = requests.get(
            f"{full_url}/requirementtree/project/{project_id}",
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        folders = response.json()
        
        count = len(folders) if isinstance(folders, list) else 1
        print(f"   [OK] Success: {count} requirement folders retrieved")
        
        return {
            "status": "success",
            "endpoint": f"/requirementtree/project/{project_id}",
            "data": folders,
            "count": count,
            "project_id": project_id
        }
    except requests.exceptions.HTTPError as e:
        print(f"   [ERROR] HTTP Error: {e.response.status_code} - {e}")
        return {
            "status": "error",
            "endpoint": f"/requirementtree/project/{project_id}",
            "error": str(e),
            "status_code": e.response.status_code if e.response else None,
            "project_id": project_id
        }
    except Exception as e:
        print(f"   [ERROR] Unexpected error: {e}")
        return {
            "status": "error",
            "endpoint": f"/requirementtree/project/{project_id}",
            "error": str(e),
            "project_id": project_id
        }


def save_extraction_result(output_dir: Path, entity_name: str, result: Dict[str, Any]):
    """
    Save extraction result to JSON file (simulating lakehouse write).
    
    Creates:
    - {entity_name}_sample.json - Full data
    - {entity_name}_metadata.json - Metadata about the extraction
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().isoformat()
    
    # Save full data
    data_file = output_dir / f"{entity_name}_sample.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(result.get("data", []), f, indent=2, default=str)
    print(f"   [*] Saved data to: {data_file}")
    
    # Save metadata
    metadata = {
        "entity": entity_name,
        "extracted_at": timestamp,
        "status": result.get("status"),
        "endpoint": result.get("endpoint"),
        "count": result.get("count", 0),
        "error": result.get("error")
    }
    
    metadata_file = output_dir / f"{entity_name}_metadata.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"   [*] Saved metadata to: {metadata_file}")


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


def print_summary(results: Dict[str, Dict[str, Any]]):
    """Print extraction summary."""
    print("\n" + "=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    
    for entity, result in results.items():
        status_icon = "[OK]" if result.get("status") == "success" else "[ERROR]"
        print(f"\n{status_icon} {entity.upper()}")
        print(f"   Endpoint: {result.get('endpoint', 'N/A')}")
        print(f"   Status: {result.get('status')}")
        if result.get("count"):
            print(f"   Records: {result.get('count')}")
        if result.get("error"):
            print(f"   Error: {result.get('error')}")
    
    # Show schema for successful extractions
    print("\n" + "=" * 80)
    print("SCHEMA ANALYSIS")
    print("=" * 80)
    
    for entity, result in results.items():
        if result.get("status") == "success" and result.get("data"):
            data = result["data"]
            sample = data[0] if isinstance(data, list) and len(data) > 0 else data
            
            schema = analyze_schema(sample)
            
            print(f"\n[*] {entity.upper()} Schema:")
            print("-" * 80)
            for field_path, field_type in sorted(schema.items())[:20]:  # Show first 20 fields
                print(f"  {field_path}: {field_type}")
            if len(schema) > 20:
                print(f"  ... and {len(schema) - 20} more fields")


def main():
    """Main extraction function."""
    print("=" * 80)
    print("ZEPHYR DATA EXTRACTION - LOCAL TEST")
    print("=" * 80)
    print()
    
    # Load credentials
    try:
        print("[*] Loading credentials...")
        api_token, base_url, base_path = load_credentials()
        full_url = f"{base_url}{base_path}"
        print(f"   [OK] Base URL: {base_url}")
        print(f"   [OK] Base Path: {base_path}")
        print()
    except ValueError as e:
        print(f"[ERROR] {e}")
        return 1
    
    # Build headers
    headers = get_api_headers(api_token)
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "extract_samples"
    print(f"[*] Output directory: {output_dir}")
    print()
    
    # Extract independent endpoints (Level 0)
    print("=" * 80)
    print("EXTRACTING LEVEL 0: INDEPENDENT ENDPOINTS")
    print("=" * 80)
    print()
    
    results = {}
    
    # 1. Projects
    results["projects"] = extract_projects(full_url, headers)
    if results["projects"].get("status") == "success":
        save_extraction_result(output_dir, "projects", results["projects"])
        
        # Get first project ID for requirement folders if needed
        projects_data = results["projects"]["data"]
        if isinstance(projects_data, list) and len(projects_data) > 0:
            first_project_id = projects_data[0].get("id")
            print(f"   [*] First project ID: {first_project_id}")
    print()
    
    # 2. Releases
    results["releases"] = extract_releases(full_url, headers)
    if results["releases"].get("status") == "success":
        save_extraction_result(output_dir, "releases", results["releases"])
    print()
    
    # 3. Requirement Folders (needs project_id, but endpoint is independent)
    # We'll use TEST_PROJECT_ID or first project from results
    project_id = None
    if results["projects"].get("status") == "success":
        projects_data = results["projects"]["data"]
        if isinstance(projects_data, list) and len(projects_data) > 0:
            project_id = projects_data[0].get("id")
    
    results["requirement_folders"] = extract_requirement_folders(full_url, headers, project_id)
    if results["requirement_folders"].get("status") == "success":
        save_extraction_result(output_dir, "requirement_folders", results["requirement_folders"])
    print()
    
    # Print summary
    print_summary(results)
    
    print("\n" + "=" * 80)
    print("[OK] Extraction complete!")
    print("=" * 80)
    print(f"\n[*] Results saved to: {output_dir}")
    print("\n[*] Next steps:")
    print("   1. Review JSON files in extract_samples/")
    print("   2. Check schema analysis above")
    print("   3. Once satisfied, commit to Fabric notebook")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

