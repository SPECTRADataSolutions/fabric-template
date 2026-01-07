#!/usr/bin/env python3
"""
Test Fabric API endpoint to debug 404 error
"""

import os
import sys
from pathlib import Path

# Add Core/cli to path
workspace_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(workspace_root / "Core" / "cli"))

from spectra.fabric import FabricClient, FabricAPIError, FabricAuthError

def test_pipeline_endpoint():
    """Test the pipeline API endpoint with debug output."""
    try:
        fabric = FabricClient.from_env()
    except FabricAuthError as e:
        print(f"❌ Authentication error: {e}", file=sys.stderr)
        return 1
    
    workspace_id = "16490dde-33b4-446e-8120-c12b0a68ed88"
    pipeline_id = "be9d0663-d383-4fe6-a0aa-8ed4781e9e87"
    
    print(f"🔍 Testing Fabric API endpoint...")
    print(f"   Workspace ID: {workspace_id}")
    print(f"   Pipeline ID: {pipeline_id}")
    print(f"   Base URL: {fabric.base_url}")
    print()
    
    # Test 1: Try to get pipeline info (GET instead of POST)
    print("Test 1: GET pipeline info...")
    try:
        path = f"/workspaces/{workspace_id}/dataPipelines/{pipeline_id}"
        response = fabric._request("GET", path)
        print(f"✅ GET succeeded: {response.status_code}")
        data = response.json()
        print(f"   Pipeline name: {data.get('displayName', 'N/A')}")
        print(f"   Pipeline type: {data.get('type', 'N/A')}")
    except FabricAPIError as e:
        print(f"❌ GET failed: {e}")
    
    print()
    
    # Test 2: Try to trigger run
    print("Test 2: POST pipeline run...")
    try:
        path = f"/workspaces/{workspace_id}/dataPipelines/{pipeline_id}/run"
        payload = {"parameters": {"init_mode": True}}
        response = fabric._request("POST", path, json_body=payload)
        print(f"✅ POST succeeded: {response.status_code}")
        data = response.json()
        print(f"   Response: {data}")
        run_id = data.get("id") or data.get("runId")
        if run_id:
            print(f"   Run ID: {run_id}")
    except FabricAPIError as e:
        print(f"❌ POST failed: {e}")
        # Try to get more details from the response
        try:
            # Access the last response if available
            print(f"   Checking if this is a permissions issue...")
            print(f"   Service principal may need 'DataPipeline.Execute' permission")
        except:
            pass
    
    return 0

if __name__ == "__main__":
    sys.exit(test_pipeline_endpoint())

