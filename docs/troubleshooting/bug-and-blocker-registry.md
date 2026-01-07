# Zephyr API Bug & Blocker Registry

> **Purpose:** Comprehensive registry of all bugs, blockers, and API issues discovered during SPECTRA pipeline development.  
> **Status:** 🟡 Active - Updated as issues are discovered  
> **Last Updated:** 2025-12-08  
> **Use Case:** Report to Zephyr support, document workarounds, track resolution status

---

## 📋 Registry Overview

This registry tracks:
- **Critical Blockers** - Issues that prevent full automation
- **API Bugs** - Broken or misbehaving endpoints
- **Documentation Gaps** - Discrepancies between docs and reality
- **Workarounds** - Temporary solutions implemented
- **Resolution Status** - Tracked for reporting to Zephyr support

---

## 🔴 Critical Blockers

### BLOCKER-001: Requirement Creation API Broken

**Status:** 🔴 **CRITICAL BLOCKER**  
**Severity:** High  
**Impact:** Prevents autonomous requirement creation  
**Date Discovered:** 2025-12-08

**Issue:**
- `POST /requirement/` endpoint returns HTTP 500: `"Cannot invoke \"java.lang.Long.longValue()\" because \"id\" is null"`
- `POST /requirement/bulk` also returns HTTP 500
- `POST /externalrequirement/importall` also returns HTTP 500
- All documented requirement creation endpoints are broken

**Documentation Claims:**
- `endpoints.json` line 616: "Create new requirement [/requirement/]"
- API documentation suggests `POST /requirement` should work
- Multiple payload structures documented

**Reality:**
- All attempts fail with HTTP 500
- Tried: direct payload, wrapped payload, with id: 0, with parentId
- No working API endpoint for requirement creation found

**Workaround:**
- Create requirements manually in UI
- Use `PUT /requirement/{id}` to update existing requirements
- Use `/requirementtree/add` to create folders (not actual requirements)

**Test Evidence:**
- Scripts: `create_actual_requirement.py`, `try_create_requirement_v2.py`, `try_requirement_bulk_and_import.py`
- All attempts documented in `ZEPHYR-API-DISCOVERIES.md`

**Report to Zephyr:** ⏳ Pending

---

### BLOCKER-002: Test Repository Folder Creation API Broken

**Status:** 🔴 **CRITICAL BLOCKER**  
**Severity:** High  
**Impact:** Prevents autonomous folder creation, blocks testcase creation  
**Date Discovered:** 2025-12-08  
**Confirmed:** 2025-12-08 (via autonomous hierarchy discovery)

**Issue:**
- `POST /testcasetree` returns HTTP 400: `"For input string: \"null\""`
- Error occurs even with minimal payloads (name + projectId only)
- `/testcasetree/add` returns HTTP 405 (Method Not Allowed)
- No working API endpoint for folder creation found

**Attempted Payloads (All Failed):**
1. Minimal (omit parentId): `{"name": "...", "projectId": 45}` → HTTP 400
2. With parentId: 0: `{"name": "...", "projectId": 45, "parentId": 0}` → HTTP 400
3. Wrapped payload: `{"folder": {...}}` → HTTP 400
4. `/testcasetree/add` endpoint → HTTP 405 (Method Not Allowed)

**Autonomous Discovery Results:**
- Tested 4 different payload variations
- All failed with same error
- Confirmed via `full_api_hierarchy_discovery.py` script
- Success rate: 0/4 (0%)

**Impact:**
- Cannot create folders programmatically
- Testcases require `tcrCatalogTreeId` (folder ID)
- Cannot create testcases without folders
- Blocks complete test data creation
- Blocks 50% of entity creation (testcase, execution, allocation)

**Workaround:**
- ✅ Create folders manually in UI (Test Repository)
- ✅ Fetch folder IDs via `GET /testcasetree/projectrepository/{projectId}`
- ✅ Use folder IDs for testcase creation
- Document folder structure for manual setup

**Test Evidence:**
- Script: `test_folder_creation.py`
- Script: `build_comprehensive_spectra_test_project.py` (folder creation section)
- Script: `full_api_hierarchy_discovery.py` (Experiment 3)
- Report: `validation-reports/hierarchy-discovery-summary.md`
- All attempts documented with error responses

**Report to Zephyr:** ⏳ Pending

**Additional Notes:**
- Folder tree is currently empty (`[]`)
- No existing folders to reference
- Blocks testcase creation (requires `tcrCatalogTreeId`)
- Blocks complete test data creation workflow
- **Confirmed as critical blocker via systematic experimentation**

