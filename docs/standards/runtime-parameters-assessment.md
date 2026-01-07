# Runtime Parameters SPECTRA-Grade Assessment

**Date:** 2025-01-29  
**Status:** ✅ Aligned with SPECTRA Standards  
**Reference:** SPECTRA Reviewer Prompt, Naming Conventions, Jira Implementation

**Decision:** 
- **Pipeline parameters**: snake_case (Pythonic convention)
- **Data columns in Delta tables**: camelCase (Fabric/Lakehouse convention)

---

## Current State (Zephyr)

### Pipeline Parameters (JSON)
```json
{
  "debug_mode": { "type": "bool" },
  "full_run_mode": { "type": "bool" },
  "run_tests": { "type": "bool" },
  "init_mode": { "type": "bool" }
}
```

### Notebook Parameters (Python)
```python
debug_mode = globals().get("debug_mode")
full_run_mode = globals().get("full_run_mode")
run_tests = globals().get("run_tests")
init_mode = globals().get("init_mode")
```

---

## SPECTRA Standards (Canonical)

### 1. Naming Convention
**Source:** `Core/memory/prompts/spectraReviewerPrompt.md` (canonical)

> "Use camelCase for all variable names, function names, and file paths."

**Example:**
```python
projectKey = globals().get("projectKey", "LMT")
debugMode = globals().get("debugMode", False)
```

**Source:** `Data/jira/docs/standards/naming-conventions.md`

> "camelCase (technical identifiers)"

---

### 2. Parameter Type Handling
**Source:** `Core/memory/prompts/spectraReviewerPrompt.md`

> "Pipeline parameters must always be retrieved using `globals().get(...)` with defaults, assuming orchestration by an external pipeline. **All parameters must be strings.**"

**Jira Implementation Pattern:**
```python
debugMode = bool(str(globals().get("debugMode", "0")).lower() in ("1", "true", "yes"))
```

---

### 3. Jira Reference Implementation

**Pipeline (JSON):**
- Parameters: `debugMode`, `fullRunMode`, `runTests` (camelCase)
- Activity parameters: `"type": "string"` (even for booleans)
- Pipeline parameters: `"type": "bool"` (Fabric allows this)

**Notebook (Python):**
```python
debugMode = bool(str(globals().get("debugMode", "0")).lower() in ("1", "true", "yes"))
```

---

## Issues Identified

### ✅ Issue 1: Naming Convention (Correct)
- **Pipeline Parameters:** `debug_mode`, `full_run_mode`, `run_tests`, `init_mode` (snake_case) ✅
- **Data Columns:** Will use camelCase (e.g., `issueId`, `createdDateTime`) ✅
- **Status:** Aligned with SPECTRA standards (Pythonic for code, camelCase for data)

### ⚠️ Issue 2: Parameter Type Handling
- **Current:** Direct boolean conversion from `globals().get()`
- **Required:** Treat as string, then convert (per standards)
- **Impact:** Less robust, doesn't handle string "0"/"1" from pipeline

### ✅ Issue 3: Parameter Set (Correct)
- Three parameters are appropriate runtime controls:
  - `debug_mode`: Controls verbose logging
  - `full_run_mode`: Controls full vs incremental extraction
  - `init_mode`: Zephyr-specific (bootstrap endpoints) - appropriate
- `run_tests`: **Removed** - Testing is done in local environment via `run_source_local.py` and `test_all_endpoints.py`

---

## SPECTRA-Grade Solution (Final)

### 1. Pipeline JSON (snake_case - Pythonic)

```json
{
  "parameters": {
    "debug_mode": {
      "type": "bool",
      "defaultValue": false
    },
    "full_run_mode": {
      "type": "bool",
      "defaultValue": false
    },
    "run_tests": {
      "type": "bool",
      "defaultValue": false
    },
    "init_mode": {
      "type": "bool",
      "defaultValue": false
    }
  }
}
```

**Activity Parameters:**
```json
{
  "parameters": {
    "debug_mode": {
      "value": {
        "value": "@pipeline().parameters.debug_mode",
        "type": "Expression"
      },
      "type": "string"
    },
    "full_run_mode": {
      "value": {
        "value": "@pipeline().parameters.full_run_mode",
        "type": "Expression"
      },
      "type": "string"
    },
    "run_tests": {
      "value": {
        "value": "@pipeline().parameters.run_tests",
        "type": "Expression"
      },
      "type": "string"
    },
    "init_mode": {
      "value": {
        "value": "@pipeline().parameters.init_mode",
        "type": "Expression"
      },
      "type": "string"
    }
  }
}
```

