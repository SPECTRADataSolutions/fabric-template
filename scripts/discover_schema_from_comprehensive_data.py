"""Discover schema from comprehensive test data responses - reusable for any source.

Purpose:
- Analyze all captured API responses
- Compare sent vs received fields
- Infer field types, structures, validations
- Generate comprehensive schema definitions

Strategy:
1. Load all captured responses from comprehensive test data creation
2. Analyze field presence, types, structures (uses SDK helpers)
3. Compare payload vs response to infer transformations
4. Generate Prepare stage schema format

SPECTRA-Grade: Uses generic SDK helpers - works for any source system.
"""
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Try to import SDK helpers (if in notebook context)
try:
    from SchemaDiscoveryHelpers import SchemaDiscoveryHelpers
    USE_SDK = True
except ImportError:
    # Standalone script - use local implementation
    USE_SDK = False
    
    # Local implementation (mirrors SDK)
    class SchemaDiscoveryHelpers:
        @staticmethod
        def analyze_field_structure(field_name: str, field_value: Any, path: List[str] = None) -> Dict[str, Any]:
            """Local implementation for standalone scripts."""
            if path is None:
                path = [field_name]
            
            schema_def = {
                "fieldId": ".".join(path),
                "rawField": path,
                "targetField": path,
            }
            
            if field_value is None:
                schema_def["structureType"] = "scalar"
                schema_def["dataType"] = ["null"]
                schema_def["isNullable"] = True
            elif isinstance(field_value, bool):
                schema_def["structureType"] = "scalar"
                schema_def["dataType"] = ["bool"]
                schema_def["isNullable"] = False
            elif isinstance(field_value, int):
                schema_def["structureType"] = "scalar"
                schema_def["dataType"] = ["int64"]
                schema_def["isNullable"] = False
            elif isinstance(field_value, float):
                schema_def["structureType"] = "scalar"
                schema_def["dataType"] = ["float64"]
                schema_def["isNullable"] = False
            elif isinstance(field_value, str):
                schema_def["structureType"] = "scalar"
                schema_def["dataType"] = ["text"]
                schema_def["isNullable"] = False
            elif isinstance(field_value, list):
                schema_def["structureType"] = "array"
                if field_value:
                    first_item = field_value[0]
                    item_schema = SchemaDiscoveryHelpers.analyze_field_structure(
                        f"{field_name}_item", first_item, path + ["item"]
                    )
                    schema_def["dataType"] = item_schema["dataType"]
                    schema_def["itemStructureType"] = item_schema["structureType"]
                else:
                    schema_def["dataType"] = ["json"]
                    schema_def["itemStructureType"] = "unknown"
                schema_def["isNullable"] = True
            elif isinstance(field_value, dict):
                schema_def["structureType"] = "record"
                schema_def["dataType"] = ["json"]
                schema_def["isNullable"] = False
                schema_def["fields"] = []
                for nested_key, nested_value in field_value.items():
                    nested_path = path + [nested_key]
                    nested_schema = SchemaDiscoveryHelpers.analyze_field_structure(
                        nested_key, nested_value, nested_path
                    )
                    schema_def["fields"].append(nested_schema)
            else:
                schema_def["structureType"] = "unknown"
                schema_def["dataType"] = ["json"]
                schema_def["isNullable"] = True
            
            return schema_def
        
        @staticmethod
        def discover_schema_from_responses(
            responses: List[Dict[str, Any]],
            entity_type: str,
            logger=None
        ) -> List[Dict[str, Any]]:
            """Local implementation for standalone scripts."""
            from collections import defaultdict
            
            all_fields = defaultdict(list)
            
            for response in responses:
                entity_data = response
                if isinstance(response, dict):
                    for key in ["dto", "data", "result", "entity"]:
                        if key in response:
                            entity_data = response[key]
                            break
                    # Check for source-specific wrappers
                    for wrapper_key in response.keys():
                        if wrapper_key.endswith("Dto") or wrapper_key.endswith("DTO"):
                            entity_data = response[wrapper_key]
                            break
                
                if isinstance(entity_data, dict):
                    for field_name, field_value in entity_data.items():
                        all_fields[field_name].append(field_value)
            
            schema_definitions = []
            for field_name, values in all_fields.items():
                non_null_values = [v for v in values if v is not None]
                sample_value = non_null_values[0] if non_null_values else values[0]
                
                field_schema = SchemaDiscoveryHelpers.analyze_field_structure(field_name, sample_value, [field_name])
                
                has_null = any(v is None for v in values)
                field_schema["isNullable"] = has_null
                field_schema["isRequired"] = not has_null and len(non_null_values) == len(values)
                
                schema_definitions.append(field_schema)
            
            return schema_definitions

