# SPECTRA-Grade Runtime Flags Design
**Date:** 2025-12-02  
**Purpose:** Define proper flag system for Source stage

---

## Design Principles

### SPECTRA-Grade Flags Should Be:

1. **Explicit** - Clear what they do
2. **Independent** - Each flag has one purpose
3. **Composable** - Flags combine logically
4. **Safe** - Default to safe/fast mode
5. **Idempotent** - Safe to run multiple times

---

## Proposed Flag System

### Core Execution Flags

#### 1. `init_mode` (Default: False)

**Purpose:** Complete first-time initialization

**What it does:**
- Bootstrap endpoints catalog (228 endpoints)
- Run comprehensive endpoint validation (120 tests)
- Extract sample dimensional database (5 tables)
- Validate hierarchical access
- Generate quality gate report
- **Everything needed for first run**

**When to use:**
- First time running the notebook
- Complete rebuild after major changes
- System reset/re-initialization

**Semantic:** "Initialize everything from scratch"

**Sets internally:**
```python
if init_mode:
    test_endpoints = True
    extract_sample = True
    force_refresh = True
```

---

#### 2. `validate_only` (Default: False) ✨ NEW

**Purpose:** Run all validation without data extraction

**What it does:**
- Test hierarchical access (4 endpoints)
- Optionally test all 120 endpoints if needed
- Generate quality gate report
- **No data extraction** (validation only)

**When to use:**
- Quick API health check
- Validate after credential rotation
- Pre-flight check before extraction
- Monthly API validation

**Semantic:** "Validate environment, don't extract data"

---

#### 3. `extract_sample` (Default: False)

**Purpose:** Extract sample dimensional database for Prepare stage

**What it does:**
- Extract dimProject (37 rows)
- Extract dimRelease (44 rows)
- Extract dimCycle (84 rows)
- Extract dimTestCase (10 rows)
- Extract factTestExecution (100 rows)
- Write all to `Tables/source/sample_*`

**When to use:**
- Before starting Prepare stage
- Refresh sample data monthly
- After significant data changes in Zephyr
- Provide real data structures for schema design

**Semantic:** "Build sample dimensional database"

---

#### 4. `full_run` (Default: False) - RENAME from full_run_mode

**Purpose:** Complete validation + extraction (not initialization)

**What it does:**
- Validate environment (hierarchical + comprehensive)
- Extract sample database
- Update all validation tables
- **Doesn't force re-bootstrap** (unlike init_mode)

**When to use:**
- Periodic comprehensive runs
- Monthly deep validation
- Refresh all artifacts

**Semantic:** "Do everything (validate + extract)"

**Sets internally:**
```python
if full_run:
    validate_only = True
    extract_sample = True
```

---

### Control/Modifier Flags

#### 5. `debug_mode` (Default: False)

**Purpose:** Enhanced diagnostics and logging

**What it does:**
- Verbose logging (every step)
- Display DataFrames (`.show()`)
- Print full stack traces
- Don't fail fast (capture all errors)
- Write additional diagnostic outputs

**When to use:**
- Troubleshooting failures
- Development/testing
- Understanding data structures
- Diagnosing API issues

**Semantic:** "Show me everything"

---

#### 6. `dry_run` (Default: False) ✨ NEW

**Purpose:** Preview without writing to Delta

**What it does:**
- Run all validations
- Extract data to memory
- **Don't write to Delta tables**
- Log what would be written
- Preview mode

**When to use:**
- Testing changes
- Verifying extraction logic
- Cost estimation
- Preview before commit

**Semantic:** "Show me what would happen"

---

#### 7. `force_refresh` (Default: False) ✨ NEW

**Purpose:** Force re-extraction even if data exists

**What it does:**
- Ignore existing Delta tables
- Re-extract everything
- Overwrite all outputs
- Force comprehensive validation

**When to use:**
- Data quality issues detected
- Suspect stale data
- After API changes
- Periodic full refresh

**Semantic:** "Don't trust existing data, refresh everything"

---

### Scope Control Flags

#### 8. `test_all_endpoints` (RENAME from test_endpoints)

**Purpose:** Test all 120 GET endpoints comprehensively

**What it does:**
- Run Cell 5 (comprehensive health check)
- Test every GET endpoint
- Document which work/fail
- Write to `Tables/source/endpoint_health`

**When to use:**
- First run (via init_mode)
- Monthly API validation
- After Zephyr upgrades
- Documenting API surface

**Semantic:** "Test every single endpoint"

---

#### 9. `max_sample_rows` (Default: 100) ✨ NEW

**Purpose:** Control sample database size

**What it does:**
- Limits rows per table during extraction
- Default: 100 rows per table
- Can increase for larger samples
- Controls extraction scope

**When to use:**
- Default (100 rows) for schema design
- Larger (500 rows) for data profiling
- Smaller (10 rows) for quick tests

**Semantic:** "How much sample data to extract"

**Example:**
```python
max_sample_rows = 500  # Extract 500 rows per table
```

---

## Recommended Flag System

### Final Proposed Flags (8 total)

```python
# Core Execution (what to do)
init_mode = False           # Complete initialization (enables all)
validate_only = False       # Validate without extraction
extract_sample = False      # Extract sample dimensional database
full_run = False            # Validate + extract (no bootstrap)

# Control/Modifiers (how to do it)
debug_mode = False          # Enhanced diagnostics
dry_run = False             # Preview mode (no writes)
force_refresh = False       # Ignore existing data

# Scope Control
test_all_endpoints = False  # Test 120 endpoints (vs just 4 hierarchical)
max_sample_rows = 100       # Rows per table in sample
```

