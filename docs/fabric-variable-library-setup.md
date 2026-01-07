# Fabric Variable Library Setup - Simple Guide

**Date:** 2025-12-03  
**Method:** Official Microsoft notebookutils.variableLibrary approach  
**Source:** [Microsoft Learn - Notebook Utilities](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-utilities)

---

## What You Need (Simple Version)

### 1. Variable Library Must Exist in Workspace ✅

**Already have:** `zephyrVariables` with:

- `DXC_ZEPHYR_BASE_URL`
- `DXC_ZEPHYR_BASE_PATH`
- `DXC_ZEPHYR_API_TOKEN`

**Status:** ✅ Done (you showed me this already)

---

### 2. Notebook Loads It Directly (Code-Based)

**The notebook now uses this code:**

```python
from notebookutils import variableLibrary

# Get the library
zephyr_vars = variableLibrary.getLibrary("zephyrVariables")

# Access credentials
zephyr_base_url = zephyr_vars.DXC_ZEPHYR_BASE_URL
zephyr_base_path = zephyr_vars.DXC_ZEPHYR_BASE_PATH
zephyr_api_token = zephyr_vars.DXC_ZEPHYR_API_TOKEN
```

**Status:** ✅ Updated in notebook

---

### 3. Pipeline Configuration (Simplified!)

**You DON'T need:**

- ❌ Library variables tab mapping (ignore it!)
- ❌ Credential parameters in Base parameters (remove them!)

**You ONLY need:**

- ✅ Base parameters for mode flags

**Settings → Base parameters should have:**

| Name                 | Type   | Value                              |
| -------------------- | ------ | ---------------------------------- |
| `init_mode`          | String | `@pipeline().parameters.init_mode` |
| `debug_mode`         | String | `false`                            |
| `full_run`           | String | `false`                            |
| `test_all_endpoints` | String | `false`                            |
| `extract_sample`     | String | `false`                            |

**That's it!** NO credentials in pipeline config.

---

## What to Do Now in Fabric

### Step 1: Remove Credential Parameters (If You Added Them)

**In pipeline → notebook activity → Settings → Base parameters:**

Delete these if present:

- ❌ `zephyr_base_url`
- ❌ `zephyr_base_path`
- ❌ `zephyr_api_token`

**Keep only:**

- ✅ `init_mode`
- ✅ `debug_mode`
- ✅ `full_run` (or `full_run_mode` - rename to `full_run` to match notebook)

### Step 2: Ignore Library Variables Tab

**Library variables tab can be empty!** The `notebookutils.variableLibrary.getLibrary()` call doesn't need it.

### Step 3: Sync Updated Notebook

**Push to git:**

```bash
cd Data/zephyr
git add sourceZephyr.Notebook/
git commit -m "Use official notebookutils.variableLibrary method"
git push
```

**Then in Fabric:**

- Sync workspace from git
- Open sourceZephyr notebook
- **Toggle Cell 1 as "parameters"** (the tag thing we documented)
- Save

### Step 4: Run Pipeline

**Should work now!** The notebook will:

1. Receive mode flags from pipeline (init_mode, etc.)
2. Load credentials directly from Variable Library
3. No complex parameter mapping needed

---

## Why This is Better

**Old approach (what I was suggesting):**

```
Variable Library → Link in tab → Map in Base Parameters → Hope it works
```

**New approach (Microsoft's official way):**

```
Variable Library → Notebook loads it directly → Done
```

**Benefits:**

- ✅ Simpler configuration
- ✅ No parameter mapping errors
- ✅ More reliable (less UI state to lose)
- ✅ Official documented method

---

## Troubleshooting

### Error: "AttributeError: 'VariableLibrary' object has no attribute 'DXC_ZEPHYR_BASE_URL'"

**Cause:** Variable doesn't exist in library

**Fix:**

1. Go to workspace
2. Open zephyrVariables
3. Verify variables exist
4. Check spelling matches exactly

### Error: "ValueError: Library 'zephyrVariables' not found"

**Cause:** Variable Library doesn't exist or wrong name

**Fix:**

1. Check library name is exactly "zephyrVariables"
2. Verify library is in same workspace as notebook
3. Check you have access to library

### Error: Still saying missing credentials

**Cause:** Variable Library values are empty

**Fix:**

1. Open zephyrVariables
2. Check Default values are populated
3. Verify active value set has values

---

## Complete Checklist

**In Fabric (one-time setup):**

- [x] Variable Library "zephyrVariables" exists
- [x] Has DXC_ZEPHYR_BASE_URL (with value)
- [x] Has DXC_ZEPHYR_BASE_PATH (with value)
- [x] Has DXC_ZEPHYR_API_TOKEN (with value)
- [ ] Notebook synced from git
- [ ] Cell 1 toggled as "parameters"
- [ ] Pipeline Base parameters has mode flags ONLY
- [ ] Run pipeline

**Should work!** ✅

---

## Quick Summary

**What changed:**

- Removed credentials from Cell 1 parameters
- Notebook loads credentials using `notebookutils.variableLibrary.getLibrary()`
- No pipeline parameter mapping needed
- Simpler and more reliable

**What you need to do:**

1. Sync notebook from git
2. Toggle Cell 1 as "parameters"
3. Remove any credential parameters from pipeline Base parameters
4. Run pipeline

**It should just work now!** The official Microsoft method is much simpler.
