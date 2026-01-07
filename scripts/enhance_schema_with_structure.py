"""
Enhance Zephyr schema with structure metadata (Jira-style).

Adds:
- structureType: scalar|array|record|objectDump
- rawField: array of field path segments
- targetField: array of target field names
- dataType: enhanced with array element types
"""

import json
import yaml
from pathlib import Path

def analyze_structure(field_name: str, field_spec: dict, sample_value=None) -> dict:
    """Analyze field structure and return enhanced metadata."""
    
    field_type = field_spec.get("type", "string")
    
    # Determine structure type
    if field_type == "array":
        # Check if we have sample data to infer array contents
        if sample_value is not None and len(sample_value) > 0:
            first_element = sample_value[0]
            if isinstance(first_element, dict):
                structure_type = "array"  # Array of objects
                element_type = "object"
            elif isinstance(first_element, (int, float)):
                structure_type = "array"  # Array of numbers
                element_type = "integer" if isinstance(first_element, int) else "number"
            else:
                structure_type = "array"  # Array of strings
                element_type = "string"
        else:
            # No sample data - mark as array but unknown contents
            structure_type = "array"
            element_type = "unknown"
        
        return {
            "structureType": structure_type,
            "rawField": [field_name],
            "targetField": [field_name],  # Keep array as-is for now
            "dataType": [f"array<{element_type}>"],
            "notes": f"Array field - element type: {element_type}"
        }
    
    elif field_type == "object":
        return {
            "structureType": "record",
            "rawField": [field_name],
            "targetField": [field_name],
            "dataType": ["object"],
            "notes": "Nested object - may need flattening"
        }
    
    else:
        # Scalar field
        return {
            "structureType": "scalar",
            "rawField": [field_name],
            "targetField": [field_name],
            "dataType": [map_type(field_type)],
            "notes": None
        }

def map_type(json_type: str) -> str:
    """Map JSON Schema type to SPECTRA type."""
    mapping = {
        "integer": "int64",
        "number": "float64",
        "string": "text",
        "boolean": "bool",
        "array": "array",
        "object": "json"
    }
    return mapping.get(json_type, "text")

def enhance_intelligence():
    """Enhance intelligence schemas with structure metadata."""
    
    intelligence_dir = Path(__file__).parent.parent / "intelligence"
    schemas_dir = intelligence_dir / "schemas"
    
    enhanced_schemas = {}
    
    for schema_file in sorted(schemas_dir.glob("*.json")):
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_data = json.load(f)
        
        entity_name = schema_file.stem
        sample_data = schema_data.get("sample_data", {})
        
        enhanced_fields = []
        
        if schema_data.get("schema") and schema_data["schema"].get("properties"):
            for field_name, field_spec in schema_data["schema"]["properties"].items():
                # Get sample value if available
                sample_value = sample_data.get(field_name)
                
                # Analyze structure
                structure = analyze_structure(field_name, field_spec, sample_value)
                
                # Build enhanced field metadata
                enhanced_field = {
                    "entity": entity_name,
                    "fieldName": field_name,
                    "fieldType": field_spec.get("type", "string"),
                    "isRequired": field_name in schema_data["schema"].get("required", []),
                    "description": schema_data.get("notes", f"{entity_name}.{field_name}"),
                    "sourceEndpoint": schema_data.get("endpoint", ""),
                    "intelligenceStatus": schema_data.get("status", "unknown"),
                    
                    # Enhanced metadata (Jira-style)
                    "structureType": structure["structureType"],
                    "rawField": structure["rawField"],
                    "targetField": structure["targetField"],
                    "dataType": structure["dataType"],
                    "structureNotes": structure.get("notes")
                }
                
                enhanced_fields.append(enhanced_field)
        
        enhanced_schemas[entity_name] = enhanced_fields
    
    # Save enhanced schemas
    output_file = intelligence_dir / "enhanced-schemas.yaml"
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump({
            "metadata": {
                "generated_at": "2025-12-10",
                "source": "enhance_schema_with_structure.py",
                "enhancement": "Added Jira-style structure metadata",
                "fields_added": ["structureType", "rawField", "targetField", "dataType"]
            },
            "schemas": enhanced_schemas
        }, f, default_flow_style=False, allow_unicode=True)
    
    # Print summary
    total_fields = sum(len(fields) for fields in enhanced_schemas.values())
    array_fields = sum(1 for fields in enhanced_schemas.values() 
                      for field in fields 
                      if field["structureType"] == "array")
    scalar_fields = sum(1 for fields in enhanced_schemas.values() 
                       for field in fields 
                       if field["structureType"] == "scalar")
    
    print(f"✅ Enhanced {len(enhanced_schemas)} entities")
    print(f"📊 Total fields: {total_fields}")
    print(f"   - Scalar: {scalar_fields}")
    print(f"   - Array: {array_fields}")
    print(f"📁 Saved to: {output_file}")
    
    # Print array fields for review
    print("\n🔍 Array fields found:")
    for entity_name, fields in enhanced_schemas.items():
        for field in fields:
            if field["structureType"] == "array":
                data_type = field["dataType"][0]
                print(f"   - {entity_name}.{field['fieldName']}: {data_type}")

if __name__ == "__main__":
    enhance_intelligence()






