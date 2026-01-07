#!/usr/bin/env python3
"""
Full dimensional dataset extraction.
Extracts ALL projects, releases, cycles, and executions into dimensional tables.
Saves results as CSV files for inspection and loading.
"""

import os
import requests
import csv
import json
from datetime import datetime
from pathlib import Path

# Configuration
base_url = os.environ.get("DXC_ZEPHYR_BASE_URL", "https://velonetic.yourzephyr.com")
base_path = os.environ.get("DXC_ZEPHYR_BASE_PATH", "/flex/services/rest/latest")
api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN")

full_base = f"{base_url}{base_path}"
headers = {'Authorization': f'Bearer {api_token}'}

# Output directory
output_dir = Path(__file__).parent.parent / "docs" / "api-discovery" / "full-extraction"
output_dir.mkdir(parents=True, exist_ok=True)

# Collections for dimensional tables
dim_projects = []
dim_releases = []
dim_cycles = []
fact_executions = []
dim_test_cases = {}  # Dictionary to deduplicate

print('='*80)
print('FULL DIMENSIONAL DATASET EXTRACTION')
print('='*80)
print(f'Started: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'Output: {output_dir}')
print()

# Statistics
stats = {
    'projects_extracted': 0,
    'releases_extracted': 0,
    'cycles_extracted': 0,
    'executions_extracted': 0,
    'test_cases_extracted': 0,
    'api_calls': 0,
    'errors': []
}

print('Phase 1: Extracting dimProject...')
r = requests.get(f'{full_base}/project/details', headers=headers)
stats['api_calls'] += 1

if r.status_code == 200:
    projects = r.json()
    print(f'  Found {len(projects)} projects')
    
    for project in projects:
        dim_projects.append({
            'projectId': project['id'],
            'projectName': project.get('name', ''),
            'projectKey': project.get('key', ''),
            'projectDescription': project.get('description', ''),
            'projectLead': project.get('lead', ''),
            'isShared': project.get('shared', False),
            'isActive': project.get('active', True)
        })
        stats['projects_extracted'] += 1
    
    print(f'  ✅ Extracted {stats["projects_extracted"]} projects')
else:
    error = f'Failed to get projects: HTTP {r.status_code}'
    print(f'  ❌ {error}')
    stats['errors'].append(error)

print()
print('Phase 2: Extracting dimRelease...')

for project in dim_projects:
    project_id = project['projectId']
    print(f'  Project {project_id}: {project["projectName"]}')
    
    r = requests.get(f'{full_base}/release/project/{project_id}', headers=headers)
    stats['api_calls'] += 1
    
    if r.status_code == 200:
        releases = r.json()
        print(f'    └── {len(releases)} release(s)')
        
        for release in releases:
            dim_releases.append({
                'releaseId': release['id'],
                'releaseName': release.get('name', ''),
                'projectId': project_id,
                'releaseDescription': release.get('description', ''),
                'startDate': release.get('startDate', ''),
                'endDate': release.get('endDate', ''),
                'releaseStatus': release.get('status', '')
            })
            stats['releases_extracted'] += 1
    else:
        error = f'Failed to get releases for project {project_id}: HTTP {r.status_code}'
        print(f'    └── ❌ {error}')
        stats['errors'].append(error)

print(f'  ✅ Extracted {stats["releases_extracted"]} releases')

print()
print('Phase 3: Extracting dimCycle...')

for release in dim_releases:
    release_id = release['releaseId']
    print(f'  Release {release_id}: {release["releaseName"][:50]}')
    
    r = requests.get(f'{full_base}/cycle/release/{release_id}', headers=headers)
    stats['api_calls'] += 1
    
    if r.status_code == 200:
        cycles = r.json()
        print(f'    └── {len(cycles)} cycle(s)')
        
        for cycle in cycles:
            dim_cycles.append({
                'cycleId': cycle['id'],
                'cycleName': cycle.get('name', ''),
                'releaseId': release_id,
                'cycleDescription': cycle.get('description', ''),
                'environment': cycle.get('environment', ''),
                'build': cycle.get('build', ''),
                'startDate': cycle.get('startDate', ''),
                'endDate': cycle.get('endDate', '')
            })
            stats['cycles_extracted'] += 1
    else:
        error = f'Failed to get cycles for release {release_id}: HTTP {r.status_code}'
        print(f'    └── ⚠️ {error}')
        # Don't add to errors - empty releases are valid

print(f'  ✅ Extracted {stats["cycles_extracted"]} cycles')

print()
print('Phase 4: Extracting factTestExecution (with pagination)...')

for cycle in dim_cycles:
    cycle_id = cycle['cycleId']
    print(f'  Cycle {cycle_id}: {cycle["cycleName"][:50]}')
    
    # Handle pagination
    page = 0
    total_for_cycle = 0
    
    while True:
        params = {'cycleid': cycle_id, 'offset': page * 100, 'maxRecords': 100}
        r = requests.get(f'{full_base}/execution', headers=headers, params=params)
        stats['api_calls'] += 1
        
        if r.status_code == 200:
            exec_data = r.json()
            exec_results = exec_data.get('results', [])
            
            if not exec_results:
                break  # No more results
            
            for exec in exec_results:
                # Extract execution
                fact_executions.append({
                    'executionId': exec.get('id'),
                    'cycleId': cycle_id,
                    'testCaseId': exec.get('tcrTreeTestcase', {}).get('id', None),
                    'testerId': exec.get('testerId', None),
                    'testerName': exec.get('testerIdName', ''),
                    'status': exec.get('status', ''),
                    'assignmentDate': exec.get('assignmentDate', ''),
                    'executionDate': exec.get('executionDate', ''),
                    'lastModifiedOn': exec.get('lastModifiedOn', ''),
                    'actualTime': exec.get('actualTime', 0),
                    'estimatedTime': exec.get('estimatedTime', 0)
                })
                stats['executions_extracted'] += 1
                total_for_cycle += 1
                
                # Extract test case (deduplicate)
                if 'tcrTreeTestcase' in exec:
                    tc = exec['tcrTreeTestcase']
                    tc_id = tc.get('id')
                    if tc_id and tc_id not in dim_test_cases:
                        dim_test_cases[tc_id] = {
                            'testCaseId': tc_id,
                            'testCaseTreeId': tc.get('tcrCatalogTreeId', None),
                            'revision': tc.get('revision', 0),
                            'versionNumber': tc.get('versionNumber', 1),
                            'lastModifiedOn': tc.get('lastModifiedOn', ''),
                            'createDatetime': tc.get('createDatetime', '')
                        }
                        stats['test_cases_extracted'] += 1
            
            page += 1
            
            # Safety check - stop after 100 pages
            if page >= 100:
                print(f'    └── ⚠️ Stopped after 100 pages (10,000 records)')
                break
        else:
            error = f'Failed to get executions for cycle {cycle_id}: HTTP {r.status_code}'
            print(f'    └── ❌ {error}')
            stats['errors'].append(error)
            break
    
    if total_for_cycle > 0:
        print(f'    └── {total_for_cycle} execution(s)')

print(f'  ✅ Extracted {stats["executions_extracted"]} executions')
print(f'  ✅ Extracted {stats["test_cases_extracted"]} unique test cases')

print()
print('='*80)
print('Phase 5: Saving to CSV files...')
print('='*80)

# Save dimProject
csv_file = output_dir / 'dimProject.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    if dim_projects:
        writer = csv.DictWriter(f, fieldnames=dim_projects[0].keys())
        writer.writeheader()
        writer.writerows(dim_projects)
print(f'  ✅ dimProject.csv ({len(dim_projects)} rows)')

# Save dimRelease
csv_file = output_dir / 'dimRelease.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    if dim_releases:
        writer = csv.DictWriter(f, fieldnames=dim_releases[0].keys())
        writer.writeheader()
        writer.writerows(dim_releases)
print(f'  ✅ dimRelease.csv ({len(dim_releases)} rows)')

# Save dimCycle
csv_file = output_dir / 'dimCycle.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    if dim_cycles:
        writer = csv.DictWriter(f, fieldnames=dim_cycles[0].keys())
        writer.writeheader()
        writer.writerows(dim_cycles)
print(f'  ✅ dimCycle.csv ({len(dim_cycles)} rows)')

# Save dimTestCase
csv_file = output_dir / 'dimTestCase.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    test_cases_list = list(dim_test_cases.values())
    if test_cases_list:
        writer = csv.DictWriter(f, fieldnames=test_cases_list[0].keys())
        writer.writeheader()
        writer.writerows(test_cases_list)
print(f'  ✅ dimTestCase.csv ({len(test_cases_list)} rows)')

# Save factTestExecution
csv_file = output_dir / 'factTestExecution.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    if fact_executions:
        writer = csv.DictWriter(f, fieldnames=fact_executions[0].keys())
        writer.writeheader()
        writer.writerows(fact_executions)
print(f'  ✅ factTestExecution.csv ({len(fact_executions)} rows)')

# Save extraction metadata
metadata = {
    'extraction_date': datetime.now().isoformat(),
    'base_url': full_base,
    'statistics': stats,
    'files': {
        'dimProject': len(dim_projects),
        'dimRelease': len(dim_releases),
        'dimCycle': len(dim_cycles),
        'dimTestCase': len(dim_test_cases),
        'factTestExecution': len(fact_executions)
    }
}

json_file = output_dir / 'extraction_metadata.json'
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2)
print(f'  ✅ extraction_metadata.json')

print()
print('='*80)
print('EXTRACTION COMPLETE')
print('='*80)
print(f'Finished: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()
print('Summary:')
print(f'  Projects:   {stats["projects_extracted"]:>6} rows')
print(f'  Releases:   {stats["releases_extracted"]:>6} rows')
print(f'  Cycles:     {stats["cycles_extracted"]:>6} rows')
print(f'  Test Cases: {stats["test_cases_extracted"]:>6} rows')
print(f'  Executions: {stats["executions_extracted"]:>6} rows')
print()
print(f'  API Calls:  {stats["api_calls"]:>6}')
print(f'  Errors:     {len(stats["errors"]):>6}')
print()
print(f'Output directory: {output_dir}')
print()

if stats['errors']:
    print('⚠️ Errors encountered:')
    for error in stats['errors'][:10]:  # Show first 10
        print(f'  - {error}')
    if len(stats['errors']) > 10:
        print(f'  ... and {len(stats["errors"]) - 10} more')
else:
    print('✅ No errors - extraction successful!')

