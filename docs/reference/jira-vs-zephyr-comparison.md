# Jira vs Zephyr Source Notebook Comparison

**Date:** 2025-12-05  
**Purpose:** Identify patterns in Jira source notebook that should be ported to Zephyr

---

## 📊 High-Level Comparison

| Feature | Jira | Zephyr | Should Port? |
|---------|------|--------|--------------|
| **Architecture** | Utility notebooks (`%run sourceUtils`) | SDK notebook (`%run spectraSDK`) | ✅ Zephyr approach is better (standardized) |
| **Credentials** | Hardcoded params + Delta table | Variable Library | ✅ Zephyr approach is better (env vars) |
| **Permissions Check** | ✅ Checks BROWSE_PROJECTS | ❌ No permissions check | ⚠️ **Port if Zephyr has permissions API** |
| **Prepare Stage Init** | ✅ Calls `createPrepareTables()` | ❌ Missing | ✅ **Should port** |
| **Activity Logging** | ✅ Logs to `Tables/log/sourcelog` | ❌ Missing | ✅ **Should port** |
| **Credential Loading** | ✅ Can load from Delta tables | ❌ Only Variable Library | ⚠️ **Consider if needed for multi-workspace** |
| **Project Validation** | ✅ Validates specific project key | ✅ Validates first project dynamically | ✅ Both valid, Zephyr is more flexible |
| **Portfolio Table** | ❌ Basic `_source` table | ✅ Comprehensive portfolio table | ✅ Zephyr approach is better |
| **Front Page Display** | ❌ No summary | ✅ Portfolio summary display | ✅ Zephyr approach is better |
| **Endpoint Catalog** | ❌ Not in source stage | ✅ Bootstraps 228 endpoints | ✅ Zephyr approach is better |
| **Preview Sample** | ❌ Not in source stage | ✅ Extracts preview samples | ✅ Zephyr approach is better |

---

## ✅ What Jira Has That Zephyr Should Port

### 1. **Permissions Validation** ⚠️ (Conditional)

**Jira Pattern:**
```python
checkJiraPermissions(baseUrl, authToken, runtimeCache)
# Calls /rest/api/2/mypermissions
# Validates BROWSE_PROJECTS permission
```

**Recommendation:**
- ✅ **Port if Zephyr API has permissions endpoint**
- ⚠️ Check Zephyr API docs for `/permissions` or `/user/permissions` endpoint
- If available, add `validate_api_permissions()` to SDK helpers

**Priority:** Medium (security best practice)

---

### 2. **Prepare Stage Initialization** ✅ (High Priority)

**Jira Pattern:**
```python
createPrepareTables(sourceSystem=sourceSystem)
# Initializes prepare stage configuration tables
```

**What It Does:**
- Creates prepare stage tables in advance
- Sets up configuration for next stage
- Ensures downstream stages have what they need

**Recommendation:**
- ✅ **Definitely port** - ensures prepare stage is ready
- Add `initialize_prepare_stage()` SDK helper function
- Or add to `SourceStageHelpers.create_prepare_tables()`

**Priority:** High (ensures pipeline continuity)

---

### 3. **Activity Logging** ✅ (High Priority)

**Jira Pattern:**
```python
logStageActivity(
    result=runtimeCache["result"],
    stage=stage,
    logTablePath="Tables/log/sourcelog",
    projectKey=projectKey
)
```

**What It Does:**
- Logs execution metadata to `Tables/log/sourcelog`
- Records capabilities, status, errors
- Provides audit trail for pipeline runs

**Recommendation:**
- ✅ **Definitely port** - critical for observability
- Add `log_stage_activity()` SDK helper function
- Should log: capabilities, status, duration, errors

**Priority:** High (operational visibility)

---

### 4. **Credential Metadata** ⚠️ (Consider)

**Jira Pattern:**
```python
writeAuthCredentials(
    sourceSystem=sourceSystem,
    authToken=authToken,
    workspaceName=workspaceName
)
# Stores: workspaceName, sourceSystem, key, value, isEnabled, expiresAt
```

**What It Does:**
- Stores credentials with workspace context
- Includes expiry dates (set to 2099 if unknown)
- Supports multi-workspace deployments

**Zephyr Current:**
- Only stores masked token
- No workspace context
- No expiry dates

