# Zephyr Endpoint Catalog & Dimensional Model Mapping
**Date:** 2025-12-02  
**Purpose:** Comprehensive catalog of working endpoints, data provided, and dimensional model mapping

---

## Executive Summary

**Working Endpoints:** 36 out of 120 tested  
**Data Entities:** 7 major categories  
**Dimensional Model:** 4 Facts, 8 Dimensions identified

**Naming Convention:** camelCase for all tables (e.g., `factTestExecution`, `dimProject`)

---

## Endpoint Catalog by Business Entity

### 1. PROJECTS (Dimension) ⭐

Projects represent test management workspaces and are the top-level container.

#### Working Endpoints

| Endpoint | Records | What It Provides | Dimensional Role |
|----------|---------|------------------|------------------|
| `/project/details` | 37 | Complete project metadata, settings, owners | **dimProject** |
| `/project/normal` | 37 | Project list with basic attributes | **dimProject** (alternative) |
| `/project/lite` | 37 | Lightweight project list | **dimProject** (minimal) |
| `/project/all/leads` | 1 | Project leads/owners | **dimProject** attribute |
| `/project/count/allprojects` | 1 | Total project count | Metric |
| `/project/count/allusers` | 1 | Total user count | Metric |
| `/project/allocated/projects` | 1 | Allocated projects count | Metric |
| `/project/shared` | 33 | Shared projects list | **dimProject** flag |
| `/project/sharedprojects/{projectid}` | 1 | Projects shared FROM this project | Bridge table |
| `/project/sharedtoprojects/{projectid}` | 0 | Projects shared TO this project | Bridge table |

#### Sample Data Structure
```json
{
  "id": 40,
  "name": "Project Name",
  "description": "Project Description",
  "projectLead": "User Name",
  "startDate": 1234567890000,
  "endDate": 1234567890000,
  "shared": true/false,
  "active": true/false
}
```

#### Dimensional Model: dimProject
```
dimProject
├── ProjectKey (PK)
├── ProjectID (Business Key)
├── ProjectName
├── ProjectDescription
├── ProjectLead
├── StartDate
├── EndDate
├── IsShared (Boolean)
├── IsActive (Boolean)
└── SharedProjectCount
```

---

### 2. RELEASES (Dimension) ⭐

Releases group test cycles for a project version/release.

#### Working Endpoints

| Endpoint | Records | What It Provides | Dimensional Role |
|----------|---------|------------------|------------------|
| `/release` | 77 | All releases across all accessible projects | **dimRelease** |
| `/release/project/{projectid}` | 4 | Releases for specific project (tested: project 40) | **dimRelease** (filtered) |

#### Sample Data Structure
```json
{
  "id": 90,
  "name": "Release 1.0",
  "description": "Release description",
  "projectId": 40,
  "startDate": 1234567890000,
  "endDate": 1234567890000,
  "releaseStatus": "Active/Completed",
  "version": "1.0"
}
```

#### Dimensional Model: dimRelease
```
dimRelease
├── ReleaseKey (PK)
├── ReleaseID (Business Key)
├── ReleaseName
├── ReleaseDescription
├── ProjectKey (FK → dimProject)
├── ReleaseVersion
├── ReleaseStatus
├── StartDate
├── EndDate
└── DaysBetween (Calculated)
```

---

### 3. CYCLES (Dimension) ⭐

Test cycles organize test executions within a release.

#### Working Endpoints

| Endpoint | Records | What It Provides | Dimensional Role |
|----------|---------|------------------|------------------|
| `/cycle/release/{releaseid}` | 1 | Cycles for specific release (tested: release 90) | **dimCycle** |

**Note:** No endpoint for "all cycles" - must iterate releases to get cycles.

#### Sample Data Structure
```json
{
  "id": 133,
  "name": "Cycle 1",
  "description": "Cycle description",
  "releaseId": 90,
  "startDate": 1234567890000,
  "endDate": 1234567890000,
  "environment": "UAT/Production",
  "build": "Build 1.0.1"
}
```

#### Dimensional Model: dimCycle
```
dimCycle
├── CycleKey (PK)
├── CycleID (Business Key)
├── CycleName
├── CycleDescription
├── ReleaseKey (FK → dimRelease)
├── Environment
├── Build
├── StartDate
├── EndDate
└── DaysBetween (Calculated)
```

---

### 4. EXECUTIONS (Fact) ⭐⭐⭐

