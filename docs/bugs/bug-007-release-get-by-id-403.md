# BUG-007: Release GET by ID - Permission Denied

**Status:** ❌ Blocked  
**Severity:** 🟡 Medium  
**Impact:** Cannot validate release creation via GET by ID  
**Discovered:** 2025-12-08  
**Validation Run:** api-validation-20251208-184056.json

---

## Issue

`GET /release/{releaseid}` returns HTTP 403:
```json
{
  "errorMsg": "User does not have access to perform this operation"
}
```

---

## Observations

- ✅ **POST `/release/` works** - Can create releases
- ✅ **GET `/release/project/{projectId}` works** - Can list releases  
- ❌ **GET `/release/{releaseid}` fails** - Cannot get by ID

---

## Root Cause

API token has "create" and "list" permissions but NOT "read by ID" permission for releases.

This is a **Zephyr server-side permission configuration issue**.

---

## Workaround

Skip validation step for releases. Rely on POST response to confirm successful creation.

**Implementation:**
```python
# In comprehensive_api_validation.py
self.test_entity(
    entity_type="releases",
    ...
    skip_validation=True  # BUG-007: GET by ID returns 403
)
```

---

## Test Evidence

**Validation Run:** 2025-12-08T18:40:56Z

**Created release ID 140:**
```json
{
  "id": 140,
  "name": "API Validation Test Release",
  "projectId": 45,
  "globalRelease": true
}
```

**GET validation attempt:**
```bash
GET /release/140
Response: HTTP 403
{
  "errorMsg": "User does not have access to perform this operation"
}
```

---

## Impact

**Low-Medium:** 
- Blocks full round-trip validation for releases
- Does NOT block release creation (POST works)
- Does NOT block listing releases (GET list works)
- Only affects validation of individual release retrieval

---

## Report Status

🟡 **Pending Report** - To be reported to Zephyr support (low priority)

---

## Related

- Comprehensive API validation script: `scripts/comprehensive_api_validation.py`
- Validation reports: `validation-reports/`

