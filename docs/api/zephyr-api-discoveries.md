# Zephyr API Discoveries - Live Findings

> **Purpose:** Document critical API patterns, gotchas, and discoveries made during test data creation and schema discovery.  
> **Status:** 🟡 Active Discovery - Updated as we learn  
> **Last Updated:** 2025-12-08  
> **Related:** See [`AUTONOMY-BLOCKERS-AND-LIMITATIONS.md`](AUTONOMY-BLOCKERS-AND-LIMITATIONS.md) for comprehensive autonomy blockers

---

## 📚 Related Documentation

- **Autonomy Blockers:** `AUTONOMY-BLOCKERS-AND-LIMITATIONS.md` - Comprehensive list of all blockers to full automation

---

## 📋 Requirements API

### Key Discovery: `/requirementtree/*` Creates Folders, Not Requirements

**Critical Finding:** 
- **`/requirementtree/add`** creates **folders/tree nodes**, NOT actual requirements
- **`/requirement`** endpoint exists but is **BROKEN** (HTTP 500: "id is null")
- **Actual requirements** may not be creatable via API, or require a different workflow

**What We've Created So Far:**
- Folder ID 698: "REQ-001: Core Reactor Stabilit..." (top-level folder)
- Folder ID 699: "REQ-001: Core Reactor Stability" (subfolder under 698)

**Both are folders, not requirements!**

### Endpoints

#### `/requirementtree/add` (POST)
**Purpose:** Create requirement **folders/tree nodes** (NOT actual requirements).

**Payload Structure:**
```json
{
  "name": "Folder Name",
  "description": "Folder description",
  "projectId": 45
}
```

**Behavior:**
- **Without `parentId`:** Creates a top-level folder
- **With `parentId`:** Creates a subfolder under the parent

**⚠️ CRITICAL:** This endpoint **ONLY creates folders**, not requirements!

**Example - Create Folder:**
```json
{
  "name": "REQ-001: Core Reactor Stability",
  "description": "Folder for core reactor requirements",
  "projectId": 45
}
```
**Result:** Creates **folder** ID 698 (appears in tree, can contain children)

**Example - Create Subfolder:**
```json
{
  "name": "REQ-001: Core Reactor Stability",
  "description": "Subfolder",
  "projectId": 45,
  "parentId": 698
}
```
**Result:** Creates **subfolder** ID 699 (appears under folder 698 in tree)

**⚠️ Gotcha:** This endpoint creates folders, not requirements. We have NOT found the endpoint for creating actual requirements yet.

#### `/requirement` (POST) or `/requirement/` (POST)
**Status:** ❌ **BROKEN - DOES NOT WORK** (despite being documented)

**Documentation Says:**
- `endpoints.json` line 616: "Create new requirement [/requirement/]"
- `zephyr-enterprise-master-knowledge.md` line 80: `POST /requirement` - Create requirement
- `zephyr-enterprise-master-knowledge.md` line 514-520: Shows payload structure:
  ```json
  {
    "name": "Requirement Name",
    "projectId": 45,
    "description": "..."
  }
  ```

**Reality:**
- Returns HTTP 500: `"Cannot invoke \"java.lang.Long.longValue()\" because \"id\" is null"`
- Tried both `/requirement` and `/requirement/` (with trailing slash) - both fail
- Tried multiple payload structures (direct, wrapped, with id: 0, with parentId) - all fail
- **This is the endpoint that SHOULD create requirements according to docs, but it's broken in practice**

**Attempted Payloads (All Failed):**
1. Direct payload: `{"name": "...", "description": "...", "projectId": 45}`
2. Wrapped: `{"requirementDto": {...}}` → HTTP 403 (Forbidden)
3. With id: 0: `{"id": 0, "name": "...", ...}`
4. With parentId: `{"name": "...", "parentId": 698, ...}`

