#!/usr/bin/env python3
"""
Investigate WHY duplicates exist in the endpoint catalog.

This script:
1. Checks if duplicates exist in the source endpoints.json (if available)
2. Examines the parsing/generation process
3. Identifies if duplicates were introduced during embedding
4. Traces the origin of each duplicate
"""
import json
import re
import ast
from pathlib import Path
from collections import defaultdict

repo_root = Path(__file__).parent.parent

print("=" * 80)
print("INVESTIGATING ROOT CAUSE OF ENDPOINT DUPLICATES")
print("=" * 80)
print()

# 1. Check if endpoints.json exists (source file)
endpoints_json = repo_root / "docs" / "endpoints.json"
if endpoints_json.exists():
    print("✅ Found source endpoints.json")
    print(f"   Path: {endpoints_json}")
    print()
    
    with open(endpoints_json, "r", encoding="utf-8") as f:
        try:
            source_data = json.load(f)
            print(f"   Type: {type(source_data)}")
            if isinstance(source_data, list):
                print(f"   Count: {len(source_data)} endpoints")
            elif isinstance(source_data, dict):
                print(f"   Keys: {list(source_data.keys())[:5]}...")
        except Exception as e:
            print(f"   ⚠️ Could not parse as JSON: {e}")
            # Try to read as text to see structure
            f.seek(0)
            content = f.read(1000)
            print(f"   First 1000 chars: {content[:200]}...")
else:
    print("❌ Source endpoints.json NOT FOUND")
    print(f"   Expected: {endpoints_json}")
    print("   Note: Zephyr may use embedded catalog only")
    print()

# 2. Read embedded catalog from SDK
sdk_notebook = repo_root / "spectraSDK.Notebook" / "notebook_content.py"
print("2. Examining embedded catalog in SDK notebook...")
print(f"   Path: {sdk_notebook}")
print()

if not sdk_notebook.exists():
    print("❌ SDK notebook not found!")
    exit(1)

with open(sdk_notebook, "r", encoding="utf-8") as f:
    content = f.read()

# Extract the catalog
match = re.search(r'ZEPHYR_ENDPOINTS_CATALOG\s*=\s*\[(.*?)\]', content, re.DOTALL)
if not match:
    print("❌ Could not find ZEPHYR_ENDPOINTS_CATALOG")
    exit(1)

# Parse using ast.literal_eval (safer than eval)
catalog_str = match.group(1)
catalog_str = "[" + catalog_str + "]"

try:
    endpoints = ast.literal_eval(catalog_str)
    print(f"✅ Parsed {len(endpoints)} endpoints from embedded catalog")
except Exception as e:
    print(f"❌ Could not parse catalog: {e}")
    exit(1)

# 3. Find duplicates and analyze them
print()
print("3. Analyzing duplicates...")
print("=" * 80)

# Group by path + method (true duplicates)
path_method_groups = defaultdict(list)
for i, endpoint in enumerate(endpoints):
    path = endpoint.get("endpoint_path", "")
    method = endpoint.get("http_method", "")
    key = (path, method)
    path_method_groups[key].append((i, endpoint))

true_duplicates = {k: v for k, v in path_method_groups.items() if len(v) > 1}

if true_duplicates:
    print(f"\n🔴 Found {len(true_duplicates)} TRUE DUPLICATE(S) (same path + method):\n")
    
    for (path, method), occurrences in sorted(true_duplicates.items()):
        print(f"   {method} {path}")
        print(f"   Appears {len(occurrences)} time(s) at indices: {[idx for idx, _ in occurrences]}")
        
        # Compare the entries
        descriptions = [ep.get("description", "") for _, ep in occurrences]
        categories = [ep.get("category", "") for _, ep in occurrences]
        hierarchical = [ep.get("hierarchical", False) for _, ep in occurrences]
        
        if len(set(descriptions)) > 1:
            print(f"   ⚠️ DIFFERENT DESCRIPTIONS:")
            for idx, (_, ep) in enumerate(occurrences):
                print(f"      {idx+1}. '{ep.get('description', '')}'")
        
        if len(set(categories)) > 1:
            print(f"   ⚠️ DIFFERENT CATEGORIES:")
            for idx, (_, ep) in enumerate(occurrences):
                print(f"      {idx+1}. Category: {ep.get('category', '')}")
        
        if len(set(hierarchical)) > 1:
            print(f"   ⚠️ DIFFERENT HIERARCHICAL FLAGS:")
            for idx, (_, ep) in enumerate(occurrences):
                print(f"      {idx+1}. Hierarchical: {ep.get('hierarchical', False)}")
        
        # Check if entries are identical
        first_entry = dict(occurrences[0][1])
        all_identical = True
        differences = []
        
        for idx, (_, ep) in enumerate(occurrences[1:], 1):
            for key in first_entry:
                if first_entry[key] != ep.get(key):
                    all_identical = False
                    differences.append(f"      Entry {idx+1}: {key} = {ep.get(key)} (expected {first_entry[key]})")
        
        if all_identical:
            print(f"   ✅ All entries are IDENTICAL (exact duplicate)")
        else:
            print(f"   ⚠️ Entries have DIFFERENCES:")
            for diff in differences:
                print(diff)
        
        print()
