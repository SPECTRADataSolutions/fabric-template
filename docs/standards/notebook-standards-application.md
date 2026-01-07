# SPECTRA Notebook Standards Application Guide

**Version:** 1.0  
**Status:** ✅ Active  
**Purpose:** Define what "apply notebook standards" means and how to do it

---

## Overview

When you say **"apply notebook standards"**, this document defines exactly what will be done to make a notebook SPECTRA-grade.

**Canonical Reference:** `sourceZephyr.Notebook/notebook_content.py`

---

## What "Apply Notebook Standards" Does

### 1. **Structure Compliance** ✅

**Applies:** `NOTEBOOK-FORMATTING-STANDARD.md`

- ✅ Header block with METADATA (kernel, lakehouse, environment)
- ✅ Markdown documentation block (stage title, description, outputs)
- ✅ SDK import cell (isolated, `%run spectraSDK`)
- ✅ Parameters cell with type hints and inline comments
- ✅ Context cell (`NotebookSession.load_context()`)
- ✅ Initialize cell (`session.initialize()`)
- ✅ Execute cell(s) (main stage logic)
- ✅ Validate cell (`session.validate()`)
- ✅ Record cell (`session.record(spark=spark)`)
- ✅ Finalise cell (`session.finalise()`)
- ✅ METADATA block after every code cell
- ✅ Section headers with SPECTRA suffix (`# == N. SECTION =================================================== SPECTRA`)

---

### 2. **Code Extraction to SDK** 🔧

**Extracts all reusable logic to SDK helpers:**

#### **Helper Functions** → `PrepareStageHelpers` class in SDK

**Functions to extract:**
- `generate_target_name()` - Generate SPECTRA target field names
- `singularize()` - Convert plural to singular for dimensions
- `infer_spectra_type()` - Infer SPECTRA data types from Python values
- `determine_group()` - Determine logical grouping and sort order

**Location:** `Data/fabric-sdk/src/spectra_fabric_sdk/stages/prepare_helpers.py`

**Format:**
```python
class PrepareStageHelpers:
    """SPECTRA-grade Prepare stage helpers."""
    
    @staticmethod
    def generate_target_name(field_name: str, prop_name: str = None, is_array: bool = False) -> str:
        """
        Generate target field name following SPECTRA explicit naming convention.
        
        Args:
            field_name: Source field name (e.g., "id", "name", "cyclePhases")
            prop_name: Nested property name (e.g., "id", "name")
            is_array: Whether this is an array field
            
        Returns:
            Target field name (e.g., "cycleId", "cycleName", "cyclePhaseId")
        """
        # Implementation...
```

#### **Stage Logic** → `PrepareStageHelpers.execute_prepare_stage()`

**Logic to extract:**
- Schema discovery from samples (`discover=True` mode)
- Intelligence loading from SDK (normal mode)
- Schema enhancement from source samples
- Prepare table creation (`prepare._schema`, `prepare._dependencies`, `prepare._constraints`)
- Prepare table validation

**Location:** `Data/fabric-sdk/src/spectra_fabric_sdk/stages/prepare_helpers.py`

**Format:**
```python
class PrepareStageHelpers:
    """SPECTRA-grade Prepare stage helpers."""
    
    @staticmethod
    def execute_prepare_stage(
        spark,
        session: NotebookSession,
        discover: bool = False
    ) -> None:
        """
        Execute Prepare stage - load intelligence and create Prepare tables.
        
        Args:
            spark: SparkSession
            session: NotebookSession instance
            discover: If True, build schema from samples; if False, load from intelligence
        """
        log = session.log
        
        if discover:
            PrepareStageHelpers._discover_schema_from_samples(spark, session)
        else:
            PrepareStageHelpers._load_intelligence_from_sdk(session)
        
        if session.params.get("bootstrap", True):
            PrepareStageHelpers._create_prepare_tables(spark, session)
            PrepareStageHelpers._validate_prepare_tables(spark, session)
```

#### **Notebook Simplification**

