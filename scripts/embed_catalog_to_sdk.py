#!/usr/bin/env python3
"""Embed Zephyr endpoints catalog into SDK notebook."""

with open('scripts/catalog_embedded.txt', 'r', encoding='utf-8') as f:
    catalog = f.read()

with open('spectraSDK.Notebook/notebook_content.py', 'r', encoding='utf-8') as f:
    notebook = f.read()

# Find insertion point (after "# Hierarchical: 25/228 endpoints require parent IDs")
insert_marker = "# Hierarchical: 25/228 endpoints require parent IDs"
insert_idx = notebook.find(insert_marker)

if insert_idx == -1:
    raise ValueError("Could not find insertion marker in notebook")

# Find the end of the header section (before "# METADATA")
metadata_marker = "# METADATA ********************"
metadata_idx = notebook.find(metadata_marker, insert_idx)

if metadata_idx == -1:
    raise ValueError("Could not find METADATA marker after insertion point")

# Build new notebook: header + catalog + rest
new_notebook = (
    notebook[:insert_idx + len(insert_marker)] + 
    "\n\n" + 
    catalog + 
    "\n\n" + 
    notebook[metadata_idx:]
)

with open('spectraSDK.Notebook/notebook_content.py', 'w', encoding='utf-8') as f:
    f.write(new_notebook)

print(f"✅ Embedded {len(catalog.split(chr(10)))} lines of catalog into SDK notebook")

