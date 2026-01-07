# Error Handling - Final SPECTRA-Grade Design

**Date:** 2025-12-08  
**Status:** ✅ Final Design Approved  
**Purpose:** Complete error handling design using existing SpectraError hierarchy

---

## 🎯 Final Decision

**Approach:** Extend existing **specific** error classes (ValidationError, AuthenticationError, etc.) with structured fields

**Principle:** Use specific classes directly - no generic wrapper. Semantic clarity over generic abstraction.

**Key Insight:** `SpectraError` is too broad. Use specific classes (ValidationError, AuthenticationError, ExternalServiceError) directly for both raising and tracking.

---

## 📐 Architecture

### 1. Base Class Stays Simple (Backward Compatible)

**Location:** `Core/shared/python/spectra-core/src/spectra_core/errors.py`

```python
class SpectraError(Exception):
    """Base exception for all SPECTRA errors"""
    def __init__(self, message: str, code: str = "SPECTRA_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)
```

**Benefits:**
- ✅ Backward compatible - existing code still works
- ✅ Simple base - no structured fields at base level
- ✅ Specific classes handle structured tracking

---

### 2. Extended Specific Error Classes (With Structured Fields)

**Each specific class extends itself with structured tracking fields:**

```python
class ValidationError(SpectraError):
    """Raised when input validation fails"""
    
    def __init__(self, message: str, **kwargs):
        # Structured fields for tracking
        self.category = kwargs.get("category", "validation")
        self.context = kwargs.get("context", {})
        self.retryable = False  # Validation errors never retryable
        self.stage = kwargs.get("stage")
        self.source_system = kwargs.get("source_system")
        super().__init__(message, "VALIDATION_ERROR")


class AuthenticationError(SpectraError):
    """Raised when authentication fails"""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        self.category = kwargs.get("category", "auth")
        self.context = kwargs.get("context", {})
        self.retryable = False  # Auth errors never retryable
        self.stage = kwargs.get("stage")
        self.source_system = kwargs.get("source_system")
        super().__init__(message, "AUTHENTICATION_ERROR")


class ExternalServiceError(SpectraError):
    """Raised when an external service call fails"""
    
    def __init__(self, service: str, message: str, **kwargs):
        self.service = service
        self.category = kwargs.get("category", "api")
        self.context = kwargs.get("context", {})
        self.context.update({"service": service})
        self.retryable = kwargs.get("retryable", True)  # Usually retryable
        self.stage = kwargs.get("stage")
        self.source_system = kwargs.get("source_system")
        super().__init__(f"{service}: {message}", "EXTERNAL_SERVICE_ERROR")
```

**Benefits:**
- ✅ Semantic clarity - ValidationError is clear
- ✅ Type safety - catch specific errors
- ✅ No generic wrapper - uses existing hierarchy
- ✅ SPECTRA-grade - simple, focused

---

### 3. Error Classification Helper

**Location:** `spectraSDK.Notebook/notebook_content.py`

```python
class ErrorClassification:
    """Classify errors and return appropriate SpectraError instances."""
    
    RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
    NON_RETRYABLE_STATUS_CODES = {400, 401, 403, 404}
    
    @staticmethod
    def classify_http_error(status_code: int, error: Exception, **kwargs):
        """Classify HTTP error, return appropriate specific error class."""
        from spectra_core.errors import (
            AuthenticationError, AuthorizationError, 
            NotFoundError, ExternalServiceError
        )
        
        context = kwargs.get("context", {})
        context["status_code"] = status_code
        
        # Return specific class based on status code
        if status_code == 401:
            return AuthenticationError(
                message=str(error),
                category="auth",
                context=context,
                **{k: v for k, v in kwargs.items() if k != "context"}
            )
        elif status_code == 403:
            return AuthorizationError(
                message=str(error),
                category="auth",
                context=context,
                **{k: v for k, v in kwargs.items() if k != "context"}
            )
        elif status_code == 404:
            return NotFoundError(
                resource=kwargs.get("resource", "Resource"),
                identifier=kwargs.get("identifier", "unknown"),
                category="api",
                context=context,
                **{k: v for k, v in kwargs.items() if k not in ("context", "resource", "identifier")}
            )
        else:
            # 429, 500, 502, 503, 504 → ExternalServiceError
            retryable = status_code in ErrorClassification.RETRYABLE_STATUS_CODES
            return ExternalServiceError(
                service=kwargs.get("service", "API"),
                message=str(error),
                category="api",
                context=context,
                retryable=retryable,
                **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
            )
    
    @staticmethod
    def classify_exception(error: Exception, **kwargs) -> SpectraError:
        """Classify any exception, return appropriate SpectraError."""
        from spectra_core.errors import (
            SpectraError, ExternalServiceError, ValidationError,
            AuthenticationError, ConfigurationError
        )
        
        if isinstance(error, requests.exceptions.Timeout):
            return ExternalServiceError(
                service=kwargs.get("service", "API"),
                message=str(error),
                category="network",
                context=kwargs.get("context", {}),
                retryable=True,
                **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
            )
        elif isinstance(error, requests.exceptions.ConnectionError):
            return ExternalServiceError(
                service=kwargs.get("service", "API"),
                message=str(error),
                category="network",
                context=kwargs.get("context", {}),
                retryable=True,
                **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
            )
        elif isinstance(error, requests.exceptions.HTTPError):
            status_code = error.response.status_code if error.response else 0
            return ErrorClassification.classify_http_error(status_code, error, **kwargs)
        else:
            return SpectraError(
                message=str(error),
                code="UNKNOWN_ERROR",
                category="unknown",
                context=kwargs.get("context", {}),
                retryable=False,
                **{k: v for k, v in kwargs.items() if k != "context"}
            )
```

