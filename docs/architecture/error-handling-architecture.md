# Error Handling Architecture - SPECTRA-Grade Design

**Date:** 2025-12-08  
**Status:** 🎯 Architectural Analysis  
**Purpose:** Determine the most SPECTRA-grade error handling architecture

---

## 🔍 Current State Analysis

### Existing SPECTRA Error Hierarchy

**Location:** `Core/shared/python/spectra-core/src/spectra_core/errors.py`

```python
SpectraError (base)
├── ValidationError
├── AuthenticationError
├── AuthorizationError
├── NotFoundError
├── ConfigurationError
└── ExternalServiceError
```

**Purpose:** Simple exceptions for raising/error handling  
**Structure:** Message + code only

---

### Current Pipeline Error Handling

**Pattern:** Simple try/except with string errors
```python
try:
    response = requests.get(url, headers=headers, timeout=timeout)
except Exception as e:
    logger.error(f"❌ Authentication failed: {str(e)}")
    return {"status": "Failed", "error": str(e)}
```

**Problems:**
- ❌ No structured error information
- ❌ No retry logic
- ❌ No error classification
- ❌ No error collection for graceful degradation

---

## 🎯 Requirements Analysis

### Two Different Needs

#### 1. **Exception Raising** (What exists)
- Raise exceptions when things fail
- Simple, standard Python exceptions
- Used for error handling/control flow

#### 2. **Error Tracking & Retry Logic** (New need)
- Structured error information (category, code, context)
- Retryable vs non-retryable classification
- Error collection for graceful degradation
- Activity logging

**Key Insight:** These are **complementary, not competing** needs!

---

## 🏗️ SPECTRA-Grade Architecture

### Principle: Separation of Concerns

**Exception Raising** → Use existing `SpectraError` hierarchy  
**Error Tracking** → New structured error class for operations

### Option 1: Single Structured Error Class ✅ (Recommended)

**Design:**
```python
class OperationError:
    """Structured error for pipeline operations (tracking, retry, logging)."""
    category: str  # "auth", "network", "data", "validation", "api"
    code: str      # "TIMEOUT", "RATE_LIMITED", etc.
    message: str
    context: Dict[str, Any]
    retryable: bool
    exception: Optional[Exception] = None  # Original exception if any
    stage: Optional[str] = None
    source_system: Optional[str] = None
```

**Usage:**
- Wrap exceptions when catching
- Collect errors without raising
- Classify for retry logic
- Log to activity tables

**Pros:**
- ✅ Single source of truth for structured errors
- ✅ Works for all stages/sources
- ✅ Simple, no hierarchy complexity
- ✅ Complements existing exception system

**Cons:**
- ⚠️ Different from existing error classes (but that's OK - different purpose)

---

### Option 2: Extend Existing Hierarchy ❌

**Design:**
```python
class SpectraError(Exception):
    # Add structured fields
    category: str
    context: Dict[str, Any]
    retryable: bool
    ...
```

**Problems:**
- ❌ Mixes exception raising with error tracking
- ❌ Breaks existing code that uses simple SpectraError
- ❌ Over-complicated for simple exception needs
- ❌ Not all errors need structured tracking

---

### Option 3: Separate Hierarchy ❌

**Design:**
```python
class PipelineError(SpectraError):
    """Base for pipeline errors"""
    
class APITimeoutError(PipelineError):
    """API timeout"""
    
class RateLimitError(PipelineError):
    """Rate limit"""
...
```

**Problems:**
- ❌ Too many classes for simple operations
- ❌ Over-engineering
- ❌ Hard to maintain
- ❌ Not SPECTRA-grade (keep it simple)

---

## ✅ Recommended Architecture

### Two Complementary Systems

#### 1. **Exception System** (Keep as-is)
```python
# For raising exceptions
raise AuthenticationError("Invalid credentials")
raise ValidationError("Missing required field")
```

**Used for:** Control flow, error propagation

#### 2. **Operation Error Tracking** (New)
```python
class OperationError:
    """Structured error for pipeline operations."""
    category: str
    code: str
    message: str
    context: Dict[str, Any]
    retryable: bool
    exception: Optional[Exception] = None
    stage: Optional[str] = None
    source_system: Optional[str] = None
```

**Used for:** Error tracking, retry logic, graceful degradation, activity logging

---

## 🔧 Integration Pattern

### Example: API Request with Error Tracking

```python
def validate_api_authentication(...):
    """Validate API authentication with error tracking."""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return {"status": "Success"}, data
    except requests.exceptions.Timeout as e:
        # Create structured error (for tracking/retry)
        error = OperationError(
            category="network",
            code="TIMEOUT",
            message=str(e),
            context={"endpoint": url, "timeout": timeout},
            retryable=True,
            exception=e,
            stage="source",
            source_system="zephyr"
        )
        
        # Optionally raise exception (for control flow)
        # raise ExternalServiceError("API", str(e))
        
        # Return structured error (for graceful degradation)
        return {"status": "Failed"}, None, error
```

---

## 🎯 Final Recommendation

### Single Class: `OperationError`

**Rationale:**
1. **Separation of Concerns** - Exceptions for raising, OperationError for tracking
2. **Single Responsibility** - One class, one purpose
3. **Modular** - Reusable across all stages/sources
4. **Simple** - No complex hierarchy
5. **SPECTRA-Grade** - Clear, focused, reusable

**Name Justification:**
- `OperationError` - Clear it's for operational error tracking
- Generic enough for all stages (Source, Prepare, Extract, etc.)
- Distinct from exception classes (different purpose)

---

## 📋 Implementation Plan

1. **Create `OperationError` class** in SDK
2. **Create `ErrorClassification` helper** - Classify exceptions → OperationError
3. **Create `APIRequestHandler`** - Wraps API calls, returns OperationError
4. **Create `ErrorCollector`** - Collects OperationError instances
5. **Keep existing exception system** - No changes needed

---

## ✅ Benefits

1. **Complements Existing System** - Doesn't break anything
2. **Clear Separation** - Exceptions for control flow, OperationError for tracking
3. **Reusable** - Works for all stages, all sources
4. **Simple** - One class, clear purpose
5. **SPECTRA-Grade** - Modular, focused, zero tech debt

---

**Version:** 1.0.0  
**Date:** 2025-12-08

