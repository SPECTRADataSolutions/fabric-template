# Zephyr Enterprise Master Knowledge Base

**Status:** 🟢 Active Research  
**Last Updated:** 2025-12-06  
**Purpose:** Comprehensive understanding of Zephyr Enterprise architecture, data model, API, and workflows

---

## 🎯 Executive Summary

Zephyr Enterprise is a test management platform with a hierarchical data model centered around projects, releases, cycles, and executions. Understanding the complete architecture enables SPECTRA to build accurate, comprehensive data pipelines.

**Key Hierarchy:**
```
Project (ID: 45 for SpectraTestProject)
  ├── Requirements (top-level in browser, linked to testcases via allocation)
  ├── Releases (time-bounded containers)
  │   └── Cycles (test execution containers)
  │       └── Executions (testcase runs in cycles)
  └── Test Repository (folder tree structure)
      └── Folders (tree nodes, nested structure)
          └── Testcases (test definitions, require tcrCatalogTreeId = folder ID)
```

**Critical Understanding:**
- **Requirements** = Top-level entities (shown at top of browser UI)
- **Test Repository** = Folder tree + testcases (design phase)
- **Releases/Cycles** = Time-based execution containers (execution phase)
- **Executions** = Actual test runs (testcase scheduled in cycle)
- **Folder Tree** = Required for testcase creation (must create folder first)
- **tcrCatalogTreeId** = Folder tree node ID (mandatory for testcase POST)

---

## 📐 Data Model Hierarchy

### Level 0: Project (Top Container)
- **Endpoint:** `/project/details`, `/project/normal`, `/project/lite`
- **Primary Key:** `id` (integer)
- **Characteristics:**
  - Projects are the top-level organizational unit
  - Each project contains: releases, cycles, testcases, requirements, folders
  - Projects have members, groups, isolation levels
  - Can be global or project-specific
  - Status field: `"2"` = active
  - `hasChild`: indicates child entities exist
  - `members`: array (usually empty, managed via UI/API separately)
  
**Schema (from discovery):**
```json
{
  "id": 45,
  "version": 0,
  "name": "SpectraTestProject",
  "description": "...",
  "startDate": 1764979914622,
  "projectStartDate": "12/06/2025",
  "status": "2",
  "members": [],
  "projectGroups": [],
  "sharedProjects": [],
  "isolationLevel": 0,
  "dashboardSecured": false,
  "dashboardRestricted": false,
  "createdOn": 1764979915893,
  "shared": false,
  "active": true,
  "customProperties": {},
  "globalProject": false,
  "allowedGlobalProject": false,
  "autoUpdateTestStatus": false,
  "webhookId": 0,
  "allowedInternalRequirements": false
}
```

### Level 1: Requirements (Linked to Testcases)
- **Endpoints:**
  - `GET /requirement/project/{projectId}` - Get requirements for project
  - `POST /requirement` - Create requirement
  - `PUT /requirement` - Update requirement
  - `GET /requirement/{requirementId}` - Get requirement by ID
- **Primary Key:** `id` (integer)
- **Relationship:** Requirements link to testcases (many-to-many)
- **Characteristics:**
  - Requirements exist at project level
  - Testcases can be allocated to requirements
  - Requirements are top-level entities (not under releases/cycles)
  - Browser UI: Requirements shown at top level

**Key Endpoints:**
- `/testcase/allocate/requirement` - Allocate testcase to requirement
- `/testcase/allocate/requirement` (bulk) - Bulk allocate

### Level 1: Releases (Time-Bounded Containers)
- **Endpoints:**
  - `GET /release` - All releases (across projects)
  - `GET /release/project/{projectId}` - Releases for specific project
  - `POST /release` - Create release
  - `PUT /release` - Update release
- **Primary Key:** `id` (integer)
- **Parent:** Project (`projectId`)
- **Characteristics:**
  - Releases contain cycles
  - Time-bounded: `startDate`, `endDate` (milliseconds since epoch)
  - `status`: 0 = active
  - `globalRelease`: can span projects
  - `projectRelease`: project-specific
  - `hasChild`: indicates cycles exist
  - Incremental field: `lastModifiedOn`

