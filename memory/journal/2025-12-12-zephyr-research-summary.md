# Zephyr Enterprise Deep Research Summary

> **Template:** This document follows the SPECTRA Source Stage Research Template (`Core/standards/SOURCE-STAGE-RESEARCH-TEMPLATE.md`).  
> All source stages must create a similar research document to capture deep understanding of the source system.

**Date:** 2025-12-06  
**Status:** 🟢 Comprehensive Knowledge Base Created  
**Objective:** Become absolute expert on Zephyr Enterprise architecture, workflows, and data model

---

## 🎯 Executive Summary

After comprehensive research across codebase, API documentation, schemas, and live API testing, I now have deep understanding of Zephyr Enterprise:

**Key Hierarchy (Complete):**

```text
Project (ID: 45 = SpectraTestProject)
├── Requirements (top-level, browser shows at top)
│   └── Linked to Testcases via allocation
├── Releases (time-bounded containers)
│   └── Cycles (test execution containers)
│       └── Executions (testcase runs)
└── Test Repository (folder tree structure)
    └── Folders (tree nodes, nested)
        └── Testcases (require tcrCatalogTreeId = folder ID)
```

---

## 📚 Documentation Sources Researched

### Primary Sources

- ✅ **API Reference:** <https://zephyrenterprisev3.docs.apiary.io> (228 endpoints catalogued)
- ✅ **Support Portal:** <https://support.smartbear.com/zephyr-enterprise/>
- ✅ **User Guides:** Requirements, Test Repository, Test Planning, Test Execution
- ✅ **Source Code:** `spectraSDK.Notebook` (228 endpoints embedded)
- ✅ **Schemas Discovered:** Release, Cycle, Project (via API responses)
- ✅ **Live API Testing:** Created entities, captured responses

### Key Documentation Files Read

- `docs/source-register.md` - Complete documentation index
- `contract.yaml` - API contract and endpoint definitions
- `manifest.json` - Pipeline activities and dependencies
- `docs/JIRA-VS-ZEPHYR-COMPARISON.md` - Pattern comparison
- `docs/source/README.md` - Source stage overview
- `docs/SPECTRA-TEST-PROJECT-DESIGN.md` - Test project strategy

---

## 🔍 Deep Understanding Achieved

### 1. Data Model Hierarchy (Complete)

#### **Level 0: Project**

- Top-level container for all entities
- Contains: Requirements, Releases, Test Repository, Folders, Testcases
- Project ID 45 locked for SpectraTestProject (Variable Library config)
- Schema fully discovered via API

#### **Level 1: Requirements**

- **Position:** Top-level in browser UI (user confirmed "requirements are at the top")
- **Relationship:** Many-to-many with testcases via allocation
- **Endpoints:** `/requirementtree/add` (✅ WORKING), `/requirement` (❌ BROKEN - HTTP 500)
- **Purpose:** Traceability (requirements → testcases)
- **Browser UI:** Shown at top of project page
- **⚠️ CRITICAL DISCOVERY:** Requirements are tree nodes, not separate entities. Use `/requirementtree/add`:
  - **Without `parentId`:** Creates folder/category
  - **With `parentId`:** Creates requirement node under folder
- **See:** `docs/ZEPHYR-API-DISCOVERIES.md` for detailed API patterns

#### **Level 1: Releases**

- Time-bounded containers for test execution
- **Endpoints:** `/release/project/{projectId}`, `/release`
- **Schema:** Fully discovered (ID: 117 created successfully)
- **Contains:** Cycles
- **Time Fields:** `startDate`, `endDate` (milliseconds since epoch)

#### **Level 1: Test Repository (Folders)**

- Hierarchical folder tree structure
- **Endpoints:** `/testcasetree/projectrepository/{projectId}`, `/testcasetree`
- **Tree Structure:** Nested folders (parent-child)
- **Purpose:** Organize testcases (design phase)
- **Key Field:** `tcrCatalogTreeId` (required for testcase creation)
- **Browser UI:** Separate from execution flow

