"""Update prepareZephyr to use ZephyrIntelligence from SDK instead of loading files."""

from pathlib import Path

prepare_file = Path(__file__).parent.parent / "prepareZephyr.Notebook" / "notebook_content.py"

# Read current content
with open(prepare_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the intelligence loading section
old_section_start = '# == 4. EXECUTE (Load Intelligence) ================================= SPECTRA'
old_section_end = 'session.add_capability("intelligenceLoaded",'

# Find positions
start_pos = content.find(old_section_start)
end_pos = content.find(old_section_end)

if start_pos == -1 or end_pos == -1:
    print("❌ Could not find intelligence loading section")
    exit(1)

# Find the end of the add_capability line
end_pos = content.find('\n', end_pos + len(old_section_end))
while content[end_pos:end_pos+20].strip().endswith(')'):
    end_pos = content.find('\n', end_pos + 1)

# New simplified section
new_section = '''# == 4. EXECUTE (Load Intelligence) ================================= SPECTRA

log.info("=" * 80)
log.info("Loading API Intelligence from SDK...")
log.info("=" * 80)

from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, BooleanType,
    ArrayType, MapType
)

# Load intelligence from ZephyrIntelligence (embedded in SDK)
log.info("Loading from ZephyrIntelligence class...")

# Load schemas
schema_data = []
for entity_name, entity_schema in ZephyrIntelligence.SCHEMAS.items():
    if entity_schema.get("schema") and entity_schema["schema"].get("properties"):
        for field_name, field_spec in entity_schema["schema"]["properties"].items():
            schema_data.append({
                "entity": entity_name,
                "fieldName": field_name,
                "fieldType": field_spec.get("type", "string"),
                "isRequired": field_name in entity_schema["schema"].get("required", []),
                "description": entity_schema.get("notes", f"{entity_name}.{field_name}"),
                "sourceEndpoint": entity_schema.get("endpoint", ""),
                "intelligenceStatus": entity_schema.get("status", "unknown")
            })

log.info(f"  Loaded {len(schema_data)} fields from {len(ZephyrIntelligence.SCHEMAS)} entities")

# Load dependencies
dependencies_data = []
for entity, deps_info in ZephyrIntelligence.DEPENDENCIES.items():
    depends_on = deps_info.get("depends_on", [])
    required_by = deps_info.get("required_by", [])
    
    dependencies_data.append({
        "entity": entity,
        "dependsOn": depends_on,
        "requiredBy": required_by,
        "dependencyCount": len(depends_on),
        "dependentCount": len(required_by),
        "isIndependent": len(depends_on) == 0,
        "isLeaf": len(required_by) == 0
    })

log.info(f"  Loaded {len(dependencies_data)} entity dependencies")

# Load constraints
constraints_data = []
constraints = ZephyrIntelligence.get_all_constraints()

# Extract blockers
for blocker in constraints.get("blockers", []):
    constraints_data.append({
        "constraintId": blocker.get("id", "unknown"),
        "constraintType": "blocker",
        "entity": blocker.get("entity", "unknown"),
        "endpoint": blocker.get("endpoint", ""),
        "severity": blocker.get("severity", "unknown"),
        "issue": blocker.get("issue", ""),
        "impact": blocker.get("impact", ""),
        "workaround": str(blocker.get("workaround", {})),
        "workaroundStatus": blocker.get("workaround", {}).get("status", "unknown")
    })

# Extract bugs
for bug in constraints.get("bugs", []):
    constraints_data.append({
        "constraintId": bug.get("id", "unknown"),
        "constraintType": "bug",
        "entity": bug.get("entity", "unknown"),
        "endpoint": bug.get("endpoint", ""),
        "severity": bug.get("severity", "unknown"),
        "issue": bug.get("issue", ""),
        "impact": bug.get("impact", ""),
        "workaround": str(bug.get("workaround", {})),
        "workaroundStatus": bug.get("workaround", {}).get("status", "unknown")
    })

# Extract quirks
for quirk in constraints.get("quirks", []):
    constraints_data.append({
        "constraintId": quirk.get("id", "unknown"),
        "constraintType": "quirk",
        "entity": quirk.get("entity", "unknown"),
        "endpoint": "",
        "severity": quirk.get("severity", "low"),
        "issue": quirk.get("issue", ""),
        "impact": quirk.get("impact", ""),
        "workaround": str(quirk.get("workaround", {})),
        "workaroundStatus": quirk.get("workaround", {}).get("status", "unknown")
    })

log.info(f"  Loaded {len(constraints_data)} API constraints")

log.info("=" * 80)
log.info(f"Intelligence loaded from SDK:")
log.info(f"  - Schemas: {len(schema_data)} fields")
log.info(f"  - Dependencies: {len(dependencies_data)} entities")
log.info(f"  - Constraints: {len(constraints_data)} items")
log.info("=" * 80)

session.add_capability("intelligenceLoaded",
                      schema_fields=len(schema_data),
                      dependencies=len(dependencies_data),
                      constraints=len(constraints_data))'''

# Replace
new_content = content[:start_pos] + new_section + content[end_pos+1:]

# Write back
with open(prepare_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Updated prepareZephyr to use ZephyrIntelligence from SDK")
print(f"📊 Removed {end_pos - start_pos} chars of file-loading code")
print(f"📊 Added {len(new_section)} chars of SDK-based code")
print("🚀 prepareZephyr now uses embedded intelligence!")






