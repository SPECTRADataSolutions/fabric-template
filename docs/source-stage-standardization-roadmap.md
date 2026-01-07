# Source Stage Standardization Roadmap

**Date:** 2025-12-04  
**Goal:** Standardize Source stage notebooks across Jira and Zephyr

---

## 🎯 Approach: Best-of-Both Pattern

**Strategy:** Extract the best patterns from each notebook, create a unified standard, then migrate both notebooks to the standard.

---

## 📊 Pattern Inventory

### ✅ What Zephyr Does Better

1. **Modern Parameter Design**

   - `bootstrap`, `backfill`, `preview`, `debug`
   - Clear, validated, part of a family
   - **Action:** Backport to Jira

2. **No `%run` Magic Commands**

   - Proper Python imports
   - SDK-based utilities
   - **Action:** Backport to Jira

3. **Endpoint Bootstrap Pattern**

   - Embedded endpoint data
   - First-run bootstrap works immediately
   - **Action:** Add to Jira if applicable

4. **Smart Debug Mode**
   - Auto-enables when running locally
   - **Action:** Backport to Jira

---

### ✅ What Jira Does Better

1. **Metadata Declarations**

   - Explicit `source_system`, `stage`, `notebook_name`
   - **Action:** Add to Zephyr

2. **Stage Activity Logging**

   - `log_stage_activity()` function
   - Operational telemetry
   - **Action:** Add to Zephyr

3. **Vendor-Specific Health Checks**

   - `checkJiraAuth()`, `checkJiraPermissions()`, `checkJiraProjectAccess()`
   - **Action:** Create Zephyr equivalents

4. **Credential Storage**
   - `write_auth_credentials()` pattern
   - **Action:** Add to Zephyr

---

## 🗺️ Standardization Phases

### Phase 1: Create the Standard (NOW)

**Deliverable:** `Core/framework/standards/SOURCE-STAGE-STANDARD.md`

**Status:** ✅ **COMPLETE**

**Contents:**

- Mandatory structure
- Best practices from both notebooks
- Endpoint bootstrap pattern documented
- Health check pattern documented
- Complete checklist

---

### Phase 2: Enhance Zephyr (HIGH PRIORITY)

**Goal:** Add missing Jira patterns to Zephyr

**Tasks:**

#### 2.1 Add Metadata Declarations (Contract-Driven)

```python
# Add at top of notebook (after parameters)
from spectra_fabric_sdk.contract_utils import load_contract_metadata

_metadata = load_contract_metadata()  # Reads Data/zephyr/contract.yaml
source_system = _metadata["source_system"]   # From contract: "zephyr"
source_name = _metadata["source_name"]       # From contract: "Zephyr Enterprise"
stage = _metadata["stage"]                    # Inferred: "source"
notebook_name = _metadata["notebook_name"]    # Inferred: "sourceZephyr"
base_url = _metadata["base_url"]             # From contract
workspace_name = _metadata["workspace_name"]  # From contract
lakehouse_id = _metadata["lakehouse_id"]     # From contract
_running_locally = _metadata["is_local"]     # Already exists, can merge
```

**File:** `Data/zephyr/sourceZephyr.Notebook/notebook_content.py`  
**Location:** After parameter block (around line 69)

**Note:** This replaces ALL hardcoding with contract reads (see `CONTRACT-DRIVEN-METADATA.md`)

**Benefit:** Zero hardcoded values - all from Discovery phase contract ✅

---

#### 2.2 Add Stage Activity Logging

**Requirement:** Import `log_stage_activity()` from SDK or create shared utility

**Location:** End of notebook (before summary)

```python
from spectra_fabric_sdk.logging_utils import log_stage_activity

# At end of notebook
log_stage_activity(
    result=runtime_cache.get("result", {"status": "Success", "capabilities": []}),
    stage=stage,
    log_table_path="Tables/log/sourcelog",
    source_system=source_system
)
```

**Note:** Need to create `runtime_cache` if not exists