---

## Flag Semantics & Relationships

### Hierarchy

```
init_mode
  ├── force_refresh = True (implicit)
  ├── test_all_endpoints = True (implicit)
  └── extract_sample = True (implicit)

full_run
  ├── validate_only = True (implicit)
  └── extract_sample = True (implicit)

validate_only
  └── test_all_endpoints = True (implicit)
```

### Modifiers Apply to All

```python
if dry_run:
    # Run everything but don't write to Delta
    
if debug_mode:
    # Add verbose logging to whatever runs
    
if force_refresh:
    # Ignore existing data in whatever runs
```

---

## Usage Examples

### Example 1: First Time Setup

```python
init_mode = True
# Implicitly sets: test_all_endpoints=True, extract_sample=True, force_refresh=True
# Duration: ~3-5 minutes
# Result: Complete initialization
```

### Example 2: Quick Debug

```python
debug_mode = True
# Normal run with verbose logging
# Duration: ~5 seconds
# Result: See exactly what's happening
```

### Example 3: Test API Changes

```python
test_all_endpoints = True
debug_mode = True
# Test all 120 endpoints with verbose logging
# Duration: ~65 seconds
# Result: Updated endpoint health check with diagnostics
```

### Example 4: Refresh Sample for Prepare

```python
extract_sample = True
max_sample_rows = 500  # Larger sample
# Extract bigger sample database
# Duration: ~2 minutes
# Result: 5 tables with 500 rows each
```

### Example 5: Preview Extraction

```python
extract_sample = True
dry_run = True
# Test extraction logic without writing
# Duration: ~90 seconds
# Result: See what would be extracted (no writes)
```

### Example 6: Force Refresh Everything

```python
full_run = True
force_refresh = True
# Re-validate and re-extract everything
# Duration: ~3-5 minutes
# Result: All data refreshed
```

---

## Implementation Logic

### Flag Processing Order

```python
# 1. Process init_mode first (sets others)
if init_mode:
    test_all_endpoints = True
    extract_sample = True
    force_refresh = True

# 2. Process full_run (sets validation + extraction)
if full_run:
    test_all_endpoints = True
    extract_sample = True

# 3. Process validate_only (sets testing)
if validate_only:
    test_all_endpoints = True
    extract_sample = False  # Override if set

# 4. Apply modifiers
if dry_run:
    # Disable all writes
    
if debug_mode:
    # Enable verbose logging
```

---

## Comparison with Current

### Current Flags (5)

```python
debug_mode = False
full_run_mode = False  # Unclear purpose
init_mode = False      # Does everything
test_endpoints = False  # NEW
extract_sample = False  # NEW
```

**Issues:**
- init_mode too broad
- full_run_mode unclear
- No dry_run capability
- No force_refresh
- No scope control

### Proposed Flags (9)

```python
# Core Execution
init_mode = False           # ✅ Clear: complete initialization
validate_only = False       # ✨ NEW: validation without extraction
extract_sample = False      # ✅ Clear: sample database
full_run = False            # ✅ Renamed & clarified

# Control/Modifiers
debug_mode = False          # ✅ Clear: diagnostics
dry_run = False             # ✨ NEW: preview mode
force_refresh = False       # ✨ NEW: ignore existing

# Scope
test_all_endpoints = False  # ✅ Renamed from test_endpoints
max_sample_rows = 100       # ✨ NEW: control sample size
```

**Benefits:**
- Clear semantics for each flag
- Fine-grained control
- Safe defaults
- Composable
- Explicit intent

---

## Recommended Implementation

### Phase 1: Add Core Flags (Now)

```python
# Add to notebook parameters:
init_mode = False
validate_only = False
extract_sample = False
test_all_endpoints = False (rename from test_endpoints)
debug_mode = False
```

### Phase 2: Add Advanced Flags (Later)

```python
# Add when needed:
dry_run = False
force_refresh = False
max_sample_rows = 100
```

---

## Summary

### What init_mode Should Be

✅ **Complete initialization:**
- Bootstrap endpoints
- Test all 120 endpoints
- Extract sample database
- Validate everything
- First-run setup

**Semantic:** "Set up everything from scratch"

### What debug_mode Should Be

✅ **Enhanced diagnostics:**
- Verbose logging
- Display DataFrames
- Full stack traces
- Don't fail fast

**Semantic:** "Show me everything that's happening"

### What test_endpoints Should Be (Renamed)

✅ **test_all_endpoints:**
- Test all 120 GET endpoints
- Document what works/fails
- Update health check table

**Semantic:** "Test every endpoint comprehensively"

### What extract_sample Should Be

✅ **Extract sample dimensional database:**
- 5 tables to Delta
- Max 100 rows per table (configurable)
- For Prepare stage schema design

**Semantic:** "Build sample database for Prepare"

### New Flags Needed

✅ **validate_only** - Validation without extraction  
✅ **dry_run** - Preview without writes  
✅ **force_refresh** - Ignore existing data  
✅ **max_sample_rows** - Control sample size

---

**Should I implement the complete SPECTRA-grade flag system with all 9 flags?**

---

*Analysis: 2025-12-02 21:40 GMT*

