# Zephyr Prepare Stage - Schema Design

**Status:** 🟡 In Progress  
**Version:** 1.0.0  
**Date:** 2025-12-06  
**Objective:** Design metadata-driven schema definitions for Zephyr Prepare stage

---

## 🎯 Purpose

The Prepare stage creates **schema-only configuration tables** (`prepare._schema`, `prepare._endpoints`, `prepare._statusMap`) that drive downstream Extract, Clean, Transform, and Refine stages in a metadata-driven pipeline.

**Key Principle:** Schema definitions are **machine-readable, automation-friendly** configurations that describe:

- Field-level metadata (types, nullability, structure)
- Field mapping (raw → target)
- Dimensional model mappings (dimensionName, bridgeName)
- Data quality rules (nullable, required, defaults)

---

## 📋 Schema Table Structure

Following Jira Prepare stage pattern, adapted for Zephyr entities:

### `prepare._schema` Table

**Purpose:** Field-level metadata for all Zephyr entities

**Core Fields:**

- `group` (string): Logical grouping (core, execution, requirements, test_repository)
- `groupSortOrder` (int): Display order for groups
- `entity` (string): Entity name (project, release, cycle, testcase, execution, requirement, folder)
- `entitySortOrder` (int): Display order for entities
- `fieldId` (string): Unique field identifier (e.g., "id", "name", "projectId", "cyclePhases.item")
- `structureType` (string): **scalar** | **record** | **array** | **objectDump**
- `rawField` (array<string>): JSON path segments from source (e.g., ["cyclePhases", "item"])
- `targetField` (array<string>): Target field path (usually same as rawField, or bridge table name)
- `dataType` (array<string>): SLT types: **text** | **int64** | **float64** | **bool** | **date** | **datetime** | **json**

**Metadata Fields:**

- `isInApiIssue` (bool): Present in API response (default: true)
- `isInChangelog` (bool): Tracked in changelog (default: false)
- `isNullable` (bool): Field can be null (default: true, refine based on API docs)
- `defaultValue` (string): Default value if missing
- `description` (string): Human-readable description
- `notes` (string): Additional notes for developers
- `initialDataType` (string): Original inferred type (for provenance)

**Refine Stage Mapping:**

- `dimensionName` (string): Target dimension table (e.g., "dimProject", "dimCycle")
- `bridgeName` (string): Bridge table name for arrays (e.g., "bridgeTestcaseCycle")
- `keyField` (array<bool>): Primary/foreign key flags
- `isInFactIssue` (array<bool>): Included in fact tables

**PII & Ordering:**

- `piiLevel` (array<string>): PII classification (public, internal, confidential)
- `columnOrder` (array<int>): Display order in tables

---

## 🏗️ Entity Hierarchy & Grouping

**Group 1: Core Entities (groupSortOrder=1)**

- `project` (entitySortOrder=1): Project catalogue
- `release` (entitySortOrder=2): Release metadata
- `cycle` (entitySortOrder=3): Test cycle metadata
- `testcase` (entitySortOrder=4): Testcase definitions

**Group 2: Execution Entities (groupSortOrder=2)**

- `execution` (entitySortOrder=1): Test execution results

**Group 3: Requirements (groupSortOrder=3)**

- `requirement` (entitySortOrder=1): Requirements catalogue

**Group 4: Test Repository (groupSortOrder=4)**

- `folder` (entitySortOrder=1): Test Repository folder tree nodes

---

## 📊 Structure Type Patterns

### Scalar Fields

**Example: Release Name**

```json
{
  "fieldId": "name",
  "structureType": "scalar",
  "rawField": ["name"],
  "targetField": ["name"],
  "dataType": ["text"],
  "isNullable": false,
  "description": "Release name"
}
```

### Record Fields (Nested Objects)

**Example: Release Dates Object**

```json
{
  "fieldId": "dates",
  "structureType": "record",
  "rawField": ["dates"],
  "targetField": ["dates"],
  "dataType": ["json"],
  "isNullable": true,
  "description": "Release date information",
  "notes": "Nested object - may be flattened in Transform stage"
}
```

**Flattened Fields:**

```json
{
  "fieldId": "dates.startDate",
  "structureType": "scalar",
  "rawField": ["dates", "startDate"],
  "targetField": ["dates", "startDate"],
  "dataType": ["datetime"],
  "isNullable": true
}
```

