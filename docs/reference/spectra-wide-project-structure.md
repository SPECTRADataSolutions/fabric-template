# SPECTRA-Wide GitHub Project Structure

> **Purpose:** Single unified GitHub project for all SPECTRA work (features, bugs, blockers, docs) across all domains  
> **Status:** ⚠️ **SUPERSEDED** - Using service-specific backlog projects instead (e.g., `zephyr-backlog`)  
> **Last Updated:** 2025-12-08

---

## ⚠️ Note

This document proposed a single SPECTRA-wide project. **We've moved to service-specific backlog projects** following the naming convention `{service}-backlog` (e.g., `zephyr-backlog`).

**Current Approach:**
- `Backlog` project = Universal ideas from Labs queue (`ideas.json`)
- `zephyr-backlog` project = Zephyr-specific work (bugs, blockers, tasks, features)
- `portal-backlog` project = Portal-specific work
- `foundation-backlog` project = Foundation-specific work

**See:** `Data/zephyr/docs/zephyr-backlog-project.md` for Zephyr backlog structure.

This document is kept for reference but is superseded.

---

## 🎯 Design Philosophy

**One Project, Rich Metadata** - Single source of truth for all SPECTRA work with powerful filtering:

- ✅ **Unified View** - See all work across all domains in one place
- ✅ **Rich Filtering** - Filter by domain, service, stage, type, severity, vendor
- ✅ **Cross-Domain Visibility** - Easy to see dependencies and blockers across domains
- ✅ **Flexible Views** - Create views for specific contexts (e.g., "All Zephyr Blockers", "Data Domain Features")

---

## 📋 Custom Fields

### **1. Domain** (single_select)
**Purpose:** Which SPECTRA domain owns this work

**Options:**
- Core
- Data
- Design
- Engagement
- Engineering
- Media
- Security

**Default:** None (required)

---

### **2. Service** (single_select)
**Purpose:** Which service/repository contains the work

**Options:** (dynamically populated based on domain, or comprehensive list)
- **Core:** framework, cli, operations, assistant, mcp-service, labs, portal, etc.
- **Data:** zephyr, jira, xero, unifi, fabric-sdk, etc.
- **Design:** [design services]
- **Engagement:** [engagement services]
- **Engineering:** [engineering services]
- **Media:** [media services]
- **Security:** [security services]

**Default:** None (required)

---

### **3. Stage** (single_select)
**Purpose:** SPECTRA methodology stage

**Options:**
- Source
- Prepare
- Extract
- Clean
- Transform
- Refine
- Analyse

**Default:** None (optional - only for pipeline work)

---

### **4. Type** (single_select)
**Purpose:** What kind of work is this?

**Options:**
- Feature
- Bug
- Blocker
- Documentation
- Enhancement
- Refactoring
- Technical Debt

**Default:** Feature

---

### **5. Severity** (single_select)
**Purpose:** Impact/urgency level

**Options:**
- Critical
- High
- Medium
- Low

**Default:** Medium

---

### **6. Vendor** (single_select)
**Purpose:** For external vendor issues (Zephyr API bugs, etc.)

**Options:**
- None (internal issue)
- Zephyr
- Jira
- Microsoft (Fabric/Azure)
- Railway
- GitHub
- Other

**Default:** None

---

### **7. Playbook** (text)
**Purpose:** Which playbook is this related to? (optional)

**Format:** `{stage}.{number}-{description}`  
**Example:** `prepare.001-createTestData`

**Default:** None (optional)

---

### **8. Report Status** (single_select)
**Purpose:** For vendor issues - reporting status

**Options:**
- N/A (internal issue)
- Pending Report
- Reported
- In Progress (Vendor)
- Resolved by Vendor

**Default:** N/A

---

## 📊 Project Views

### **View 1: All Work (Default)**
- **Type:** Board
- **Group By:** Domain
- **Sort By:** Severity (Critical → Low)
- **Filter:** None (all work)

---

### **View 2: Critical Blockers**
- **Type:** Table
- **Columns:** Title, Domain, Service, Stage, Vendor, Report Status
- **Filter:** `field:Type=Blocker AND field:Severity=Critical`

---

### **View 3: By Stage**
- **Type:** Board
- **Group By:** Stage
- **Sort By:** Severity
- **Filter:** `field:Stage!=null`

---

### **View 4: Vendor Issues**
- **Type:** Table
- **Columns:** Title, Domain, Service, Vendor, Report Status, Severity
- **Filter:** `field:Vendor!=None`