---

#### 2.3 Create Zephyr Health Check Functions

**Location:** Add to notebook or create `zephyr_source_utils.py`

**Functions to create:**

```python
def check_zephyr_auth(
    base_url: str,
    auth_token: str,
    runtime_cache: dict = None
) -> None:
    """Verify Zephyr API authentication.

    Tests /serverInfo or /project endpoint.
    Updates runtime_cache["result"]["capabilities"].
    """
    # TODO: Implement Zephyr auth check
    pass

def check_zephyr_project_access(
    base_url: str,
    auth_token: str,
    project_id: int,
    runtime_cache: dict = None
) -> None:
    """Verify can access specific Zephyr project.

    Tests /project/details endpoint.
    Updates runtime_cache["result"]["capabilities"].
    """
    # TODO: Implement project access check
    pass

def check_zephyr_hierarchical_access(
    base_url: str,
    auth_token: str,
    runtime_cache: dict = None
) -> None:
    """Verify hierarchical access (project → release → cycle).

    Tests multi-level endpoint traversal.
    Updates runtime_cache["result"]["capabilities"].
    """
    # Zephyr already has this! Just needs to update runtime_cache
    pass
```

**Note:** Zephyr already does hierarchical validation - just needs to follow Jira's pattern of updating `runtime_cache`

---

#### 2.4 Add Credential Storage

**Location:** After successful health checks

```python
from spectra_fabric_sdk.source_utils import write_auth_credentials

write_auth_credentials(
    source_system=source_system,
    auth_token=zephyr_api_token,
    workspace_name=workspace_name
)
```

**Note:** Need to ensure `create_source_tables()` has been called first

---

### Phase 3: Enhance Jira (MEDIUM PRIORITY)

**Goal:** Backport Zephyr's innovations to Jira

**Tasks:**

#### 3.1 Modernize Parameters

**Current (Jira):**

```python
debugMode = bool(str(globals().get("debugMode", "0")).lower() in ("1", "true", "yes"))
```

**Target (Zephyr pattern):**

```python
bootstrap: bool = False
backfill: bool = False
preview: bool = False
debug: bool = False
```

**Migration:**

- Keep `debugMode` for backward compatibility
- Add new parameters
- Map old → new internally
- Document migration path

---

#### 3.2 Remove `%run` Magic Commands

**Current (Jira):**

```python
%run dateTimeUtils
%run loggingUtils
%run sourceUtils
%run prepareUtils
```

**Target:** SDK imports

```python
from spectra_fabric_sdk.datetime_utils import ...
from spectra_fabric_sdk.logging_utils import ...
from spectra_fabric_sdk.source_utils import ...
```

**Migration:**

- Promote utilities to SDK
- Update imports
- Test thoroughly
- Keep `%run` as fallback if needed

---

#### 3.3 Add Endpoint Bootstrap (if applicable)

**Question:** Does Jira have an endpoint catalogue like Zephyr?

**If YES:**

- Embed endpoint data in notebook
- Add `bootstrap` parameter support
- Create endpoints table

**If NO:**

- Skip (not all sources need this)

---

#### 3.4 Add Smart Debug Mode

**Current:** Manual `debugMode` parameter

**Target:** Auto-enable when running locally

```python
_running_locally = os.path.exists("/.cursor") or os.path.exists("/.vscode")
debug = debug or _running_locally  # Auto-enable locally
```

---

### Phase 4: Extract Shared Utilities (ONGOING)

**Goal:** Promote common functions to SDK

**Candidates:**

1. **`log_stage_activity()`**

   - Location: `Data/jira/_utils/loggingUtils.Notebook/notebook_content.py`
   - Promote to: `spectra_fabric_sdk.logging_utils`
   - Status: ✅ Ready

2. **`create_source_tables()`**

   - Location: `Data/jira/_utils/sourceUtils.Notebook/notebook_content.py`
   - Promote to: `spectra_fabric_sdk.source_utils`
   - Status: ✅ Ready

