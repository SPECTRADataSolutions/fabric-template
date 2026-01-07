# SPECTRA-Grade Preview Sample Extraction Architecture

**Date:** 2025-12-08  
**Objective:** Determine the most SPECTRA-grade way to handle preview sample extraction

---

## 🎯 SPECTRA Principles Applied

### Core SPECTRA Principles:
1. **Single Responsibility** - Each stage has one clear purpose
2. **Separation of Concerns** - Stages are independent and focused
3. **Metadata-Driven** - Everything declarative and automation-friendly
4. **Self-Contained** - Stages can run independently
5. **Reusability** - No duplication, shared patterns via SDK
6. **Complete Understanding** - Full visibility into data structures
7. **Modular to the Core** - Clean boundaries between stages

---

## 📋 Stage Responsibilities (SPECTRA-Grade)

### Source Stage Purpose:
> **"Establishes connectivity, validates authentication, and catalogs all available Zephyr API endpoints for downstream pipeline stages."**

**Core Responsibilities:**
- ✅ Validate API authentication
- ✅ Validate hierarchical access (Projects → Releases → Cycles → Executions → Test Cases)
- ✅ Catalog endpoints (228 endpoints)
- ✅ Create portfolio/config/credentials tables
- ✅ **Demonstrate visibility** - Prove we CAN access all hierarchy levels

**Key Insight:**
- "Visibility demonstrated" means **validating access**, not necessarily extracting samples
- Validation already proves visibility: `validate_api_resource_access()` checks each level
- Source stage doesn't NEED samples for its core purpose

---

### Prepare Stage Purpose:
> **"Creates metadata-driven schema definitions that drive downstream Extract, Clean, Transform, and Refine stages."**

**Core Responsibilities:**
- ✅ Introspect data structures
- ✅ Understand field types, nullability, arrays, nested objects
- ✅ Generate schema definitions
- ✅ Create `prepare._schema`, `prepare._endpoints`, `prepare._statusMap`

**Key Insight:**
- Prepare stage NEEDS samples to understand structure
- Schema design requires introspection of actual data
- This is Prepare stage's **core responsibility** - understanding data structure

---

## 🎯 SPECTRA-Grade Solution

### **Option: Prepare Stage Owns Sample Extraction**

**Rationale:**
1. **Single Responsibility:**
   - Source stage: Validates connectivity and access
   - Prepare stage: Understands data structure (needs samples for this)

2. **Separation of Concerns:**
   - Source stage proves we CAN extract (validation)
   - Prepare stage extracts to UNDERSTAND structure (introspection)

3. **Self-Contained:**
   - Prepare stage doesn't depend on source stage running with `preview=True`
   - Can run independently
   - No tight coupling

4. **Clear Ownership:**
   - Samples are "for Prepare stage schema design" → Prepare stage owns them
   - Source stage doesn't need samples for its purpose

5. **Reusability:**
   - Use SDK helper method: `PrepareStageHelpers.extract_introspection_samples()`
   - Can be reused by other stages if needed
   - No duplication

---

## 🏗️ Proposed Architecture

### Source Stage:
```python
# Source stage validates access (doesn't extract samples)
auth_result, all_projects = SourceStageHelpers.validate_api_authentication(...)

# Validate hierarchical access (proves visibility)
if first_project_id:
    validate_api_resource_access("/release/project/{projectId}", ...)  # Projects → Releases
    validate_api_resource_access("/cycle/release/{releaseId}", ...)    # Releases → Cycles
    validate_api_resource_access("/execution/cycle/{cycleId}", ...)    # Cycles → Executions
    validate_api_resource_access("/testcase/{testcaseId}", ...)        # Executions → Test Cases

# Contract fulfilled: "Visibility demonstrated" = validation proves access
```

