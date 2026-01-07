"""
Phase 3: Probe - Auto-generate schemas using genson

This script creates ONE sample of each working entity and uses genson
to auto-generate JSON schemas from the API responses.

Output: intelligence/schemas/*.json
"""

import json
import httpx
import yaml
from pathlib import Path
from genson import SchemaBuilder
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# Configuration
BASE_URL = "https://velonetic.yourzephyr.com/flex/services/rest/latest"
PROJECT_ID = 45

# Load API token from variables.json
def load_api_token() -> str:
    """Load API token from zephyrVariables.VariableLibrary."""
    var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
    if var_lib_path.exists():
        with open(var_lib_path, "r") as f:
            data = json.load(f)
            for var in data.get("variables", []):
                if var.get("name") == "API_TOKEN":
                    return var.get("value")
    return None

API_TOKEN = load_api_token()

def get_headers() -> dict:
    """Get HTTP headers with authentication."""
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

async def probe_release(client: httpx.AsyncClient) -> dict:
    """Probe release entity and generate schema."""
    print("🔬 Probing: release...")
    
    # Create sample release
    payload = {
        "projectId": PROJECT_ID,
        "name": f"API Intelligence Probe - Release {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "description": "Auto-generated for schema discovery",
        "startDate": datetime.now().strftime("%Y-%m-%d"),
        "globalRelease": True,
        "projectRelease": False
    }
    
    response = await client.post(f"{BASE_URL}/release", json=payload, headers=get_headers())
    
    if response.status_code not in [200, 201]:
        print(f"  ❌ Failed: HTTP {response.status_code}")
        print(f"  Response: {response.text}")
        return None
    
    data = response.json()
    print(f"  ✅ Created release ID: {data.get('id')}")
    
    # Generate schema with genson
    builder = SchemaBuilder()
    builder.add_object(data)
    schema = builder.to_schema()
    
    return {
        "entity": "release",
        "sample_data": data,
        "schema": schema,
        "endpoint": "/release",
        "method": "POST",
        "status": "✅ Working",
        "notes": "BLOCKER-003: Locks for >60s after creation"
    }

async def probe_requirement_folder(client: httpx.AsyncClient) -> dict:
    """Probe requirement_folder entity and generate schema."""
    print("🔬 Probing: requirement_folder...")
    
    # Create sample folder
    payload = {
        "projectId": PROJECT_ID,
        "name": f"API Intelligence Probe - Req Folder {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "description": "Auto-generated for schema discovery"
    }
    
    response = await client.post(f"{BASE_URL}/requirementtree/add", json=payload, headers=get_headers())
    
    if response.status_code not in [200, 201]:
        print(f"  ❌ Failed: HTTP {response.status_code}")
        print(f"  Response: {response.text}")
        return None
    
    data = response.json()
    print(f"  ✅ Created folder ID: {data.get('id')}")
    
    # Generate schema with genson
    builder = SchemaBuilder()
    builder.add_object(data)
    schema = builder.to_schema()
    
    return {
        "entity": "requirement_folder",
        "sample_data": data,
        "schema": schema,
        "endpoint": "/requirementtree/add",
        "method": "POST",
        "status": "✅ Working",
        "notes": "Works perfectly"
    }

async def probe_requirement(client: httpx.AsyncClient, folder_id: int) -> dict:
    """Probe requirement entity and generate schema."""
    print("🔬 Probing: requirement...")
    
    # Create sample requirement (using workaround)
    payload = {
        "projectId": PROJECT_ID,
        "name": f"API Intelligence Probe - Requirement {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "description": "Auto-generated for schema discovery",
        "parentId": folder_id
    }
    
    response = await client.post(f"{BASE_URL}/requirementtree/add", json=payload, headers=get_headers())
    
    if response.status_code not in [200, 201]:
        print(f"  ❌ Failed: HTTP {response.status_code}")
        print(f"  Response: {response.text}")
        return None
    
    data = response.json()
    print(f"  ✅ Created requirement ID: {data.get('id')}")
    
    # Generate schema with genson
    builder = SchemaBuilder()
    builder.add_object(data)
    schema = builder.to_schema()
    
    return {
        "entity": "requirement",
        "sample_data": data,
        "schema": schema,
        "endpoint": "/requirementtree/add",
        "method": "POST",
        "status": "✅ Working (workaround)",
        "notes": "BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId."
    }

