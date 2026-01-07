"""
Generate Python code from intelligence artifacts for embedding in spectraSDK.

This script reads the intelligence folder and converts YAML/JSON to Python dicts
that can be embedded directly in the SDK notebook.
"""

import json
import yaml
from pathlib import Path

def generate_intelligence_code():
    """Generate Python code for intelligence data."""
    
    intelligence_dir = Path(__file__).parent.parent / "intelligence"
    
    output = []
    output.append("# " + "=" * 78)
    output.append("# ZEPHYR API INTELLIGENCE")
    output.append("# Auto-generated from intelligence/ folder")
    output.append("# Source: API Intelligence Framework (7-phase discovery)")
    output.append("# " + "=" * 78)
    output.append("")
    output.append("class ZephyrIntelligence:")
    output.append('    """Zephyr API intelligence - schemas, dependencies, constraints."""')
    output.append("")
    
    # Load schemas
    output.append("    # Schemas from intelligence/schemas/*.json")
    output.append("    SCHEMAS = {")
    
    schemas_dir = intelligence_dir / "schemas"
    for schema_file in sorted(schemas_dir.glob("*.json")):
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_data = json.load(f)
            entity_name = schema_file.stem
            output.append(f'        "{entity_name}": {{')
            output.append(f'            "entity": "{entity_name}",')
            output.append(f'            "endpoint": "{schema_data.get("endpoint", "")}",')
            output.append(f'            "method": "{schema_data.get("method", "GET")}",')
            output.append(f'            "status": {repr(schema_data.get("status", "unknown"))},')
            schema_json = json.dumps(schema_data.get("schema", {}), indent=16).replace(chr(10), chr(10) + " " * 12)
            # Replace JSON null with Python None
            schema_json = schema_json.replace(': null', ': None')
            output.append(f'            "schema": {schema_json},')
            output.append(f'            "notes": {repr(schema_data.get("notes", ""))}')
            output.append('        },')
    
    output.append("    }")
    output.append("")
    
    # Load dependencies
    with open(intelligence_dir / "dependencies.yaml", 'r', encoding='utf-8') as f:
        deps_data = yaml.safe_load(f)
    
    output.append("    # Dependencies from intelligence/dependencies.yaml")
    output.append(f"    DEPENDENCIES = {repr(deps_data['dependencies'])}")
    output.append("")
    
    # Load constraints (quirks)
    with open(intelligence_dir / "quirks.yaml", 'r', encoding='utf-8') as f:
        quirks_data = yaml.safe_load(f)
    
    output.append("    # Constraints from intelligence/quirks.yaml")
    output.append(f"    CONSTRAINTS = {repr(quirks_data['quirks'])}")
    output.append("")
    
    # Helper methods
    output.append("    @classmethod")
    output.append("    def get_schema(cls, entity: str):")
    output.append('        """Get schema for an entity."""')
    output.append("        return cls.SCHEMAS.get(entity)")
    output.append("")
    
    output.append("    @classmethod")
    output.append("    def get_dependencies(cls, entity: str):")
    output.append('        """Get dependencies for an entity."""')
    output.append("        return cls.DEPENDENCIES.get(entity, {})")
    output.append("")
    
    output.append("    @classmethod")
    output.append("    def get_creation_order(cls):")
    output.append('        """Get entities in dependency order."""')
    output.append("        # Based on topological sort from intelligence/creation-order.yaml")
    with open(intelligence_dir / "creation-order.yaml", 'r', encoding='utf-8') as f:
        order_data = yaml.safe_load(f)
    output.append(f"        return {repr(order_data['perfect_order'])}")
    output.append("")
    
    output.append("    @classmethod")
    output.append("    def get_all_constraints(cls):")
    output.append('        """Get all constraints (blockers, bugs, quirks)."""')
    output.append("        return cls.CONSTRAINTS")
    
    return "\n".join(output)

if __name__ == "__main__":
    code = generate_intelligence_code()
    
    output_file = Path(__file__).parent.parent / "intelligence" / "intelligence.py"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"✅ Generated: {output_file}")
    print(f"📊 Lines: {len(code.splitlines())}")
    print("")
    print("Next step: Copy this code into a new cell in spectraSDK.Notebook")

