"""
Apply manual overrides to enriched intelligence.

Takes enriched-intelligence.yaml and applies manual overrides for:
- Array structures (cyclePhases, requirements, etc.)
- Singularization fixes
- Field grouping corrections

SPECTRA-grade: Evidence-based enrichment + expert overrides for unknowns.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any

# Paths
ENRICHED_FILE = Path("intelligence/enriched-intelligence.yaml")
OVERRIDES_FILE = Path("intelligence/manual-overrides.yaml")
OUTPUT_FILE = Path("intelligence/complete-intelligence.yaml")

def apply_overrides(enriched: Dict, overrides: Dict) -> Dict:
    """Apply manual overrides to enriched intelligence."""
    
    result = enriched.copy()
    override_specs = overrides.get("overrides", {})
    
    print("\n" + "=" * 80)
    print("🔧 Applying Manual Overrides")
    print("=" * 80)
    
    # Apply field overrides
    for entity_name, entity_data in result.get("entities", {}).items():
        fields = entity_data.get("fields", [])
        updated_fields = []
        
        for field in fields:
            field_id = field.get("fieldId")
            
            if field_id in override_specs:
                override = override_specs[field_id]
                print(f"\n✏️ Overriding {entity_name}.{field_id}:")
                print(f"   Reason: {override.get('reason', 'No reason given')}")
                
                # Merge override with existing field (override wins)
                updated_field = field.copy()
                updated_field.update({
                    "entity": override.get("entity"),
                    "structureType": override.get("structureType"),
                    "rawField": override.get("rawField"),
                    "targetField": override.get("targetField"),
                    "dataType": override.get("dataType"),
                    "notes": override.get("notes", field.get("notes", "")),
                })
                
                # Add dimensional modeling fields if present
                if override.get("dimensionName"):
                    updated_field["dimensionName"] = override["dimensionName"]
                if override.get("bridgeName"):
                    updated_field["bridgeName"] = override["bridgeName"]
                if override.get("confidence"):
                    updated_field["confidence"] = override["confidence"]
                
                print(f"   ✅ entity: {override.get('entity')}")
                print(f"   ✅ rawField: {override.get('rawField')}")
                print(f"   ✅ targetField: {override.get('targetField')}")
                
                updated_fields.append(updated_field)
            else:
                updated_fields.append(field)
        
        entity_data["fields"] = updated_fields
    
    # Update metadata
    result["metadata"]["overrides_applied"] = len(override_specs)
    result["metadata"]["override_source"] = str(OVERRIDES_FILE)
    
    return result

def main():
    """Main process."""
    
    print("=" * 80)
    print("📝 Applying Manual Overrides to Enriched Intelligence")
    print("=" * 80)
    
    # Load enriched intelligence
    print(f"\n📂 Loading enriched intelligence from: {ENRICHED_FILE}")
    with open(ENRICHED_FILE, 'r', encoding='utf-8') as f:
        enriched = yaml.safe_load(f)
    
    # Load overrides
    print(f"📂 Loading manual overrides from: {OVERRIDES_FILE}")
    with open(OVERRIDES_FILE, 'r', encoding='utf-8') as f:
        overrides = yaml.safe_load(f)
    
    # Apply overrides
    complete = apply_overrides(enriched, overrides)
    
    # Save complete intelligence
    print(f"\n💾 Saving complete intelligence to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(complete, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print("\n" + "=" * 80)
    print("✅ Complete Intelligence Generated!")
    print("=" * 80)
    
    # Summary
    total_entities = len(complete.get("entities", {}))
    total_fields = sum(len(e.get("fields", [])) for e in complete["entities"].values())
    overridden_count = complete["metadata"].get("overrides_applied", 0)
    
    print(f"\n📊 Summary:")
    print(f"  Total entities: {total_entities}")
    print(f"  Total fields: {total_fields}")
    print(f"  Manual overrides applied: {overridden_count}")
    print(f"  Dependencies: {len(complete.get('dependencies', {}).get('independent_entities', []))}")
    print(f"  Constraints: {len(complete.get('constraints', {}).get('quirks', {}).get('blockers', []))}")
    
    print("\n" + "=" * 80)
    print("🎯 Next Steps:")
    print("  1. Review: intelligence/complete-intelligence.yaml")
    print("  2. Regenerate: python scripts/generate_intelligence_python.py")
    print("  3. Update SDK: python scripts/append_intelligence_to_sdk.py")
    print("  4. Update prepareZephyr: Use new schema structure")
    print("=" * 80)

if __name__ == "__main__":
    main()






