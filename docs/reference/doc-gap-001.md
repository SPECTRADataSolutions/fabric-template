---
title: "[DOC-GAP] [DOC-GAP-001] Endpoint Duplicates in Catalog"
labels: [
  "project:zephyr",
  "type:documentation",
  "vendor:zephyr",
  "severity:low",
  "api-issue",
  "zephyr-support",
  "stage:source",
  "playbook:source-003-bootstrapEndpoints"
]
assignees: []
---

**Registry ID:** DOC-GAP-001
**Type:** DOC-GAP
**Stage:** Source
**Playbooks:** `source.003-bootstrapEndpoints`
**Severity:** Low
**Status:** ⚠️ **RESOLVED**
**Date Discovered:** 2025-12-08
**Report Status:** ✅ Not needed (internal issue, resolved)

---

## Description

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

---

## Test Evidence

- Script: `analyze_endpoint_duplicates.py`
- Script: `verify_zero_duplicates.py`
- Documented in `ENDPOINT-DUPLICATES-ROOT-CAUSE.md`

---

## Related

- Registry: `docs/bug-and-blocker-registry.md`
- Mapping: `docs/issue-to-playbook-mapping.md`
- Playbook: `Core/operations/playbooks/fabric/1-source/source.003-bootstrapEndpoints.md`
