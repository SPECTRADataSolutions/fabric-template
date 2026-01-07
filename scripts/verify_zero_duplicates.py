#!/usr/bin/env python3
"""Verify that the parsed catalog has zero duplicates."""
import ast
import json
from pathlib import Path
from collections import defaultdict

repo_root = Path(__file__).parent
catalog_file = repo_root / "endpoints_catalog.py"

print("=" * 80)
print("VERIFYING ZERO DUPLICATES IN PARSED CATALOG")
print("=" * 80)
print()

# Import the catalog directly
import sys
sys.path.insert(0, str(repo_root))
from endpoints_catalog import ENDPOINTS_CATALOG
catalog = ENDPOINTS_CATALOG

print(f"✅ Loaded catalog: {len(catalog)} endpoints")
print()

# Check for duplicates by (full_path, method)
seen = {}
duplicates = []

for i, ep in enumerate(catalog):
    key = (ep.get("full_path", ""), ep.get("http_method", ""))
    if key in seen:
        duplicates.append((i, seen[key], key, ep))
    else:
        seen[key] = i

if duplicates:
    print(f"🔴 Found {len(duplicates)} duplicate(s):\n")
    for dup_idx, orig_idx, key, ep in duplicates:
        print(f"   {key[1]} {key[0]}")
        print(f"   Original: Index {orig_idx}")
        print(f"   Duplicate: Index {dup_idx}")
        print(f"   Description: {ep.get('description', '')[:60]}")
        print()
else:
    print("✅ ZERO DUPLICATES - All endpoints are unique!")
    print()

# Check metadata completeness
print("=" * 80)
print("METADATA COMPLETENESS CHECK")
print("=" * 80)
print()

missing_fields = defaultdict(int)
for ep in catalog:
    required_fields = ["endpoint_path", "full_path", "http_method", "category", "description"]
    for field in required_fields:
        if not ep.get(field):
            missing_fields[field] += 1

if missing_fields:
    print("⚠️ Missing fields:")
    for field, count in missing_fields.items():
        print(f"   {field}: {count} endpoints missing")
else:
    print("✅ All required fields present")

# Check new metadata fields
has_query_params = sum(1 for ep in catalog if ep.get("query_parameters"))
has_path_params = sum(1 for ep in catalog if ep.get("path_parameters"))
has_resource = sum(1 for ep in catalog if ep.get("resource"))

print(f"\n📊 Metadata coverage:")
print(f"   Endpoints with query_parameters: {has_query_params}/{len(catalog)}")
print(f"   Endpoints with path_parameters: {has_path_params}/{len(catalog)}")
print(f"   Endpoints with resource string: {has_resource}/{len(catalog)}")

# Sample endpoints with parameters
print("\n📋 Sample endpoints with parameters:")
samples = [ep for ep in catalog if ep.get("query_parameters") or ep.get("path_parameters")][:5]
for ep in samples:
    print(f"\n   {ep['http_method']} {ep['full_path']}")
    if ep.get("path_parameters"):
        print(f"      Path params: {ep['path_parameters']}")
    if ep.get("query_parameters"):
        print(f"      Query params: {ep['query_parameters']}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total endpoints: {len(catalog)}")
print(f"Unique (full_path, method): {len(seen)}")
print(f"Duplicates: {len(duplicates)}")
print(f"Status: {'✅ ZERO DUPLICATES' if not duplicates else '🔴 HAS DUPLICATES'}")