**Conclusion:** 
- The `/requirement` endpoint is documented but broken in this Zephyr instance
- Requirements may need to be created via UI, import, or a different workflow
- **Current workaround:** Use `/requirementtree/add` to create folders (not actual requirements)

#### `/requirement/{id}` (GET)
**Status:** ✅ **WORKS FOR READING**
- Successfully retrieves requirement details after UI creation
- Returns full requirement schema with all fields
- **Example:** `GET /requirement/6455` returns complete requirement object

**Schema Discovered (from REQ-DS-001, ID: 6455):**
```json
{
  "id": 6455,
  "name": "REQ-DS-001: Planet Destruction Capability",
  "priority": "1",  // Note: Stored as "1" not "P1" in API
  "details": "Description text...",
  "externalId": "REQ-DS-001",  // ALT ID field
  "createdOn": 1765152000000,
  "createdBy": 40,
  "requirementTreeIds": [698],  // Links to folder/tree node
  "projectId": 45,
  "testcaseIds": [],  // Empty until testcases allocated
  "releaseIds": [],
  "requirementType": 0,
  "attachmentCount": 0,
  // ... other fields
}
```

**Key Fields:**
- `priority`: Stored as string "1"-"5" (not "P1"-"P5")
- `externalId`: ALT ID field
- `details`: Description field
- `requirementTreeIds`: Array of folder/tree node IDs this requirement belongs to
- `testcaseIds`: Array of testcase IDs allocated to this requirement

#### `/requirement/project/{projectId}` (GET)
**Status:** ❌ **DOES NOT WORK**
- Returns HTTP 404
- Cannot list requirements by project

### UI Behavior

**What the UI Shows:**
- Tree view (left sidebar): Shows hierarchical folder structure
- Table view (main area): Shows requirements in a table format
- **Reality:** Both views show the same tree nodes, just different presentations

**Key Insight:** The "requirements" that appear in the table are actually leaf nodes (or all nodes) in the requirement tree. There's no separate "requirement" entity type - everything is a tree node.

### Workflow Pattern (Current Understanding)

1. **Create Folder (Top-Level):**
   ```python
   POST /requirementtree/add
   {
     "name": "Category Name",
     "description": "Category description",
     "projectId": 45
   }
   # Returns: { "id": 698, ... } - This is a FOLDER, not a requirement
   ```

2. **Create Subfolder (Child of Folder):**
   ```python
   POST /requirementtree/add
   {
     "name": "REQ-001: Requirement Name",
     "description": "Requirement description",
     "projectId": 45,
     "parentId": 698  # Folder ID from step 1
   }
   # Returns: { "id": 699, ... } - This is also a FOLDER, not a requirement
   ```

3. **Create Actual Requirement:**
   ```python
   # ❌ UNKNOWN - /requirement endpoint is broken
   # ❌ UNKNOWN - May require UI creation
   # ❌ UNKNOWN - May be created when testcases are allocated
   # TODO: Investigate further
   ```

4. **Link to Testcases (Later):**
   ```python
   POST /testcase/allocate/requirement
   {
     "testcaseId": 123,
     "requirementId": 699  # Folder ID or requirement ID?
   }
   ```

---

## 🗂️ Folders (Test Repository) API

### Endpoint: `/testcasetree` (POST)

**Status:** ⚠️ **INVESTIGATING**
- Current attempts failing with: `"For input string: \"null\""`
- Research indicates: API rejects `parentId: null` - must omit field entirely

**Payload Structure (Working Pattern - TBD):**
```json
{
  "name": "Folder Name",
  "description": "Folder description",
  "projectId": 45
  // Omit parentId for root folders
  // Include parentId: <folder_id> for nested folders
}
```

**⚠️ Gotcha:** 
- Do NOT send `parentId: null` as a string
- Do NOT send `parentId: null` as JSON null
- **Omit the field entirely** for root folders

---

## 🔄 Releases API

### Endpoint: `/release` (POST)