**Schema (from discovery):**
```json
{
  "id": 117,
  "name": "Schema Discovery Release",
  "description": "...",
  "startDate": 1764982074307,
  "releaseStartDate": "12/06/2025",
  "endDate": 1772758074307,
  "releaseEndDate": "03/06/2026",
  "createdDate": 1764982075624,
  "status": 0,
  "projectId": 45,
  "orderId": 5,
  "globalRelease": false,
  "projectRelease": false,
  "hasChild": false,
  "syncEnabled": false
}
```

### Level 1: Test Repository (Folders + Testcases)
- **Structure:** Hierarchical folder tree containing testcases
- **Tree API:** Test Repository uses "tree" concept (TCR = Test Case Repository)
- **Key Endpoints:**
  - `GET /testcasetree/projectrepository/{projectId}` - Get entire Test Repository tree for project
  - `GET /testcasetree/hierarchy` - Get TCR hierarchy
  - `GET /testcasetree` - Get Testcase Tree (with filters)
  - `POST /testcasetree` - Create Tree node (folder)
  - `DELETE /testcasetree` - Delete Testcase Tree node
  - `POST /testcasetree/copy` - Copy tree node to another location
- **Folders (Tree Nodes):**
  - Nested structure (parent-child relationships)
  - Represented as tree nodes with IDs
  - `tcrCatalogTreeId`: Required field when creating testcases (identifies folder location)
  - Tree ID represents the folder path in the hierarchy
- **Testcases:**
  - Stored in folder hierarchy (tree structure)
  - Require `tcrCatalogTreeId` on creation (must specify folder location)
  - Can be linked to requirements
  - Can be assigned to releases/cycles for execution
  - Primary entity for test definition
  - Tree operations: `/testcase/tree` - Get testcases by tree IDs

### Level 2: Cycles (Test Execution Containers)
- **Endpoints:**
  - `GET /cycle/release/{releaseId}` - Cycles for release
  - `POST /cycle` - Create cycle
  - `PUT /cycle` - Update cycle
- **Primary Key:** `id` (integer)
- **Parent:** Release (`releaseId`)
- **Characteristics:**
  - Cycles contain executions (testcase runs)
  - Can have phases (`cyclePhases`)
  - Environment/build metadata: `environment`, `build`
  - Time-bounded: `startDate`, `endDate`
  - `status`: 0 = active
  - `revision`: incremental version number
  - `hasChild`: indicates executions exist
  - Incremental field: `lastModifiedOn`

**Schema (from discovery):**
```json
{
  "id": 199,
  "environment": "Discovery",
  "build": "1.0",
  "name": "Schema Discovery Cycle",
  "startDate": 1764982074307,
  "endDate": 1772758074307,
  "cycleStartDate": "12/06/2025",
  "cycleEndDate": "03/06/2026",
  "status": 0,
  "revision": 278,
  "releaseId": 117,
  "cyclePhases": [],
  "createdOn": 1764982076999,
  "hasChild": false
}
```

### Level 2: Testcases (Test Definitions)
- **Endpoints:** 59 testcase-related endpoints (largest category)
- **Key Endpoints:**
  - `GET /testcase/project/{projectId}` - Testcases for project
  - `POST /testcase` - Create testcase
  - `PUT /testcase` - Update testcase
  - `GET /testcase/{testcaseId}` - Get testcase by ID
- **Primary Key:** `id` (integer)
- **Parent:** Project (via folders) or Release
- **Characteristics:**
  - Testcases are defined in Test Repository (folder structure)
  - Can be allocated to requirements
  - Can be assigned to cycles for execution
  - `tcrCatalogTreeId`: Required for creation (folder location)
  - Bulk operations supported
  - Can be cloned, versioned
  - Search functionality extensive

**Key Relationships:**
- **Requirements:** Many-to-many via allocation
- **Folders:** Parent folder in Test Repository tree
- **Executions:** One-to-many (testcase can have multiple execution runs)

### Level 3: Executions (Testcase Runs)
- **Endpoints:** 21 execution-related endpoints
- **Key Endpoints:**
  - `GET /execution/cycle/{cycleId}` - Executions for cycle
  - `POST /execution` - Create execution (schedule testcase)
  - `PUT /execution` - Update execution status
  - `GET /execution/{executionId}` - Get execution by ID
- **Primary Key:** `id` (integer)
- **Parent:** Cycle (`cycleId`)
- **Testcase Link:** Execution references testcase
- **Characteristics:**
  - Execution = scheduled testcase run in a cycle
  - Status tracking: Pass, Fail, Blocked, Not Executed
  - Assignment: can assign tester
  - Bulk execution support
  - Change history tracked
  - Incremental field: `lastTestedOn`

