# Source Notebook Run Modes
**File:** `sourceZephyr.Notebook/notebook_content.py`  
**Purpose:** Define what runs in each mode

---

## Run Modes

### 1. **Normal Mode** (Default - Fast Validation)
**Duration:** ~5 seconds  
**API Calls:** ~5  
**Purpose:** Regular health check - verify environment still working

### 2. **init_mode** (First Time Setup + Comprehensive Validation)
**Duration:** ~3-5 minutes  
**API Calls:** ~200-250  
**Purpose:** Bootstrap system + comprehensive validation + sample extraction

### 3. **full_run_mode** (Periodic Deep Validation)
**Duration:** ~3-5 minutes  
**API Calls:** ~200-250  
**Purpose:** Refresh comprehensive validation + update sample database

---

## What Runs When

### EVERY Run (Normal Mode)

| Cell | What | Duration | API Calls | Why Every Time |
|------|------|----------|-----------|----------------|
| Cell 3 | Project handshake | ~1s | 1 | Fast fail if connectivity broken |
| Cell 4 | Endpoints check | ~1s | 0 | Check if table exists (reads only) |
| Cell 4a | Hierarchical validation | ~2s | 4 | Prove hierarchy still works |
| Cell 6 | Quality gate report | ~1s | 0 | Show current readiness |

**Total:** ~5 seconds, 5 API calls ✅

**Purpose:** Fast validation that environment is healthy

---

### init_mode OR full_run_mode ONLY

| Cell | What | Duration | API Calls | Why Conditional |
|------|------|----------|-----------|-----------------|
| Cell 4 | Endpoints bootstrap | ~1s | 0 | Only if table missing or force init |
| Cell 5 | Comprehensive health check | ~60s | ~120 | **Expensive - tests ALL 120 endpoints** |
| Cell 7 | Sample database extraction | ~90s | ~50-100 | **Expensive - extracts complete dataset** |

**Total:** ~150 seconds, ~200 API calls

**Purpose:** One-time setup or periodic refresh

---

## Detailed Cell Logic

### Cell 3: Project Handshake
```python
# ALWAYS RUNS
r = session.get(f"{base_url}/project")
if r.status_code != 200:
    raise RuntimeError("Auth failed")
```

**Why:** Fast fail if basic connectivity broken

---

### Cell 4: Endpoints Bootstrap
```python
# CONDITIONAL: Only if table doesn't exist OR init_mode
should_bootstrap = init_mode

if not should_bootstrap:
    try:
        # Try to read existing table
        df = spark.read.format("delta").load("Tables/source/endpoints")
        # Table exists, don't bootstrap
    except:
        # Table doesn't exist, must bootstrap
        should_bootstrap = True

if should_bootstrap:
    # Bootstrap 228 endpoints to Delta
    # This is ONE-TIME (or force with init_mode)
```

**Why:** Endpoints don't change often, only load once

---

### Cell 4a: Hierarchical Validation
```python
# ALWAYS RUNS (fast - only 4 endpoints)
# Test: Projects → Releases → Cycles → Executions
```

**Why:** Fast proof that hierarchy still works (4 API calls, ~2 seconds)

---

### Cell 5: Comprehensive Endpoint Health Check
```python
# SHOULD BE CONDITIONAL - Currently runs every time!
# TODO: Wrap in if statement

if init_mode or full_run_mode:
    # Test ALL 120 GET endpoints
    # Takes ~60 seconds, 120 API calls
    # Writes to Tables/source/endpoint_health
else:
    # Skip - read previous results if needed
    log.info("Skipping comprehensive health check (not in init/full run mode)")
```

**Why:** Expensive (120 API calls), results don't change often

**Current Status:** ⚠️ **NEEDS UPDATE** - currently runs every time!

---

### Cell 6: Quality Gate Report
```python
# ALWAYS RUNS
if health_check_results:
    # Generate report from Cell 5 results
else:
    # Generate report from Cell 4a hierarchical validation only
    # Simpler report but still valid
```

**Why:** Always show current readiness status

---

### Cell 7: Sample Database Extraction
```python
# CONDITIONAL - Already correct!
if full_run_mode or init_mode:
    # Extract complete sample dimensional database
    # 5 tables, 265 rows, ~50-100 API calls
    # Writes to Tables/source/sample_*
else:
    log.info("Skipping sample extraction (not in init/full run mode)")
```