**PRIMARY FACT TABLE** - Test executions are the core transactional data.

#### Working Endpoints

| Endpoint | Records | What It Provides | Dimensional Role |
|----------|---------|------------------|------------------|
| `/execution{?cycleid}` | Paginated | Executions for specific cycle (tested: cycle 133) | **factTestExecution** |

**Note:** No endpoint for "all executions" - must iterate cycles to get executions.

#### Sample Data Structure
```json
{
  "id": 33023,
  "assignmentDate": 1764633600000,
  "executionDate": 1764670851000,
  "status": "1",  // Status code (Pass/Fail/Blocked/etc)
  "testerId": 38,
  "testerIdName": "Preethi Samuel",
  "cycleId": 133,
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
  "actualTime": 3600000,  // milliseconds
  "estimatedTime": 7200000
}
```

#### Dimensional Model: factTestExecution
```
factTestExecution (Grain: One row per test execution)
├── ExecutionKey (PK, Surrogate)
├── ExecutionID (Business Key)
├── CycleKey (FK → dimCycle)
├── TestCaseKey (FK → dimTestCase)
├── TesterKey (FK → dimUser)
├── ExecutionDateKey (FK → dimDate)
├── AssignmentDateKey (FK → dimDate)
├── ExecutionStatusKey (FK → dimExecutionStatus)
├── ActualTimeMinutes (Measure)
├── EstimatedTimeMinutes (Measure)
├── TimeVarianceMinutes (Calculated Measure)
└── LastModifiedDate
```

**Measures:**
- Count of Executions
- Pass Count
- Fail Count
- Blocked Count
- Pass Rate (%)
- Average Execution Time
- Time Variance (Actual vs Estimated)

---

### 5. TEST CASES (Dimension) ⭐

Test case repository and structure.

#### Working Endpoints

| Endpoint | Records | What It Provides | Dimensional Role |
|----------|---------|------------------|------------------|
| `/testcase/tags` | 30 | All test case tags | **dimTestCaseTag** |
| `/testcasetree/projectrepository/{projectid}` | 9 | Test case tree structure for project | **dimTestCaseTree** / Hierarchy |

#### Dimensional Model: dimTestCase
```
dimTestCase (Type 2 SCD - versioned)
├── TestCaseKey (PK, Surrogate)
├── TestCaseID (Business Key)
├── TestCaseVersionID (Business Key)
├── TestCaseName
├── TestCaseDescription
├── TreeID (FK → dimTestCaseTree)
├── Priority
├── Revision
├── VersionNumber
├── CreatedDate
├── LastModifiedDate
├── EffectiveFromDate (SCD Type 2)
├── EffectiveToDate (SCD Type 2)
└── IsCurrent (Boolean)
```

---

### 6. USERS (Dimension) ⭐

Users who create, execute, and manage tests.

#### Working Endpoints

| Endpoint | Records | What It Provides | Dimensional Role |
|----------|---------|------------------|------------------|
| `/user/defect` | 2 | Defect users/owners | **dimUser** subset |
| `/usertoken` | 3 | User tokens (API access) | **dimUser** attribute |
| `/admin/user/preference` | 212 | User preferences | **dimUser** attributes |

#### Dimensional Model: dimUser
```
dimUser
├── UserKey (PK, Surrogate)
├── UserID (Business Key)
├── UserName
├── UserEmail
├── UserRole
├── IsActive (Boolean)
├── CreatedDate
└── LastLoginDate
```

---

### 7. CONFIGURATION & METADATA (Dimensions)

#### Working Endpoints

| Category | Endpoint | Records | Dimensional Role |
|----------|----------|---------|------------------|
| **Admin** | `/admin/preference/admin` | 76 | Configuration settings |
| **Admin** | `/admin/app` | 23 | Application settings |
| **Admin** | `/admin/preference/lov/all` | 65 | List of values |
| **Admin** | `/admin/preference/all` | 212 | All preferences |
| **Admin** | `/admin/preference/anonymous` | 91 | Anonymous preferences |
| **Admin** | `/admin/backup/schedule` | 1 | Backup schedule |
| **Admin** | `/admin/ldap/default/settings` | 1 | LDAP settings |
| **Fields** | `/field/fieldtype` | 16 | **dimFieldType** |
| **Fields** | `/field/importfields/{entityName}` | 0 | Import field mappings |
| **Fields** | `/field/entity/{entityname}` | 0 | Entity field definitions |
| **System** | `/info/license` | 1 | License information |
| **System** | `/license/` | 1 | License details |
| **System** | `/system/info/cache/info` | 1 | Cache statistics |
| **System** | `/system/info/license` | 1 | System license info |
| **System** | `/system/info/stats` | 1 | System statistics |
| **Templates** | `/parsertemplate` | 9 | Parser templates |
| **Search** | `/advancesearch/reindex/health` | 1 | Search health |
| **Repository** | `/global-repository/project` | 0 | Global repository projects |

