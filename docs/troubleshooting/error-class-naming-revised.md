# Error Class Naming - Revised Analysis

**Date:** 2025-12-08  
**Status:** 🔍 Analysis  
**Purpose:** Find better naming than "SpectraError" for structured error tracking

---

## 🤔 The Problem

**Existing:** `SpectraError` is too broad/generic  
**Existing:** We have specific classes (ValidationError, AuthenticationError, etc.)  
**Question:** Do we even need a generic base class for tracking?

---

## 🎯 Analysis: Do We Need a New Class?

### Option 1: Use Existing Specific Classes ✅ (Best)

**Approach:** Extend existing specific classes (ValidationError, AuthenticationError, etc.) with structured fields

**Pros:**
- ✅ Semantic meaning (ValidationError is clear)
- ✅ Type safety (catch specific errors)
- ✅ No new classes needed
- ✅ Uses what exists

**Cons:**
- ⚠️ All classes need updating
- ⚠️ Need to choose right class for each error

**Implementation:**
```python
# Extend existing classes
class ValidationError(SpectraError):
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            code="VALIDATION_ERROR",
            category=kwargs.get("category", "validation"),
            context=kwargs.get("context", {}),
            retryable=False,
            **{k: v for k, v in kwargs.items() if k not in ("category", "context")}
        )

# Use directly - no generic class needed
error = ValidationError(
    message="Missing required field: id",
    context={"entity": "projects", "field": "id"},
    stage="source",
    source_system="zephyr"
)
```

---

### Option 2: Create Structured Error Wrapper ❌

**Approach:** Create a wrapper class that wraps existing errors

**Cons:**
- ❌ Adds complexity
- ❌ Two layers (error + wrapper)
- ❌ Not SPECTRA-grade (keep it simple)

---

### Option 3: Use Specific Classes Only ✅ (Recommended)

**Approach:** Always use specific error classes (ValidationError, AuthenticationError, ExternalServiceError)

**When creating errors:**
```python
# API timeout → ExternalServiceError
error = ExternalServiceError(
    service="Zephyr API",
    message="Request timed out",
    category="network",
    context={"endpoint": url, "timeout": 10},
    retryable=True,
    stage="source",
    source_system="zephyr"
)

# Data validation failure → ValidationError
error = ValidationError(
    message="Missing required field: id",
    category="data",
    context={"entity": "projects"},
    retryable=False,
    stage="source"
)

# Auth failure → AuthenticationError
error = AuthenticationError(
    message="Invalid credentials",
    category="auth",
    context={"endpoint": "/auth"},
    retryable=False,
    stage="source"
)
```

**Pros:**
- ✅ Semantic clarity
- ✅ No generic class needed
- ✅ Use existing hierarchy
- ✅ Type safety

**Cons:**
- ⚠️ Need to choose right class (but that's good - forces clear thinking)

---

## ✅ Recommendation: Use Existing Specific Classes

**Principle:** Use specific error classes, extend them with structured fields

**No new generic class needed!**

**Pattern:**
1. Extend existing classes (ValidationError, AuthenticationError, ExternalServiceError, etc.)
2. Add structured fields (category, context, retryable, stage, source_system)
3. Use specific classes based on error type
4. ErrorClassification returns appropriate specific class

**Example:**
```python
# ErrorClassification returns specific class
def classify_http_error(status_code: int, error: Exception, **kwargs):
    if status_code == 401:
        return AuthenticationError(
            message=str(error),
            category="auth",
            context={"status_code": status_code, **kwargs.get("context", {})},
            retryable=False,
            **{k: v for k, v in kwargs.items() if k != "context"}
        )
    elif status_code in {429, 500, 502, 503, 504}:
        return ExternalServiceError(
            service=kwargs.get("service", "API"),
            message=str(error),
            category="api",
            context={"status_code": status_code, **kwargs.get("context", {})},
            retryable=True,
            **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
        )
    else:
        return ValidationError(
            message=str(error),
            category="api",
            context={"status_code": status_code, **kwargs.get("context", {})},
            retryable=False,
            **{k: v for k, v in kwargs.items() if k != "context"}
        )
```

---

## 🎯 Final Design

**No "SpectraError" generic class needed!**

**Instead:**
1. Extend existing specific classes with structured fields
2. Use ErrorClassification to return appropriate specific class
3. ErrorCollector collects any SpectraError subclass (polymorphic)
4. Use specific classes based on error semantics

**Benefits:**
- ✅ Semantic clarity
- ✅ Type safety
- ✅ No generic class confusion
- ✅ Uses existing hierarchy

---

**Version:** 1.0.0  
**Date:** 2025-12-08

