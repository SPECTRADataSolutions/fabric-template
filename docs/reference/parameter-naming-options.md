# Parameter Naming Options - 7 Families

**Date:** 2025-12-03  
**Goal:** All 4 parameters feel like one cohesive family

---

## Option A: Simple Verbs (Minimal)

```python
bootstrap: bool = False  # Bootstrap endpoints
backfill: bool = False   # Backfill all data
sample: bool = False     # Extract sample
debug: bool = False      # Enhanced logging
```

**Family vibe:** Action commands, minimal, clean

---

## Option B: Mode Suffix (Consistent)

```python
bootstrap_mode: bool = False  # Bootstrap mode
backfill_mode: bool = False   # Backfill mode
sample_mode: bool = False     # Sample mode
debug_mode: bool = False      # Debug mode
```

**Family vibe:** All modes, explicit, consistent suffix

---

## Option C: Enable Prefix (Activation)

```python
enable_bootstrap: bool = False  # Enable bootstrap
enable_backfill: bool = False   # Enable backfill
enable_sample: bool = False     # Enable sample extraction
enable_debug: bool = False      # Enable debug logging
```

**Family vibe:** All activation switches, clear intent

---

## Option D: Run Prefix (Execution)

```python
run_bootstrap: bool = False  # Run bootstrap
run_backfill: bool = False   # Run backfill
run_sample: bool = False     # Run sample extraction
run_debug: bool = False      # Run in debug mode
```

**Family vibe:** All execution directives, action-oriented

---

## Option E: Is/Should Questions (State)

```python
is_first_run: bool = False    # Is this the first run?
should_backfill: bool = False # Should backfill all data?
should_sample: bool = False   # Should extract sample?
is_debug: bool = False        # Is debug enabled?
```

**Family vibe:** Conversational, question-based, natural language

---

## Option F: Stage Operations (Namespaced)

```python
source_init: bool = False      # Initialize source
source_reload: bool = False    # Reload all source data
source_sample: bool = False    # Sample source data
source_debug: bool = False     # Debug source stage
```

**Family vibe:** All namespaced to stage, very explicit

---

## Option G: Data Engineering Terms (Technical)

```python
cold_start: bool = False       # Cold start (first run)
full_load: bool = False        # Full load (vs incremental)
sample_data: bool = False      # Sample data extraction
verbose: bool = False          # Verbose logging
```

**Family vibe:** Industry standard terms, professional

---

## Comparison Table

| Style            | Example            | Pros           | Cons                          | SPECTRA-Grade? |
| ---------------- | ------------------ | -------------- | ----------------------------- | -------------- |
| **A: Simple**    | `bootstrap`        | Minimal, clean | Maybe too terse               | ⭐⭐⭐⭐       |
| **B: \_mode**    | `bootstrap_mode`   | Consistent     | Verbose                       | ⭐⭐⭐⭐       |
| **C: enable\_**  | `enable_bootstrap` | Clear intent   | Long                          | ⭐⭐⭐         |
| **D: run\_**     | `run_bootstrap`    | Action-clear   | "run_debug" awkward           | ⭐⭐⭐         |
| **E: is/should** | `is_first_run`     | Natural        | Mixed pattern (is/should)     | ⭐⭐           |
| **F: source\_**  | `source_init`      | Namespaced     | Redundant (already in Source) | ⭐⭐           |
| **G: Technical** | `cold_start`       | Industry terms | Less intuitive                | ⭐⭐⭐         |

---

## My Top 3 Recommendations

### 🥇 Option A: Simple Verbs

```python
bootstrap: bool = False
backfill: bool = False
sample: bool = False
debug: bool = False
```

**Why:** Elegant, minimal, action-oriented. Each word is precise.

### 🥈 Option B: Mode Family

```python
bootstrap_mode: bool = False
backfill_mode: bool = False
sample_mode: bool = False
debug_mode: bool = False
```

**Why:** Consistent suffix, all feel like "modes of operation"

### 🥉 Option G: Data Engineering

```python
cold_start: bool = False    # Industry term for first run
full_load: bool = False     # Standard term for complete reload
sample: bool = False        # Extract sample
verbose: bool = False       # Enhanced logging
```

**Why:** Professional, industry-standard terms

---

## Pattern Analysis

**What makes a family?**

- Same word structure (all verbs, all nouns, all adjectives)
- Same length pattern (all single, all compound)
- Same prefix/suffix (consistent decoration)
- Same semantic domain (all actions, all states)

**Best families:**

- **A** - All single-word action verbs
- **B** - All "\_mode" suffixed
- **G** - All industry terms

---

## Visual Comparison

```python
# OPTION A - Simple & Clean
bootstrap = False
backfill = False
sample = False
debug = False

# OPTION B - Consistent Pattern
bootstrap_mode = False
backfill_mode = False
sample_mode = False
debug_mode = False

# OPTION G - Professional Terms
cold_start = False
full_load = False
sample = False
verbose = False
```

---

## Which Feels Most SPECTRA?

**SPECTRA values:**

- Clarity over brevity
- Precision over convention
- Elegance over verbosity
- Pattern consistency

**My ranking:**

1. **Option A** - Simple verbs (most elegant)
2. **Option B** - Mode family (most consistent)
3. **Option G** - Industry terms (most professional)

---

**Which resonates with you?** Or want me to generate 5 MORE options? 🎯
