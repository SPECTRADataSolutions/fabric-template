# Playbook-Issue Integration

> **Purpose:** SPECTRA-grade approach to linking playbooks with GitHub issues  
> **Status:** 🟡 Proposed Structure  
> **Last Updated:** 2025-12-08

---

## 🎯 SPECTRA-Grade Approach

**Three-Layer System:**

1. **Contract** (`contracts/*.contract.yaml`) - Defines stage obligations, inputs, outputs, quality gates
2. **Manifest** (`manifest.json`) - Enumerates activities (pipeline activities, stages, dependencies)
3. **Playbooks** (`Core/operations/playbooks/fabric/*/`) - Step-by-step execution guides

**Issue Tracking:**
- **Each playbook = one piece of work = one issue** in `zephyr-backlog` project
- Work is naturally scoped to playbook size
- Issues link back to playbooks via references
- Playbooks reference issues when bugs/blockers are discovered

**Key Principle:** No automation needed - just consistent pattern. When you create a playbook, create the corresponding issue manually.

---

## 📋 Current State

### **Contracts**

**Location:** `Data/zephyr/contracts/`

**Files:**
- `source.contract.yaml` - Source stage contract (v3.0.0)
- Future: `prepare.contract.yaml`, `extract.contract.yaml`, etc.

**Purpose:**
- Define stage obligations (what must be done)
- Define inputs/outputs (data contracts)
- Define quality gates (validation requirements)
- Define dependencies (workspace, pipeline, notebook IDs)

---

### **Manifests**

**Location:** `Data/zephyr/manifest.json` (or `spectra.manifest.json`)

**Purpose:**
- Enumerate pipeline activities
- Define stage sequence
- Define activity dependencies
- Define inputs/outputs between activities

**Structure:**
```json
{
  "version": "1.0.0",
  "pipelines": [{
    "name": "zephyr",
    "activities": [
      {
        "id": "source",
        "stage": "Source",
        "activityType": "notebook",
        "inputs": null,
        "outputs": ["source.portfolio", "source.endpoints"]
      },
      {
        "id": "prepare",
        "stage": "Prepare",
        "activityType": "notebook",
        "inputs": {"endpoints": "source.endpoints"},
        "outputs": ["prepare._schema"]
      }
    ]
  }]
}
```

---

### **Playbooks**

**Location:** `Core/operations/playbooks/fabric/{stage}/`

**Files:**
- `source.001-createSourceNotebook.md`
- `source.002-addNotebookToPipeline.md`
- `source.003-bootstrapEndpoints.md`
- `prepare.000-discoverFieldMetadata.md`
- `prepare.001-createTestData.md`
- etc.

**Purpose:**
- Step-by-step execution guides
- Prerequisites, procedures, validation
- Evidence capture
- Dependencies between playbooks

---

## 🔗 Playbook-Issue Linking

### **Option 1: Issue for Each Playbook (Recommended)**

**Approach:**
- Create a task/issue in `zephyr-backlog` for each playbook
- Issue title: `[PLAYBOOK] {playbook.name} - {playbook.title}`
- Issue body includes:
  - Playbook reference: `Core/operations/playbooks/fabric/{stage}/{playbook.name}.md`
  - Purpose, prerequisites, dependencies
  - Acceptance criteria (from playbook "produces" section)
  - Links to discovered bugs/blockers

**Benefits:**
- Track playbook execution status
- Link bugs/blockers to specific playbooks
- Track dependencies between playbooks
- Clear progress visibility

**Example Issue:**
```markdown
# [PLAYBOOK] prepare.001-createTestData - Create Comprehensive Test Data

**Playbook:** `Core/operations/playbooks/fabric/2-prepare/prepare.001-createTestData.md`

## Purpose
Create comprehensive test data in Zephyr's SpectraTestProject for schema discovery.

## Prerequisites
- `prepare.000-discoverFieldMetadata.md` completed
- Field metadata available in `docs/schemas/discovered/field_metadata.json`

## Acceptance Criteria
- [ ] All enum values tested
- [ ] All validation rules respected
- [ ] All relationships established
- [ ] API responses captured for introspection

## Discovered Issues
- BLOCKER-002: Test Repository Folder Creation API Broken
- BUG-002: Cycle Phase `startDate` Required
- BUG-003: Release `globalRelease` vs `projectRelease` Conflict
- BUG-004: Testcase Payload Must Be Wrapped
- BUG-005: Folder `parentId: null` Rejected

## Status
⏳ In Progress
```

---

## 🎯 SPECTRA-Grade Approach

### **Simple Model:**

1. **Playbook = Issue** - Each playbook is one piece of work, tracked as one issue
   - Work naturally scoped to playbook size
   - Track execution status
   - Link to contracts/manifests
   - Show dependencies

2. **Bug/Blocker Issues** - Create issues when problems discovered
   - Link to playbook where discovered
   - Link to playbook issue
   - Track resolution

3. **Contract Alignment** - Issues align with contract obligations
   - Each contract obligation → playbook → issue
   - Quality gates tracked in issues
   - Validation status tracked

4. **Manifest Integration** - Activities in manifest map to playbooks
   - Each activity → playbook → issue
   - Dependencies tracked
   - Stage progression tracked