---

### 4. API Request Handler with Retry

**Location:** `spectraSDK.Notebook/notebook_content.py`

```python
class APIRequestHandler:
    """Handle API requests with retry logic and error classification."""
    
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        logger: Optional[SPECTRALogger] = None
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.logger = logger
    
    def execute_with_retry(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Tuple[Any, Optional[SpectraError]]:
        """Execute function with retry logic, return result and optional SpectraError."""
        import random
        import time
        
        for attempt in range(self.max_attempts):
            try:
                result = func(*args, **kwargs)
                if attempt > 0 and self.logger:
                    self.logger.info(f"✅ Succeeded on attempt {attempt + 1}")
                return result, None
            except Exception as e:
                # Classify error
                error = ErrorClassification.classify_exception(
                    e,
                    context={**kwargs.get("context", {}), "attempt": attempt + 1},
                    **{k: v for k, v in kwargs.items() if k != "context"}
                )
                
                # Check if should retry
                if not error.retryable or attempt == self.max_attempts - 1:
                    if self.logger:
                        self.logger.error(f"❌ Failed after {attempt + 1} attempt(s): {error.message}")
                    return None, error
                
                # Calculate delay with exponential backoff + jitter
                delay = min(self.base_delay * (2.0 ** attempt), self.max_delay)
                delay = delay * (0.5 + random.random() * 0.5)  # Jitter
                
                if self.logger:
                    self.logger.warning(f"⚠️ Attempt {attempt + 1} failed, retrying in {delay:.1f}s: {error.message}")
                
                time.sleep(delay)
        
        return None, error
```

---

### 5. Error Collector

**Location:** `spectraSDK.Notebook/notebook_content.py`

```python
class ErrorCollector:
    """Collect errors without failing stage - enables graceful degradation."""
    
    def __init__(self):
        # Collect any SpectraError subclass (polymorphic)
        self.errors: List[Exception] = []
        self.critical_errors: List[Exception] = []
    
    def add(self, error: Exception, critical: bool = False):
        """Add error to collector (accepts any SpectraError subclass)."""
        if critical:
            self.critical_errors.append(error)
        else:
            self.errors.append(error)
    
    def has_critical_errors(self) -> bool:
        """Check if any critical errors exist."""
        return len(self.critical_errors) > 0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get error summary for logging."""
        from collections import Counter
        
        # Handle both SpectraError subclasses (with structured fields) and generic exceptions
        all_errors = self.errors + self.critical_errors
        categories = Counter(
            getattr(e, "category", "unknown") for e in all_errors
        )
        codes = Counter(
            getattr(e, "code", type(e).__name__) for e in all_errors
        )
        error_types = Counter(type(e).__name__ for e in all_errors)
        
        return {
            "total_errors": len(self.errors),
            "critical_errors": len(self.critical_errors),
            "errors_by_category": dict(categories),
            "errors_by_code": dict(codes),
            "errors_by_type": dict(error_types),
            "has_retryable_errors": any(
                getattr(e, "retryable", False) for e in all_errors
            ),
        }
```

---

## 🔧 Integration with SourceStageHelpers

### Updated Method Signatures

```python
@staticmethod
def validate_api_authentication(
    base_url: str,
    api_token: str,
    test_endpoint: str,
    logger: "SPECTRALogger",
    timeout: int = 10,
    auth_header: str = "Authorization",
    auth_prefix: str = "Bearer",
    max_retries: int = 3,
) -> Tuple[Dict, Optional[List], Optional[SpectraError]]:
    """Validate API authentication with retry logic."""
    from spectra_core.errors import AuthenticationError
    
    handler = APIRequestHandler(max_attempts=max_retries, logger=logger)
    
    def _make_request():
        url = f"{base_url}{test_endpoint}"
        headers = {auth_header: f"{auth_prefix} {api_token}"}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    result, error = handler.execute_with_retry(
        _make_request,
        context={"endpoint": test_endpoint, "base_url": base_url},
        service="Zephyr API"
    )
    
    if error:
        if isinstance(error, AuthenticationError) or error.code == "AUTHENTICATION_ERROR":
            return {"status": "Failed", "error": error.message}, None, error
        return {"status": "Failed", "error": error.message}, None, error
    
    # Success
    data = result
    if isinstance(data, list):
        count = len(data)
    elif isinstance(data, dict):
        count = len(data.get("projects", data.get("items", [])))
    else:
        count = 1
    
    logger.info(f"✅ Authentication successful ({count} items)")
    return {"status": "Success", "count": count}, data, None
```

---

## ✅ Benefits

1. **Single System** - Uses existing SpectraError hierarchy
2. **Backward Compatible** - Existing code works (optional fields)
3. **Semantic Classes** - ValidationError, AuthenticationError, etc.
4. **Structured Tracking** - Category, context, retryable, stage, source_system
5. **Reusable** - Works across all stages and sources
6. **SPECTRA-Grade** - Simple, focused, zero tech debt

---

## 📋 Implementation Steps

1. ✅ Extend `SpectraError` in core package
2. ✅ Update subclasses to accept structured fields
3. ✅ Add `ErrorClassification` to SDK
4. ✅ Add `APIRequestHandler` to SDK
5. ✅ Add `ErrorCollector` to SDK
6. ✅ Update `SourceStageHelpers` methods to use retry logic
7. ✅ Update `execute_source_stage()` for graceful degradation
8. ✅ Implement activity logging in `NotebookSession.record()`
9. ✅ Remove preview samples from source stage

---

**Version:** 1.0.0  
**Date:** 2025-12-08  
**Status:** ✅ Ready for Implementation

