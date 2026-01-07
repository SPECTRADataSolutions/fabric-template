# Playbook Structure Analysis

**Date:** 2025-12-11  
**Purpose:** Analyse current playbook structure and determine optimal structure

---

## Current State

### **Setup Stage (0-setup):**
- 7 playbooks: `setup.000` through `setup.006`
- Each playbook: Single responsibility (create repo, workspace, lakehouse, etc.)

### **Source Stage (1-source):**
- 3 playbooks: `source.001`, `source.002`, `source.003`
- Each playbook: Single responsibility (create notebook, add to pipeline, bootstrap endpoints)

### **Prepare Stage (2-prepare):**
- 5+ playbooks:
  - `prepare.000` - Discover field metadata
  - `prepare.001` - Create test data
  - `prepare.002` - Introspect schemas
  - `prepare.003` - Load schema into notebook
  - `prepare.004` - Create requirements
  - (Some duplicates: `prepare.001-comprehensive-api-validation.md`, `prepare.004-createRequirements.md`)

---

## Analysis: Many Playbooks vs One Orchestration Playbook

### **Option 1: Many Granular Playbooks (Current)**

**Structure:**
```
prepare.000-discoverFieldMetadata.md
prepare.001-createTestData.md
prepare.002-introspectSchemas.md
prepare.003-loadSchemaIntoNotebook.md
prepare.004-createRequirements.md
```

**Pros:**
- ✅ Single responsibility per playbook
- ✅ Can run individual steps independently
- ✅ Easy to test individual steps
- ✅ Clear dependencies (prepare.001 requires prepare.000)
- ✅ Reusable (can run prepare.002 without running prepare.001 if data exists)

**Cons:**
- ❌ Need to know which playbooks to run
- ❌ Manual orchestration (run prepare.000, then prepare.001, then...)
- ❌ Easy to miss a step
- ❌ No single "run prepare stage" command

---

### **Option 2: One Orchestration Playbook**

**Structure:**
```
prepare.000-orchestrate-prepare-stage.md
```

**Content:**
- Step 1: Discover field metadata
- Step 2: Create test data
- Step 3: Introspect schemas
- Step 4: Load schema into notebook
- Step 5: Create requirements

**Pros:**
- ✅ Single "run prepare stage" command
- ✅ Can't miss steps (all in one place)
- ✅ Clear flow from start to finish
- ✅ Easy to orchestrate via solution engine

**Cons:**
- ❌ Can't run individual steps independently
- ❌ Harder to test individual steps
- ❌ Less reusable (must run entire playbook)
- ❌ Large playbook (harder to maintain)

---

### **Option 3: Hybrid (Orchestration + Granular)**

**Structure:**
```
prepare.000-orchestrate-prepare-stage.md  # Main orchestration
prepare.001-discoverFieldMetadata.md      # Step 1 (can run independently)
prepare.002-createTestData.md             # Step 2 (can run independently)
prepare.003-introspectSchemas.md          # Step 3 (can run independently)
prepare.004-loadSchemaIntoNotebook.md     # Step 4 (can run independently)
prepare.005-createRequirements.md         # Step 5 (can run independently)
```

**How it works:**
- `prepare.000` orchestrates all steps
- Each step playbook can be run independently
- Solution engine uses `prepare.000` for automation
- Manual users can use individual playbooks

**Pros:**
- ✅ Best of both worlds
- ✅ Automation uses orchestration playbook
- ✅ Manual users can run individual steps
- ✅ Clear dependencies
- ✅ Reusable components

**Cons:**
- ⚠️ Some duplication (orchestration references steps)
- ⚠️ Need to maintain both

---

## Recommendation: **Option 3 (Hybrid)**

### **Why Hybrid is Optimal:**

1. **For Automation (Solution Engine):**
   - Uses `prepare.000-orchestrate-prepare-stage.md`
   - Single command: "run prepare stage"
   - All steps executed in order
   - Quality gates at each step

2. **For Manual Users:**
   - Can run individual playbooks if needed
   - Can skip steps if prerequisites already met
   - Can test individual steps
   - Can re-run specific steps

3. **For Self-Improvement:**
   - If gap detected, update orchestration playbook
   - Individual playbooks remain reusable
   - Standards updated in orchestration playbook

---

## Proposed Structure

### **Orchestration Playbook:**

**`prepare.000-orchestrate-prepare-stage.md`**

