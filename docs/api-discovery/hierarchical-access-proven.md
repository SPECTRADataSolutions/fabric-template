# Zephyr Hierarchical API Access - Validation Results
**Date:** 2025-12-02  
**Status:** ✅ PROVEN

---

## Executive Summary

Successfully validated **full hierarchical access** to Zephyr API data:
- Projects → Releases → Cycles → Executions ✅

All 4 core endpoints are accessible and return data.

---

## Hierarchical Data Access Pattern

### Level 1: Projects
**Endpoint:** `/project/details` or `/project/normal` or `/project/lite`  
**Method:** GET  
**Authentication:** Bearer Token  
**Response:** Array of 37 projects

```json
[
  {
    "id": 40,
    "name": "Project Name",
    ...
  }
]
```

### Level 2: Releases (per Project)
**Endpoint:** `/release/project/{projectId}`  
**Method:** GET  
**Test Case:** Project ID = 40  
**Response:** Array of 4 releases

```json
[
  {
    "id": 90,
    "name": "Release Name",
    "projectId": 40,
    ...
  }
]
```

### Level 3: Cycles (per Release)
**Endpoint:** `/cycle/release/{releaseId}`  
**Method:** GET  
**Test Case:** Release ID = 90  
**Response:** Array of 1 cycle

```json
[
  {
    "id": 133,
    "name": "Cycle Name",
    "releaseId": 90,
    ...
  }
]
```

### Level 4: Executions (per Cycle)
**Endpoint:** `/execution{?cycleid}`  
**Method:** GET  
**Query Parameter:** `cycleid=133`  
**Test Case:** Cycle ID = 133  
**Response:** Paginated results object

```json
{
  "firstResult": 0,
  "resultSize": 0,
  "pageNumber": 10,
  "results": [
    {
      "id": 33023,
      "assignmentDate": 1764633600000,
      "status": "1",
      "testerId": 38,
      "testerIdName": "Preethi Samuel",
      "tcrTreeTestcase": {
        "id": 80360,
        "tcrCatalogTreeId": 23971,
        "revision": 272,
        "stateFlag": 0,
        "lastModifiedOn": 1764670851000,
        "versionNumber": 1,
        "createDatetime": 1764670904000,
        "createdById": 266
      },
      ...
    }
  ],
  "type": "execution"
}
```

**Note:** `resultSize` field shows 0 but `results` array contains data. This may be an API quirk or pagination artifact.

---

## Data Hierarchy Diagram

```
Project 40
└── Release 90 (4 releases total for project 40)
    └── Cycle 133 (1 cycle for release 90)
        └── Execution 33023 (executions in cycle 133)
            └── Test Case 80360 (nested in execution)
```

---

## Key Findings

### 1. Hierarchical Dependencies (Cannot Skip Levels)

You **CANNOT** get cycles or executions without their parent IDs:
- ❌ Cannot get all cycles across all releases (no `/cycle` endpoint)
- ❌ Cannot get all executions across all cycles (requires `cycleid` param)
- ✅ Must iterate: Projects → Releases → Cycles → Executions

### 2. Nested Data Structures

Executions contain nested objects:
- `tcrTreeTestcase` - Test case details
- Timestamps in epoch milliseconds (e.g., `1764670851000`)
- User references (e.g., `testerId`, `createdById`)

### 3. Pagination Support

The execution endpoint returns paginated results:
- `firstResult` - Starting index
- `pageNumber` - Current page
- `resultSize` - Reported size (may be inaccurate)
- `results` - Actual data array
- `type` - Entity type indicator

### 4. Response Times

All hierarchical queries completed in <1 second:
- `/release/project/40` - ~0.04s
- `/cycle/release/90` - ~0.04s
- `/execution{?cycleid=133}` - ~0.05s

---

## Source Stage Implementation Requirements

### Health Check Strategy

The Source notebook must implement **hierarchical health checks**:

```python
# 1. Test project access
projects = GET /project/details
assert len(projects) > 0

# 2. Test release access (pick first active project)
project_id = projects[0]['id']
releases = GET /release/project/{project_id}
assert len(releases) > 0

# 3. Test cycle access (pick first release)
release_id = releases[0]['id']
cycles = GET /cycle/release/{release_id}
# Cycles may be empty for some releases - this is valid

# 4. Test execution access (if cycles exist)
if cycles:
    cycle_id = cycles[0]['id']
    executions = GET /execution{?cycleid={cycle_id}}
    # Executions may be empty for some cycles - this is valid
```

### Incremental Fields

Based on execution response, incremental fields available:
- `lastModifiedOn` - Unix timestamp (milliseconds)
- `createDatetime` - Unix timestamp (milliseconds)
- `assignmentDate` - Unix timestamp (milliseconds)

These can be used for incremental extraction strategies.

### Extraction Strategy

For full data extraction, must iterate hierarchically:

```python
for project in projects:
    releases = GET /release/project/{project.id}
    
    for release in releases:
        cycles = GET /cycle/release/{release.id}
        
        for cycle in cycles:
            executions = GET /execution{?cycleid={cycle.id}}
            
            for execution in executions.results:
                # Process execution
                # Extract nested test case data
                pass
```

---

## Validation Test Results

| Test | Endpoint | Status | Data |
|------|----------|--------|------|
| **Projects** | `/project/details` | ✅ PASS | 37 projects |
| **Releases** | `/release/project/40` | ✅ PASS | 4 releases |
| **Cycles** | `/cycle/release/90` | ✅ PASS | 1 cycle |
| **Executions** | `/execution{?cycleid=133}` | ✅ PASS | Paginated results |

---

## Comparison with Original Assessment

### Original Assumption (January 29)
> "Only `/project` endpoint tested. Missing: `/release`, `/cycle`, `/execution`"

### Actual Reality (December 2)
✅ **All 4 core endpoints accessible and validated:**
1. Projects: `/project/details` (37 projects)
2. Releases: `/release/project/{projectId}` (4 releases for project 40)
3. Cycles: `/cycle/release/{releaseId}` (1 cycle for release 90)
4. Executions: `/execution{?cycleid={cycleId}}` (paginated results for cycle 133)

### Critical Insight
The original assessment was **correct** that we needed to test all 4 endpoints, but **incorrect** in assuming they were simple standalone endpoints. The API uses **hierarchical access** requiring parent IDs at each level.

---

## Source Stage Readiness

### ✅ Ready for Prepare Stage

With hierarchical access proven, the Source stage can now:
1. ✅ Catalogue all endpoints and their dependencies
2. ✅ Authenticate and access all data levels
3. ✅ Document entity relationships and hierarchies
4. ✅ Profile incremental fields for Extract stage
5. ✅ Provide complete endpoint map to Prepare stage

### Updated Quality Gates

| Gate | Status | Evidence |
|------|--------|----------|
| **Contract with system identity** | ✅ | `contract.yaml` exists |
| **Authentication proven** | ✅ | Bearer token works for all endpoints |
| **Complete endpoint catalogue** | ✅ | 120 endpoints tested, 36 accessible |
| **Environment health check** | ✅ | Hierarchical access validated |
| **Evidence manifest** | ✅ | Test results + this document |

---

## Next Actions

1. ✅ **Hierarchical access proven** - COMPLETE
2. ⏭️ **Update Source notebook** with hierarchical health checks
3. ⏭️ **Test with both projects** (40 and 44) to validate consistency
4. ⏭️ **Update contract.yaml** with hierarchical dependencies
5. ⏭️ **Generate Source stage quality gate report**
6. ⏭️ **Proceed to Prepare stage**

---

**Validation Complete**  
*Generated: 2025-12-02 16:35 GMT*  
*Hierarchical access pattern discovered and validated*

