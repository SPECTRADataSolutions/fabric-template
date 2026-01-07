# GitHub Project Structure - Zephyr Pipeline

> **Purpose:** Structure for tracking bugs, blockers, and issues in GitHub Projects, aligned with SPECTRA stages and playbooks  
> **Status:** ⚠️ **SUPERSEDED** - See [`spectra-wide-project-structure.md`](spectra-wide-project-structure.md) for unified SPECTRA-wide project  
> **Last Updated:** 2025-12-08

---

## ⚠️ Note

This document proposed a Zephyr-specific project. **We've moved to a single SPECTRA-wide project** with rich metadata fields. See [`spectra-wide-project-structure.md`](spectra-wide-project-structure.md) for the new structure.

This document is kept for reference but is superseded.

---

## 📋 Project Structure

### **Project: Zephyr Pipeline Development**

**Organization:** By SPECTRA Stage → Playbook → Issues

```
Zephyr Pipeline Development
├── Stage 1: Source
│   ├── source.001-createSourceNotebook
│   │   └── [Issues discovered during this playbook]
│   ├── source.002-addNotebookToPipeline
│   │   └── [Issues discovered during this playbook]
│   └── source.003-bootstrapEndpoints
│       └── [Issues discovered during this playbook]
│
├── Stage 2: Prepare
│   ├── prepare.000-discoverFieldMetadata
│   │   └── [Issues discovered during this playbook]
│   ├── prepare.001-createTestData
│   │   ├── BLOCKER-001: Requirement Creation API Broken
│   │   ├── BLOCKER-002: Folder Creation API Broken
│   │   ├── BUG-003: Release globalRelease Conflict
│   │   ├── BUG-004: Testcase Payload Wrapper
│   │   └── BUG-005: Folder parentId: null
│   ├── prepare.002-introspectSchemas
│   │   └── [Issues discovered during this playbook]
│   ├── prepare.003-loadSchemaIntoNotebook
│   │   └── [Issues discovered during this playbook]
│   └── prepare.004-create-requirements
│       └── BLOCKER-001: Requirement Creation API Broken
│
├── Stage 3: Extract
│   └── [Future playbooks]
│
├── Stage 4: Clean
│   └── [Future playbooks]
│
├── Stage 5: Transform
│   └── [Future playbooks]
│
├── Stage 6: Refine
│   └── [Future playbooks]
│
└── Stage 7: Analyse
    └── [Future playbooks]
```

---

## 🎯 Issue Mapping

### **Current Issues → Playbooks**

| Issue ID | Title | Stage | Playbook | Status |
|----------|-------|-------|----------|--------|
| **BLOCKER-001** | Requirement Creation API Broken | Prepare | `prepare.001-createTestData`<br>`prepare.004-create-requirements` | 🔴 Critical |
| **BLOCKER-002** | Folder Creation API Broken | Prepare | `prepare.001-createTestData` | 🔴 Critical |
| **BUG-001** | `/requirementtree/add` Creates Folders, Not Requirements | Prepare | `prepare.004-create-requirements` | 🐛 Bug |
| **BUG-002** | Cycle Phase `startDate` Required but Not Documented | Prepare | `prepare.001-createTestData` | 🐛 Bug |
| **BUG-003** | Release `globalRelease` vs `projectRelease` Conflict | Prepare | `prepare.001-createTestData` | 🐛 Bug |
| **BUG-004** | Testcase Payload Must Be Wrapped | Prepare | `prepare.001-createTestData` | 🐛 Bug |
| **BUG-005** | Folder `parentId: null` Rejected as String | Prepare | `prepare.001-createTestData` | 🐛 Bug |
| **DOC-GAP-001** | Endpoint Duplicates in Catalog | Source | `source.003-bootstrapEndpoints` | ✅ Resolved |
| **DOC-GAP-002** | Requirement API Endpoint Confusion | Prepare | `prepare.004-create-requirements` | ⚠️ Documented |

---

## 📝 GitHub Project Setup

### **Project Fields**

**Status Field:**
- 🔴 Critical Blocker
- 🐛 API Bug
- ⚠️ Documentation Gap
- ✅ Resolved
- ⏳ Pending Report

