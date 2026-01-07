# Prepare Stage - Preview Sample Extraction Design

**Date:** 2025-12-08  
**Question:** Should preview samples be extracted at the START of prepare stage for schema introspection?

---

## 🔍 Current Prepare Stage Workflow

### Step 1: Discover Schemas
**Tool:** `scripts/discover_schemas_via_creation.py`
- **Creates** sample entities in SpectraTestProject (via POST/PUT)
- Captures full API response schemas
- Saves to `docs/schemas/discovered/*_created_response.json`

### Step 2: Generate Prepare Schema
**Tool:** `scripts/generate_prepare_schema.py`
- Reads discovered schema JSON files
- Analyzes structure (scalar/record/array)
- Generates Prepare stage schema format

### Step 3: Prepare Stage Notebook
**Notebook:** `prepareZephyr.Notebook`
- Loads schema from generated JSON
- Creates `prepare._schema`, `prepare._endpoints`, `prepare._statusMap` tables

---

## 🤔 Architectural Question

**Should prepare stage extract preview samples to introspect structure?**

### Option A: Prepare Stage Extracts Samples Itself (Introspection)

**Workflow:**
1. **Prepare stage starts**
2. **Extract preview samples from SpectraTestProject** (via GET API)
   - Extract projects, releases, cycles, executions, testcases
   - Store in Delta tables (e.g., `prepare.sampleProjects`, `prepare.sampleReleases`)
3. **Introspect samples** to understand structure
   - Analyze JSON structures
   - Infer field types, nullability
   - Detect arrays, nested objects
4. **Generate schema** from introspection
5. **Create `prepare._schema` table**

**Pros:**
- ✅ Self-contained - Prepare stage owns its schema discovery
- ✅ Dynamic - Can introspect actual data structures
- ✅ No dependency on source stage for samples
- ✅ Can refresh samples when schema changes

**Cons:**
- ❌ Duplicate extraction logic (same as source stage)
- ❌ Extra API calls (but only for SpectraTestProject)
- ❌ Prepare stage does API extraction (might be source stage responsibility)

---

### Option B: Prepare Stage Uses Source Stage Samples (Current Intent)

**Workflow:**
1. **Source stage extracts preview samples** (when `preview=True`)
   - Creates `source.sampleProjects`, `source.sampleReleases`, etc.
   - From SpectraTestProject (project ID 45)
2. **Prepare stage reads source stage samples**
   - Reads from `source.sampleProjects`, `source.sampleReleases`, etc.
   - Introspects structure from Delta tables
   - Generates schema
3. **Create `prepare._schema` table**

**Pros:**
- ✅ Single source of truth (source stage owns extraction)
- ✅ Reuses source stage extraction logic
- ✅ Separation of concerns (source extracts, prepare designs)

**Cons:**
- ❌ Dependency on source stage running with `preview=True`
- ❌ Samples might not exist if source stage didn't run with preview
- ❌ Source stage might extract from wrong project

---

### Option C: Prepare Stage Uses Discovered Schema JSONs (Current Implementation)

**Workflow:**
1. **Separate script:** `discover_schemas_via_creation.py`
   - Creates entities in SpectraTestProject
   - Captures API response schemas
   - Saves to JSON files
2. **Prepare stage loads JSON files**
   - Reads `docs/schemas/discovered/*.json`
   - Generates schema from JSON definitions
   - Creates `prepare._schema` table

**Pros:**
- ✅ No API calls in prepare stage
- ✅ Fast (just reading JSON files)
- ✅ Deterministic (same schemas every time)

**Cons:**
- ❌ Requires separate script run before prepare stage
- ❌ JSON files might be stale
- ❌ No introspection from actual Delta table data

---

## 🎯 Analysis: What Does Prepare Stage Need?

### Prepare Stage Purpose:
> "Creates metadata-driven schema definitions that drive downstream Extract, Clean, Transform, and Refine stages"

### What Prepare Needs:
1. **Structure understanding:**
   - Field types (scalar, record, array)
   - Nested objects
   - Arrays and bridge tables

