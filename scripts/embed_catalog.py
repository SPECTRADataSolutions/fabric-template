#!/usr/bin/env python3
"""
Embed Zephyr endpoints catalog in SDK notebook.
Converts JSON-style true/false to Python True/False.
"""

import re

# Read the generated catalog
with open('scripts/endpoints_catalog.py', 'r') as f:
    catalog_content = f.read()

# Convert JSON booleans to Python booleans
catalog_content = catalog_content.replace('true', 'True').replace('false', 'False')

# Extract just the ENDPOINTS_CATALOG list (lines 8-1833)
lines = catalog_content.split('\n')
catalog_lines = []
in_catalog = False

for line in lines:
    if 'ENDPOINTS_CATALOG = [' in line:
        in_catalog = True
        catalog_lines.append('ZEPHYR_ENDPOINTS_CATALOG = [')
    elif in_catalog:
        if line.strip() == ']':
            catalog_lines.append(']')
            break
        catalog_lines.append(line)

catalog_embedded = '\n'.join(catalog_lines)

print(f"✅ Generated embedded catalog ({len(catalog_embedded)} chars)")
print(f"📊 First 300 chars:")
print(catalog_embedded[:300])
print("\n...\n")
print(f"📊 Last 300 chars:")
print(catalog_embedded[-300:])

# Save to a temporary file for inspection
with open('scripts/catalog_embedded.txt', 'w') as f:
    f.write(catalog_embedded)

print(f"\n💾 Saved to scripts/catalog_embedded.txt")