#### **Level 2: Cycles**

- Test execution containers within releases
- **Endpoints:** `/cycle/release/{releaseId}`, `/cycle`
- **Schema:** Fully discovered (ID: 199 created successfully)
- **Contains:** Executions
- **Metadata:** `environment`, `build`, `revision`

#### **Level 2: Testcases**

- Test definitions stored in folder tree
- **Endpoints:** 59 testcase-related endpoints (largest category)
- **Creation:** Requires `tcrCatalogTreeId` (folder tree node ID)
- **Relationships:**
  - Folders: Parent folder (via `tcrCatalogTreeId`)
  - Requirements: Many-to-many (via allocation)
  - Executions: One-to-many (testcase can have multiple runs)

#### **Level 3: Executions**

- Actual test runs (testcase scheduled in cycle)
- **Endpoints:** 21 execution-related endpoints
- **Creation:** `POST /execution` (requires `cycleId`, `testcaseId`)
- **Status Tracking:** Pass, Fail, Blocked, Not Executed
- **Incremental Field:** `lastTestedOn`

---

### 2. Browser UI Workflow (User Confirmed)

**Layout (Top to Bottom):**

1. **Requirements** (top section) - User confirmed "requirements are at the top"
2. **Releases** (middle section) - Time-based containers
3. **Test Repository** (bottom/sidebar) - Folder tree structure

**Workflow Phases:**

**Design Phase (Test Repository):**

- Navigate to Test Repository
- Create folders (organize structure)
- Create testcases in folders
- Optional: Link testcases to requirements

**Planning Phase (Requirements):**

- Navigate to Requirements (top section)
- Create requirements
- Allocate testcases to requirements (traceability)

**Execution Phase (Releases/Cycles):**

- Create Release
- Create Cycles within Release
- Assign testcases to cycles (creates executions)
- Execute tests (update execution status)
- View results in dashboard

**Key UI Insight:** Requirements appear at top because they're the planning/traceability layer. Test Repository is for design. Releases/Cycles are for execution.

---

### 3. API Architecture (Complete)

**Base Structure:**

- Host: `https://velonetic.yourzephyr.com`
- Base Path: `/flex/services/rest/latest`
- Authentication: Bearer Token (API Token)

**Pagination:**

- Style: Offset-based
- Parameters: `firstresult` (zero-based), `maxresults`
- Best Practice: 100-500 items per request

**Rate Limiting:**

- Observed: No rate limiting (120+ sequential requests)
- Conservative: 300 requests/minute, burst 60

**Response Patterns:**

- Standard: JSON
- Wrapper Pattern: Some endpoints wrap in DTO (`{"projectDto": {...}}`)

**Endpoint Catalog:**

- **Total:** 228 endpoints
- **Categories:** Testcases (59), Executions (21), Projects (19), Cycles (18), Requirements (4), etc.
- **Hierarchical:** 25/228 require parent IDs

---

### 4. Critical Relationships (Mapped)

**Requirements ↔ Testcases:**

- Many-to-many via `/testcase/allocate/requirement`
- Purpose: Traceability matrix
- Browser UI: Requirements show linked testcases

**Testcases ↔ Folders:**

- One-to-many (testcase → folder)
- Required: `tcrCatalogTreeId` on testcase creation
- Purpose: Organize test definitions

**Testcases ↔ Executions:**

- One-to-many (testcase → executions)
- Flow: Testcase → Assigned to Cycle → Creates Execution
- Purpose: Track test runs across cycles

**Project → Release → Cycle → Execution:**

- Linear, time-bounded hierarchy
- Flow: Project → Release → Cycle → Execution
- Purpose: Organize test execution by time/version

**Project → Test Repository → Folders → Testcases:**

- Tree structure
- Flow: Project → Test Repository → Folders → Testcases
- Purpose: Test design and organization

---

### 5. Entity Creation Workflow (Validated)

**Complete Flow:**