**Before (inline code):**
```python
# == 4. EXECUTE ====================================================== SPECTRA

log.info("=" * 80)
if discover:
    log.info("DISCOVERY MODE: Building perfect schema from sample data...")
    # ... 500+ lines of inline code ...
else:
    log.info("Loading API Intelligence from SDK...")
    # ... 200+ lines of inline code ...
```

**After (SDK helper):**
```python
# == 4. EXECUTE ====================================================== SPECTRA

PrepareStageHelpers.execute_prepare_stage(
    spark=spark,
    session=session,
    discover=discover
)
```

---

### 3. **Logging Standards** 📝

**Applies:** `sourceZephyr` logging principles

#### **Logging Pattern**

**Before (inconsistent):**
```python
log.info("=" * 80)
log.info("Creating Prepare stage tables...")
log.info("=" * 80)
log.info("== Creating prepare._schema DataFrame...")
log.info(f"  == Schema fields: {schema_count}")
log.info("  >> Writing prepare._schema to Delta...")
log.info("  OK prepare._schema created")
```

**After (SPECTRA-grade, matches sourceZephyr):**
```python
log.info("=" * 80)
log.info("Creating Prepare stage tables from enhanced intelligence...")
log.info("=" * 80)
log.info("== Creating prepare._schema DataFrame...")
log.info(f"  == Schema fields: {schema_count}")
log.info("  >> Writing prepare._schema to Delta...")
log.info("  OK prepare._schema created")
```

#### **Log Message Format**

- ✅ Section headers: `log.info("=" * 80)` and `log.info("SECTION NAME")`
- ✅ Subsection headers: `log.info("== Subsection name...")`
- ✅ Actions: `log.info("  >> Action description...")`
- ✅ Success: `log.info("  OK Success message")`
- ✅ Warnings: `log.warning("  !! WARNING: Message")`
- ✅ Errors: `log.error("  !! ERROR: Message")`
- ✅ Info: `log.info("  == Info message")`

**No Unicode/emoji characters** - Use ASCII equivalents:
- ✅ `==` (not `ƒôè`)
- ✅ `>>` (not `ƒÆ¥`)
- ✅ `OK` (not `Ô£à`)
- ✅ `!!` (not `ÔØî`)

---

### 4. **Code Quality** ✨

#### **Docstrings**

**Every function/class gets SPECTRA-grade docstrings:**

```python
def generate_target_name(field_name: str, prop_name: str = None, is_array: bool = False) -> str:
    """
    Generate target field name following SPECTRA explicit naming convention.
    
    Args:
        field_name: Source field name (e.g., "id", "name", "cyclePhases")
        prop_name: Nested property name (e.g., "id", "name")
        is_array: Whether this is an array field
        
    Returns:
        Target field name (e.g., "cycleId", "cycleName", "cyclePhaseId")
        
    Examples:
        >>> generate_target_name("id", None, False)
        "cycleId"
        >>> generate_target_name("cyclePhases", "id", True)
        "cyclePhaseId"
    """
```

#### **Type Hints**

**All functions have complete type hints:**

```python
def infer_spectra_type(value: Any, is_array_element: bool = False) -> str:
    """
    Infer SPECTRA data type from Python value.
    
    Args:
        value: Python value (bool, int, float, str, list, dict)
        is_array_element: Whether this is an array element
        
    Returns:
        SPECTRA data type ("bool", "int64", "float64", "text", "array<...>")
    """
```

#### **Error Handling**

**All functions have proper error handling:**

```python
try:
    # Operation
    log.info("  OK Operation succeeded")
except Exception as e:
    log.error(f"  !! Operation failed: {e}")
    raise
```

---

### 5. **Module Organisation** 📦

#### **SDK Structure**

**New file:** `Data/fabric-sdk/src/spectra_fabric_sdk/stages/prepare_helpers.py`