else:
    print("✅ No true duplicates found (same path + method)")

# 4. Check if source file has duplicates
if endpoints_json.exists():
    print()
    print("4. Checking source endpoints.json for duplicates...")
    print("=" * 80)
    
    try:
        with open(endpoints_json, "r", encoding="utf-8") as f:
            source_data = json.load(f)
        
        if isinstance(source_data, list):
            source_path_method = defaultdict(list)
            for i, item in enumerate(source_data):
                # Try to extract path and method
                path = item.get("path") or item.get("endpoint_path") or item.get("url") or ""
                method = item.get("method") or item.get("http_method") or item.get("verb") or ""
                if path and method:
                    source_path_method[(path, method)].append(i)
            
            source_duplicates = {k: v for k, v in source_path_method.items() if len(v) > 1}
            
            if source_duplicates:
                print(f"\n🔴 Source file has {len(source_duplicates)} duplicate(s):")
                for (path, method), indices in list(source_duplicates.items())[:5]:
                    print(f"   {method} {path} - appears at indices: {indices}")
                print("\n   💡 CONCLUSION: Duplicates exist in SOURCE file")
            else:
                print("\n✅ Source file has NO duplicates")
                print("   💡 CONCLUSION: Duplicates introduced during embedding/parsing")
        else:
            print("   ⚠️ Source file structure not recognized (not a list)")
    except Exception as e:
        print(f"   ⚠️ Could not analyze source file: {e}")

# 5. Check generation scripts
print()
print("5. Checking generation/embedding scripts...")
print("=" * 80)

generation_scripts = [
    repo_root / "scripts" / "generate_endpoints_module.py",
    repo_root / "scripts" / "embed_catalog_to_sdk.py",
    repo_root / "scripts" / "embed_catalog.py",
    repo_root / "scripts" / "parse_endpoints.py",
]

for script_path in generation_scripts:
    if script_path.exists():
        print(f"\n✅ Found: {script_path.name}")
        # Check if script has deduplication logic
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
            if "duplicate" in script_content.lower() or "unique" in script_content.lower() or "set(" in script_content:
                print(f"   Has deduplication logic: YES")
            else:
                print(f"   Has deduplication logic: NO ⚠️")
    else:
        print(f"❌ Not found: {script_path.name}")

# 6. Check for malformed entries
print()
print("6. Checking for malformed entries...")
print("=" * 80)

malformed = []
for i, endpoint in enumerate(endpoints):
    path = endpoint.get("endpoint_path", "")
    method = endpoint.get("http_method", "")
    description = endpoint.get("description", "")
    
    # Check for malformed paths
    if path.startswith("/") and "/" in path[1:]:
        # Check for double slashes
        if "//" in path:
            malformed.append((i, "double_slash", path))
        # Check for uppercase in path (should be lowercase)
        if any(c.isupper() for c in path if c not in ["{", "}", "/"]):
            malformed.append((i, "uppercase_in_path", path))
        # Check for spaces
        if " " in path:
            malformed.append((i, "space_in_path", path))
    
    # Check for malformed methods
    if method and method.upper() != method:
        malformed.append((i, "lowercase_method", method))
    
    # Check for weird descriptions
    if description and len(description) > 200:
        malformed.append((i, "long_description", description[:50]))

if malformed:
    print(f"\n⚠️ Found {len(malformed)} potentially malformed entry/entries:")
    for idx, (i, issue_type, value) in enumerate(malformed[:10], 1):
        print(f"   {idx}. Index {i}: {issue_type}")
        print(f"      Value: {value[:100]}")
else:
    print("\n✅ No obvious malformed entries")

# 7. Summary and recommendations
print()
print("=" * 80)
print("ROOT CAUSE ANALYSIS SUMMARY")
print("=" * 80)

if true_duplicates:
    print("\n🔴 ROOT CAUSE:")
    print("   True duplicates exist in embedded catalog")
    print()
    print("   POSSIBLE CAUSES:")
    print("   1. Source endpoints.json contains duplicates")
    print("   2. Parsing/generation script doesn't deduplicate")
    print("   3. Manual edits introduced duplicates")
    print("   4. Multiple sources merged without deduplication")
    print()
    print("   RECOMMENDATION:")
    print("   - Add deduplication logic to generation script")
    print("   - Remove duplicates from source file (if exists)")
    print("   - Re-generate embedded catalog")
else:
    print("\n✅ No true duplicates found")
    print("   (Only URL change duplicates, which are acceptable)")

print()
print("=" * 80)

