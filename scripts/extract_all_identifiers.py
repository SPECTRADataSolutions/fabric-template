#!/usr/bin/env python3
"""
Extract ALL identifiers from sample data for comprehensive endpoint testing.
Looks for any field ending in 'Id' or 'ID' in all responses.
"""

import os
import requests
import json
from pathlib import Path

# Configuration
base_url = os.environ.get("DXC_ZEPHYR_BASE_URL", "https://velonetic.yourzephyr.com")
base_path = os.environ.get("DXC_ZEPHYR_BASE_PATH", "/flex/services/rest/latest")
api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN")

full_base = f"{base_url}{base_path}"
headers = {'Authorization': f'Bearer {api_token}'}

# Dictionary to store all IDs by type
all_ids = {}

def extract_ids_from_dict(data, parent_key=''):
    """Recursively extract all fields ending in 'Id' or 'ID'."""
    if isinstance(data, dict):
        for key, value in data.items():
            # Check if key ends with Id or ID
            if key.endswith('Id') or key.endswith('ID'):
                if value is not None and value != '':
                    # Store the ID
                    if key not in all_ids:
                        all_ids[key] = set()
                    if isinstance(value, (int, str)):
                        all_ids[key].add(value)
            
            # Recurse into nested structures
            extract_ids_from_dict(value, key)
    elif isinstance(data, list):
        for item in data:
            extract_ids_from_dict(item, parent_key)

print('='*80)
print('EXTRACTING ALL IDENTIFIERS FROM SAMPLE DATA')
print('='*80)
print()

# Extract IDs from CSV files
print('Phase 1: Checking CSV files...')
csv_dir = Path(__file__).parent.parent / "docs" / "api-discovery" / "sample-100-extraction"

try:
    import csv
    
    for csv_file in csv_dir.glob('*.csv'):
        print(f'  Scanning {csv_file.name}...')
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                extract_ids_from_dict(row)
except Exception as e:
    print(f'  ⚠️ Error reading CSVs: {e}')

print(f'  Found {len(all_ids)} ID types from CSVs')
print()

# Extract IDs from API calls - get richer nested data
print('Phase 2: Extracting IDs from live API calls...')

# Get detailed execution with all nested fields
print('  Getting executions with nested data...')
r = requests.get(f'{full_base}/execution', headers=headers, params={'cycleid': 164, 'maxRecords': 10})
if r.status_code == 200:
    data = r.json()
    extract_ids_from_dict(data)
    print('    ✅ Extracted from execution response')

# Get detailed project data
print('  Getting project details...')
r = requests.get(f'{full_base}/project/details', headers=headers)
if r.status_code == 200:
    data = r.json()
    extract_ids_from_dict(data)
    print('    ✅ Extracted from project response')

# Get release data
print('  Getting release data...')
r = requests.get(f'{full_base}/release', headers=headers)
if r.status_code == 200:
    data = r.json()
    extract_ids_from_dict(data)
    print('    ✅ Extracted from release response')

# Get user data (might have defectId or other IDs)
print('  Getting user data...')
r = requests.get(f'{full_base}/user/filter', headers=headers)
if r.status_code == 200:
    data = r.json()
    extract_ids_from_dict(data)
    print('    ✅ Extracted from user response')

# Get test case tree data
print('  Getting test case tree...')
r = requests.get(f'{full_base}/testcasetree/projectrepository/44', headers=headers)
if r.status_code == 200:
    data = r.json()
    extract_ids_from_dict(data)
    print('    ✅ Extracted from test case tree response')

# Get field data
print('  Getting field data...')
r = requests.get(f'{full_base}/field/metadata', headers=headers)
if r.status_code == 200:
    data = r.json()
    extract_ids_from_dict(data)
    print('    ✅ Extracted from field metadata response')

print()
print('='*80)
print('ALL IDENTIFIERS FOUND')
print('='*80)

# Convert sets to sorted lists and display
for key in sorted(all_ids.keys()):
    # Convert to list and try to get a sample
    id_values = list(all_ids[key])
    # Try to convert to int for sorting, keep as is if can't
    try:
        id_list = sorted([int(x) if isinstance(x, (int, str)) and str(x).isdigit() else x for x in id_values if isinstance(x, int) or (isinstance(x, str) and str(x).isdigit())])[:10]
    except:
        id_list = list(id_values)[:10]
    
    print(f'{key:30} → {len(all_ids[key]):4} unique values (sample: {id_list[:3]})')

# Save to JSON for use in testing
output_file = Path(__file__).parent.parent / "docs" / "api-discovery" / "all_identifiers.json"
# Convert sets to lists, ensuring all values are serializable
ids_serializable = {}
for key, values in all_ids.items():
    # Convert to ints where possible
    id_list = []
    for val in values:
        try:
            if isinstance(val, str) and val.isdigit():
                id_list.append(int(val))
            elif isinstance(val, int):
                id_list.append(val)
            else:
                id_list.append(str(val))
        except:
            id_list.append(str(val))
    ids_serializable[key] = sorted(id_list) if id_list and all(isinstance(x, int) for x in id_list) else id_list

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(ids_serializable, f, indent=2)

print()
print(f'✅ Identifiers saved to: {output_file}')
print()
print('Now run: python scripts/test_all_endpoints_comprehensive.py')
print('(Updated script will use these identifiers)')