### Array Fields

**Array of Scalars:**

```json
{
  "fieldId": "tags",
  "structureType": "array",
  "rawField": ["tags"],
  "targetField": ["tags"],
  "dataType": ["text"],
  "isNullable": true,
  "description": "Array of tag strings"
}
```

**Array of Records (Bridge Table):**

```json
{
  "fieldId": "cyclePhases",
  "structureType": "array",
  "rawField": ["cyclePhases"],
  "targetField": ["cycle_cyclePhases_bridge"],
  "dataType": ["json"],
  "isNullable": true,
  "bridgeName": "cycle_cyclePhases_bridge",
  "description": "Array of cycle phase records - bridge table: cycle_cyclePhases_bridge"
}
```

---

## 🔄 Schema Generation Workflow

### Step 1: Discover Schemas

**Tool:** `scripts/discover_schemas_via_creation.py`

- Creates sample entities in SpectraTestProject
- Captures full API response schemas
- Saves to `docs/schemas/discovered/*_created_response.json`

### Step 2: Generate Prepare Schema

**Tool:** `scripts/generate_prepare_schema.py`

- Reads discovered schema JSON files
- Analyzes structure (scalar/record/array)
- Infers data types
- Generates Prepare stage schema format
- Outputs to `docs/prepare/prepare_schema_generated.json`

### Step 3: Refine & Validate

**Manual Steps:**

1. Review generated schema
2. Set `isNullable` based on API documentation
3. Add descriptive `description` fields
4. Set `dimensionName` for dimension tables
5. Set `bridgeName` for array bridges
6. Validate against SpectraTestProject

### Step 4: Integrate into Notebook

**Tool:** `prepareZephyr.Notebook`

- Loads schema from generated JSON (or embedded constant)
- Creates `prepare._schema` Delta table
- Validates schema coherence
- Registers table in Spark metastore

---

## 🧪 Validation Rules

### Schema Coherence

1. **Array entities must have bridgeName**

   - All fields with `structureType="array"` containing records must have `bridgeName` set

2. **Dimension name consistency**

   - All fields for same entity must reference same `dimensionName` (if set)
   - Cannot have multiple different `dimensionName` values per entity

3. **Bridge name consistency**
   - All array fields creating bridge tables must have consistent `bridgeName`

### Field Completeness

1. **Required fields**

   - `fieldId`, `structureType`, `rawField`, `targetField`, `dataType` always required

2. **Nullable vs Required**
   - Primary keys (`id`) should be `isNullable: false`
   - Foreign keys should match source system requirements

---

## 📐 Dimensional Model Mapping

**Note:** Full dimensional model design in `docs/refine/DIMENSIONAL-MODEL-DESIGN.md`

**Preview Mapping:**

| Entity      | Dimension Table  | Fact Table      | Bridge Tables               |
| ----------- | ---------------- | --------------- | --------------------------- |
| project     | `dimProject`     | -               | -                           |
| release     | `dimRelease`     | -               | -                           |
| cycle       | `dimCycle`       | -               | -                           |
| testcase    | `dimTestcase`    | -               | -                           |
| execution   | -                | `factExecution` | -                           |
| requirement | `dimRequirement` | -               | `bridgeTestcaseRequirement` |

**Field Mapping:**

- Set `dimensionName` on all fields belonging to a dimension
- Set `bridgeName` on array fields that create bridge tables
- Set `isInFactIssue` on fields that belong to fact tables

---

## 🚀 Next Steps

1. ✅ Complete schema discovery for all entities
2. ✅ Create schema generation utility
3. ⏳ Generate initial schema from discovered schemas
4. ⏳ Review and refine schema definitions
5. ⏳ Integrate into `prepareZephyr` notebook
6. ⏳ Validate against SpectraTestProject

---

## 📚 References

- **Jira Pattern:** `Data/jira/2-prepare/prepareJiraConfig.Notebook/notebook_content.py`
- **Source Stage:** `Data/zephyr/sourceZephyr.Notebook/notebook_content.py`
- **Schema Discovery:** `Data/zephyr/scripts/discover_schemas_via_creation.py`
- **Zephyr Research:** `Data/zephyr/docs/ZEPHYR-RESEARCH-SUMMARY.md`
