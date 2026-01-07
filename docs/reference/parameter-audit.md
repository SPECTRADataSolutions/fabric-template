# Parameter Audit - What Do We REALLY Need?

**Date:** 2025-12-03  
**Current:** 10 parameters  
**Question:** Are they all necessary or just "nice to have"?

---

## Current Parameters (10)

| Parameter              | Purpose                  | Necessary? | Assessment                    |
| ---------------------- | ------------------------ | ---------- | ----------------------------- |
| **init_mode**          | Complete initialization  | ✅ YES     | First run bootstrap           |
| **full_run**           | Comprehensive validation | ❓ MAYBE   | Overlaps with init_mode?      |
| **debug_mode**         | Enhanced logging         | ✅ YES     | Essential for troubleshooting |
| **test_all_endpoints** | Test all endpoints       | ❌ NO      | Auto-set by modes             |
| **validate_outputs**   | Validate sample data     | ❓ MAYBE   | Nice to have, not critical    |
| **extract_sample**     | Extract sample DB        | ✅ YES     | Needed for Prepare stage      |
| **max_sample_rows**    | Row limit                | ✅ YES     | Control sample size           |
| **trace_execution_id** | Trace specific execution | ❌ NO      | Over-engineering for Source   |
| **dry_run**            | Preview mode             | ❌ NO      | Complexity for minimal value  |
| **force_refresh**      | Ignore existing data     | ❌ NO      | Auto-set by init_mode         |

---

## Critical Questions

### 1. What IS Source Stage For?

**SPECTRA Methodology:**

- **Source stage** = Handshake + Connectivity validation
- Lightweight check
- Bootstrap metadata (endpoints)
- Maybe extract sample for schema design

**NOT for:**

- Heavy data extraction (that's later stages)
- Complex testing (that's validation)
- Production data loads (that's Transform/Refine)

### 2. What Are The Real Use Cases?

**Use Case 1: First Run (Once)**

- Bootstrap endpoints to Delta
- Extract sample for schema design
- Validate connectivity

**Use Case 2: Daily Production (Ongoing)**

- Validate connectivity still works
- Maybe refresh sample
- That's it!

**Use Case 3: Debugging (As Needed)**

- Enhanced logging
- See what's happening

**That's 3 use cases! Not 10 parameters.**

---

## Proposed SPECTRA-Grade Design

### Option 1: Single Mode Parameter

```python
# === Execution Mode ===
mode: str = "daily"  # Options: init, daily, debug

# === Configuration ===
max_sample_rows: int = 100  # Sample size for schema design
```

**Mode definitions:**

- **init** - First run (bootstrap + extract sample)
- **daily** - Production (just connectivity check)
- **debug** - Troubleshooting (enhanced logging + sample)

**That's 2 parameters! Down from 10.**

### Option 2: Minimal Flags

```python
# === Execution Control ===
init_mode: bool = False      # First run only (bootstrap endpoints)
debug_mode: bool = False     # Enhanced logging

# === Data Extraction ===
extract_sample: bool = False # Extract sample for schema design
max_sample_rows: int = 100   # Sample size
```

**That's 4 parameters! Down from 10.**

**Logic:**

- init_mode → bootstrap + extract_sample
- debug_mode → just logging
- extract_sample → controlled independently
- No overrides, no contradictions

### Option 3: Source Stage Reality Check

**What does Source ACTUALLY need to do?**

1. **Once (init):** Bootstrap endpoints
2. **Always:** Validate connectivity
3. **Optional:** Extract sample for Prepare

**Simplest design:**

```python
# === Source Stage Parameters ===
init_mode: bool = False      # Bootstrap endpoints (first run only)
extract_sample: bool = False # Extract sample for schema design (as needed)
debug_mode: bool = False     # Enhanced logging (troubleshooting)

# init_mode behavior:
# - Bootstraps endpoints to Delta (once)
# - Automatically sets extract_sample=True
# - That's it! Source is lightweight.
```

**That's 3 parameters! Absolute minimum.**

---

## What To Remove & Why

### ❌ Remove: full_run

**Why:** What's the difference between init and full_run? They both seem "complete". This is confusing.

**Replace with:** init_mode covers it (first run is the full run)

### ❌ Remove: test_all_endpoints

**Why:** Auto-set by modes. Users shouldn't control this directly.

**Replace with:** Automatic based on mode

### ❌ Remove: validate_outputs

**Why:** Nice to have, but Source stage is lightweight. Save validation for Prepare/Clean stages.

**Replace with:** Nothing (or move to Prepare stage)

### ❌ Remove: trace_execution_id

**Why:** Over-engineering. Source stage doesn't track individual executions yet.

**Replace with:** Add later if actually needed

### ❌ Remove: dry_run

**Why:** Preview mode adds complexity for minimal value. Source stage is already lightweight.

**Replace with:** debug_mode (see what happens without separate preview)

### ❌ Remove: force_refresh

**Why:** Auto-set by init_mode. Don't need separate flag.

**Replace with:** Implicit in init_mode

---

## SPECTRA-Grade Recommendation

### Absolute Minimum (3 parameters)

```python
# === Source Stage Parameters ===
# Source is lightweight: validate connectivity + optional sample extraction

init_mode: bool = False      # Bootstrap endpoints (first run only)
                             # → Also extracts sample automatically
                             # → Use once, then never again

extract_sample: bool = False # Extract sample dimensional DB for schema design
                             # → Independent control (can run without init)
                             # → Use when: Prepare stage needs fresh sample

debug_mode: bool = False     # Enhanced logging and DataFrame displays
                             # → Use when: Troubleshooting issues
                             # → No side effects, just visibility
```

**Logic:**

```python
# Parameter logic (ultra-simple)
if init_mode:
    extract_sample = True  # Init always gets sample
    log.info("init_mode=True → will bootstrap endpoints + extract sample")

log.info(f"Effective: init={init_mode}, extract={extract_sample}, debug={debug_mode}")
```

**That's it! No contradictions possible, crystal clear.**

---

## My Strong Recommendation

**Go with 3 parameters:**

1. `init_mode` - First run (bootstrap)
2. `extract_sample` - Get sample data
3. `debug_mode` - Enhanced logging

**Why 3 is SPECTRA-grade:**

- ✅ Pattern of Seven principle (3 is a subset)
- ✅ Each has distinct purpose
- ✅ No overlap or confusion
- ✅ No contradictions possible
- ✅ Easy to understand
- ✅ Easy to use

**Remove 7 parameters that add complexity without value:**

- full_run (covered by init_mode)
- test_all_endpoints (automatic)
- validate_outputs (too early in pipeline)
- trace_execution_id (premature optimization)
- dry_run (unnecessary complexity)
- force_refresh (implicit in init_mode)
- max_sample_rows (can default to 100, rarely changed)

---

## The Question

**10 parameters → 3 parameters**

**Should I simplify to these 3 essential parameters?** 🎯
