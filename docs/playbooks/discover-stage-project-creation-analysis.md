# Discover Stage Project Creation Analysis

> **Question:** Should Labs Discover stage also create the project (GitHub repo, GitHub Project v2, initial structure)?

**Date:** 2025-12-05  
**Status:** Analysis

---

## Current Flow

### Labs Discover Stage (Current)
**Location:** `Core/solution-engine/src/solution_engine/stages/discover.py`

**What it does:**
1. ✅ Extracts service name from user input
2. ✅ Validates service name meets SPECTRA standards
3. ✅ Checks for duplicates in service catalog
4. ✅ Creates discover manifest
5. ✅ Outputs: service_name, problem, idea

**What it doesn't do:**
- ❌ Create GitHub repository
- ❌ Create GitHub Project v2
- ❌ Create initial project structure
- ❌ Create contract.yaml
- ❌ Create any artifacts

### Project Creation (Current)
**Location:** Manual process via playbooks

**Current flow:**
1. **setup.000** - Create initial artifacts (contract.yaml, icons)
2. **setup.001** - Create GitHub repository
3. **setup.002** - Create Fabric workspace
4. **setup.003** - Create Fabric environment
5. **setup.004** - Create Fabric lakehouse
6. **setup.005** - Create Fabric pipeline
7. **setup.006** - Create Fabric variable library

**Then:**
- Playbooks generate GitHub Project v2 (proposed)
- Design stage works with existing project

---

## Proposed: Discover Creates Project

### Option 1: Discover Stage Calls Project Creation

**Flow:**
```
Labs Discover Stage
  ↓
1. Extract & validate service name ✅
2. Check for duplicates ✅
3. **NEW: Create GitHub repository** (call setup.001)
4. **NEW: Create GitHub Project v2** (from playbooks)
5. **NEW: Create initial structure** (contract.yaml, README, etc.)
6. Create discover manifest
  ↓
Output: service_name, problem, idea, **+ project_url, project_id**
```

**Pros:**
- ✅ Immediate project structure after validation
- ✅ Design stage has actual project to work with
- ✅ Single entry point (Discover does everything)
- ✅ Automated end-to-end

**Cons:**
- ❌ Discover stage becomes heavy (does discovery + creation)
- ❌ Mixing concerns (discovery logic + project creation)
- ❌ Harder to test (requires GitHub/Fabric access)
- ❌ Can't easily skip project creation for some ideas

**Verdict:** ⚠️ **Functional but not ideal** - mixing concerns.

---

### Option 2: Discover Outputs → Automated Project Creation Step

**Flow:**
```
Labs Discover Stage
  ↓
1. Extract & validate service name ✅
2. Check for duplicates ✅
3. Create discover manifest
4. **NEW: Trigger project creation step** (separate process)
  ↓
Project Creation Step (Automatic)
  ↓
1. Read discover manifest
2. Create GitHub repository (setup.001)
3. Create GitHub Project v2 (from playbooks)
4. Create initial structure (instantiate template)
5. Commit & push
  ↓
Design Stage (now has project)
```

**Pros:**
- ✅ Separation of concerns (Discover vs Create)
- ✅ Discover stays lightweight
- ✅ Project creation can be skipped if needed
- ✅ Can test Discover independently
- ✅ Project creation can be async/background

**Cons:**
- ⚠️ Two-step process (Discover → Create → Design)
- ⚠️ Need to handle project creation failures

**Verdict:** ✅ **BETTER** - Clean separation, flexible.

---

### Option 3: Discover Orchestrates Project Creation (Recommended)

**Flow:**
```
Labs Discover Stage
  ↓
1. Extract & validate service name ✅
2. Check for duplicates ✅
3. Create discover manifest
4. **NEW: Orchestrate project creation** (delegates to project creator)
  ↓
Project Creator (Separate Module/Service)
  ↓
- Reads discover manifest
- Instantiates template (contract.yaml, structure)
- Creates GitHub repository
- Creates GitHub Project v2 (from playbooks)
- Commits initial structure
  ↓
Design Stage (has project ready)
```

**Structure:**
```
Core/solution-engine/
├── stages/
│   └── discover.py           # Lightweight, delegates project creation
├── orchestrators/
│   └── project_creator.py    # NEW: Handles all project creation
└── integrations/
    ├── github.py             # GitHub repo creation
    └── fabric.py             # Fabric workspace creation
```

