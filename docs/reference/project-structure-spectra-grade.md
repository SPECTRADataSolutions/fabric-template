# SPECTRA-Grade Project Structure

> **Purpose:** Define the SPECTRA-grade approach for structuring GitHub Projects to align with Solution Engine methodology  
> **Status:** 🟡 Superseded by `project-hierarchy-spectra-grade.md`  
> **Last Updated:** 2025-12-08  
> **See:** `project-hierarchy-spectra-grade.md` for the complete hierarchy specification

---

## 🎯 Design Philosophy

**Hierarchical Structure:**
```
Initiative (1 per project)
  └─ Epic: Discover (stage epic)
      └─ Task: Contract Obligation 1
      └─ Task: Contract Obligation 2
  └─ Epic: Source (stage epic)
      └─ Task: Playbook Task
      └─ Bug/Blocker (if discovered)
  └─ Epic: Design (stage epic)
      └─ Task: Playbook Task
  └─ Epic: Build (stage epic)
      └─ Task: Playbook Task
  └─ Epic: Test (stage epic)
      └─ Task: Playbook Task
  └─ Epic: Deploy (stage epic)
      └─ Task: Playbook Task
  └─ Epic: Optimise (stage epic)
      └─ Task: Playbook Task
```

**Key Principles:**
1. **One Initiative Per Project** - Every project (except Backlog) has a single top-level initiative
2. **Stage Epics** - Each SPECTRA stage becomes an epic under the initiative
3. **Contract-Driven Tasks** - Tasks derive from contract obligations and playbooks
4. **Solution Engine Integration** - Project structure mirrors Solution Engine stages
5. **Traceability** - Clear path from Initiative → Epic → Task → Contract/Playbook

---

## 📋 Project Structure

### **1. Initiative (Top Level)**

**Purpose:** Single high-level initiative representing the entire project

**When Created:**
- When an idea is upgraded from Labs queue to a project
- Contains all high-level detail for the project

**Fields:**
- **Title:** Project name (e.g., "Zephyr Pipeline Development")
- **Type:** Initiative
- **Priority:** Based on idea priority
- **Status:** Todo → In Progress → Done
- **Body:** 
  - Purpose from idea
  - Target maturity level
  - Implementation location
  - Notes from idea

**Example:**
```
Title: Zephyr Pipeline Development
Type: Initiative
Priority: Critical
Status: In Progress
Body:
  Purpose: Unified test management analytics pipeline for Zephyr Enterprise
  Target Maturity: L3 - Beta
  Implementation: Data/zephyr
  Notes: Full SPECTRA pipeline implementation
```

---

### **2. Stage Epics**

**Purpose:** Each SPECTRA stage becomes an epic under the initiative

**Epics:**
1. **Discover** - Discovery and requirements gathering
2. **Source** - Connectivity, authentication, endpoint cataloging
3. **Design** - Architecture and planning
4. **Build** - Implementation
5. **Test** - Validation
6. **Deploy** - Release
7. **Optimise** - Performance tuning

**Fields:**
- **Title:** `[STAGE] {Stage Name}` (e.g., "[STAGE] Source")
- **Type:** Epic
- **Parent:** Initiative
- **Status:** Todo → In Progress → Done
- **Body:**
  - Stage purpose
  - Contract reference
  - Key obligations
  - Dependencies

**Example:**
```
Title: [STAGE] Source
Type: Epic
Parent: Zephyr Pipeline Development (Initiative)
Status: In Progress
Body:
  Purpose: Catalog all Zephyr API endpoints, authenticate, validate access
  Contract: Data/zephyr/contracts/source.contract.yaml
  Obligations:
    - Auth succeeds against Zephyr base URL
    - Endpoint catalog comprehensive
    - Hierarchical access validated
  Dependencies: None (first stage)
```

---

### **3. Tasks (Contract Obligations & Playbooks)**

**Purpose:** Individual work items derived from contracts and playbooks

