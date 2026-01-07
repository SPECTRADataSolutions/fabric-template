# SPECTRA-Grade Project Hierarchy

> **Purpose:** Define the complete hierarchy for SPECTRA projects: Initiative → Activities → Playbooks/Tasks  
> **Status:** 🟡 Proposed  
> **Last Updated:** 2025-12-08

---

## 🎯 Design Philosophy

**Two Planes of Stages:**
1. **Solution Engine Activities** - Lifecycle activities (Discover, Provision, Design, Build, Test, Deploy, Optimise)
2. **Pipeline Stages** - Data pipeline stages (Source, Prepare, Extract, Clean, Transform, Refine, Analyse)

**Key Insight:** A "stage" is only a stage when it's part of a pipeline. Before that, it's an "activity".

**Hierarchy:**
```
Initiative (1 per project)
  └─ Activity: Provision (FIRST - create environment)
      └─ Task/Story: Provision Fabric Workspace
      └─ Task/Story: Provision GitHub Repo
      └─ Task/Story: Provision Discord Channel
  └─ Activity: Discover (SECOND - discover within provisioned environment)
      └─ Task/Story: Discovery Playbook 1
      └─ Task/Story: Discovery Playbook 2
  └─ Activity: Source (pipeline stage)
      └─ Task/Story: source.001-createSourceNotebook
      └─ Task/Story: source.002-bootstrapAuthentication
      └─ Task/Story: source.003-bootstrapEndpoints
  └─ Activity: Prepare (pipeline stage)
      └─ Task/Story: prepare.000-discoverFieldMetadata
      └─ Task/Story: prepare.001-createTestData
      └─ Task/Story: prepare.002-introspectSchemas
  └─ Activity: Extract (pipeline stage)
      └─ Task/Story: extract.001-...
  └─ Activity: Clean, Transform, Refine, Analyse (pipeline stages)
  └─ Activity: Design, Build, Test, Deploy, Optimise (Solution Engine activities)
```

---

## 🔄 Workflow: Idea → Project

### **Step 1: Idea in Labs Queue**

**Location:** `Core/labs/queue/ideas.json`

**Process:**
1. User discusses idea with Cursor AI
2. AI saves idea to `ideas.json`
3. Automatic sync to Backlog project (GitHub)

**Fields:**
- id, name, type, purpose, priority, status
- target_maturity, implementation_location, notes

---

### **Step 2: Select Idea & Scaffold Project**

**Trigger:** User selects idea from Backlog (highest priority/most impactful)

**Actions:**
1. Create GitHub Project (if not exists)
2. Create Initiative issue (see below)
3. Create Activity Epics (see below)
4. Populate Discover Activity with tasks

---

### **Step 3: Initiative (Top Level)**

**Purpose:** Single high-level initiative representing the entire project

**When Created:** When idea is scaffolded into project

**Source:** Idea details from `ideas.json`

**Fields:**
- **Title:** Idea name (e.g., "Zephyr Pipeline Development")
- **Type:** Initiative
- **Priority:** From idea priority
- **Status:** Todo → In Progress → Done
- **Body:**
  - Purpose (from idea)
  - Problem statement (what problem are we solving?)
  - Target maturity level (from idea)
  - Implementation location (from idea)
  - Notes (from idea)
  - Solution Engine contract reference

**Example:**
```
Title: Zephyr Pipeline Development
Type: Initiative
Priority: Critical
Status: In Progress
Body:
  ## Purpose
  Unified test management analytics pipeline for Zephyr Enterprise
  
  ## Problem Statement
  Need comprehensive analytics and reporting for Zephyr test management data
  
  ## Target Maturity
  L3 - Beta
  
  ## Implementation Location
  Data/zephyr
  
  ## Solution Engine Contract
  See: Data/zephyr/contracts/ (as they are created)
```

---

### **Step 4: Activities (Children of Initiative)**

**Purpose:** Major work areas - both Solution Engine activities and Pipeline stages

**Types:**
1. **Solution Engine Activities:**
   - Discover
   - Provision
   - Design
   - Build
   - Test
   - Deploy
   - Optimise

2. **Pipeline Stages (become activities):**
   - Source
   - Prepare
   - Extract
   - Clean
   - Transform
   - Refine
   - Analyse

**Fields:**
- **Title:** Activity name (e.g., "Discover", "Source", "Provision")
- **Type:** Epic
- **Parent:** Initiative
- **Status:** Todo → In Progress → Done
- **Body:**
  - Activity purpose
  - Contract reference (if exists)
  - Key obligations/outcomes
  - Dependencies
  - Manifest reference (if exists)

**Example:**
```
Title: Discover
Type: Epic
Parent: Zephyr Pipeline Development (Initiative)
Status: In Progress
Body:
  ## Purpose
  Discovery and requirements gathering. Define project scope, identify stakeholders,
  gather requirements, create project structure, set up repository, define contracts.
  
  ## Contract
  See: Solution Engine Discover stage contract
  
  ## Key Outcomes
  - Project scope defined
  - Requirements gathered
  - Contracts defined
  - Repository structure created
  
  ## Dependencies
  None (first activity)
```

---

### **Step 5: Playbooks/Tasks (Children of Activities)**

**Purpose:** Individual work items - each playbook becomes a task/story

**Types:**
- **Task** - Playbook execution
- **Story** - User story for playbook
- **Bug** - Issues discovered during playbook execution

**Fields:**
- **Title:** Playbook name (e.g., "Bootstrap Endpoints Catalog")
- **Type:** Task / Story / Bug
- **Priority:** Critical / High / Medium / Low
- **Parent:** Activity Epic
- **Status:** Todo → In Progress → Done
- **Body:**
  - Playbook reference
  - Contract obligation (if applicable)
  - Acceptance criteria
  - Dependencies
  - PR link (when created)

