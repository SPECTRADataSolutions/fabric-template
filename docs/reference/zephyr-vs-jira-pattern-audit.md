# Zephyr vs Jira Source Notebook Pattern Audit

**Date:** 2025-12-04  
**Auditor:** Mark  
**Method:** Side-by-side comparison in Cursor

---

## ✅ What Zephyr Does BETTER

1. **No `%run` magic commands** - proper Python imports instead
2. **Modern parameter design** - `bootstrap`, `backfill`, `preview`, `debug` (clear, validated, family)
3. **Embedded endpoint data** - 228 endpoints in notebook (no external dependency)
4. **Smart debug mode** - auto-enables when running locally

---

## ❌ What Zephyr is MISSING (vs Jira)

### 1. Metadata Declaration

**Jira has:**
```python
source_system = "jira"
stage = "source"
notebook_name = "sourceJira"
```

**Zephyr missing:** These declarations don't exist

**Impact:** Unclear what system/stage this notebook is for  
**Fix Required:** Add declarations at top of notebook

---

### 2. Hardcoded Configuration

**Both Jira AND Zephyr hardcode:**
```python
workspace_id = "23c6e7e1-4466-4132-b39c-fe3bcb504f26"
lakehouse_id = "e6dfef5c-d848-403e-a61b-ec9d54689134"
semantic_model_id = "a23e2567-6f97-4046-b353-a8848a2479f5"
base_url = "https://jira.dxc.com"
```

**Problem:** Hardcoded values not portable, environment-specific  
**Pattern:** Both notebooks do this (not just Zephyr)  
**Discussion:** Should these come from config/env vars?

---

### 3. Stage Activity Logging

**Jira uses:**
```python
log_stage_activity(...)  # Records stage execution metadata
```

**Zephyr missing:** Not using this function

**Impact:** No operational logging for orchestration/monitoring  
**Fix Required:** Add `log_stage_activity()` call at end

---

### 4. Vendor-Specific Health Checks

**Jira has:**
```python
checkJiraProjectAccess()
checkJiraPermissions()
checkJiraAuth()
```

**Zephyr missing:** No equivalent Zephyr-specific functions

**Impact:** Generic health check, not Zephyr-specific validation  
**Fix Required:** Create Zephyr equivalents:
- `check_zephyr_project_access()`
- `check_zephyr_permissions()`  
- `check_zephyr_auth()`

---

## 📊 Standardization Assessment

| Pattern | Jira | Zephyr | Action Required |
|---------|------|--------|-----------------|
| Metadata declarations | ✅ | ❌ | Add source_system, stage, notebook_name |
| Modern parameters | ❌ | ✅ | Backport to Jira |
| Stage activity logging | ✅ | ❌ | Add to Zephyr |
| Vendor health checks | ✅ | ❌ | Create Zephyr versions |
| Embedded data | ❌ | ✅ | Consider for Jira |
| Config hardcoding | ⚠️ | ⚠️ | Both need improvement |
| No %run commands | ❌ | ✅ | Backport to Jira |

---

## 🎯 Proposed Fixes for Zephyr

### Fix 1: Add Metadata Declarations

```python
# ========== Notebook Metadata ==========
source_system = "zephyr"
stage = "source"
notebook_name = "sourceZephyr"
```

### Fix 2: Add Stage Activity Logging

```python
# At end of notebook
log_stage_activity(
    stage=stage,
    source_system=source_system,
    notebook_name=notebook_name,
    status="success",
    rows_processed=total_rows,
    duration_seconds=execution_time,
    # ... other metadata
)
```

### Fix 3: Create Zephyr Health Check Functions

```python
def check_zephyr_auth() -> bool:
    """Verify Zephyr API authentication."""
    # Test /serverInfo or similar endpoint
    pass

def check_zephyr_project_access(project_id: int) -> bool:
    """Verify can access specific project."""
    # Test /project/details
    pass

def check_zephyr_permissions() -> dict:
    """Check what Zephyr permissions current token has."""
    # Test various endpoints to map permissions
    pass
```

### Fix 4: Extract Hardcoded Config (BOTH notebooks)

**Option A: Environment Variables**
```python
workspace_id = os.getenv("FABRIC_WORKSPACE_ID")
lakehouse_id = os.getenv("FABRIC_LAKEHOUSE_ID")
base_url = os.getenv("ZEPHYR_BASE_URL")
```

**Option B: Config Table (SPECTRA pattern)**
```python
# Read from Tables/source/_config
config = spark.read.table("source._config").first()
workspace_id = config.workspaceId
lakehouse_id = config.lakehouseId
```

**Option C: Fabric Metadata (if available)**
```python
# Use Fabric's built-in workspace context
workspace_id = spark.conf.get("spark.workspace.id")
```

---

## 🔄 Bidirectional Improvements

**Zephyr → Jira:**
- Modern parameter design (bootstrap/backfill/preview/debug)
- No %run dependencies
- Embedded data pattern

**Jira → Zephyr:**
- Metadata declarations
- Stage activity logging
- Vendor-specific health checks

---

## 📝 Discussion Points

### 1. Should we declare source_system/stage/notebook_name?

**Pros:**
- Self-documenting
- Enables `log_stage_activity()`
- Clear identity

**Cons:**
- Redundant (filename already says this)
- More to maintain

**Recommendation:** **YES** - standardize across all notebooks

---

### 2. Should we extract hardcoded config?

**Current State:** Both Jira and Zephyr hardcode

**Options:**
1. **Keep as-is** (simplest, works)
2. **Move to env vars** (portable)
3. **Move to config table** (SPECTRA pattern)
4. **Use Fabric metadata** (if available)

**Recommendation:** **Discuss further** - affects all notebooks

---

### 3. Should Zephyr have vendor-specific health checks?

**YES.** Each vendor has unique:
- Auth patterns
- Permission models
- API capabilities
- Common errors

**Zephyr should have:**
- `check_zephyr_auth()` - validate token
- `check_zephyr_project_access()` - test project endpoint
- `check_zephyr_cycle_access()` - test hierarchical access
- `check_zephyr_permissions()` - map what token can do

---

## 🎯 Implementation Priority

**High Priority (Do Now):**
1. Add metadata declarations to Zephyr
2. Add `log_stage_activity()` call
3. Create Zephyr health check functions

**Medium Priority (Next Sprint):**
4. Backport modern parameters to Jira
5. Extract hardcoded config pattern

**Low Priority (Future):**
6. Remove %run from all Jira notebooks
7. Embedded data pattern for Jira

---

## 📋 Action Items

- [ ] Add source_system/stage/notebook_name to Zephyr
- [ ] Import and call `log_stage_activity()`
- [ ] Create `check_zephyr_auth()`
- [ ] Create `check_zephyr_project_access()`
- [ ] Create `check_zephyr_permissions()`
- [ ] Document config extraction pattern options
- [ ] Create SOURCE-STAGE-STANDARDS.md for consistency

---

## Next Steps

**Immediate:** Fix the schema registration issue first (current blocker)  
**Then:** Apply these standardization improvements

**Goal:** All Source stage notebooks follow same pattern regardless of vendor.


