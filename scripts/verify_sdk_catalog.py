#!/usr/bin/env python3
"""Verify the embedded catalog in SDK notebook has zero duplicates."""
import re
import ast
from pathlib import Path

repo_root = Path(__file__).parent.parent
sdk_notebook = repo_root / "spectraSDK.Notebook" / "notebook_content.py"

print("=" * 80)
print("VERIFYING EMBEDDED CATALOG IN SDK NOTEBOOK")
print("=" * 80)
print()

# Read notebook
with open(sdk_notebook, "r", encoding="utf-8") as f:
    content = f.read()

# Extract catalog
match = re.search(r'ZEPHYR_ENDPOINTS_CATALOG\s*=\s*\[(.*?)\]', content, re.DOTALL)
if not match:
    print("❌ Could not find ZEPHYR_ENDPOINTS_CATALOG")
    exit(1)

catalog_str = "[" + match.group(1) + "]"
catalog = ast.literal_eval(catalog_str)

print(f"✅ Loaded {len(catalog)} endpoints from embedded catalog")
print()

# Check for duplicates
seen = set()
duplicates = []

for i, ep in enumerate(catalog):
    full_path = ep.get("full_path", "")
    method = ep.get("http_method", "")
    key = (full_path, method)
    
    if key in seen:
        duplicates.append((i, key, ep))
    else:
        seen.add(key)

if duplicates:
    print(f"🔴 Found {len(duplicates)} duplicate(s):\n")
    for dup_idx, key, ep in duplicates[:5]:
        print(f"   {key[1]} {key[0]}")
        print(f"   Index: {dup_idx}")
        print(f"   Description: {ep.get('description', '')[:60]}")
        print()
else:
    print("✅ ZERO DUPLICATES - All endpoints are unique!")
    print()

# Check metadata fields
print("=" * 80)
print("METADATA FIELDS CHECK")
print("=" * 80)
print()

required_fields = ["endpoint_path", "full_path", "http_method", "category", "description"]
new_fields = ["query_parameters", "path_parameters", "resource"]

all_present = True
for field in required_fields + new_fields:
    missing = sum(1 for ep in catalog if field not in ep)
    if missing > 0:
        print(f"⚠️ {field}: {missing} endpoints missing")
        all_present = False
    else:
        print(f"✅ {field}: All {len(catalog)} endpoints have it")

if all_present:
    print("\n✅ All metadata fields present!")

# Sample endpoints with parameters
print("\n" + "=" * 80)
print("SAMPLE ENDPOINTS WITH PARAMETERS")
print("=" * 80)
print()

samples = [ep for ep in catalog if ep.get("query_parameters") or ep.get("path_parameters")][:3]
for ep in samples:
    print(f"\n{ep['http_method']} {ep['full_path']}")
    print(f"   Base path: {ep['endpoint_path']}")
    if ep.get("path_parameters"):
        print(f"   Path params: {ep['path_parameters']}")
    if ep.get("query_parameters"):
        print(f"   Query params: {ep['query_parameters']}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total endpoints: {len(catalog)}")
print(f"Unique (full_path, method): {len(seen)}")
print(f"Duplicates: {len(duplicates)}")
print(f"Status: {'✅ ZERO DUPLICATES' if not duplicates else '🔴 HAS DUPLICATES'}")
print(f"Metadata: {'✅ Complete' if all_present else '⚠️ Incomplete'}")

