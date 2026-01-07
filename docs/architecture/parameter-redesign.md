# Parameter Redesign - SPECTRA-Grade

**Date:** 2025-12-03  
**Current:** 10 parameters (overlapping purposes)  
**Goal:** Clear, distinct, no confusion

---

## Key Insight

**full_run is NOT the same as init_mode!**

- **init_mode** = Bootstrap (first run setup)
- **full_run** = Backfill (reset watermark, reload ALL data)

These are **different technical operations**!

---

## Semantic Clarity Issues

### Current Names

| Parameter        | Intent          | Confusion               |
| ---------------- | --------------- | ----------------------- |
| `init_mode`      | First run       | ✅ Clear                |
| `full_run`       | Reset watermark | ❌ Vague - "full" what? |
| `extract_sample` | Get sample      | ✅ Clear                |
| `debug_mode`     | Logging         | ✅ Clear                |

**Problem:** "full_run" doesn't say what it's full of or what it does.

---

## Better Names for "full_run"

### Option 1: `full_refresh`

```python
full_refresh: bool = False  # Reset watermark, reload ALL data from epoch
```

**Pros:** Clear intent (refresh everything)  
**Cons:** None

### Option 2: `reset_watermark`

```python
reset_watermark: bool = False  # Reset last_extract_date to epoch
```

**Pros:** Technically precise  
**Cons:** Requires understanding "watermark" concept

### Option 3: `backfill_all`

```python
backfill_all: bool = False  # Reload all historical data
```

**Pros:** Data engineering standard term  
**Cons:** Might not be familiar to all users

### Option 4: `reload_all`

```python
reload_all: bool = False  # Reload all data (ignore last run date)
```

**Pros:** Simple, clear  
**Cons:** Less precise

**My vote: `full_refresh`** - Clear, common, describes intent

---

## Revised Parameter Structure

### Core Parameters (4)

```python
# === Execution Modes ===
init_mode: bool = False      # First run: bootstrap endpoints (run once)
full_refresh: bool = False   # Reset watermark: reload ALL data from epoch
extract_sample: bool = False # Extract sample DB for schema design
debug_mode: bool = False     # Enhanced logging and diagnostics
```

**What each does:**

**init_mode:**

- Bootstraps endpoints to Delta (first run)
- Automatically sets `extract_sample=True`
- Run once, never again

**full_refresh:**

- Resets last_extract_date to epoch (1970-01-01)
- Forces complete data reload
- Use when: Need to rebuild entire database

**extract_sample:**

- Extracts sample data to Delta
- Use when: Prepare stage needs schema sample
- Independent of init/refresh

**debug_mode:**

- Enhanced logging (INFO/DEBUG levels)
- Shows DataFrames
- No side effects

---

## Relationships

```python
# Parameter logic (crystal clear)
if init_mode:
    extract_sample = True  # Init always gets sample
    log.info("init_mode → will bootstrap endpoints + extract sample")

if full_refresh:
    log.info("full_refresh → will reset watermark to epoch, reload ALL data")
    # Note: This is different from init!
    # init = first setup
    # full_refresh = complete reload

# No contradictions possible!
```

---

## What About The Others?

### test_all_endpoints

**Current:** User flag  
**Better:** Automatic based on mode  
**Decision:** Remove as parameter, make internal logic

```python
# Internal logic (not a parameter)
should_test_endpoints = init_mode or debug_mode
```

### validate_outputs

**Current:** User flag  
**Better:** Always validate if extracting  
**Decision:** Remove as parameter, make automatic

```python
# Internal logic
if extract_sample:
    # Always validate sample data
```

### max_sample_rows

**Current:** User parameter  
**Better:** Constant or rare override  
**Decision:** Keep but maybe make it optional/advanced

```python
# Advanced tuning (rarely changed)
max_sample_rows: int = 100
```

### trace_execution_id

**Current:** User parameter  
**Better:** Not needed in Source stage  
**Decision:** Remove (premature optimization)

### dry_run

**Current:** User parameter  
**Better:** Source is already lightweight, preview adds no value  
**Decision:** Remove (unnecessary complexity)

### force_refresh

**Current:** User parameter  
**Better:** This IS what full_refresh means  
**Decision:** Remove (redundant with full_refresh)

---

## Final SPECTRA-Grade Design

### Essential Parameters (4)

```python
# === Source Stage Parameters ===
# Source validates connectivity + optionally extracts sample for schema design

init_mode: bool = False      # First run: bootstrap endpoints to Delta
                             # → Auto-sets: extract_sample=True
                             # → Run: Once only (first pipeline run)

full_refresh: bool = False   # Complete reload: reset watermark to epoch
                             # → Reloads: ALL historical data
                             # → Run: When rebuilding database

extract_sample: bool = False # Extract sample dimensional DB
                             # → Creates: Sample tables for Prepare stage
                             # → Run: When Prepare needs fresh sample

debug_mode: bool = False     # Enhanced diagnostics
                             # → Adds: Verbose logging, DataFrame displays
                             # → Run: When troubleshooting issues
```

### Advanced/Optional (if needed)

```python
max_sample_rows: int = 100   # Sample size (rarely changed)
```

---

## Logic (Crystal Clear)

```python
# === Parameter Logic ===
log.info(f"Mode: init={init_mode}, refresh={full_refresh}, sample={extract_sample}, debug={debug_mode}")

# Init mode sets sample
if init_mode:
    if not extract_sample:
        log.info("init_mode → enabling extract_sample")
        extract_sample = True

# Contradiction check (only one real contradiction)
if init_mode and full_refresh:
    raise ValueError(
        "init_mode and full_refresh are mutually exclusive:\n"
        "  • init_mode = First run (bootstrap)\n"
        "  • full_refresh = Complete reload (reset watermark)\n"
        "  Choose one!"
    )

# Internal flags (not parameters)
should_test_endpoints = init_mode or debug_mode
should_validate = extract_sample  # Always validate if extracting

log.info(f"Effective: sample={extract_sample}, test={should_test_endpoints}, validate={should_validate}")
```

**Clean. Simple. SPECTRA-grade. ✨**

---

## Comparison

| Aspect              | Current (10) | Proposed (4)         |
| ------------------- | ------------ | -------------------- |
| **Parameters**      | 10           | 4                    |
| **Overrides**       | Many         | One (init → sample)  |
| **Contradictions**  | Multiple     | One (init + refresh) |
| **Clarity**         | Confusing    | Crystal clear        |
| **User Experience** | Complex      | Simple               |

---

## My Recommendation

**Strip down to 4 essential parameters:**

1. `init_mode` - First run
2. `full_refresh` - Complete reload (renamed from full_run)
3. `extract_sample` - Get sample
4. `debug_mode` - Logging

**Remove 6 parameters that add clunk:**

- full_run (rename to full_refresh)
- test_all_endpoints (automatic)
- validate_outputs (automatic)
- trace_execution_id (not needed yet)
- dry_run (unnecessary)
- force_refresh (redundant)
- max_sample_rows (optional/default)

**Result:** SPECTRA-grade simplicity! 🎯

---

**Should I implement this 4-parameter design?**
