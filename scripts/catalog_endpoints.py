"""
Phase 2: Catalog - Document all Zephyr endpoints

This script transforms docs/endpoints.json into intelligence/endpoints.yaml
with enriched metadata about authentication, methods, and entity relationships.

Output: intelligence/endpoints.yaml
"""

import json
import yaml
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

def load_endpoints_json() -> List[Dict]:
    """Load existing endpoints.json."""
    endpoints_file = Path(__file__).parent.parent / "docs" / "endpoints.json"
    with open(endpoints_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["endpoints"]

def extract_entity_from_path(path: str) -> str:
    """Extract entity name from API path."""
    # Remove leading slash and parameters
    clean_path = path.lstrip("/").split("?")[0].split("{")[0].rstrip("/")
    
    # Get first segment as entity
    entity = clean_path.split("/")[0] if clean_path else "unknown"
    
    return entity

def catalog_endpoints(raw_endpoints: List[Dict]) -> Dict:
    """Catalog and enrich endpoint data."""
    
    # Group by entity
    by_entity = defaultdict(list)
    by_method = defaultdict(int)
    
    for endpoint in raw_endpoints:
        resource = endpoint.get("resource", "")
        method = endpoint.get("method", "GET")
        path = endpoint.get("path", "")
        
        # Extract path from resource if path is empty
        if not path and "[" in resource:
            path = resource.split("[")[1].split("]")[0]
        
        entity = extract_entity_from_path(path)
        
        by_entity[entity].append({
            "resource": resource,
            "method": method,
            "path": path,
            "description": resource.split("[")[0].strip()
        })
        
        by_method[method] += 1
    
    # Build catalog
    catalog = []
    for entity, endpoints in sorted(by_entity.items()):
        methods = defaultdict(list)
        for ep in endpoints:
            methods[ep["method"]].append({
                "path": ep["path"],
                "description": ep["description"]
            })
        
        catalog.append({
            "entity": entity,
            "endpoint_count": len(endpoints),
            "methods": {
                method: paths for method, paths in sorted(methods.items())
            }
        })
    
    return {
        "metadata": {
            "generated_at": "2025-12-09",
            "source": "Phase 2: Catalog",
            "method": "Transformed from docs/endpoints.json",
            "total_endpoints": len(raw_endpoints),
            "unique_entities": len(by_entity),
            "methods_breakdown": dict(by_method)
        },
        "catalog": catalog,
        "authentication": {
            "type": "Bearer Token",
            "header": "Authorization: Bearer {token}",
            "notes": "All endpoints require authentication except public endpoints"
        },
        "pagination": {
            "supported": True,
            "parameters": ["maxresults", "offset", "startindex"],
            "notes": "Most GET endpoints support pagination"
        },
        "rate_limits": {
            "documented": False,
            "observed": None,
            "notes": "No official rate limit documentation found"
        },
        "core_entities": {
            "project": {
                "endpoints": [ep for ep in raw_endpoints if "project" in ep.get("path", "").lower()],
                "primary_path": "/project",
                "notes": "Top-level container"
            },
            "release": {
                "endpoints": [ep for ep in raw_endpoints if "release" in ep.get("path", "").lower() and "externalrelease" not in ep.get("path", "").lower()],
                "primary_path": "/release",
                "notes": "BLOCKER-003: Locks for >60s after creation"
            },
            "cycle": {
                "endpoints": [ep for ep in raw_endpoints if "cycle" in ep.get("path", "").lower()],
                "primary_path": "/cycle",
                "notes": "Requires unlocked release"
            },
            "testcase": {
                "endpoints": [ep for ep in raw_endpoints if "testcase" in ep.get("path", "").lower() and "testcasetree" not in ep.get("path", "").lower()],
                "primary_path": "/testcase",
                "notes": "Requires tcrCatalogTreeId (folder ID)"
            },
            "testcasetree": {
                "endpoints": [ep for ep in raw_endpoints if "testcasetree" in ep.get("path", "").lower()],
                "primary_path": "/testcasetree",
                "notes": "BLOCKER-002: Folder creation broken (HTTP 400)"
            },
            "requirement": {
                "endpoints": [ep for ep in raw_endpoints if "requirement" in ep.get("path", "").lower() and "requirementtree" not in ep.get("path", "").lower() and "externalrequirement" not in ep.get("path", "").lower()],
                "primary_path": "/requirement",
                "notes": "BLOCKER-001: POST /requirement broken (HTTP 500)"
            },
            "requirementtree": {
                "endpoints": [ep for ep in raw_endpoints if "requirementtree" in ep.get("path", "").lower()],
                "primary_path": "/requirementtree/add",
                "notes": "Workaround for requirement creation"
            },
            "execution": {
                "endpoints": [ep for ep in raw_endpoints if "execution" in ep.get("path", "").lower()],
                "primary_path": "/execution",
                "notes": "Links testcase to cycle"
            }
        }
    }

def main():
    """Generate endpoints.yaml from catalog."""
    
    print("📚 Phase 2: Catalog - Documenting all Zephyr endpoints...")
    print()
    
    # Load raw endpoints
    raw_endpoints = load_endpoints_json()
    print(f"📥 Loaded {len(raw_endpoints)} endpoints from docs/endpoints.json")
    print()
    
    # Catalog endpoints
    data = catalog_endpoints(raw_endpoints)
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "intelligence"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write endpoints.yaml
    output_file = output_dir / "endpoints.yaml"
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"✅ Catalog complete!")
    print()
    print(f"📊 Results:")
    print(f"  • Total endpoints: {data['metadata']['total_endpoints']}")
    print(f"  • Unique entities: {data['metadata']['unique_entities']}")
    print()
    print(f"📁 Output: {output_file}")
    print()
    print("🔑 Methods Breakdown:")
    for method, count in data['metadata']['methods_breakdown'].items():
        print(f"  • {method}: {count}")
    print()
    print("🎯 Core Entities Cataloged:")
    for entity, info in data['core_entities'].items():
        endpoint_count = len(info['endpoints'])
        print(f"  • {entity}: {endpoint_count} endpoints - {info['notes']}")
    print()
    print("✅ Phase 2 complete! Ready for Phase 3: Probe")

if __name__ == "__main__":
    main()







