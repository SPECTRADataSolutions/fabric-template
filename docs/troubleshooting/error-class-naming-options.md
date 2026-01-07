# Error Class Naming Options

**Date:** 2025-12-08  
**Purpose:** Find the best name for the generic error class

---

## 🎯 Requirements

1. **Generic** - Works for all stages and sources
2. **Clear** - Immediately understandable
3. **Concise** - Not too verbose
4. **Conventional** - Follows Python naming patterns
5. **Contextual** - Indicates SPECTRA/operational context

---

## 📋 Option Comparison

### Option 1: `StageError`
**Pros:**
- ✅ Simple, concise
- ✅ Clear - indicates stage operations
- ✅ Generic - works for all stages

**Cons:**
- ⚠️ Doesn't indicate SPECTRA context
- ⚠️ Might be confused with "stage" as in theater/development stage

**Usage:**
```python
error = StageError(
    category="api",
    code="TIMEOUT",
    message="Request timed out",
    context={"endpoint": "/projects"},
    retryable=True,
    stage="source",
    source_system="zephyr"
)
```

---

### Option 2: `ExecutionError`
**Pros:**
- ✅ Generic - works for any execution context
- ✅ Clear - indicates runtime/execution errors
- ✅ Concise

**Cons:**
- ⚠️ Very generic (might be confused with standard Python errors)
- ⚠️ Doesn't indicate structured/contextual nature

**Usage:**
```python
error = ExecutionError(
    category="api",
    code="TIMEOUT",
    ...
)
```

---

### Option 3: `PipelineError`
**Pros:**
- ✅ Clear SPECTRA context (data pipeline)
- ✅ Generic - works for all pipeline stages
- ✅ Concise

**Cons:**
- ⚠️ "Pipeline" might be ambiguous (CI/CD vs data pipeline)

**Usage:**
```python
error = PipelineError(
    category="api",
    code="TIMEOUT",
    ...
)
```

---

### Option 4: `OperationError`
**Pros:**
- ✅ Generic - works for any operation
- ✅ Clear - indicates operational context
- ✅ Concise

**Cons:**
- ⚠️ Very generic (might conflict with standard library concepts)

**Usage:**
```python
error = OperationError(
    category="api",
    code="TIMEOUT",
    ...
)
```

---

### Option 5: `SPECTRAStageError`
**Pros:**
- ✅ Explicit SPECTRA context
- ✅ Clear stage association
- ✅ Unambiguous

**Cons:**
- ⚠️ Verbose (long name)
- ⚠️ "Stage" might be redundant (could just be SPECTRAError)

**Usage:**
```python
error = SPECTRAStageError(
    category="api",
    code="TIMEOUT",
    ...
)
```

---

### Option 6: `TaskError`
**Pros:**
- ✅ Generic - works for any task
- ✅ Concise
- ✅ Clear - indicates discrete operation

**Cons:**
- ⚠️ Too generic (doesn't indicate SPECTRA context)
- ⚠️ Might be confused with task queues/jobs

**Usage:**
```python
error = TaskError(
    category="api",
    code="TIMEOUT",
    ...
)
```

---

### Option 7: `ProcessingError`
**Pros:**
- ✅ Generic - works for data processing operations
- ✅ Clear - indicates processing context
- ✅ Concise

**Cons:**
- ⚠️ Very generic (might be too broad)
- ⚠️ Doesn't indicate structured/contextual nature

**Usage:**
```python
error = ProcessingError(
    category="api",
    code="TIMEOUT",
    ...
)
```

---

### Option 8: `ContextualError`
**Pros:**
- ✅ Descriptive - emphasizes structured context
- ✅ Generic - works for any context
- ✅ Clear - indicates rich error information

**Cons:**
- ⚠️ Verbose
- ⚠️ Doesn't indicate SPECTRA/pipeline context

**Usage:**
```python
error = ContextualError(
    category="api",
    code="TIMEOUT",
    ...
)
```

---

## 🏆 Top Recommendations

### 1. `StageError` ⭐ (Best Balance)
- Simple, clear, concise
- Immediately understood in SPECTRA context
- Works for all stages and sources
- **Verdict:** Best choice for SPECTRA notebooks

### 2. `PipelineError` ⭐ (Second Choice)
- Clear SPECTRA context
- Generic enough for all stages
- Slightly more specific than `StageError`

### 3. `ExecutionError` (Third Choice)
- Very generic
- Clear operational context
- Might be too generic

---

## 🎯 Recommendation: `StageError`

**Rationale:**
1. **Concise** - Short and easy to type
2. **Clear** - In SPECTRA context, "stage" is well-understood
3. **Generic** - Works for Source, Prepare, Extract, etc.
4. **Conventional** - Follows Python `*Error` naming pattern
5. **Flexible** - Can be used across all sources (Zephyr, Jira, UniFi, Xero)

**With Context Fields:**
```python
class StageError:
    """Structured error for SPECTRA pipeline stage operations."""
    category: str
    code: str
    message: str
    context: Dict[str, Any]
    retryable: bool
    stage: Optional[str] = None  # "source", "prepare", etc.
    source_system: Optional[str] = None  # "zephyr", "jira", etc.
```

The `stage` and `source_system` fields provide context, so the class name can be generic.

---

## ✅ Final Decision

**Recommended Name:** `StageError`

**Alternative if you prefer explicit SPECTRA branding:** `PipelineError`

---

**Version:** 1.0.0  
**Date:** 2025-12-08

