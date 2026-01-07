"""Generate Prepare stage schema definitions from discovered Zephyr entity schemas.

This utility:
1. Reads discovered schema JSON files (release_created_response.json, etc.)
2. Analyzes field structures (scalar, record, array)
3. Generates Prepare stage schema definitions (prepare._schema format)
4. Outputs schema as JSON for review before committing to notebook

Following Jira Prepare stage pattern but adapted for Zephyr entities.
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from datetime import datetime


def infer_structure_type(value: Any) -> str:
    """Infer structure type (scalar, record, array) from a Python value."""
    if isinstance(value, list):
        return "array"
    elif isinstance(value, dict):
        return "record"
    else:
        return "scalar"


def infer_data_type(value: Any) -> str:
    """Infer SLT data type from a Python value."""
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int64"
    elif isinstance(value, float):
        return "float64"
    elif isinstance(value, str):
        # Try to detect date/datetime patterns
        if value.isdigit() and len(value) == 13:  # Unix timestamp in milliseconds
            return "datetime"
        elif "/" in value and len(value) == 10:  # Date format like "12/06/2025"
            return "date"
        else:
            return "text"
    elif value is None:
        return "text"  # Default for null
    else:
        return "text"  # Default fallback


def flatten_schema(
    data: Dict[str, Any],
    entity_name: str,
    group: str = "core",
    group_sort_order: int = 1,
    entity_sort_order: int = 1,
    prefix: List[str] = None,
    field_id_prefix: str = "",
) -> List[Dict[str, Any]]:
    """Flatten a nested JSON structure into Prepare stage schema format."""
    if prefix is None:
        prefix = []

    schema_fields = []
    field_counter = 0

    for key, value in data.items():
        field_counter += 1
        current_path = prefix + [key]
        field_id = f"{field_id_prefix}{key}" if field_id_prefix else key

        structure_type = infer_structure_type(value)
        
        # Determine nullability (currently all nullable - refine after validation)
        is_nullable = True

        if structure_type == "scalar":
            data_type = infer_data_type(value)
            schema_fields.append({
                "group": group,
                "groupSortOrder": group_sort_order,
                "entity": entity_name,
                "entitySortOrder": entity_sort_order,
                "fieldId": field_id,
                "structureType": "scalar",
                "rawField": current_path,
                "targetField": current_path,
                "dataType": [data_type],
                "isInApiIssue": True,
                "isInChangelog": False,
                "isNullable": is_nullable,
                "defaultValue": None,
                "description": f"{entity_name} field: {key}",
                "notes": None,
                "initialDataType": data_type,
                "type": None,
                "columnOrder": None,
                "piiLevel": None,
                "isInFactIssue": None,
                "keyField": None,
                "dimensionName": None,
                "bridgeName": None,
            })

        elif structure_type == "record":
            # Recursively process nested objects
            nested_fields = flatten_schema(
                value,
                entity_name=entity_name,
                group=group,
                group_sort_order=group_sort_order,
                entity_sort_order=entity_sort_order,
                prefix=current_path,
                field_id_prefix=f"{field_id}.",
            )
            schema_fields.extend(nested_fields)

            # Also create a record-level field entry
            schema_fields.append({
                "group": group,
                "groupSortOrder": group_sort_order,
                "entity": entity_name,
                "entitySortOrder": entity_sort_order,
                "fieldId": field_id,
                "structureType": "record",
                "rawField": current_path,
                "targetField": current_path,
                "dataType": ["json"],  # Records stored as JSON for now
                "isInApiIssue": True,
                "isInChangelog": False,
                "isNullable": is_nullable,
                "defaultValue": None,
                "description": f"{entity_name} nested object: {key}",
                "notes": "Nested object structure",
                "initialDataType": "json",
                "type": None,
                "columnOrder": None,
                "piiLevel": None,
                "isInFactIssue": None,
                "keyField": None,
                "dimensionName": None,
                "bridgeName": None,
            })

        elif structure_type == "array":
            if len(value) > 0:
                # Analyze first element to determine array item type
                first_item = value[0]
                if isinstance(first_item, dict):
                    # Array of records - need bridge table
                    schema_fields.append({
                        "group": group,
                        "groupSortOrder": group_sort_order,
                        "entity": entity_name,
                        "entitySortOrder": entity_sort_order,
                        "fieldId": field_id,
                        "structureType": "array",
                        "rawField": current_path,
                        "targetField": [f"{entity_name}_{key}_bridge"],  # Bridge table name
                        "dataType": ["json"],  # Array items as JSON
                        "isInApiIssue": True,
                        "isInChangelog": False,
                        "isNullable": is_nullable,
                        "defaultValue": None,
                        "description": f"{entity_name} array: {key}",
                        "notes": f"Array of records - bridge table: {entity_name}_{key}_bridge",
                        "initialDataType": "json",
                        "type": None,
                        "columnOrder": None,
                        "piiLevel": None,
                        "isInFactIssue": None,
                        "keyField": None,
                        "dimensionName": None,
                        "bridgeName": f"{entity_name}_{key}_bridge",
                    })

                    # Flatten first array item for bridge table schema
                    nested_fields = flatten_schema(
                        first_item,
                        entity_name=f"{entity_name}_{key}_bridge",
                        group=group,
                        group_sort_order=group_sort_order,
                        entity_sort_order=entity_sort_order + 100,  # Bridge tables after main entity
                        prefix=[],
                        field_id_prefix="",
                    )
                    schema_fields.extend(nested_fields)
                else:
                    # Array of scalars
                    item_type = infer_data_type(first_item)
                    schema_fields.append({
                        "group": group,
                        "groupSortOrder": group_sort_order,
                        "entity": entity_name,
                        "entitySortOrder": entity_sort_order,
                        "fieldId": field_id,
                        "structureType": "array",
                        "rawField": current_path,
                        "targetField": current_path,
                        "dataType": [item_type],
                        "isInApiIssue": True,
                        "isInChangelog": False,
                        "isNullable": is_nullable,
                        "defaultValue": None,
                        "description": f"{entity_name} array: {key}",
                        "notes": f"Array of {item_type}",
                        "initialDataType": item_type,
                        "type": None,
                        "columnOrder": None,
                        "piiLevel": None,
                        "isInFactIssue": None,
                        "keyField": None,
                        "dimensionName": None,
                        "bridgeName": None,
                    })
            else:
                # Empty array - can't infer type, default to text array
                schema_fields.append({
                    "group": group,
                    "groupSortOrder": group_sort_order,
                    "entity": entity_name,
                    "entitySortOrder": entity_sort_order,
                    "fieldId": field_id,
                    "structureType": "array",
                    "rawField": current_path,
                    "targetField": current_path,
                    "dataType": ["text"],
                    "isInApiIssue": True,
                    "isInChangelog": False,
                    "isNullable": is_nullable,
                    "defaultValue": None,
                    "description": f"{entity_name} array: {key}",
                    "notes": "Empty array - type inferred as text",
                    "initialDataType": "text",
                    "type": None,
                    "columnOrder": None,
                    "piiLevel": None,
                    "isInFactIssue": None,
                    "keyField": None,
                    "dimensionName": None,
                    "bridgeName": None,
                })

    return schema_fields


def generate_prepare_schema_from_entity(
    entity_name: str,
    schema_file: Path,
    group: str = "core",
    group_sort_order: int = 1,
    entity_sort_order: int = 1,
) -> List[Dict[str, Any]]:
    """Generate Prepare stage schema from a discovered entity schema file."""
    if not schema_file.exists():
        print(f"⚠️  Schema file not found: {schema_file}")
        return []

    with open(schema_file, "r") as f:
        entity_data = json.load(f)

    # Handle wrapped responses (e.g., {"releaseDto": {...}})
    if isinstance(entity_data, dict) and len(entity_data) == 1:
        first_key = list(entity_data.keys())[0]
        if first_key.endswith("Dto") or first_key.endswith("DTO"):
            entity_data = entity_data[first_key]

    if not isinstance(entity_data, dict):
        print(f"⚠️  Invalid schema format in {schema_file}: expected dict, got {type(entity_data)}")
        return []

    schema_fields = flatten_schema(
        entity_data,
        entity_name=entity_name,
        group=group,
        group_sort_order=group_sort_order,
        entity_sort_order=entity_sort_order,
    )

    return schema_fields


def main():
    """Generate Prepare stage schema for all discovered Zephyr entities."""
    scripts_dir = Path(__file__).parent
    repo_root = scripts_dir.parent
    schemas_dir = repo_root / "docs" / "schemas" / "discovered"
    output_dir = repo_root / "docs" / "prepare"

    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("GENERATING PREPARE STAGE SCHEMA FROM DISCOVERED SCHEMAS")
    print("=" * 80)
    print()

    # Define entity mappings (entity_name, schema_file, group, group_sort, entity_sort)
    entities = [
        ("project", "project_details_response.json", "core", 1, 1),
        ("release", "release_created_response.json", "core", 1, 2),
        ("cycle", "cycle_created_response.json", "core", 1, 3),
        ("testcase", "testcase_created_response.json", "core", 1, 4),
        ("execution", "execution_created_response.json", "execution", 2, 1),
        ("requirement", "requirement_created_response.json", "requirements", 3, 1),
        ("folder", "folder_tree_node_response.json", "test_repository", 4, 1),
    ]

    all_schema_fields = []

    for entity_name, schema_filename, group, group_sort, entity_sort in entities:
        schema_file = schemas_dir / schema_filename
        
        if not schema_file.exists():
            print(f"⏭️  Skipping {entity_name} - schema file not found: {schema_filename}")
            continue

        print(f"📊 Processing {entity_name}...")
        schema_fields = generate_prepare_schema_from_entity(
            entity_name=entity_name,
            schema_file=schema_file,
            group=group,
            group_sort_order=group_sort,
            entity_sort_order=entity_sort,
        )

        if schema_fields:
            all_schema_fields.extend(schema_fields)
            print(f"   ✅ Generated {len(schema_fields)} schema fields")
        else:
            print(f"   ⚠️  No schema fields generated")

    print()
    print("=" * 80)
    print("SCHEMA GENERATION SUMMARY")
    print("=" * 80)
    print(f"Total schema fields: {len(all_schema_fields)}")
    
    # Group by entity
    entity_counts = {}
    for field in all_schema_fields:
        entity = field["entity"]
        entity_counts[entity] = entity_counts.get(entity, 0) + 1

    print(f"\nFields per entity:")
    for entity, count in sorted(entity_counts.items()):
        print(f"  - {entity}: {count} fields")

    # Save to JSON
    output_file = output_dir / "prepare_schema_generated.json"
    with open(output_file, "w") as f:
        json.dump(all_schema_fields, f, indent=2)

    print(f"\n✅ Schema saved to: {output_file}")
    print(f"\n💡 Next steps:")
    print(f"   1. Review generated schema: {output_file}")
    print(f"   2. Refine nullable/required fields based on API documentation")
    print(f"   3. Add descriptions and notes")
    print(f"   4. Set dimensionName and bridgeName for refine stage")
    print(f"   5. Integrate into prepareZephyr notebook")


if __name__ == "__main__":
    main()