```python
"""
SPECTRA Prepare Stage Helpers.

Provides SPECTRA-grade functions for Prepare stage execution:
- Schema discovery from samples
- Intelligence loading from SDK
- Prepare table creation
- Prepare table validation
"""

from typing import Any, Dict, List, Optional, Tuple
from spectra_fabric_sdk.session import NotebookSession


class PrepareStageHelpers:
    """SPECTRA-grade Prepare stage helpers."""
    
    @staticmethod
    def execute_prepare_stage(spark, session: NotebookSession, discover: bool = False) -> None:
        """Execute Prepare stage - main entry point."""
        # Implementation...
    
    @staticmethod
    def _discover_schema_from_samples(spark, session: NotebookSession) -> List[Dict]:
        """Discover schema from sample data (discover=True mode)."""
        # Implementation...
    
    @staticmethod
    def _load_intelligence_from_sdk(session: NotebookSession) -> List[Dict]:
        """Load intelligence from SDK (normal mode)."""
        # Implementation...
    
    # ... more helper methods ...
```

#### **SDK Export**

**Update:** `Data/fabric-sdk/src/spectra_fabric_sdk/_init_.py`

```python
from .stages.prepare_helpers import PrepareStageHelpers

__all__ = [
    # ... existing exports ...
    "PrepareStageHelpers",
]
```

---

## Step-by-Step Application Process

### **Step 1: Scan Notebook for Modules**

**Identify:**
- Helper functions (standalone functions)
- Inline logic (should be in SDK)
- Logging patterns (should match sourceZephyr)

**Output:** List of functions/modules to extract

---

### **Step 2: Create SDK Helpers**

**Create:** `Data/fabric-sdk/src/spectra_fabric_sdk/stages/prepare_helpers.py`

**Extract:**
- All helper functions → `PrepareStageHelpers` class methods
- All stage logic → `PrepareStageHelpers.execute_prepare_stage()`
- All validation → `PrepareStageHelpers._validate_prepare_tables()`

**Format:**
- SPECTRA-grade docstrings
- Complete type hints
- Proper error handling
- Logging matches sourceZephyr pattern

---

### **Step 3: Update Notebook**

**Replace inline code with SDK helper call:**

**Before:**
```python
# == 4. EXECUTE ====================================================== SPECTRA

# 500+ lines of inline code...
```

**After:**
```python
# == 4. EXECUTE ====================================================== SPECTRA

PrepareStageHelpers.execute_prepare_stage(
    spark=spark,
    session=session,
    discover=discover
)
```

---

### **Step 4: Fix Logging**

**Update all log messages to match sourceZephyr:**
- Remove Unicode/emoji characters
- Use consistent format (==, >>, OK, !!)
- Match sourceZephyr logging style

---

### **Step 5: Verify Structure**

**Check compliance with `NOTEBOOK-FORMATTING-STANDARD.md`:**
- ✅ All required cells present
- ✅ All METADATA blocks present
- ✅ Section headers correct
- ✅ Parameters have type hints
- ✅ Logging matches sourceZephyr

---

## Summary: What Gets Done

When you say **"apply notebook standards"**, we:

1. ✅ **Extract all code to SDK** - Create `PrepareStageHelpers` class
2. ✅ **Simplify notebook** - Replace inline code with `PrepareStageHelpers.execute_prepare_stage()`
3. ✅ **Fix logging** - Match sourceZephyr logging pattern (ASCII, consistent format)
4. ✅ **Add docstrings** - SPECTRA-grade docstrings for all functions
5. ✅ **Add type hints** - Complete type hints for all functions
6. ✅ **Verify structure** - Ensure compliance with `NOTEBOOK-FORMATTING-STANDARD.md`
7. ✅ **Test** - Verify notebook still works after extraction

**Result:** Notebook matches `sourceZephyr` canonical format - clean, minimal, SDK-driven.

---

## Next Steps

**For prepareZephyr notebook:**

1. Scan for all modules/functions
2. Create `PrepareStageHelpers` in SDK
3. Extract all logic to SDK
4. Simplify notebook to match sourceZephyr
5. Fix logging to match sourceZephyr
6. Test and verify

---

## Version History

- **v1.0** (2025-12-10): Initial standard application guide

---

## References

- **Notebook Formatting Standard:** `docs/standards/NOTEBOOK-FORMATTING-STANDARD.md`
- **Canonical Example:** `sourceZephyr.Notebook/notebook_content.py`
- **SDK Location:** `Data/fabric-sdk/src/spectra_fabric_sdk/`

