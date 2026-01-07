# Fact Table Modeling (Business Process Driven)

**Date**: 2025-12-10  
**Status**: ✅ Active Standard  
**Purpose**: Define how fact tables are named, structured, and built based on business processes

---

## Overview

Fact tables in SPECTRA are **business process driven**, not technically derived. Each fact table represents a measurable business activity or event.

---

## Business Process → Fact Table Mapping

### **Zephyr Business Processes**

| Business Process | Fact Table | Grain | Example |
|-----------------|------------|-------|---------|
| Test execution | `factExecution` | One row per testcase-cycle execution | "Test case X executed in cycle Y" |
| Cycle management | `factCycle` | One row per cycle | "Cycle Z created/updated" |
| Project management | `factProject` | One row per project | "Project A created/updated" |
| Requirement coverage | `factRequirementCoverage` | One row per requirement-cycle allocation | "Requirement R allocated to cycle C" |
| Cycle status history | `factCycleStatusHistory` | One row per status transition | "Cycle moved from In Progress → Completed" |

---

## Fact Table Naming Convention

**Pattern:** `fact{Entity}` (PascalCase)

**Rules:**
- Entity name is singular (cycle → factCycle, not factCycles)
- Entity name is capitalized (Cycle → factCycle)
- Reflects business process, not technical structure

**Examples:**
- `factExecution` (test execution business process)
- `factCycle` (cycle management business process)
- `factProject` (project management business process)
- `factRequirementCoverage` (requirement allocation business process)

---

## Schema Fields for Fact Table Modeling

### **1. `factTableName` (String)**

**Purpose:** Which fact table does this field belong to?

**Values:**
- `"factCycle"` - Field belongs to cycle fact table
- `"factExecution"` - Field belongs to execution fact table
- `""` - Field doesn't belong to any fact table (dimension/bridge only)

**Usage:**
```python
# In Clean stage: Build factCycle table
fact_fields = schema.filter(F.col("factTableName") == "factCycle")
                   .filter(F.col("isInFactIssue") == True)
                   .filter(F.col("keyField") == True)
```

### **2. `factGrain` (String)**

**Purpose:** What is the grain of this fact table?

**Values:**
- `"one row per cycle"` - Fact table grain
- `"one row per execution"` - Fact table grain
- `""` - Not a fact table field

**Usage:**
- Documents fact table grain for validation
- Ensures grain consistency (grain check)

### **3. `isInFactIssue` (ArrayType(BooleanType))**

**Purpose:** Does this field belong in a fact table?

**Values:**
- `[True]` - Field belongs in fact table
- `[False]` - Field doesn't belong in fact table

**Rules:**
- Only scalar fields can be `[True]` (arrays → dimensions/bridges)
- Only key fields can be `[True]` (id, key, name, *Id fields)

### **4. `keyField` (ArrayType(BooleanType))**

**Purpose:** Is this a key field (primary/foreign key)?

**Values:**
- `[True]` - Key field (id, key, name, *Id)
- `[False]` - Not a key field

---

## Where Modeling Logic Lives

### **Prepare Stage: Define Fact Tables**

**Responsibility:** Define which fields belong to which fact tables

**How:**
1. Schema discovery detects business processes (from entity names)
2. Assigns `factTableName` based on source entity:
   - `cycle` → `factCycle`
   - `execution` → `factExecution`
   - `project` → `factProject`
3. Sets `factGrain` based on entity:
   - `cycle` → `"one row per cycle"`
   - `execution` → `"one row per execution"`

**Output:** `prepare._schema` with fact table metadata

### **Clean Stage: Build Fact Tables**

**Responsibility:** Build fact tables from schema metadata

**How:**
1. Load schema from `prepare._schema`
2. Group fields by `factTableName`:
   ```python
   fact_tables = schema.filter(F.col("factTableName") != "")
                      .groupBy("factTableName")
                      .agg(...)
   ```
3. For each fact table:
   - Load anchor (dateTimeCreated entity)
   - Join all fields with matching `factTableName`
   - Ensure grain consistency (one row per entity)
   - Write to `Tables/clean/fact{Entity}`

**Output:** `factCycle`, `factExecution`, etc. (one row per entity)

---

## Example: Building factCycle

### **1. Prepare Stage (Schema Definition)**

```python
# Schema discovery detects "cycle" entity
schema_data.append({
    "entity": "cycleId",
    "fieldId": "id",
    "factTableName": "factCycle",  # ← Business process: cycle management
    "factGrain": "one row per cycle",  # ← Grain definition
    "isInFactIssue": [True],
    "keyField": [True],
    ...
})
```

### **2. Clean Stage (Fact Table Building)**

```python
# Load schema
schema = spark.read.format("delta").load("Tables/prepare/_schema")

# Get all fields for factCycle
fact_cycle_fields = (schema
    .filter(F.col("factTableName") == "factCycle")
    .filter(F.col("isInFactIssue") == True)
    .filter(F.col("keyField") == True)
    .filter(F.col("structureType") != "array")
)

# Load anchor (dateTimeCreated)
anchor = spark.read.format("delta").load("Tables/clean/dateTimeCreated")

# Build factCycle by joining all fact fields
fact_cycle = anchor.select("cycleId", "dateTimeCreated")

for field in fact_cycle_fields.collect():
    entity = field["entity"]
    df_entity = spark.read.format("delta").load(f"Tables/clean/{entity}")
    fact_cycle = fact_cycle.join(df_entity, on="cycleId", how="left")

# Grain check: ensure one row per cycle
assert fact_cycle.count() == fact_cycle.select("cycleId").distinct().count()

# Write fact table
fact_cycle.write.format("delta").save("Tables/clean/factCycle")
```

---

## Multiple Fact Tables

**SPECTRA supports multiple fact tables per pipeline:**

- Each business process gets its own fact table
- Fields are assigned to fact tables via `factTableName`
- Clean stage builds all fact tables in parallel

**Example (Zephyr):**
- `factCycle` - Cycle management
- `factExecution` - Test execution
- `factProject` - Project management
- `factRequirementCoverage` - Requirement allocation

---

## Business Process Detection

**How Prepare stage detects business processes:**

1. **From entity names:**
   - `cycle` → Business process: "Cycle management" → `factCycle`
   - `execution` → Business process: "Test execution" → `factExecution`
   - `project` → Business process: "Project management" → `factProject`

2. **From sample data:**
   - Analyze entity structure
   - Identify measurable events (executions, status changes)
   - Assign fact table names based on entity

3. **Manual override:**
   - Can be manually set in intelligence YAML
   - Overrides auto-detection if needed

---

## Validation

**Grain Check (Clean Stage):**
```python
def assert_grain(df, fact_table_name, grain_key):
    """Ensure fact table has correct grain."""
    total = df.count()
    distinct = df.select(grain_key).distinct().count()
    if total != distinct:
        raise ValueError(f"{fact_table_name} grain breach: {total} rows vs {distinct} distinct {grain_key}")
```

**Schema Validation (Prepare Stage):**
- All fields with `factTableName` must have `factGrain`
- All fields with `isInFactIssue=True` must have `factTableName`
- Grain must match entity (e.g., `factCycle` → `"one row per cycle"`)

---

## References

- **Jira Implementation**: `Data/jira/6-refine/refineFacts.Notebook/notebook_content.py`
- **Schema Flags**: `factTableName`, `factGrain`, `isInFactIssue`, `keyField` in `prepare._schema`
- **Business Processes**: Defined in `docs/refine/dimensional-model-design.md`

---

**Version**: 1.0  
**Last Updated**: 2025-12-10  
**Status**: ✅ Active Standard





