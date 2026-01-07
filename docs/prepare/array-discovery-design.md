# Array Discovery in Prepare Stage

## Purpose
The Prepare stage should analyze actual SOURCE data to discover array element types and enhance the schema with real structure information.

## Why This Belongs in Prepare

**Prepare Stage Responsibilities:**
1. ✅ Load API intelligence (what the API claims exists)
2. ✅ **Analyze source data** (what actually exists in our data)
3. ✅ Reconcile intelligence with reality
4. ✅ Create enhanced schema for Extract stage

This mirrors Jira's approach - the schema isn't just documentation, it's **data-driven metadata**.

## Discovery Process

### Step 1: Load Source Tables
```python
df_cycles = spark.read.format("delta").load("Tables/source/cycles")
df_releases = spark.read.format("delta").load("Tables/source/releases")
# Note: requirements not extracted yet
```

### Step 2: Discover Array Element Types
```python
# Find cycles with populated cyclePhases
cycles_with_phases = df_cycles.filter(
    F.col("cyclePhases").isNotNull() &
    (F.size(F.col("cyclePhases")) > 0)
).limit(1)

if cycles_with_phases.count() > 0:
    sample = cycles_with_phases.first()
    phases = sample["cyclePhases"]
    
    if isinstance(phases[0], dict):
        # Array of objects - need to flatten or keep as JSON
        element_type = "object"
        structure_type = "array<object>"
    elif isinstance(phases[0], (int, float)):
        element_type = "integer"
        structure_type = "array<integer>"
    else:
        element_type = "string"
        structure_type = "array<string>"
```

### Step 3: Enhance Schema
```python
# Update schema_data with discovered types
for field in schema_data:
    if field["fieldName"] == "cyclePhases":
        field["structureType"] = structure_type
        field["dataType"] = [structure_type]
        field["structureNotes"] = f"Array of {element_type} (discovered from source data)"
```

### Step 4: Write Enhanced Schema
```python
# Write to prepare._schema with enhanced metadata
df_schema = spark.createDataFrame(schema_data, schema_table_schema)
session.delta.write(df_schema, "prepare._schema", "Tables/prepare/_schema", mode="overwrite")
```

## Benefits

- ✅ **Data-driven**: Schema reflects actual data, not just API documentation
- ✅ **Handles missing docs**: Discovers structure even if API docs are incomplete
- ✅ **Validates intelligence**: Confirms API intelligence matches reality
- ✅ **Guides Extract**: Extract stage knows how to handle each array
- ✅ **Jira parity**: Same approach as mature Jira pipeline

## Implementation

Add new cell to prepareZephyr after intelligence loading:
- Cell 4a: Load Intelligence from SDK
- **Cell 4b: Discover array structures from source data** (NEW)
- Cell 5: Create tables with enhanced schema