**Outputs:**
- ✅ `source.portfolio` - Dashboard metadata
- ✅ `source.config` - Runtime config
- ✅ `source.credentials` - Auth status
- ✅ `source.endpoints` - Endpoint catalog
- ❌ **No preview samples** (not source stage's responsibility)

---

### Prepare Stage:
```python
# Prepare stage extracts samples for schema introspection
test_project_id = session.variables.get("TEST_PROJECT_ID")  # 45 (SpectraTestProject)

if session.params["bootstrap"] or not _samples_exist():
    # Extract all hierarchy levels from SpectraTestProject
    samples = PrepareStageHelpers.extract_introspection_samples(
        spark=spark,
        delta=session.delta,
        logger=log,
        base_url=base_url,
        api_token=api_token,
        test_project_id=test_project_id,
        sample_limit=10
    )
    
    # Creates: prepare.sampleProjects, prepare.sampleReleases, 
    #          prepare.sampleCycles, prepare.sampleExecutions, prepare.sampleTestcases

# Introspect structure from samples
schema_data = PrepareStageHelpers.introspect_schema_from_samples(
    spark=spark,
    samples_tables=["prepare.sampleProjects", "prepare.sampleReleases", ...],
    logger=log
)

# Generate prepare._schema table
PrepareStageHelpers.create_prepare_schema_table(
    spark=spark,
    delta=session.delta,
    schema_data=schema_data,
    logger=log
)
```

**Outputs:**
- ✅ `prepare._schema` - Field-level metadata (from introspection)
- ✅ `prepare._endpoints` - API endpoint configs
- ✅ `prepare._statusMap` - Status mappings
- ✅ `prepare.sampleProjects` (temporary, for introspection)
- ✅ `prepare.sampleReleases` (temporary, for introspection)
- ✅ `prepare.sampleCycles` (temporary, for introspection)
- ✅ `prepare.sampleExecutions` (temporary, for introspection)
- ✅ `prepare.sampleTestcases` (temporary, for introspection)

**Note:** Sample tables are temporary (can be cleaned up after schema generation)

---

## ✅ Benefits (SPECTRA-Grade)

1. **Clear Ownership:**
   - Source stage: Connectivity & validation
   - Prepare stage: Schema design (needs samples)

2. **No Dependencies:**
   - Prepare stage doesn't require source stage to run with `preview=True`
   - Each stage can run independently

3. **Single Source of Truth:**
   - Samples extracted from SpectraTestProject (ID 45)
   - Deterministic, perfect structure

4. **Separation of Concerns:**
   - Source validates access
   - Prepare understands structure

5. **Self-Contained:**
   - Prepare stage owns its introspection workflow
   - No tight coupling between stages

6. **Reusable:**
   - SDK helper methods for extraction and introspection
   - Can be reused by other stages if needed

---

## 📋 Updated Contracts

### Source Contract:
```yaml
obligations:
  core:
    - "Auth succeeds against Zephyr base URL + path for all accessible endpoints."
    - "Hierarchical access validated: Projects → Releases → Cycles → Executions → Test Cases."
    # ✅ Validation proves visibility, samples not needed

data_outputs:
  - "source.portfolio: Metadata table for source system dashboard"
  - "source.config: Runtime configuration snapshot"
  - "source.credentials: Masked credential validation status"
  - "source.endpoints: Complete endpoint catalog (228 endpoints)"
  # ❌ Remove preview samples (Prepare stage responsibility)
```

### Prepare Contract (NEW):
```yaml
obligations:
  core:
    - "Extract introspection samples from SpectraTestProject (TEST_PROJECT_ID)"
    - "Introspect data structures (scalar, record, array, nullability)"
    - "Generate metadata-driven schema definitions"
    - "Create prepare._schema, prepare._endpoints, prepare._statusMap tables"

inputs:
  - "source.endpoints: API endpoint catalog"
  - "source.portfolio: Source system metadata"
  - "TEST_PROJECT_ID: SpectraTestProject ID (from Variable Library)"

data_outputs:
  - "prepare._schema: Field-level metadata for all entities"
  - "prepare._endpoints: API endpoint configurations"
  - "prepare._statusMap: Status mappings"
  - "prepare.sampleProjects: Introspection samples (temporary)"
  - "prepare.sampleReleases: Introspection samples (temporary)"
  - "prepare.sampleCycles: Introspection samples (temporary)"
  - "prepare.sampleExecutions: Introspection samples (temporary)"
  - "prepare.sampleTestcases: Introspection samples (temporary)"
```

---

## 🔧 Implementation Plan

### Phase 1: Remove Samples from Source Stage
- ✅ Remove `preview` parameter extraction from `sourceZephyr.Notebook`
- ✅ Update contract to remove preview samples from `data_outputs`
- ✅ Keep hierarchical validation (proves visibility)

### Phase 2: Add Sample Extraction to Prepare Stage
- ✅ Create `PrepareStageHelpers.extract_introspection_samples()` method
- ✅ Extract all 5 hierarchy levels from SpectraTestProject
- ✅ Store in `prepare.sample*` tables

### Phase 3: Add Schema Introspection
- ✅ Create `PrepareStageHelpers.introspect_schema_from_samples()` method
- ✅ Analyze Delta table structures
- ✅ Infer field types, nullability, arrays, nested objects
- ✅ Generate Prepare stage schema format

### Phase 4: Update Contracts
- ✅ Create `contracts/prepare.contract.yaml`
- ✅ Update `contracts/source.contract.yaml` (remove preview samples)
- ✅ Create `manifests/prepare.manifest.yaml`

---

## ✅ SPECTRA-Grade Checklist

- [x] **Single Responsibility** - Each stage has clear purpose
- [x] **Separation of Concerns** - No overlap in responsibilities
- [x] **Self-Contained** - Prepare stage can run independently
- [x] **Clear Ownership** - Prepare owns schema introspection (needs samples)
- [x] **No Dependencies** - Prepare doesn't require source stage preview mode
- [x] **Reusable Patterns** - SDK helper methods
- [x] **Metadata-Driven** - Schema from introspection
- [x] **Complete Understanding** - Introspect all hierarchy levels
- [x] **Modular** - Clean stage boundaries

---

## 🎯 Final Recommendation

**SPECTRA-Grade Approach:**

1. **Source Stage:** 
   - Validates access (hierarchical validation)
   - No preview samples (not its responsibility)
   - Contract: "Visibility demonstrated" = validation, not extraction

2. **Prepare Stage:**
   - Extracts samples from SpectraTestProject
   - Introspects structure for schema design
   - Owns sample extraction (core to its purpose)

**This aligns with SPECTRA principles:**
- ✅ Single responsibility
- ✅ Separation of concerns
- ✅ Self-contained stages
- ✅ Clear ownership
- ✅ No unnecessary dependencies

---

**Version:** 1.0.0  
**Date:** 2025-12-08  
**Status:** 🟢 SPECTRA-Grade Architecture