**Types:**
- **Task** - Playbook execution, contract obligation fulfillment
- **Bug** - API issues, bugs discovered during execution
- **Feature** - New capabilities

**Fields:**
- **Title:** Descriptive title (no type prefix)
- **Type:** Task / Bug / Feature
- **Priority:** Critical / High / Medium / Low
- **Parent:** Stage Epic
- **Status:** Todo → In Progress → Done
- **Body:**
  - Playbook reference (if applicable)
  - Contract obligation (if applicable)
  - Acceptance criteria
  - Dependencies

**Example:**
```
Title: Bootstrap Endpoints Catalog
Type: Task
Priority: Critical
Parent: [STAGE] Source (Epic)
Status: Done
Body:
  Playbook: source.003-bootstrapEndpoints.md
  Contract Obligation: "Endpoint catalog comprehensive"
  Acceptance Criteria:
    - endpoints.json bootstrapped to Fabric Files
    - source.endpoints table populated
    - Zero duplicates
  Dependencies: source.001, source.002
```

---

### **4. Bugs/Blockers (Child Issues)**

**Purpose:** Issues discovered during playbook execution

**Fields:**
- **Title:** Descriptive title (no type prefix)
- **Type:** Bug
- **Priority:** Based on severity (Critical → High → Medium → Low)
- **Parent:** Stage Epic (where discovered)
- **Status:** Todo → In Progress → Done
- **Body:**
  - Registry ID
  - Playbook where discovered
  - Workaround
  - Test evidence
  - Report status

**Example:**
```
Title: Requirement Creation API Broken
Type: Bug
Priority: High
Parent: [STAGE] Prepare (Epic)
Status: Todo
Body:
  Registry ID: BLOCKER-001
  Discovered in: prepare.004-create-requirements.md
  Issue: POST /requirement/ returns HTTP 500
  Workaround: Create manually in UI
  Report Status: Pending
```

---

## 🔄 Workflow: Idea → Project

### **Step 1: Idea in Labs Queue**

**Location:** `Core/labs/queue/ideas.json`

**Fields:**
- id, name, type, purpose, priority, status
- target_maturity, implementation_location

---

### **Step 2: Upgrade Idea to Project**

**Trigger:** Idea status changes to "ready-to-implement" or explicit upgrade

**Actions:**
1. Create GitHub Project (if not exists)
2. Create Initiative issue:
   - Title: Idea name
   - Type: Initiative
   - Body: Purpose, maturity, location, notes
3. Create Stage Epics:
   - Discover, Source, Design, Build, Test, Deploy, Optimise
   - All start as "Todo"
4. Populate Discover Epic:
   - Tasks from Discover contract obligations
   - Tasks from Solution Engine discover stage

---

### **Step 3: Discover Stage**

**Epic:** [STAGE] Discover

**Tasks Derived From:**
- Solution Engine discover stage activities
- Discover contract obligations
- Project-specific discovery needs

**Example Tasks:**
- Define project scope
- Identify stakeholders
- Gather requirements
- Create project structure
- Set up repository

---

### **Step 4: Source Stage**

**Epic:** [STAGE] Source

**Tasks Derived From:**
- Source contract obligations
- Source playbooks
- Solution Engine source stage activities

**Example Tasks:**
- Create source notebook
- Bootstrap endpoints catalog
- Validate authentication
- Test endpoint access

---

### **Step 5: Subsequent Stages**

**Pattern:** Each stage follows the same pattern:
1. Epic created under Initiative
2. Tasks derived from contract obligations
3. Playbooks executed as tasks
4. Bugs/blockers created as child issues when discovered

---

## 🔗 Solution Engine Integration

### **Contract → Epic → Task Mapping**

**Structure:**
```
Contract (source.contract.yaml)
  └─ Obligation: "Endpoint catalog comprehensive"
      └─ Epic: [STAGE] Source
          └─ Task: Bootstrap Endpoints Catalog
              └─ Playbook: source.003-bootstrapEndpoints.md
```

