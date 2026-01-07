"""
Helper to load ZEPHYR_ENDPOINTS_CATALOG from SDK.
"""
import sys
from pathlib import Path

def load_catalog():
    """Load Zephyr endpoints catalog from SDK."""
    sdk_path = Path(__file__).parent.parent / "spectraSDK.Notebook" / "notebook_content.py"
    
    if not sdk_path.exists():
        raise FileNotFoundError(f"SDK not found: {sdk_path}")
    
    # Read SDK file and extract catalog
    sdk_content = sdk_path.read_text(encoding="utf-8")
    
    # Find the catalog definition
    catalog_start = sdk_content.find("ZEPHYR_ENDPOINTS_CATALOG = [")
    if catalog_start == -1:
        raise ValueError("ZEPHYR_ENDPOINTS_CATALOG not found in SDK")
    
    # Find the end of the catalog (next top-level assignment or cell marker)
    catalog_end = sdk_content.find("\n\n# ", catalog_start)
    if catalog_end == -1:
        catalog_end = sdk_content.find("\n# CELL", catalog_start)
    
    catalog_code = sdk_content[catalog_start:catalog_end]
    
    # Execute to get the catalog
    local_vars = {}
    exec(catalog_code, {}, local_vars)
    
    return local_vars["ZEPHYR_ENDPOINTS_CATALOG"]


def find_endpoints_by_category(catalog, category):
    """Find all endpoints for a category."""
    return [ep for ep in catalog if ep.get("category") == category]


def find_endpoint_by_method(endpoints, method):
    """Find endpoint with specific HTTP method."""
    for ep in endpoints:
        if ep.get("http_method") == method:
            return ep
    return None


def group_endpoints_by_entity(catalog):
    """
    Group endpoints by entity type for testing.
    
    Returns dict:
    {
        "releases": {
            "GET_list": endpoint,
            "GET_by_id": endpoint,
            "POST": endpoint,
            "PUT": endpoint,
            "DELETE": endpoint
        }
    }
    """
    entities = {}
    
    # Key entity categories to test
    categories = ["releases", "cycles", "requirements", "testcases", "executions"]
    
    for category in categories:
        endpoints = find_endpoints_by_category(catalog, category)
        
        entity_endpoints = {
            "GET_list": None,
            "GET_by_id": None,
            "POST": None,
            "PUT": None,
            "DELETE": None
        }
        
        for ep in endpoints:
            method = ep.get("http_method")
            path = ep.get("endpoint_path", "")
            full_path = ep.get("full_path", "")
            
            # Identify endpoint type
            if method == "GET":
                # GET by ID has path parameters
                if ep.get("path_parameters") and category.rstrip("s") + "id" in str(ep.get("path_parameters")).lower():
                    entity_endpoints["GET_by_id"] = ep
                # GET list typically has projectid parameter
                elif "project" in path.lower() or "projectid" in str(ep.get("path_parameters")).lower():
                    entity_endpoints["GET_list"] = ep
            elif method == "POST":
                # Special handling for testcases - must be /testcase with NO path params
                if category == "testcases":
                    if (path == "/testcase" or path == "/testcase/") and (not ep.get("path_parameters") or ep.get("path_parameters") == []):
                        entity_endpoints["POST"] = ep
                else:
                    # POST to create (usually has no path params or just project)
                    if not ep.get("path_parameters") or ep.get("path_parameters") == []:
                        entity_endpoints["POST"] = ep
            elif method == "PUT":
                # PUT to update (has ID in path)
                if ep.get("path_parameters"):
                    entity_endpoints["PUT"] = ep
            elif method == "DELETE":
                # DELETE (has ID in path)
                if ep.get("path_parameters"):
                    entity_endpoints["DELETE"] = ep
        
        entities[category] = entity_endpoints
    
    return entities


if __name__ == "__main__":
    # Test
    catalog = load_catalog()
    print(f"Loaded {len(catalog)} endpoints")
    
    entities = group_endpoints_by_entity(catalog)
    for entity, eps in entities.items():
        print(f"\n{entity.upper()}:")
        for op, ep in eps.items():
            if ep:
                print(f"  {op}: {ep.get('full_path')}")
            else:
                print(f"  {op}: NOT FOUND")

