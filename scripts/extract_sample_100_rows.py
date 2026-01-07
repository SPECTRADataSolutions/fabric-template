#!/usr/bin/env python3
"""
Sample dimensional dataset extraction - 100 rows max per table.
Quick extraction to demonstrate dimensional model structure.
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
output_dir = Path(__file__).parent.parent / "docs" / "api-discovery" / "sample-100-extraction"
output_dir.mkdir(parents=True, exist_ok=True)

# Collections for dimensional tables
dim_projects = []
dim_releases = []
dim_cycles = []
fact_executions = []
dim_test_cases = {}  # Dictionary to deduplicate

# Limits
MAX_PROJECTS = 100
MAX_RELEASES = 100
MAX_CYCLES = 100
MAX_EXECUTIONS = 100

print('='*80)
print('SAMPLE DIMENSIONAL DATASET EXTRACTION (100 rows max per table)')
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

print('Phase 1: Extracting dimProject (max 100)...')
r = requests.get(f'{full_base}/project/details', headers=headers)
stats['api_calls'] += 1

if r.status_code == 200:
    projects = r.json()[:MAX_PROJECTS]  # Limit to 100
    print(f'  Found {len(projects)} projects (limited to {MAX_PROJECTS})')
    
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
print('Phase 2: Extracting dimRelease (max 100)...')

for project in dim_projects:
    if stats['releases_extracted'] >= MAX_RELEASES:
        print(f'  ⚠️ Reached limit of {MAX_RELEASES} releases')
        break
    
    project_id = project['projectId']
    print(f'  Project {project_id}: {project["projectName"][:50]}', end='')
    
    r = requests.get(f'{full_base}/release/project/{project_id}', headers=headers)
    stats['api_calls'] += 1
    
    if r.status_code == 200:
        releases = r.json()
        remaining = MAX_RELEASES - stats['releases_extracted']
        releases = releases[:remaining]  # Only take what we need
        print(f' → {len(releases)} release(s)')
        
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
    elif r.status_code == 403:
        print(f' → ⚠️ Access denied')
    else:
        print(f' → ❌ HTTP {r.status_code}')
        stats['errors'].append(f'Failed to get releases for project {project_id}: HTTP {r.status_code}')

print(f'  ✅ Extracted {stats["releases_extracted"]} releases')

print()
print('Phase 3: Extracting dimCycle (max 100)...')

for release in dim_releases:
    if stats['cycles_extracted'] >= MAX_CYCLES:
        print(f'  ⚠️ Reached limit of {MAX_CYCLES} cycles')
        break
    
    release_id = release['releaseId']
    print(f'  Release {release_id}: {release["releaseName"][:50]}', end='')
    
    r = requests.get(f'{full_base}/cycle/release/{release_id}', headers=headers)
    stats['api_calls'] += 1
    
    if r.status_code == 200:
        cycles = r.json()
        remaining = MAX_CYCLES - stats['cycles_extracted']
        cycles = cycles[:remaining]  # Only take what we need
        print(f' → {len(cycles)} cycle(s)')
        
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
        print(f' → ⚠️ HTTP {r.status_code}')

print(f'  ✅ Extracted {stats["cycles_extracted"]} cycles')

print()
print('Phase 4: Extracting factTestExecution (max 100)...')

for cycle in dim_cycles:
    if stats['executions_extracted'] >= MAX_EXECUTIONS:
        print(f'  ⚠️ Reached limit of {MAX_EXECUTIONS} executions')
        break
    
    cycle_id = cycle['cycleId']
    print(f'  Cycle {cycle_id}: {cycle["cycleName"][:50]}', end='')
    
    remaining = MAX_EXECUTIONS - stats['executions_extracted']
    
    r = requests.get(f'{full_base}/execution', headers=headers, params={'cycleid': cycle_id, 'maxRecords': remaining})
    stats['api_calls'] += 1
    
    if r.status_code == 200:
        exec_data = r.json()
        exec_results = exec_data.get('results', [])[:remaining]  # Take only what we need
        print(f' → {len(exec_results)} execution(s)')
        
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
    else:
        print(f' → ❌ HTTP {r.status_code}')
        stats['errors'].append(f'Failed to get executions for cycle {cycle_id}: HTTP {r.status_code}')

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
    'extraction_type': 'sample_100_rows',
    'base_url': full_base,
    'limits': {
        'max_projects': MAX_PROJECTS,
        'max_releases': MAX_RELEASES,
        'max_cycles': MAX_CYCLES,
        'max_executions': MAX_EXECUTIONS
    },
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
print(f'  Projects:   {stats["projects_extracted"]:>6} rows (max {MAX_PROJECTS})')
print(f'  Releases:   {stats["releases_extracted"]:>6} rows (max {MAX_RELEASES})')
print(f'  Cycles:     {stats["cycles_extracted"]:>6} rows (max {MAX_CYCLES})')
print(f'  Test Cases: {stats["test_cases_extracted"]:>6} rows')
print(f'  Executions: {stats["executions_extracted"]:>6} rows (max {MAX_EXECUTIONS})')
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
    print('✅ No errors - sample extraction successful!')

print()
print('Files ready for analysis:')
print(f'  - dimProject.csv ({len(dim_projects)} rows)')
print(f'  - dimRelease.csv ({len(dim_releases)} rows)')
print(f'  - dimCycle.csv ({len(dim_cycles)} rows)')
print(f'  - dimTestCase.csv ({len(dim_test_cases)} rows)')
print(f'  - factTestExecution.csv ({len(fact_executions)} rows)')