---

## 🔄 Browser UI Workflow

### Top-Level Navigation
1. **Project Selection** → Shows all accessible projects
2. **Project Dashboard** → Overview of project status

### Project Structure in Browser
```
Project: SpectraTestProject
├── Requirements (top section)
│   └── List of requirements
│       └── Linked testcases shown
├── Releases (time-based containers)
│   └── Release: "v1.0"
│       └── Cycles
│           └── Cycle: "Smoke Tests"
│               └── Executions (testcase runs)
└── Test Repository (folder tree)
    └── Folders (nested structure)
        └── Testcases (test definitions)
```

### Key UI Patterns
1. **Requirements First:** Requirements shown at top (user says "requirements are at the top")
2. **Folders for Organization:** Testcases organized in folder hierarchy
3. **Release → Cycle → Execution:** Linear flow for test execution
4. **Test Repository:** Separate from execution flow (design vs. execution)

---

## 🔌 API Architecture

### Base URL Structure
- **Host:** `https://velonetic.yourzephyr.com`
- **Base Path:** `/flex/services/rest/latest`
- **Full URL:** `{host}{base_path}`

### Authentication
- **Method:** Bearer Token (API Token)
- **Header:** `Authorization: Bearer {api_token}`
- **Token Generation:** Via Zephyr UI (Admin → API Tokens)

### Pagination
- **Style:** Offset-based
- **Parameters:**
  - `firstresult`: Zero-based starting point (0 = first record)
  - `maxresults`: Maximum items per request (default varies)
- **Best Practice:** 100-500 items per request

### Rate Limiting
- **Observed:** No rate limiting detected (120+ sequential requests)
- **Conservative Limits:**
  - Burst: 60 requests
  - Sustained: 300 requests/minute

### Response Formats
- **Standard:** JSON
- **Wrapper Pattern:** Some endpoints wrap response in DTO object
  - Example: `{"projectDto": {...}}`
  - Example: `{"releaseDto": {...}}`

---

## 📊 Endpoint Catalog (228 Total)

### By Category
| Category | Count | Key Endpoints |
|----------|-------|---------------|
| **Testcases** | 59 | Create, update, search, allocate, clone |
| **Executions** | 21 | Schedule, execute, bulk operations |
| **Projects** | 19 | CRUD, details, user assignments |
| **Cycles** | 18 | Create, update, clone, phase management |
| **Admin** | 11 | Preferences, applications, backup |
| **Users** | 15 | User management, assignments |
| **Requirements** | 4 | CRUD, allocation to testcases |
| **Releases** | 5 | CRUD, project-specific |
| **Other** | 76 | Attachments, automation, search, etc. |

### Hierarchical Endpoints (25/228)
Endpoints requiring parent IDs:
- `/release/project/{projectId}` - Releases for project
- `/cycle/release/{releaseId}` - Cycles for release
- `/execution/cycle/{cycleId}` - Executions for cycle
- `/testcase/project/{projectId}` - Testcases for project
- `/requirement/project/{projectId}` - Requirements for project

### CRUD Patterns
Most entities follow standard REST patterns:
- `GET /{entity}` - List all
- `GET /{entity}/{id}` - Get by ID
- `GET /{entity}/parent/{parentId}` - Get by parent
- `POST /{entity}` - Create
- `PUT /{entity}` - Update
- `DELETE /{entity}` - Delete

---

## 🗂️ Test Repository Structure

### Folders
- **Hierarchical:** Parent-child relationships
- **Tree Structure:** Nested folders
- **Purpose:** Organize testcases
- **Navigation:** Folder tree in browser UI

### Testcases in Folders
- **Location:** Defined by `tcrCatalogTreeId` (folder tree ID)
- **Relationship:** Testcase → Folder (required for creation)
- **Search:** Can search testcases by folder
- **Bulk Operations:** Can operate on folder contents

### Folder vs. Release Assignment
- **Folder:** Where testcase is defined (design phase)
- **Release/Cycle:** Where testcase is executed (execution phase)
- **Separation:** Design (folder) vs. Execution (release/cycle)

---

## 🔗 Key Relationships

### Requirements ↔ Testcases
- **Relationship:** Many-to-many
- **Endpoint:** `/testcase/allocate/requirement`
- **Purpose:** Link testcases to requirements (traceability)
- **Browser UI:** Requirements show linked testcases

