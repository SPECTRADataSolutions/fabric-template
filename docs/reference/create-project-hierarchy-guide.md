# Create Project Hierarchy Guide

> **Purpose:** Step-by-step guide for creating a SPECTRA-grade GitHub Project hierarchy  
> **Status:** ✅ Production  
> **Last Updated:** 2025-12-08

---

## 🎯 Overview

This guide documents the process for creating a GitHub Project with the SPECTRA-grade hierarchy:

```
Initiative (1 per project)
  └─ Activity: Provision
      └─ Task/Story: Provision playbook 1
      └─ Task/Story: Provision playbook 2
  └─ Activity: Discover
      └─ Task/Story: Discovery playbook 1
      └─ Task/Story: Discovery playbook 2
  └─ Activity: Source (pipeline stage)
      └─ Task/Story: source.001-createSourceNotebook
      └─ Task/Story: source.002-bootstrapAuthentication
  └─ Activity: Prepare (pipeline stage)
      └─ Task/Story: prepare.000-discoverFieldMetadata
      └─ Task/Story: prepare.001-createTestData
  └─ Activity: Extract, Clean, Transform, Refine, Analyse (pipeline stages)
  └─ Activity: Design, Build, Test, Deploy, Optimise (Solution Engine activities)
```

---

## 📋 Prerequisites

1. **GitHub App credentials** configured in `.env`:
   - `SPECTRA_APP_ID`
   - `SPECTRA_APP_INSTALLATION_ID`
   - `SPECTRA_APP_PRIVATE_KEY_PATH`

2. **Project config file** created at `Core/operations/config/projects/{project-name}.yml`:
   ```yaml
   project: {Project Name}
   owner: {GitHub Org}
   repo: {Repository Name}
   description: >
     Project description

   schemaVersion: 1
   createProject: true
   addToProject: false

   defaultLabels:
     - project:{project-name}

   labels:
     - name: type:epic
       color: 1f6feb
     - name: type:task
       color: 0e8a16
     - name: type:bug
       color: b60205
     - name: type:blocker
       color: d93f0b
     # ... stage labels, severity labels, etc.

   milestones:
     - name: Provision Complete
       description: Environment provisioned
     - name: Discover Complete
       description: Discovery complete
     # ... more milestones
   ```

3. **Token minting script** at `Data/.github/scripts/spectra_assistant_token.py`

---

## 🚀 Step-by-Step Process

### **Step 1: Create GitHub Project**

**Script:** `Core/operations/scripts/create_{project}_project.py`

```python
#!/usr/bin/env python
"""
Create {Project Name} GitHub Project.
"""

import sys
from pathlib import Path

# Add Core/operations/scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from simple_project_bootstrap import GitHub
from create_zephyr_project import get_token

def main():
    # Mint GitHub App token
    app_id = "2172220"
    installation_id = "95900295"
    key_path = Path(__file__).parent.parent.parent.parent / "Core" / "Vault" / "spectra-assistant.private-key.pem"
    
    token = get_token(app_id, installation_id, key_path)
    gh = GitHub(token)
    
    # Get organization ID
    org_login = "SPECTRADataSolutions"  # or SPECTRACoreSolutions
    q_org = "query($login:String!){ organization(login:$login){ id } }"
    org_data = gh.gql(q_org, {"login": org_login})
    org_id = org_data["data"]["organization"]["id"]
    
    # Create project
    project_name = "{Project Name}"
    q_create = "mutation($input:CreateProjectV2Input!){ createProjectV2(input:$input){ projectV2 { id title number } } }"
    variables = {"input": {"ownerId": org_id, "title": project_name}}
    
    create_data = gh.gql(q_create, variables)
    project = create_data["data"]["createProjectV2"]["projectV2"]
    
    print(f"✅ Created project: {project['title']}")
    print(f"   ID: {project['id']}")
    print(f"   Number: {project['number']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**Run:**
```bash
cd Core/operations/scripts
python create_{project}_project.py
```

**Output:**
```
✅ Created project: {Project Name}
   ID: PVT_kwH...
   Number: 5
