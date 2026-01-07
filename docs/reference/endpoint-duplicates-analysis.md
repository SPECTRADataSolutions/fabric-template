# Zephyr Endpoint Duplicates Analysis

> **Date:** 2025-12-08  
> **Status:** 🟡 Analysis Complete  
> **Purpose:** Document duplicate endpoint titles and identify if they're due to URL changes

---

## 📊 Summary

- **Total endpoints:** 228
- **Unique descriptions:** 205
- **Duplicate titles:** 19

**Finding:** ✅ **YES - Most duplicates are due to URL changes** (different `endpoint_path` values)

---

## 🔍 Duplicate Categories

### 1. **URL Changes (Different Paths)** - 13 duplicates

These duplicates have the same title but different endpoint paths, indicating API versioning or URL restructuring:

| Title | Path 1 | Path 2 | Notes |
|-------|--------|--------|-------|
| Bulk Update Testcase values | `PUT /testcase/bulk` | `PUT /testcase/update/bulk` | URL restructuring |
| Get All Users Present in the System. | `GET /user/filter` | `GET /user` | Different query methods |
| Get All user preferences | `GET /admin/ldap/default/settings` | `GET /admin/user/preference` | Different admin endpoints |
| Get Count Of Testcases By Phase ids. | `GET /testcase/count/ids` | `GET /testcase/count` | URL versioning |
| Get License Information | `GET /license`<br>`GET /system/info/license`<br>`GET /system/info/servertime`<br>`GET /system/info/stats` | (4 different paths) | Multiple ways to get license info |
| Get Schedules by Criteria | `GET /execution/user/project` | `GET /execution` | Filtered vs. general |
| Get Testcase by Criteria | `GET /testcase/planning` | `GET /testcase` | Planning-specific vs. general |
| Get Testcase by ID | `GET /testcase` | `GET /testcase/altid` | ID vs. ALT ID lookup |
| Get Testcase usage history details | `GET //executionchangehistory` | `GET /tcuh/testcase` | URL restructuring (note: double slash in first) |
| Get Traceable Path from Root | `GET /testcase/path` | `GET /testcase/pathbyrelease` | Release-specific variant |
| Search via filters | `POST /advancesearch`<br>`POST /advancesearch/zql` (3x) | (2 different paths, one appears 3x) | ZQL vs. standard search |
| Update tree node values | `PUT /testcasetree/assignuser` | `PUT /testcasetree` | Specific vs. general update |
| get Scheduled job via scheduled job id | `GET /automation/schedule` | `GET /fileWatcher/watcher` | Different automation endpoints |
| get status count for releaseid | `GET /cycle/status/count` | `PUT /cycle/toggle` | ⚠️ Different methods too |

**Recommendation:** These are **legitimate duplicates** - different endpoints that happen to have similar descriptions. Consider:
- Updating descriptions to be more specific (e.g., "Get License Information (System Info)" vs. "Get License Information (Direct)")
- Documenting which endpoint to use when (if one is deprecated)

---

### 2. **True Duplicates (Same Path + Method)** - 5 duplicates

These are actual duplicates that should be deduplicated:

| Title | Path | Method | Count |
|-------|------|--------|-------|
| Create Cycle Phase | `POST /cycle` | POST | 2 |
| Create teststep | `POST /testcase` | POST | 2 |
| Get all tags | `GET /testcase/tags` | GET | 2 |
| Update Testcase values | `PUT /testcase` | PUT | 2 |

**Recommendation:** ⚠️ **These should be deduplicated** - same endpoint appears twice in catalog.

---

### 3. **Malformed Entry** - 1 duplicate

| Title | Path | Method | Issue |
|-------|------|--------|-------|
| Search and Edit the Testcase | `PUT /testcase/search/update/bulk` | PUT | Normal |
| Search and Edit the Testcase | `/TESTCASE/SEARCH/ALLOCATE/BULK/REQUIREMENT /testcase/search/update/bulk` | (mixed) | ⚠️ **MALFORMED** - uppercase prefix + duplicate path |

**Recommendation:** 🔴 **Fix this entry** - appears to be a parsing error or malformed data.

---

## 🎯 Action Items

### High Priority

1. **Deduplicate true duplicates** (5 endpoints):
   - `POST /cycle` (Create Cycle Phase) - appears 2x
   - `POST /testcase` (Create teststep) - appears 2x
   - `GET /testcase/tags` (Get all tags) - appears 2x
   - `PUT /testcase` (Update Testcase values) - appears 2x

2. **Fix malformed entry**:
   - `Search and Edit the Testcase` - has malformed path with uppercase prefix

### Medium Priority

3. **Clarify descriptions** for URL change duplicates:
   - Add specificity to distinguish between similar endpoints
   - Document which endpoint is preferred (if one is deprecated)

4. **Investigate "Get License Information"**:
   - 4 different endpoints with same title
   - Determine if all are needed or if some are deprecated

### Low Priority

5. **Document URL versioning**:
   - Create mapping of old vs. new endpoint paths
   - Note which endpoints are deprecated

---

## 📝 Technical Details

**Analysis Method:**
- Parsed embedded `ZEPHYR_ENDPOINTS_CATALOG` from `spectraSDK.Notebook/notebook_content.py`
- Grouped endpoints by `description` field
- Compared `endpoint_path`, `http_method`, and `category` for duplicates

**Script:** `scripts/analyze_endpoint_duplicates.py`

---

## 🔗 Related Documentation

- `docs/ZEPHYR-API-DISCOVERIES.md` - API patterns and gotchas
- `docs/ZEPHYR-RESEARCH-SUMMARY.md` - Complete research summary
- `spectraSDK.Notebook/notebook_content.py` - Embedded endpoints catalog

---

**Last Updated:** 2025-12-08

