# Error Handling - SPECTRA-Grade Design

**Date:** 2025-12-08  
**Status:** 🎯 Design Complete, Ready for Implementation  
**Purpose:** SPECTRA-grade error handling system for source stage

---

## 🎯 Design Principles

1. **SDK-First** - All error handling logic in reusable SDK classes
2. **Type-Safe** - Structured error objects, not strings
3. **Modular** - Reusable across all stages
4. **Graceful** - Degrade gracefully, continue with partial data
5. **Observable** - Full error context for debugging

---

## 📐 Architecture

### Core Components

1. **`SourceStageError`** - Structured error class
2. **`ErrorClassification`** - Classify errors (retryable vs. non-retryable)
3. **`APIRequestHandler`** - Retry logic for API calls
4. **`ErrorCollector`** - Collect errors without failing stage
5. **Integration** - Update `SourceStageHelpers` to use new system

---

## 🔧 Implementation Details

### 1. Extended SpectraError (Use Existing Hierarchy)

**Location:** `Core/shared/python/spectra-core/src/spectra_core/errors.py`

**Design:** Extend existing `SpectraError` base class with structured fields

```python
class SpectraError(Exception):
    """Base exception for all SPECTRA errors with structured tracking."""
    
    def __init__(
        self,
        message: str,
        code: str = "SPECTRA_ERROR",
        category: Optional[str] = None,  # "auth", "network", "data", "validation", "api"
        context: Optional[Dict[str, Any]] = None,  # endpoint, timestamp, attempt_number, status_code
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

# Existing specific classes inherit structured fields:
# - ValidationError (retryable=False, category="validation")
# - AuthenticationError (retryable=False, category="auth")
# - ExternalServiceError (retryable=True, category="api")
```

### 2. Error Classification

```python
class ErrorClassification:
    """Classify errors as retryable or non-retryable, return SpectraError instances."""
    
    RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
    NON_RETRYABLE_STATUS_CODES = {400, 401, 403, 404}
    
    @staticmethod
    def classify_http_error(status_code: int, error: Exception, **kwargs) -> SpectraError:
        """Classify HTTP error based on status code, return appropriate SpectraError."""
        from spectra_core.errors import ExternalServiceError
        
        context = kwargs.get("context", {})
        context["status_code"] = status_code
        
        if status_code in RETRYABLE_STATUS_CODES:
            return ExternalServiceError(
                service=kwargs.get("service", "API"),
                message=str(error),
                category="api",
                context=context,
                retryable=True,
                **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
            )
        else:
            return ExternalServiceError(
                service=kwargs.get("service", "API"),
                message=str(error),
                category="api",
                context=context,
                retryable=False,
                **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
            )
```

### 3. API Request Handler with Retry

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
        """Execute function with retry logic, return SpectraError instances."""
        from spectra_core.errors import SpectraError, ExternalServiceError
        
        for attempt in range(self.max_attempts):
            try:
                result = func(*args, **kwargs)
                if attempt > 0 and self.logger:
                    self.logger.info(f"✅ Succeeded on attempt {attempt + 1}")
                return result, None
            except requests.exceptions.Timeout as e:
                error = ExternalServiceError(
                    service=kwargs.get("service", "API"),
                    message=str(e),
                    category="network",
                    context={**kwargs.get("context", {}), "attempt": attempt + 1},
                    retryable=True,
                    **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
                )
                if attempt == self.max_attempts - 1:
                    return None, error
                self._wait_before_retry(attempt, error)
            except requests.exceptions.ConnectionError as e:
                error = ExternalServiceError(
                    service=kwargs.get("service", "API"),
                    message=str(e),
                    category="network",
                    context={**kwargs.get("context", {}), "attempt": attempt + 1},
                    retryable=True,
                    **{k: v for k, v in kwargs.items() if k not in ("context", "service")}
                )
                if attempt == self.max_attempts - 1:
                    return None, error
                self._wait_before_retry(attempt, error)
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code if e.response else 0
                error = ErrorClassification.classify_http_error(
                    status_code, e,
                    context={**kwargs.get("context", {}), "attempt": attempt + 1},
                    **{k: v for k, v in kwargs.items() if k != "context"}
                )
                if not error.retryable or attempt == self.max_attempts - 1:
                    return None, error
                self._wait_before_retry(attempt, error)
            except Exception as e:
                error = SpectraError(
                    message=str(e),
                    code="UNKNOWN_ERROR",
                    category="unknown",
                    context={**kwargs.get("context", {}), "attempt": attempt + 1},
                    retryable=False,
                    **{k: v for k, v in kwargs.items() if k not in ("context",)}
                )
                return None, error
        
        return None, error