```

---

### **Step 2: Link Project to Repository**

**Script:** `Core/operations/scripts/link_{project}_project.py`

```python
#!/usr/bin/env python
"""
Link {Project Name} Project to repository.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from simple_project_bootstrap import GitHub
from create_zephyr_project import get_token

def main():
    # Mint token
    app_id = "2172220"
    installation_id = "95900295"
    key_path = Path(__file__).parent.parent.parent.parent / "Core" / "Vault" / "spectra-assistant.private-key.pem"
    
    token = get_token(app_id, installation_id, key_path)
    gh = GitHub(token)
    
    # Get repository ID
    repo_owner = "SPECTRADataSolutions"
    repo_name = "{repo}"
    q_repo = "query($owner:String!,$repo:String!){ repository(owner:$owner,name:$repo){ id } }"
    repo_data = gh.gql(q_repo, {"owner": repo_owner, "repo": repo_name})
    repo_id = repo_data["data"]["repository"]["id"]
    
    # Link project to repository
    project_id = "PVT_kwH..."  # From Step 1 output
    q_link = "mutation($projectId:ID!,$repositoryId:ID!){ linkProjectV2ToRepository(input:{projectId:$projectId repositoryId:$repositoryId}){ clientMutationId } }"
    gh.gql(q_link, {"projectId": project_id, "repositoryId": repo_id})
    
    print(f"✅ Linked project to {repo_owner}/{repo_name}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**Run:**
```bash
cd Core/operations/scripts
python link_{project}_project.py
```

---

### **Step 3: Create Initiative Issue**

**Script:** `Core/operations/scripts/restructure_project_issues.py` (reusable)

```python
def create_initiative(gh: GitHub, owner: str, repo: str, project_id: str, project_name: str, purpose: str) -> Dict:
    """Create top-level Initiative issue."""
    title = project_name
    body = f"""
## Purpose
{purpose}

## Target Maturity
L3 - Beta

## Implementation
Data/{repo}

## Notes
Full SPECTRA pipeline implementation, aligning with Solution Engine activities and SPECTRA stages.
"""
    labels = [f"project:{repo}", "type:initiative", "priority:critical"]
    
    # Create issue
    issue_data = gh.request("POST", f"{gh.api}/repos/{owner}/{repo}/issues", {
        "title": title,
        "body": body,
        "labels": labels
    })
    
    # Add to project
    issue_id = issue_data["node_id"]
    q_add = """
    mutation($projectId:ID!,$contentId:ID!){
      addProjectV2ItemById(input:{projectId:$projectId contentId:$contentId}){
        item { id }
      }
    }
    """
    gh.gql(q_add, {"projectId": project_id, "contentId": issue_id})
    
    return issue_data
```

**Call:**
```python
initiative = create_initiative(
    gh, 
    "SPECTRADataSolutions", 
    "zephyr", 
    "PVT_kwH...", 
    "Zephyr Pipeline Development",
    "Unified test management analytics pipeline for Zephyr Enterprise."
)
print(f"✅ Created Initiative #{initiative['number']}")
```

---

### **Step 4: Create Activity Epics**

**Order (CRITICAL):**
1. **Provision** - Provision environment FIRST
2. **Discover** - Then discover requirements
3. **Source, Prepare, Extract, Clean, Transform, Refine, Analyse** - Pipeline stages
4. **Design, Build, Test, Deploy, Optimise** - Solution Engine activities

**Script:**
```python
def create_activity_epic(gh: GitHub, owner: str, repo: str, project_id: str, activity: str, description: str, initiative_id: str) -> Dict:
    """Create Activity Epic."""
    title = activity  # Just the activity name (no [ACTIVITY] prefix)
    body = f"""
## Purpose
{description}

## Dependencies
{dependencies}

