# Source Stage Playbook Coverage Analysis

**Date:** 2025-12-08  
**Status:** 🔍 Analysis Complete  
**Purpose:** Identify missing playbooks for complete source stage coverage

---

## 📊 Current Playbooks (3)

### ✅ Existing Playbooks

1. **`source.001-createSourceNotebook.md`**
   - **Purpose:** Create Source notebook artifact in Fabric
   - **Covers:** Notebook creation via CLI/UI, Git sync, pipeline wiring
   - **Status:** ✅ Complete

2. **`source.002-addNotebookToPipeline.md`**
   - **Purpose:** Attach Source notebook to pipeline
   - **Covers:** ID capture, pipeline activity configuration, variable binding
   - **Status:** ✅ Complete

3. **`source.003-bootstrapEndpoints.md`**
   - **Purpose:** Bootstrap endpoints catalog (init_mode)
   - **Covers:** Endpoints module generation, bootstrap to Files area, populate Delta table
   - **Status:** ✅ Complete

---

## ❌ Missing Playbooks (Critical Gaps)

### 4. **`source.004-executeSourceStage.md`** ⚠️ **MISSING**

**Purpose:** Execute the Source stage notebook and verify successful completion.

**What It Should Cover:**
- Running source stage notebook in Fabric (interactive or pipeline mode)
- Verifying execution completes without errors
- Checking Delta tables are created
- Verifying all contract obligations are met
- Capturing execution evidence (logs, outputs, metrics)

**Why It's Needed:**
- Playbooks 001-003 are setup/configuration
- No playbook covers **actual execution** of the source stage
- Execution is a critical step that needs documentation

**Content Should Include:**
- How to run notebook (interactive vs pipeline)
- Parameter configuration (bootstrap, backfill, preview, test)
- Expected execution time
- What success looks like (logs, table creation)
- Troubleshooting common execution errors

---

### 5. **`source.005-validateSourceStage.md`** ⚠️ **MISSING** (Critical)

**Purpose:** Quality gates and validation for Source stage outputs.

**What It Should Cover:**
- Contract compliance verification
- Delta table validation (existence, schema, row counts)
- Data quality checks (nulls, duplicates, required fields)
- Authentication verification
- Hierarchical access validation completeness
- Endpoint catalog completeness (228 endpoints)
- Preview samples validation (all 5 hierarchy levels)
- Activity logging verification
- Discord notification verification

**Why It's Needed:**
- Source stage contract has explicit obligations that must be verified
- Quality gates ensure SPECTRA-grade outputs
- Validates handoff readiness for Prepare stage
- Catches issues before downstream stages

**Based on Contract Requirements:**
- ✅ Auth succeeds
- ✅ Hierarchical access validated (all 5 levels)
- ✅ Endpoint catalog comprehensive (228)
- ✅ Dynamic project discovery
- ✅ Preview samples (all hierarchy levels)
- ✅ Portfolio, config, credentials, endpoints tables exist
- ✅ Test coverage >75%
- ✅ Data validation functions used

**Content Should Include:**
- SQL queries to verify table existence and row counts
- Schema validation checks
- Contract compliance checklist
- Quality gate pass/fail criteria
- Automated validation script/notebook

---

### 6. **`source.006-sourceStageHandoff.md`** ⚠️ **MISSING** (Critical)

**Purpose:** Prepare and document handoff from Source to Prepare stage.

**What It Should Cover:**
- Source stage completion verification
- Required outputs for Prepare stage
- Dependencies Prepare stage needs (portfolio, endpoints, samples)
- Handoff checklist (all tables exist, validated, documented)
- Prepare stage prerequisites
- Communication/notification of completion
- Documentation of any known issues or limitations

**Why It's Needed:**
- Clear handoff prevents downstream stage blockers
- Documents what Prepare stage can rely on
- Captures completion evidence
- Enables autonomous Prepare stage execution