**Why:** Expensive, sample data doesn't change often ✅

---

## Recommended Updates

### Cell 5 Needs Conditional Logic

**Current (WRONG):**
```python
# Cell 5: Always runs comprehensive health check
log.info("Starting endpoint health check...")
# Tests 120 endpoints every time
```

**Should Be:**
```python
# Cell 5: Conditional comprehensive health check
COMPREHENSIVE_HEALTH_CHECK_ENABLED = init_mode or full_run_mode

if COMPREHENSIVE_HEALTH_CHECK_ENABLED:
    log.info("Starting comprehensive endpoint health check (120 endpoints)...")
    # Test ALL 120 endpoints
    # Write to Tables/source/endpoint_health
else:
    log.info("Skipping comprehensive health check (not in init/full run mode)")
    log.info("Using hierarchical validation results for quality gate")
    # Quality gate will use Cell 4a results only
```

---

## Run Mode Comparison

### Normal Run (Default)

**Cells that run:**
- Cell 1-2: Parameters ✅
- Cell 3: Project handshake ✅
- Cell 4: Check endpoints table (read only) ✅
- Cell 4a: Hierarchical validation (4 endpoints) ✅
- Cell 5: **SKIP** comprehensive health check
- Cell 6: Quality gate (based on Cell 4a only) ✅
- Cell 7: **SKIP** sample extraction

**Duration:** ~5 seconds  
**API Calls:** 5  
**Purpose:** Quick validation

---

### init_mode=True (First Time Setup)

**Cells that run:**
- Cell 1-2: Parameters ✅
- Cell 3: Project handshake ✅
- Cell 4: **Bootstrap 228 endpoints** ✅
- Cell 4a: Hierarchical validation ✅
- Cell 5: **Comprehensive health check (120 endpoints)** ✅
- Cell 6: Quality gate (comprehensive) ✅
- Cell 7: **Sample database extraction (5 tables)** ✅

**Duration:** ~3-5 minutes  
**API Calls:** ~200-250  
**Purpose:** Complete setup + validation

---

### full_run_mode=True (Periodic Refresh)

**Same as init_mode** but doesn't force re-bootstrap if table exists

**Duration:** ~3-5 minutes  
**API Calls:** ~200-250  
**Purpose:** Refresh validation + sample data

---

## Recommendation

### Update Cell 5 to be Conditional

```python
# Add at start of Cell 5:
COMPREHENSIVE_HEALTH_CHECK_ENABLED = init_mode or full_run_mode

if not COMPREHENSIVE_HEALTH_CHECK_ENABLED:
    log.info("=" * 60)
    log.info("Comprehensive Endpoint Health Check - SKIPPED")
    log.info("=" * 60)
    log.info("Not in init_mode or full_run_mode - using hierarchical validation only")
    log.info("Set full_run_mode=True to run comprehensive endpoint health check")
    log.info("=" * 60)
    health_check_results = []  # Empty - will use hierarchical results
    
else:
    log.info("=" * 60)
    log.info("Comprehensive Endpoint Health Check - ALL 120 ENDPOINTS")
    log.info("=" * 60)
    # ... existing health check code ...
```

**Then update Cell 6 to handle both scenarios:**
```python
# If we have comprehensive health check results, use them
# Otherwise, use hierarchical validation for quality gate
```

---

## Summary

### What Should ONLY Run in init_mode?

1. ✅ **Endpoints bootstrap** (Cell 4) - Only if table missing or init_mode
2. ✅ **Comprehensive health check** (Cell 5) - **NEEDS UPDATE** to be conditional
3. ✅ **Sample database extraction** (Cell 7) - Already conditional

### What Should Run EVERY Time?

1. ✅ Project handshake (Cell 3) - Fast fail
2. ✅ Hierarchical validation (Cell 4a) - Fast proof (4 endpoints)
3. ✅ Quality gate report (Cell 6) - Show readiness

### Benefits

**Normal run:** Fast (~5 seconds) for regular monitoring  
**init_mode/full_run_mode:** Comprehensive (~3-5 min) for deep validation

**Should I update Cell 5 to be conditional?**

---

*Analysis: 2025-12-02 21:20 GMT*