## Key Outcomes
{outcomes}
"""
    labels = [f"project:{repo}", "type:epic", f"stage:{activity.lower()}"]
    
    # Create issue
    issue_data = gh.request("POST", f"{gh.api}/repos/{owner}/{repo}/issues", {
        "title": title,
        "body": body,
        "labels": labels
    })
    
    # Add to project and set parent
    issue_id = issue_data["node_id"]
    q_add = """
    mutation($projectId:ID!,$contentId:ID!){
      addProjectV2ItemById(input:{projectId:$projectId contentId:$contentId}){
        item { id }
      }
    }
    """
    gh.gql(q_add, {"projectId": project_id, "contentId": issue_id})
    
    # TODO: Set parent field to initiative_id using GraphQL
    
    return issue_data
```

**Call:**
```python
activities = [
    ("Provision", "Provision infrastructure and environment"),
    ("Discover", "Discovery and requirements gathering"),
    ("Source", "Connectivity, authentication, endpoint cataloging"),
    ("Prepare", "Schema introspection, metadata configuration, test data"),
    ("Extract", "Extract raw data from source systems"),
    ("Clean", "Standardize, deduplicate, validate data"),
    ("Transform", "Enrich and integrate data"),
    ("Refine", "Model facts/dimensions, performance structures"),
    ("Analyse", "Measures and presentation outputs"),
    ("Design", "Architecture and planning"),
    ("Build", "Implementation"),
    ("Test", "Validation and quality gates"),
    ("Deploy", "Release and deployment"),
    ("Optimise", "Performance tuning and optimization")
]

for activity, description in activities:
    epic = create_activity_epic(gh, owner, repo, project_id, activity, description, initiative_id)
    print(f"✅ Created Epic #{epic['number']}: {activity}")
```

---

### **Step 5: Create Tasks from Playbooks**

**For each playbook in `Core/operations/playbooks/fabric/{stage}/`:**

```python
def create_task_from_playbook(gh: GitHub, owner: str, repo: str, project_id: str, playbook_path: str, parent_epic_number: int) -> Dict:
    """Create Task issue from playbook."""
    # Parse playbook frontmatter
    playbook_content = Path(playbook_path).read_text()
    # Extract title, description, prerequisites, acceptance criteria
    
    title = "{Playbook Title}"  # e.g., "Bootstrap Endpoints Catalog"
    body = f"""
## Playbook
{playbook_path}

## Purpose
{purpose}

## Prerequisites
{prerequisites}

## Acceptance Criteria
{acceptance_criteria}

## Contract Obligation
{contract_obligation}
"""
    labels = [f"project:{repo}", "type:task", f"stage:{stage}", f"playbook:{playbook_name}"]
    
    # Create issue
    issue_data = gh.request("POST", f"{gh.api}/repos/{owner}/{repo}/issues", {
        "title": title,
        "body": body,
        "labels": labels
    })
    
    # Add to project and set parent
    # TODO: Set parent field to parent_epic_number
    
    return issue_data
```

---

## ✅ Verification

**Check project structure:**
```bash
# View project
open https://github.com/orgs/SPECTRADataSolutions/projects/{number}

# Verify hierarchy:
# - 1 Initiative
# - 14 Activity Epics (Provision first, then Discover, then stages, then Solution Engine activities)
# - N Tasks (one per playbook)
```

**Verify issue hierarchy:**
- Initiative is parent of all Activity Epics
- Activity Epics are parents of Tasks
- Tasks reference playbooks

---

## 📝 Key Principles

1. **Provision BEFORE Discover**
   - Provision creates the environment (Fabric workspace, GitHub repo, Discord channel)
   - Discover happens within that provisioned environment

2. **Clean Titles**
   - No "[ACTIVITY]" or "[STAGE]" prefixes
   - Just the activity name: "Provision", "Discover", "Source"
   - Type designation goes in Type field and labels

3. **Single Responsibility**
   - Each playbook = one task/issue
   - Tasks scoped to playbook size

4. **Traceability**
   - Initiative → Activity → Task → Playbook
   - Each task links to playbook
   - Each playbook links to contract obligation

5. **Solution Engine Alignment**
   - Activities align with Solution Engine lifecycle
   - Pipeline stages are also activities (when part of pipeline context)
   - Provision → Discover → Source → Prepare → Extract → Clean → Transform → Refine → Analyse → Design → Build → Test → Deploy → Optimise

---

## 🔗 Related Documentation

- `Data/zephyr/docs/project-hierarchy-spectra-grade.md` - Full hierarchy specification
- `Data/zephyr/docs/playbook-issue-integration.md` - Playbook-issue integration
- `Core/operations/config/projects/zephyr-backlog.yml` - Project config

---

**Status:** ✅ Production  
**Last Updated:** 2025-12-08

