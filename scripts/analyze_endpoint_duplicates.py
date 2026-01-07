#!/usr/bin/env python3
"""
Analyze Zephyr endpoints catalog for duplicate titles and check if they're due to URL changes.

This script:
1. Reads the embedded endpoints catalog from spectraSDK.Notebook
2. Finds endpoints with duplicate titles (description field)
3. Checks if duplicates have different endpoint_path values
4. Reports findings
"""
import json
import re
from pathlib import Path
from collections import defaultdict

# Get the SDK notebook path
repo_root = Path(__file__).parent.parent
sdk_notebook = repo_root / "spectraSDK.Notebook" / "notebook_content.py"

print("=" * 80)
print("ANALYZING ENDPOINT DUPLICATES IN ZEPHYR CATALOG")
print("=" * 80)
print(f"\nReading from: {sdk_notebook}")
print()

# Read the SDK notebook
if not sdk_notebook.exists():
    print(f"❌ ERROR: SDK notebook not found at {sdk_notebook}")
    exit(1)

with open(sdk_notebook, "r", encoding="utf-8") as f:
    content = f.read()

# Extract the ZEPHYR_ENDPOINTS_CATALOG
# Look for the pattern: ZEPHYR_ENDPOINTS_CATALOG = [
match = re.search(r'ZEPHYR_ENDPOINTS_CATALOG\s*=\s*\[(.*?)\]', content, re.DOTALL)
if not match:
    print("❌ ERROR: Could not find ZEPHYR_ENDPOINTS_CATALOG in SDK notebook")
    exit(1)

# Parse the catalog (it's Python dict syntax, not JSON)
# We'll use eval (safe here as it's our own code)
try:
    # Extract just the list content
    catalog_str = match.group(1)
    # Wrap it in brackets to make it a valid Python expression
    catalog_str = "[" + catalog_str + "]"
    # Replace single quotes with double quotes for JSON compatibility
    catalog_str = catalog_str.replace("'", '"')
    # Fix Python booleans to JSON booleans
    catalog_str = catalog_str.replace("True", "true").replace("False", "false")
    # Parse as JSON
    endpoints = json.loads(catalog_str)
except Exception as e:
    print(f"❌ ERROR: Could not parse endpoints catalog: {e}")
    print("\nTrying alternative parsing method...")
    
    # Alternative: Use ast.literal_eval
    import ast
    try:
        catalog_str = match.group(1)
        catalog_str = "[" + catalog_str + "]"
        endpoints = ast.literal_eval(catalog_str)
    except Exception as e2:
        print(f"❌ ERROR: Alternative parsing also failed: {e2}")
        exit(1)

print(f"✅ Found {len(endpoints)} endpoints in catalog")
print()

# Group by description (title)
description_groups = defaultdict(list)
for endpoint in endpoints:
    description = endpoint.get("description", "").strip()
    if description:
        description_groups[description].append(endpoint)

# Find duplicates
duplicates = {desc: endpoints_list for desc, endpoints_list in description_groups.items() if len(endpoints_list) > 1}

if not duplicates:
    print("✅ No duplicate endpoint titles found!")
    print()
else:
    print(f"⚠️ Found {len(duplicates)} duplicate title(s):\n")
    print("=" * 80)
    
    # Analyze each duplicate
    for description, endpoints_list in sorted(duplicates.items()):
        print(f"\n📋 Duplicate Title: '{description}'")
        print(f"   Appears {len(endpoints_list)} time(s):\n")
        
        # Check if paths are different
        paths = [ep.get("endpoint_path", "") for ep in endpoints_list]
        methods = [ep.get("http_method", "") for ep in endpoints_list]
        categories = [ep.get("category", "") for ep in endpoints_list]
        
        unique_paths = set(paths)
        unique_methods = set(methods)
        unique_categories = set(categories)
        
        print(f"   Unique paths: {len(unique_paths)}")
        print(f"   Unique methods: {len(unique_methods)}")
        print(f"   Unique categories: {len(unique_categories)}")
        
        if len(unique_paths) > 1:
            print(f"\n   ⚠️ DIFFERENT PATHS (likely URL change):")
            for i, endpoint in enumerate(endpoints_list, 1):
                path = endpoint.get("endpoint_path", "")
                method = endpoint.get("http_method", "")
                category = endpoint.get("category", "")
                hierarchical = endpoint.get("hierarchical", False)
                print(f"      {i}. {method} {path}")
                print(f"         Category: {category}, Hierarchical: {hierarchical}")
        elif len(unique_methods) > 1:
            print(f"\n   ⚠️ DIFFERENT METHODS (same path, different HTTP method):")
            for i, endpoint in enumerate(endpoints_list, 1):
                path = endpoint.get("endpoint_path", "")
                method = endpoint.get("http_method", "")
                category = endpoint.get("category", "")
                print(f"      {i}. {method} {path} (Category: {category})")
        else:
            print(f"\n   ⚠️ SAME PATH AND METHOD (true duplicate?):")
            for i, endpoint in enumerate(endpoints_list, 1):
                path = endpoint.get("endpoint_path", "")
                method = endpoint.get("http_method", "")
                category = endpoint.get("category", "")
                print(f"      {i}. {method} {path} (Category: {category})")
        
        print()

print("=" * 80)
print("\nSUMMARY")
print("=" * 80)
print(f"Total endpoints: {len(endpoints)}")
print(f"Unique descriptions: {len(description_groups)}")
print(f"Duplicate titles: {len(duplicates)}")

if duplicates:
    print("\n💡 RECOMMENDATION:")
    print("   - If duplicates have different paths → Likely URL versioning/change")
    print("   - If duplicates have different methods → Same endpoint, different operations")
    print("   - If duplicates have same path+method → True duplicate, should be deduplicated")

