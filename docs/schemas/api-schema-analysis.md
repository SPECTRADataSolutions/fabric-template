# Zephyr API Schema Analysis

**Date:** 2025-12-05  
**Source:** Real API responses from production Zephyr instance  
**Purpose:** Understand exact schemas for POST/PUT operations without assumptions

---

## ✅ Schemas Captured (From Real API Responses)

### 1. **Project Schema** (Complete)

**From:** `GET /project/details` response + created project response

**Required Fields for POST:**
```json
{
  "name": "string",              // REQUIRED - Project name
  "startDate": 1764979914622,    // REQUIRED - Timestamp (milliseconds)
  "active": true,                // REQUIRED - Boolean
  "status": "2"                  // REQUIRED - Status code (observed: "2" for active)
}
```

**Optional Fields (observed in responses):**
- `description` - Project description
- `externalSystem` - External system name
- `shared` - Boolean (default: false)
- `dashboardSecured` - Boolean (default: false)
- `dashboardRestricted` - Boolean (default: false)
- `isolationLevel` - Integer (default: 0)
- `globalProject` - Boolean (default: false)
- `allowedGlobalProject` - Boolean (default: false)
- `autoUpdateTestStatus` - Boolean (default: false)
- `allowedInternalRequirements` - Boolean (default: false)
- `members` - Array (default: [])
- `projectGroups` - Array (default: [])
- `sharedProjects` - Array (default: [])
- `customProperties` - Object (default: {})

**Response Structure:**
- Wrapped in `projectDto` object
- Includes auto-generated: `id`, `version`, `createdOn`, `projectStartDate`

---

### 2. **Release Schema** (Complete)

**From:** `GET /release/project/{projectId}` response

**Required Fields for POST:**
```json
{
  "name": "string",              // REQUIRED - Release name
  "projectId": 44,               // REQUIRED - Parent project ID
  "startDate": 1743375600000,    // REQUIRED - Timestamp (milliseconds)
  "endDate": 1767139200000,      // REQUIRED - Timestamp (milliseconds)
  "status": 0                    // REQUIRED - Status (observed: 0)
}
```

**Optional Fields:**
- `description` - Release description
- `orderId` - Integer (sequencing)
- `globalRelease` - Boolean (default: false)
- `projectRelease` - Boolean (default: false)
- `syncEnabled` - Boolean (default: false)

**Response Includes:**
- `id` - Auto-generated release ID
- `releaseStartDate`, `releaseEndDate` - Formatted date strings
- `createdDate` - Timestamp
- `hasChild` - Boolean

---

### 3. **Cycle Schema** (Complete)

**From:** `GET /cycle/release/{releaseId}` response

**Required Fields for POST:**
```json
{
  "name": "string",              // REQUIRED - Cycle name
  "releaseId": 106,              // REQUIRED - Parent release ID
  "startDate": 1743375600000,    // REQUIRED - Timestamp (milliseconds)
  "endDate": 1747609200000,      // REQUIRED - Timestamp (milliseconds)
  "status": 0                    // REQUIRED - Status (observed: 0)
}
```

**Optional Fields:**
- `environment` - String (e.g., "UAT101")
- `build` - String (e.g., "22.1")
- `revision` - Integer (default: 0 or auto-generated)

**Cycle Phases:**
- Cycles can have multiple `cyclePhases`
- Each phase has: `name`, `tcrCatalogTreeId` (links to testcase catalog tree), `freeForm` (boolean), `startDate`, `endDate`

**Response Includes:**
- `id` - Auto-generated cycle ID
- `cycleStartDate`, `cycleEndDate` - Formatted date strings
- `createdOn` - Timestamp
- `cyclePhases` - Array of phase objects
- `hasChild` - Boolean

---

## ⚠️ Schemas Needing More Data

### 4. **Testcase Schema** (Partial)

**Status:** Failed to fetch via testcase endpoints (500 error on `/testcase/nodes`)

**Known from Cycle Schema:**
- Testcases are linked via `tcrCatalogTreeId` in cycle phases
- Hierarchical structure (hasChild patterns suggest tree)

**Endpoints Available:**
- `POST /testcase` - Create Testcase
- `POST /testcase/bulk` - Create bulk Testcases
- `GET /testcase/{id}` - Get by ID
- `GET /testcase/nodes?treeIds={id}` - Get by tree IDs

**Next Steps:**
- Try creating a minimal testcase to see required fields
- Check Zephyr API documentation
- Test POST with minimal payload

---

### 5. **Execution Schema** (Not Captured)

**Status:** No successful fetch (tried multiple endpoint patterns)

**Known:**
- Executions are linked to cycles/cycle phases
- Statuses include: Passed, Failed, Blocked, Not Executed

**Next Steps:**
- Test POST `/execution` to understand required fields
- Check if executions are created automatically when testcases are assigned to cycles

---

## 🎯 What I Can Create With Confidence

**✅ Can create without assumptions:**
1. **Projects** - Complete schema known
2. **Releases** - Complete schema known
3. **Cycles** - Complete schema known (including cycle phase structure)

**⚠️ Need to test/infer:**
4. **Testcases** - Need to test POST to determine required fields
5. **Executions** - Need to understand creation pattern

---

## 💡 Recommendation

**Phase 1: Create what we know**
- Create SpectraTestProject (✅ done)
- Create releases with full schema
- Create cycles with cycle phases

**Phase 2: Test creation for unknowns**
- Create minimal testcase via POST to see required fields
- Document actual vs expected payload
- Iterate until perfect schema is captured

**Phase 3: Complete SpectraTestProject**
- Build full hierarchy once all schemas confirmed

---

## 📋 Next Action

Test POST `/testcase` with minimal payload to capture exact schema requirements.

