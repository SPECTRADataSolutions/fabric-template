#!/usr/bin/env python3
"""
Extract hierarchical sample data to demonstrate dependency chain.
Shows: Projects -> Releases -> Cycles -> Executions
"""

import os
import requests
import json
from datetime import datetime

# Configuration
base_url = os.environ.get("DXC_ZEPHYR_BASE_URL", "https://velonetic.yourzephyr.com")
base_path = os.environ.get("DXC_ZEPHYR_BASE_PATH", "/flex/services/rest/latest")
api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN")

full_base = f"{base_url}{base_path}"
headers = {'Authorization': f'Bearer {api_token}'}

print('Hierarchical Dependency Extraction - Sample Data')
print('='*80)
print()

# Track all extracted data
extraction_summary = {
    'projects': 0,
    'releases': 0,
    'cycles': 0,
    'executions': 0
}

# Extract hierarchy for both active projects
for project_id in [40, 44]:
    print(f'📁 PROJECT {project_id}')
    
    # Get project details
    r_proj = requests.get(f'{full_base}/project/details', headers=headers)
    if r_proj.status_code == 200:
        projects = r_proj.json()
        project = next((p for p in projects if p['id'] == project_id), None)
        if project:
            extraction_summary['projects'] += 1
            proj_name = project.get('name', 'N/A')
            proj_desc = project.get('description', 'N/A')
            if proj_desc and len(proj_desc) > 50:
                proj_desc = proj_desc[:50] + '...'
            print(f'   Name: {proj_name}')
            print(f'   Description: {proj_desc}')
    
    # Get releases for this project
    r_rel = requests.get(f'{full_base}/release/project/{project_id}', headers=headers)
    if r_rel.status_code == 200:
        releases = r_rel.json()
        print(f'   └── 📋 {len(releases)} Releases')
        extraction_summary['releases'] += len(releases)
        
        # For first 2 releases, get cycles
        for i, release in enumerate(releases[:2]):
            rel_id = release['id']
            rel_name = release.get('name', 'Unnamed')
            print(f'       ├── Release {rel_id}: {rel_name}')
            
            # Get cycles for this release
            r_cyc = requests.get(f'{full_base}/cycle/release/{rel_id}', headers=headers)
            if r_cyc.status_code == 200:
                cycles = r_cyc.json()
                cycle_count = len(cycles)
                print(f'           └── 🔄 {cycle_count} Cycle(s)')
                extraction_summary['cycles'] += cycle_count
                
                # For first cycle, get executions
                if cycles:
                    cycle = cycles[0]
                    cyc_id = cycle['id']
                    cyc_name = cycle.get('name', 'Unnamed')
                    print(f'               ├── Cycle {cyc_id}: {cyc_name}')
                    
                    # Get executions for this cycle
                    r_exec = requests.get(f'{full_base}/execution', headers=headers, params={'cycleid': cyc_id})
                    if r_exec.status_code == 200:
                        exec_data = r_exec.json()
                        exec_results = exec_data.get('results', [])
                        exec_count = len(exec_results)
                        print(f'                   └── ✅ {exec_count} Execution(s)')
                        extraction_summary['executions'] += exec_count
                        
                        # Show first 2 execution details
                        for idx, exec in enumerate(exec_results[:2]):
                            exec_id = exec.get('id')
                            tester = exec.get('testerIdName', 'N/A')
                            status = exec.get('status', 'N/A')
                            print(f'                       - Execution {exec_id}')
                            print(f'                         Tester: {tester}')
                            print(f'                         Status: {status}')
                            
                            if 'tcrTreeTestcase' in exec:
                                tc = exec['tcrTreeTestcase']
                                tc_id = tc.get('id')
                                print(f'                         TestCase ID: {tc_id}')
                            
                            if idx == 0 and exec_count > 1:
                                print(f'                       ...')
                    else:
                        print(f'                   └── ⚠️ Could not get executions: {r_exec.status_code}')
                else:
                    print(f'           └── ⚠️ No cycles (empty release)')
            else:
                print(f'           └── ❌ Could not get cycles: {r_cyc.status_code}')
        
        if len(releases) > 2:
            print(f'       └── ... and {len(releases) - 2} more release(s)')
    else:
        print(f'   └── ❌ Could not get releases: {r_rel.status_code}')
    
    print()

print('='*80)
print('Extraction Summary:')
print(f'  - Projects: {extraction_summary["projects"]}')
print(f'  - Releases: {extraction_summary["releases"]}')
print(f'  - Cycles: {extraction_summary["cycles"]}')
print(f'  - Executions: {extraction_summary["executions"]}')
print()
print('✅ Hierarchical extraction complete!')

