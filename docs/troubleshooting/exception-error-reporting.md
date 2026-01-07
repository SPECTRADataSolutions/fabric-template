# Exception Error Reporting - Discord Notifications

**Date:** 2025-12-08  
**Status:** ✅ Implemented  
**Location:** `Data/zephyr/spectraSDK.Notebook/notebook_content.py`

---

## ✅ What's Done

**Added exception handling with Discord notifications for stage failures:**

### Features

1. **Exception Wrapper** - `execute_source_stage()` wrapped with try/except
2. **Failure Notifications** - Discord notification sent on any exception
3. **Error Details** - Full error type, message, and context included
4. **Graceful Failure** - Notification failures don't break the stage
5. **Critical Priority** - Exception notifications sent with "critical" priority

---

## 🎯 Implementation

### Exception Handling Flow

```
execute_source_stage()
    └─ try:
        └─ _execute_source_stage_internal()
            └─ [normal execution]
    └─ except Exception as e:
        ├─ Mark session as failed
        ├─ Send Discord notification (send_exception_notification)
        └─ Re-raise exception (fail stage)
```

### New Methods

**1. `send_exception_notification()`** - Dedicated method for exception notifications

**2. `_execute_source_stage_internal()`** - Internal implementation (wrapped by public method)

---

## 📊 Exception Notification Format

### Standard Exception
```
❌ **Zephyr Enterprise Source Stage Failed**
**Status:** Failed | **Duration:** 12.5s

**Error Type:** `AuthenticationError`
**Error Message:** ```Authentication failed: Invalid API token```

**Category:** `auth`
**Retryable:** No

**Execution:** Pipeline | **Lakehouse:** `zephyrLakehouse`

📝 **Activity Log:** `source.log`

⚠️ **Action Required:** Check activity log for full error details and stack trace
```

### Exception with Context
```
❌ **Zephyr Enterprise Source Stage Failed**
**Status:** Failed | **Duration:** 15.2s

**Error Type:** `ExternalServiceError`
**Error Message:** ```Request timed out```

**Context:** `endpoint`: /project/details, `attempt`: 3, `max_retries`: 3

**Category:** `network`
**Retryable:** Yes

**Execution:** Interactive | **Lakehouse:** `zephyrLakehouse`

📝 **Activity Log:** `source.log`

⚠️ **Action Required:** Check activity log for full error details and stack trace
```

---

## 🔧 Implementation Details

### Exception Wrapper

**Location:** `execute_source_stage()` method

**Pattern:**
```python
@staticmethod
def execute_source_stage(...):
    try:
        SourceStageHelpers._execute_source_stage_internal(...)
    except Exception as e:
        session.mark_failed(str(e))
        SourceStageHelpers.send_exception_notification(session=session, exception=e)
        raise  # Re-raise to fail stage
```

### Notification Helper

**Method:** `send_exception_notification()`

**Features:**
- Auto-detects webhook URL (source-specific or generic)
- Extracts error type and message
- Includes error context (if structured error)
- Includes error category and retryable flag (if available)
- Limits message length (500 chars) to prevent Discord truncation
- Uses code blocks for error messages
- Critical priority for all exception notifications

---

## 📋 Error Information Captured

### From Standard Exceptions
- Error type (class name)
- Error message (truncated to 500 chars)

### From Structured Errors (SpectraError subclasses)
- Error type (class name)
- Error message
- Error category (`auth`, `network`, `validation`, etc.)
- Retryable flag (Yes/No)
- Error context (endpoint, attempt, status_code, etc.)

---

## 🎨 Notification Features

### Priority Levels
- **Critical** - All exception notifications (failures require immediate attention)

### Formatting
- Markdown formatting
- Code blocks for error messages and technical terms
- Structured sections with headers
- Activity log reference for full details

### Error Context Display
- First 3 context items shown (prevents message bloat)
- Context displayed as key-value pairs
- Helps identify where/why error occurred

---

## 🔄 Integration Points

**Exception reporting integrates with:**
1. **ErrorCollector** - Structured errors include full context
2. **ErrorClassification** - Errors are classified before notification
3. **Session Context** - Execution mode, lakehouse, stage included
4. **Activity Logging** - Reference to activity log for full stack trace
5. **Discord Notifications** - Uses same notification infrastructure

---

## 🚀 Benefits

1. **Immediate Alert** - Know about failures instantly
2. **Error Context** - Understand what went wrong and where
3. **Actionable** - Clear next steps (check activity log)
4. **Traceability** - Activity log reference for investigation
5. **No Loss** - Exceptions always reported (even if notification fails)

---

## 📊 Error Notification Flow

```
Stage Execution
    ├─ Success → Discord notification (normal priority)
    └─ Exception → Discord notification (critical priority)
        ├─ Mark session failed
        ├─ Send exception notification
        ├─ Include error details
        ├─ Reference activity log
        └─ Re-raise exception (fail stage)
```

---

## 🎯 Coverage

**Exception notifications sent for:**
- ✅ Authentication failures (AuthenticationError)
- ✅ Network timeouts (ExternalServiceError)
- ✅ Validation failures (ValidationError)
- ✅ Configuration errors (ConfigurationError)
- ✅ Unexpected exceptions (any Exception)
- ✅ Critical errors from ErrorCollector (when raised)

---

## 🔒 Safety

**Exception notification failures:**
- Don't break the stage
- Logged as debug messages
- Stage still fails (original exception re-raised)

**Message length limits:**
- Error messages truncated to 500 chars
- Prevents Discord message limits
- Full details available in activity log

---

**Version:** 1.0.0  
**Date:** 2025-12-08