**Key Principle:** No automation scripts. Just consistent pattern: create playbook → create issue manually.

---

## 📐 Implementation

### **Pattern: Playbook = Issue**

**Key Principle:** Each playbook represents one piece of work, tracked as one issue.

**When creating a playbook:**
1. Create playbook file: `Core/operations/playbooks/fabric/{stage}/{playbook.name}.md`
2. **Manually create corresponding issue** in `zephyr-backlog` project:
   - Title: `[PLAYBOOK] {playbook.name} - {playbook.title}`
   - Body includes playbook path, purpose, prerequisites, acceptance criteria
   - Labels: `type:task`, `stage:{stage}`, `playbook:{playbook.name}`
   - Milestone: Based on stage

**No automation needed** - just consistent manual process. Work is naturally scoped to playbook size.

---

### **Linking Bugs/Blockers to Playbooks**

**Current:** `issue-to-playbook-mapping.md` maps issues → playbooks

**Pattern:**
- Bug/blocker issues link to playbook via `playbook:{playbook.name}` label
- Bug issues reference playbook issue number
- Track which playbooks have blockers

---

### **Contract-Playbook-Issue Alignment**

**Structure:**
```
Contract (source.contract.yaml)
  └─ Obligation: "Endpoint catalog comprehensive"
      └─ Playbook: source.003-bootstrapEndpoints.md
          └─ Issue: [PLAYBOOK] source.003-bootstrapEndpoints
              └─ Bug: DOC-GAP-001 (if discovered)
```

**Benefits:**
- Traceability from contract → execution → issues
- Quality gates tracked at issue level
- Validation status visible

---

## 🔄 Workflow

### **When Creating New Playbook:**

1. Create playbook file: `Core/operations/playbooks/fabric/{stage}/{playbook.name}.md`
2. **Create corresponding issue in `zephyr-backlog` project:**
   - Title: `[PLAYBOOK] {playbook.name} - {playbook.title}`
   - Link to playbook file in issue body
   - Set labels: `type:task`, `stage:{stage}`, `playbook:{playbook.name}`
   - Set milestone based on stage
3. Link to contract obligation (if applicable)
4. Link to manifest activity (if applicable)

**Key Principle:** Each playbook = one piece of work = one issue. Work is naturally scoped to playbook size.

### **When Discovering Bug/Blocker:**

1. Create bug issue: `[BLOCKER-XXX] Issue Title`
2. Link to playbook: Add `playbook:{playbook.name}` label
3. Link to playbook issue: Reference playbook issue number in bug issue
4. Update `issue-to-playbook-mapping.md`

### **When Completing Playbook:**

1. Mark playbook issue as "Done"
2. Update playbook with completion evidence
3. Update contract validation status
4. Update manifest activity status

---

## 📊 Project Structure

**zephyr-backlog Project Organization:**

```
zephyr-backlog
├── Stage 1: Source
│   ├── [PLAYBOOK] source.001-createSourceNotebook
│   │   └─ Status: ✅ Done
│   ├── [PLAYBOOK] source.002-addNotebookToPipeline
│   │   └─ Status: ✅ Done
│   └── [PLAYBOOK] source.003-bootstrapEndpoints
│       └─ Status: ✅ Done
│       └─ [DOC-GAP-001] Endpoint Duplicates (Resolved)
│
├── Stage 2: Prepare
│   ├── [PLAYBOOK] prepare.000-discoverFieldMetadata
│   │   └─ Status: ⏳ Todo
│   ├── [PLAYBOOK] prepare.001-createTestData
│   │   └─ Status: 🔄 In Progress
│   │   └─ [BLOCKER-002] Folder Creation API Broken
│   │   └─ [BUG-002] Cycle Phase startDate Required
│   │   └─ [BUG-003] Release globalRelease Conflict
│   │   └─ [BUG-004] Testcase Payload Wrapper
│   │   └─ [BUG-005] Folder parentId: null
│   ├── [PLAYBOOK] prepare.002-introspectSchemas
│   │   └─ Status: ⏳ Blocked (waiting for prepare.001)
│   └── [PLAYBOOK] prepare.003-loadSchemaIntoNotebook
│       └─ Status: ⏳ Blocked (waiting for prepare.002)
```

---

## ✅ Benefits

1. **Full Traceability** - Contract → Playbook → Issue → Bug
2. **Progress Tracking** - See playbook execution status
3. **Dependency Management** - Clear blocking relationships
4. **Quality Gates** - Track validation at issue level
5. **Documentation** - Playbooks remain source of truth
6. **Automation** - Scripts can create/update issues from playbooks

---

## 🚀 Next Steps

1. ⏳ Create initial playbook issues for existing playbooks (manual)
2. ⏳ Enhance bug/blocker issues to link to playbook issues
3. ⏳ Update contract validation to reference issues
4. ⏳ Create manifest → playbook → issue mapping

**Note:** No automation scripts needed - just consistent manual process. Each playbook = one issue.

---

## 📚 References

- **Contracts:** `Data/zephyr/contracts/`
- **Playbooks:** `Core/operations/playbooks/fabric/`
- **Issue Mapping:** `Data/zephyr/docs/issue-to-playbook-mapping.md`
- **Project Config:** `Core/operations/config/projects/zephyr-backlog.yml`

