# Zephyr API Hierarchy Discovery - Complete Summary

> **Discovered:** 2025-12-08  
> **Method:** Systematic autonomous experimentation  
> **Status:** 🟡 Partial Success (3/8 entities working)

---

## 🎯 Objective

Discover the TRUE canonical creation order for Zephyr entities by:
1. Testing each entity type with minimal payloads
2. Identifying dependencies through systematic experimentation
3. Building a complete dependency graph
4. Determining optimal creation order

---

## ✅ Working Entities (Level 0 - Independent)

### 1. **Release**
- **Endpoint:** `POST /release`
- **Dependencies:** None (independent)
- **Payload:**
  ```json
  {
    "projectId": 45,
    "name": "Release Name",
    "description": "Description",
    "startDate": "2025-12-08",
    "globalRelease": true,
    "projectRelease": false
  }
  ```
- **Success Rate:** 100%
- **Notes:** 
  - ✅ Works perfectly
  - ⚠️ **CRITICAL:** Locks for >60 seconds after creation
  - ✅ **WORKAROUND:** Use existing releases (no lock)

### 2. **Requirement Folder**
- **Endpoint:** `POST /requirementtree/add`
- **Dependencies:** None (independent)
- **Payload:**
  ```json
  {
    "projectId": 45,
    "name": "Folder Name",
    "description": "Description"
  }
  ```
- **Success Rate:** 100%
- **Notes:** ✅ Works perfectly

---

## ✅ Working Entities (Level 1 - Single Dependency)

### 3. **Requirement** (actual requirement, not folder)
- **Endpoint:** `POST /requirementtree/add` (with `parentId`)
- **Dependencies:** `requirement_folder`
- **Payload:**
  ```json
  {
    "projectId": 45,
    "name": "Requirement Name",
    "description": "Description",
    "parentId": 704  // ID of parent folder
  }
  ```
- **Success Rate:** 100% (with workaround)
- **Notes:** 
  - ❌ `POST /requirement` is BROKEN (HTTP 500)
  - ✅ **WORKAROUND:** Use `/requirementtree/add` with `parentId`
  - Creates a tree node (appears as subfolder/requirement)

### 4. **Cycle**
- **Endpoint:** `POST /cycle`
- **Dependencies:** `release`
- **Payload:**
  ```json
  {
    "projectId": 45,
    "releaseId": 131,  // Use EXISTING release
    "name": "Cycle Name",
    "description": "Description",
    "environment": "Production",
    "build": "1.0.0",
    "revision": 1,
    "status": 0,
    "startDate": 1765221829260,
    "endDate": 1767139200000
  }
  ```
- **Success Rate:** 100% (with existing release)
- **Notes:** 
  - ❌ FAILS with newly created releases (locked >60s)
  - ✅ **WORKS** with existing releases (no lock)
  - ⚠️ Do NOT include `cyclePhases` in payload

---

## ❌ Blocked Entities

### 5. **Testcase Folder** 🔴 BLOCKER-002
- **Endpoint:** `POST /testcasetree`
- **Dependencies:** None (should be independent)
- **Status:** ❌ **BROKEN**
- **Error:** `HTTP 400: For input string: "null"`
- **Attempts:**
  1. Direct payload (omit `parentId`) → FAIL
  2. With `parentId: 0` → FAIL
  3. Wrapped payload → FAIL
  4. `/testcasetree/add` endpoint → HTTP 405 (Method Not Allowed)
- **Impact:** 🔥 **CRITICAL** - Blocks testcase creation
- **Workaround:** ✅ Create folders manually in UI, fetch ID via API

### 6. **Testcase**
- **Endpoint:** `POST /testcase`
- **Dependencies:** `testcase_folder`
- **Status:** ⏸️ **BLOCKED** (by testcase_folder failure)
- **Expected Payload:**
  ```json
  {
    "testcase": {  // Wrapped format required
      "projectId": 45,
      "tcrCatalogTreeId": 123,  // Folder ID
      "name": "Testcase Name",
      "description": "Description",
      "priority": "Critical"
    }
  }
  ```
- **Notes:** Cannot test until folder issue resolved

### 7. **Execution**
- **Endpoint:** `POST /execution`
- **Dependencies:** `cycle`, `testcase`
- **Status:** ⏸️ **BLOCKED** (by testcase_folder failure)
- **Expected Payload:**
  ```json
  {
    "cycleId": 209,
    "testcaseId": 456,
    "projectId": 45,
    "status": 1,
    "executedBy": "mark@spectradatasolutions.com"
  }
  ```
