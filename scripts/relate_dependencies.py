"""
Phase 4: Relate - Build dependency graph using networkx

This script builds a complete dependency graph showing which entities
depend on which other entities, using networkx for graph analysis.

Output: intelligence/dependencies.yaml + dependency-graph.png
"""

import yaml
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List

def build_dependency_graph() -> nx.DiGraph:
    """Build dependency graph from existing knowledge."""
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Add all entities as nodes
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
    
    # Add edges (dependencies)
    # Format: (dependency, dependent) - "dependent depends on dependency"
    # Arrow points FROM dependency TO dependent
    
    # Level 0: Independent (no dependencies)
    # - project (created manually in UI)
    # - release (no dependencies)
    # - requirement_folder (no dependencies)
    
    # Level 1: Single dependency
    G.add_edge("requirement_folder", "requirement")  # requirement needs folder
    G.add_edge("release", "cycle")                   # cycle needs release
    G.add_edge("project", "testcase_folder")         # folder needs project (assumed)
    
    # Level 2: Multiple dependencies
    G.add_edge("testcase_folder", "testcase")        # testcase needs folder
    G.add_edge("testcase", "allocation")             # allocation needs testcase
    
    # Level 3: Complex dependencies
    G.add_edge("testcase", "execution")              # execution needs testcase
    G.add_edge("cycle", "execution")                 # execution needs cycle
    
    return G

def analyze_graph(G: nx.DiGraph) -> Dict:
    """Analyze dependency graph and extract insights."""
    
    # Check if graph is acyclic (DAG)
    is_dag = nx.is_directed_acyclic_graph(G)
    
    # Find cycles if any
    cycles = []
    if not is_dag:
        cycles = list(nx.simple_cycles(G))
    
    # Get dependencies for each entity
    dependencies = {}
    for node in G.nodes():
        deps = list(G.predecessors(node))  # What does this node depend on? (incoming edges)
        dependents = list(G.successors(node))  # What depends on this node? (outgoing edges)
        
        dependencies[node] = {
            "depends_on": deps,
            "required_by": dependents,
            "dependency_count": len(deps),
            "dependent_count": len(dependents)
        }
    
    # Find independent entities (no dependencies)
    independent = [node for node in G.nodes() if G.in_degree(node) == 0]
    
    # Find leaf entities (nothing depends on them)
    leaves = [node for node in G.nodes() if G.out_degree(node) == 0]
    
    # Calculate levels (topological generations)
    levels = {}
    if is_dag:
        for i, generation in enumerate(nx.topological_generations(G)):
            for node in generation:
                levels[node] = i
    
    return {
        "is_dag": is_dag,
        "has_cycles": not is_dag,
        "cycles": cycles,
        "dependencies": dependencies,
        "independent_entities": independent,
        "leaf_entities": leaves,
        "levels": levels,
        "total_entities": G.number_of_nodes(),
        "total_dependencies": G.number_of_edges()
    }

def visualize_graph(G: nx.DiGraph, output_path: Path):
    """Create visual representation of dependency graph."""
    
    plt.figure(figsize=(14, 10))
    
    # Use hierarchical layout
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Color nodes by level
    node_colors = []
    for node in G.nodes():
        in_degree = G.in_degree(node)
        if in_degree == 0:
            node_colors.append('#90EE90')  # Light green for independent
        elif in_degree == 1:
            node_colors.append('#87CEEB')  # Sky blue for single dependency
        elif in_degree == 2:
            node_colors.append('#FFB6C1')  # Light pink for multiple dependencies
        else:
            node_colors.append('#FF6B6B')  # Red for complex dependencies
    
    # Draw graph
    nx.draw(G, pos, 
            with_labels=True, 
            node_color=node_colors,
            node_size=3000,
            font_size=10,
            font_weight='bold',
            arrows=True,
            arrowsize=20,
            edge_color='#666666',
            linewidths=2,
            width=2)
    
    # Add title and legend
    plt.title("Zephyr API Entity Dependency Graph", fontsize=16, fontweight='bold')
    
    # Create legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#90EE90', label='Independent (Level 0)'),
        Patch(facecolor='#87CEEB', label='Single Dependency (Level 1)'),
        Patch(facecolor='#FFB6C1', label='Multiple Dependencies (Level 2)'),
        Patch(facecolor='#FF6B6B', label='Complex Dependencies (Level 3+)')
    ]
    plt.legend(handles=legend_elements, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"📊 Graph visualization saved: {output_path}")

def main():
    """Build and analyze dependency graph."""
    
    print("🕸️ Phase 4: Relate - Building dependency graph with networkx...")
    print()
    
    # Build graph
    G = build_dependency_graph()
    print(f"✅ Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print()
    
    # Analyze graph
    analysis = analyze_graph(G)
    
    # Check for cycles
    if analysis['has_cycles']:
        print("⚠️ WARNING: Circular dependencies detected!")
        for cycle in analysis['cycles']:
            print(f"  • Cycle: {' → '.join(cycle)}")
        print()
    else:
        print("✅ Graph is a DAG (Directed Acyclic Graph) - no circular dependencies")
        print()
    
    # Display results
    print("📊 Dependency Analysis:")
    print()
    print(f"Independent Entities (Level 0):")
    for entity in analysis['independent_entities']:
        print(f"  • {entity}")
    print()
    
    print("Entity Dependencies:")
    for entity, info in sorted(analysis['dependencies'].items(), key=lambda x: x[1]['dependency_count']):
        if info['depends_on']:
            deps = ', '.join(info['depends_on'])
            print(f"  • {entity} depends on: {deps}")
    print()
    
    print("Dependency Levels:")
    for level in sorted(set(analysis['levels'].values())):
        entities_at_level = [e for e, l in analysis['levels'].items() if l == level]
        print(f"  • Level {level}: {', '.join(entities_at_level)}")
    print()
    
    # Save analysis
    output_dir = Path(__file__).parent.parent / "intelligence"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save dependencies.yaml
    output_file = output_dir / "dependencies.yaml"
    output_data = {
        "metadata": {
            "generated_at": "2025-12-09",
            "source": "Phase 4: Relate",
            "method": "networkx graph analysis",
            "is_dag": analysis['is_dag'],
            "total_entities": analysis['total_entities'],
            "total_dependencies": analysis['total_dependencies']
        },
        "dependencies": analysis['dependencies'],
        "hierarchy": {
            f"level_{level}": [e for e, l in analysis['levels'].items() if l == level]
            for level in sorted(set(analysis['levels'].values()))
        },
        "independent_entities": analysis['independent_entities'],
        "leaf_entities": analysis['leaf_entities']
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"💾 Saved: {output_file}")
    print()
    
    # Visualize graph
    graph_file = output_dir / "dependency-graph.png"
    visualize_graph(G, graph_file)
    print()
    
    print("✅ Phase 4 complete! Ready for Phase 5: Sequence")

if __name__ == "__main__":
    main()

