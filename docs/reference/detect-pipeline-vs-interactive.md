# Detecting Pipeline vs Interactive Execution in Fabric

**Problem:** Auto-enable debug mode when running interactively in Fabric UI, but not in pipeline.

---

## 🎯 Use Cases

**Interactive Mode (Fabric UI):**
- Developer clicking "Run all" in notebook
- Manual cell execution for testing
- **Want:** Auto-enable debug mode for visibility

**Pipeline Mode (Automated):**
- Data Pipeline executing notebook
- Scheduled runs
- **Want:** Use pipeline parameter (explicit control)

---

## 🔍 Detection Methods

### Method 1: Check for Pipeline Parameters

```python
# In pipeline: Parameters are injected via @pipeline().parameters.debug
# In interactive: Parameters use notebook defaults

def is_running_in_pipeline() -> bool:
    """
    Detect if notebook is running in pipeline vs interactive.
    
    When running in pipeline, Fabric injects parameters.
    When running interactively, parameters have default values only.
    """
    # Check if parameters were explicitly passed (not defaults)
    # Problem: Can't distinguish between "pipeline passed False" and "interactive default False"
    
    # Try checking for pipeline-specific spark configs
    try:
        # Fabric might set these when running in pipeline
        activity_id = spark.conf.get("trident.activity.id", None)
        moniker_id = spark.conf.get("trident.moniker.id", None)
        operation_type = spark.conf.get("trident.operation.type", None)
        
        # If operation.type is "SessionCreation" - this is interactive
        # If operation.type is "PipelineRun" or similar - this is pipeline
        
        if operation_type == "SessionCreation":
            return False  # Interactive session
        elif activity_id and moniker_id:
            return True  # Likely pipeline
        else:
            return False  # Unknown, assume interactive
            
    except:
        return False  # Error, assume interactive

# Usage
_in_pipeline = is_running_in_pipeline()
_in_interactive = not _in_pipeline

# Auto-enable debug in interactive mode
if _in_interactive and not debug:
    debug = True
    log.info("ℹ️ Auto-enabled debug mode (running interactively in Fabric)")
```

**Status:** ⚠️ **Experimental** - Based on observed spark.conf keys

---

### Method 2: Check Operation Type

From error messages, we see:
```
trident.operation.type=SessionCreation
```

This suggests Fabric sets operation type:
- `SessionCreation` = Interactive notebook session
- `PipelineRun` (hypothetical) = Pipeline execution

```python
def is_interactive_session() -> bool:
    """Check if running in interactive Fabric session."""
    operation_type = spark.conf.get("trident.operation.type", "")
    return operation_type == "SessionCreation"

# Usage
if is_interactive_session():
    debug = True
```

**Status:** 🔄 **Needs validation** - Check if this works

---

### Method 3: Simplest (Just Remove Auto-Debug)

```python
# Don't auto-enable debug mode
# Users explicitly set debug=True when needed

# In pipeline: Pass debug parameter
# In interactive: Manually set debug=True in parameters cell
```

**Status:** ✅ **Always works** - Explicit control

---

## 🎯 Recommended Approach

**Option A: Try Method 2, fallback to explicit**
```python
# Check if interactive session
try:
    operation_type = spark.conf.get("trident.operation.type", "")
    _in_interactive = (operation_type == "SessionCreation")
except:
    _in_interactive = False

# Auto-enable debug in interactive mode
if _in_interactive and not debug:
    log.info("ℹ️ Auto-enabled debug mode (interactive Fabric session)")
    debug = True
```

**Option B: Remove auto-debug feature**
```python
# Just use debug parameter as-is
# No auto-detection
```

---

## 📝 Decision

**Test Method 2 first** - Check if `trident.operation.type` reliably indicates interactive vs pipeline.

If it doesn't work consistently, **remove the feature** and use explicit debug parameter control.

---

**Next Steps:**
1. Test in Fabric interactive mode - check `spark.conf.get("trident.operation.type")`
2. Test in pipeline mode - check if value changes
3. Implement if reliable, remove if not