**Stage Field:**
- Source
- Prepare
- Extract
- Clean
- Transform
- Refine
- Analyse

**Playbook Field:**
- `source.001-createSourceNotebook`
- `source.002-addNotebookToPipeline`
- `source.003-bootstrapEndpoints`
- `prepare.000-discoverFieldMetadata`
- `prepare.001-createTestData`
- `prepare.002-introspectSchemas`
- `prepare.003-loadSchemaIntoNotebook`
- `prepare.004-create-requirements`
- [Future playbooks]

**Severity Field:**
- Critical
- High
- Medium
- Low

**Report Status:**
- ⏳ Pending Report to Zephyr
- 📧 Reported to Zephyr
- 🔄 In Progress (Zephyr)
- ✅ Resolved by Zephyr

---

## 🔄 Workflow

### **When Issue Discovered:**

1. **Create GitHub Issue:**
   - Title: `[BLOCKER/BUG/DOC-GAP-XXX] Issue Title`
   - Body: Copy from `bug-and-blocker-registry.md`
   - Labels: `bug`, `blocker`, `api-issue`, `zephyr-support`
   - Assign to: Current stage owner

2. **Add to Project:**
   - Add to "Zephyr Pipeline Development" project
   - Set Stage: [Current stage]
   - Set Playbook: [Playbook where discovered]
   - Set Status: [Critical Blocker/Bug/Documentation Gap]
   - Set Severity: [Critical/High/Medium/Low]
   - Set Report Status: ⏳ Pending Report

3. **Update Registry:**
   - Add issue to `bug-and-blocker-registry.md`
   - Link to GitHub issue number
   - Update summary statistics

4. **Link Playbook:**
   - Add issue reference to playbook markdown
   - Document workaround in playbook if applicable

---

## 📊 Project Views

### **View 1: By Stage**
Group issues by SPECTRA stage to see blockers per stage.

### **View 2: By Playbook**
Group issues by playbook to see what's blocking each playbook.

### **View 3: Critical Blockers**
Filter to show only critical blockers across all stages.

### **View 4: Pending Reports**
Show all issues that need to be reported to Zephyr support.

### **View 5: By Severity**
Group by severity to prioritize fixes/workarounds.

---

## 🔗 Integration with Registry

**Two-Way Sync:**
- GitHub Issues = Active tracking, assignments, discussions
- `bug-and-blocker-registry.md` = Comprehensive documentation, reporting template

**When Creating Issue:**
- Copy issue details from registry
- Add GitHub issue number to registry
- Link registry entry to GitHub issue

**When Updating:**
- Update both GitHub issue and registry
- Keep status in sync
- Use GitHub for workflow, registry for documentation

---

## 📋 Issue Template

```markdown
## Issue: [BLOCKER/BUG/DOC-GAP-XXX] - [Title]

**Registry ID:** [BLOCKER-001, BUG-001, etc.]
**Stage:** [Source/Prepare/Extract/etc.]
**Playbook:** [playbook.001-name]
**Severity:** [Critical/High/Medium/Low]
**Status:** [Critical Blocker/Bug/Documentation Gap]
**Report Status:** ⏳ Pending Report to Zephyr

### Description
[From registry]

### Impact
[From registry]

### Workaround
[From registry]

### Test Evidence
[Links to scripts, responses]

### Related
- Registry: `docs/bug-and-blocker-registry.md`
- Playbook: `Core/operations/playbooks/fabric/[stage]/[playbook].md`
```

---

## 🎯 Benefits

1. **Visibility:** See all blockers per stage/playbook at a glance
2. **Tracking:** GitHub Projects provides kanban-style tracking
3. **Reporting:** Easy to generate reports for Zephyr support
4. **Alignment:** Issues directly linked to playbooks where discovered
5. **Workflow:** Standard GitHub issue workflow (assignments, labels, milestones)
6. **Documentation:** Registry remains comprehensive reference

---

**Last Updated:** 2025-12-08  
**Next Steps:** Create GitHub project and migrate current issues