### Testcases ↔ Executions
- **Relationship:** One-to-many
- **Flow:** Testcase → Assigned to Cycle → Creates Execution
- **Purpose:** Track testcase runs across cycles

### Project → Release → Cycle → Execution
- **Hierarchy:** Linear, time-bounded
- **Flow:** 
  1. Project contains Releases
  2. Release contains Cycles
  3. Cycle contains Executions
  4. Execution references Testcase

### Project → Test Repository → Folders → Testcases
- **Hierarchy:** Tree structure
- **Flow:**
  1. Project contains Test Repository
  2. Test Repository has Folders (tree)
  3. Folders contain Testcases

---

## 📝 Entity Lifecycle

### Project Creation Flow
1. `POST /project` → Create project
2. Add members (via UI or PUT /project)
3. Create Requirements (if needed)
4. Create Releases
5. Populate Test Repository (folders + testcases)

### Release Setup Flow
1. `POST /release` → Create release (requires projectId)
2. `POST /cycle` → Create cycles (requires releaseId)
3. Assign testcases to cycles (creates executions)

### Testcase Creation Flow
1. Navigate to Test Repository folder
2. `POST /testcase` → Create testcase (requires projectId, tcrCatalogTreeId)
3. Optional: Allocate to requirement
4. Optional: Assign to release/cycle

### Execution Flow
1. Testcase assigned to Cycle → Creates Execution
2. `POST /execution` → Manual schedule (or automatic)
3. Execution status updated: Pass/Fail/Blocked
4. `PUT /execution` → Update execution result

---

## 🔍 API Discovery Findings

### Successful Endpoint Patterns
- ✅ Projects: `/project/details` (full metadata)
- ✅ Releases: `/release/project/{projectId}` (hierarchical)
- ✅ Cycles: `/cycle/release/{releaseId}` (hierarchical)
- ✅ Executions: `/execution/cycle/{cycleId}` (hierarchical)

### Challenges Discovered
- ⚠️ Testcase Creation: Requires `tcrCatalogTreeId` (folder tree ID)
- ⚠️ Project Membership: Members array usually empty (managed separately)
- ⚠️ Requirements: Need to discover allocation endpoints

### Schema Discovery Success
- ✅ Release schema captured (via POST /release)
- ✅ Cycle schema captured (via POST /cycle)
- ⚠️ Testcase schema: Need folder tree ID to create

---

## 🎯 SPECTRA Implementation Implications

### Source Stage
1. **Projects:** Bootstrap first (seed list)
2. **Releases:** Extract per project (hierarchical)
3. **Cycles:** Extract per release (hierarchical)
4. **Executions:** Extract per cycle (hierarchical)
5. **Testcases:** Extract per project (Test Repository)
6. **Requirements:** Extract per project (top-level)
7. **Folders:** Extract folder tree structure

### Key Considerations
- **Hierarchical Access:** Must follow parent → child order
- **Incremental Fields:** Use `lastModifiedOn`, `lastTestedOn`
- **Bulk Operations:** Leverage for efficiency
- **Folder Tree:** Understand structure before testcase creation
- **Requirements:** Separate from execution flow

### Test Project Strategy
- **Locked Project ID:** 45 (SpectraTestProject)
- **Location:** Variable Library (`TEST_PROJECT_ID`)
- **Purpose:** Deterministic test fixture
- **Contains:** Perfect structure for validation

---

## 📚 Documentation Sources

### Primary
- **API Reference:** https://zephyrenterprisev3.docs.apiary.io
- **Support Portal:** https://support.smartbear.com/zephyr-enterprise/
- **User Guide:** https://support.smartbear.com/zephyr-enterprise/docs/en/zephyr-user-guide.html

### Key Guides
- Requirements: https://support.smartbear.com/zephyr-enterprise/docs/en/requirements.html
- Test Repository: https://support.smartbear.com/zephyr-enterprise/docs/en/test-repository.html
- Test Planning: https://support.smartbear.com/zephyr-enterprise/docs/en/test-planning.html
- Test Execution: https://support.smartbear.com/zephyr-enterprise/docs/en/test-execution.html

---

## 🔬 Next Research Areas

