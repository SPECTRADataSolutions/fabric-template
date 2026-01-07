# Zephyr Source Notebook - Runtime Flags Reference
**Date:** 2025-12-02  
**Purpose:** Clear explanation of each runtime flag

---

## Runtime Flags

### 1. `debug_mode` (Default: False)

**What it does:**
- Shows verbose logging
- Displays DataFrames (`.show()`)
- Prints full stack traces on errors

**When to use:**
- Debugging issues
- Development
- Troubleshooting

**Example:**
```python
debug_mode = True
```

---

### 2. `test_endpoints` (Default: False) ✨ NEW

**What it does:**
- Runs comprehensive endpoint health check (Cell 5)
- Tests ALL 120 GET endpoints
- Takes ~60 seconds, ~120 API calls
- Writes to `Tables/source/endpoint_health`

**When to use:**
- First time setup (OR use init_mode)
- After API changes
- Monthly validation
- Documenting API surface

**Example:**
```python
test_endpoints = True  # Test all 120 endpoints
```

---

### 3. `extract_sample` (Default: False) ✨ NEW

**What it does:**
- Extracts complete sample dimensional database (Cell 7)
- 5 tables: dimProject, dimRelease, dimCycle, dimTestCase, factTestExecution
- Max 100 rows per table (265 total)
- Takes ~90 seconds, ~100 API calls
- Writes to `Tables/source/sample_*`

**When to use:**
- First time setup (OR use init_mode)
- Before starting Prepare stage
- Monthly sample refresh
- Testing schema changes

**Example:**
```python
extract_sample = True  # Extract sample database for Prepare stage
```

---

### 4. `init_mode` (Default: False)

**What it does:**
- **ENABLES ALL INITIALIZATION:**
  - Bootstraps endpoints (Cell 4)
  - test_endpoints = True (Cell 5)
  - extract_sample = True (Cell 7)
- Complete first-time setup
- Takes ~3-5 minutes, ~250 API calls

**When to use:**
- Very first run
- Complete rebuild
- Major reset

**Example:**
```python
init_mode = True  # Full initialization
```

**Equivalent to:**
```python
test_endpoints = True
extract_sample = True
# Plus forces endpoints bootstrap
```

---

### 5. `full_run_mode` (Default: False)

**What it does:**
- Currently unused (reserved for full pipeline execution in Extract stage)
- In Source stage: Same as normal mode

**When to use:**
- Reserved for future use (Extract/Transform/Load stages)

---

## Flag Combinations

### Fast Validation (Default - Every Run)

```python
# All flags False (default)
```

**Duration:** ~5 seconds  
**API Calls:** 5  
**Tests:** 4 hierarchical endpoints  
**Extracts:** Nothing  
**Use for:** Regular monitoring

---

### Test Endpoints Only

```python
test_endpoints = True
```

**Duration:** ~65 seconds (5s base + 60s testing)  
**API Calls:** ~125 (5 + 120)  
**Tests:** 120 GET endpoints  
**Extracts:** Nothing  
**Use for:** API validation without data extraction

---

### Extract Sample Only

```python
extract_sample = True
```

**Duration:** ~95 seconds (5s base + 90s extraction)  
**API Calls:** ~105 (5 + 100)  
**Tests:** 4 hierarchical endpoints  
**Extracts:** 5 tables, 265 rows  
**Use for:** Refresh sample database for Prepare stage

---

### Test + Extract

```python
test_endpoints = True
extract_sample = True
```

**Duration:** ~155 seconds (~2.5 minutes)  
**API Calls:** ~225  
**Tests:** 120 endpoints  
**Extracts:** 5 tables  
**Use for:** Comprehensive validation + sample database

---

### Full Initialization

```python
init_mode = True  # Automatically enables test_endpoints + extract_sample
```

**Duration:** ~3-5 minutes  
**API Calls:** ~250  
**Tests:** 120 endpoints  
**Extracts:** 5 tables  
**Bootstraps:** 228 endpoints  
**Use for:** First time setup

---

## What Runs When - Clear Matrix