- **Notes:** Cannot test until testcase issue resolved

### 8. **Allocation** (links requirements to testcases)
- **Endpoint:** `POST /allocation`
- **Dependencies:** `requirement`, `testcase`
- **Status:** ⏸️ **BLOCKED** (by testcase_folder failure)
- **Expected Payload:**
  ```json
  {
    "requirementId": 707,
    "testcaseId": 456
  }
  ```
- **Notes:** Cannot test until testcase issue resolved

---

## 📋 Canonical Creation Order (Discovered)

### **Level 0: Independent Entities**
1. ✅ **Release** (use existing to avoid lock)
2. ✅ **Requirement Folder**

### **Level 1: Single Dependencies**
3. ✅ **Requirement** (depends on requirement_folder)
4. ✅ **Cycle** (depends on release - use existing!)

### **Level 2: Multiple Dependencies** (Blocked)
5. ❌ **Testcase Folder** (BLOCKER-002 - API broken)
6. ⏸️ **Testcase** (depends on testcase_folder)
7. ⏸️ **Execution** (depends on cycle + testcase)
8. ⏸️ **Allocation** (depends on requirement + testcase)

---

## 🌳 Dependency Graph

```
[independent] → release
[independent] → requirement_folder
                    ↓
requirement_folder → requirement
                    
release → cycle

[BLOCKED] testcase_folder → testcase
                                ↓
                    cycle + testcase → execution
                    
                requirement + testcase → allocation
```

---

## 🔴 Critical Blockers

### **BLOCKER-002: Testcase Folder Creation API Broken**
- **Impact:** 🔥 **CRITICAL** - Blocks entire testcase/execution workflow
- **Error:** `HTTP 400: For input string: "null"`
- **All Attempts Failed:**
  - Direct payload
  - With `parentId: 0`
  - Wrapped payload
  - `/testcasetree/add` endpoint (HTTP 405)
- **Workaround:** ✅ Create folders manually in UI

### **Release Lock Duration >60s**
- **Impact:** 🟡 **MEDIUM** - Slows automated testing
- **Issue:** Newly created releases lock for >60 seconds
- **Workaround:** ✅ Use existing releases (no lock)

---

## ✅ Recommended Approach for Test Data Creation

### **Phase 1: Use Existing Releases**
```python
# Use existing "The Death Star Project - Phase 1" (ID: 131)
RELEASE_ID = 131  # No lock, works immediately
```

### **Phase 2: Create Requirement Hierarchy**
```python
1. Create requirement folder
2. Create requirements under folder
```

### **Phase 3: Create Cycles**
```python
# Use existing release (no delay needed)
Create cycles under release ID 131
```

### **Phase 4: Manual Folder Creation (WORKAROUND)**
```python
1. Create folders in UI (Test Repository)
2. Fetch folder IDs via API
3. Use IDs for testcase creation
```

### **Phase 5: Create Testcases**
```python
# Once folder IDs are known
Create testcases under folders
```

### **Phase 6: Create Executions**
```python
# Link cycles + testcases
Create executions
```

### **Phase 7: Create Allocations**
```python
# Link requirements + testcases
Create allocations
```

---

## 📊 Success Rate

**Overall:** 4/8 entities working (50%)

**By Level:**
- Level 0 (Independent): 2/2 (100%) ✅
- Level 1 (Single Dep): 2/2 (100%) ✅
- Level 2 (Multiple Deps): 0/4 (0%) ❌ (blocked by folder API)

---

## 🎯 Next Steps

1. ✅ **Use existing releases** (avoid lock)
2. ✅ **Create requirement hierarchy** (works perfectly)
3. ✅ **Create cycles** (with existing release)
4. ⚠️ **Manual folder creation** (UI workaround)
5. ⏸️ **Test testcase creation** (once folders exist)
6. ⏸️ **Test execution creation** (once testcases exist)
7. ⏸️ **Test allocation creation** (once testcases exist)

---

## 📁 Generated Reports

- `hierarchy-discovery-full-20251208-192232.json` - Full experimental results
- `hierarchy-with-existing-20251208-192635.json` - Results with existing release
- `canonical-creation-order.md` - This summary

---

**Status:** 🟡 Partial Success - 50% working, 50% blocked by folder API