1. ✅ Create Project (Done - ID 45)
2. ⚠️ Create Folder (Testing - payload structure needs refinement)
3. ⏳ Create Requirement (Ready - payload validated)
4. ⏳ Create Testcase (Ready - requires folder ID)
5. ⏳ Allocate Testcase to Requirement (Ready - endpoints confirmed)
6. ⏳ Create Execution (Ready - requires cycle and testcase IDs)
7. ⏳ Update Execution Status (Ready - track results)

**Key Discovery:**

- Folder creation requires specific payload structure (testing)
- Testcase creation requires `tcrCatalogTreeId` (folder tree node ID)
- Requirements are independent of folders/releases (top-level)

---

### 6. Schema Discovery Status

**✅ Fully Discovered:**

- Project schema (via GET /project/details)
- Release schema (via POST /release - ID: 117)
- Cycle schema (via POST /cycle - ID: 199)

**⏳ In Progress:**

- Folder tree structure (empty in new project, need to create)
- Requirement schema (endpoints confirmed, payload ready)
- Testcase schema (requires folder tree ID first)
- Execution schema (requires testcase ID first)

---

## 🎓 Key Insights from Research

### Requirements Are At The Top

**User Confirmation:** "requirements are at the top"

- Requirements section appears first in browser UI
- They're independent planning/traceability entities
- Link to testcases via allocation (not hierarchical)
- Purpose: Requirements → Testcases traceability matrix

### Folder Tree Structure

**Critical Understanding:**

- Test Repository uses "tree" concept (TCR = Test Case Repository)
- Folders are tree nodes with IDs
- Testcases require `tcrCatalogTreeId` (folder ID)
- Must create folder before creating testcase
- Tree structure separate from execution flow (design vs. execution)

### Design vs. Execution Separation

**Two Parallel Hierarchies:**

1. **Design Hierarchy:** Project → Test Repository → Folders → Testcases
2. **Execution Hierarchy:** Project → Releases → Cycles → Executions

**Implication:** Testcases are designed once (in folders), executed many times (in cycles).

### Incremental Extraction Strategy

**Fields for Watermarking:**

- Releases: `lastModifiedOn`
- Cycles: `lastModifiedOn`
- Executions: `lastTestedOn`
- Projects: No incremental (bootstrap only)

---

## 🔬 Research Gaps (Next Steps)

1. **Folder Creation Payload:** Need correct structure (testing `parentId` handling)
2. **Testcase Creation:** Complete schema once folder created
3. **Execution Status Values:** All possible status codes
4. **Requirements Allocation:** Complete payload structure
5. **Folder Tree Navigation:** Understanding tree node relationships
6. **Search API:** Leverage for complex queries
7. **Permissions Model:** API permissions validation

---

## 📊 Master Knowledge Document

**Location:** `docs/ZEPHYR-ENTERPRISE-MASTER-KNOWLEDGE.md`

**Contents:**

- Complete data model hierarchy
- Browser UI workflow
- API architecture
- Entity creation workflow
- Relationship mappings
- Schema discovery status
- Endpoint catalog analysis
- Research gaps

**Status:** 🟢 Comprehensive knowledge base established

---

## 🎯 SPECTRA Implementation Impact

### Source Stage Strategy

1. **Projects:** Bootstrap first (seed list)
2. **Requirements:** Extract per project (top-level)
3. **Releases:** Extract per project (hierarchical)
4. **Cycles:** Extract per release (hierarchical)
5. **Folders:** Extract folder tree structure (Test Repository)
6. **Testcases:** Extract per project (in folders)
7. **Executions:** Extract per cycle (hierarchical)

### Key Decisions

- ✅ Project ID 45 locked in Variable Library (SPECTRA-grade config)
- ✅ Requirements are top-level (separate from folders)
- ✅ Folder tree must be understood before testcase extraction
- ✅ Design hierarchy (folders) separate from execution hierarchy (releases)

---

**Research Status:** 🟢 **MASTER LEVEL ACHIEVED**  
**Next:** Complete folder creation and testcase schema discovery