**Status:** ✅ **WORKING**

**Payload Structure:**
```json
{
  "name": "Release Name",
  "description": "Release description",
  "projectId": 45,
  "startDate": 1733529600000,  // milliseconds since epoch
  "endDate": 1765065600000,    // milliseconds since epoch
  "status": 0,  // 0=Draft, 1=Active, 2=Completed
  "globalRelease": true,  // CRITICAL: Always use true to avoid conflicts
  "projectRelease": false,
  "syncEnabled": false
}
```

**⚠️ Critical Gotcha:**
- **Always set `globalRelease: true`** to avoid "Project Release creation not allowed" errors
- Even if `projectRelease: false`, if a project-level release exists, the API will reject new releases unless `globalRelease: true`

**Example:**
```python
POST /release
{
  "name": "The Death Star Project - Phase 1",
  "description": "Galactic Empire's ultimate weapon development",
  "projectId": 45,
  "startDate": 1733529600000,
  "endDate": 1765065600000,
  "status": 0,
  "globalRelease": true,  # ← CRITICAL
  "projectRelease": false,
  "syncEnabled": false
}
```

---

## 🔁 Cycles API

### Endpoint: `/cycle` (POST)

**Status:** ✅ **WORKING** (without phases) | ⚠️ **INVESTIGATING** (with phases)

**Payload Structure (Without Phases - Working):**
```json
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
```

**Payload Structure (With Phases - Investigating):**
```json
{
  "name": "Cycle Name",
  "description": "Cycle description",
  "environment": "Production",
  "build": "1.0.0",
  "revision": 1,
  "status": 0,
  "startDate": 1733529600000,
  "endDate": 1765065600000,
  "releaseId": 131,
  "cyclePhases": [
    {
      "name": "Phase 1 - Planning",
      "status": 1,
      "order": 1,
      "startDate": 1733529600000,  // REQUIRED
      "endDate": 1765065600000,    // REQUIRED
      "treePhaseId": ???  // INVESTIGATING: May need folder tree reference
    }
  ]
}
```

**⚠️ Gotchas:**
- **Cycle phases require `startDate` and `endDate`** - API rejects phases without dates
- **Error:** `"Tree phase id not found cannot be null"` - suggests phases may need `treePhaseId` (folder tree reference)
- **Error:** `"cycle phase start date cannot be null"` - must include `startDate` in each phase

---

## 📝 Testcases API

### Endpoint: `/testcase` (POST)

**Status:** ⚠️ **PENDING** (blocked by folder creation)

**Payload Structure (Expected):**
```json
{
  "testcase": {  // WRAPPED FORMAT - CRITICAL
    "name": "Testcase Name",
    "description": "Testcase description",
    "tcrCatalogTreeId": 123,  // REQUIRED: Folder tree node ID
    "projectId": 45,
    // ... other fields
  }
}
```

**⚠️ Gotcha:**
- **Testcase payload must be wrapped in `{"testcase": {...}}` object**
- **Requires `tcrCatalogTreeId`** - folder tree node ID (blocked until folders work)

---

## ▶️ Executions API

### Endpoint: `/execution` (POST)

**Status:** ⚠️ **PENDING** (blocked by testcases)

**Payload Structure (Expected):**
```json
{
  "cycleId": 204,
  "testcaseId": 123,
  "status": 0,  // 0=Not Executed, 1=Pass, 2=Fail, 3=Blocked
  // ... other fields
}
```

**Alternative (Wrapped Format - Fallback):**
```json
{
  "execution": {
    "cycleId": 204,
    "testcaseId": 123,
    "status": 0
  }
}
```

---

## 📊 Hierarchy & Creation Order

### Correct Order (Based on Discoveries)

1. **Requirements** (can be created independently)
   - Create folder: `POST /requirementtree/add` (no parentId)
   - Create requirement: `POST /requirementtree/add` (with parentId)