def discover_schema_from_responses(discovered_dir: Path, entity_type: str) -> List[Dict[str, Any]]:
    """Discover schema for an entity type from all captured responses - uses SDK helpers."""
    print(f"\n📊 Analyzing {entity_type} responses...")
    
    # Find all response files for this entity type
    response_files = list(discovered_dir.glob(f"*{entity_type.lower()}*response*.json"))
    error_files = list(discovered_dir.glob(f"*{entity_type.lower()}*error*.json"))
    
    if not response_files:
        print(f"   ⚠️ No response files found for {entity_type}")
        return []
    
    print(f"   📁 Found {len(response_files)} response file(s)")
    if error_files:
        print(f"   ⚠️ Found {len(error_files)} error file(s) - validation issues detected")
    
    # Load all responses
    responses = []
    for response_file in response_files:
        with open(response_file, "r") as f:
            responses.append(json.load(f))
    
    # Use SDK helper for discovery
    schema_definitions = SchemaDiscoveryHelpers.discover_schema_from_responses(
        responses=responses,
        entity_type=entity_type,
        logger=None
    )
    
    for field_schema in schema_definitions:
        print(f"   ✅ {field_schema['fieldId']}: {field_schema['structureType']} ({field_schema['dataType'][0]})")
    
    print(f"   ✅ Discovered {len(schema_definitions)} fields")
    return schema_definitions

def main(discovered_dir: Optional[Path] = None):
    """Main discovery function - reusable."""
    if discovered_dir is None:
        discovered_dir = Path(__file__).parent.parent / "docs" / "schemas" / "discovered" / "comprehensive"
    
    output_dir = discovered_dir.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("🔍 SCHEMA DISCOVERY FROM COMPREHENSIVE TEST DATA")
    print("=" * 80)
    print(f"📁 Analyzing responses from: {discovered_dir}\n")
    
    if not discovered_dir.exists():
        print(f"❌ Directory not found: {discovered_dir}")
        print(f"💡 Run build_comprehensive_test_data_reusable.py first to create test data")
        return
    
    # Schema discovery results
    discovered_schema = {}
    
    # Discover schemas for all entity types found in directory
    print("\n" + "=" * 80)
    print("1️⃣ DISCOVERING SCHEMAS")
    print("=" * 80)
    
    # Auto-detect entity types from response files
    response_files = list(discovered_dir.glob("*_response.json"))
    entity_types = set()
    for file in response_files:
        # Extract entity type from filename (e.g., "release_Release_1_response.json" -> "release")
        parts = file.stem.split("_")
        if len(parts) >= 2:
            entity_types.add(parts[0].lower())
    
    # Also check for common entity types
    common_entities = ["release", "cycle", "folder", "testcase", "execution", "requirement"]
    for entity_type in common_entities:
        entity_types.add(entity_type)
    
    for entity_type in sorted(entity_types):
        schema = discover_schema_from_responses(discovered_dir, entity_type)
        if schema:
            discovered_schema[f"{entity_type}s"] = schema

    # Save discovered schemas
    print("\n" + "=" * 80)
    print("💾 SAVING DISCOVERED SCHEMAS")
    print("=" * 80)
    
    schema_output_file = output_dir / "comprehensive_discovered_schemas.json"
    with open(schema_output_file, "w") as f:
        json.dump(discovered_schema, f, indent=2)
    
    print(f"✅ Schema definitions saved to: {schema_output_file}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 DISCOVERY SUMMARY")
    print("=" * 80)
    
    total_fields = sum(len(schema) for schema in discovered_schema.values())
    print(f"✅ Total fields discovered: {total_fields}")
    
    for entity_type, schema in discovered_schema.items():
        if schema:
            scalar_count = sum(1 for f in schema if f.get("structureType") == "scalar")
            record_count = sum(1 for f in schema if f.get("structureType") == "record")
            array_count = sum(1 for f in schema if f.get("structureType") == "array")
            print(f"   {entity_type}: {len(schema)} fields ({scalar_count} scalar, {record_count} record, {array_count} array)")
    
    print(f"\n💡 Next steps:")
    print(f"   1. Review discovered schemas in: {schema_output_file}")
    print(f"   2. Generate Prepare stage schema format")
    print(f"   3. Document validation rules from error responses")
    
    return discovered_schema


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discover schema from comprehensive test data responses")
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Input directory with captured responses (default: docs/schemas/discovered/comprehensive)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory for discovered schemas (default: docs/schemas/discovered)"
    )
    
    args = parser.parse_args()
    
    discovered_dir = Path(args.input) if args.input else None
    main(discovered_dir)