1. **Folder Tree Creation:** Create folder structure to understand tree node creation
2. **Requirements Allocation:** Complete flow from requirements to testcases
3. **Execution Statuses:** All possible status values and transitions
4. **Bulk Operations:** Optimize for large-scale data extraction
5. **Search API:** Leverage search endpoints for complex queries
6. **Permissions Model:** Understand project access and API permissions
7. **Testcase Creation with Tree:** Create folder, then testcase, to get complete schema

---

## 🏗️ Complete Entity Creation Workflow

### Step-by-Step: Creating a Complete Test Structure

**1. Create Project** ✅ (Done - Project 45)
```python
POST /project
{
  "name": "SpectraTestProject",
  "description": "...",
  "startDate": timestamp,
  "active": True,
  "status": "2"
}
```

**2. Create Folder in Test Repository** (Required for testcases)
```python
POST /testcasetree
{
  "name": "Folder Name",
  "projectId": 45,
  "parentId": null  # Root folder, or parent folder ID
}
# Returns: { "id": treeNodeId, ... }
```

**3. Create Requirement** (Top-level, shown at top of browser)
```python
POST /requirement
{
  "name": "Requirement Name",
  "projectId": 45,
  "description": "..."
}
# Returns: { "id": requirementId, ... }
```

**4. Create Release** ✅ (Done - ID 117)
```python
POST /release
{
  "name": "Release Name",
  "projectId": 45,
  "startDate": timestamp,
  "endDate": timestamp,
  "status": 0
}
# Returns: { "id": releaseId, ... }
```

**5. Create Cycle** ✅ (Done - ID 199)
```python
POST /cycle
{
  "name": "Cycle Name",
  "releaseId": 117,
  "startDate": timestamp,
  "endDate": timestamp,
  "status": 0,
  "environment": "Test",
  "build": "1.0"
}
# Returns: { "id": cycleId, ... }
```

**6. Create Testcase** (Requires folder tree ID)
```python
POST /testcase
{
  "testcase": {
    "name": "Testcase Name",
    "projectId": 45,
    "tcrCatalogTreeId": treeNodeId,  # REQUIRED - from step 2
    "description": "..."
  }
}
# Returns: { "id": testcaseId, ... }
```

**7. Allocate Testcase to Requirement** (Link testcase to requirement)
```python
POST /testcase/allocate/requirement
{
  "testcaseId": testcaseId,
  "requirementId": requirementId
}
```

**8. Create Execution** (Schedule testcase in cycle)
```python
POST /execution
{
  "cycleId": 199,
  "testcaseId": testcaseId,
  "status": 0  # Not Executed
}
# Returns: { "id": executionId, ... }
```

**9. Update Execution Status** (Record test result)
```python
PUT /execution
{
  "id": executionId,
  "status": 1,  # Pass, Fail, Blocked, etc.
  "executedBy": userId,
  "executedOn": timestamp
}
```

---

## 🌐 Browser UI Structure & Flow

### Project View Layout (Top to Bottom)

**1. Requirements Section** (Top of page)
- Shows all requirements for the project
- Each requirement shows linked testcases
- Requirements are independent of releases/cycles
- Purpose: Traceability (requirements → testcases)

**2. Releases Section** (Middle)
- List of all releases
- Time-bounded containers
- Expand to show cycles
- Purpose: Organize test execution by time/version

**3. Test Repository Section** (Bottom/Sidebar)
- Folder tree structure
- Contains testcase definitions
- Separate from execution flow
- Purpose: Test design and organization

### Workflow in Browser UI

**Design Phase (Test Repository):**
1. Navigate to Test Repository
2. Create folders (organize structure)
3. Create testcases in folders
4. (Optional) Link testcases to requirements

**Planning Phase (Requirements):**
1. Navigate to Requirements section (top)
2. Create requirements
3. Allocate testcases to requirements (traceability)

**Execution Phase (Releases/Cycles):**
1. Create Release
2. Create Cycles within Release
3. Assign testcases to cycles (creates executions)
4. Execute tests (update execution status)
5. View results in dashboard

### Key UI Insights
- **Requirements are at the top** - First thing users see
- **Folders organize testcases** - Tree structure for design
- **Releases/Cycles organize execution** - Time-based containers
- **Separation of concerns:** Design (folders) vs. Execution (releases)

---

**Status:** 🟡 In Progress  
**Last Updated:** 2025-12-06  
**Next:** Complete folder creation workflow and testcase schema discovery