### **Manifest → Project Status**

**Activities in manifest map to tasks:**
- Each activity → Task issue
- Activity status → Task status
- Activity dependencies → Task dependencies

---

## 📊 GitHub Project Fields

### **Custom Fields (Required)**

1. **Type** (Single Select)
   - Initiative
   - Epic
   - Task
   - Bug
   - Feature

2. **Priority** (Single Select)
   - Critical
   - High
   - Medium
   - Low

3. **Stage** (Single Select)
   - Discover
   - Source
   - Design
   - Build
   - Test
   - Deploy
   - Optimise

4. **Parent** (Text)
   - Initiative ID or Epic ID

5. **Contract** (Text)
   - Path to contract file (e.g., `source.contract.yaml`)

6. **Playbook** (Text)
   - Path to playbook file (e.g., `source.003-bootstrapEndpoints.md`)

---

## 🚀 Implementation Steps

### **Phase 1: Update Existing Issues**

1. Remove type prefixes from titles (`[BLOCKER]`, `[BUG]`, etc.)
2. Set Type field (Bug/Feature/Task)
3. Set Priority field (from Severity)
4. Create Initiative issue: "Zephyr Pipeline Development"
5. Create Stage Epics:
   - [STAGE] Discover
   - [STAGE] Source
   - [STAGE] Design
   - [STAGE] Build
   - [STAGE] Test
   - [STAGE] Deploy
   - [STAGE] Optimise
6. Set Parent field for all existing issues to appropriate Stage Epic

### **Phase 2: Update Issue Creation Script**

1. Parse title (remove type prefix like `[BLOCKER]`, `[BUG]`)
2. Set Type field from registry (Bug/Feature/Task)
3. Set Priority from Severity (Critical/High/Medium/Low)
4. Set Parent to appropriate Stage Epic (based on playbook stage)
5. Set Stage field (from playbook mapping)

### **Phase 3: Solution Engine Integration**

1. Create script to generate Initiative + Epics from idea:
   - Read idea from `Core/labs/queue/ideas.json`
   - Create Initiative issue with idea details
   - Create 7 Stage Epics (Discover, Source, Design, Build, Test, Deploy, Optimise)
2. Create script to generate Tasks from contract obligations:
   - Parse contract YAML (e.g., `source.contract.yaml`)
   - Create Task for each obligation
   - Link to appropriate Stage Epic
   - Reference playbook if exists
3. Create script to sync manifest activities to tasks:
   - Read manifest JSON
   - Map activities to tasks
   - Update task status from manifest
   - Track dependencies

### **Phase 4: Discover Stage Epic Population**

**When:** Idea upgraded to project

**Actions:**
1. Create Discover Epic
2. Populate with tasks from:
   - Solution Engine discover stage activities
   - Discover contract obligations (if exists)
   - Project-specific discovery needs:
     - Define project scope
     - Identify stakeholders
     - Gather requirements
     - Create project structure
     - Set up repository
     - Define contracts
     - Create manifests

**Example Discover Tasks:**
- Define Zephyr pipeline scope
- Identify Zephyr API capabilities
- Gather Zephyr requirements
- Create `Data/zephyr` repository structure
- Define `source.contract.yaml`
- Create `source.manifest.yaml`
- Set up Fabric workspace
- Bootstrap GitHub project

---

## ✅ Benefits

1. **Clear Hierarchy** - Initiative → Epic → Task structure
2. **Stage Alignment** - Epics align with SPECTRA stages
3. **Contract Traceability** - Tasks link to contract obligations
4. **Solution Engine Integration** - Project mirrors Solution Engine flow
5. **SPECTRA-Grade** - Structured, traceable, methodology-aligned

---

**Status:** 🟡 Proposed  
**Next Steps:** Review and refine structure, implement Phase 1 updates

