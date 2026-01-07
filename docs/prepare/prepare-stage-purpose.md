# Prepare Stage Purpose & Design

**Date:** 2025-12-11  
**Status:** 🎯 Design Phase  
**Purpose:** Define Prepare stage's role in the SPECTRA pipeline

---

## Core Purpose

**Prepare stage creates metadata-driven configuration tables that drive downstream stages.**

### **What Prepare Does:**

1. **Reads from Source stage:**

   - `source.endpoints` - Full API endpoint catalog (224 endpoints)
   - `Tables/source/*` - Actual data samples (if available)
   - Intelligence gained from Source stage validation

2. **Generates schema metadata:**

   - One entity per row (canonical entity name)
   - Field-level metadata extracted from actual data
   - Auto-detects new fields when data changes
   - Provides metadata for Extract, Clean, Transform, Refine stages

3. **Outputs:**
   - `prepare.schema` - Field-level metadata (one row per entity)
   - `prepare.dependencies` - Entity relationships
   - `prepare.constraints` - API limitations & workarounds

---

## Design Principles

### **1. Data-Driven Schema Generation**

**Principle:** Schema should be generated from actual data, not hardcoded intelligence.

**Approach:**

- Use `source.endpoints` to know which endpoints to call
- Use intelligence to know HOW to call them (order, dependencies, parameters)
- **Fetch sample data from API** using those endpoints
- Analyze JSON structure to infer schema
- One entity per row (e.g., "cycle", "project", "release")
- Fields grouped by entity and structure type

**Benefits:**

- Auto-detects new fields when API changes
- No manual schema updates needed
- Always matches actual data structure

---

### **2. One Entity Per Row**

**Principle:** Each row in `prepare.schema` represents one entity.

**Structure:**

```
entity | entitySortOrder | fieldId | structureType | rawField | targetField | dataType | ...
-------|-----------------|---------|---------------|----------|-------------|----------|----
cycle  | 0               | id      | scalar        | [id]     | [cycleId]   | [int64]  | ...
cycle  | 0               | name    | scalar        | [name]   | [cycleName] | [text]   | ...
cycle  | 0               | phases  | array         | [phases] | [cyclePhaseId] | [array<int64>] | ...
```

**Key Points:**

- `entity` = Canonical source entity name ("cycle", not "cycleId")
- `entity` is unique per row (one row per entity+structureType combination)
- Fields stored as arrays: `rawField`, `targetField`, `dataType`
- When flattened, one entity can produce multiple rows

---

### **3. Single Schema Table**

**Question:** Do we want one single schema table?

**Answer:** ✅ **YES** - One `prepare.schema` table with all entities.

**Rationale:**

- Simpler to query and maintain
- Consistent structure across all entities
- Easy to filter by `entity` when needed
- Matches Jira pattern (proven approach)

**Alternative (NOT recommended):**

- Separate tables per entity (`prepare.cycle_schema`, `prepare.project_schema`)
- More complex to maintain
- Harder to query across entities
- Doesn't match Jira pattern

---

## Data Flow

### **Inputs (from Source stage):**

1. **`source.endpoints`** - Endpoint catalog

   - Endpoint paths (e.g., "/cycle", "/project")
   - HTTP methods
   - Query parameters
   - Path parameters

2. **Intelligence (from SDK):**

   - How to extract data (which endpoints, in what order)
   - Entity dependencies (projects → releases → cycles → executions)
   - API constraints and workarounds
   - **Purpose:** Tells Prepare HOW to fetch samples correctly

3. **API Credentials (from Variable Library):**
   - `BASE_URL`, `API_TOKEN`, `BASE_PATH`
   - **Purpose:** Authentication to fetch samples from API

---

### **Process:**

1. **Read endpoints from `source.endpoints`:**

   ```python
   df_endpoints = spark.table("source.endpoints")
   cycle_endpoints = df_endpoints.filter(col("endpoint_path") == "/cycle")
   ```