**Content Should Include:**
- Handoff checklist (all outputs verified)
- Prepare stage dependencies list
- Known issues/limitations document
- Completion evidence capture
- Next steps for Prepare stage

---

## 🤔 Optional/Enhancement Playbooks

### 7. **`source.007-troubleshootSourceStage.md`** (Optional)

**Purpose:** Common troubleshooting scenarios and solutions.

**What It Should Cover:**
- Authentication failures
- API rate limiting
- Missing endpoints
- Delta table creation failures
- Preview sample extraction failures
- Pipeline execution errors

**Why It Might Be Useful:**
- Reduces support burden
- Standardises troubleshooting approach
- Documents known issues and fixes

---

## 📋 SPECTRA Methodology Alignment

**Source Stage Responsibilities (7-Stage Pattern):**

1. **Parameters** → Covered by `source.001` (notebook creation includes parameter setup)
2. **Context** → Covered by `source.002` (pipeline wiring provides context)
3. **Initialize** → Missing - could be part of `source.004` (execution)
4. **Execute** → **Missing - `source.004-executeSourceStage.md`**
5. **Validate** → **Missing - `source.005-validateSourceStage.md`**
6. **Record** → Partially covered (activity logging exists but no playbook)
7. **Finalise** → **Missing - `source.006-sourceStageHandoff.md`**

---

## 🎯 Priority Ranking

### 🔴 **Critical (Must Have)**

1. **`source.005-validateSourceStage.md`** - Quality gates are essential for SPECTRA-grade
2. **`source.006-sourceStageHandoff.md`** - Clear handoff prevents downstream blockers

### 🟡 **High Priority (Should Have)**

3. **`source.004-executeSourceStage.md`** - Execution is a core stage responsibility

### 🟢 **Nice to Have**

4. **`source.007-troubleshootSourceStage.md`** - Useful but not blocking

---

## 📊 Coverage Summary

| Category | Count | Status |
|----------|-------|--------|
| **Setup/Configuration** | 3 | ✅ Complete |
| **Execution** | 0 | ❌ Missing |
| **Validation/Quality Gates** | 0 | ❌ Missing |
| **Handoff** | 0 | ❌ Missing |
| **Troubleshooting** | 0 | ⚠️ Optional |
| **Total** | 3/6 required | ⚠️ 50% coverage |

---

## 🎯 Recommended Action Plan

### Phase 1: Critical Playbooks (Immediate)

1. **Create `source.005-validateSourceStage.md`**
   - Quality gates for contract compliance
   - Delta table validation
   - SQL queries for verification
   - Automated validation approach

2. **Create `source.006-sourceStageHandoff.md`**
   - Handoff checklist
   - Prepare stage dependencies
   - Completion evidence

### Phase 2: Execution Playbook

3. **Create `source.004-executeSourceStage.md`**
   - How to run source stage
   - Parameter configuration
   - Success criteria
   - Execution evidence

### Phase 3: Enhancement (Optional)

4. **Create `source.007-troubleshootSourceStage.md`**
   - Common issues and fixes
   - Debugging approaches

---

## 📚 Reference Materials

**Contract Requirements:**
- `contracts/source.contract.yaml` - Source stage obligations
- `docs/SOURCE-STAGE-CONTRACT-AUDIT.md` - Contract compliance audit
- `docs/SOURCE-STAGE-BASELINE-PLAN.md` - Implementation plan

**Existing Playbooks:**
- `Core/operations/playbooks/fabric/1-source/source.001-createSourceNotebook.md`
- `Core/operations/playbooks/fabric/1-source/source.002-addNotebookToPipeline.md`
- `Core/operations/playbooks/fabric/1-source/source.003-bootstrapEndpoints.md`

**SDK Features:**
- `SourceStageValidation` class - Comprehensive table validation
- `DataValidation` class - Data quality checks
- `SourceStageHelpers` - Helper methods for validation

---

**Version:** 1.0.0  
**Status:** 🟢 Analysis Complete  
**Next Step:** Create missing playbooks starting with `source.005-validateSourceStage.md`