async def probe_cycle(client: httpx.AsyncClient, release_id: int) -> dict:
    """Probe cycle entity and generate schema."""
    print("🔬 Probing: cycle...")
    
    # Create sample cycle (using existing release to avoid lock)
    payload = {
        "projectId": PROJECT_ID,
        "releaseId": release_id,
        "name": f"API Intelligence Probe - Cycle {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "description": "Auto-generated for schema discovery",
        "environment": "Production",
        "build": "1.0.0",
        "revision": 1,
        "status": 0,
        "startDate": int(datetime.now().timestamp() * 1000),
        "endDate": int((datetime.now().timestamp() + 86400 * 30) * 1000)  # 30 days from now
    }
    
    response = await client.post(f"{BASE_URL}/cycle", json=payload, headers=get_headers())
    
    if response.status_code not in [200, 201]:
        print(f"  ❌ Failed: HTTP {response.status_code}")
        print(f"  Response: {response.text}")
        return None
    
    data = response.json()
    print(f"  ✅ Created cycle ID: {data.get('id')}")
    
    # Generate schema with genson
    builder = SchemaBuilder()
    builder.add_object(data)
    schema = builder.to_schema()
    
    return {
        "entity": "cycle",
        "sample_data": data,
        "schema": schema,
        "endpoint": "/cycle",
        "method": "POST",
        "status": "✅ Working",
        "notes": "Requires unlocked release. Use existing releases."
    }

async def probe_testcase_folder(client: httpx.AsyncClient) -> dict:
    """Attempt to probe testcase_folder (expected to fail)."""
    print("🔬 Probing: testcase_folder...")
    
    # Attempt to create folder (expected to fail)
    payload = {
        "projectId": PROJECT_ID,
        "name": f"API Intelligence Probe - TC Folder {datetime.now().strftime('%Y%m%d%H%M%S')}",
        "description": "Auto-generated for schema discovery"
    }
    
    response = await client.post(f"{BASE_URL}/testcasetree", json=payload, headers=get_headers())
    
    if response.status_code not in [200, 201]:
        print(f"  ❌ Failed: HTTP {response.status_code}")
        print(f"  Response: {response.text}")
        return {
            "entity": "testcase_folder",
            "sample_data": None,
            "schema": None,
            "endpoint": "/testcasetree",
            "method": "POST",
            "status": "❌ Broken",
            "notes": "BLOCKER-002: API rejects valid payloads (HTTP 400)",
            "error": response.text
        }
    
    data = response.json()
    print(f"  ✅ Created folder ID: {data.get('id')}")
    
    # Generate schema with genson
    builder = SchemaBuilder()
    builder.add_object(data)
    schema = builder.to_schema()
    
    return {
        "entity": "testcase_folder",
        "sample_data": data,
        "schema": schema,
        "endpoint": "/testcasetree",
        "method": "POST",
        "status": "✅ Working",
        "notes": "Unexpectedly working!"
    }

async def get_existing_release(client: httpx.AsyncClient) -> int:
    """Get an existing unlocked release."""
    print("🔍 Finding existing unlocked release...")
    
    response = await client.get(f"{BASE_URL}/release?projectId={PROJECT_ID}", headers=get_headers())
    
    if response.status_code == 200:
        releases = response.json()
        if releases:
            # Use the oldest release (most likely unlocked)
            oldest = min(releases, key=lambda r: r.get('id', 0))
            release_id = oldest.get('id')
            print(f"  ✅ Using existing release ID: {release_id}")
            return release_id
    
    print("  ⚠️ No existing releases found. Will create new one.")
    return None

async def main():
    """Run schema probing for all entities."""
    
    print("🔬 Phase 3: Probe - Auto-generating schemas with genson...")
    print()
    
    if not API_TOKEN:
        print("❌ Error: ZEPHYR_API_TOKEN not found in environment")
        return
    
    results = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Get existing release for cycle creation
        existing_release_id = await get_existing_release(client)
        print()
        
        # Probe release
        release_result = await probe_release(client)
        if release_result:
            results.append(release_result)
        print()
        
        # Probe requirement folder
        folder_result = await probe_requirement_folder(client)
        if folder_result:
            results.append(folder_result)
            folder_id = folder_result['sample_data'].get('id')
            print()
            
            # Probe requirement (depends on folder)
            requirement_result = await probe_requirement(client, folder_id)
            if requirement_result:
                results.append(requirement_result)
            print()
        
        # Probe cycle (using existing release)
        if existing_release_id:
            cycle_result = await probe_cycle(client, existing_release_id)
            if cycle_result:
                results.append(cycle_result)
            print()
        
        # Attempt testcase folder (expected to fail)
        testcase_folder_result = await probe_testcase_folder(client)
        if testcase_folder_result:
            results.append(testcase_folder_result)
        print()
    
    # Save schemas
    output_dir = Path(__file__).parent.parent / "intelligence" / "schemas"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for result in results:
        entity = result['entity']
        schema_file = output_dir / f"{entity}.json"
        
        with open(schema_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        
        print(f"💾 Saved: {schema_file}")
    
    print()
    print(f"✅ Phase 3 complete!")
    print()
    print(f"📊 Results:")
    print(f"  • Total entities probed: {len(results)}")
    print(f"  • Working: {len([r for r in results if '✅' in r['status']])}")
    print(f"  • Broken: {len([r for r in results if '❌' in r['status']])}")
    print()
    print("✅ Phase 3 complete! Ready for Phase 4: Relate")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

