# Error Handling Implementation Plan

**Date:** 2025-12-08  
**Status:** 🎯 Ready to Execute  
**Purpose:** Step-by-step implementation of SPECTRA-grade error handling

---

## 📋 Implementation Steps

### Step 1: Extend Core SpectraError (If Accessible) OR Embed in SDK
**Location 1 (Preferred):** `Core/shared/python/spectra-core/src/spectra_core/errors.py`  
**Location 2 (Fallback):** `spectraSDK.Notebook/notebook_content.py` (if core not accessible)

**Changes:**
1. Extend `SpectraError` base class with structured fields (category, context, retryable, stage, source_system)
2. Update existing subclasses to accept structured fields via `**kwargs`
3. If SDK can't import from core, embed extended version in SDK notebook

### Step 2: Add Error Handling Helper Classes to SDK
**Location:** `spectraSDK.Notebook/notebook_content.py` (before `SourceStageHelpers`)

**Classes to Add:**
1. `ErrorClassification` - Error classification helper (returns SpectraError instances)
2. `APIRequestHandler` - Retry logic wrapper (uses SpectraError)
3. `ErrorCollector` - Error aggregation (collects SpectraError instances)

**Lines to Insert:** After line 2886 (before `SourceStageHelpers`)

---

### Step 2: Update SourceStageHelpers Methods
**Methods to Update:**
1. `validate_api_authentication()` - Use `APIRequestHandler`
2. `validate_api_resource_access()` - Use `APIRequestHandler`
3. `bootstrap_endpoints_catalog()` - Use `APIRequestHandler` (optional)
4. `execute_source_stage()` - Add error collection and graceful degradation

---

### Step 3: Implement Activity Logging
**Location:** `NotebookSession.record()` method

**What to Implement:**
- Write execution log to `Tables/log/sourcelog` Delta table
- Capture: timestamp, status, capabilities, errors, duration, context

---

### Step 4: Remove Preview Samples References
**Files to Update:**
1. `sourceZephyr.Notebook/notebook_content.py` - Remove preview parameter/execution
2. `contracts/source.contract.yaml` - Remove preview samples from outputs
3. `manifests/source.manifest.yaml` - Remove preview samples
4. `SourceStageHelpers.execute_source_stage()` - Remove preview logic

---

### Step 5: Update Contract
**File:** `contracts/source.contract.yaml`

**Changes:**
- Mark error handling as complete
- Remove preview samples requirement
- Add error handling to obligations

---

## ✅ Testing Checklist

- [ ] Test retry on transient failures (timeout, connection error)
- [ ] Test non-retryable errors (401, 403, 404)
- [ ] Test graceful degradation (continue with partial failures)
- [ ] Test activity logging (verify Delta table created)
- [ ] Test error classification (verify retryable vs non-retryable)
- [ ] Test error collection (verify errors aggregated)

---

**Version:** 1.0.0  
**Date:** 2025-12-08

