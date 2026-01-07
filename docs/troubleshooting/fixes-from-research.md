# Validation Fixes from Research Docs

> **Source:** `ZEPHYR-API-DISCOVERIES.md` and `zephyr-research-summary.md`  
> **Date:** 2025-12-08

---

## ✅ Solutions Found

### 1. **Testcases - CORRECT ENDPOINT CONFIRMED**

**From Research:**
```markdown
### Endpoint: `/testcase` (POST)
Status: ⚠️ PENDING (blocked by folder creation)

Payload Structure (Expected):
{
  "testcase": {  // WRAPPED FORMAT - CRITICAL
    "name": "Testcase Name",
    "description": "Testcase description",
    "tcrCatalogTreeId": 123,  // REQUIRED: Folder tree node ID
    "projectId": 45
  }
}

⚠️ Gotcha:
- Testcase payload must be wrapped in {"testcase": {...}} object
- Requires tcrCatalogTreeId - folder tree node ID
```

**Current Problem:**
- Catalog mapper is returning `/testcasetree` (creates folders)
- Should return `/testcase` (creates testcases)

**Fix:**
Update `load_sdk_catalog.py` to specifically find `/testcase/` POST endpoint, not `/testcasetree`.

---

### 2. **Cycles - Payload Structure Issue**

**From Research:**
```markdown
### Endpoint: `/cycle` (POST)
Status: ✅ WORKING (without phases) | ⚠️ INVESTIGATING (with phases)

Payload Structure (Without Phases - Working):
{
  "name": "Cycle Name",
  "description": "Cycle description",
  "environment": "Production",
  "build": "1.0.0",
  "revision": 1,
  "status": 0,  // 0=Draft, 1=Active, 2=Completed
  "startDate": 1733529600000,
  "endDate": 1765065600000,
  "releaseId": 131
  // Omit cyclePhases for now
}

Payload Structure (With Phases - Investigating):
{
  ..., 
  "cyclePhases": [
    {
      "name": "Phase Name",
      "startDate": 1733529600000,  // REQUIRED
      "endDate": 1765065600000     // REQUIRED
    }
  ]
}

⚠️ Gotcha:
- cyclePhases startDate/endDate are REQUIRED
- We've added these, but still getting HTTP 400
```

**Current Problem:**
- POST `/cycle/` returns HTTP 400
- Payload includes `cyclePhases` with `startDate`/`endDate`
- Research says it works WITHOUT phases, but WITH phases is "investigating"

**Fix Options:**
1. **Try without cyclePhases first** (research says this works)
2. Review date format (milliseconds vs ISO string)
3. Check if cyclePhases needs different structure

---

### 3. **Releases - GET by ID Not Documented**

**From Research:**
- POST `/release` is ✅ WORKING
- GET by ID not covered in research docs
- But we know POST works and creates releases successfully

**Current Problem:**
- POST creates release (ID 137) ✅
- GET `/release/137` returns HTTP 403

**Possible Causes:**
1. **Wrong endpoint format** - Maybe need `/release/project/{projectId}` instead?
2. **Permissions** - Token might not have GET by ID permission
3. **Endpoint doesn't exist** - May only support GET all or GET by project

**From SDK Catalog:**
```python
{
    "endpoint_path": "/release",
    "full_path": "/release/{releaseid}",
    "http_method": "GET",
    "description": "Get Release by Release ID"
}
```

**Fix:**
Test manually with different formats:
- `GET /release/137`
- `GET /release/137/` (trailing slash)
- `GET /release?id=137` (query param)

---

### 4. **Requirements - Known Broken**

**From Research:**
```markdown
#### `/requirement` (POST)
Status: ❌ BROKEN - DOES NOT WORK (despite being documented)

Reality:
- Returns HTTP 500: "Cannot invoke \"java.lang.Long.longValue()\" because \"id\" is null"
- This is the endpoint that SHOULD create requirements, but it's broken

#### `/requirement/{id}` (GET)
Status: ✅ WORKS FOR READING
- Successfully retrieves requirement details after UI creation
```

**Current Problem:**
- POST `/requirementtree/add` works (creates folders) ✅
- GET `/requirement/702` returns HTTP 500

**Conclusion:**
GET by ID might not work. Accept this as a known limitation.

---

## 🔧 Implementation Fixes

### Fix 1: Update Catalog Mapper for Testcases

```python
# In load_sdk_catalog.py - group_endpoints_by_entity()

# Special handling for testcases
if category == "testcases":
    for ep in endpoints:
        method = ep.get("http_method")
        path = ep.get("endpoint_path", "")
        
        if method == "POST":
            # Look for exact /testcase endpoint (not /testcasetree!)
            if path == "/testcase" or path == "/testcase/":
                entity_endpoints["POST"] = ep
```

### Fix 2: Simplify Cycle Payload (Remove Phases)

```python
# In comprehensive_api_validation.py - test_all_entities()

payload={
    "projectId": self.project_id,
    "releaseId": release_id,
    "name": "API Validation Test Cycle",
    "description": "Automated validation test cycle",
    "environment": "Production",
    "build": "1.0.0",
    "revision": 1,
    "status": 0,
    "startDate": int(datetime.now().timestamp() * 1000),
    "endDate": int(datetime(2025, 12, 31).timestamp() * 1000)
    # OMIT cyclePhases - research says this works
}
```

### Fix 3: Test Release GET Manually

```bash
# Test these variations manually
curl -H "Authorization: Bearer $TOKEN" \
  https://velonetic.yourzephyr.com/flex/services/rest/latest/release/137

curl -H "Authorization: Bearer $TOKEN" \
  https://velonetic.yourzephyr.com/flex/services/rest/latest/release/137/

# If both fail, accept GET by ID doesn't work
```

---

## 📊 Expected Outcomes After Fixes

1. **Testcases:** Should POST successfully to `/testcase` with wrapped payload
2. **Cycles:** Should POST successfully without `cyclePhases`
3. **Releases:** May still fail validation, but document as known limitation
4. **Requirements:** Accept validation failure as known limitation

---

**Next:** Implement fixes and re-run validation