```markdown
# Prepare Stage Orchestration

## Purpose
Orchestrate complete Prepare stage to create metadata-driven configuration tables.

## Process

### Step 1: Discover Field Metadata
**Playbook:** `prepare.001-discoverFieldMetadata.md`
- Discovers field types, enum values, validation rules
- Output: `docs/schemas/discovered/field_metadata.json`

### Step 2: Create Test Data
**Playbook:** `prepare.002-createTestData.md`
- Creates comprehensive test data using discovered metadata
- Output: Test entities in Zephyr, captured API responses

### Step 3: Introspect Schemas
**Playbook:** `prepare.003-introspectSchemas.md`
- Generates schema JSON from test data
- Output: `prepare_schema_generated.json`

### Step 4: Load Schema Into Notebook
**Playbook:** `prepare.004-loadSchemaIntoNotebook.md`
- Loads schema into Fabric notebook
- Creates Delta tables
- Output: `prepare.schema`, `prepare.dependencies`, `prepare.constraints`

### Step 5: Create Requirements (Optional)
**Playbook:** `prepare.005-createRequirements.md`
- Creates requirements structure
- Output: Requirements in Zephyr

## Quality Gates
- ✅ All steps completed successfully
- ✅ Schema has rows for all entities
- ✅ One entity per row
- ✅ Tables created and registered

## Dependencies
- Requires: Source stage complete
- Enables: Extract stage
```

### **Individual Step Playbooks:**

- `prepare.001-discoverFieldMetadata.md` - Can run independently
- `prepare.002-createTestData.md` - Can run independently
- `prepare.003-introspectSchemas.md` - Can run independently
- `prepare.004-loadSchemaIntoNotebook.md` - Can run independently
- `prepare.005-createRequirements.md` - Can run independently

---

## Implementation

### **For Solution Engine:**

```python
# solution_engine/stages/build.py
def execute_prepare_stage(covenant):
    # Read orchestration playbook
    playbook = read_playbook("prepare.000-orchestrate-prepare-stage.md")
    
    # Execute each step
    for step in playbook.steps:
        step_playbook = read_playbook(step.playbook_path)
        execute_step(step_playbook)
        validate_quality_gate(step.quality_gates)
```

### **For Manual Users:**

```bash
# Option 1: Run entire stage
follow prepare.000-orchestrate-prepare-stage.md

# Option 2: Run individual step
follow prepare.002-createTestData.md
```

---

## Benefits

1. **Automation:**
   - Solution engine uses orchestration playbook
   - Single command runs entire stage
   - Quality gates at each step

2. **Flexibility:**
   - Manual users can run individual steps
   - Can skip steps if prerequisites met
   - Can test individual steps

3. **Maintainability:**
   - Orchestration playbook shows complete flow
   - Individual playbooks remain focused
   - Easy to update individual steps

4. **Self-Improvement:**
   - Gaps detected in orchestration playbook
   - Standards updated in orchestration playbook
   - Individual playbooks remain reusable

---

## Migration Plan

1. **Create orchestration playbook:**
   - `prepare.000-orchestrate-prepare-stage.md`
   - References existing step playbooks

2. **Rename existing playbooks:**
   - `prepare.000-discoverFieldMetadata.md` → `prepare.001-discoverFieldMetadata.md`
   - `prepare.001-createTestData.md` → `prepare.002-createTestData.md`
   - `prepare.002-introspectSchemas.md` → `prepare.003-introspectSchemas.md`
   - `prepare.003-loadSchemaIntoNotebook.md` → `prepare.004-loadSchemaIntoNotebook.md`
   - `prepare.004-createRequirements.md` → `prepare.005-createRequirements.md`

3. **Update references:**
   - Update all playbook references
   - Update README.md
   - Update documentation

---

## Questions to Answer

1. **✅ Is many playbooks per stage optimal?** NO - Hybrid is better (orchestration + granular)

2. **✅ Should we have orchestration playbooks?** YES - One per stage for automation

3. **✅ Should we keep granular playbooks?** YES - For manual users and flexibility

4. **✅ Should solution engine use orchestration?** YES - Single command per stage

---

## Version History

- **v1.0** (2025-12-11): Initial analysis of playbook structure

---

## References

- **Current Playbooks:** `Core/operations/playbooks/fabric/2-prepare/`
- **Playbook Structure:** `Core/operations/playbooks/STRUCTURE.md`
- **Solution Engine:** `Core/solution-engine/README.md`




