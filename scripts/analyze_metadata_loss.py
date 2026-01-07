#!/usr/bin/env python3
"""
Analyze what metadata we're losing during parsing that could differentiate endpoints.

The issue: We're stripping query parameters and path parameters, which may cause
different endpoints to appear as duplicates.
"""
import json
import re
from pathlib import Path
from collections import defaultdict

repo_root = Path(__file__).parent.parent
endpoints_json = repo_root / "docs" / "endpoints.json"

print("=" * 80)
print("ANALYZING METADATA LOSS DURING PARSING")
print("=" * 80)
print()

def extract_path_from_resource(resource: str) -> str:
    """Current parsing logic - strips query params and path params."""
    match = re.search(r'\[([^\]]+)\]', resource)
    if match:
        path = match.group(1)
        # Remove query parameters for path matching
        return path.split('?')[0].split('{')[0].rstrip('/')
    return ""

def extract_full_path(resource: str) -> str:
    """Extract full path with parameters preserved."""
    match = re.search(r'\[([^\]]+)\]', resource)
    if match:
        return match.group(1)
    return ""

with open(endpoints_json, "r", encoding="utf-8") as f:
    data = json.load(f)

endpoints = data.get("endpoints", [])

print(f"Source file has {len(endpoints)} endpoints\n")
print("=" * 80)
print("1. CHECKING WHAT METADATA EXISTS IN SOURCE")
print("=" * 80)

# Sample a few endpoints to see structure
print("\nSample endpoints from source:")
for i, ep in enumerate(endpoints[:5], 1):
    print(f"\n{i}. Resource: {ep.get('resource', '')}")
    print(f"   Method: {ep.get('method', '')}")
    print(f"   Path field: {ep.get('path', '')}")
    print(f"   Full path (from resource): {extract_full_path(ep.get('resource', ''))}")
    print(f"   Parsed path (current): {extract_path_from_resource(ep.get('resource', ''))}")

print("\n" + "=" * 80)
print("2. CHECKING FOR ENDPOINTS THAT BECOME DUPLICATES AFTER PARSING")
print("=" * 80)

# Group by parsed path+method
parsed_groups = defaultdict(list)
full_path_groups = defaultdict(list)

for i, ep in enumerate(endpoints):
    resource = ep.get("resource", "")
    method = ep.get("method", "").upper()
    
    parsed_path = extract_path_from_resource(resource)
    full_path = extract_full_path(resource)
    
    if parsed_path and method:
        parsed_groups[(parsed_path, method)].append((i, ep, full_path))
    
    if full_path and method:
        full_path_groups[(full_path, method)].append((i, ep))

# Find where parsing creates duplicates
parsed_duplicates = {k: v for k, v in parsed_groups.items() if len(v) > 1}
full_path_duplicates = {k: v for k, v in full_path_groups.items() if len(v) > 1}

print(f"\nAfter parsing (stripping params): {len(parsed_duplicates)} duplicate groups")
print(f"With full paths preserved: {len(full_path_duplicates)} duplicate groups")
print()

if parsed_duplicates:
    print("🔴 Examples where parsing creates duplicates:\n")
    
    for (parsed_path, method), occurrences in list(parsed_duplicates.items())[:10]:
        print(f"   {method} {parsed_path}")
        print(f"   Appears {len(occurrences)} time(s) after parsing:\n")
        
        # Check if full paths are different
        full_paths = [full for _, _, full in occurrences]
        unique_full_paths = set(full_paths)
        
        if len(unique_full_paths) > 1:
            print(f"   ⚠️ DIFFERENT FULL PATHS (metadata lost!):")
            for idx, (i, ep, full_path) in enumerate(occurrences, 1):
                resource = ep.get("resource", "")
                print(f"      {idx}. Index {i}: {full_path}")
                print(f"         Resource: {resource[:80]}")
        else:
            print(f"   ✅ Same full path (true duplicate in source)")
        
        print()

print("=" * 80)
print("3. METADATA WE'RE CURRENTLY CAPTURING")
print("=" * 80)

print("\nCurrent fields in embedded catalog:")
print("  - endpoint_path: Base path (query params & path params stripped)")
print("  - http_method: HTTP method")
print("  - category: Derived from path")
print("  - description: Text before '['")
print("  - requires_auth: Hardcoded True")
print("  - hierarchical: Derived from path patterns")

print("\n" + "=" * 80)
print("4. METADATA WE'RE LOSING")
print("=" * 80)

print("\n❌ Lost during parsing:")
print("  - Query parameters: {?key}, {?scheduleId}, etc.")
print("  - Path parameters: {id}, {cycleid}, {testcaseVersionId}, etc.")
print("  - Full resource string: Original description with full path")
print("  - Path parameter names: Could differentiate endpoints")

print("\n💡 Example of information loss:")
example = "Get Preference by key [/admin/preference{?key}]"
print(f"  Source: {example}")
print(f"  Full path: {extract_full_path(example)}")
print(f"  Parsed path: {extract_path_from_resource(example)}")
print(f"  Lost: Query parameter '?key'")

example2 = "Get Preference Item Usage [/admin/preference/item/usage{?preferencename}{?value}{?id}]"
print(f"\n  Source: {example2}")
print(f"  Full path: {extract_full_path(example2)}")
print(f"  Parsed path: {extract_path_from_resource(example2)}")
print(f"  Lost: Query parameters '?preferencename', '?value', '?id'")

print("\n" + "=" * 80)
print("5. RECOMMENDATION")
print("=" * 80)

print("\nTo achieve ZERO duplicates, we should:")
print("  1. ✅ Keep full path with parameters (or at least parameter placeholders)")
print("  2. ✅ Add query_parameters field (list of query param names)")
print("  3. ✅ Add path_parameters field (list of path param names)")
print("  4. ✅ Keep full resource string for reference")
print("  5. ✅ Deduplicate by (full_path, method) instead of (base_path, method)")

print("\nAlternative (if we want base paths for matching):")
print("  - Keep base_path for matching")
print("  - Add full_path for uniqueness")
print("  - Deduplicate by (full_path, method)")
print("  - This way, endpoints with different params are NOT duplicates")

print("\n" + "=" * 80)

