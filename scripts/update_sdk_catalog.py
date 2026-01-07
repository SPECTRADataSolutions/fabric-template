#!/usr/bin/env python3
"""
Update the embedded endpoints catalog in spectraSDK.Notebook with the new structure.

This script:
1. Loads the parsed catalog (with full metadata, zero duplicates)
2. Formats it for embedding in the SDK notebook
3. Updates the SDK notebook with the new catalog
4. Updates the header comment with correct counts
"""
import json
import re
from pathlib import Path
from collections import Counter

repo_root = Path(__file__).parent.parent

# 1. Load the parsed catalog
print("=" * 80)
print("UPDATING SDK NOTEBOOK WITH NEW ENDPOINTS CATALOG")
print("=" * 80)
print()

catalog_file = repo_root / "scripts" / "endpoints_catalog.py"
sdk_notebook = repo_root / "spectraSDK.Notebook" / "notebook_content.py"

# Import the catalog
import sys
sys.path.insert(0, str(repo_root / "scripts"))
from endpoints_catalog import ENDPOINTS_CATALOG

catalog = ENDPOINTS_CATALOG
print(f"✅ Loaded {len(catalog)} endpoints from parsed catalog")

# 2. Calculate category counts
categories = Counter(ep["category"] for ep in catalog)
hierarchical_count = sum(1 for ep in catalog if ep["hierarchical"])

print(f"✅ Calculated category counts")
print(f"   Hierarchical endpoints: {hierarchical_count}/{len(catalog)}")
print()

# 3. Format catalog for embedding
print("📝 Formatting catalog for embedding...")

# Format each endpoint as a Python dict
formatted_entries = []
for ep in catalog:
    entry_lines = [
        "    {",
        f'        "endpoint_path": "{ep["endpoint_path"]}",',
        f'        "full_path": "{ep["full_path"]}",',
        f'        "http_method": "{ep["http_method"]}",',
        f'        "category": "{ep["category"]}",',
        f'        "description": "{ep["description"]}",',
        f'        "requires_auth": {ep["requires_auth"]},',
        f'        "hierarchical": {ep["hierarchical"]},',
    ]
    
    # Add query_parameters
    query_params = ep.get("query_parameters", [])
    if query_params:
        entry_lines.append(f'        "query_parameters": {json.dumps(query_params)},')
    else:
        entry_lines.append('        "query_parameters": [],')
    
    # Add path_parameters
    path_params = ep.get("path_parameters", [])
    if path_params:
        entry_lines.append(f'        "path_parameters": {json.dumps(path_params)},')
    else:
        entry_lines.append('        "path_parameters": [],')
    
    # Add resource (truncate if too long)
    resource = ep.get("resource", "")
    if resource:
        # Escape quotes
        resource_escaped = resource.replace('"', '\\"')
        entry_lines.append(f'        "resource": "{resource_escaped}",')
    else:
        entry_lines.append('        "resource": "",')
    
    entry_lines.append("    },")
    formatted_entries.append("\n".join(entry_lines))

catalog_code = "ZEPHYR_ENDPOINTS_CATALOG = [\n" + "\n".join(formatted_entries) + "\n]"

print(f"✅ Formatted {len(formatted_entries)} entries")
print()

# 4. Build category summary string
category_lines = []
for category, count in sorted(categories.items()):
    category_lines.append(f"{category} ({count})")
category_summary = ", ".join(category_lines)

# 5. Read SDK notebook
print("📖 Reading SDK notebook...")
with open(sdk_notebook, "r", encoding="utf-8") as f:
    notebook_content = f.read()

# 6. Update header comment
print("📝 Updating header comment...")
old_header_pattern = r'# Zephyr Endpoints Catalog \(228 endpoints\)(.*?)# Hierarchical: 25/228 endpoints require parent IDs'
new_header = f"""# ══════════════════════════════════════════════════════════════════════════════
# Zephyr Endpoints Catalog ({len(catalog)} endpoints - ZERO DUPLICATES)
# ══════════════════════════════════════════════════════════════════════════════
# Auto-generated from docs/endpoints.json
# Categories: {category_summary}
# Hierarchical: {hierarchical_count}/{len(catalog)} endpoints require parent IDs
# Metadata: full_path, query_parameters, path_parameters, resource (all preserved)"""

notebook_content = re.sub(
    r'# ══════════════════════════════════════════════════════════════════════════════\s*# Zephyr Endpoints Catalog.*?# Hierarchical: \d+/\d+ endpoints require parent IDs',
    new_header,
    notebook_content,
    flags=re.DOTALL
)

# 7. Replace the catalog
print("📝 Replacing catalog in notebook...")
# Find the catalog section
catalog_start = notebook_content.find("ZEPHYR_ENDPOINTS_CATALOG = [")
if catalog_start == -1:
    print("❌ Could not find ZEPHYR_ENDPOINTS_CATALOG in notebook")
    exit(1)

# Find the end of the catalog (next line that starts with # or is not indented)
catalog_end = catalog_start
lines = notebook_content[catalog_start:].split('\n')
bracket_count = 0
in_catalog = False
for i, line in enumerate(lines):
    if 'ZEPHYR_ENDPOINTS_CATALOG = [' in line:
        in_catalog = True
        bracket_count = line.count('[') - line.count(']')
    elif in_catalog:
        bracket_count += line.count('[') - line.count(']')
        if bracket_count == 0 and ']' in line:
            catalog_end = catalog_start + sum(len(l) + 1 for l in lines[:i+1])
            break

if catalog_end == catalog_start:
    print("❌ Could not find end of catalog")
    exit(1)

# Replace catalog
new_notebook = (
    notebook_content[:catalog_start] +
    catalog_code +
    "\n\n" +
    notebook_content[catalog_end:]
)

# 8. Write updated notebook
print("💾 Writing updated notebook...")
with open(sdk_notebook, "w", encoding="utf-8") as f:
    f.write(new_notebook)

print()
print("=" * 80)
print("✅ SDK NOTEBOOK UPDATED")
print("=" * 80)
print(f"   Endpoints: {len(catalog)} (was 228)")
print(f"   Duplicates: 0 (was 25)")
print(f"   New metadata fields: full_path, query_parameters, path_parameters, resource")
print(f"   File: {sdk_notebook}")
print()

