"""
Generate Python code from complete-intelligence.yaml for embedding in spectraSDK.

This script reads the COMPLETE intelligence (enriched + overrides) and converts it
to Python dicts that can be embedded directly in the SDK notebook.

SPECTRA-grade: Evidence-based discovery + expert overrides.
"""

import json
import yaml
from pathlib import Path

def generate_intelligence_code():
    """Generate Python code for complete intelligence data."""
    
    intelligence_dir = Path(__file__).parent.parent / "intelligence"
    complete_intel_file = intelligence_dir / "complete-intelligence.yaml"
    
    if not complete_intel_file.exists():
        print(f"❌ ERROR: {complete_intel_file} not found!")
        print("   Run: python scripts/apply_manual_overrides.py first")
        return None
    
    # Load complete intelligence
    with open(complete_intel_file, 'r', encoding='utf-8') as f:
        complete = yaml.safe_load(f)
    
    output = []
    output.append("# " + "=" * 78)
    output.append("# ZEPHYR API INTELLIGENCE (COMPLETE)")
    output.append("# Auto-generated from intelligence/complete-intelligence.yaml")
    output.append("# Source: API Intelligence Framework + Manual Overrides")
    output.append("# Maturity: L6 (Jira-proven pattern)")
    output.append("# " + "=" * 78)
    output.append("")
    output.append("class ZephyrIntelligence:")
    output.append('    """Zephyr API intelligence - complete schema with dimensional modeling."""')
    output.append("")
    
    # Entities with full schema (including rawField, targetField, etc.)
    output.append("    # Complete entity schemas (fields include: entity, fieldId, structureType,")
    output.append("    # rawField, targetField, dataType, dimensionName, bridgeName, etc.)")
    output.append("    ENTITIES = {")
    
    for entity_name, entity_data in complete.get("entities", {}).items():
        output.append(f'        "{entity_name}": {{')
        output.append(f'            "endpoint": "{entity_data.get("endpoint", "")}",')
        output.append(f'            "field_count": {entity_data.get("field_count", 0)},')
        
        # Fields array
        fields_json = json.dumps(entity_data.get("fields", []), indent=16).replace(chr(10), chr(10) + " " * 12)
        # Replace JSON literals with Python literals
        fields_json = fields_json.replace(': null', ': None')
        fields_json = fields_json.replace(': true', ': True')
        fields_json = fields_json.replace(': false', ': False')
        output.append(f'            "fields": {fields_json}')
        output.append('        },')
    
    output.append("    }")
    output.append("")
    
    # Dependencies
    deps_data = complete.get("dependencies", {})
    output.append("    # Dependencies (creation order)")
    for dep_key, dep_value in deps_data.items():
        if dep_key not in ["metadata"]:
            dep_json = json.dumps(dep_value, indent=8).replace(chr(10), chr(10) + " " * 4)
            # Replace JSON literals with Python literals
            dep_json = dep_json.replace(': null', ': None')
            dep_json = dep_json.replace(': true', ': True')
            dep_json = dep_json.replace(': false', ': False')
            output.append(f"    {dep_key.upper()} = {dep_json}")
    output.append("")
    
    # Constraints
    constraints_data = complete.get("constraints", {}).get("quirks", {})
    output.append("    # Constraints (blockers, bugs, API quirks)")
    output.append("    CONSTRAINTS = {")
    for constraint_type, constraint_list in constraints_data.items():
        if constraint_type not in ["metadata"]:
            constraint_json = json.dumps(constraint_list, indent=12).replace(chr(10), chr(10) + " " * 8)
            # Replace JSON literals with Python literals
            constraint_json = constraint_json.replace(': null', ': None')
            constraint_json = constraint_json.replace(': true', ': True')
            constraint_json = constraint_json.replace(': false', ': False')
            output.append(f'        "{constraint_type}": {constraint_json},')
    output.append("    }")
    output.append("")
    
    # Helper methods
    output.append("    @classmethod")
    output.append("    def get_entity_fields(cls, entity: str):")
    output.append('        """Get all fields for an entity (with complete schema)."""')
    output.append("        return cls.ENTITIES.get(entity, {}).get('fields', [])")
    output.append("")
    
    output.append("    @classmethod")
    output.append("    def get_entity_schema(cls, entity: str):")
    output.append('        """Get complete entity schema."""')
    output.append("        return cls.ENTITIES.get(entity, {})")
    output.append("")
    
    output.append("    @classmethod")
    output.append("    def get_dependencies(cls, entity: str):")
    output.append('        """Get dependencies for an entity."""')
    output.append("        for dep in getattr(cls, 'INDEPENDENT_ENTITIES', []):")
    output.append("            if dep == entity:")
    output.append("                return {'depends_on': [], 'required_by': []}")
    output.append("        return {}")
    output.append("")
    
    output.append("    @classmethod")
    output.append("    def get_creation_order(cls):")
    output.append('        """Get entities in dependency order."""')
    creation_order = deps_data.get("creation_order", [])
    output.append(f"        return {repr(creation_order)}")
    output.append("")
    
    output.append("    @classmethod")
    output.append("    def get_all_constraints(cls):")
    output.append('        """Get all constraints (blockers, bugs, quirks)."""')
    output.append("        return cls.CONSTRAINTS")
    output.append("")
    
    output.append("    @classmethod")
    output.append("    def get_array_fields(cls, entity: str):")
    output.append('        """Get all array-type fields for an entity."""')
    output.append("        fields = cls.get_entity_fields(entity)")
    output.append('        return [f for f in fields if f.get("structureType") == "array"]')
    output.append("")
    
    output.append("    @classmethod")
    output.append("    def get_dimensional_fields(cls, entity: str):")
    output.append('        """Get fields with dimensional modeling metadata."""')
    output.append("        fields = cls.get_entity_fields(entity)")
    output.append('        return [f for f in fields if "dimensionName" in f or "bridgeName" in f]')
    
    return "\n".join(output)

if __name__ == "__main__":
    print("=" * 80)
    print("🔧 Generating Complete Intelligence Python Code")
    print("=" * 80)
    
    code = generate_intelligence_code()
    
    if code:
        output_file = Path(__file__).parent.parent / "intelligence" / "complete_intelligence.py"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"✅ Generated: {output_file}")
        print(f"📊 Lines: {len(code.splitlines())}")
        print("")
        print("=" * 80)
        print("🎯 Next Steps:")
        print("  1. Review: intelligence/complete_intelligence.py")
        print("  2. Append to SDK: python scripts/append_complete_intelligence_to_sdk.py")
        print("  3. Test in Fabric: Run prepareZephyr notebook")
        print("=" * 80)
    else:
        print("❌ Failed to generate intelligence code")
        exit(1)

