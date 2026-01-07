---
title: "[BLOCKER] [BLOCKER-001] Requirement Creation API Broken"
labels: [
  "project:zephyr",
  "type:bug",
  "type:blocker",
  "vendor:zephyr",
  "severity:high",
  "api-issue",
  "zephyr-support",
  "stage:prepare",
  "playbook:prepare-004-create-requirements"
]
assignees: []
---

**Registry ID:** BLOCKER-001
**Type:** BLOCKER
**Stage:** Prepare
**Playbooks:** `prepare.004-create-requirements`
**Severity:** High
**Status:** 🔴 **CRITICAL BLOCKER**
**Date Discovered:** 2025-12-08
**Report Status:** ⏳ Pending

---

## Description

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

---

## Workaround

- Create requirements manually in UI
- Use `PUT /requirement/{id}` to update existing requirements
- Use `/requirementtree/add` to create folders (not actual requirements)

---

## Test Evidence

- Scripts: `create_actual_requirement.py`, `try_create_requirement_v2.py`, `try_requirement_bulk_and_import.py`
- All attempts documented in `ZEPHYR-API-DISCOVERIES.md`

---

## Related

- Registry: `docs/bug-and-blocker-registry.md`
- Mapping: `docs/issue-to-playbook-mapping.md`
- Playbook: `Core/operations/playbooks/fabric/2-prepare/prepare.004-create-requirements.md`