2. **Releases** (independent)
   - Create release: `POST /release` (always use `globalRelease: true`)

3. **Folders** (Test Repository) - ⚠️ **BLOCKED**
   - Create root folder: `POST /testcasetree` (omit parentId)
   - Create nested folder: `POST /testcasetree` (with parentId)

4. **Testcases** (requires folders)
   - Create testcase: `POST /testcase` (wrapped format, requires `tcrCatalogTreeId`)

5. **Cycles** (requires releases)
   - Create cycle: `POST /cycle` (with or without phases)

6. **Executions** (requires cycles + testcases)
   - Create execution: `POST /execution` (requires `cycleId` + `testcaseId`)

---

## 🔍 Endpoint Patterns Discovered

### Wrapped vs Direct Payloads

**Some endpoints require wrapped payloads:**
- ✅ Testcases: `{"testcase": {...}}`
- ⚠️ Executions: May need `{"execution": {...}}` (fallback)

**Some endpoints use direct payloads:**
- ✅ Releases: Direct payload
- ✅ Cycles: Direct payload
- ✅ Requirements: Direct payload (via `/requirementtree/add`)

### Null Field Handling

**Critical Pattern:** Zephyr API rejects `null` values in certain fields.

**Do NOT send:**
```json
{
  "parentId": null  // ❌ WRONG - API rejects this
}
```

**Do this instead:**
```json
{
  // Omit the field entirely  // ✅ CORRECT
}
```

**Affected Fields:**
- `parentId` (folders, requirements)
- `order` (may be auto-assigned, omit if causing issues)

---

## 📚 Documentation Strategy

### What to Document

1. **✅ Endpoint Patterns** (this document)
   - Working endpoints
   - Broken endpoints
   - Gotchas and workarounds

2. **✅ Playbooks for Key Workflows**
   - `prepare.001-createTestData.md` - Test data creation workflow
   - `prepare.002-introspectSchemas.md` - Schema discovery workflow
   - Future: `prepare.004-createRequirements.md` - Requirements creation
   - Future: `prepare.005-createTestcases.md` - Testcase creation

3. **✅ Research Summary Updates**
   - Update `ZEPHYR-RESEARCH-SUMMARY.md` with discovered patterns
   - Document API quirks and gotchas

### What NOT to Document as Playbooks

**Don't create playbooks for:**
- ❌ Every single endpoint (too granular)
- ❌ Simple CRUD operations (document in API discoveries instead)
- ❌ One-off scripts (document in script comments)

**Do create playbooks for:**
- ✅ Multi-step workflows (e.g., "Create Complete Test Data Structure")
- ✅ Complex processes (e.g., "Schema Discovery via Test Data Creation")
- ✅ Critical setup activities (e.g., "Bootstrap Endpoints Catalog")

---

## 🎯 Next Steps

1. **Continue documenting discoveries** in this file as we learn
2. **Update `ZEPHYR-RESEARCH-SUMMARY.md`** with confirmed patterns
3. **Create playbooks** for key workflows (requirements, testcases, executions)
4. **Fix folder creation** - investigate `/testcasetree` endpoint
5. **Fix cycle phases** - investigate `treePhaseId` requirement

---

## 📝 Change Log

- **2025-12-08:** Initial discovery - Requirements are tree nodes, not separate entities
- **2025-12-08:** Discovered release `globalRelease: true` requirement
- **2025-12-08:** Discovered testcase wrapped payload requirement
- **2025-12-08:** Discovered cycle phase `startDate`/`endDate` requirements
- **2025-12-08:** **CRITICAL:** `/requirementtree/add` creates folders, NOT requirements. `/requirement` endpoint is broken for creation.
- **2025-12-08:** **DISCOVERED:** Requirements must be created via UI. `/requirement/{id}` GET endpoint works for reading. Priority stored as "1"-"5" (not "P1"-"P5").

