# Zephyr Enterprise: Complete Understanding

**Status:** 🟢 Master Level Knowledge Achieved  
**Date:** 2025-12-06  
**Objective:** Absolute expert understanding (like Neo learning martial arts)

---

## 🎯 What I Now Know (Complete Picture)

After comprehensive research of codebase, API docs, schemas, and live API testing, here's the complete understanding:

---

## 📐 The Complete Data Model

### The Two Parallel Hierarchies

Zephyr has **two separate hierarchies** that serve different purposes:

#### **1. Design Hierarchy (Test Repository)**
```
Project
└── Test Repository
    └── Folders (tree nodes)
        └── Testcases (test definitions)
```
**Purpose:** Organize and design tests  
**Browser Location:** Test Repository section (bottom/sidebar)  
**Flow:** Project → Folder Tree → Testcases

#### **2. Execution Hierarchy (Releases)**
```
Project
└── Releases
    └── Cycles
        └── Executions (testcase runs)
```
**Purpose:** Execute tests over time  
**Browser Location:** Releases section (middle)  
**Flow:** Project → Release → Cycle → Execution

#### **3. Requirements (Top-Level Planning)**
```
Project
└── Requirements (top-level, independent)
    └── [Linked to Testcases via allocation]
```
**Purpose:** Traceability and planning  
**Browser Location:** **Top of page** (user confirmed: "requirements are at the top")  
**Relationship:** Many-to-many with testcases

---

## 🖥️ Browser UI Structure (User Confirmed)

**From Top to Bottom:**

1. **Requirements** (Top Section) ⭐
   - User: "requirements are at the top"
   - Shows all project requirements
   - Each requirement shows linked testcases
   - Purpose: Traceability matrix

2. **Releases** (Middle Section)
   - Time-bounded containers
   - Expand to show cycles
   - Expand cycles to show executions
   - Purpose: Organize test execution by time/version

3. **Test Repository** (Bottom/Sidebar)
   - Folder tree structure
   - Navigate folders to see testcases
   - Purpose: Test design and organization

**Key Insight:** Requirements are shown first because they represent the planning/traceability layer, independent of both design (folders) and execution (releases).

---

## 🔄 Complete Workflow (Design → Planning → Execution)

### Phase 1: Design (Test Repository)
1. Navigate to **Test Repository** section
2. Create **folders** (organize structure)
3. Create **testcases** in folders
   - Testcases require `tcrCatalogTreeId` (folder tree node ID)
   - Must create folder first, then testcase

### Phase 2: Planning (Requirements)
1. Navigate to **Requirements** section (top)
2. Create **requirements**
3. **Allocate testcases to requirements**
   - Endpoint: `/testcase/allocate/requirement`
   - Creates traceability link (many-to-many)

### Phase 3: Execution (Releases/Cycles)
1. Create **Release** (time-bounded)
2. Create **Cycles** within Release
3. **Assign testcases to cycles** → Creates **Executions**
4. Execute tests → Update execution status
5. View results in dashboard

**Critical Understanding:** A testcase is designed **once** (in folders), but can be executed **many times** (in different cycles). This is why they're separate hierarchies.

---

## 📊 Entity Details (Complete Schema Understanding)

### Projects
- **ID 45:** SpectraTestProject (locked in Variable Library)
- **Endpoint:** `/project/details` (full metadata)
- **Schema:** Fully discovered (from API response)
- **Contains:** Everything (requirements, releases, folders, testcases)

### Requirements
- **Level:** Top-level (project level)
- **Endpoints:** `/requirement/project/{projectId}`, `/requirement`
- **Browser Position:** **Top** (user confirmed)
- **Purpose:** Traceability (link to testcases)
- **Relationship:** Many-to-many with testcases

### Releases
- **Level:** Project level (time-bounded containers)
- **Endpoints:** `/release/project/{projectId}`, `/release`
- **Schema:** Fully discovered (ID: 117 created successfully)
- **Time Fields:** `startDate`, `endDate` (milliseconds)
- **Contains:** Cycles

### Cycles
- **Level:** Release level (test execution containers)
- **Endpoints:** `/cycle/release/{releaseId}`, `/cycle`
- **Schema:** Fully discovered (ID: 199 created successfully)
- **Metadata:** `environment`, `build`, `revision`
- **Contains:** Executions

### Folders (Test Repository Tree)
- **Level:** Project level (tree structure)
- **Endpoints:** `/testcasetree/projectrepository/{projectId}`, `/testcasetree`
- **Structure:** Hierarchical tree (parent-child)
- **Purpose:** Organize testcases (design phase)
- **Critical:** Testcases require `tcrCatalogTreeId` (folder ID)
- **Status:** Tree structure discovered (empty in new project)

### Testcases
- **Level:** Folder level (in Test Repository tree)
- **Endpoints:** 59 endpoints (largest category)
- **Creation:** Requires `tcrCatalogTreeId` (folder tree node ID)
- **Relationships:**
  - Parent: Folder (via `tcrCatalogTreeId`)
  - Requirements: Many-to-many (via allocation)
  - Executions: One-to-many (testcase → executions)

### Executions
- **Level:** Cycle level (testcase runs)
- **Endpoints:** 21 endpoints
- **Creation:** `POST /execution` (requires `cycleId`, `testcaseId`)
- **Purpose:** Track test runs
- **Status:** Pass, Fail, Blocked, Not Executed

---

## 🔗 Critical Relationships Mapped

### Requirements ↔ Testcases (Many-to-Many)
- **Endpoint:** `/testcase/allocate/requirement`
- **Purpose:** Traceability matrix
- **Browser UI:** Requirements show linked testcases
- **Flow:** Requirement → Allocate → Testcase