2. **Use intelligence to determine fetch order:**

   ```python
   # Intelligence tells us: projects → releases → cycles → executions
   # So we fetch in that order, using dependencies
   # Example: Get a project first, then its releases, then cycles
   ```

3. **Fetch sample data from API:**

   ```python
   # Use endpoint + intelligence to make API call
   project_id = get_test_project_id()  # From intelligence or config
   releases = fetch_from_api("/release/project/{project_id}")
   release_id = releases[0]["id"]
   cycles = fetch_from_api("/cycle/release/{release_id}")
   sample_cycle = cycles[0]  # Use first cycle as sample
   ```

4. **Analyze structure:**

   - Infer entity name from endpoint (e.g., "/cycle" → "cycle")
   - Analyze JSON structure (scalar, array, object)
   - Extract all fields
   - Generate target field names (SPECTRA naming convention)

5. **Build schema rows:**
   - One row per entity (or entity+structureType)
   - Fields stored as arrays
   - Metadata populated (group, groupSortOrder, etc.)

---

### **Outputs:**

1. **`prepare.schema`** - Field-level metadata

   - One row per entity
   - Fields as arrays
   - Complete metadata for downstream stages

2. **`prepare.dependencies`** - Entity relationships

   - Which entities depend on which
   - Extracted from Source stage intelligence

3. **`prepare.constraints`** - API limitations
   - Known issues
   - Workarounds
   - Extracted from Source stage intelligence

---

## Auto-Update Mechanism

### **How Schema Auto-Updates:**

1. **On each Prepare run:**

   - Read latest data from `Tables/source/*`
   - Compare with existing `prepare.schema`
   - Detect new fields
   - Add new rows to schema

2. **Field detection:**

   ```python
   existing_fields = set(df_schema.filter(col("entity") == "cycle").select("fieldId").rdd.flatMap(lambda x: x).collect())
   new_fields = set(sample_cycle.keys()) - existing_fields

   if new_fields:
       log.warning(f"  !! New fields detected in cycle: {new_fields}")
       # Add new schema rows
   ```

3. **Version tracking:**
   - Track schema version
   - Log changes
   - Alert on breaking changes

---

## Implementation Plan

### **Phase 1: Base Schema (Current Focus)**

**Goal:** Create base schema with one entity per row extracted directly from endpoints.

**Steps:**

1. Read endpoints from `source.endpoints`
2. Use intelligence to determine which endpoints to call and in what order
3. **Fetch sample data from API** using those endpoints (intelligence tells us how)
4. For each entity, analyze sample JSON structure
5. Build one row per entity
6. Store fields as arrays

**Output:** `prepare.schema` with basic structure (entity, fieldId, structureType, rawField, targetField, dataType)

---

### **Phase 2: Auto-Update**

**Goal:** Auto-detect new fields when data changes.

**Steps:**

1. Compare new data with existing schema
2. Detect new fields
3. Auto-add to schema
4. Log changes

---

### **Phase 3: Full Metadata**

**Goal:** Complete metadata (groups, dimensions, bridges, fact tables).

**Steps:**

1. Add logical grouping
2. Add dimension/bridge names
3. Add fact table metadata
4. Add business process mapping

---

## Questions to Answer

1. **✅ One single schema?** YES - One `prepare.schema` table

2. **✅ One entity per row?** YES - One row per entity (or entity+structureType)

3. **✅ Generate from API samples?** YES - Fetch samples using `source.endpoints` + intelligence, then analyze

4. **✅ Auto-update?** YES - Phase 2 (after base schema works)

---

## Next Steps

1. **Review this design** - Confirm approach
2. **Implement Phase 1** - Base schema from Source stage
3. **Test** - Verify schema generation works
4. **Iterate** - Add auto-update, full metadata

---

## Version History

- **v1.0** (2025-12-11): Initial design document

---

## References

- **Source Stage:** `docs/source/README.md`
- **Canonical Schema Design:** `docs/prepare/canonical-spectra-schema-design.md`
- **Jira Pattern:** `Data/jira/2-prepare/prepareJiraConfig.Notebook/notebook_content.py`