| Cell | What | Normal | test_endpoints | extract_sample | init_mode |
|------|------|--------|----------------|----------------|-----------|
| Cell 3 | Project handshake | ✅ | ✅ | ✅ | ✅ |
| Cell 4 | Endpoints bootstrap | ⚠️ | ⚠️ | ⚠️ | ✅ |
| Cell 4a | Hierarchical validation (4 endpoints) | ✅ | ✅ | ✅ | ✅ |
| Cell 5 | Comprehensive health check (120 endpoints) | ❌ | ✅ | ❌ | ✅ |
| Cell 6 | Quality gate report | ✅ | ✅ | ✅ | ✅ |
| Cell 7 | Sample database extraction (5 tables) | ❌ | ❌ | ✅ | ✅ |

⚠️ = Only if table doesn't exist  
✅ = Always runs  
❌ = Skipped

---

## Recommended Usage Patterns

### Daily/Hourly Monitoring

```python
# Use defaults - fast health check
# Takes ~5 seconds
```

**Output:**
- Hierarchical validation ✅
- Quality gate status ✅
- Fast and efficient ✅

---

### First Time Setup

```python
init_mode = True
```

**Output:**
- Endpoints catalogued (228) ✅
- All 120 endpoints tested ✅
- Sample database extracted (5 tables) ✅
- Complete environment validation ✅

---

### Monthly API Validation

```python
test_endpoints = True  # Just test endpoints, don't extract
```

**Output:**
- Updated endpoint health check ✅
- Current API status documented ✅
- No data extraction (fast) ✅

---

### Before Starting Prepare Stage

```python
extract_sample = True  # Extract sample DB for schema design
```

**Output:**
- Complete sample database in Delta ✅
- Prepare stage has real data to design from ✅

---

### Comprehensive Deep Validation

```python
test_endpoints = True
extract_sample = True
```

**Output:**
- Complete endpoint testing ✅
- Fresh sample database ✅
- Full validation ✅

---

## Parameter Definition

### In Pipeline Configuration

```python
# Pipeline parameters (snake_case)
{
    "debug_mode": false,
    "test_endpoints": false,  # NEW - explicit endpoint testing
    "extract_sample": false,  # NEW - explicit sample extraction
    "init_mode": false,
    "full_run_mode": false
}
```

### In Variable Library

```
DXC_ZEPHYR_DEBUG_MODE=False
DXC_ZEPHYR_TEST_ENDPOINTS=False
DXC_ZEPHYR_EXTRACT_SAMPLE=False
DXC_ZEPHYR_INIT_MODE=False
DXC_ZEPHYR_FULL_RUN_MODE=False
```

---

## Benefits of Explicit Flags

### Before (Overloaded)

```python
init_mode = True  # Does EVERYTHING (bootstrap + test + extract)
full_run_mode = True  # Unclear what it does
```

**Problem:** Not granular, hard to control

### After (Explicit)

```python
test_endpoints = True  # Just test endpoints
extract_sample = True  # Just extract sample
init_mode = True  # Complete setup (enables both)
```

**Benefit:** Clear intent, fine-grained control ✅

---

## Decision Tree

```
First time running?
  └─ YES → init_mode=True
  └─ NO → Continue...

Need to validate API?
  └─ YES → test_endpoints=True
  └─ NO → Continue...

Need sample data for Prepare stage?
  └─ YES → extract_sample=True
  └─ NO → Continue...

Just monitoring?
  └─ YES → Use defaults (normal mode)
```

---

## Summary

### NEW Flags

1. ✅ **test_endpoints** - Controls Cell 5 (comprehensive endpoint testing)
2. ✅ **extract_sample** - Controls Cell 7 (sample database extraction)

### Logic

```python
# Cell 5 runs if:
if test_endpoints or init_mode:
    # Test ALL 120 endpoints

# Cell 7 runs if:
if extract_sample or init_mode:
    # Extract 5 sample tables
```

### Benefits

- ✅ **Explicit intent** - Clear what each flag does
- ✅ **Fine-grained control** - Test without extracting, or vice versa
- ✅ **init_mode convenience** - Still enables everything for first run
- ✅ **Performance** - Normal runs stay fast (5 seconds)

---

**Status:** ✅ Implemented - Notebook now has explicit test_endpoints and extract_sample flags!

---

*Created: 2025-12-02 21:35 GMT*  
*Runtime flags now explicit and granular*

