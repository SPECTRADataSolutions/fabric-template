# Error Handling Reusability Analysis

**Date:** 2025-12-08  
**Status:** 🔍 Analysis Complete  
**Purpose:** Ensure error handling is reusable across all SPECTRA source systems and stages

---

## 🔍 Current Design Review

### Classes Proposed

1. **`SourceStageError`** ❌ **NOT REUSABLE** - Name suggests source-specific
2. **`ErrorClassification`** ✅ **REUSABLE** - Generic HTTP/network error classification
3. **`APIRequestHandler`** ✅ **REUSABLE** - Generic API retry handler
4. **`ErrorCollector`** ✅ **REUSABLE** - Generic error aggregation

---

## 🎯 SPECTRA Source Systems

Found in codebase:
- ✅ **Zephyr** - Test management (`Data/zephyr/`)
- ✅ **Jira** - Issue tracking (`Data/jira/`)
- ✅ **UniFi** - Network management (`Data/unifi/`)
- ✅ **Xero** - Accounting (`Data/xero/`)

**All need:** API error handling, retry logic, graceful degradation

---

## 🎯 SPECTRA Stages

All 7 stages may need error handling:
- **Source** - API calls, authentication, endpoint validation
- **Prepare** - Schema discovery, validation
- **Extract** - Data extraction, pagination
- **Clean** - Data quality checks, validation
- **Transform** - Data transformation, type coercion
- **Refine** - Dimensional modeling, fact/dim creation
- **Analyse** - Aggregations, calculations

**All stages need:** Error collection, structured reporting, activity logging

---

## ✅ Generic Patterns Found

### Existing Reusable Pattern

**Location:** `Core/operations/src/bridge/retry.py`

**Classes:**
- `CircuitBreakerError` - Generic exception
- `retry_with_backoff()` - Generic decorator
- `CircuitBreaker` - Generic circuit breaker

**Usage:** Already used by `ServiceRegistry` and `FabricPaginator`

**Conclusion:** This is generic and reusable, but:
- Decorator pattern (not class-based)
- Doesn't handle HTTP status codes
- Doesn't classify errors
- Doesn't collect errors for graceful degradation

---

## 🔧 Revised Design: Fully Reusable

### Generic Naming Convention

1. **`SPECTRAError`** (not `SourceStageError`)
   - Generic error class for all stages
   - Can be used by Source, Prepare, Extract, etc.

2. **`ErrorClassification`** ✅ (keep as-is)
   - Generic HTTP/network error classification
   - Works for any API (Zephyr, Jira, UniFi, Xero)

3. **`APIRequestHandler`** ✅ (keep as-is)
   - Generic API retry handler
   - Works for any REST API

4. **`ErrorCollector`** ✅ (keep as-is)
   - Generic error aggregation
   - Works for any stage

---

## 📐 Reusability Matrix

| Component | Zephyr Source | Jira Source | UniFi Source | Xero Source | Other Stages |
|-----------|---------------|-------------|--------------|-------------|--------------|
| `SPECTRAError` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ErrorClassification` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `APIRequestHandler` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ErrorCollector` | ✅ | ✅ | ✅ | ✅ | ✅ |

**All components are reusable across all sources and stages.**

---

## 🏗️ Architecture Decision

### Option 1: Embedded in SDK Notebook (Current)
**Pros:**
- Available to all notebooks that `%run spectraSDK`
- Self-contained, no external dependencies
- Fast iteration

**Cons:**
- Duplicated across source systems (each has own SDK notebook)
- Not shared with non-notebook code (bridge, operations)

### Option 2: Shared in Core/operations (Recommended)
**Pros:**
- Single source of truth
- Reusable by bridge, operations, SDK notebooks
- Aligns with existing `retry.py` pattern

**Cons:**
- Requires importing from external module (not available in notebook)

### Option 3: Hybrid (Best SPECTRA-Grade)
**Pros:**
- SDK notebook has embedded version (for notebooks)
- Core/operations has shared version (for Python code)
- Both share same design/API
- Notebooks can embed, Python code can import

**Cons:**
- Need to keep in sync (but same implementation)

---

## ✅ Recommended Approach: Hybrid

### Implementation Strategy

1. **Create generic classes** in SDK with generic names
2. **Embed in SDK notebook** - Available to all notebooks
3. **Copy to Core/operations** - Available to Python code
4. **Keep API identical** - Same classes, same methods

### Generic Class Names

```python
# In SDK notebook (and Core/operations)
class SPECTRAError:  # Not SourceStageError
    """Generic error for all SPECTRA stages and sources."""
    category: str  # "auth", "network", "data", "validation", "api"
    code: str      # Error code
    message: str
    context: Dict[str, Any]
    retryable: bool
    stage: Optional[str] = None  # "source", "prepare", etc.
    source_system: Optional[str] = None  # "zephyr", "jira", etc.

class ErrorClassification:  # Generic
    """Classify errors for any API."""

class APIRequestHandler:  # Generic
    """Handle API requests with retry for any REST API."""

class ErrorCollector:  # Generic
    """Collect errors for any stage."""
```

---

## 📋 Reusability Checklist

- [x] Generic naming (not source/stage-specific)
- [x] Works for all source systems (Zephyr, Jira, UniFi, Xero)
- [x] Works for all stages (Source, Prepare, Extract, etc.)
- [x] Configurable (max_attempts, delays, etc.)
- [x] Type-safe (structured errors, not strings)
- [x] Modular (independent components)
- [x] Observable (full error context)

---

## 🎯 Next Steps

1. **Rename `SourceStageError` → `SPECTRAError`**
2. **Make all classes generic** (no source/stage assumptions)
3. **Embed in SDK notebook** (for notebooks)
4. **Optionally copy to Core/operations** (for Python code)
5. **Document reuse pattern** (how other sources/stages use it)

---

**Version:** 1.0.0  
**Date:** 2025-12-08

