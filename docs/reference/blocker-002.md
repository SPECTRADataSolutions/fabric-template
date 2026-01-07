---
title: "[BLOCKER] [BLOCKER-002] Test Repository Folder Creation API Broken"
labels: [
  "project:zephyr",
  "type:bug",
  "type:blocker",
  "vendor:zephyr",
  "severity:high",
  "api-issue",
  "zephyr-support",
  "stage:prepare",
  "playbook:prepare-001-createTestData"
]
assignees: []
---

**Registry ID:** BLOCKER-002
**Type:** BLOCKER
**Stage:** Prepare
**Playbooks:** `prepare.001-createTestData`
**Severity:** High
**Status:** 🔴 **CRITICAL BLOCKER**
**Date Discovered:** 2025-12-08
**Report Status:** ⏳ Pending

---

## Description

**Status:** 🔴 **CRITICAL BLOCKER**  
**Severity:** High  
**Impact:** Prevents autonomous folder creation, blocks testcase creation  
**Date Discovered:** 2025-12-08

**Issue:**
- `POST /testcasetree` returns HTTP 400: `"For input string: \"null\""`
- Error occurs even with minimal payloads (name + projectId only)
- `/testcasetree/add` returns HTTP 405 (Method Not Allowed)
- No working API endpoint for folder creation found

**Attempted Payloads (All Failed):**
1. Minimal: `{"name": "...", "projectId": 45}`
2. With description: `{"name": "...", "description": "...", "projectId": 45}`
3. Wrapped: `{"testcasetree": {...}}`
4. All return same error: `"For input string: \"null\""`

**Impact:**
- Cannot create folders programmatically
- Testcases require `tcrCatalogTreeId` (folder ID)
- Cannot create testcases without folders
- Blocks complete test data creation

**Workaround:**
- Create folders manually in UI
- Capture folder IDs for testcase creation
- Document folder structure for manual setup

**Test Evidence:**
- Script: `test_folder_creation.py`
- Script: `build_comprehensive_spectra_test_project.py` (folder creation section)
- All attempts documented with error responses

**Report to Zephyr:** ⏳ Pending

**Additional Notes:**
- Folder tree is currently empty (`[]`)
- No existing folders to reference
- Blocks testcase creation (requires `tcrCatalogTreeId`)
- Blocks complete test data creation workflow

---

## 🐛 API Bugs

---

## Workaround

- Create folders manually in UI
- Capture folder IDs for testcase creation
- Document folder structure for manual setup

---

## Test Evidence

- Script: `test_folder_creation.py`
- Script: `build_comprehensive_spectra_test_project.py` (folder creation section)
- All attempts documented with error responses

---

## Related

- Registry: `docs/bug-and-blocker-registry.md`
- Mapping: `docs/issue-to-playbook-mapping.md`
- Playbook: `Core/operations/playbooks/fabric/2-prepare/prepare.001-createTestData.md`
