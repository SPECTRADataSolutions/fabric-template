"""
Enrich Zephyr intelligence with Jira-pattern schema fields.

Takes existing intelligence (schemas, dependencies, constraints) and adds:
- Proper rawField/targetField/dataType arrays
- Correct entity semantics (target dimension, not source)
- Flattening specifications for nested objects/arrays
- Removes redundant fieldName

SPECTRA-grade: Follows proven Jira L6 pattern.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any

# Paths
SCHEMAS_DIR = Path("intelligence/schemas")
OUTPUT_FILE = Path("intelligence/enriched-intelligence.yaml")

def infer_data_type(json_type: str) -> str:
    """Convert JSON schema type to SPECTRA data type."""
    type_map = {
        "string": "text",
        "integer": "int64",
        "number": "float64",
        "boolean": "bool",
        "array": "array<unknown>",  # Will be refined based on content
        "object": "json",  # Default for complex objects
    }
    return type_map.get(json_type, "text")

def enrich_scalar_field(entity_name: str, field_name: str, field_spec: Dict) -> Dict:
    """Enrich a scalar field following SPECTRA explicit naming convention."""
    json_type = field_spec.get("type", "string")
    data_type = infer_data_type(json_type)
    
    # EXPLICIT naming convention for clarity
    # id → cycleId, name → cycleName, etc.
    if field_name == "id":
        entity_target = f"{entity_name}Id"
    elif field_name == "name":
        entity_target = f"{entity_name}Name"
    elif "date" in field_name.lower() or "time" in field_name.lower():
        # Keep date fields as-is (already semantic)
        entity_target = field_name
    else:
        # Other fields: keep as-is (description, status, etc.)
        entity_target = field_name
    
    return {
        "fieldId": field_name,                  # RAW API field
        "entity": entity_target,                # TARGET column name
        "structureType": "scalar",
        "rawField": [field_name],               # Single element array
        "targetField": [entity_target],         # Single output
        "dataType": [data_type],                # Single type
        "isRequired": field_name in field_spec.get("required", []),
        "isNullable": not (field_name in field_spec.get("required", [])),
        "description": f"{entity_name}.{field_name}",
    }

def enrich_array_field(entity_name: str, field_name: str, field_spec: Dict, sample_data: List = None) -> Dict:
    """Enrich an array field following Jira pattern."""
    
    # Determine array element type
    items_schema = field_spec.get("items", {})
    items_type = items_schema.get("type", "unknown")
    
    if items_type == "object":
        # Array of objects - need to flatten
        properties = items_schema.get("properties", {})
        
        if not properties and sample_data:
            # Infer from sample data
            if sample_data and len(sample_data) > 0 and isinstance(sample_data[0], dict):
                properties = {k: {"type": type(v).__name__} for k, v in sample_data[0].items()}
        
        # Extract property names
        raw_fields = list(properties.keys()) if properties else []
        
        # Generate target field names using EXPLICIT naming convention
        # Example: cyclePhases[].id → cyclePhaseId (EXPLICIT - full prefix)
        field_singular = singularize(field_name)
        
        target_fields = []
        data_types = []
        for prop in raw_fields:
            # EXPLICIT naming: ALWAYS prefix with singular entity
            target_fields.append(generate_target_field_name(field_singular, prop))
            
            prop_type = properties[prop].get("type", "string")
            data_types.append(f"array<{infer_data_type(prop_type)}>")
        
        return {
            "fieldId": field_name,                  # RAW API field (plural)
            "entity": field_singular,               # TARGET dimension (SINGULAR!)
            "structureType": "array",
            "rawField": raw_fields,                 # Properties per element
            "targetField": target_fields,           # Flattened outputs
            "dataType": data_types,                 # Array types
            "isRequired": False,                    # Arrays usually optional
            "isNullable": True,
            "description": f"{entity_name}.{field_name} array",
            "dimensionName": f"dim{field_singular.capitalize()}",
            "bridgeName": f"bridge{field_singular.capitalize()}",
        }
    else:
        # Array of scalars (e.g., releaseIds: [1, 2, 3])
        field_singular = singularize(field_name)
        element_type = infer_data_type(items_type)
        
        return {
            "fieldId": field_name,                  # RAW API field
            "entity": field_singular,               # TARGET (singular)
            "structureType": "array",
            "rawField": [field_name],               # The field itself
            "targetField": [field_singular],        # Singular output
            "dataType": [f"array<{element_type}>"], # Array type
            "isRequired": False,
            "isNullable": True,
            "description": f"{entity_name}.{field_name} array of {element_type}",
        }

def enrich_object_field(entity_name: str, field_name: str, field_spec: Dict) -> Dict:
    """Enrich a nested object field following Jira pattern (record)."""
    
    properties = field_spec.get("properties", {})
    raw_fields = list(properties.keys())
    
    # Generate target field names
    target_fields = []
    data_types = []
    for prop in raw_fields:
        # Example: user.id → userId, user.name → userName
        if prop == "id":
            target_fields.append(f"{field_name}Id")
        elif prop == "name":
            target_fields.append(f"{field_name}Name")
        else:
            target_fields.append(f"{field_name}{prop.capitalize()}")
        
        prop_type = properties[prop].get("type", "string")
        data_types.append(infer_data_type(prop_type))
    
    return {
        "fieldId": field_name,                  # RAW API field
        "entity": field_name,                   # TARGET concept
        "structureType": "record",
        "rawField": raw_fields,                 # Properties to extract
        "targetField": target_fields,           # Flattened outputs
        "dataType": data_types,                 # Types
        "isRequired": False,
        "isNullable": True,
        "description": f"{entity_name}.{field_name} nested object",
        "dimensionName": f"dim{field_name.capitalize()}",
    }

def singularize(word: str) -> str:
    """Simple singularization following Jira conventions."""
    if word.endswith("ies"):
        return word[:-3] + "y"  # categories → category
    elif word.endswith("ses"):
        return word[:-2]        # phases → phase
    elif word.endswith("s"):
        return word[:-1]        # releases → release
    return word

def generate_target_field_name(singular_entity: str, property_name: str) -> str:
    """
    Generate explicit target field name following SPECTRA convention.
    
    Rule: ALWAYS prefix with singular entity for clarity (no ambiguity).
    Example: cyclePhase + name → cyclePhaseName
    """
    # Capitalize first letter of property
    prop_capitalized = property_name[0].upper() + property_name[1:] if property_name else ""
    return f"{singular_entity}{prop_capitalized}"

def enrich_entity_schema(entity_name: str, entity_schema: Dict) -> List[Dict]:
    """Enrich all fields in an entity schema."""
    
    schema = entity_schema.get("schema")
    
    # Handle broken/missing schemas (API probe failed)
    if schema is None:
        print(f"  ⚠️ Schema is null - API probe failed")
        print(f"     Status: {entity_schema.get('status', 'unknown')}")
        print(f"     Notes: {entity_schema.get('notes', 'No notes')}")
        return []  # Return empty field list
    
    properties = schema.get("properties", {})
    required_fields = schema.get("required", [])
    
    enriched_fields = []
    
    for field_name, field_spec in properties.items():
        field_type = field_spec.get("type", "string")
        
        if field_type == "array":
            enriched = enrich_array_field(entity_name, field_name, field_spec)
        elif field_type == "object":
            enriched = enrich_object_field(entity_name, field_name, field_spec)
        else:
            enriched = enrich_scalar_field(entity_name, field_name, field_spec)
        
        # Add common fields
        enriched["group"] = classify_field_group(field_name)
        enriched["sourceEndpoint"] = entity_schema.get("endpoint", "")
        enriched["apiStatus"] = entity_schema.get("status", "unknown")
        enriched["notes"] = entity_schema.get("notes", "")
        
        enriched_fields.append(enriched)
    
    return enriched_fields

def classify_field_group(field_name: str) -> str:
    """Classify field into logical group."""
    if field_name in ["id", "key", "name"]:
        return "identity"
    elif "date" in field_name.lower() or "time" in field_name.lower():
        return "timestamps"
    elif field_name in ["releaseIds", "requirements", "phases", "categories"]:
        return "relationships"
    elif field_name in ["description", "notes", "metadata"]:
        return "metadata"
    elif field_name in ["status", "state", "active", "locked"]:
        return "status"
    else:
        return "attributes"

def main():
    """Main enrichment process."""
    
    print("=" * 80)
    print("🔧 Enriching Zephyr Intelligence with Jira Pattern")
    print("=" * 80)
    
    # Load existing schemas
    enriched_intelligence = {
        "metadata": {
            "version": "2.0",
            "enriched_at": "2025-12-10",
            "pattern": "Jira L6 Proven Pattern",
            "changes": [
                "Added rawField/targetField/dataType arrays",
                "Fixed entity semantic (target dimension, not source)",
                "Removed fieldName (redundant with fieldId)",
                "Added flattening specifications",
                "Added field grouping",
            ]
        },
        "entities": {}
    }
    
    # Load each entity schema
    for schema_file in SCHEMAS_DIR.glob("*.json"):
        entity_name = schema_file.stem
        
        print(f"\n📊 Enriching {entity_name}...")
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            entity_schema = json.load(f)
        
        enriched_fields = enrich_entity_schema(entity_name, entity_schema)
        
        enriched_intelligence["entities"][entity_name] = {
            "endpoint": entity_schema.get("endpoint", ""),
            "method": entity_schema.get("method", "POST"),
            "status": entity_schema.get("status", "unknown"),
            "notes": entity_schema.get("notes", ""),
            "fields": enriched_fields,
            "field_count": len(enriched_fields),
        }
        
        print(f"  ✅ Enriched {len(enriched_fields)} fields")
        
        # Show examples
        for field in enriched_fields[:3]:
            print(f"     {field['fieldId']} → {field['entity']} ({field['structureType']})")
    
    # Load dependencies (keep as-is)
    with open("intelligence/dependencies.yaml", 'r', encoding='utf-8') as f:
        enriched_intelligence["dependencies"] = yaml.safe_load(f)
    
    # Load constraints (keep as-is)
    with open("intelligence/quirks.yaml", 'r', encoding='utf-8') as f:
        enriched_intelligence["constraints"] = yaml.safe_load(f)
    
    # Save enriched intelligence
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(enriched_intelligence, f, default_flow_style=False, allow_unicode=True)
    
    print("\n" + "=" * 80)
    print(f"✅ Enriched intelligence saved to: {OUTPUT_FILE}")
    print("=" * 80)
    
    # Summary
    total_fields = sum(e["field_count"] for e in enriched_intelligence["entities"].values())
    print(f"\n📊 Summary:")
    print(f"  Entities: {len(enriched_intelligence['entities'])}")
    print(f"  Total fields: {total_fields}")
    print(f"  Dependencies: {len(enriched_intelligence['dependencies'])}")
    print(f"  Constraints: {len(enriched_intelligence['constraints'].get('blockers', []))} blockers, "
          f"{len(enriched_intelligence['constraints'].get('bugs', []))} bugs, "
          f"{len(enriched_intelligence['constraints'].get('quirks', []))} quirks")

if __name__ == "__main__":
    main()

