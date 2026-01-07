# Test Project Configuration: SPECTRA-Grade Pattern

## Overview

The `TEST_PROJECT_ID` is **locked to project 45** for this environment and stored in the **Variable Library**, not as a pipeline parameter.

## Why Variable Library, Not Pipeline Parameters?

### ❌ Anti-Pattern: Pipeline Parameters for Constants

**Don't use pipeline parameters for environment-specific constants:**
- Pipeline parameters are for **runtime decisions** (e.g., `bootstrap=True`, `preview=False`)
- Constants belong in **configuration**, not parameters
- Makes it harder to change per-environment without modifying code

### ✅ SPECTRA-Grade Pattern: Variable Library

**Use Variable Library for environment configuration:**
- **Centralized**: All environment config in one place
- **Environment-specific**: Easy to change per environment without code changes
- **Version-controlled**: Variable Library is in Git, but values can be overridden in Fabric UI
- **Type-safe**: SDK reads from Variable Library with type checking

## Configuration

**Variable Library:** `zephyrVariables.VariableLibrary/variables.json`

```json
{
  "name": "TEST_PROJECT_ID",
  "note": "SpectraTestProject ID - locked to project 45 for this environment. Environment-specific constant, NOT a pipeline parameter.",
  "type": "String",
  "value": "45"
}
```

## Usage

### In Scripts

```python
from scripts.zephyr_utils import get_test_project_id

# Get locked project ID
project_id = get_test_project_id()  # Returns 45
```

### In Notebooks

```python
from spectraSDK import VariableLibrary

variables = VariableLibrary("zephyrVariables")
test_project_id = int(variables.get("TEST_PROJECT_ID"))  # Returns "45" as int
```

## Security Note

**Project ID 45 is locked** for this environment. All scripts and notebooks should use this ID via Variable Library, not hardcoded or parameterized values.

## Migration from Pipeline Parameters

If you previously used `project_id` as a pipeline parameter:

1. ❌ **Remove** `project_id` from pipeline parameters
2. ✅ **Add** `TEST_PROJECT_ID` to Variable Library
3. ✅ **Update** notebooks/scripts to read from Variable Library
4. ✅ **Lock** to project 45 for this environment

## Examples

### ✅ Correct (SPECTRA-Grade)

```python
# Script reads from Variable Library
project_id = get_test_project_id()  # Always 45 in this environment
```

### ❌ Incorrect (Anti-Pattern)

```python
# Hardcoded
project_id = 45  # ❌ Not flexible per environment

# Pipeline parameter
project_id = pipeline_params.get("project_id")  # ❌ Runtime decision, not config
```

## Benefits

1. **Environment Isolation**: Different environments can have different test project IDs
2. **Configuration Override**: Values can be changed in Fabric UI without Git commits
3. **Single Source of Truth**: Variable Library is the canonical config source
4. **SPECTRA-Grade**: Follows SPECTRA's configuration pattern (centralized, type-safe)