3. **`write_auth_credentials()`**

   - Location: `Data/jira/_utils/sourceUtils.Notebook/notebook_content.py`
   - Promote to: `spectra_fabric_sdk.source_utils`
   - Status: ✅ Ready

4. **`register_delta_table()`**

   - Location: Zephyr notebook (embedded)
   - Promote to: `spectra_fabric_sdk.delta_utils`
   - Status: ✅ Ready

5. **`is_running_locally()`**
   - Location: Zephyr notebook (embedded)
   - Promote to: `spectra_fabric_sdk.runtime`
   - Status: ✅ Ready

---

## 📋 Implementation Priority

### High Priority (Do First)

1. ✅ **Create SOURCE-STAGE-STANDARD.md** - COMPLETE
2. **Add metadata declarations to Zephyr** - 5 minutes
3. **Add stage activity logging to Zephyr** - 15 minutes
4. **Create Zephyr health check functions** - 30 minutes
5. **Add credential storage to Zephyr** - 10 minutes

**Total:** ~1 hour to bring Zephyr up to standard

---

### Medium Priority (Next Sprint)

6. **Modernize Jira parameters** - 1 hour
7. **Remove `%run` from Jira** - 2 hours
8. **Add smart debug to Jira** - 30 minutes
9. **Promote shared utilities to SDK** - 2 hours

**Total:** ~5.5 hours

---

### Low Priority (Future)

10. **Add endpoint bootstrap to Jira** (if applicable) - TBD
11. **Extract hardcoded config** (both notebooks) - TBD
12. **Create Source stage template** - 1 hour

---

## 🎯 Success Criteria

**Zephyr Source Notebook:**

- ✅ Has metadata declarations
- ✅ Has stage activity logging
- ✅ Has vendor-specific health checks
- ✅ Has credential storage
- ✅ Already has modern parameters ✅
- ✅ Already has endpoint bootstrap ✅

**Jira Source Notebook:**

- ✅ Has metadata declarations ✅
- ✅ Has stage activity logging ✅
- ✅ Has vendor-specific health checks ✅
- ✅ Has credential storage ✅
- ⚠️ Needs modern parameters
- ⚠️ Needs `%run` removal

**Both notebooks:**

- ✅ Follow SOURCE-STAGE-STANDARD.md
- ✅ Pass standardization checklist
- ✅ Use SDK utilities (not embedded code)

---

## 🚀 Next Steps

**Immediate (Today):**

1. Review SOURCE-STAGE-STANDARD.md
2. Add metadata declarations to Zephyr
3. Add stage activity logging to Zephyr

**This Week:** 4. Create Zephyr health check functions 5. Add credential storage to Zephyr 6. Test Zephyr notebook end-to-end

**Next Week:** 7. Start Jira modernization 8. Promote utilities to SDK

---

## 💡 Decision Points

### 1. Should we standardize NOW or AFTER fixing current bugs?

**Recommendation:** **Do both in parallel**

- Standardization is mostly additive
- Won't break existing functionality
- Makes future maintenance easier

### 2. Should Jira get endpoint bootstrap?

**Question:** Does Jira have an endpoint catalogue?

**If YES:** Add bootstrap pattern  
**If NO:** Skip (not mandatory)

### 3. Should we extract hardcoded config now?

**Recommendation:** **Not now**

- Works as-is
- Low priority
- Can extract later when we have 3+ sources

---

## 📝 Notes

**Endpoint Bootstrap Pattern:**

- Unique to Zephyr (228 endpoints)
- Only needed if source has endpoint catalogue
- Optional enhancement, not mandatory

**Vendor-Specific Health Checks:**

- Each vendor has unique endpoints
- Must be custom per source system
- Pattern is standardized, implementation is vendor-specific

**Stage Activity Logging:**

- Universal function
- Just needs to be called
- No vendor-specific logic

---

**Last Updated:** 2025-12-04  
**Owner:** Mark  
**Status:** Ready for implementation
