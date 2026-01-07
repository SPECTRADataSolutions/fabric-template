# Parameter Design Analysis - Is It SPECTRA-Grade?

**Date:** 2025-12-03  
**Question:** If init_mode=True but extract_sample=False, will it work?  
**Answer:** Yes, because init_mode **overrides** extract_sample

---

## Current Parameter Logic

### Parameters Defined

```python
# Core Execution Modes
init_mode: bool = False             # Complete initialization
debug_mode: bool = False            # Enhanced diagnostics
full_run: bool = False              # Comprehensive validation

# Validation & Testing
test_all_endpoints: bool = False    # Test all 120 endpoints
validate_outputs: bool = False      # Validate sample data

# Data Extraction
extract_sample: bool = False        # Extract sample database
max_sample_rows: int = 100          # Max rows per table

# Tracing & Debugging
trace_execution_id: int = 0         # Specific execution trace
dry_run: bool = False               # Preview mode
force_refresh: bool = False         # Ignore existing data
```

### Override Logic (Lines 445-458)

```python
# Apply parameter logic (init_mode and full_run set other flags)
if init_mode:
    test_all_endpoints = True      # ✅ Override
    extract_sample = True           # ✅ Override
    force_refresh = True            # ✅ Override

if full_run:
    test_all_endpoints = True      # ✅ Override
    extract_sample = True           # ✅ Override

# Validate parameter combinations
if dry_run and not extract_sample:
    print("⚠️  Warning: dry_run=True but extract_sample=False")

if trace_execution_id != 0 and not extract_sample:
    print(f"⚠️  Warning: trace_execution_id={trace_execution_id} but extract_sample=False")
```

---

## Is This SPECTRA-Grade?

### ✅ What's Good

1. **Semantic Modes**

   - `init_mode` means "complete initialization" (clear intent)
   - Automatically sets required flags
   - User doesn't need to remember dependencies

2. **Override Logic**

   - init_mode WILL work even if extract_sample=False
   - The mode overrides contradictory settings
   - Prevents user errors

3. **Some Validation**

   - Warns if dry_run without extract_sample
   - Warns if trace_execution_id without extract_sample

4. **Good Defaults**
   - Everything False by default
   - Safe starting point

### ⚠️ What's Missing (Not SPECTRA-Grade Yet)

1. **No Explicit Conflict Detection**

   ```python
   # If user sets:
   init_mode = True
   extract_sample = False  # Contradictory!

   # Current: Silently overrides (works but confusing)
   # SPECTRA-grade: Warn user about override
   ```

2. **No Parameter Dependency Documentation**

   - Which parameters depend on others?
   - Which combinations are invalid?
   - What does each mode actually do?

3. **Limited Validation**

   - Only 2 validation checks
   - No check for: init_mode + dry_run (contradictory?)
   - No check for: full_run + init_mode together

4. **No Logging of Overrides**
   - User might not know their setting was overridden
   - Silent overrides are confusing

---

## SPECTRA-Grade Parameter Design

### Principle 1: Explicit Override Warnings

```python
# Parameter override logic with logging
if init_mode:
    if not test_all_endpoints:
        log.warning("init_mode=True → overriding test_all_endpoints to True")
    if not extract_sample:
        log.warning("init_mode=True → overriding extract_sample to True")
    if not force_refresh:
        log.warning("init_mode=True → overriding force_refresh to True")

    test_all_endpoints = True
    extract_sample = True
    force_refresh = True
```

### Principle 2: Document Dependencies

```python
# === Core Execution Modes ===
init_mode: bool = False             # Complete initialization
                                    # → Sets: test_all_endpoints, extract_sample, force_refresh
                                    # → Use for: First run, complete bootstrap

full_run: bool = False              # Comprehensive validation + extraction
                                    # → Sets: test_all_endpoints, extract_sample
                                    # → Use for: Validation runs
```

### Principle 3: Validate Contradictions

```python
# Validate parameter combinations
contradictions = []

if init_mode and dry_run:
    contradictions.append("init_mode + dry_run (init writes data, dry_run prevents writes)")

if init_mode and full_run:
    contradictions.append("init_mode + full_run (both are complete modes, choose one)")

if extract_sample and max_sample_rows == 0:
    contradictions.append("extract_sample=True but max_sample_rows=0 (nothing to extract)")

if contradictions:
    log.error("❌ Parameter contradictions detected:")
    for c in contradictions:
        log.error(f"   • {c}")
    raise ValueError(f"Invalid parameter combination. Fix: {contradictions}")
```

