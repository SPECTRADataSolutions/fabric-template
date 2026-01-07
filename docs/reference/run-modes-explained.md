# Zephyr Source Notebook - Run Modes Explained
**Date:** 2025-12-02  
**Purpose:** Clear explanation of what runs when

---

## Quick Reference

| Mode | Duration | API Calls | When to Use |
|------|----------|-----------|-------------|
| **Normal** (default) | ~5 seconds | 5 | Regular monitoring |
| **init_mode=True** | ~3-5 minutes | ~250 | First time setup |
| **full_run_mode=True** | ~3-5 minutes | ~250 | Periodic refresh |

---

## Mode 1: Normal Run (Default)

**Parameters:**
```python
init_mode = False  # default
full_run_mode = False  # default
```

### What Runs (FAST - Every Time)

| Cell | What It Does | API Calls | Duration |
|------|--------------|-----------|----------|
| Cell 3 | Test `/project` endpoint | 1 | ~1s |
| Cell 4 | Check if endpoints table exists (read only) | 0 | ~1s |
| Cell 4a | Test hierarchical chain (4 endpoints) | 4 | ~2s |
| Cell 5 | **SKIP** comprehensive health check | 0 | ~0s |
| Cell 6 | Quality gate (based on Cell 4a) | 0 | ~1s |
| Cell 7 | **SKIP** sample extraction | 0 | ~0s |

**Total:** ~5 seconds, 5 API calls ✅

### What It Validates

✅ Authentication works  
✅ Projects accessible  
✅ Hierarchical access works (Projects → Releases → Cycles → Executions)  
✅ Environment healthy

### What It Writes to Delta

- `Tables/source/hierarchical_validation` (updated)
- `Tables/source/quality_gate_report` (updated)
- `Tables/log/_sourcelog` (audit log)

### When to Use

- ✅ Regular scheduled runs
- ✅ Quick health checks
- ✅ Monitoring dashboards
- ✅ CI/CD pipelines

---

## Mode 2: init_mode=True (First Time Setup)

**Parameters:**
```python
init_mode = True
```

### What Runs (COMPREHENSIVE - One Time)

| Cell | What It Does | API Calls | Duration |
|------|--------------|-----------|----------|
| Cell 3 | Test `/project` endpoint | 1 | ~1s |
| Cell 4 | **Bootstrap 228 endpoints** to Delta | 0 | ~1s |
| Cell 4a | Test hierarchical chain | 4 | ~2s |
| Cell 5 | **Test ALL 120 GET endpoints** | ~120 | ~60s |
| Cell 6 | Comprehensive quality gate | 0 | ~1s |
| Cell 7 | **Extract complete sample database** | ~50-100 | ~90s |

**Total:** ~3-5 minutes, ~250 API calls

### What It Validates

✅ All 228 endpoints catalogued  
✅ All 120 GET endpoints tested  
✅ 84 working endpoints documented  
✅ Hierarchical access proven  
✅ Complete sample database extracted  
✅ Foreign key integrity validated

### What It Writes to Delta

- `Tables/source/endpoints` (228 endpoints) ← **init_mode only**
- `Tables/source/hierarchical_validation`
- `Tables/source/endpoint_health` (120 endpoints) ← **init_mode only**
- `Tables/source/quality_gate_report`
- `Tables/source/sample_dimProject` (37 rows) ← **init_mode only**
- `Tables/source/sample_dimRelease` (44 rows) ← **init_mode only**
- `Tables/source/sample_dimCycle` (84 rows) ← **init_mode only**
- `Tables/source/sample_dimTestCase` (10 rows) ← **init_mode only**
- `Tables/source/sample_factTestExecution` (100 rows) ← **init_mode only**
- `Tables/log/_sourcelog`

**Total:** 10 Delta tables

### When to Use

- ✅ First time running the notebook
- ✅ After major API changes
- ✅ After credential rotation
- ✅ To regenerate sample database
- ✅ To refresh endpoint catalog