**Workflow:**
1. Issue created for playbook
2. Check out issue in Cursor
3. Work on single issue
4. Create PR from issue
5. PR carries out the work
6. PR merged → Issue closed

**Example:**
```
Title: Bootstrap Endpoints Catalog
Type: Task
Priority: Critical
Parent: Source (Epic)
Status: In Progress
Body:
  ## Playbook
  source.003-bootstrapEndpoints.md
  
  ## Contract Obligation
  "Endpoint catalog comprehensive"
  
  ## Acceptance Criteria
  - endpoints.json bootstrapped to Fabric Files
  - source.endpoints table populated
  - Zero duplicates
  - All endpoints validated
  
  ## Dependencies
  - source.001-createSourceNotebook (done)
  - source.002-bootstrapAuthentication (done)
  
  ## PR
  #123 - Bootstrap endpoints catalog
```

---

## 🔄 Activity Flow

### **Discover Activity**

**Purpose:** Discovery and requirements gathering

**Tasks:**
- Define project scope
- Identify stakeholders
- Gather requirements
- Create project structure
- Define contracts
- Create manifests

**Contract:** Solution Engine Discover stage contract

**Manifest:** Created during discovery

---

### **Provision Activity**

**Purpose:** Provision infrastructure and environment

**Tasks:**
- Provision Fabric workspace
- Provision GitHub repo
- Provision Discord channel
- Set up CI/CD
- Configure secrets
- Bootstrap project structure

**Dependencies:** Discover activity complete

---

### **Source Activity (Pipeline Stage)**

**Purpose:** Connectivity, authentication, endpoint cataloging

**Tasks:**
- source.001-createSourceNotebook
- source.002-bootstrapAuthentication
- source.003-bootstrapEndpoints

**Contract:** `source.contract.yaml`

**Manifest:** `source.manifest.yaml`

**Dependencies:** Discover activity complete

---

### **Prepare Activity (Pipeline Stage)**

**Purpose:** Schema introspection, test data creation

**Tasks:**
- prepare.000-discoverFieldMetadata
- prepare.001-createTestData
- prepare.002-introspectSchemas
- prepare.003-loadSchemaIntoNotebook

**Contract:** `prepare.contract.yaml` (future)

**Manifest:** `prepare.manifest.yaml` (future)

**Dependencies:** Source activity complete

---

### **Subsequent Activities**

**Pattern:** Each activity follows the same pattern:
1. Activity Epic created under Initiative
2. Tasks derived from playbooks
3. Each task creates a PR
4. PR merged → Task closed
5. Activity complete → Next activity

---

## 🔗 Solution Engine Integration

### **Contract → Activity → Task Mapping**

**Structure:**
```
Contract (source.contract.yaml)
  └─ Obligation: "Endpoint catalog comprehensive"
      └─ Activity: [ACTIVITY] Source
          └─ Task: Bootstrap Endpoints Catalog
              └─ Playbook: source.003-bootstrapEndpoints.md
              └─ PR: #123
```

### **Manifest → Task Status**

**Activities in manifest map to tasks:**
- Each activity → Task issue
- Activity status → Task status
- Activity dependencies → Task dependencies

---

## 📊 GitHub Project Fields

### **Custom Fields (Required)**

1. **Type** (Single Select)
   - Initiative
   - Epic (for Activities)
   - Task
   - Story
   - Bug
   - Feature

2. **Priority** (Single Select)
   - Critical
   - High
   - Medium
   - Low

3. **Activity** (Single Select)
   - Discover
   - Provision
   - Source
   - Prepare
   - Extract
   - Clean
   - Transform
   - Refine
   - Analyse
   - Design
   - Build
   - Test
   - Deploy
   - Optimise

4. **Parent** (Text)
   - Initiative ID or Activity Epic ID

5. **Contract** (Text)
   - Path to contract file (e.g., `source.contract.yaml`)

6. **Playbook** (Text)
   - Path to playbook file (e.g., `source.003-bootstrapEndpoints.md`)

7. **PR** (Text)
   - PR number or URL (when created)

---

## 🚀 Implementation Steps

### **Phase 1: Update Project Structure**

1. Rename "Stage Epics" to "Activity Epics"
2. Add Provision Activity Epic
3. Update existing issues to use Activity hierarchy
4. Link issues to Activity Epics as children

### **Phase 2: Idea → Project Scaffolding**

1. Create script to scaffold project from idea:
   - Read idea from `ideas.json`
   - Create Initiative issue
   - Create Activity Epics (Discover, Provision, Source, Prepare, etc.)
   - Populate Discover Activity with tasks

### **Phase 3: Playbook → Task Automation**

1. Update playbook creation process:
   - When playbook created → Create Task issue
   - Link to appropriate Activity Epic
   - Set contract/playbook references

2. Update issue creation script:
   - Remove type prefixes
   - Set Type field
   - Set Priority field
   - Set Parent to Activity Epic
   - Set Activity field

### **Phase 4: PR Integration**

1. Create script to link PRs to tasks:
   - When PR created from issue → Update PR field
   - When PR merged → Close issue
   - Update Activity Epic status

---

## ✅ Benefits

1. **Clear Hierarchy** - Initiative → Activity → Task structure
2. **Solution Engine Alignment** - Activities align with Solution Engine
3. **Pipeline Integration** - Pipeline stages become activities
4. **Contract Traceability** - Tasks link to contract obligations
5. **Playbook Integration** - Each playbook = one task = one PR
6. **SPECTRA-Grade** - Structured, traceable, methodology-aligned

---

**Status:** 🟡 Proposed  
**Next Steps:** Review and refine structure, implement Phase 1 updates

