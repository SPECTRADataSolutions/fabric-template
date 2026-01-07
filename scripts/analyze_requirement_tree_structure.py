#!/usr/bin/env python3
"""
Analyze the actual requirement tree structure to understand what folders exist
and where requirements are located.
"""
import requests
import json
from pathlib import Path

# Get API credentials
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

if not api_token:
    print("ERROR: API token not found")
    exit(1)

base_url = "https://velonetic.yourzephyr.com"
base_path = "/flex/services/rest/latest"
full_url = f"{base_url}{base_path}"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

test_project_id = 45
requirement_ids = [6455, 6456, 6457]  # REQ-DS-001, REQ-DS-002, REQ-DS-003

print("=" * 80)
print("ANALYZING REQUIREMENT TREE STRUCTURE")
print("=" * 80)
print(f"\nProject ID: {test_project_id}")
print()

# Get requirement tree
print("1. Getting requirement tree structure...")
tree_url = f"{full_url}/requirementtree/{test_project_id}"
try:
    tree_response = requests.get(tree_url, headers=headers, timeout=10)
    if tree_response.status_code == 200:
        tree_data = tree_response.json()
        
        # Recursive function to print tree structure
        def print_tree(nodes, indent=0, prefix=""):
            if isinstance(nodes, list):
                for i, node in enumerate(nodes):
                    is_last = i == len(nodes) - 1
                    current_prefix = "└── " if is_last else "├── "
                    print_tree(node, indent, current_prefix)
            elif isinstance(nodes, dict):
                node_id = nodes.get("id")
                node_name = nodes.get("name", "Unknown")
                has_children = nodes.get("hasChild", False) or (isinstance(nodes.get("children"), list) and len(nodes.get("children", [])) > 0)
                
                print(f"{' ' * indent}{prefix}{node_name} (ID: {node_id})" + (" [HAS CHILDREN]" if has_children else ""))
                
                # Print children if they exist
                if "children" in nodes and nodes["children"]:
                    child_prefix = "│   " if prefix.startswith("├") else "    "
                    print_tree(nodes["children"], indent + 4, child_prefix)
            else:
                # Single node
                node_id = tree_data.get("id") if isinstance(tree_data, dict) else None
                node_name = tree_data.get("name", "Unknown") if isinstance(tree_data, dict) else str(tree_data)
                print(f"{prefix}{node_name} (ID: {node_id})")
        
        print("\n📁 REQUIREMENT TREE STRUCTURE:")
        print("=" * 80)
        print_tree(tree_data)
        
        # Save full tree for analysis
        output_dir = Path(__file__).parent.parent / "docs" / "schemas" / "discovered" / "requirements"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "requirement_tree_structure.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(tree_data, f, indent=2)
        print(f"\n💾 Full tree saved to: {output_file}")
        
    else:
        print(f"❌ HTTP {tree_response.status_code}: {tree_response.text[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")

# Get each requirement and show its folder location
print(f"\n2. Checking requirement folder assignments...")
print("=" * 80)

for req_id in requirement_ids:
    get_url = f"{full_url}/requirement/{req_id}"
    try:
        response = requests.get(get_url, headers=headers, timeout=10)
        if response.status_code == 200:
            req = response.json()
            req_name = req.get("name", "Unknown")
            tree_ids = req.get("requirementTreeIds", [])
            
            print(f"\n{req_name} (ID: {req_id})")
            print(f"   requirementTreeIds: {tree_ids}")
            
            # Look up folder names
            if tree_ids:
                for tree_id in tree_ids:
                    # Try to get folder info
                    folder_url = f"{full_url}/requirementtree/{tree_id}"
                    try:
                        folder_response = requests.get(folder_url, headers=headers, timeout=10)
                        if folder_response.status_code == 200:
                            folder_data = folder_response.json()
                            folder_name = folder_data.get("name", "Unknown")
                            print(f"   → Folder ID {tree_id}: '{folder_name}'")
                        else:
                            print(f"   → Folder ID {tree_id}: (Could not retrieve name)")
                    except:
                        print(f"   → Folder ID {tree_id}: (Error retrieving)")
            else:
                print(f"   ⚠️ No folder assigned (requirementTreeIds is empty)")
    except Exception as e:
        print(f"❌ Error getting requirement {req_id}: {e}")

print(f"\n" + "=" * 80)
print("ANALYSIS")
print("=" * 80)
print("\nThis shows:")
print("  1. Complete folder tree structure")
print("  2. Which folder each requirement is assigned to")
print("  3. Whether 'The Death Star Project' folder exists and where it is")

