#!/usr/bin/env python3
"""
Check if the source endpoints.json has duplicates that parse to the same path+method.
"""
import json
import re
from pathlib import Path
from collections import defaultdict

repo_root = Path(__file__).parent.parent
endpoints_json = repo_root / "docs" / "endpoints.json"

print("=" * 80)
print("CHECKING SOURCE endpoints.json FOR DUPLICATES")
print("=" * 80)
print()

def extract_path_from_resource(resource: str) -> str:
    """Extract path from resource string like 'Get All Preferences [/admin/preference/admin]'"""
    match = re.search(r'\[([^\]]+)\]', resource)
    if match:
        path = match.group(1)
        # Remove query parameters
        path = path.split('?')[0]
        # Remove path parameters placeholders like {id}
        path = re.sub(r'\{[^}]+\}', '', path)
        return path
    return ""

with open(endpoints_json, "r", encoding="utf-8") as f:
    data = json.load(f)

endpoints = data.get("endpoints", [])
print(f"Source file has {len(endpoints)} endpoints")
print(f"Source file claims count: {data.get('count', 'N/A')}")
print()

# Parse all endpoints and group by path+method
path_method_groups = defaultdict(list)
for i, ep in enumerate(endpoints):
    resource = ep.get("resource", "")
    method = ep.get("method", "").upper()
    path = extract_path_from_resource(resource)
    
    if path and method:
        key = (path, method)
        path_method_groups[key].append((i, ep, resource))

# Find duplicates
duplicates = {k: v for k, v in path_method_groups.items() if len(v) > 1}

if duplicates:
    print(f"🔴 SOURCE FILE HAS {len(duplicates)} DUPLICATE(S) (same parsed path + method):\n")
    
    for (path, method), occurrences in sorted(duplicates.items()):
        print(f"   {method} {path}")
        print(f"   Appears {len(occurrences)} time(s):\n")
        
        for idx, (i, ep, resource) in enumerate(occurrences, 1):
            print(f"      {idx}. Index {i}: '{resource}'")
        
        print()
    
    print("=" * 80)
    print("CONCLUSION:")
    print("   ✅ Duplicates EXIST in source file")
    print("   💡 These parse to the same path+method, causing duplicates in catalog")
    print()
    print("   ROOT CAUSE:")
    print("   - Source endpoints.json has multiple entries that parse to same path+method")
    print("   - parse_endpoints.py doesn't deduplicate during parsing")
    print("   - All duplicates are preserved in embedded catalog")
else:
    print("✅ Source file has NO duplicates (by parsed path+method)")
    print()
    print("   CONCLUSION:")
    print("   - Duplicates introduced during parsing/embedding process")
    print("   - Or source has entries that parse differently but result in same path")

print()
print(f"Total unique path+method combinations: {len(path_method_groups)}")
print(f"Total endpoints in source: {len(endpoints)}")
print(f"Difference: {len(endpoints) - len(path_method_groups)} duplicate(s)")

