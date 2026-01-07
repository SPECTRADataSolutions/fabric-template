# Parameter Naming - Creating a Family

**Date:** 2025-12-03  
**Issue:** Mixing "mode" with other naming patterns  
**Goal:** All parameters feel like they belong together

---

## Current Inconsistency

```python
init_mode: bool         # Uses "mode"
full_refresh: bool      # Action verb
extract_sample: bool    # Action verb
debug_mode: bool        # Uses "mode"
```

**Problem:** "mode" vs "action verb" - inconsistent!

---

## What Are These Parameters Really?

**They're execution directives** - telling the Source stage what to do.

---

## Naming Options

### Option 1: All "mode" suffix

```python
init_mode: bool = False        # First run mode
refresh_mode: bool = False     # Complete reload mode
sample_mode: bool = False      # Sample extraction mode
debug_mode: bool = False       # Debug mode
```

**Feel:** Consistent, but "sample_mode" feels forced

### Option 2: All actions (verbs)

```python
bootstrap: bool = False        # Bootstrap endpoints
reload: bool = False           # Reload all data from epoch
sample: bool = False           # Extract sample database
debug: bool = False            # Enable debug logging
```

**Feel:** Clean, action-oriented, but might be TOO terse

### Option 3: All "run\_" prefix

```python
run_init: bool = False         # Run initialization
run_refresh: bool = False      # Run full refresh
run_sample: bool = False       # Run sample extraction
run_debug: bool = False        # Run debug mode
```

**Feel:** Consistent, but "run_debug" is odd (debug isn't run, it's enabled)

### Option 4: All "do\_" prefix

```python
do_init: bool = False          # Do initialization
do_refresh: bool = False       # Do full refresh
do_sample: bool = False        # Do sample extraction
do_debug: bool = False         # Do debug logging
```

**Feel:** Consistent, but "do\_" is verbose for booleans

### Option 5: Context-specific verbs

```python
bootstrap: bool = False        # Bootstrap endpoints (once)
backfill: bool = False         # Backfill all historical data
sample: bool = False           # Sample for schema design
debug: bool = False            # Debug with enhanced logging
```

**Feel:** Each word is semantically precise for its purpose

### Option 6: Categorized with underscores

```python
stage_init: bool = False       # Initialize stage
stage_refresh: bool = False    # Refresh all data
stage_sample: bool = False     # Extract sample
stage_debug: bool = False      # Debug stage
```

**Feel:** Clear grouping, but redundant (we're already in Source stage)

---

## My Recommendation

**Option 2 + Better Names:**

```python
# === Source Stage Execution ===
bootstrap: bool = False      # Bootstrap endpoints (first run only)
backfill: bool = False       # Backfill all data (reset watermark to epoch)
sample: bool = False         # Extract sample for schema design
debug: bool = False          # Enhanced logging and diagnostics
```

**Why this works:**

- ✅ All single words (family)
- ✅ All action-oriented (verbs/states)
- ✅ Each semantically precise
- ✅ No prefixes/suffixes needed
- ✅ Clean and elegant

**OR if you prefer "mode" consistency:**

```python
# === Source Stage Execution ===
bootstrap_mode: bool = False    # Bootstrap endpoints (first run)
backfill_mode: bool = False     # Backfill all data (reset watermark)
sample_mode: bool = False       # Sample extraction mode
debug_mode: bool = False        # Debug mode
```

**Why this works:**

- ✅ All have "\_mode" suffix (family)
- ✅ Consistent pattern
- ✅ Clear purpose
- ✅ Familiar pattern

---

## Question for You

**Which family style do you prefer?**

**A) Simple (4 single words):**

```python
bootstrap, backfill, sample, debug
```

**B) Mode suffix (consistent):**

```python
bootstrap_mode, backfill_mode, sample_mode, debug_mode
```

**C) Something else?**

What feels most SPECTRA-grade to you? 🎯