2. **Field metadata:**
   - Data types (text, int64, datetime, etc.)
   - Nullability
   - Field paths (JSON paths)

3. **Entity relationships:**
   - Foreign keys
   - Hierarchy (projects → releases → cycles → executions)

### Where Can This Come From?

**Option 1: API Response Schemas (Current)**
- ✅ Already have: `docs/schemas/discovered/*.json`
- ✅ Perfect structure (from POST/PUT responses)
- ✅ Complete field definitions

**Option 2: Preview Sample Data (Delta Tables)**
- ✅ Actual data structures
- ✅ Can introspect from Delta tables
- ✅ Can validate against real data

**Option 3: Both**
- Use JSON schemas as primary
- Use preview samples to validate/verify

---

## 💡 Recommendation

### **Option D: Hybrid Approach (Best of All Worlds)**

**Prepare Stage Workflow:**

1. **Try to load from JSON files first** (fast, deterministic)
   - Load `docs/schemas/discovered/*.json`
   - If exists → use it

2. **Fallback to preview sample introspection** (if JSON missing)
   - Check if `source.sampleProjects`, etc. exist
   - If exists → introspect from Delta tables
   - Generate schema from samples

3. **Fallback to direct extraction** (if samples missing)
   - Extract from SpectraTestProject directly
   - Store samples temporarily
   - Introspect and generate schema

**Benefits:**
- ✅ Fast path: JSON files (if available)
- ✅ Self-healing: Introspect if JSON missing
- ✅ No dependencies: Can extract if source stage didn't run
- ✅ Validation: Can verify JSON schemas against actual samples

---

## 📋 Prepare Stage Manifest (What Should It Say?)

### Current State:
- **No prepare manifest exists** (only source.manifest.yaml)
- **No prepare contract exists** (only source.contract.yaml)

### What Prepare Stage Should Define:

**Inputs:**
- `source.endpoints` - API endpoint catalog
- `source.portfolio` - Source system metadata
- `source.sampleProjects` (optional) - Preview samples for introspection
- OR `docs/schemas/discovered/*.json` - Discovered schemas

**Outputs:**
- `prepare._schema` - Field-level metadata
- `prepare._endpoints` - API endpoint configurations
- `prepare._statusMap` - Status mappings

**Responsibilities:**
- Introspect data structures (from samples or JSON)
- Generate metadata-driven schema definitions
- Validate schema coherence

---

## 🎯 Decision Needed

**Should prepare stage:**

**A) Extract preview samples itself** (self-contained, no dependencies)
- Extract from SpectraTestProject at start
- Introspect structure
- Generate schema

**B) Use source stage samples** (reuse, separation of concerns)
- Read from `source.sampleProjects`, etc.
- Introspect from Delta tables
- Generate schema

**C) Use JSON schema files** (current, fast)
- Load from `docs/schemas/discovered/*.json`
- No introspection needed
- Requires separate script run

**D) Hybrid** (flexible, self-healing)
- Try JSON first
- Fallback to source stage samples
- Fallback to direct extraction

---

## 📝 My Recommendation

**Option D: Hybrid Approach**

**Rationale:**
1. **Fast path** - Use JSON if available (no API calls)
2. **Self-healing** - Can introspect if JSON missing
3. **Flexible** - Works with or without source stage samples
4. **Validation** - Can verify JSON against actual samples

**Implementation:**
```python
# In prepareZephyr.Notebook

# Step 1: Try to load from JSON
if schema_json_exists:
    schema_data = load_from_json()
else:
    # Step 2: Try to introspect from source stage samples
    if spark.table("source.sampleProjects").count() > 0:
        schema_data = introspect_from_delta_tables()
    else:
        # Step 3: Extract from SpectraTestProject directly
        test_project_id = session.variables.get("TEST_PROJECT_ID")
        samples = extract_preview_samples(test_project_id)
        schema_data = introspect_from_samples(samples)
```

---

**What do you think? Should prepare stage:**
- Extract samples itself?
- Use source stage samples?
- Use JSON files (current)?
- Hybrid approach?