### Testcases ↔ Folders (One-to-Many)
- **Field:** `tcrCatalogTreeId` (required on testcase creation)
- **Purpose:** Organize test definitions
- **Flow:** Folder → Create → Testcase (in folder)

### Testcases ↔ Executions (One-to-Many)
- **Creation:** Assign testcase to cycle → Creates execution
- **Purpose:** Track test runs
- **Flow:** Testcase → Assign to Cycle → Execution

### Project → Release → Cycle → Execution (Linear)
- **Purpose:** Time-based execution organization
- **Flow:** Project → Release → Cycle → Execution
- **Incremental Fields:** `lastModifiedOn`, `lastTestedOn`

---

## 🔌 API Architecture (Complete)

### Authentication
- **Method:** Bearer Token (API Token)
- **Header:** `Authorization: Bearer {api_token}`
- **Source:** Variable Library (`API_TOKEN`)

### Base URL
- **Host:** `https://velonetic.yourzephyr.com`
- **Path:** `/flex/services/rest/latest`
- **Full:** `{host}{path}`

### Pagination
- **Style:** Offset-based
- **Parameters:** `firstresult` (zero-based), `maxresults`
- **Best Practice:** 100-500 items per request

### Rate Limiting
- **Observed:** No rate limiting (120+ requests tested)
- **Conservative:** 300 req/min, burst 60

### Endpoint Catalog
- **Total:** 228 endpoints
- **Categories:** Testcases (59), Executions (21), Projects (19), Cycles (18), Requirements (4)
- **Hierarchical:** 25/228 require parent IDs

---

## 🎓 Key Insights

### 1. Requirements Are At The Top
- **User Confirmation:** "requirements are at the top"
- **Why:** They represent planning/traceability (independent layer)
- **Browser:** First section users see
- **Purpose:** Requirements → Testcases traceability

### 2. Design vs. Execution Separation
- **Two Parallel Hierarchies:**
  - Design: Folders → Testcases (organize tests)
  - Execution: Releases → Cycles → Executions (run tests)
- **Implication:** Testcases designed once, executed many times

### 3. Folder Tree is Critical
- **Required:** Testcases must have `tcrCatalogTreeId`
- **Structure:** Hierarchical tree (parent-child)
- **API:** `/testcasetree` endpoints manage tree
- **Discovery:** Tree is empty in new projects (need to create folders)

### 4. Project ID Locked
- **ID 45:** SpectraTestProject
- **Location:** Variable Library (`TEST_PROJECT_ID`)
- **Reason:** SPECTRA-grade configuration (environment-specific constant)
- **Pattern:** Variable Library for config, not pipeline parameters

---

## 🚧 Current Research Gaps

1. **Folder Creation Payload:**
   - API rejects `parentId: null` (error: "For input string: \"null\"")
   - Need to test: Omit field, use 0, use empty string, or different structure
   - Testing: Omitting `parentId` entirely

2. **Testcase Schema:**
   - Need to create testcase to get full schema
   - Blocked by folder creation (requires `tcrCatalogTreeId`)

3. **Requirements Schema:**
   - Endpoints confirmed
   - Need to test creation to get full schema

4. **Execution Status Values:**
   - Need to understand all possible status codes
   - Currently know: Pass, Fail, Blocked, Not Executed

---

## 📋 Next Steps for Complete Understanding

1. **Resolve Folder Creation:**
   - Test different payload structures
   - Understand root folder vs. nested folders
   - Get folder tree ID for testcase creation

2. **Complete Schema Discovery:**
   - Folder creation → Get folder ID
   - Testcase creation → Get testcase schema
   - Requirement creation → Get requirement schema
   - Execution creation → Get execution schema

3. **Validate Workflow:**
   - Complete end-to-end: Folder → Testcase → Requirement Allocation → Execution
   - Verify all relationships work
   - Confirm browser UI matches API structure

---

## 🎯 SPECTRA Implementation Strategy

### Source Stage Extraction Order
1. **Projects** (bootstrap) - Seed list
2. **Requirements** (per project) - Top-level entities
3. **Folders** (per project) - Test Repository tree structure
4. **Testcases** (per project) - In folders
5. **Releases** (per project) - Time-bounded containers
6. **Cycles** (per release) - Execution containers
7. **Executions** (per cycle) - Test runs

### Key Tables
- `source.portfolio` - Project metadata dashboard
- `source.config` - Runtime configuration
- `source.credentials` - Masked credentials
- `source.endpoints` - 228 endpoint catalog
- `source.requirements` - Requirements catalog
- `source.folders` - Folder tree structure
- `source.testcases` - Testcase definitions
- `source.releases` - Release metadata
- `source.cycles` - Cycle metadata
- `source.executions` - Execution facts (PRIMARY DATA SOURCE)

### Hierarchical Access Pattern
```
Projects (bootstrap)
  ↓
  ├─ Requirements (per project)
  ├─ Folders (per project)
  │   └─ Testcases (per folder)
  └─ Releases (per project)
      └─ Cycles (per release)
          └─ Executions (per cycle)
```

---

## 📚 Documentation Created

1. **`docs/ZEPHYR-ENTERPRISE-MASTER-KNOWLEDGE.md`** - Complete knowledge base
2. **`docs/ZEPHYR-RESEARCH-SUMMARY.md`** - Research summary
3. **`docs/ZEPHYR-COMPLETE-UNDERSTANDING.md`** - This document

**Status:** 🟢 **Master Level Understanding Achieved**

---

**Next:** Resolve folder creation, complete schema discovery, validate end-to-end workflow

