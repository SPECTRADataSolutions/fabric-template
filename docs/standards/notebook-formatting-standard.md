# SPECTRA Notebook Formatting Standard

**Version:** 1.1  
**Status:** ✅ Active  
**Last Updated:** 2025-12-10  
**Canonical Reference:** `sourceZephyr.Notebook/notebook_content.py`

---

## Overview

This standard defines the canonical structure and formatting for all SPECTRA Fabric notebooks. All notebooks must follow this pattern for consistency, maintainability, and SPECTRA-grade quality.

**Canonical Example:** `sourceZephyr.Notebook/notebook_content.py`

---

## Structure

### 1. Header Block (Required)

```python
# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "...",
# META       "default_lakehouse_name": "...",
# META       "default_lakehouse_workspace_id": "...",
# META       "known_lakehouses": [...]
# META     },
# META     "environment": {
# META       "environmentId": "...",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }
```

**Purpose:** Fabric metadata for kernel, lakehouse, and environment configuration.

---

### 2. Markdown Documentation Block (Required)

```python
# MARKDOWN ********************

# # 🔗 Source Stage — Zephyr Enterprise
# ### Connectivity • Authentication • Endpoint Intelligence
# 
# Establishes secure connectivity, validates authentication, and catalogs all available API endpoints for downstream SPECTRA pipeline stages.
# 
# ---
# 
# ## Outputs
# - `source.portfolio` — Dashboard-ready system overview & metrics
# - `source.config` — Canonical configuration settings
# - `source.credentials` — Masked authentication materials
# - `source.endpoints` — Full API catalog
```

**Purpose:** Stage documentation, purpose, and outputs. Use emojis for visual clarity.

**Format:**
- Stage title with emoji
- Subtitle with key capabilities
- Brief description
- `---` separator
- Outputs list (if applicable)

---

### 3. SDK Import Cell (Required)

```python
# CELL ********************

%run spectraSDK

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

**Purpose:** Load SPECTRA SDK. **CRITICAL:** Magic commands (`%run`, `%pip`, `%conda`) MUST be in isolated cells with no other code or comments.

**Rules:**
- ✅ Magic command in its own cell
- ✅ METADATA block immediately after
- ❌ No comments or other code in magic command cell

---

### 4. Parameters Cell (Required)

```python
# CELL ********************

# == 1. PARAMETERS =================================================== SPECTRA

bootstrap: bool = True  # Create/update Prepare stage configuration tables
test: bool = False  # Run comprehensive validation tests (Stage 5)
discover: bool = False  # Create sample entities for version change detection

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

**Purpose:** Define notebook parameters with type hints and inline comments.

**Format:**
- Section header: `# == N. SECTION NAME =================================================== SPECTRA`
- Type hints: `parameter: type = default_value`
- Inline comments explaining purpose
- METADATA block after

---

### 5. Context Cell (Required)

```python
# CELL ********************

# == 2. CONTEXT ====================================================== SPECTRA

session = NotebookSession("zephyrVariables")  # Variable Library name
session.load_context(bootstrap=bootstrap, backfill=backfill, spark=spark, preview=False, test=test)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

**Purpose:** Initialize NotebookSession and load context.

**Pattern:**
- Create `NotebookSession` with Variable Library name
- Call `load_context()` with parameters
- METADATA block after

---

### 6. Initialize Cell (Required)

```python
# CELL ********************

# == 3. INITIALIZE =================================================== SPECTRA

log = session.initialize()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

**Purpose:** Initialize logging and return logger instance.

**Pattern:**
- `log = session.initialize()`
- METADATA block after

---

### 7. Execute Cell(s) (Required)

```python
# CELL ********************

# == 4. EXECUTE ====================================================== SPECTRA

# Stage-specific execution logic here
SourceStageHelpers.execute_source_stage(spark=spark, session=session)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

**Purpose:** Main stage execution logic.

**Pattern:**
- Section header with stage name
- Execution logic (can be multiple cells if needed)
- METADATA block after each cell

---

### 8. Validate Cell (Required)

```python
# CELL ********************

# == 5. VALIDATE ===================================================== SPECTRA

session.validate()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

**Purpose:** Validate stage outputs and quality gates.

**Pattern:**
- `session.validate()`
- METADATA block after

---

### 9. Record Cell (Required)

```python
# CELL ********************

# == 6. RECORD ======================================================= SPECTRA

session.record(spark=spark)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

**Purpose:** Record stage activity to log table.

**Pattern:**
- `session.record(spark=spark)`
- Logs to: `Tables/log/{stage}log` (e.g., `Tables/log/sourcelog`, `Tables/log/preparelog`)
- METADATA block after

**Log Path Format:**
- ✅ `Tables/log/{stage}log` (all logs in central log schema)
- ❌ `Tables/{stage}/{stage}log` (incorrect - logs should be centralized)

---

### 10. Finalise Cell (Required)

```python
# CELL ********************

