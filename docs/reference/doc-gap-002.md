---
title: "[DOC-GAP] [DOC-GAP-002] Requirement API Endpoint Confusion"
labels: [
  "project:zephyr",
  "type:documentation",
  "vendor:zephyr",
  "severity:medium",
  "api-issue",
  "zephyr-support",
  "stage:prepare",
  "playbook:prepare-004-create-requirements"
]
assignees: []
---

**Registry ID:** DOC-GAP-002
**Type:** DOC-GAP
**Stage:** Prepare
**Playbooks:** `prepare.004-create-requirements`
**Severity:** Medium
**Status:** ⚠️ **DOCUMENTED**
**Date Discovered:** 2025-12-08
**Report Status:** ⏳ Pending

---

## Description

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

---

## Related

- Registry: `docs/bug-and-blocker-registry.md`
- Mapping: `docs/issue-to-playbook-mapping.md`
- Playbook: `Core/operations/playbooks/fabric/2-prepare/prepare.004-create-requirements.md`