---

### **View 5: By Domain**
- **Type:** Board
- **Group By:** Domain
- **Sort By:** Type, then Severity
- **Filter:** None

---

### **View 6: Data Domain Pipeline Work**
- **Type:** Board
- **Group By:** Stage
- **Sort By:** Service, then Severity
- **Filter:** `field:Domain=Data AND field:Stage!=null`

---

### **View 7: Zephyr Issues**
- **Type:** Table
- **Columns:** Title, Stage, Playbook, Type, Severity, Report Status
- **Filter:** `field:Service=zephyr OR field:Vendor=Zephyr`

---

### **View 8: Pending Vendor Reports**
- **Type:** Table
- **Columns:** Title, Domain, Service, Vendor, Severity
- **Filter:** `field:Vendor!=None AND field:Report Status=Pending Report`

---

## 🔄 Workflow

### **When Creating Issue:**

1. **Set Required Fields:**
   - Domain (required)
   - Service (required)
   - Type (defaults to Feature)
   - Severity (defaults to Medium)

2. **Set Optional Fields:**
   - Stage (if pipeline work)
   - Vendor (if external issue)
   - Playbook (if playbook-related)
   - Report Status (if vendor issue)

3. **Add Labels:**
   - `domain:{domain}` (e.g., `domain:data`)
   - `service:{service}` (e.g., `service:zephyr`)
   - `type:{type}` (e.g., `type:blocker`)
   - `vendor:{vendor}` (if applicable)

---

## 📝 Example Issues

### **Example 1: Zephyr API Blocker**
- **Title:** `[BLOCKER-001] Requirement Creation API Broken`
- **Domain:** Data
- **Service:** zephyr
- **Stage:** Prepare
- **Type:** Blocker
- **Severity:** Critical
- **Vendor:** Zephyr
- **Playbook:** `prepare.001-createTestData`
- **Report Status:** Pending Report

---

### **Example 2: Feature Request**
- **Title:** `Add Star Wars Test Dataset`
- **Domain:** Core
- **Service:** labs
- **Type:** Feature
- **Severity:** Medium
- **Vendor:** None
- **Playbook:** None

---

### **Example 3: Documentation Gap**
- **Title:** `[DOC-GAP-001] Endpoint Duplicates in Catalog`
- **Domain:** Data
- **Service:** zephyr
- **Stage:** Source
- **Type:** Documentation
- **Severity:** Low
- **Vendor:** None
- **Playbook:** `source.003-bootstrapEndpoints`

---

## 🎨 Labels Strategy

**Auto-apply labels based on fields:**
- `domain:{domain}` - From Domain field
- `service:{service}` - From Service field
- `type:{type}` - From Type field
- `vendor:{vendor}` - From Vendor field (if not None)
- `stage:{stage}` - From Stage field (if set)

**Manual labels:**
- `zephyr-support` - For Zephyr vendor issues
- `api-issue` - For API-related bugs
- `blocker` - For critical blockers
- `needs-triage` - For issues needing review

---

## 🔗 Integration with Registries

**For Zephyr bugs/blockers:**
- GitHub Issue = Active tracking, assignments, discussions
- `bug-and-blocker-registry.md` = Comprehensive documentation, reporting template

**Two-way sync:**
- Create issue from registry → Add issue number to registry
- Update issue → Update registry status
- Report to vendor → Update Report Status field

---

## 📐 Project Schema Files

**Location:** `Core/operations/config/projects/schemas/spectra-wide/`

**Files:**
- `fields.json` - Custom field definitions
- `views.json` - View definitions
- `project.json` - Project metadata

---

## ✅ Benefits

1. **Single Source of Truth** - All SPECTRA work in one place
2. **Powerful Filtering** - Find exactly what you need with rich metadata
3. **Cross-Domain Visibility** - See dependencies and blockers across domains
4. **Flexible Views** - Create views for any context
5. **Vendor Tracking** - Track external issues and reporting status
6. **Stage Alignment** - Pipeline work aligned with SPECTRA methodology

---

## 🚀 Next Steps

1. ✅ Create project config: `Core/operations/config/projects/spectra-wide-backlog.yml`
2. ✅ Create schema files: `Core/operations/config/projects/schemas/spectra-wide/`
3. ✅ Update `generate_github_issues_from_registry.py` to use new fields
4. ⏳ Create GitHub project using config
5. ⏳ Set up views in GitHub project
6. ⏳ Migrate existing issues (if any) to new project structure

