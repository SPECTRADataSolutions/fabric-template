# Error Handling - Using Existing SpectraError

**Date:** 2025-12-08  
**Status:** 🎯 Design Decision  
**Purpose:** Extend existing `SpectraError` instead of creating new class

---

## 🎯 Decision: Extend Existing System

**Principle:** Use what exists, extend as needed

**Existing:** `SpectraError` (message + code)  
**Extend:** Add structured fields (category, context, retryable, etc.)

---

## 📐 Extended SpectraError Design

### Current Structure
```python
class SpectraError(Exception):
    def __init__(self, message: str, code: str = "SPECTRA_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)
```

### Extended Structure
```python
class SpectraError(Exception):
    """Base exception for all SPECTRA errors with structured tracking."""
    
    def __init__(
        self,
        message: str,
        code: str = "SPECTRA_ERROR",
        category: Optional[str] = None,  # "auth", "network", "data", etc.
        context: Optional[Dict[str, Any]] = None,
        retryable: bool = False,
        stage: Optional[str] = None,
        source_system: Optional[str] = None,
    ):
        self.message = message
        self.code = code
        self.category = category
        self.context = context or {}
        self.retryable = retryable
        self.stage = stage
        self.source_system = source_system
        super().__init__(message)
```

---

## ✅ Benefits

1. **Single System** - One error class for everything
2. **Backward Compatible** - Existing code still works (optional fields)
3. **Unified** - Same class for raising AND tracking
4. **SPECTRA-Grade** - Use what exists, extend as needed

---

## 🔧 Usage Examples

### Simple Usage (Existing Code Still Works)
```python
raise ValidationError("Missing required field")
# Still works - category, context, etc. are optional
```

### Structured Usage (New Capability)
```python
raise SpectraError(
    message="Request timed out",
    code="TIMEOUT",
    category="network",
    context={"endpoint": url, "timeout": 10},
    retryable=True,
    stage="source",
    source_system="zephyr"
)
```

### In Exception Handling
```python
try:
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
except requests.exceptions.Timeout as e:
    # Create structured error
    error = SpectraError(
        message=str(e),
        code="TIMEOUT",
        category="network",
        context={"endpoint": url},
        retryable=True,
        stage="source",
        source_system="zephyr"
    )
    # Can raise it
    raise error
    # Or return it for tracking
    return {"status": "Failed"}, None, error
```

---

## 🔄 Migration Strategy

1. **Extend SpectraError** - Add optional fields
2. **Update ErrorClassification** - Return SpectraError instances
3. **Update APIRequestHandler** - Return SpectraError instances
4. **Existing Code** - Continues to work (backward compatible)

---

## 📋 Implementation

### Location: `Core/shared/python/spectra-core/src/spectra_core/errors.py`

**Change:** Add optional parameters to `SpectraError.__init__()`

**Backward Compatibility:** All parameters optional except `message`

---

**Version:** 1.0.0  
**Date:** 2025-12-08

