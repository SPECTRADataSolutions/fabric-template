# SPECTRA-Grade Governance Clarifications
**Date:** 2025-01-29  
**Status:** 🟢 Active Standards  
**Purpose:** Define SPECTRA-grade standards for version pinning, ownership, and audit logging

---

## 1. Framework Version Pinning

### SPECTRA Standard

**YES, we should pin framework versions** for reproducibility and deterministic builds.

### Implementation

- **Contract Field:** `artifacts.environment.version` (NOT "frameworkVersion" - simpler is better)
- **Format:** Semantic versioning (e.g., `2.0.0`, `>=2.0.0,<3.0.0`)
- **Source:** Read from `pyproject.toml` in Fabric SDK repo
- **Update Strategy:** 
  - Pin to specific version for stability (e.g., `2.0.0`)
  - Or use compatible version range (e.g., `>=2.0.0,<3.0.0`)
  - Update during Source stage setup when deploying environment

### Rationale

- **Deterministic builds** - Same version = same behavior
- **Reproducibility** - Can replay exact pipeline state
- **Risk management** - Avoid unexpected breaking changes
- **SPECTRA principle** - "deterministic, structured, version-controlled"

### Current State

- **Fabric SDK Version:** `2.0.0` (per `pyproject.toml`)
- **Contract:** Not yet specified
- **Action:** Add `version` to contract during Source stage setup

---

## 2. Owner Field Definition

### SPECTRA Standard

The `owner` field in governance represents **the accountable party** - who is responsible for:
- **Business decisions** - Approving changes, scope, priorities
- **Technical decisions** - Architecture, methodology compliance
- **Point of contact** - Who to ask questions, escalate issues
- **Authority** - Who can approve deviations, exceptions

### Implementation

- **Format:** Organization name or individual name
- **Examples:**
  - `"SPECTRA Data Solutions"` - Organization-level ownership
  - `"Mark Maconnachie (SPECTRA)"` - Individual with context
  - `"SPECTRA Data Solutions - Zephyr Team"` - Team-level
- **Best Practice:** Include context (organization/team) for clarity

### For Zephyr

**Recommended:** `"SPECTRA Data Solutions"` (current value is correct)

**Rationale:**
- SPECTRA is the service provider/contractor
- Mark is the implementer, but SPECTRA is the accountable entity
- Matches contract structure (SPECTRA provides service to Velenetic)

### SPECTRA Principle

- **Accountability** - Clear ownership = clear responsibility
- **Governance** - Owner gates decisions and exceptions
- **Legacy** - Future teams know who to contact

---

## 3. Audit Logging - What Are "Runs"?

### SPECTRA Standard

**"Runs" = Pipeline Executions**

Each time a pipeline executes (scheduled or manual), it's a "run" that should be logged.

### What Gets Logged

1. **Pipeline Execution Metadata**
   - Run ID (unique identifier)
   - Start time / end time
   - Status (Success, Failed, Cancelled)
   - Trigger (scheduled, manual, API)
   - Duration

2. **Stage-Level Activity**
   - Each stage (Source, Prepare, Extract, etc.) logs to Delta tables
   - Location: `Tables/log/_<stage>log` (e.g., `Tables/log/_sourcelog`)
   - Fields: stage, status, loggedAt, entityName, rowCount, duration, etc.

### SPECTRA Implementation

**Delta Tables Only** - All logging stays within Fabric workspace:

- `Tables/log/_sourcelog` - Source stage activity
- `Tables/log/_extractlog` - Extract stage activity
- `Tables/log/_cleanlog` - Clean stage activity
- etc.

**Key Principle:** 
- **All Zephyr data stays in Fabric workspace** - no external logging
- Delta tables provide both machine-readable and queryable audit trail
- No chronicle/journal entries outside workspace
- Fabric workspace is the single source of truth for all Zephyr pipeline data

### Current Contract Value

```yaml
auditLog: "Core/memory chronicle entry per run"
```

**This is INCORRECT for Zephyr** - should be Delta tables only.

### SPECTRA Principle

- **Audit Transparency** - Comprehensive audit trails for compliance
- **Deterministic** - Every run is logged, traceable, replayable
- **Legacy** - Future teams can understand what happened

---

## Summary: SPECTRA-Grade Answers

### Q1: Framework Version Pinning?

**Answer:** ✅ YES - Pin to specific version (e.g., `2.0.0`) in contract
- **Field:** `artifacts.environment.version` (NOT "frameworkVersion" - simpler is better)
- **Value:** `"2.0.0"` (current Fabric SDK version)
- **Update:** During Source stage environment setup

### Q2: Owner Field?

**Answer:** ✅ Current value is correct - `"SPECTRA Data Solutions"`
- **Represents:** Accountable party (business + technical decisions)
- **Context:** SPECTRA is service provider, accountable to Velenetic
- **No change needed**

### Q3: Audit Logging - What Are "Runs"?

**Answer:** ❌ Current value is INCORRECT - should be Delta tables only
- **"Runs"** = Each pipeline execution (scheduled or manual)
- **SPECTRA Principle:** All Zephyr data stays in Fabric workspace
- **Implementation:** 
  - Delta tables only (`Tables/log/_<stage>log`)
  - NO chronicle/journal entries outside workspace
  - Fabric workspace is single source of truth
- **Correct Value:** `"Delta tables in Fabric workspace (Tables/log/_<stage>log)"`
- **Action:** Update contract to reflect Delta-only logging

---

## Next Steps

1. **Add `version` to contract** during Source stage setup (NOT "frameworkVersion")
2. **Keep `owner` as is** - "SPECTRA Data Solutions"
3. **Update `auditLog`** - Change to Delta tables only (no external chronicle/journal)
4. **Implement logging** in Source notebook to write to Delta tables only (`Tables/log/_sourcelog`)

---

**Last Updated:** 2025-01-29