---

### BLOCKER-003: Release Lock Duration >60 Seconds

**Status:** 🟡 **MEDIUM BLOCKER**  
**Severity:** Medium  
**Impact:** Slows automated testing, prevents sequential release→cycle creation  
**Date Discovered:** 2025-12-08  
**Confirmed:** 2025-12-08 (via autonomous hierarchy discovery)

**Issue:**
- Newly created releases lock for MORE than 60 seconds
- Attempting to create cycles during lock period returns HTTP 400: `"Operation failed. The Release with ID{X} and name{Y} is locked. Please try again later."`
- Lock duration is >60 seconds, possibly 2-5 minutes

**Experimental Evidence:**
- 15-second delay: ❌ FAIL - "Release locked"
- 30-second delay: ❌ FAIL - "Release locked"
- 60-second delay: ❌ FAIL - "Release locked"
- **Conclusion:** Lock duration is **>60 seconds**

**Impact:**
- Cannot create cycles immediately after release creation
- Sequential testing becomes very slow (2-5 minute waits per release)
- Blocks rapid iteration during development
- Makes automated test data creation impractical

**Workaround:**
- ✅ **Use existing releases** (no lock, works immediately)
- ✅ Pre-create releases manually in UI before automation
- ✅ Hardcode existing release IDs in scripts
- ✅ Example: Use "The Death Star Project - Phase 1" (ID: 131)

**Test Evidence:**
- Script: `full_api_hierarchy_discovery.py` (Experiment 4)
- Script: `test_with_existing_release.py` (successful with existing release)
- Report: `validation-reports/hierarchy-discovery-summary.md`
- Report: `docs/critical-discovery-release-lock-duration.md`

**Successful Workaround:**
```python
# Use existing release (no lock)
RELEASE_ID = 131  # "The Death Star Project - Phase 1"

# Create cycle immediately (no delay needed)
cycle_payload = {"releaseId": RELEASE_ID, ...}
response = requests.post("/cycle", json=cycle_payload)
# ✅ SUCCESS - Cycle ID: 207 (no wait required)
```

**Report to Zephyr:** ⏳ Pending

**Additional Notes:**
- Existing releases (created days ago) work perfectly
- No lock issues with old releases
- **Recommended approach:** Pre-create releases, use their IDs
- Avoids long delays in automated testing

---

## 🐛 API Bugs

### BUG-001: `/requirementtree/add` Creates Folders, Not Requirements

**Status:** 🐛 **API BEHAVIOR MISMATCH**  
**Severity:** Medium  
**Impact:** Confusion about what endpoint actually does  
**Date Discovered:** 2025-12-08

**Issue:**
- Endpoint name suggests it creates requirements
- Actually creates folders/tree nodes in requirement tree
- No clear distinction between folders and actual requirements in API

**Behavior:**
- Without `parentId`: Creates top-level folder
- With `parentId`: Creates subfolder under parent
- Both create folders, not requirements that appear in table view

**Documentation Gap:**
- Endpoint name misleading
- No clear documentation on difference between folders and requirements
- Requirement table view vs. tree view confusion

**Workaround:**
- Use `/requirementtree/add` for folders only
- Create actual requirements manually in UI
- Use `PUT /requirement/{id}` to update requirements

**Test Evidence:**
- Script: `create_star_wars_requirement.py`
- Script: `create_actual_requirement.py`
- Documented in `ZEPHYR-API-DISCOVERIES.md`

**Report to Zephyr:** ⏳ Pending

---

### BUG-002: Cycle Phase `startDate` Required but Not Documented

**Status:** 🐛 **VALIDATION ERROR**  
**Severity:** Medium  
**Impact:** Cycle creation fails with phases  
**Date Discovered:** 2025-12-08

**Issue:**
- Cycle creation with `cyclePhases` fails: `"Tree phase id not found cannot be null."`
- Error message unclear - suggests missing `treePhaseId`
- Actually requires `startDate` (and `endDate`) for each phase

**Root Cause:**
- Each `cyclePhase` object requires `startDate` field
- Documentation doesn't clearly state this requirement
- Error message doesn't indicate missing `startDate`

