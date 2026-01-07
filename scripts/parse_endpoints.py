"""
Parse Zephyr endpoints.json and generate structured endpoint catalog.

Converts the raw API documentation format into SPECTRA-standard endpoint catalog
with proper categorisation and metadata.
"""

import json
import re
from pathlib import Path
from typing import List, Dict


def extract_path_from_resource(resource: str) -> str:
    """Extract API path from resource description.
    
    Example: "Get All Projects [/project/details]" -> "/project/details"
    Returns base path (for matching) - query params and path params stripped.
    """
    match = re.search(r'\[([^\]]+)\]', resource)
    if match:
        path = match.group(1)
        # Remove query parameters for path matching
        return path.split('?')[0].split('{')[0].rstrip('/')
    return ""

def extract_full_path(resource: str) -> str:
    """Extract full path with parameters preserved.
    
    Example: "Get Preference [/admin/preference{?key}]" -> "/admin/preference{?key}"
    Returns full path including query params and path params (for uniqueness).
    """
    match = re.search(r'\[([^\]]+)\]', resource)
    if match:
        return match.group(1)
    return ""

def extract_query_parameters(resource: str) -> list:
    """Extract query parameter names from resource.
    
    Example: "/admin/preference{?key}{?value}" -> ["key", "value"]
    """
    match = re.search(r'\[([^\]]+)\]', resource)
    if not match:
        return []
    
    path = match.group(1)
    # Find all {?param} patterns
    query_params = re.findall(r'\{\?([^}]+)\}', path)
    return query_params

def extract_path_parameters(resource: str) -> list:
    """Extract path parameter names from resource.
    
    Example: "/cycle/{cycleid}/phase/{phaseid}" -> ["cycleid", "phaseid"]
    """
    match = re.search(r'\[([^\]]+)\]', resource)
    if not match:
        return []
    
    path = match.group(1)
    # Find all {param} patterns (not query params)
    path_params = re.findall(r'\{([^?}]+)\}', path)
    return path_params


def categorise_endpoint(path: str, method: str) -> str:
    """Categorise endpoint by path pattern."""
    path_lower = path.lower()
    
    # Primary objects (from contract)
    if path_lower.startswith('/project'):
        return "projects"
    elif path_lower.startswith('/release'):
        return "releases"
    elif path_lower.startswith('/cycle'):
        return "cycles"
    elif path_lower.startswith('/execution'):
        return "executions"
    elif path_lower.startswith('/testcase'):
        return "testcases"
    elif path_lower.startswith('/requirement'):
        return "requirements"
    
    # Administrative
    elif path_lower.startswith('/admin'):
        return "admin"
    elif path_lower.startswith('/user'):
        return "users"
    elif path_lower.startswith('/group'):
        return "groups"
    elif path_lower.startswith('/role'):
        return "roles"
    
    # System
    elif path_lower.startswith('/system'):
        return "system"
    elif path_lower.startswith('/license'):
        return "license"
    elif path_lower.startswith('/info'):
        return "info"
    
    # Automation/Jobs
    elif path_lower.startswith('/automation') or path_lower.startswith('/upload-file'):
        return "automation"
    
    # Other
    elif path_lower.startswith('/attachment'):
        return "attachments"
    elif path_lower.startswith('/defect'):
        return "defects"
    elif path_lower.startswith('/field'):
        return "fields"
    elif path_lower.startswith('/search') or path_lower.startswith('/advancesearch'):
        return "search"
    
    return "other"


def is_hierarchical(path: str) -> bool:
    """Check if endpoint requires parent IDs (hierarchical)."""
    hierarchical_patterns = [
        r'\{project[idId]*\}',
        r'\{release[idId]*\}',
        r'\{cycle[idId]*\}',
        r'\{cyclephase[idId]*\}',
        r'/project/',
        '/release/',
        '/cycle/',
    ]
    
    for pattern in hierarchical_patterns:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False


def parse_endpoints_json(json_path: Path) -> List[Dict]:
    """Parse endpoints.json and return structured endpoint catalog."""
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    endpoints = []
    seen = set()  # Track (full_path, method) for deduplication
    
    for ep in data.get('endpoints', []):
        resource = ep.get('resource', '')
        method = ep.get('method', '').upper()
        
        # Extract paths
        base_path = extract_path_from_resource(resource)  # For matching/categorisation
        full_path = extract_full_path(resource)  # For uniqueness
        
        if not base_path or not full_path:
            continue  # Skip if no path extracted
        
        # Deduplicate by (full_path, method) - this ensures zero duplicates
        uniqueness_key = (full_path, method)
        if uniqueness_key in seen:
            continue  # Skip duplicate
        seen.add(uniqueness_key)
        
        # Extract metadata
        query_params = extract_query_parameters(resource)
        path_params = extract_path_parameters(resource)
        category = categorise_endpoint(base_path, method)
        hierarchical = is_hierarchical(full_path)  # Check full path for hierarchical
        
        endpoint_data = {
            "endpoint_path": base_path,  # Base path for matching
            "full_path": full_path,  # Full path with params for uniqueness
            "http_method": method,
            "category": category,
            "description": resource.split('[')[0].strip() if '[' in resource else resource,
            "requires_auth": True,  # All Zephyr endpoints require auth
            "hierarchical": hierarchical,
            "query_parameters": query_params,  # List of query param names
            "path_parameters": path_params,  # List of path param names
            "resource": resource,  # Full resource string for reference
        }
        
        endpoints.append(endpoint_data)
    
    return endpoints


def main():
    """Generate endpoint catalog."""
    
    # Paths
    repo_root = Path(__file__).parent.parent
    endpoints_json = repo_root / "docs" / "endpoints.json"
    output_py = repo_root / "scripts" / "endpoints_catalog.py"
    
    print(f"📖 Parsing {endpoints_json}...")
    endpoints = parse_endpoints_json(endpoints_json)
    
    print(f"✅ Parsed {len(endpoints)} endpoints")
    
    # Generate Python catalog (use Python syntax, not JSON)
    # Convert JSON booleans to Python booleans
    catalog_json = json.dumps(endpoints, indent=2)
    catalog_json = catalog_json.replace('true', 'True').replace('false', 'False')
    
    catalog_code = f'''"""
Zephyr Endpoint Catalog - Auto-generated from endpoints.json

Total: {len(endpoints)} endpoints
Generated: {__import__('datetime').datetime.utcnow().isoformat()}
"""

ENDPOINTS_CATALOG = {catalog_json}

# Category summary
CATEGORY_COUNTS = {{
    category: len([e for e in ENDPOINTS_CATALOG if e["category"] == category])
    for category in set(e["category"] for e in ENDPOINTS_CATALOG)
}}

# Hierarchical endpoints
HIERARCHICAL_ENDPOINTS = [
    e for e in ENDPOINTS_CATALOG if e["hierarchical"]
]
'''
    
    output_py.write_text(catalog_code)
    print(f"💾 Saved catalog to {output_py}")
    
    # Print summary
    from collections import Counter
    categories = Counter(e["category"] for e in endpoints)
    
    print("\n📊 Category Summary:")
    for category, count in sorted(categories.items()):
        print(f"  {category:20s}: {count:3d} endpoints")
    
    hierarchical_count = sum(1 for e in endpoints if e["hierarchical"])
    print(f"\n🔗 Hierarchical endpoints: {hierarchical_count}/{len(endpoints)}")


if __name__ == "__main__":
    main()

