# Zephyr API Autonomy Blockers & Known Limitations

> **Date:** 2025-12-08  
> **Purpose:** Document all discovered limitations that prevent full automation/autonomy of Zephyr pipeline  
> **Status:** 🟡 Active - Updated as blockers are discovered or resolved  
> **Impact:** High - Blocks full autonomous pipeline execution

---

## 🚨 Critical Autonomy Blockers

### 1. **Requirement Creation - API Broken** ❌ **CRITICAL BLOCKER**

**Status:** ❌ **CANNOT BE AUTOMATED**

**Issue:**
- `POST /requirement/` endpoint is documented but **broken** (HTTP 500)
- Error: `"Cannot invoke \"java.lang.Long.longValue()\" because \"id\" is null"`
- All payload variations fail (direct, wrapped, with id: 0, with parentId, etc.)
- `POST /requirement/bulk` also broken (HTTP 500)
- `POST /externalrequirement/importall` requires external system configuration (not for direct creation)

**What Works:**
- ✅ `POST /requirementtree/add` - Creates **folders/tree nodes** (not actual requirements)
- ✅ `PUT /requirement/{id}` - Updates existing requirements (works)
- ✅ `GET /requirement/{id}` - Reads requirements (works)
- ✅ **Manual UI creation** - Only reliable way to create requirements

**Workaround:**
1. Create requirement folders via `/requirementtree/add`
2. Create actual requirements **manually in UI**
3. Use `PUT /requirement/{id}` to update requirements programmatically

**Impact:**
- **Blocks:** Autonomous requirement creation
- **Requires:** Manual intervention for requirement setup
- **Affects:** `prepare.001-createTestData.md` - Cannot fully automate Star Wars test dataset

**Evidence:**
- `Data/zephyr/scripts/try_create_requirement_v2.py` - All attempts failed
- `Data/zephyr/scripts/try_requirement_bulk_and_import.py` - Bulk and import failed
- `Data/zephyr/docs/ZEPHYR-API-DISCOVERIES.md` - Documented findings

**Resolution Status:** ⏳ **NO WORKAROUND** - Must use UI for requirement creation

---

### 2. **Folder Creation - parentId: null Handling** ⚠️ **RESOLVED**

**Status:** ✅ **RESOLVED** (but was a blocker)

**Issue:**
- API rejects `parentId: null` as a string
- Error: `"For input string: \"null\""` (HTTP 400)
- Root folders require `parentId` field to be **omitted entirely**

