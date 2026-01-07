# Debug Logging and Runtime Parameters

**Date:** 2025-01-29  
**Status:** SPECTRA-Grade Standards  
**Reference:** SPECTRA Pipeline Standards, Audit Logging Standards

---

## Debug Mode Logging

### Current Implementation

**Logger:** `initialise_logger()` from `spectra.modules.shared.logging`  
**Output:** stdout/stderr (Fabric notebook output)  
**Level Control:** `logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)`

### SPECTRA-Grade Standard

**Two-Tier Logging:**

1. **Verbose Debug Logs (stdout/stderr)**
   - Controlled by `debug_mode` parameter
   - When `debug_mode=True`: Logs DEBUG level messages to stdout
   - When `debug_mode=False`: Logs INFO level and above only
   - Used for: Detailed execution traces, schema previews, data samples
   - **Location:** Fabric notebook output (stdout/stderr)

2. **Audit Logs (Delta Tables)**
   - Always written (regardless of `debug_mode`)
   - Stage-level activity summaries
   - **Location:** `Tables/log/_<stage>log` (e.g., `Tables/log/_sourcelog`)
   - **Format:** Structured records with status, duration, row counts, etc.

### Implementation Pattern

```python
# 1. Setup logger (stdout/stderr)
log = initialise_logger("sourceZephyr")
log.setLevel(logging.DEBUG if debug_mode else logging.INFO)

# 2. Verbose debug logs (stdout only when debug_mode=True)
if debug_mode:
    log.debug("Detailed execution trace...")
    display(df.sample(10))  # Show data samples

# 3. Audit logs (Delta table - always written)
from spectra.modules.shared.logging import log_stage_activity

log_stage_activity(
    result={
        "status": "success",
        "rowCount": row_count,
        "duration": duration
    },
    stage="source",
    logTablePath="Tables/log/_sourcelog",
    entityName="zephyr",
    projectKey=None  # Not scoped yet
)
```

---

## Runtime Parameters Assessment

### Current Parameters (Source Stage)

1. **`debug_mode`** ✅
   - **Purpose:** Control verbose logging and debug output
   - **Default:** `false` (production-safe)
   - **Usage:** Controls log level and data previews

2. **`full_run_mode`** ✅
   - **Purpose:** Control full vs incremental extraction
   - **Default:** `false` (incremental by default)
   - **Usage:** Not yet used in Source stage (will be used in Extract stage)

3. **`init_mode`** ✅
   - **Purpose:** Bootstrap endpoints.json to Delta table (Zephyr-specific)
   - **Default:** `false` (one-time operation)
   - **Usage:** Source stage bootstrap

### Potential Additional Parameters

#### 1. `project_key` / `project_id` (Future)

**Status:** Not needed for Source stage (handshake only)  
**Future Use:** Extract/Clean/Transform stages may need project scoping

**Rationale:**
- Zephyr API has project-scoped endpoints (e.g., `/release/project/{projectid}`)
- Currently Source stage lists ALL projects (no scoping needed)
- Extract stage will likely need `project_id` to scope data extraction
- **Recommendation:** Add when Extract stage is implemented

**Example:**
```python
# Future Extract stage
project_id = get_param("project_id", "DXC_ZEPHYR_PROJECT_ID", None)
if project_id:
    # Scope extraction to specific project
    url = f"{base_url}/release/project/{project_id}"
else:
    # Extract all projects (full catalogue)
    url = f"{base_url}/release"
```

#### 2. `watermark_date` (Future)

**Status:** Not needed for Source stage  
**Future Use:** Extract stage incremental loads

**Rationale:**
- Zephyr supports incremental extraction (`supportsIncremental: true` in contract)
- Extract stage will need `lastExtractDate` or `watermark_date`
- **Recommendation:** Add when Extract stage implements incremental logic

---

## Recommendations

### ✅ Keep Current Parameters

- `debug_mode` - Essential for troubleshooting
- `full_run_mode` - Standard SPECTRA parameter (will be used in Extract)
- `init_mode` - Zephyr-specific bootstrap (needed for Source stage)

### ⏸️ Defer Additional Parameters

- `project_id` - Add when Extract stage needs project scoping
- `watermark_date` - Add when Extract stage implements incremental loads

### 📝 Logging Implementation

1. **Update Source notebook** to write audit logs to `Tables/log/_sourcelog`
2. **Keep debug logs** in stdout (Fabric notebook output)
3. **Use `log_stage_activity()`** for structured audit logging

---

## SPECTRA-Grade Pattern

```python
# === Parameters ===
debug_mode = get_bool_param("debug_mode", "DXC_ZEPHYR_DEBUG_MODE", False)
full_run_mode = get_bool_param("full_run_mode", "DXC_ZEPHYR_FULL_RUN_MODE", False)
init_mode = get_bool_param("init_mode", "DXC_ZEPHYR_INIT_MODE", False)

# === Logger Setup ===
log = initialise_logger("sourceZephyr")
log.setLevel(logging.DEBUG if debug_mode else logging.INFO)

# === Execution ===
# ... pipeline logic ...

# === Audit Logging (Delta Table) ===
from spectra.modules.shared.logging import log_stage_activity

log_stage_activity(
    result={
        "status": "success",
        "rowCount": row_count,
        "duration": duration,
        "endpointsChecked": endpoint_count
    },
    stage="source",
    logTablePath="Tables/log/_sourcelog",
    entityName="zephyr"
)
```

---

## Summary

**Current Parameters:** ✅ Appropriate for Source stage  
**Debug Logging:** stdout for verbose, Delta tables for audit  
**Future Parameters:** Add `project_id` and `watermark_date` when Extract stage is implemented




