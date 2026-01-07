# Source Notebook Cleanup Plan

**Date:** 2025-12-05  
**Purpose:** Comprehensive cleanup of `sourceZephyr` notebook to align with SPECTRA standards

---

## 🔍 Analysis Summary

### 1. Source Table (`source.source`) - Legacy Analysis

**Current fields:**
- `source_system`, `source_name`, `base_url`, `base_path`, `full_url`
- `workspace_id`, `lakehouse_id`, `lakehouse_name`
- `last_updated`

**In Variable Library (`zephyrVariables`):**
- `SOURCE_SYSTEM` ✅
- `SOURCE_NAME` ✅
- `BASE_URL` ✅
- `BASE_PATH` ✅
- API_TOKEN (secret)

**Fabric Runtime Context:**
- `workspace_id` ✅
- `lakehouse_id` ✅
- `lakehouse_name` ✅

**Verdict:** Source table is **90% redundant**. Most fields are:
- ✅ In Variable Library (already managed)
- ✅ In Fabric Runtime (automatically available)
- ✅ Can be inferred from notebook context

**Recommendation:** 
- **Minimal source table** - Store only:
  - `source_system` (key reference)
  - `last_updated` (audit trail)
  - Optional: `contract_version` (for traceability)

### 2. Config Table (`source.config`) - Purpose

**Current fields:**
- `execution_mode` (pipeline vs interactive)
- `operation_type` (from Pipeline class)
- `last_updated`

**Purpose:** 
- Runtime execution context (critical for debugging)
- Pipeline vs interactive mode tracking
- Operation type tracking (SessionCreation, etc.)

**Verdict:** ✅ **KEEP** - Important for operational visibility

**Recommendation:**
- Add more runtime context:
  - `notebook_name`
  - `stage`
  - `sdk_version`
  - `fabric_environment_id`

### 3. Endpoints - Current State

**Current:** Only 5 endpoints hardcoded in notebook
**Available:** 228 endpoints in `docs/endpoints.json`
**Contract defines:** 4 primary objects (projects, releases, cycles, executions)

**Issue:** Endpoints table should contain ALL 228 endpoints for cataloguing

**Recommendation:**
- Load all 228 endpoints from `endpoints.json`
- Categorise by:
  - `category` (projects, releases, cycles, executions, admin, etc.)
  - `method` (GET, POST, PUT, DELETE)
  - `requires_auth` (True/False)
  - `hierarchical` (True/False)
  - `status` (working, failing, deprecated)
- Store in `source.endpoints` Delta table
- Use SDK to bootstrap

### 4. Contract vs Manifest Alignment

**Source Contract (`contracts/source.contract.yaml`):**
- Defines: authentication, hierarchical access, endpoint catalogue
- Obligations: 120 GET endpoints tested, 84 working
- Outputs: Sample dimensional database

**Manifest (`manifests/source.manifest.yaml`):**
- Documents: Comprehensive endpoint testing results
- Shows: 228 endpoints catalogued, 120 tested, 84 working
- Evidence: Quality gates, sample extraction

**Verdict:** ✅ **ALIGNED** - Contract defines obligations, manifest records evidence

**Gap:** Contract references old variable names (`DXC_ZEPHYR_*`) vs current clean names

**Recommendation:**
- Update contract to reference clean Variable Library names
- Document manifest as evidence of contract fulfilment

### 5. Bad Practices from sourceJira

**Identified Issues:**

1. **Inline `register_delta_table()` function** ❌
   - Should be in SDK
   - Duplicated logic
   - Not reusable

2. **Hardcoded project ID** ❌
   - `first_project_id = 44`
   - Should come from API response or Variable Library

3. **Magic number** ❌
   - `[:10]` in sample extraction
   - Should be parameterised

4. **Manual table registration** ⚠️
   - Explicit registration calls at end
   - Should be handled by SDK automatically

**Recommendation:**
- Move `register_delta_table()` to SDK as `DeltaTable.register()`
- Use first project from API response
- Parameterise sample limits
- Auto-register tables in SDK write() method

### 6. Shared Modules to Move to SDK

**Current inline functions:**
- `register_delta_table()` → SDK `DeltaTable.register()`
- Health check functions → SDK `SourceHealth` class?
- Endpoint bootstrap logic → SDK `EndpointCatalog` class?

**Recommendation:**
- Move table registration to SDK (already in `DeltaTable`)
- Keep health checks in notebook (source-specific logic)
- Move endpoint catalog to SDK as utility function

---

## ✅ Cleanup Tasks

### Phase 1: Table Structure Cleanup

- [ ] Simplify `source.source` table (remove redundant fields)
- [ ] Enhance `source.config` table (add runtime context)
- [ ] Document `source.config` purpose in comments

### Phase 2: Endpoints Enhancement

- [ ] Load all 228 endpoints from `endpoints.json`
- [ ] Categorise endpoints by type/category
- [ ] Add endpoint status tracking (working, failing, deprecated)
- [ ] Update SDK to support endpoint catalog bootstrap

### Phase 3: Move Shared Code to SDK

- [ ] Remove inline `register_delta_table()` function
- [ ] Use SDK `DeltaTable.register()` instead
- [ ] Create `EndpointCatalog` utility in SDK
- [ ] Move endpoint parsing logic to SDK

### Phase 4: Remove Bad Practices

- [ ] Remove hardcoded project ID (use API response)
- [ ] Parameterise sample limits
- [ ] Remove manual table registration (use SDK auto-register)

### Phase 5: Contract Alignment

- [ ] Update contract variable references
- [ ] Document manifest as contract evidence
- [ ] Align notebook with contract obligations

---

## 📊 Expected Outcomes

1. **Cleaner notebook:** ~150 lines (down from ~420)
2. **All 228 endpoints** registered in Delta
3. **Zero hardcoded values** (everything from Variable Library or runtime)
4. **SDK handles** all shared logic
5. **Contract aligned** with implementation

---

## 🎯 Success Criteria

- ✅ Source table minimal (3-4 fields only)
- ✅ Config table well-documented
- ✅ All 228 endpoints in Delta
- ✅ Zero inline utility functions
- ✅ Zero hardcoded IDs/values
- ✅ Contract and manifest aligned

---

**Next Steps:** Start with Phase 1 (table cleanup) and work through systematically.

