# Issue to Playbook Mapping

> **Purpose:** Map all discovered bugs/blockers to the playbooks where they were discovered  
> **Status:** 🟡 Active - Updated as issues are discovered  
> **Last Updated:** 2025-12-08

---

## 📋 Current Issue Mapping

### **Stage 1: Source**

#### `source.001-createSourceNotebook`
- ✅ No issues discovered

#### `source.002-addNotebookToPipeline`
- ✅ No issues discovered

#### `source.003-bootstrapEndpoints`
- **DOC-GAP-001:** Endpoint Duplicates in Catalog
  - **Status:** ✅ Resolved
  - **Impact:** Endpoint catalog contained duplicates
  - **Resolution:** Fixed parsing logic, zero duplicates achieved

---

### **Stage 2: Prepare**

#### `prepare.000-discoverFieldMetadata`
- ✅ No issues discovered yet (not executed)

#### `prepare.001-createTestData`
- **BLOCKER-002:** Test Repository Folder Creation API Broken
  - **Status:** 🔴 Critical Blocker
  - **Impact:** Cannot create folders, blocks testcase creation
  - **Workaround:** Manual folder creation in UI

- **BUG-002:** Cycle Phase `startDate` Required but Not Documented
  - **Status:** 🐛 Bug (Resolved)
  - **Impact:** Cycle creation with phases failed
  - **Resolution:** Added `startDate`/`endDate` to phases

- **BUG-003:** Release `globalRelease` vs `projectRelease` Conflict
  - **Status:** 🐛 Bug (Resolved)
  - **Impact:** Release creation failed with confusing error
  - **Resolution:** Always use `globalRelease: true`

- **BUG-004:** Testcase Payload Must Be Wrapped
  - **Status:** 🐛 Bug (Resolved)
  - **Impact:** Testcase creation failed
  - **Resolution:** Wrap payload in `{"testcase": {...}}`

- **BUG-005:** Folder `parentId: null` Rejected as String
  - **Status:** 🐛 Bug (Resolved, but endpoint still broken)
  - **Impact:** Folder creation failed
  - **Resolution:** Omit `parentId` field for root folders

#### `prepare.002-introspectSchemas`
- ✅ No issues discovered yet (waiting for complete test data)

#### `prepare.003-loadSchemaIntoNotebook`
- ✅ No issues discovered yet (waiting for complete schema)

#### `prepare.004-create-requirements`
- **BLOCKER-001:** Requirement Creation API Broken
  - **Status:** 🔴 Critical Blocker
  - **Impact:** Cannot create requirements programmatically
  - **Workaround:** Manual requirement creation in UI

- **BUG-001:** `/requirementtree/add` Creates Folders, Not Requirements
  - **Status:** 🐛 Bug
  - **Impact:** Confusion about endpoint behavior
  - **Workaround:** Use for folders only, create requirements manually

- **DOC-GAP-002:** Requirement API Endpoint Confusion
  - **Status:** ⚠️ Documentation Gap
  - **Impact:** Misleading endpoint names and behavior
  - **Workaround:** Documented in API discoveries

---

## 📊 Summary by Playbook

| Playbook | Critical Blockers | Bugs | Doc Gaps | Total |
|----------|------------------|------|----------|-------|
| `source.003-bootstrapEndpoints` | 0 | 0 | 1 (resolved) | 1 |
| `prepare.001-createTestData` | 1 | 4 | 0 | 5 |
| `prepare.004-create-requirements` | 1 | 1 | 1 | 3 |
| **Total** | **2** | **5** | **2** | **9** |

---

## 🎯 GitHub Project Structure

### **Project: Zephyr Pipeline Development**

**Organization:**
```
Zephyr Pipeline Development
├── Stage 1: Source
│   ├── source.001-createSourceNotebook
│   │   └── [No issues]
│   ├── source.002-addNotebookToPipeline
│   │   └── [No issues]
│   └── source.003-bootstrapEndpoints
│       └── DOC-GAP-001: Endpoint Duplicates (✅ Resolved)
│
├── Stage 2: Prepare
│   ├── prepare.000-discoverFieldMetadata
│   │   └── [Not executed yet]
│   ├── prepare.001-createTestData
│   │   ├── BLOCKER-002: Folder Creation API Broken
│   │   ├── BUG-002: Cycle Phase startDate Required
│   │   ├── BUG-003: Release globalRelease Conflict
│   │   ├── BUG-004: Testcase Payload Wrapper
│   │   └── BUG-005: Folder parentId: null
│   ├── prepare.002-introspectSchemas
│   │   └── [Waiting for test data]
│   ├── prepare.003-loadSchemaIntoNotebook
│   │   └── [Waiting for schema]
│   └── prepare.004-create-requirements
│       ├── BLOCKER-001: Requirement Creation API Broken
│       ├── BUG-001: requirementtree/add Creates Folders
│       └── DOC-GAP-002: Requirement API Confusion
│
└── Stage 3-7: [Future stages]
```

---

## 🔄 Workflow for Adding Issues

### **When Issue Discovered During Playbook Execution:**

1. **Identify Playbook:**
   - Which playbook were you following?
   - At what step did the issue occur?

2. **Create GitHub Issue:**
   - Title: `[BLOCKER/BUG/DOC-GAP-XXX] Issue Title`
   - Body: Copy from `bug-and-blocker-registry.md`
   - Labels: `bug`, `blocker`, `api-issue`, `zephyr-support`, `[stage]-[playbook]`
   - Assign to: Current stage owner

3. **Add to Project:**
   - Add to "Zephyr Pipeline Development" project
   - Set Stage: [Current stage]
   - Set Playbook: [Playbook where discovered]
   - Set Status: [Critical Blocker/Bug/Documentation Gap]
   - Set Severity: [Critical/High/Medium/Low]
   - Set Report Status: ⏳ Pending Report

4. **Update Registry:**
   - Add issue to `bug-and-blocker-registry.md`
   - Link to GitHub issue number
   - Update this mapping document

5. **Link Playbook:**
   - Add issue reference to playbook markdown
   - Document workaround in playbook if applicable

---

## 📝 Issue Labels

### **Stage Labels:**
- `stage:source`
- `stage:prepare`
- `stage:extract`
- `stage:clean`
- `stage:transform`
- `stage:refine`
- `stage:analyse`

### **Playbook Labels:**
- `playbook:source.001`
- `playbook:source.002`
- `playbook:source.003`
- `playbook:prepare.000`
- `playbook:prepare.001`
- `playbook:prepare.002`
- `playbook:prepare.003`
- `playbook:prepare.004`
- [Future playbooks]

### **Type Labels:**
- `bug`
- `blocker`
- `api-issue`
- `zephyr-support`
- `documentation-gap`

### **Priority Labels:**
- `priority:critical`
- `priority:high`
- `priority:medium`
- `priority:low`

---

## 🔗 Related Documentation

- **Bug Registry:** `bug-and-blocker-registry.md` - Complete issue documentation
- **Project Structure:** `github-project-structure.md` - GitHub Projects setup guide
- **API Discoveries:** `ZEPHYR-API-DISCOVERIES.md` - Detailed API patterns
- **Autonomy Blockers:** `AUTONOMY-BLOCKERS-AND-LIMITATIONS.md` - Autonomy impact focus

---

**Last Updated:** 2025-12-08  
**Next Review:** After completing Prepare stage test data creation

