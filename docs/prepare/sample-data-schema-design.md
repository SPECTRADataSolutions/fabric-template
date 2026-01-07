# Sample Data Schema Design

## Decision: `sample/` vs `validation/`

**SPECTRA-grade decision: Use `Tables/sample/` for isolated test/discovery data.**

## Rationale

### Why `sample/` (CHOSEN) ✅
- ✅ **Clearer naming** - Immediately obvious what's inside (sample data)
- ✅ **No confusion** - "validation" is already Stage 5 in SPECTRA methodology
- ✅ **Broader purpose** - Can be used for discovery, testing, demonstrations, reference
- ✅ **Standard terminology** - Common data engineering term
- ✅ **Data classification** - Describes what the data IS, not what process created it

### Why NOT `validation/` ❌
- ❌ **Naming collision** - Stage 5 is "Validate" in SPECTRA
- ❌ **Confusing** - Could mean validation results, validation reports
- ❌ **Narrower purpose** - Implies only for validation/testing
- ❌ **Process-oriented** - Describes a process, not data classification

## Schema Structure

```
Tables/
├── source/          # Raw API data (production)
│   ├── cycles/
│   └── releases/
├── prepare/         # Metadata/configuration (NEVER entity data)
│   ├── _schema/
│   ├── _dependencies/
│   └── _constraints/
├── sample/          # Sample data for discovery/testing (ISOLATED)
│   ├── cycles/      # ← Sample cycles created for array discovery
│   ├── requirements/
│   └── _metadata/   # ← Documentation of what samples exist
├── extract/         # Production extracted data (CLEAN - no test data!)
│   ├── cycles/
│   └── requirements/
├── clean/
├── transform/
└── refine/
```

## Rules

### **Prepare Stage:**
- ✅ **CAN write to:** `Tables/prepare/*` (metadata only)
- ✅ **CAN write to:** `Tables/sample/*` (IF discover=True)
- ❌ **NEVER writes to:** `Tables/extract/*`, `Tables/source/*`
- ✅ **Always reads from:** `Tables/source/*` (passive discovery)

### **Extract Stage:**
- ✅ **Reads from:** `Tables/source/*` (production data)
- ✅ **Reads from:** `Tables/prepare/*` (schema metadata)
- ❌ **NEVER reads from:** `Tables/sample/*` (isolated!)
- ✅ **Writes to:** `Tables/extract/*` (production only)

### **Sample Data Lifecycle:**
- **Created by:** Prepare stage (when `discover=True`)
- **Purpose:** Array structure discovery, schema validation
- **Lifespan:** Persistent for reference (can be deleted after discovery complete)
- **Isolation:** Completely separate from production pipeline

## Parameter Design

```python
# prepareZephyr parameters
bootstrap: bool = True   # Create/update prepare tables
test: bool = False       # Run comprehensive tests (Stage 5)
discover: bool = False   # Create samples for array discovery (writes to Tables/sample/)
```

**When `discover=True`:**
- Prepare will create minimal sample entities in `Tables/sample/`
- Analyze sample data for array structures
- Enhance schema with discovered types
- Log warning that sample data exists

## Benefits

- ✅ **Zero data pollution** - Production extract stays clean
- ✅ **Explicit opt-in** - `discover=True` makes intent clear
- ✅ **Traceable** - `Tables/sample/_metadata/` documents what samples exist
- ✅ **Deletable** - Can drop entire `sample/` schema after discovery
- ✅ **Reusable** - Samples can be used for testing, demos, documentation

## Jira Comparison

**Jira doesn't need this** because:
- Jira always has production data in source
- Arrays are always populated
- No discovery needed

**Zephyr needs this** because:
- Test project (45) may have empty arrays
- Real project (44) discovery was for one-time probing
- Need isolated space for structural discovery

## Implementation Status

- ✅ **Documented** - This design doc
- ⏸️ **Not implemented** - Current prepareZephyr uses passive discovery only
- 🎯 **Future enhancement** - Add `discover=True` mode when needed

**Current approach (passive discovery from source) is SPECTRA-grade for L1-L3!**






