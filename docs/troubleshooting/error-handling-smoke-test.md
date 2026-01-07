# Error Handling Smoke Test Guide

**Date:** 2025-12-08  
**Status:** 🧪 Testing Guide  
**Purpose:** Verify error handling and quarantining components work correctly

---

## 🧪 Smoke Test Overview

**Error Handling Status:**
- ✅ **Error Classes** - Implemented and working
- ✅ **Error Classification** - Implemented and working
- ✅ **API Request Handler** - Implemented and working
- ✅ **Error Collector** - Implemented and working
- ✅ **Exception Notifications** - Implemented and working
- ⏳ **Quarantining** - Design complete, NOT YET IMPLEMENTED

---

## 📋 Test 1: Error Handling in Action

### Test Authentication Failure

**In notebook, temporarily break auth:**

```python
# Temporarily modify execute_source_stage to force auth failure
# Or set invalid API_TOKEN in Variable Library

# Expected behavior:
# - AuthenticationError raised
# - Discord notification sent with error details
# - Stage fails immediately
# - Activity log records failure
```

### Test Network Timeout

**Force timeout:**

```python
# Call with very short timeout
result, error = handler.execute_with_retry(
    requests.get,
    url,
    timeout=0.001,  # 1ms timeout (will fail)
    service="Test API",
    stage="source",
    source_system="zephyr"
)

# Expected behavior:
# - ExternalServiceError with retryable=True
# - Retry logic activates (with exponential backoff)
# - After max retries, error returned
```

### Test Non-Critical Errors

**Trigger resource access failure:**

```python
# Use invalid project ID
project_result = SourceStageHelpers.validate_api_resource_access(
    base_url=base_url,
    api_token=api_token,
    resource_endpoint="/release/project/{projectId}",
    resource_id="99999",  # Invalid ID
    ...
)

# Expected behavior:
# - Error collected (non-critical)
# - Stage continues
# - Warning logged
# - Error summary in activity log
```

---

## 📋 Test 2: Error Collector

**Verify error collection:**

```python
from spectraSDK import ErrorCollector

collector = ErrorCollector()

# Add errors
collector.add(ValidationError("Test error 1"), critical=False)
collector.add(AuthenticationError("Critical error"), critical=True)

# Check summary
summary = collector.get_summary()
print(summary)

# Expected output:
# {
#     "total_errors": 1,
#     "critical_errors": 1,
#     "errors_by_category": {"validation": 1, "auth": 1},
#     "errors_by_type": {"ValidationError": 1, "AuthenticationError": 1},
#     "has_retryable_errors": False
# }
```

---

## 📋 Test 3: Activity Logging

**Check activity log table:**

```sql
-- Query activity log
SELECT * FROM source.log
ORDER BY recorded_at DESC
LIMIT 5;
```

**Expected fields:**
- execution_id, notebook_name, stage
- status, duration_seconds
- capabilities, error_summary
- start_time, end_time, recorded_at

---

## 📋 Test 4: Discord Notifications

**Verify notifications sent:**

1. **Success notification** - Check Discord channel after successful run
2. **Failure notification** - Force failure, check Discord for critical alert
3. **Error details** - Verify error type, message, context included

---

## ❌ Quarantining Status

**NOT YET IMPLEMENTED**

**Design Complete:**
- ✅ Design document: `docs/QUARANTINING-SPECTRA-GRADE-DESIGN.md`
- ✅ Metadata-driven validation rules
- ✅ SDK-first approach
- ✅ Integration with SpectraError

**Implementation Pending:**
- ⏳ `DataQualityHelpers` class
- ⏳ `validate_and_quarantine()` method
- ⏳ Integration into source stage

**See:** `docs/QUARANTINING-SPECTRA-GRADE-DESIGN.md` for full design

---

## 🎯 Quick Test Checklist

- [ ] Error classes have `message` attribute
- [ ] Error classification returns correct error types
- [ ] API request handler retries on timeout
- [ ] Error collector aggregates errors correctly
- [ ] Non-critical errors don't fail stage
- [ ] Critical errors fail stage immediately
- [ ] Activity log table created and populated
- [ ] Discord notifications sent on success
- [ ] Discord notifications sent on failure
- [ ] Portfolio display shows at end

---

**Version:** 1.0.0  
**Date:** 2025-12-08

