# Single-Word Alternatives for "sample"

**Context:** Extract sample dimensional database for schema design  
**Current:** `sample: bool` (too vague)  
**Need:** Clear single-word alternative

---

## Option A Family - Refined

### Original

```python
bootstrap: bool = False  # Bootstrap endpoints
backfill: bool = False   # Backfill all data
sample: bool = False     # ❌ Vague
debug: bool = False      # Enhanced logging
```

### Alternative 1: "prototype"

```python
bootstrap: bool = False  # Bootstrap endpoints
backfill: bool = False   # Backfill all data
prototype: bool = False  # Extract prototype database
debug: bool = False      # Enhanced logging
```

**Meaning:** Extracting a prototype/example of the dimensional model

### Alternative 2: "schema"

```python
bootstrap: bool = False  # Bootstrap endpoints
backfill: bool = False   # Backfill all data
schema: bool = False     # Extract schema sample
debug: bool = False      # Enhanced logging
```

**Meaning:** Extracting data for schema design

### Alternative 3: "preview"

```python
bootstrap: bool = False  # Bootstrap endpoints
backfill: bool = False   # Backfill all data
preview: bool = False    # Preview dimensional model
debug: bool = False      # Enhanced logging
```

**Meaning:** Previewing what the data looks like

### Alternative 4: "specimen"

```python
bootstrap: bool = False  # Bootstrap endpoints
backfill: bool = False   # Backfill all data
specimen: bool = False   # Extract data specimen
debug: bool = False      # Enhanced logging
```

**Meaning:** Scientific term for sample (more formal)

### Alternative 5: "snapshot"

```python
bootstrap: bool = False  # Bootstrap endpoints
backfill: bool = False   # Backfill all data
snapshot: bool = False   # Extract data snapshot
debug: bool = False      # Enhanced logging
```

**Meaning:** Point-in-time snapshot of the data

### Alternative 6: "extract"

```python
bootstrap: bool = False  # Bootstrap endpoints
backfill: bool = False   # Backfill all data
extract: bool = False    # Extract sample dataset
debug: bool = False      # Enhanced logging
```

**Meaning:** Extract (what's implied: sample data)

### Alternative 7: "explore"

```python
bootstrap: bool = False  # Bootstrap endpoints
backfill: bool = False   # Backfill all data
explore: bool = False    # Explore with sample data
debug: bool = False      # Enhanced logging
```

**Meaning:** Exploratory data extraction

---

## My Top 3

### 🥇 `prototype`

**Why:** Implies "building a prototype dimensional model"  
**Clear:** Yes - prototype of what? The database!  
**SPECTRA-esque:** Has that architectural feel

### 🥈 `schema`

**Why:** Extracting FOR schema design (that's the purpose)  
**Clear:** Yes - getting data to design schemas  
**SPECTRA-esque:** Technical and precise

### 🥉 `preview`

**Why:** Previewing the dimensional structure  
**Clear:** Yes - preview of the final database  
**SPECTRA-esque:** User-friendly, understandable

---

## Final Family Examples

### With "prototype"

```python
bootstrap: bool = False  # Bootstrap endpoints (once)
backfill: bool = False   # Backfill all data (reset watermark)
prototype: bool = False  # Prototype dimensional model (sample)
debug: bool = False      # Enhanced logging
```

### With "schema"

```python
bootstrap: bool = False  # Bootstrap endpoints (once)
backfill: bool = False   # Backfill all data (reset watermark)
schema: bool = False     # Schema design sample (for Prepare)
debug: bool = False      # Enhanced logging
```

### With "preview"

```python
bootstrap: bool = False  # Bootstrap endpoints (once)
backfill: bool = False   # Backfill all data (reset watermark)
preview: bool = False    # Preview dimensional model (sample)
debug: bool = False      # Enhanced logging
```

---

## Visual Appeal

```python
# Current (mixed)
init_mode
full_run
extract_sample
debug_mode

# Option A1: prototype
bootstrap
backfill
prototype
debug

# Option A2: schema
bootstrap
backfill
schema
debug

# Option A3: preview
bootstrap
backfill
preview
debug
```

**They all flow beautifully!**

---

## My Recommendation

**Use `prototype`:**

```python
bootstrap: bool = False  # Bootstrap endpoints (first run)
backfill: bool = False   # Backfill all data (reset watermark)
prototype: bool = False  # Prototype dimensional model (sample)
debug: bool = False      # Enhanced logging
```

**Why:**

- ✅ Single-word family
- ✅ Clear intent (building a prototype)
- ✅ Architecturally sound
- ✅ All action-oriented
- ✅ No confusion possible

**Second choice: `schema`** (more technical, equally clear)

---

**What do you think? prototype, schema, or preview?** 🎯