**Resolution:**
- ✅ Fixed in `build_comprehensive_spectra_test_project.py`
- ✅ Logic: Omit `parentId` field for root folders (don't send `null`)
- ✅ Only include `parentId` when actual parent ID exists

**Impact:**
- **Was blocking:** Test data creation (folders couldn't be created)
- **Now:** Fully automated folder creation works

**Evidence:**
- `Data/zephyr/scripts/build_comprehensive_spectra_test_project.py` - Fixed folder creation logic

---

### 3. **Release Creation - globalRelease vs projectRelease Conflict** ⚠️ **RESOLVED**

**Status:** ✅ **RESOLVED** (but was a blocker)

**Issue:**
- API prevents creating project-level release if one already exists
- Error: `"Project Release creation not allowed as it is already created at project level."` (HTTP 400)
- Even with `projectRelease: false`, API rejects if project-level release exists

**Resolution:**
- ✅ Always use `globalRelease: true` and `projectRelease: false` for new releases
- ✅ Global releases don't have this restriction
- ✅ Fixed in `build_comprehensive_spectra_test_project.py`

**Impact:**
- **Was blocking:** Release creation in test data script
- **Now:** Fully automated release creation works

**Evidence:**
- `Data/zephyr/scripts/test_single_entry.py` - Confirmed fix works
- `Data/zephyr/scripts/build_comprehensive_spectra_test_project.py` - Fixed release creation

---

### 4. **Testcase Creation - Wrapped Payload Required** ⚠️ **RESOLVED**

**Status:** ✅ **RESOLVED** (but was a blocker)

**Issue:**
- API requires testcase payload to be wrapped in `{"testcase": {...}}` object
- Error: `"testcase object missing"` (HTTP 400) when sending direct payload

**Resolution:**
- ✅ Always wrap testcase payload: `{"testcase": {...}}`
- ✅ Fixed in `build_comprehensive_spectra_test_project.py`

**Impact:**
- **Was blocking:** Testcase creation in test data script
- **Now:** Fully automated testcase creation works

**Evidence:**
- `Data/zephyr/scripts/validate_test_data_dry_run.py` - Identified issue
- `Data/zephyr/scripts/build_comprehensive_spectra_test_project.py` - Fixed testcase wrapping

---

### 5. **Cycle Phase Creation - startDate/endDate Required** ⚠️ **RESOLVED**

**Status:** ✅ **RESOLVED** (but was a blocker)

**Issue:**
- API requires `startDate` and `endDate` for each `cyclePhase` object
- Error: `"cycle phase start date cannot be null."` (HTTP 400)

**Resolution:**
- ✅ Add `startDate` and `endDate` to each phase (default to cycle's dates if missing)
- ✅ Fixed in `build_comprehensive_spectra_test_project.py`

**Impact:**
- **Was blocking:** Cycle creation with phases
- **Now:** Fully automated cycle creation works

**Evidence:**
- `Data/zephyr/scripts/build_comprehensive_spectra_test_project.py` - Fixed cycle phase dates

---

### 6. **Execution Creation - Payload Structure** ⚠️ **PARTIALLY RESOLVED**

**Status:** ⚠️ **PARTIALLY RESOLVED** (may need wrapped payload)

**Issue:**
- Execution endpoint may require wrapped payload `{"execution": {...}}`
- Some executions fail with direct payload (HTTP 500)

**Resolution:**
- ✅ Added fallback to wrapped payload in `build_comprehensive_spectra_test_project.py`
- ⚠️ May still have issues depending on execution state

**Impact:**
- **May block:** Execution creation in some scenarios
- **Workaround:** Wrapped payload fallback implemented

**Evidence:**
- `Data/zephyr/scripts/build_comprehensive_spectra_test_project.py` - Wrapped payload fallback

---

### 7. **Endpoint Catalog Duplicates** ✅ **RESOLVED**

**Status:** ✅ **RESOLVED**

**Issue:**
- Endpoint catalog contained 25 true duplicates (same path + method)
- Metadata loss during parsing (query/path parameters stripped)
- Caused confusion and potential API call errors

**Resolution:**
- ✅ Fixed `parse_endpoints.py` to preserve full metadata
- ✅ Deduplication based on `(full_path, method)`
- ✅ Zero duplicates achieved (224 unique endpoints)
- ✅ All metadata preserved (query_parameters, path_parameters, resource)

**Impact:**
- **Was blocking:** Accurate endpoint discovery
- **Now:** Clean, deduplicated catalog with full metadata

**Evidence:**
- `Data/zephyr/docs/ENDPOINT-DUPLICATES-ROOT-CAUSE.md` - Full analysis
- `Data/zephyr/scripts/parse_endpoints.py` - Fixed parsing logic
- `Data/zephyr/spectraSDK.Notebook/notebook_content.py` - Updated catalog

---

## 📋 API Behavior Gotchas (Non-Blocking but Important)

### 8. **Requirement Tree Structure - Folders vs Requirements**

**Status:** ⚠️ **UNDERSTOOD** (not a blocker, but confusing)

**Issue:**
- `/requirementtree/add` creates **folders/tree nodes**, not actual requirements
- Requirements appear in both tree view and table view, but they're the same tree nodes
- No separate "requirement" entity type - everything is a tree node

**Impact:**
- **Not blocking:** Can create folders programmatically
- **Confusing:** Terminology doesn't match API behavior
- **Workaround:** Create folders via API, requirements via UI

**Evidence:**
- `Data/zephyr/docs/ZEPHYR-API-DISCOVERIES.md` - Full documentation

---

### 9. **Release Deletion - Last Active Release Protection**

**Status:** ⚠️ **UNDERSTOOD** (not a blocker, but limitation)

**Issue:**
- API prevents deletion of the last active release
- Error: `"The last active release of the project cannot be deleted."` (HTTP 400)

**Impact:**
- **Not blocking:** Can work around by creating new release first
- **Limitation:** Cannot delete all releases (must keep at least one active)

**Evidence:**
- `Data/zephyr/scripts/delete_all_releases.py` - Encountered this limitation

---

### 10. **GET /requirement/project/{projectId} - Not Available**

**Status:** ⚠️ **UNDERSTOOD** (not a blocker, but limitation)

**Issue:**
- `GET /requirement/project/{projectId}` returns HTTP 404
- Cannot list requirements by project via API

**Impact:**
- **Not blocking:** Can use `GET /requirement/{id}` for individual requirements
- **Limitation:** Must know requirement IDs to retrieve them

**Evidence:**
- `Data/zephyr/scripts/try_create_requirement_v2.py` - Confirmed 404

---

## 🎯 Autonomy Impact Summary

| Blocker | Status | Impact | Workaround |
|---------|--------|--------|------------|
| **Requirement Creation** | ❌ **BROKEN** | **CRITICAL** - Blocks full automation | Manual UI creation required |
| Folder Creation | ✅ **RESOLVED** | Was blocking | Fixed - omit parentId for root |
| Release Creation | ✅ **RESOLVED** | Was blocking | Fixed - use globalRelease: true |
| Testcase Creation | ✅ **RESOLVED** | Was blocking | Fixed - wrap in {"testcase": {...}} |
| Cycle Phases | ✅ **RESOLVED** | Was blocking | Fixed - add startDate/endDate |
| Execution Creation | ⚠️ **PARTIAL** | May block | Wrapped payload fallback |
| Endpoint Duplicates | ✅ **RESOLVED** | Was blocking | Fixed - deduplication logic |
| Requirement Tree | ⚠️ **UNDERSTOOD** | Not blocking | Create folders via API, requirements via UI |
| Release Deletion | ⚠️ **LIMITATION** | Not blocking | Keep at least one active release |
| Requirement Listing | ⚠️ **LIMITATION** | Not blocking | Use individual GET /requirement/{id} |

---

## 🚀 Current Autonomy Status

### ✅ **Fully Automated:**
- ✅ Endpoint cataloging (Source stage)
- ✅ Folder creation (Test Repository)
- ✅ Release creation
- ✅ Cycle creation
- ✅ Testcase creation
- ✅ Execution creation (with fallback)
- ✅ Requirement updates (PUT)
- ✅ Requirement reading (GET)

### ⚠️ **Partially Automated:**
- ⚠️ Requirement creation (folders only - actual requirements require UI)
- ⚠️ Execution creation (may need wrapped payload)

### ❌ **Manual Intervention Required:**
- ❌ **Requirement creation** (actual requirements, not folders)
- ❌ Initial requirement setup for test data

---

## 📝 Recommendations

### For Full Autonomy:

1. **Requirement Creation:**
   - **Option A:** Contact Zephyr support to fix `POST /requirement/` endpoint
   - **Option B:** Use external system import (Jira, etc.) if available
   - **Option C:** Accept manual requirement creation as part of setup

2. **Test Data Creation:**
   - Create requirements manually in UI first
   - Then automate everything else (releases, cycles, testcases, executions)
   - Document manual steps in playbooks

3. **Pipeline Design:**
   - Design pipeline to handle missing requirements gracefully
   - Use `PUT /requirement/{id}` to update requirements programmatically
   - Focus automation on data extraction/transformation, not requirement creation

---

## 🔄 Update History

- **2025-12-08:** Initial documentation of all discovered blockers
- **2025-12-08:** Resolved: Folder creation, Release creation, Testcase creation, Cycle phases, Endpoint duplicates
- **2025-12-08:** Confirmed: Requirement creation API is broken (no workaround)

---

**Last Updated:** 2025-12-08  
**Next Review:** When new blockers discovered or resolved