**Fix Applied:**
- Added `startDate` to each phase (defaults to cycle's `startDate`)
- Added `endDate` to each phase
- Cycle creation now succeeds

**Test Evidence:**
- Script: `build_comprehensive_spectra_test_project.py`
- Fixed in cycle creation logic

**Report to Zephyr:** ⏳ Pending (documentation update needed)

---

### BUG-003: Release `globalRelease` vs `projectRelease` Conflict

**Status:** 🐛 **API VALIDATION ISSUE**  
**Severity:** Medium  
**Impact:** Release creation fails with confusing error  
**Date Discovered:** 2025-12-08

**Issue:**
- Error: `"Project Release creation not allowed as it is already created at project level."`
- Occurs even when `projectRelease: false`
- Zephyr prevents multiple project-level releases

**Root Cause:**
- Project can only have one project-level release
- Setting `globalRelease: true` avoids this restriction
- Error message doesn't clearly explain the restriction

**Fix Applied:**
- Always set `globalRelease: true` for new releases
- Set `projectRelease: false` to avoid conflicts
- Release creation now succeeds

**Test Evidence:**
- Script: `test_single_entry.py`
- Script: `build_comprehensive_spectra_test_project.py`
- Fixed in release creation logic

**Report to Zephyr:** ⏳ Pending (error message clarity)

---

### BUG-004: Testcase Payload Must Be Wrapped

**Status:** 🐛 **API REQUIREMENT**  
**Severity:** Low  
**Impact:** Testcase creation fails without wrapper  
**Date Discovered:** 2025-12-08

**Issue:**
- Direct testcase payload returns: `"testcase object missing"`
- API requires payload wrapped in `{"testcase": {...}}`

**Fix Applied:**
- Always wrap testcase payload in `{"testcase": {...}}`
- Testcase creation now succeeds

**Test Evidence:**
- Script: `build_comprehensive_spectra_test_project.py`
- Fixed in testcase creation logic

**Report to Zephyr:** ⏳ Pending (documentation update needed)

---

### BUG-005: Folder `parentId: null` Rejected as String

**Status:** 🐛 **API VALIDATION ISSUE**  
**Severity:** Medium  
**Impact:** Folder creation fails (though endpoint is broken anyway)  
**Date Discovered:** 2025-12-08

**Issue:**
- Sending `parentId: null` returns: `"For input string: \"null\""`
- API rejects null as string value
- Must omit field entirely for root folders

**Fix Applied:**
- Omit `parentId` field entirely if `None` or `"ROOT"`
- Don't send `parentId: null` as string

**Note:** This fix doesn't resolve the folder creation blocker (BLOCKER-002), as the endpoint fails even without `parentId`.

**Test Evidence:**
- Script: `build_comprehensive_spectra_test_project.py`
- Fixed in folder creation logic (though endpoint still broken)

**Report to Zephyr:** ⏳ Pending

---

## ⚠️ Documentation Gaps

### DOC-GAP-001: Endpoint Duplicates in Catalog

**Status:** ⚠️ **RESOLVED**  
**Severity:** Low  
**Impact:** Confusion about endpoint uniqueness  
**Date Discovered:** 2025-12-08  
**Date Resolved:** 2025-12-08

**Issue:**
- Embedded endpoint catalog contained 25 duplicate titles
- User requirement: Zero duplicates

**Root Cause:**
- Source `endpoints.json` contained 3 exact duplicates
- Parsing script stripped query/path parameters, causing 22 additional "false" duplicates
- No deduplication logic in parsing

**Resolution:**
- Modified `parse_endpoints.py` to:
  - Preserve `full_path` (including parameters) for uniqueness
  - Extract `query_parameters` and `path_parameters` as separate metadata
  - Implement deduplication based on `(full_path, method)`
- Updated embedded catalog: 224 unique endpoints, zero duplicates
- Created verification scripts

**Test Evidence:**
- Script: `analyze_endpoint_duplicates.py`
- Script: `verify_zero_duplicates.py`
- Documented in `ENDPOINT-DUPLICATES-ROOT-CAUSE.md`

**Report to Zephyr:** ✅ Not needed (internal issue, resolved)

---

### DOC-GAP-002: Requirement API Endpoint Confusion

**Status:** ⚠️ **DOCUMENTED**  
**Severity:** Medium  
**Impact:** Misleading endpoint names and behavior  
**Date Discovered:** 2025-12-08

**Issue:**
- `/requirementtree/add` name suggests requirement creation
- Actually creates folders/tree nodes
- `/requirement` endpoint documented but broken
- No clear distinction between folders and requirements

**Documentation Needed:**
- Clear distinction between requirement folders and actual requirements
- Working endpoint for requirement creation (or fix broken endpoint)
- Better error messages

**Report to Zephyr:** ⏳ Pending

---

## 🔧 Workarounds Implemented

### WORKAROUND-001: Manual Requirement Creation

**For:** BLOCKER-001 (Requirement Creation API Broken)

**Implementation:**
- Create requirements manually in Zephyr UI
- Capture requirement IDs
- Use `PUT /requirement/{id}` to update requirements programmatically
- Use `/requirementtree/add` to create folder structure

**Status:** ✅ Active  
**Documentation:** `prepare.004-create-requirements.md`

---

### WORKAROUND-002: Manual Folder Creation

**For:** BLOCKER-002 (Folder Creation API Broken)

**Implementation:**
- Create folders manually in Zephyr UI (Test Repository)
- Capture folder IDs
- Use folder IDs for testcase creation (`tcrCatalogTreeId`)

**Status:** ✅ Active  
**Documentation:** `Core/memory/journal/2025-12-08-prepare-stage-flow.md`

---

### WORKAROUND-003: Always Use `globalRelease: true`

**For:** BUG-003 (Release Conflict)

**Implementation:**
- Always set `globalRelease: true` for new releases
- Set `projectRelease: false` to avoid conflicts
- Prevents "project release already exists" error

**Status:** ✅ Active  
**Code:** `build_comprehensive_spectra_test_project.py`

---

### WORKAROUND-004: Wrap Testcase Payloads

**For:** BUG-004 (Testcase Payload Wrapper)

**Implementation:**
- Always wrap testcase payload: `{"testcase": {...}}`
- Ensures API accepts payload

**Status:** ✅ Active  
**Code:** `build_comprehensive_spectra_test_project.py`

---

### WORKAROUND-005: Omit `parentId` for Root Folders

**For:** BUG-005 (parentId: null Rejection)

**Implementation:**
- Omit `parentId` field entirely if `None` or `"ROOT"`
- Don't send `parentId: null` as string

**Status:** ✅ Active (though endpoint still broken)  
**Code:** `build_comprehensive_spectra_test_project.py`

---

## 📊 Summary Statistics

**Total Issues:** 7
- **Critical Blockers:** 2
- **API Bugs:** 4
- **Documentation Gaps:** 2 (1 resolved)

**By Status:**
- 🔴 **Critical Blockers:** 2
- 🐛 **API Bugs:** 4
- ⚠️ **Documentation Gaps:** 2
- ✅ **Resolved:** 1
- ⏳ **Pending Report:** 6

**By Impact:**
- **High Impact:** 2 (BLOCKER-001, BLOCKER-002)
- **Medium Impact:** 4 (BUG-001, BUG-002, BUG-003, BUG-005)
- **Low Impact:** 1 (BUG-004)

---

## 📝 Reporting Template

When reporting to Zephyr support, use this template:

```markdown
## Issue: [BLOCKER/BUG ID] - [Title]

**Severity:** [Critical/High/Medium/Low]
**Date Discovered:** [YYYY-MM-DD]
**Environment:** Zephyr Enterprise v3.x
**API Base:** https://velonetic.yourzephyr.com/flex/services/rest/latest

### Description
[Detailed description of the issue]

### Expected Behavior
[What should happen according to documentation]

### Actual Behavior
[What actually happens]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Request/Response Examples
**Request:**
```json
[Example payload]
```

**Response:**
```json
[Error response]
```

### Impact
[How this affects our use case]

### Workaround
[Current workaround, if any]
```

---

## 🔗 Related Documentation

- **Autonomy Blockers:** `AUTONOMY-BLOCKERS-AND-LIMITATIONS.md` - Comprehensive blockers list
- **API Discoveries:** `ZEPHYR-API-DISCOVERIES.md` - Detailed API patterns and gotchas
- **Endpoint Analysis:** `ENDPOINT-DUPLICATES-ROOT-CAUSE.md` - Endpoint catalog issues (resolved)
- **Prepare Stage Flow:** `Core/memory/journal/2025-12-08-prepare-stage-flow.md` - Current workflow with workarounds

---

## 📅 Change Log

**2025-12-08:**
- Initial registry created
- Added BLOCKER-001 (Requirement Creation)
- Added BLOCKER-002 (Folder Creation)
- Added BUG-001 through BUG-005
- Added DOC-GAP-001 (resolved) and DOC-GAP-002
- Documented all workarounds

---

**Last Updated:** 2025-12-08  
**Next Review:** After completing Prepare stage test data creation