**Pros:**
- ✅ Clean separation (Discover orchestrates, doesn't implement)
- ✅ Discover stays focused on discovery logic
- ✅ Project creator is reusable (can be called from elsewhere)
- ✅ Easy to test (mock project creator)
- ✅ Can skip project creation if needed
- ✅ Project creator can be enhanced independently

**Cons:**
- ⚠️ Slightly more complex architecture

**Verdict:** ✅ **BEST** - Clean architecture, reusable, testable.

---

## Recommendation: Option 3 (Discover Orchestrates)

### Implementation

**1. Discover Stage Enhancement:**
```python
# Core/solution-engine/src/solution_engine/stages/discover.py

def execute_discover(...):
    # Current discovery logic
    service_name = _extract_service_name(user_input)
    _validate_service_name(service_name)
    _check_duplicates(service_name)
    
    # Create discover manifest
    manifest.add_output("service_name", service_name)
    manifest.add_output("problem", problem)
    manifest.add_output("idea", idea)
    
    # NEW: Orchestrate project creation
    if should_create_project(manifest):
        from ..orchestrators.project_creator import create_project
        
        project_info = create_project(
            service_name=service_name,
            idea_type=manifest.get("idea_type"),  # service, feature, tool, etc.
            contract_data=manifest.get("contract_data")
        )
        
        manifest.add_output("project_url", project_info["url"])
        manifest.add_output("project_id", project_info["id"])
        manifest.add_output("github_repo_url", project_info["github_repo_url"])
```

**2. Project Creator Module:**
```python
# Core/solution-engine/src/solution_engine/orchestrators/project_creator.py

def create_project(service_name: str, idea_type: str, contract_data: dict):
    """
    Create complete project structure:
    - Instantiate template (contract.yaml, structure)
    - Create GitHub repository
    - Create GitHub Project v2 (from playbooks)
    - Commit initial structure
    """
    
    # 1. Instantiate template
    template_instantiated = instantiate_template(
        source_key=service_name,
        template_path="Core/operations/templates/fabric-project",
        output_path=f"Data/{service_name}"
    )
    
    # 2. Create GitHub repository
    repo_url = github.create_repository(
        org="SPECTRADataSolutions",
        name=service_name,
        description=contract_data.get("description")
    )
    
    # 3. Create GitHub Project v2
    project_id = github.create_project_v2(
        org="SPECTRADataSolutions",
        name=f"{service_name} Development",
        description=f"Development backlog for {service_name}",
        fields=generate_project_fields_from_playbooks(service_name)
    )
    
    # 4. Generate issues from playbooks
    issues = generate_issues_from_playbooks(
        playbooks_path=f"Data/{service_name}/docs/playbooks"
    )
    github.create_project_issues(project_id, issues)
    
    # 5. Commit & push
    git.commit_and_push(repo_url, template_instantiated)
    
    return {
        "url": repo_url,
        "id": project_id,
        "github_repo_url": repo_url
    }
```

**3. Template Instantiation:**
```python
# Core/solution-engine/src/solution_engine/orchestrators/template_instantiation.py

def instantiate_template(source_key: str, template_path: str, output_path: str):
    """
    Instantiate parameterised template for new source project.
    Uses template + contract.yaml to generate complete project structure.
    """
    # Read template
    template = load_template(template_path)
    
    # Read contract (if exists, otherwise generate from discover outputs)
    contract = load_or_generate_contract(source_key)
    
    # Instantiate all template files
    for template_file in template.files:
        instantiated_content = template_file.render(contract)
        write_file(output_path, template_file.path, instantiated_content)
    
    return output_path
```

---

## Where Should This Live?

### Option A: In Solution Engine (Recommended)
**Location:** `Core/solution-engine/src/solution_engine/orchestrators/project_creator.py`

**Why:**
- ✅ Solution engine already orchestrates stages
- ✅ Project creation is part of service lifecycle
- ✅ Integrates with Discover stage naturally
- ✅ Reusable across different idea types

### Option B: Separate Service
**Location:** `Core/project-factory/` (new service)

**Why:**
- ✅ Separation of concerns
- ✅ Can be called from anywhere
- ✅ Independent versioning

**Why not:**
- ❌ Overkill for now (can evolve later)
- ❌ Adds complexity

### Option C: In Labs Engine
**Location:** `Core/labs/engine/project_creator.py`

**Why:**
- ✅ Labs already processes ideas
- ✅ Natural fit for idea → project flow

**Why not:**
- ❌ Labs is queue processor, not project creator
- ❌ Solution engine is the execution layer

**Verdict:** ✅ **Option A (Solution Engine)** - Natural fit, already orchestrates.

---

## Benefits of Discover Creating Project

### 1. Immediate Feedback
- User says "create zephyr pipeline"
- Discover validates idea
- Project created immediately
- User can see progress right away

### 2. Design Stage Ready
- Design stage has actual project to work with
- Can generate architecture in real repo
- Can create real issues in GitHub Project v2

### 3. End-to-End Automation
- Idea → Project → Design → Build → Deploy
- No manual steps between stages
- Fully automated pipeline

### 4. Playbook-Driven
- Project creation uses playbooks
- GitHub Project v2 generated from playbooks
- Issues created from playbook definitions
- Everything traceable

---

## Implementation Plan

### Phase 1: Project Creator Module
1. Create `orchestrators/project_creator.py`
2. Implement template instantiation
3. Implement GitHub repository creation
4. Test with dummy service

### Phase 2: Discover Integration
1. Enhance Discover stage to orchestrate project creation
2. Add project creation flags (when to create, when to skip)
3. Handle project creation failures gracefully

### Phase 3: Playbook Integration
1. Generate GitHub Project v2 from playbooks
2. Generate issues from playbook definitions
3. Link playbooks to GitHub Project v2 issues

### Phase 4: Template Instantiation
1. Build template instantiation engine
2. Test with Zephyr template
3. Validate instantiated projects

---

## Conclusion

**Recommendation:** ✅ **Discover Should Orchestrate Project Creation**

**Best Place:** `Core/solution-engine/src/solution_engine/orchestrators/project_creator.py`

**Benefits:**
- ✅ Immediate project structure after validation
- ✅ Design stage has real project to work with
- ✅ End-to-end automation
- ✅ Playbook-driven (GitHub Project v2 + issues)
- ✅ Clean separation (Discover orchestrates, doesn't implement)

**Implementation:**
- Discover stage calls project creator
- Project creator handles all project creation
- Template instantiation creates structure
- Playbooks generate GitHub Project v2 + issues

**Status:** Ready to implement

---

**Next Steps:**
1. Review and approve approach
2. Build project creator module
3. Enhance Discover stage
4. Test with Zephyr as proof of concept