---

## Mode 3: full_run_mode=True (Periodic Refresh)

**Parameters:**
```python
full_run_mode = True
```

### What Runs (Same as init_mode)

Exactly the same as init_mode **except**:
- Won't force re-bootstrap endpoints if table already exists
- Otherwise identical behavior

**Total:** ~3-5 minutes, ~250 API calls

### When to Use

- ✅ Monthly/quarterly API validation
- ✅ Refresh sample database with latest data
- ✅ Update endpoint health check results
- ✅ Periodic deep validation

---

## What Should ONLY Happen in init_mode?

### Answer: 3 Things

**1. Endpoints Bootstrap** (Cell 4)
- **Only if:** Table doesn't exist OR init_mode=True
- **What:** Load 228 endpoints to Delta
- **Why:** One-time catalog, doesn't change

**2. Comprehensive Endpoint Health Check** (Cell 5)
- **Only if:** init_mode=True OR full_run_mode=True
- **What:** Test ALL 120 GET endpoints
- **Why:** Expensive (120 API calls, 60 seconds)

**3. Sample Database Extraction** (Cell 7)
- **Only if:** init_mode=True OR full_run_mode=True
- **What:** Extract 5 dimensional tables (265 rows)
- **Why:** Expensive (~100 API calls, 90 seconds)

---

## Performance Comparison

### Normal Run (Every Hour)

```
Duration: ~5 seconds
API Calls: 5
Cost: Minimal
Validates: Basic connectivity + hierarchy
```

**Perfect for:** Monitoring, scheduled runs, quick checks

### init_mode / full_run_mode (Monthly)

```
Duration: ~3-5 minutes
API Calls: ~250
Cost: Higher
Validates: Everything + extracts sample data
```

**Perfect for:** Setup, deep validation, sample refresh

---

## What Prepare Stage Gets

### From Normal Runs

- Current health status
- Hierarchical validation results
- Quality gate status

### From init_mode / full_run_mode

**Plus:**
- Complete endpoint catalog (228 endpoints)
- Comprehensive health check (84/120 working)
- **Complete sample dimensional database in Delta** ✅
  - dimProject (37 rows)
  - dimRelease (44 rows)
  - dimCycle (84 rows)
  - dimTestCase (10 rows)
  - factTestExecution (100 rows)

**Prepare can immediately:**
```python
# Read real data structures
df = spark.read.format("delta").load("Tables/source/sample_dimProject")
df.printSchema()  # See actual schema
df.show(10)  # See actual data

# Design transformations on real data!
```

---

## Recommendations

### Regular Operation (Hourly/Daily)

```python
# Just run with defaults - fast validation
init_mode = False
full_run_mode = False
# Takes ~5 seconds
```

### First Time Setup

```python
# Run with init_mode to bootstrap everything
init_mode = True
# Takes ~3-5 minutes
# Extracts sample database for Prepare stage
```

### Periodic Deep Validation (Monthly)

```python
# Run with full_run_mode to refresh
full_run_mode = True
# Takes ~3-5 minutes
# Updates sample database with latest data
```

---

## Summary

### What ONLY runs in init_mode or full_run_mode:

1. ✅ **Cell 4:** Endpoints bootstrap (only if needed)
2. ✅ **Cell 5:** Comprehensive health check (120 endpoints) ← **Now conditional!**
3. ✅ **Cell 7:** Sample database extraction (5 tables) ← **Already conditional**

### What ALWAYS runs:

1. ✅ **Cell 3:** Project handshake (fast fail)
2. ✅ **Cell 4a:** Hierarchical validation (4 endpoints, fast)
3. ✅ **Cell 6:** Quality gate report (show readiness)

**Result:**
- Normal runs: **Fast** (~5 seconds)
- init/full runs: **Comprehensive** (~3-5 minutes)

---

*Updated: 2025-12-02 21:30 GMT*  
*Cell 5 now properly conditional - only runs in init_mode or full_run_mode*