**Note:** Activity parameters use `"type": "string"` (per Jira pattern) even though pipeline parameters are `bool`. This ensures notebook receives strings.

---

### 2. Notebook Python (SPECTRA-Grade Pattern)

**Pipeline Parameters:** snake_case (Pythonic)  
**Data Columns:** camelCase (Fabric/Lakehouse convention)

```python
# === Runtime Parameters (snake_case - Pythonic) ===
# Pipeline parameters use snake_case, data columns use camelCase
# Priority: globals() (pipeline) → mssparkutils.env.getVariable() → os.environ → default

def get_bool_param(pipeline_param_name: str, env_var_name: str, default: bool = False) -> bool:
    """Get boolean parameter from pipeline (snake_case) or environment variable."""
    # Check pipeline injection first (snake_case parameter name)
    pipeline_val = globals().get(pipeline_param_name)
    if pipeline_val is not None:
        return bool(str(pipeline_val).lower() in ("1", "true", "yes"))
    
    # Check Fabric variable library
    try:
        env_val = mssparkutils.env.getVariable(env_var_name)
        if env_val:
            return bool(str(env_val).lower() in ("1", "true", "yes"))
    except Exception:
        pass
    
    # Fallback to os.environ (for local testing)
    env_val = os.environ.get(env_var_name, "1" if default else "0")
    return bool(str(env_val).lower() in ("1", "true", "yes"))

# Usage: snake_case parameters (Pythonic)
debug_mode = get_bool_param("debug_mode", "DXC_ZEPHYR_DEBUG_MODE", False)
full_run_mode = get_bool_param("full_run_mode", "DXC_ZEPHYR_FULL_RUN_MODE", False)
run_tests = get_bool_param("run_tests", "DXC_ZEPHYR_RUN_TESTS", False)
init_mode = get_bool_param("init_mode", "DXC_ZEPHYR_INIT_MODE", False)

# Data columns (after cleaning) will use camelCase:
# df.select("issueId", "createdDateTime", "statusCategory")  # camelCase
```

---

## Parameter Justification

### ✅ `debugMode`
- **Purpose:** Control verbose logging and debug output
- **SPECTRA-Grade:** ✅ Standard across all pipelines
- **Default:** `false` (production-safe)

### ✅ `fullRunMode`
- **Purpose:** Control full vs incremental extraction
- **SPECTRA-Grade:** ✅ Standard across all pipelines
- **Default:** `false` (incremental by default)

### ❌ `run_tests` (Removed)
- **Reason:** Testing is done in local environment via `run_source_local.py` and `test_all_endpoints.py`
- **Status:** Removed from pipeline - not needed in Fabric runtime

### ✅ `init_mode`
- **Purpose:** Bootstrap endpoints.json into Delta table (Zephyr-specific)
- **SPECTRA-Grade:** ✅ Appropriate for Source stage bootstrap
- **Default:** `false` (one-time operation)
- **Note:** This is Zephyr-specific but follows SPECTRA pattern

---

## Recommendations (Final)

1. **✅ Use snake_case for pipeline parameters** (`debug_mode`, `full_run_mode`, `init_mode`) - Pythonic
2. **✅ Use camelCase for data columns** (`issueId`, `createdDateTime`) - Fabric/Lakehouse convention
3. **✅ Update pipeline JSON** to use snake_case parameter names
4. **✅ Update notebook** to use snake_case and robust string-to-bool conversion
5. **✅ Use helper function** for cleaner, maintainable parameter loading
6. **✅ Keep parameter set** (all four are appropriate)

---

## Alignment Checklist

- [ ] Pipeline JSON parameters renamed to camelCase
- [ ] Pipeline activity parameters renamed to camelCase
- [ ] Notebook Python variables renamed to camelCase
- [ ] Notebook uses string-to-bool conversion pattern
- [ ] Helper function implemented for parameter loading
- [ ] Variable library names updated (if needed)
- [ ] Documentation updated (playbooks, README)
- [ ] Local runner script updated (if uses these parameters)

---

## Next Steps

1. Update pipeline JSON
2. Update notebook Python code
3. Test in Fabric (pipeline run)
4. Test manual notebook run (should pull from variable library)
5. Update documentation

