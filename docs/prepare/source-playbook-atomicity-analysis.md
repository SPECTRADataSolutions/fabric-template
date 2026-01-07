# Source Stage Playbook Atomicity Analysis

**Date:** 2025-12-11  
**Purpose:** Infer missing playbooks from implementation and determine perfect atomicity

---

## What the Source Stage Actually Does

Based on implementation analysis (`sourceZephyr.Notebook`, `SOURCE-TABLES-LIFECYCLE.md`, `source-notebook-complete-flow.md`):

### **Infrastructure Setup:**
1. ✅ Create notebook artifact (`source.001`)
2. ✅ Wire notebook to pipeline (`source.002`)

### **Metadata Bootstrap:**
3. ✅ Bootstrap endpoints catalog (`source.003`)

### **Runtime Execution (MISSING PLAYBOOKS):**
4. ❌ Create runtime metadata tables (`source.config`, `source.credentials`, `source.portfolio`)
5. ❌ Validate authentication and connectivity
6. ❌ Validate hierarchical access (Projects → Releases → Cycles → Executions)
7. ❌ Comprehensive endpoint health check (120 GET endpoints)
8. ❌ Create quality gate report

### **Optional Operations (MISSING PLAYBOOKS):**
9. ❌ Extract preview samples (`source.sampleProjects`, `source.sampleReleases`)

### **Validation (MISSING PLAYBOOK):**
10. ❌ Validate source stage completion (`source.004` - referenced but not created)

---

## Perfect Atomicity Analysis

### **Principle: Separation of Concerns**

Each playbook should:
- ✅ Have a **single, clear responsibility**
- ✅ Be **independently executable** (can run on its own)
- ✅ Have **clear inputs and outputs**
- ✅ Be **not too small** (not a single function call)
- ✅ Be **not too big** (not multiple unrelated operations)

---

## Current Playbooks (3)

### **✅ source.001 - Create Source Notebook**
**Responsibility:** Infrastructure setup - create notebook artifact  
**Atomicity:** ✅ Perfect - Single responsibility, independently executable  
**Inputs:** Workspace, lakehouse, pipeline  
**Outputs:** Notebook artifact with `.platform` file  
**Can run independently:** ✅ Yes (requires setup playbooks)

---

### **✅ source.002 - Add Notebook to Pipeline**
**Responsibility:** Infrastructure setup - wire notebook to pipeline  
**Atomicity:** ✅ Perfect - Single responsibility, independently executable  
**Inputs:** Notebook logicalId, workspaceId, pipeline  
**Outputs:** Pipeline activity configured  
**Can run independently:** ✅ Yes (requires source.001)

---

### **✅ source.003 - Bootstrap Endpoints**
**Responsibility:** Metadata bootstrap - create endpoints catalog  
**Atomicity:** ✅ Perfect - Single responsibility, independently executable  
**Inputs:** Endpoints JSON, init_mode parameter  
**Outputs:** `source.endpoints` table, `Files/config/{sourceKey}/endpoints.json`  
**Can run independently:** ✅ Yes (requires source.001, source.002)

---

## Missing Playbooks (7)

### **❌ source.004 - Validate Source Stage**
**Responsibility:** Quality gates - validate source stage completion  
**Atomicity:** ✅ Perfect - Single responsibility (validation)  
**Inputs:** All source tables, quality gate criteria  
**Outputs:** Quality gate report, pass/fail status  
**Can run independently:** ✅ Yes (requires all source operations complete)  
**Status:** Referenced in `source.003` but not created

**What it should do:**
- Validate `source.endpoints` table exists and populated
- Validate `source.config` table exists
- Validate `source.credentials` table exists
- Validate `source.portfolio` table exists
- Validate no duplicate endpoints (same path + method)
- Validate hierarchical access works
- Validate endpoint health check passed
- Output: Quality gate report

---

### **❌ source.005 - Create Runtime Metadata Tables**
**Responsibility:** Runtime execution - create config, credentials, portfolio tables  
**Atomicity:** ✅ Perfect - Single responsibility (runtime metadata)  
**Inputs:** Session context, variable library, SDK  
**Outputs:** `source.config`, `source.credentials`, `source.portfolio` tables  
**Can run independently:** ✅ Yes (requires source.001, source.002, SDK)

