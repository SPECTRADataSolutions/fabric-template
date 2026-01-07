#!/usr/bin/env python3
"""
Extract and categorize endpoints from endpoints.json for testing.
Identifies which endpoints are relevant for Source stage health checks.
"""

import json
from pathlib import Path
from typing import Any

# Load endpoints
repo_root = Path(__file__).parent.parent
endpoints_file = repo_root / "docs" / "endpoints.json"

with open(endpoints_file, "r", encoding="utf-8") as f:
    data = json.load(f)

endpoints = data.get("endpoints", [])

# Categorize endpoints
categories = {
    "data_extraction": [],  # Endpoints we'll actually extract data from
    "search_query": [],      # Search/query endpoints
    "admin": [],            # Admin/configuration endpoints
    "write_operations": [],  # POST/PUT/DELETE endpoints
    "other": []             # Everything else
}

# Keywords that indicate data extraction endpoints
data_keywords = [
    "project", "release", "cycle", "execution", "testcase", "requirement",
    "teststep", "testresult", "attachment", "user", "group", "audit"
]

# Keywords that indicate search endpoints
search_keywords = ["search", "advancesearch", "query", "filter"]

for ep in endpoints:
    resource = ep.get("resource", "").lower()
    method = ep.get("method", "").upper()
    path = ep.get("path", "")
    
    # Extract path from resource description
    # Format: "Get Projects [/project]"
    if "[" in resource and "]" in resource:
        path_start = resource.find("[")
        path_end = resource.find("]")
        if path_start != -1 and path_end != -1:
            path = resource[path_start + 1:path_end].split("?")[0]  # Remove query params
    
    # Categorize
    if method in ["POST", "PUT", "DELETE"]:
        categories["write_operations"].append(ep)
    elif any(kw in resource.lower() for kw in ["admin", "preference", "backup", "ldap", "automation"]):
        categories["admin"].append(ep)
    elif any(kw in resource.lower() for kw in search_keywords):
        categories["search_query"].append(ep)
    elif any(kw in resource.lower() for kw in data_keywords):
        categories["data_extraction"].append(ep)
    else:
        categories["other"].append(ep)

# Print summary
print("=" * 60)
print("Endpoint Categorization")
print("=" * 60)
print(f"Total endpoints: {len(endpoints)}")
print()
for cat, eps in categories.items():
    print(f"{cat}: {len(eps)} endpoints")
print()

# Show data extraction endpoints (most relevant for Source stage)
print("=" * 60)
print("Data Extraction Endpoints (for Source stage testing)")
print("=" * 60)
for ep in categories["data_extraction"][:50]:  # Show first 50
    resource = ep.get("resource", "")
    method = ep.get("method", "")
    # Extract path
    path = ""
    if "[" in resource and "]" in resource:
        path_start = resource.find("[")
        path_end = resource.find("]")
        if path_start != -1 and path_end != -1:
            path = resource[path_start + 1:path_end].split("?")[0]
    print(f"  {method:6} {path}")

if len(categories["data_extraction"]) > 50:
    print(f"  ... and {len(categories['data_extraction']) - 50} more")

print()
print("=" * 60)
print("Search/Query Endpoints")
print("=" * 60)
for ep in categories["search_query"][:20]:  # Show first 20
    resource = ep.get("resource", "")
    method = ep.get("method", "")
    path = ""
    if "[" in resource and "]" in resource:
        path_start = resource.find("[")
        path_end = resource.find("]")
        if path_start != -1 and path_end != -1:
            path = resource[path_start + 1:path_end].split("?")[0]
    print(f"  {method:6} {path}")