#### Dimensional Model: dimExecutionStatus
```
dimExecutionStatus (Reference/Lookup)
├── ExecutionStatusKey (PK)
├── StatusCode (Business Key, e.g., "1", "2", "3")
├── StatusName (e.g., "Pass", "Fail", "Blocked")
├── StatusCategory (e.g., "Success", "Failure", "Pending")
└── SortOrder
```

---

## Complete Dimensional Model Architecture

### Star Schema Design

```
         dimProject
              |
         dimRelease
              |
         dimCycle
              |
              ↓
    ┌─────────────────────┐
    │ factTestExecution  │ ← dimTestCase
    │  (Grain: 1 per exec)│ ← dimUser (Tester)
    └─────────────────────┘ ← dimExecutionStatus
              ↓               ← dimDate (Execution)
         dimDate            ← dimDate (Assignment)
```

### Fact Tables

#### factTestExecution (Primary)
**Grain:** One row per test execution  
**Keys:** Cycle, TestCase, Tester, ExecutionDate, AssignmentDate, Status  
**Measures:** Count, ActualTime, EstimatedTime, TimeVariance  
**Source:** `/execution{?cycleid}` (must iterate cycles)

#### factTestStep (Optional - Future)
**Grain:** One row per test step result  
**Keys:** Execution, TestStep, User  
**Measures:** StepDuration, StepStatus  
**Source:** Not yet tested

### Dimension Tables

1. **dimProject** - Source: `/project/details`
2. **dimRelease** - Source: `/release`
3. **dimCycle** - Source: `/cycle/release/{releaseid}`
4. **dimTestCase** - Source: `/testcasetree/...` + execution nesting
5. **dimUser** - Source: `/user/*` endpoints
6. **dimExecutionStatus** - Source: Hardcoded or `/admin/preference/lov/all`
7. **dimDate** - Source: Generated calendar table
8. **dimTestCaseTree** - Source: `/testcasetree/projectrepository/{projectid}`

---

## Data Extraction Strategy

### Hierarchical Extraction Pattern

```python
# Level 1: Projects (Dimension)
projects = extract("/project/details")  # 37 records

for project in projects:
    # Level 2: Releases (Dimension)
    releases = extract(f"/release/project/{project.id}")  # 4 per project
    
    for release in releases:
        # Level 3: Cycles (Dimension)
        cycles = extract(f"/cycle/release/{release.id}")  # 1 per release
        
        for cycle in cycles:
            # Level 4: Executions (FACT)
            page = 0
            while True:
                executions = extract(
                    f"/execution",
                    params={"cycleid": cycle.id, "page": page}
                )
                
                if not executions.results:
                    break
                    
                # Process fact records
                load_to_fact_table(executions.results)
                page += 1
```

### Parallel Extraction Optimization

```python
# After initial project/release/cycle dimensions loaded,
# parallelize execution extraction:

from concurrent.futures import ThreadPoolExecutor

cycle_ids = get_all_cycle_ids_from_dim()

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(extract_executions_for_cycle, cycle_ids)
```

---

## Failed Endpoints & Why They Matter

### Critical Missing Data

#### 1. Test Step Results
**Failed Endpoints:**
- `/execution/teststepresult/{id}` - 404
- `/execution/teststepresult` - 404
- `/testcase/{testcaseVersionId}/teststep` - 404

**Impact:** Cannot build factTestStep (detailed step-level metrics)  
**Workaround:** May be nested in execution response

#### 2. Defects/Issues
**Failed Endpoint:**
- `/defect/{defectId}` - Timeout

**Impact:** Cannot link executions to defects  
**Workaround:** May need integration with Jira instead

#### 3. Test Case Details
**Failed Endpoints:**
- `/testcase/{testcaseId}` - 404
- `/testcase/detail/{id}` - 404

**Impact:** Cannot get full test case attributes directly  
**Workaround:** Test case details nested in execution response (`tcrTreeTestcase`)

