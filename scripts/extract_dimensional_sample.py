#!/usr/bin/env python3
"""
Extract hierarchical sample and display as dimensional tables.
Shows how source data maps to dimensional model.
"""

import os
import requests
import csv
from io import StringIO

# Configuration
base_url = os.environ.get("DXC_ZEPHYR_BASE_URL", "https://velonetic.yourzephyr.com")
base_path = os.environ.get("DXC_ZEPHYR_BASE_PATH", "/flex/services/rest/latest")
api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN")

full_base = f"{base_url}{base_path}"
headers = {'Authorization': f'Bearer {api_token}'}

# Collections for dimensional tables
dim_projects = []
dim_releases = []
dim_cycles = []
fact_executions = []

print('Extracting Dimensional Sample Data...')
print()

# Extract for both projects
for project_id in [40, 44]:
    # Get project details
    r_proj = requests.get(f'{full_base}/project/details', headers=headers)
    if r_proj.status_code == 200:
        projects = r_proj.json()
        project = next((p for p in projects if p['id'] == project_id), None)
        if project:
            dim_projects.append({
                'projectId': project['id'],
                'projectName': project.get('name', 'N/A'),
                'projectDescription': project.get('description', 'N/A')[:100]
            })
    
    # Get releases for this project
    r_rel = requests.get(f'{full_base}/release/project/{project_id}', headers=headers)
    if r_rel.status_code == 200:
        releases = r_rel.json()
        
        # Get first 2 releases only
        for release in releases[:2]:
            rel_id = release['id']
            dim_releases.append({
                'releaseId': rel_id,
                'releaseName': release.get('name', 'N/A'),
                'projectId': project_id  # Foreign key
            })
            
            # Get cycles for this release
            r_cyc = requests.get(f'{full_base}/cycle/release/{rel_id}', headers=headers)
            if r_cyc.status_code == 200:
                cycles = r_cyc.json()
                
                # Get first cycle only
                if cycles:
                    cycle = cycles[0]
                    cyc_id = cycle['id']
                    dim_cycles.append({
                        'cycleId': cyc_id,
                        'cycleName': cycle.get('name', 'N/A'),
                        'releaseId': rel_id  # Foreign key
                    })
                    
                    # Get executions for this cycle
                    r_exec = requests.get(f'{full_base}/execution', headers=headers, params={'cycleid': cyc_id})
                    if r_exec.status_code == 200:
                        exec_data = r_exec.json()
                        exec_results = exec_data.get('results', [])
                        
                        # Get first 3 executions only
                        for exec in exec_results[:3]:
                            fact_executions.append({
                                'executionId': exec.get('id'),
                                'cycleId': cyc_id,  # Foreign key
                                'testCaseId': exec.get('tcrTreeTestcase', {}).get('id', 'N/A'),
                                'testerName': exec.get('testerIdName', 'N/A'),
                                'status': exec.get('status', 'N/A')
                            })

# Display tables
print('='*80)
print('dimProject - Dimension Table')
print('='*80)
print(f'{"projectId":<12} {"projectName":<30} {"projectDescription":<35}')
print('-'*80)
for row in dim_projects:
    print(f'{row["projectId"]:<12} {row["projectName"]:<30} {row["projectDescription"]:<35}')

print()
print('='*80)
print('dimRelease - Dimension Table')
print('='*80)
print(f'{"releaseId":<12} {"releaseName":<40} {"projectId (FK)":<15}')
print('-'*80)
for row in dim_releases:
    print(f'{row["releaseId"]:<12} {row["releaseName"]:<40} {row["projectId"]:<15}')

print()
print('='*80)
print('dimCycle - Dimension Table')
print('='*80)
print(f'{"cycleId":<12} {"cycleName":<40} {"releaseId (FK)":<15}')
print('-'*80)
for row in dim_cycles:
    print(f'{row["cycleId"]:<12} {row["cycleName"]:<40} {row["releaseId"]:<15}')

print()
print('='*80)
print('factTestExecution - Fact Table (Sample)')
print('='*80)
print(f'{"execId":<10} {"cycleId":<10} {"testCaseId":<12} {"testerName":<25} {"status":<8}')
print('-'*80)
for row in fact_executions:
    print(f'{row["executionId"]:<10} {row["cycleId"]:<10} {row["testCaseId"]:<12} {row["testerName"]:<25} {row["status"]:<8}')

print()
print('='*80)
print('Summary')
print('='*80)
print(f'dimProject rows: {len(dim_projects)}')
print(f'dimRelease rows: {len(dim_releases)}')
print(f'dimCycle rows: {len(dim_cycles)}')
print(f'factTestExecution rows: {len(fact_executions)}')
print()
print('Relationships:')
print('  dimProject (1) --> (*) dimRelease')
print('  dimRelease (1) --> (*) dimCycle')
print('  dimCycle (1) --> (*) factTestExecution')
print('  factTestExecution (*) --> (1) dimTestCase (nested)')
print()
print('✅ Dimensional sample extraction complete!')