**What it should do:**
- Create `source.config` table (execution context)
- Create `source.credentials` table (masked auth)
- Create `source.portfolio` table (dashboard metadata)
- All tables use `mode="overwrite"` (always recreated)
- Preserve `discovery_date` in portfolio (from first run)

**Why separate:** These are runtime tables created every execution, different from bootstrap (endpoints).

---

### **❌ source.006 - Validate Authentication and Connectivity**
**Responsibility:** Validation - test authentication and basic connectivity  
**Atomicity:** ✅ Perfect - Single responsibility (auth validation)  
**Inputs:** API credentials, base URL, base path  
**Outputs:** Auth status, connectivity status, `source.credentials` updated  
**Can run independently:** ✅ Yes (requires credentials configured)

**What it should do:**
- Test authentication against base URL + path
- Test basic connectivity (handshake endpoint)
- Update `source.credentials` with validation status
- Fast fail if auth broken

**Why separate:** Auth validation is a distinct operation that can fail independently.

---

### **❌ source.007 - Validate Hierarchical Access**
**Responsibility:** Validation - test hierarchical dependency chain  
**Atomicity:** ✅ Perfect - Single responsibility (hierarchical validation)  
**Inputs:** `source.endpoints` table, API credentials  
**Outputs:** Hierarchical validation results, `source.hierarchical_validation` table  
**Can run independently:** ✅ Yes (requires source.003, source.006)

**What it should do:**
- Test `/project/details` → get projects
- Test `/release/project/{id}` → get releases for project
- Test `/cycle/release/{id}` → get cycles for release
- Test `/execution?cycleid={id}` → get executions for cycle
- Validate all 4 levels work
- Create `source.hierarchical_validation` table

**Why separate:** Hierarchical validation is a distinct validation step.

---

### **❌ source.008 - Comprehensive Endpoint Health Check**
**Responsibility:** Validation - test all GET endpoints  
**Atomicity:** ✅ Perfect - Single responsibility (endpoint health)  
**Inputs:** `source.endpoints` table, API credentials  
**Outputs:** `source.endpoint_health` table (120 rows), health metrics  
**Can run independently:** ✅ Yes (requires source.003, source.006)

**What it should do:**
- Test ALL 120 GET endpoints with basic parameters
- Document which endpoints work/fail
- Create `source.endpoint_health` table
- Calculate success rate
- Duration: ~30-60 seconds

**Why separate:** Comprehensive health check is a distinct validation operation.

---

### **❌ source.009 - Extract Preview Samples**
**Responsibility:** Optional operation - extract sample data for validation  
**Atomicity:** ✅ Perfect - Single responsibility (sample extraction)  
**Inputs:** `source.endpoints` table, API credentials, `preview=True` parameter  
**Outputs:** `source.sampleProjects`, `source.sampleReleases` tables  
**Can run independently:** ✅ Yes (requires source.003, source.006, source.007)

**What it should do:**
- Extract sample projects (limited to sample_limit, default 10)
- Extract sample releases (limited to sample_limit)
- Create `source.sampleProjects` table
- Create `source.sampleReleases` table
- Only runs if `preview=True`

**Why separate:** Preview extraction is optional and distinct from validation.

---

### **❌ source.010 - Create Quality Gate Report**
**Responsibility:** Quality gates - generate quality gate report  
**Atomicity:** ✅ Perfect - Single responsibility (quality reporting)  
**Inputs:** All validation results (hierarchical, health check, auth)  
**Outputs:** `source.quality_gate_report` table, pass/fail status  
**Can run independently:** ✅ Yes (requires source.007, source.008)

**What it should do:**
- Aggregate validation results
- Calculate quality metrics
- Determine readiness for Prepare stage
- Create `source.quality_gate_report` table
- Output: Pass/fail status

**Why separate:** Quality gate reporting is a distinct operation that aggregates results.

---

## Recommended Playbook Structure

### **Infrastructure (Setup):**
- `source.001` - Create source notebook ✅
- `source.002` - Add notebook to pipeline ✅

### **Metadata (Bootstrap):**
- `source.003` - Bootstrap endpoints ✅

