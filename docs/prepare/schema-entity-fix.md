# Schema Entity Fix - SPECTRA-Grade Pattern

**Date**: 2025-12-10  
**Status**: 🔧 Critical Fix Required  
**Issue**: Schema discovery using target field names as entity instead of canonical source entity names

---

## Problem

Current schema discovery is using **target field names** (like "cycleId", "cycleName") as the `entity` field, but it should use the **canonical source entity name** (like "cycle").

**Current (WRONG):**
- `entity: "cycleId"` (target field name)
- `entity: "cycleName"` (target field name)
- `entity: "cyclePhase"` (target concept)

**Required (CORRECT):**
- `entity: "cycle"` (canonical source entity name)
- `entity: "cycle"` (same entity, different fields)
- `entity: "cycle"` (same entity, different structureType)

---

## Requirements

1. **`entity` = Canonical source entity name** (e.g., "cycle", "release", "requirement")
   - NOT a target field name
   - NOT a programmatic name or ID
   - Must be unique per row (one row per entity+structureType)

2. **`fieldId` = Raw API field name** (e.g., "id", "name", "cyclePhases")
   - Original name in Zephyr before any changes
   - May or may not need to change

3. **`description` format**: `{entity}.{field}` (e.g., "cycle.id", "cycle.name")

4. **`rawField` = Array of raw field paths** (like Jira)
   - For scalars: `["id"]`
   - For records: `["iconUrl", "id", "name"]`
   - For arrays: `["id", "name"]` (properties per element)

5. **At Prepare stage**: One row per entity (or one row per entity+structureType)
   - After flattening in Clean/Transform, we'll have multiple entities per row
   - But at Prepare, it's one row per entity

---

## Solution

**Group fields by (entity, structureType) and store in arrays:**

```python
# Group fields by (entity, structureType)
entity_fields = {}  # (entity, structureType) -> {rawField: [], targetField: [], dataType: [], ...}

for field_name, field_value in sample_cycle.items():
    structure_type = determine_structure_type(field_value)
    entity = source_entity  # "cycle", "release", "requirement"
    
    key = (entity, structure_type)
    
    if structure_type == "scalar":
        entity_fields[key]["rawField"].append(field_name)
        entity_fields[key]["targetField"].append(generate_target_name(field_name))
        entity_fields[key]["dataType"].append(infer_spectra_type(field_value))
        entity_fields[key]["fieldIds"].append(field_name)
        entity_fields[key]["descriptions"].append(f"{entity}.{field_name}")
    
    elif structure_type == "record":
        properties = list(field_value.keys())
        entity_fields[key]["rawField"].extend([f"{field_name}.{prop}" for prop in properties])
        entity_fields[key]["targetField"].extend([generate_target_name(field_name, prop) for prop in properties])
        entity_fields[key]["dataType"].extend([infer_spectra_type(field_value[prop]) for prop in properties])
        entity_fields[key]["fieldIds"].append(field_name)
        entity_fields[key]["descriptions"].append(f"{entity}.{field_name} (nested object)")
    
    elif structure_type == "array":
        # Similar logic for arrays
        ...

# Create schema rows - one per (entity, structureType)
for (entity, structure_type), fields in entity_fields.items():
    schema_data.append({
        "entity": entity,  # CANONICAL SOURCE ENTITY NAME
        "entitySortOrder": entity_sort_counter[entity],
        "fieldId": fields["fieldIds"][0],  # Primary fieldId
        "structureType": structure_type,
        "rawField": fields["rawField"],  # Array
        "targetField": fields["targetField"],  # Array
        "dataType": fields["dataType"],  # Array
        "description": "; ".join(fields["descriptions"]),
        ...
    })
```

---

## Example Output

**Before (WRONG):**
```
entity: "cycleId", fieldId: "id", rawField: ["id"], targetField: ["cycleId"]
entity: "cycleName", fieldId: "name", rawField: ["name"], targetField: ["cycleName"]
entity: "cyclePhase", fieldId: "cyclePhases", rawField: ["id", "name"], targetField: ["cyclePhaseId", "cyclePhase"]
```

**After (CORRECT):**
```
entity: "cycle", fieldId: "id", rawField: ["id", "name", "cycleStartDate", ...], targetField: ["cycleId", "cycleName", "cycleStartDate", ...], structureType: "scalar"
entity: "cycle", fieldId: "cyclePhases", rawField: ["cyclePhases.id", "cyclePhases.name"], targetField: ["cyclePhaseId", "cyclePhase"], structureType: "record"
entity: "cycle", fieldId: "requirements", rawField: ["requirements[].id", "requirements[].name"], targetField: ["requirementId", "requirement"], structureType: "array"
```

---

## Implementation

This requires a complete rewrite of the schema discovery logic in `prepareZephyr.Notebook/notebook_content.py` starting from line 220.

**Key Changes:**
1. Use `source_entity` as `entity` (not target field names)
2. Group fields by (entity, structureType)
3. Store all fields in arrays (rawField, targetField, dataType)
4. One row per entity+structureType combination
5. Ensure entity is unique per row

---

**Version**: 1.0  
**Last Updated**: 2025-12-10  
**Status**: 🔧 Critical Fix Required