### Principle 4: Mode Hierarchy

```python
# Define clear hierarchy
MODES = {
    "init_mode": {
        "sets": ["test_all_endpoints", "extract_sample", "force_refresh"],
        "conflicts_with": ["dry_run"],
        "description": "Complete first-run initialization"
    },
    "full_run": {
        "sets": ["test_all_endpoints", "extract_sample"],
        "conflicts_with": ["init_mode"],
        "description": "Comprehensive validation run"
    },
    "dry_run": {
        "requires": ["extract_sample"],
        "conflicts_with": ["init_mode", "force_refresh"],
        "description": "Preview without writing"
    }
}
```

---

## Proposed SPECTRA-Grade Design

### Option 1: Smart Defaults (Current + Warnings)

```python
# Keep current override logic BUT add warnings
if init_mode:
    overrides = []
    if not test_all_endpoints: overrides.append("test_all_endpoints")
    if not extract_sample: overrides.append("extract_sample")
    if not force_refresh: overrides.append("force_refresh")

    if overrides:
        log.warning(f"init_mode=True → overriding: {', '.join(overrides)}")

    test_all_endpoints = True
    extract_sample = True
    force_refresh = True
```

**Pros:** Works with any input, self-correcting  
**Cons:** User might not realize override happened

### Option 2: Strict Validation (Fail Fast)

```python
# Validate BEFORE overriding
if init_mode:
    if dry_run:
        raise ValueError("init_mode and dry_run are incompatible (init writes, dry_run doesn't)")

    # Then override
    test_all_endpoints = True
    extract_sample = True
    force_refresh = True
```

**Pros:** Forces user to understand parameters  
**Cons:** More failures, learning curve

### Option 3: Presets (Simplest)

```python
# Single parameter for common scenarios
preset: str = "default"  # Options: default, init, full, debug, sample

PRESETS = {
    "default": {},
    "init": {"init_mode": True},
    "full": {"full_run": True},
    "debug": {"debug_mode": True, "extract_sample": True},
    "sample": {"extract_sample": True, "max_sample_rows": 10}
}
```

**Pros:** Simple for users  
**Cons:** Less flexible

---

## Recommendation

### SPECTRA-Grade = Option 1 + Documentation

1. **Keep smart overrides** (works with any input)
2. **Add explicit warnings** (user knows what happened)
3. **Document dependencies** (inline comments)
4. **Validate contradictions** (fail on impossible combinations)

### Implementation

```python
# === Parameter Validation & Logic ===

# Log parameter state
log.info(f"Parameters: init_mode={init_mode}, full_run={full_run}, extract_sample={extract_sample}")

# Check for contradictions
if init_mode and dry_run:
    raise ValueError("init_mode and dry_run are incompatible")
if init_mode and full_run:
    log.warning("Both init_mode and full_run are True - init_mode takes precedence")

# Apply mode overrides with logging
if init_mode:
    overrides = []
    if not test_all_endpoints: overrides.append("test_all_endpoints")
    if not extract_sample: overrides.append("extract_sample")
    if not force_refresh: overrides.append("force_refresh")

    if overrides:
        log.info(f"init_mode=True → setting: {', '.join(overrides)}")

    test_all_endpoints = True
    extract_sample = True
    force_refresh = True

if full_run:
    if not init_mode:  # Don't log if init_mode already set these
        overrides = []
        if not test_all_endpoints: overrides.append("test_all_endpoints")
        if not extract_sample: overrides.append("extract_sample")

        if overrides:
            log.info(f"full_run=True → setting: {', '.join(overrides)}")

    test_all_endpoints = True
    extract_sample = True

# Final parameter state
log.info(f"Effective: test={test_all_endpoints}, extract={extract_sample}, force={force_refresh}, debug={debug_mode}")
```

---

## Answer to Your Question

**Q:** "If init_mode=True but extract_sample=False, will init mode work?"

**A:** **YES**, because:

1. init_mode overrides extract_sample to True
2. This happens at lines 445-448
3. Your setting is ignored (but should be warned!)

**Current behavior:** Works but silent  
**SPECTRA-grade:** Works + warns user about override

---

## Next Steps

1. Add override warnings
2. Add contradiction validation
3. Document parameter dependencies
4. Add final state logging

**Should I implement these SPECTRA-grade improvements?** 🎯
