#!/usr/bin/env python
"""
Test cycle creation using EXISTING release (no lock issues).
"""
import requests
import json
import time
from pathlib import Path
from datetime import datetime

# Get API token
spectra_root = Path(__file__).parent.parent.parent.parent
env_file = spectra_root / ".env"

api_token = None
if env_file.exists():
    with open(env_file, "r") as f:
        for line in f:
            if line.startswith("ZEPHYR_API_TOKEN=") or line.startswith("SPECTRA_ZEPHYR_API_TOKEN="):
                api_token = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

if not api_token:
    var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
    if var_lib_path.exists():
        with open(var_lib_path, "r") as f:
            var_lib = json.load(f)
            for var in var_lib.get("variables", []):
                if var.get("name") == "API_TOKEN":
                    api_token = var.get("value")
                    break

BASE_URL = "https://velonetic.yourzephyr.com/flex/services/rest/latest"
PROJECT_ID = 45

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

print("="*80)
print("TEST CYCLE CREATION WITH EXISTING RELEASE")
print("="*80)

# Use existing "The Death Star Project - Phase 1" release (ID: 131)
# This was created days ago, so definitely not locked
RELEASE_ID = 131

print(f"\nUsing existing release ID: {RELEASE_ID}")
print("(The Death Star Project - Phase 1 - created 2025-12-07)")

ts = datetime.now().strftime('%Y%m%d-%H%M%S')

cycle_payload = {
    "projectId": PROJECT_ID,
    "releaseId": RELEASE_ID,
    "name": f"Test Cycle {ts}",
    "description": "Testing with existing release (no lock)",
    "environment": "Production",
    "build": "1.0.0",
    "revision": 1,
    "status": 0,
    "startDate": int(datetime.now().timestamp() * 1000),
    "endDate": int(datetime(2025, 12, 31).timestamp() * 1000)
}

print(f"\nPayload:")
print(json.dumps(cycle_payload, indent=2))

print(f"\nPOST /cycle...")
response = requests.post(
    f"{BASE_URL}/cycle",
    headers=headers,
    json=cycle_payload,
    timeout=15
)

print(f"Status: {response.status_code}")

if 200 <= response.status_code < 300:
    data = response.json()
    cycle_id = data.get("id")
    print(f"\n✅ SUCCESS - Cycle ID: {cycle_id}")
    print(f"\nFull response:")
    print(json.dumps(data, indent=2))
else:
    print(f"\n❌ FAILED")
    print(f"Error: {response.text}")

