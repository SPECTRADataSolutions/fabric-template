"""
Discover array field contents from Project 44 (read-only).

Queries real Zephyr data to understand array structures:
- cycle.cyclePhases
- requirement.requirements
- requirement.categories
- requirement.releaseIds

NO WRITES - Pure discovery only!
"""

import os
import httpx
import json
from pathlib import Path
from dotenv import load_dotenv

# Load credentials from zephyrVariables
# BASE_URL: https://velonetic.yourzephyr.com
# BASE_PATH: /flex/services/rest/latest  
# API_TOKEN: (from variables.json)

BASE_URL = "https://velonetic.yourzephyr.com/flex/services/rest/latest"
AUTH_TOKEN = "ccef8f5b690eb973d5d8ef191a8f1d65f9b85860"
PROJECT_ID = 44  # "1.BP2 Test Management" (real project)

headers = {
    "zapiAccessKey": AUTH_TOKEN,
    "Content-Type": "application/json"
}

def discover_cycles_with_phases():
    """Find cycles with populated cyclePhases array."""
    print("\n🔍 Discovering cycle.cyclePhases...")
    
    try:
        # Step 1: Get releases for project 44
        releases_response = httpx.get(
            f"{BASE_URL}/release/project/{PROJECT_ID}",
            headers=headers,
            timeout=30.0
        )
        
        if releases_response.status_code != 200:
            print(f"  ❌ Error getting releases: {releases_response.status_code}")
            return None
        
        releases = releases_response.json()
        if not releases:
            print("  ⚠️ No releases found for project 44")
            return None
        
        print(f"  📊 Found {len(releases)} releases")
        
        # Step 2: Get cycles for first release
        for release in releases[:3]:  # Check first 3 releases
            release_id = release.get("id")
            
            cycles_response = httpx.get(
                f"{BASE_URL}/cycle/release/{release_id}",
                headers=headers,
                timeout=30.0
            )
            
            if cycles_response.status_code == 200:
                cycles = cycles_response.json()
                
                # Find cycles with non-empty cyclePhases
                for cycle in cycles[:10] if isinstance(cycles, list) else [cycles]:
                    if cycle.get("cyclePhases") and len(cycle["cyclePhases"]) > 0:
                        print(f"  ✅ Found cycle with phases: ID {cycle.get('id')}")
                        print(f"     cyclePhases: {json.dumps(cycle['cyclePhases'][:2], indent=2)[:200]}...")
                        return cycle["cyclePhases"]
        
        print("  ⚠️ No cycles with populated cyclePhases found")
        return None
            
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return None

def discover_requirements_nested():
    """Find requirements with nested requirements array."""
    print("\n🔍 Discovering requirement.requirements...")
    
    try:
        # Get requirement tree for project 44
        response = httpx.get(
            f"{BASE_URL}/requirementtree/project/{PROJECT_ID}",
            headers=headers,
            timeout=30.0
        )
        
        if response.status_code == 200:
            tree = response.json()
            
            # Recursively search for nested requirements
            def find_nested(node, depth=0):
                if isinstance(node, dict):
                    if node.get("requirements") and len(node["requirements"]) > 0:
                        print(f"  ✅ Found requirement with nested: ID {node.get('id')} (depth {depth})")
                        print(f"     requirements: {json.dumps(node['requirements'][:2], indent=2)[:300]}...")
                        return node["requirements"]
                    
                    # Recurse into children
                    for key, value in node.items():
                        if isinstance(value, (dict, list)):
                            result = find_nested(value, depth + 1)
                            if result:
                                return result
                                
                elif isinstance(node, list):
                    for item in node:
                        result = find_nested(item, depth)
                        if result:
                            return result
                
                return None
            
            result = find_nested(tree)
            if not result:
                print("  ⚠️ No requirements with nested requirements found")
            return result
            
        else:
            print(f"  ❌ Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return None

def discover_release_ids():
    """Find requirements with populated releaseIds."""
    print("\n🔍 Discovering requirement.releaseIds...")
    
    try:
        # Get requirement tree
        response = httpx.get(
            f"{BASE_URL}/requirementtree/project/{PROJECT_ID}",
            headers=headers,
            timeout=30.0
        )
        
        if response.status_code == 200:
            tree = response.json()
            
            # Search for releaseIds
            def find_release_ids(node):
                if isinstance(node, dict):
                    if node.get("releaseIds") and len(node["releaseIds"]) > 0:
                        print(f"  ✅ Found requirement with releaseIds: ID {node.get('id')}")
                        print(f"     releaseIds: {node['releaseIds']}")
                        return node["releaseIds"]
                    
                    for value in node.values():
                        if isinstance(value, (dict, list)):
                            result = find_release_ids(value)
                            if result:
                                return result
                                
                elif isinstance(node, list):
                    for item in node:
                        result = find_release_ids(item)
                        if result:
                            return result
                
                return None
            
            result = find_release_ids(tree)
            if not result:
                print("  ⚠️ No requirements with releaseIds found")
            return result
            
        else:
            print(f"  ❌ Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return None

def discover_categories():
    """Find requirements with populated categories."""
    print("\n🔍 Discovering requirement.categories...")
    
    try:
        response = httpx.get(
            f"{BASE_URL}/requirementtree/project/{PROJECT_ID}",
            headers=headers,
            timeout=30.0
        )
        
        if response.status_code == 200:
            tree = response.json()
            
            # Search for categories
            def find_categories(node):
                if isinstance(node, dict):
                    if node.get("categories") and len(node["categories"]) > 0:
                        print(f"  ✅ Found requirement with categories: ID {node.get('id')}")
                        print(f"     categories: {json.dumps(node['categories'][:2], indent=2)[:200]}...")
                        return node["categories"]
                    
                    for value in node.values():
                        if isinstance(value, (dict, list)):
                            result = find_categories(value)
                            if result:
                                return result
                                
                elif isinstance(node, list):
                    for item in node:
                        result = find_categories(item)
                        if result:
                            return result
                
                return None
            
            result = find_categories(tree)
            if not result:
                print("  ⚠️ No requirements with categories found")
            return result
            
        else:
            print(f"  ❌ Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return None

def main():
    """Run all discovery queries."""
    print("=" * 80)
    print(f"🔍 Discovering Array Contents from Project {PROJECT_ID}")
    print(f"📡 Zephyr URL: {BASE_URL}")
    print(f"🔒 Read-only mode - NO WRITES")
    print("=" * 80)
    
    # Discover all array types
    results = {
        "cyclePhases": discover_cycles_with_phases(),
        "requirements": discover_requirements_nested(),
        "releaseIds": discover_release_ids(),
        "categories": discover_categories()
    }
    
    # Save results
    output_file = Path(__file__).parent.parent / "intelligence" / "array-samples.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n" + "=" * 80)
    print(f"✅ Discovery complete!")
    print(f"📁 Results saved to: {output_file}")
    print("=" * 80)
    
    # Summary
    found = sum(1 for v in results.values() if v is not None)
    print(f"\n📊 Summary: Found {found}/4 array types with data")

if __name__ == "__main__":
    main()

