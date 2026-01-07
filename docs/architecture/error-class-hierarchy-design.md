# Error Class Hierarchy Design

**Date:** 2025-12-08  
**Status:** 🎯 Design Analysis  
**Purpose:** Determine if we need specific error classes vs. single class with codes

---

## 🔍 Current SPECTRA Error Hierarchy

```python
SpectraError (base)
├── ValidationError
├── AuthenticationError
├── AuthorizationError
├── NotFoundError
├── ConfigurationError
└── ExternalServiceError
```

**Purpose:** Semantic error types - can catch specific errors

---

## 🤔 Question: Do We Need Specific Classes?

### Option 1: Keep Hierarchy ✅ (Recommended)

**Design:**
- Keep existing specific classes (ValidationError, AuthenticationError, etc.)
- Extend base `SpectraError` with structured fields
- All subclasses inherit structured fields

**Pros:**
- ✅ Semantic clarity - `catch ValidationError` is clear
- ✅ Type safety - Can catch specific error types
- ✅ Existing code continues to work
- ✅ Flexible - Can catch specific or general

**Usage:**
```python
# Specific error class (semantic)
raise ValidationError("Missing required field", category="validation", retryable=False)

# Can catch specifically
try:
    validate_data()
except ValidationError as e:
    # Handle validation errors specifically
    handle_validation_error(e)

# Or catch generally
except SpectraError as e:
    # Handle any SPECTRA error, use structured fields
    if e.retryable:
        retry_operation()
```

---

### Option 2: Single Class with Codes ❌

**Design:**
- Only `SpectraError` class
- Use `code` field for classification

**Pros:**
- ✅ Simpler - one class

**Cons:**
- ❌ Lose semantic meaning
- ❌ Can't catch specific error types
- ❌ Breaking change for existing code
- ❌ Less type-safe

**Usage:**
```python
# All errors are SpectraError
raise SpectraError("Missing required field", code="VALIDATION_ERROR")

# Must check code manually
try:
    validate_data()
except SpectraError as e:
    if e.code == "VALIDATION_ERROR":
        handle_validation_error(e)
    elif e.code == "AUTHENTICATION_ERROR":
        handle_auth_error(e)
    # Less clean than specific classes
```

---

## ✅ Recommended: Keep Hierarchy + Extend Base

### Extended Design

```python
class SpectraError(Exception):
    """Base exception for all SPECTRA errors with structured tracking."""
    
    def __init__(
        self,
        message: str,
        code: str = "SPECTRA_ERROR",
        category: Optional[str] = None,
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


class ValidationError(SpectraError):
    """Raised when input validation fails"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            code="VALIDATION_ERROR",
            category=kwargs.get("category", "validation"),
            retryable=False,  # Validation errors are not retryable
            **{k: v for k, v in kwargs.items() if k != "category"}
        )


class AuthenticationError(SpectraError):
    """Raised when authentication fails"""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(
            message,
            code="AUTHENTICATION_ERROR",
            category=kwargs.get("category", "auth"),
            retryable=False,  # Auth errors are not retryable
            **{k: v for k, v in kwargs.items() if k != "category"}
        )


class ExternalServiceError(SpectraError):
    """Raised when an external service call fails"""
    
    def __init__(self, service: str, message: str, **kwargs):
        super().__init__(
            f"{service}: {message}",
            code="EXTERNAL_SERVICE_ERROR",
            category=kwargs.get("category", "api"),
            context={**kwargs.get("context", {}), "service": service},
            **{k: v for k, v in kwargs.items() if k not in ("category", "context")}
        )
        self.service = service
```

---

## 🎯 When to Use What

### Use Specific Classes When:
- ✅ Need semantic meaning (`ValidationError` is clearer than `code="VALIDATION_ERROR"`)
- ✅ Want to catch specific error types
- ✅ Need type safety in exception handling
- ✅ Error type has default properties (e.g., `retryable=False` for ValidationError)

### Use Structured Fields When:
- ✅ Need tracking/retry logic (check `retryable` flag)
- ✅ Need context for logging/debugging
- ✅ Need stage/source_system for activity logging
- ✅ Error classification (check `category`)

---

## 📊 Best Practice Pattern

```python
# Create specific error with structured fields
try:
    validate_api_response(data)
except ValueError as e:
    raise ValidationError(
        message=f"Invalid response format: {str(e)}",
        context={"endpoint": url, "response_size": len(data)},
        stage="source",
        source_system="zephyr"
    ) from e

# Can catch specifically
try:
    process_data()
except ValidationError as e:
    logger.warning(f"Validation failed: {e.message}")
    # e.retryable is False (from ValidationError default)
    # e.category is "validation" (from ValidationError default)
    return None

# Or catch generally and use structured fields
except SpectraError as e:
    if e.retryable:
        # Retry logic
        retry_operation()
    else:
        # Log and continue
        logger.error(f"{e.category} error: {e.message}", extra=e.context)
```

---

## ✅ Final Recommendation

**Keep the hierarchy** - Best of both worlds:
1. **Semantic classes** - Clear meaning, type safety
2. **Structured fields** - Tracking, retry logic, logging
3. **Backward compatible** - Existing code works
4. **Flexible** - Use what you need

**Principle:** Specific classes for semantic meaning, structured fields for operational tracking.

---

**Version:** 1.0.0  
**Date:** 2025-12-08

