# Zephyr Backlog Project

> **Purpose:** GitHub Project for tracking all Zephyr pipeline work (bugs, blockers, features, tasks)  
> **Project Name:** `zephyr-backlog`  
> **Owner:** SPECTRADataSolutions  
> **Repository:** zephyr  
> **Last Updated:** 2025-12-08

---

## 🎯 Purpose

The `zephyr-backlog` project tracks all Zephyr-specific work:

- **Bugs** - API issues, payload problems, endpoint failures
- **Blockers** - Critical issues preventing progress
- **Features** - New capabilities for the Zephyr pipeline
- **Tasks** - Implementation work across all 7 SPECTRA stages
- **Documentation** - Gaps, improvements, clarifications

**Separation of Concerns:**
- `Backlog` project = Universal ideas from Labs queue (`ideas.json`)
- `zephyr-backlog` project = Zephyr-specific work (bugs, blockers, tasks, features)

---

## 📋 Project Configuration

**Config File:** `Core/operations/config/projects/zephyr-backlog.yml`

**Labels:**
- `project:zephyr` - All Zephyr work
- `type:bug`, `type:blocker`, `type:feature`, `type:documentation`, etc.
- `stage:source`, `stage:prepare`, `stage:extract`, etc.
- `severity:critical`, `severity:high`, `severity:medium`, `severity:low`
- `vendor:zephyr` - For Zephyr API issues
- `api-issue`, `zephyr-support`, `needs-triage`

**Milestones:**
- Source Complete
- Prepare In Progress
- Extract Planned
- Clean Planned
- Transform Planned
- Refine Planned
- Analyse Planned

---

## 🔄 Workflow

### **Creating Issues from Bug Registry**

Use `Data/zephyr/scripts/generate_github_issues_from_registry.py`:

```bash
cd Data/zephyr
python scripts/generate_github_issues_from_registry.py --output-dir issues
```

This generates GitHub issue markdown files from `docs/bug-and-blocker-registry.md`.

### **Manual Issue Creation**

1. Create issue in `SPECTRADataSolutions/zephyr` repository
2. Add to `zephyr-backlog` project
3. Set labels (type, stage, severity, vendor)
4. Set milestone (if applicable)
5. Link to playbook if discovered during playbook execution

---

## 📊 Issue Structure

### **Bug/Blocker Issues**

**Title Format:** `[BLOCKER/BUG/DOC-GAP-XXX] Issue Title`

**Labels:**
- `project:zephyr`
- `type:bug` or `type:blocker`
- `stage:{stage}` (e.g., `stage:prepare`)
- `severity:{severity}` (e.g., `severity:critical`)
- `vendor:zephyr` (if Zephyr API issue)
- `api-issue`, `zephyr-support`

**Body Includes:**
- Registry ID
- Type, Stage, Playbooks
- Severity, Status
- Description
- Workaround (if available)
- Test Evidence
- Related Documentation

---

## 🔗 Integration

**Bug Registry:** `docs/bug-and-blocker-registry.md` - Comprehensive documentation  
**Issue Mapping:** `docs/issue-to-playbook-mapping.md` - Maps issues to playbooks  
**Issue Generation:** `scripts/generate_github_issues_from_registry.py` - Auto-generates issues

**Two-Way Sync:**
- GitHub Issues = Active tracking, assignments, discussions
- Bug Registry = Comprehensive documentation, reporting template

---

## 📐 Naming Convention

**Pattern:** `{service}-backlog`

**Examples:**
- `zephyr-backlog` ✅
- `jira-backlog` ✅
- `portal-backlog` ✅
- `foundation-backlog` ✅

**Benefits:**
- Clear separation of concerns
- Service-specific tracking
- Consistent naming across SPECTRA
- Easy to discover and manage

---

## ✅ Benefits

1. **Focused Tracking** - All Zephyr work in one place
2. **Clear Labels** - Easy filtering by type, stage, severity
3. **Milestone Alignment** - Track progress by SPECTRA stage
4. **Vendor Issues** - Track Zephyr API bugs separately
5. **Playbook Integration** - Link issues to specific playbooks

---

## 🚀 Next Steps

1. ✅ Create project config: `Core/operations/config/projects/zephyr-backlog.yml`
2. ✅ Update issue generation script
3. ⏳ Create GitHub project using config
4. ⏳ Generate initial issues from bug registry
5. ⏳ Set up views (by stage, by type, critical blockers, etc.)