**Recommendation:**
- ⚠️ **Consider porting** if multi-workspace support needed
- Otherwise, Variable Library approach is cleaner
- Could enhance `create_source_credentials_table()` to include workspace metadata

**Priority:** Low (unless multi-workspace required)

---

### 5. **Credential Loading from Delta** ⚠️ (Consider)

**Jira Pattern:**
```python
def loadAuthToken(sourceSystem="jira", key="authToken", cache=None) -> str:
    # Loads from Tables/source/_credentials
    # Returns token from Delta table
```

**What It Does:**
- Allows loading credentials from Delta tables (not just env vars)
- Useful for multi-workspace or historical credential access
- Supports credential caching

**Zephyr Current:**
- Only loads from Variable Library (env vars)
- Simpler, but less flexible

**Recommendation:**
- ⚠️ **Consider porting** if needed for:
  - Multi-workspace deployments
  - Credential rotation tracking
  - Historical credential access
- Otherwise, Variable Library is sufficient

**Priority:** Low (unless multi-workspace required)

---

## ❌ What Zephyr Has That Jira Should Adopt

### 1. **Portfolio Table** ✅
- Comprehensive metadata for dashboard
- Endpoint metrics, capabilities, health status
- **Jira should adopt this pattern**

### 2. **Front Page Summary** ✅
- Formatted portfolio display
- Quick visibility into source status
- **Jira should adopt this pattern**

### 3. **Endpoint Catalog Bootstrap** ✅
- All endpoints catalogued upfront
- Enables dynamic endpoint discovery
- **Jira should adopt this pattern**

### 4. **SDK-Based Architecture** ✅
- Standardized, shareable functions
- Cleaner notebook code
- **Jira should migrate to SDK pattern**

### 5. **Variable Library for Credentials** ✅
- Environment-based configuration
- No hardcoded credentials
- **Jira should migrate to Variable Library**

---

## 🎯 Recommended Actions

### High Priority (Do Now)

1. **Add Activity Logging**
   ```python
   # Add to SDK:
   SourceStageHelpers.log_stage_activity(
       spark=spark,
       delta=session.delta,
       logger=log,
       session=session,
       stage="source",
       log_table_path="Tables/log/sourcelog"
   )
   ```

2. **Add Prepare Stage Initialization**
   ```python
   # Add to SDK:
   SourceStageHelpers.initialize_prepare_stage(
       spark=spark,
       delta=session.delta,
       logger=log,
       source_system=session.ctx["source_system"]
   )
   ```

### Medium Priority (Investigate First)

3. **Add Permissions Validation** (if Zephyr API supports it)
   - Check Zephyr API docs for permissions endpoint
   - If available, add `validate_api_permissions()` to SDK

### Low Priority (Only If Needed)

4. **Enhanced Credential Metadata** (if multi-workspace required)
   - Add workspace context to credentials table
   - Add expiry date tracking

5. **Credential Loading from Delta** (if multi-workspace required)
   - Add `load_credentials_from_delta()` SDK helper
   - Support credential caching

---

## 📋 Implementation Checklist

- [ ] Add `log_stage_activity()` to SDK `SourceStageHelpers`
- [ ] Add `initialize_prepare_stage()` to SDK `SourceStageHelpers`
- [ ] Update Zephyr notebook to call `log_stage_activity()` in RECORD stage
- [ ] Update Zephyr notebook to call `initialize_prepare_stage()` after config tables
- [ ] Investigate Zephyr permissions API (add to backlog if available)
- [ ] Document multi-workspace requirements (defer if not needed)

---

## 🔍 Key Differences Summary

**Jira Strengths:**
- ✅ Activity logging for observability
- ✅ Prepare stage initialization
- ✅ Permissions validation (security)

**Zephyr Strengths:**
- ✅ SDK-based architecture (standardized)
- ✅ Variable Library for credentials (cleaner)
- ✅ Portfolio table (dashboard-ready)
- ✅ Front page summary (visibility)
- ✅ Endpoint catalog bootstrap (comprehensive)

**Best Approach:**
- **Keep Zephyr's SDK architecture** ✅
- **Port Jira's activity logging** ✅
- **Port Jira's prepare stage init** ✅
- **Investigate permissions API** ⚠️
- **Enhance credential metadata if needed** ⚠️