### **Runtime (Execution):**
- `source.005` - Create runtime metadata tables ❌ **NEW**
- `source.006` - Validate authentication and connectivity ❌ **NEW**

### **Validation:**
- `source.007` - Validate hierarchical access ❌ **NEW**
- `source.008` - Comprehensive endpoint health check ❌ **NEW**
- `source.010` - Create quality gate report ❌ **NEW**

### **Optional:**
- `source.009` - Extract preview samples ❌ **NEW**

### **Quality Gates:**
- `source.004` - Validate source stage ❌ **NEW** (referenced but missing)

---

## Execution Order

### **Normal Run (bootstrap=False, preview=False):**
```
1. source.001 - Create notebook ✅
2. source.002 - Add to pipeline ✅
3. source.005 - Create runtime metadata ✅ (NEW)
4. source.006 - Validate auth ✅ (NEW)
5. source.004 - Validate completion ✅ (NEW)
```

### **Bootstrap Run (bootstrap=True, preview=False):**
```
1. source.001 - Create notebook ✅
2. source.002 - Add to pipeline ✅
3. source.003 - Bootstrap endpoints ✅
4. source.005 - Create runtime metadata ✅ (NEW)
5. source.006 - Validate auth ✅ (NEW)
6. source.007 - Validate hierarchical ✅ (NEW)
7. source.008 - Health check ✅ (NEW)
8. source.010 - Quality gate report ✅ (NEW)
9. source.004 - Validate completion ✅ (NEW)
```

### **Full Run (bootstrap=True, preview=True):**
```
1. source.001 - Create notebook ✅
2. source.002 - Add to pipeline ✅
3. source.003 - Bootstrap endpoints ✅
4. source.005 - Create runtime metadata ✅ (NEW)
5. source.006 - Validate auth ✅ (NEW)
6. source.007 - Validate hierarchical ✅ (NEW)
7. source.008 - Health check ✅ (NEW)
8. source.009 - Extract preview samples ✅ (NEW)
9. source.010 - Quality gate report ✅ (NEW)
10. source.004 - Validate completion ✅ (NEW)
```

---

## Atomicity Principles Applied

### **✅ Good Atomicity:**
- Each playbook has **single responsibility**
- Each playbook is **independently executable**
- Clear **inputs and outputs**
- **Not too small** (not just one function call)
- **Not too big** (not multiple unrelated operations)

### **Examples:**
- ✅ `source.001` - Create notebook (infrastructure setup)
- ✅ `source.003` - Bootstrap endpoints (metadata catalog)
- ✅ `source.005` - Create runtime metadata (runtime tables)
- ✅ `source.006` - Validate auth (auth validation)
- ✅ `source.007` - Validate hierarchical (hierarchical validation)
- ✅ `source.008` - Health check (endpoint validation)
- ✅ `source.009` - Extract preview (sample extraction)
- ✅ `source.010` - Quality gate report (quality reporting)
- ✅ `source.004` - Validate completion (final validation)

---

## Summary

### **Current Status:**
- ✅ 3 playbooks exist (001, 002, 003)
- ❌ 7 playbooks missing (004, 005, 006, 007, 008, 009, 010)

### **Missing Playbooks:**
1. `source.004` - Validate source stage (referenced but not created)
2. `source.005` - Create runtime metadata tables
3. `source.006` - Validate authentication and connectivity
4. `source.007` - Validate hierarchical access
5. `source.008` - Comprehensive endpoint health check
6. `source.009` - Extract preview samples (optional)
7. `source.010` - Create quality gate report

### **Perfect Atomicity:**
- ✅ Each playbook has single responsibility
- ✅ Each playbook is independently executable
- ✅ Clear separation of concerns
- ✅ Not too small, not too big

---

## Version History

- **v1.0** (2025-12-11): Initial atomicity analysis based on implementation

---

## References

- **Source Tables Lifecycle:** `docs/source/SOURCE-TABLES-LIFECYCLE.md`
- **Source Complete Flow:** `docs/source-notebook-complete-flow.md`
- **Source Notebook:** `sourceZephyr.Notebook/notebook_content.py`
- **Current Playbooks:** `Core/operations/playbooks/fabric/1-source/`