# == 7. FINALISE ===================================================== SPECTRA

session.finalise()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

**Purpose:** Finalise stage execution, emit capabilities, log completion.

**Pattern:**
- `session.finalise()`
- METADATA block after

---

## Cell Structure Rules

### METADATA Blocks

**Every code cell MUST have a METADATA block immediately after:**

```python
# CELL ********************

# Code here

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

**Rules:**
- ✅ METADATA block immediately after cell code
- ✅ Always use `"language": "python"` and `"language_group": "synapse_pyspark"`
- ❌ Never skip METADATA blocks
- ❌ Never put METADATA before cell code

---

### Section Headers

**Format:**
```python
# == N. SECTION NAME =================================================== SPECTRA
```

**Pattern:**
- `==` separator
- Number and section name
- `=` padding to align
- `SPECTRA` suffix

**Examples:**
- `# == 1. PARAMETERS =================================================== SPECTRA`
- `# == 2. CONTEXT ====================================================== SPECTRA`
- `# == 4. EXECUTE ====================================================== SPECTRA`

---

### Magic Commands

**CRITICAL:** Magic commands (`%run`, `%pip`, `%conda`) MUST be in isolated cells:

```python
# CELL ********************

%run spectraSDK

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

**Rules:**
- ✅ Magic command in its own cell
- ✅ No other code or comments in magic command cell
- ✅ METADATA block immediately after
- ❌ Never mix magic commands with Python code

---

## Logging Standards

### Log Table Path

**Format:** `Tables/log/{stage}log`

**Examples:**
- `Tables/log/sourcelog`
- `Tables/log/preparelog`
- `Tables/log/extractlog`
- `Tables/log/cleanlog`

**Purpose:** All logs live in a central `log` schema for unified logging and monitoring.

**Implementation:** SDK's `session.record()` automatically uses this format.

---

## Naming Conventions

### Notebook Names

**Format:** `{stage}{SourceSystem}.Notebook`

**Examples:**
- `sourceZephyr.Notebook`
- `prepareZephyr.Notebook`
- `extractZephyr.Notebook`

**Pattern:**
- Stage name (lowercase)
- Source system name (PascalCase)
- `.Notebook` suffix

---

### Variable Names

**Parameters:**
- `bootstrap: bool = True`
- `test: bool = False`
- `discover: bool = False`

**Session:**
- `session = NotebookSession("variableLibraryName")`
- `log = session.initialize()`

---

## Code Style

### Type Hints

**Always use type hints for parameters:**

```python
bootstrap: bool = True
test: bool = False
discover: bool = False
```

---

### Comments

**Inline comments for parameters:**

```python
bootstrap: bool = True  # Create/update Prepare stage configuration tables
test: bool = False  # Run comprehensive validation tests (Stage 5)
```

**Section comments:**

```python
# == 1. PARAMETERS =================================================== SPECTRA
```

---

## SPECTRA Seven-Stage Pattern

**All notebooks follow this pattern:**

1. **Parameters** - Define inputs
2. **Context** - Load session context
3. **Initialize** - Initialize logging
4. **Execute** - Main stage logic
5. **Validate** - Quality gates
6. **Record** - Log activity
7. **Finalise** - Complete stage

---

## Compliance Checklist

- [ ] Header block with METADATA
- [ ] Markdown documentation block
- [ ] SDK import cell (isolated)
- [ ] Parameters cell with type hints
- [ ] Context cell
- [ ] Initialize cell
- [ ] Execute cell(s)
- [ ] Validate cell
- [ ] Record cell
- [ ] Finalise cell
- [ ] METADATA block after every code cell
- [ ] Section headers with SPECTRA suffix
- [ ] Log path: `Tables/{stage}/{stage}log`
- [ ] Magic commands in isolated cells
- [ ] Type hints for parameters
- [ ] Inline comments for parameters

---

## Examples

### Canonical Reference

**`sourceZephyr.Notebook/notebook_content.py`** - The canonical example for all SPECTRA notebooks.

**Key Characteristics:**
- Clean, minimal structure
- Clear section headers
- Proper METADATA blocks
- Isolated magic commands
- Type hints and comments
- SPECTRA-grade formatting

---

## Version History

- **v1.0** (2025-12-10): Initial standard based on `sourceZephyr.Notebook` canonical format

---

## References

- **Canonical Example:** `sourceZephyr.Notebook/notebook_content.py`
- **SDK Documentation:** `Data/fabric-sdk/docs/`
- **SPECTRA Methodology:** `Core/doctrine/THE-SEVEN-LEVELS-OF-MATURITY.md`