```

### 4. Error Collector

```python
class ErrorCollector:
    """Collect errors without failing stage."""
    
    def __init__(self):
        self.errors: List[SpectraError] = []
        self.critical_errors: List[SpectraError] = []
    
    def add(self, error: SpectraError, critical: bool = False):
        """Add error to collector."""
        if critical:
            self.critical_errors.append(error)
        else:
            self.errors.append(error)
    
    def has_critical_errors(self) -> bool:
        """Check if any critical errors exist."""
        return len(self.critical_errors) > 0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get error summary."""
        return {
            "total_errors": len(self.errors),
            "critical_errors": len(self.critical_errors),
            "errors_by_category": self._group_by_category(),
            "errors_by_code": self._group_by_code()
        }
```

### 5. Graceful Degradation in execute_source_stage

```python
def execute_source_stage(..., continue_on_error: bool = True):
    """Execute source stage with graceful degradation."""
    error_collector = ErrorCollector()
    request_handler = APIRequestHandler(max_attempts=3, logger=log)
    
    # 1. Auth validation (critical - fail fast if fails)
    auth_result, all_projects = request_handler.execute_with_retry(
        lambda: SourceStageHelpers._validate_auth_internal(...)
    )
    
    if auth_result is None:
        session.mark_failed("Authentication failed")
        raise RuntimeError("Cannot proceed without authentication")
    
    # 2. Bootstrap endpoints (non-critical - continue if fails)
    if session.params["bootstrap"]:
        endpoint_count, error = request_handler.execute_with_retry(
            lambda: SourceStageHelpers._bootstrap_endpoints_internal(...)
        )
        if error:
            error_collector.add(error, critical=False)
            log.warning(f"⚠️ Endpoint bootstrap failed: {error.message}")
    
    # 3. Create tables (continue even if some fail)
    try:
        SourceStageHelpers.create_source_config_table(...)
    except Exception as e:
        error_collector.add(
            SourceStageError(category="data", code="TABLE_CREATION_FAILED", ...),
            critical=False
        )
    
    # Continue with remaining operations...
    
    # Final: Check if critical errors occurred
    if error_collector.has_critical_errors():
        session.mark_failed("Critical errors occurred")
    else:
        session.add_capability("completedWithWarnings" if error_collector.errors else "completed")
    
    # Store errors in session for activity logging
    session.result["errors"] = error_collector.get_summary()
```

---

## ✅ Integration Points

### Update SourceStageHelpers Methods

1. **`validate_api_authentication()`** - Use `APIRequestHandler`
2. **`validate_api_resource_access()`** - Use `APIRequestHandler`
3. **`bootstrap_endpoints_catalog()`** - Use `APIRequestHandler`
4. **`extract_preview_sample()`** - Remove (no longer required)
5. **`execute_source_stage()`** - Add error collection and graceful degradation

### Update NotebookSession

1. **`record()`** - Log errors to Delta table
2. **`mark_failed()`** - Store critical errors
3. **`result["errors"]`** - Store error summary

---

## 📊 Benefits

1. **Retry Logic** - Automatic retry on transient failures
2. **Error Classification** - Smart retry (only retryable errors)
3. **Graceful Degradation** - Continue with partial data
4. **Structured Errors** - Full context for debugging
5. **Observability** - Errors logged to activity log
6. **Modular** - Reusable across all stages

---

## 🎯 Next Steps

1. Implement classes in SDK
2. Update SourceStageHelpers
3. Update execute_source_stage
4. Implement activity logging
5. Test error scenarios
6. Update documentation

---

**Version:** 1.0.0  
**Date:** 2025-12-08