---

## Recommended Dimensional Model Phases

### Phase 1: Core Fact + Essential Dimensions ✅
**Ready to Build:**
- factTestExecution (from `/execution{?cycleid}`)
- dimProject (from `/project/details`)
- dimRelease (from `/release`)
- dimCycle (from `/cycle/release/{releaseid}`)
- dimDate (generated)
- dimExecutionStatus (from LOV or hardcoded)

**Business Questions Answered:**
- How many tests executed per cycle/release/project?
- What is the pass rate by project/release/cycle?
- Who are the top testers by execution count?
- What is average execution time?

### Phase 2: Test Case Dimension ⚠️
**Needs More Investigation:**
- dimTestCase (nested in execution, plus `/testcasetree/*`)
- Test case versioning (SCD Type 2)
- Test case hierarchy (tree structure)

**Business Questions Answered:**
- Which test cases fail most often?
- What is coverage by test case priority?
- Test case reuse across cycles

### Phase 3: Advanced Metrics ⏭️
**Future Enhancements:**
- factTestStep (if accessible)
- dimDefect (if accessible or via Jira bridge)
- Test case-to-requirement traceability
- Custom field dimensions

---

## Data Quality & Incremental Load

### Incremental Fields Available

From execution response:
- `lastModifiedOn` - Unix timestamp (ms)
- `createDatetime` - Unix timestamp (ms)
- `assignmentDate` - Unix timestamp (ms)
- `executionDate` - Derived from execution timestamp

### Incremental Load Strategy

```sql
-- Watermark query
SELECT MAX(LastModifiedDate) 
FROM factTestExecution

-- Incremental extraction
WHERE lastModifiedOn > {watermark_timestamp}
```

### SCD Type 2 for Test Cases

Test cases have versions:
- `versionNumber` - Version identifier
- `revision` - Revision number
- Need to track effective dates for historical accuracy

---

## Business Intelligence Use Cases

### Executive Dashboard
**Data:** Projects, Releases, Executions  
**Metrics:**
- Total test coverage
- Pass rate trend
- Active projects/releases
- Top 10 failing test areas

### Test Manager Dashboard
**Data:** Cycles, Executions, Testers  
**Metrics:**
- Cycle progress (% complete)
- Tester productivity
- Execution bottlenecks
- Time variance (actual vs estimated)

### Quality Dashboard
**Data:** Executions, Test Cases, Status  
**Metrics:**
- Pass/Fail/Blocked breakdown
- Flaky test identification
- Coverage by priority
- Regression analysis

---

## Summary: What We Can Build Right Now

### ✅ Ready for Implementation

**Fact Table:**
- factTestExecution (36,000+ estimated records across 37 projects)

**Dimension Tables:**
- dimProject (37 records)
- dimRelease (77 records)
- dimCycle (estimated 100+ records)
- dimExecutionStatus (5-10 records)
- dimDate (3,650 records for 10 years)

**Power BI Reports:**
- Test Execution Dashboard
- Pass Rate Analysis
- Tester Performance
- Project Health
- Release Quality Metrics

### ⚠️ Needs Investigation

- dimTestCase (partially available, needs schema design)
- dimUser (partially available)
- factTestStep (endpoint not accessible yet)

### ❌ Not Available

- dimDefect (timeout/integration needed)
- Test case-to-requirement mapping (404 errors)
- Custom field dimensions (need to test per project)

---

## Next Steps for Dimensional Model

1. **Validate schema with sample extractions** (1 hour)
   - Extract full execution dataset for one cycle
   - Map all fields to dimensional attributes
   - Identify any missing fields

2. **Design surrogate key strategy** (30 minutes)
   - Define key generation (sequential, hash, UUID?)
   - Plan SCD Type 2 for test cases
   - Design bridge tables if needed

3. **Build Prepare stage schema artifacts** (2 hours)
   - Create DDL for dimension tables
   - Create DDL for fact table
   - Define transformation rules
   - Build sample data load

4. **Power BI data model design** (1 hour)
   - Star schema relationships
   - Calculated columns/measures
   - Role-playing dimensions (dimDate)
   - Report mockups

---

**Document Status:** ✅ COMPLETE  
**Dimensional Model:** ✅ DEFINED  
**Extraction Strategy:** ✅ DOCUMENTED  
**Ready for:** Prepare Stage Schema Design

*Generated: 2025-12-02 17:00 GMT*

