"""
Phase 5: Sequence - Determine perfect creation order using networkx topological sort

This script uses the dependency graph to automatically determine the perfect
creation order for all Zephyr entities, including timing constraints.

Output: intelligence/creation-order.yaml
"""

import yaml
import networkx as nx
from pathlib import Path
from typing import List, Dict

def load_dependency_graph() -> nx.DiGraph:
    """Load dependency graph from Phase 4."""
    
    # Rebuild graph (same as Phase 4)
    G = nx.DiGraph()
    
    entities = [
        "project",
        "release",
        "requirement_folder",
        "requirement",
        "cycle",
        "testcase_folder",
        "testcase",
        "execution",
        "allocation"
    ]
    
    G.add_nodes_from(entities)
    
    # Add edges (dependency → dependent)
    G.add_edge("requirement_folder", "requirement")
    G.add_edge("release", "cycle")
    G.add_edge("project", "testcase_folder")
    G.add_edge("testcase_folder", "testcase")
    G.add_edge("testcase", "allocation")
    G.add_edge("testcase", "execution")
    G.add_edge("cycle", "execution")
    
    return G

def determine_creation_order(G: nx.DiGraph) -> List[str]:
    """Use topological sort to determine perfect creation order."""
    
    try:
        # Topological sort gives us the perfect order!
        order = list(nx.topological_sort(G))
        return order
    except nx.NetworkXError as e:
        print(f"❌ Error: Cannot determine order - {e}")
        print("   Graph may contain cycles!")
        return []

def add_timing_constraints() -> Dict:
    """Add timing constraints from existing discoveries."""
    
    return {
        "release": {
            "wait_after_create": 10,
            "reason": "BLOCKER-003: Release locks for >60s after creation",
            "workaround": "Use existing releases instead of creating new ones",
            "severity": "critical"
        },
        "testcase_folder": {
            "status": "broken",
            "reason": "BLOCKER-002: Folder API rejects valid payloads (HTTP 400)",
            "workaround": "Manual creation required",
            "severity": "critical"
        },
        "requirement": {
            "endpoint_override": "/requirementtree/add",
            "reason": "BLOCKER-001: POST /requirement returns HTTP 500",
            "workaround": "Use /requirementtree/add with parentId",
            "severity": "high"
        },
        "testcase": {
            "status": "blocked",
            "reason": "Depends on testcase_folder which is broken",
            "severity": "high"
        },
        "execution": {
            "status": "blocked",
            "reason": "Depends on testcase which is blocked",
            "severity": "high"
        },
        "allocation": {
            "status": "blocked",
            "reason": "Depends on testcase which is blocked",
            "severity": "high"
        }
    }

def categorize_by_status(order: List[str], constraints: Dict) -> Dict:
    """Categorize entities by their creation status."""
    
    working = []
    broken = []
    blocked = []
    manual = []
    
    for entity in order:
        constraint = constraints.get(entity, {})
        status = constraint.get("status", "working")
        
        if entity == "project":
            manual.append(entity)
        elif status == "broken":
            broken.append(entity)
        elif status == "blocked":
            blocked.append(entity)
        else:
            working.append(entity)
    
    return {
        "working": working,
        "broken": broken,
        "blocked": blocked,
        "manual": manual
    }

def main():
    """Generate creation order using topological sort."""
    
    print("🎯 Phase 5: Sequence - Determining perfect creation order with networkx...")
    print()
    
    # Load dependency graph
    G = load_dependency_graph()
    print(f"✅ Loaded dependency graph: {G.number_of_nodes()} entities, {G.number_of_edges()} dependencies")
    print()
    
    # Determine creation order using topological sort
    print("🔢 Running topological sort...")
    order = determine_creation_order(G)
    
    if not order:
        print("❌ Failed to determine creation order")
        return
    
    print(f"✅ Perfect creation order determined!")
    print()
    
    # Display order
    print("📋 Creation Order (Perfect Sequence):")
    for i, entity in enumerate(order, 1):
        print(f"  {i}. {entity}")
    print()
    
    # Add timing constraints
    constraints = add_timing_constraints()
    
    # Categorize by status
    categories = categorize_by_status(order, constraints)
    
    print("📊 Status Breakdown:")
    print(f"  • Manual: {len(categories['manual'])} entities")
    print(f"  • Working: {len(categories['working'])} entities")
    print(f"  • Broken: {len(categories['broken'])} entities")
    print(f"  • Blocked: {len(categories['blocked'])} entities")
    print()
    
    # Build output
    output_data = {
        "metadata": {
            "generated_at": "2025-12-09",
            "source": "Phase 5: Sequence",
            "method": "networkx topological sort",
            "total_entities": len(order)
        },
        "perfect_order": order,
        "constraints": constraints,
        "categories": categories,
        "implementation_notes": {
            "working_sequence": [
                "1. project (manual creation in UI)",
                "2. release (API works, but locks >60s - use existing releases)",
                "3. requirement_folder (API works perfectly)",
                "4. requirement (use workaround: /requirementtree/add with parentId)",
                "5. cycle (API works with unlocked release)"
            ],
            "blocked_sequence": [
                "6. testcase_folder (BROKEN - blocks all downstream)",
                "7. testcase (blocked by folder)",
                "8. allocation (blocked by testcase)",
                "9. execution (blocked by testcase)"
            ],
            "critical_path": "testcase_folder must be fixed to unblock testcase → execution/allocation"
        },
        "recommended_approach": {
            "phase_1_working": {
                "entities": categories['working'],
                "status": "✅ Can automate now",
                "notes": "Use existing releases, requirement workaround"
            },
            "phase_2_blocked": {
                "entities": categories['broken'] + categories['blocked'],
                "status": "❌ Requires API fix or manual creation",
                "notes": "Testcase folder API must be fixed by Zephyr"
            }
        }
    }
    
    # Save creation order
    output_dir = Path(__file__).parent.parent / "intelligence"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "creation-order.yaml"
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"💾 Saved: {output_file}")
    print()
    print("✅ Phase 5 complete! Ready for Phase 6: Uncover")

if __name__ == "__main__":
    main()







