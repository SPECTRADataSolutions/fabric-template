#!/usr/bin/env python3
"""Analyze remaining endpoint failures."""

import json
from pathlib import Path

# Load latest test results
results_file = Path(__file__).parent.parent / "docs" / "api-discovery" / "comprehensive-test-1764697101.json"

with open(results_file, 'r') as f:
    data = json.load(f)

print('FINAL ENDPOINT TEST RESULTS')
print('='*80)
print(f'Passed: {data["passed"]} ({data["passed"]/data["total_tested"]*100:.1f}%)')
print(f'Failed: {data["failed"]} ({data["failed"]/data["total_tested"]*100:.1f}%)')
print(f'Skipped: {data["skipped"]}')
print()
print('REMAINING FAILURES - DETAILED BREAKDOWN')
print('='*80)

# Categorize failures
timeouts = []
bad_requests = []
not_found = []
deprecated = []
access_denied = []
other = []

for result in data['results']:
    if not result['success'] and not result['data'].get('skipped'):
        resource = result['resource'][:70]
        error_data = result['data']
        diagnosis = error_data.get('diagnosis', '')
        status = error_data.get('status_code', '')
        
        if 'RetryError' in diagnosis or 'timeout' in diagnosis.lower():
            timeouts.append((resource, error_data.get('path', '')))
        elif 'Bad request' in diagnosis:
            bad_requests.append((resource, error_data.get('error', '')[:100]))
        elif status == 404:
            not_found.append((resource, error_data.get('path', '')))
        elif status == 410:
            deprecated.append((resource, error_data.get('error', '')[:100]))
        elif status == 403:
            access_denied.append((resource, error_data.get('path', '')))
        else:
            other.append((resource, str(status) + ' - ' + str(error_data.get('error', ''))[:50]))

print(f'\n1. TIMEOUTS/RETRIES ({len(timeouts)}):')
for ep, path in timeouts:
    print(f'   - {ep}')
    print(f'     Path: {path}')

print(f'\n2. BAD REQUESTS - Missing Parameters ({len(bad_requests)}):')
for ep, error in bad_requests:
    print(f'   - {ep}')
    print(f'     Error: {error}')

print(f'\n3. NOT FOUND 404 ({len(not_found)}):')
for ep, path in not_found:
    print(f'   - {ep}')

print(f'\n4. DEPRECATED 410 ({len(deprecated)}):')
for ep, error in deprecated:
    print(f'   - {ep}')
    print(f'     {error}')

print(f'\n5. ACCESS DENIED 403 ({len(access_denied)}):')
for ep, path in access_denied:
    print(f'   - {ep}')

print(f'\n6. OTHER ERRORS ({len(other)}):')
for ep, error in other:
    print(f'   - {ep}')
    print(f'     {error}')

print()
print('='*80)
print(f'CRITICAL: Defect endpoint with actual defectId={5409341} still times out')
print('This suggests the defect endpoint is genuinely slow/broken, not ID issue.')
print('='*80)

