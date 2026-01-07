# Activity-Based Architecture

> **Vision:** Define each activity so it can be invoked alone, then orchestrate them as we please.

**Status:** Design  
**Date:** 2025-12-05

---

## 🎯 Core Principle

**Activities are standalone, composable units** - not tied to any orchestrator.

- ✅ Each activity can be invoked independently
- ✅ Activities are composable (can be chained)
- ✅ Orchestration is separate (CLI, workflows, AI agents, playbooks)
- ✅ Activities are testable in isolation
- ✅ Activities are reusable across contexts

---

## 🏗️ Architecture

### Activity Definition

Each activity is:
1. **Standalone executable** - Can be invoked directly
2. **Self-contained** - Has inputs, outputs, config
3. **Idempotent** - Can be run multiple times safely
4. **Testable** - Can be tested independently
5. **Composable** - Can be chained with other activities

### Activity Structure

```
Core/activities/
├── discover/
│   ├── validate-idea/
│   │   ├── __init__.py
│   │   ├── activity.py          # Main activity logic
│   │   ├── cli.py               # CLI entry point
│   │   └── tests/
│   ├── create-project/
│   │   ├── __init__.py
│   │   ├── activity.py
│   │   ├── cli.py
│   │   └── tests/
│   └── ...
├── source/
│   ├── discover-endpoints/
│   ├── probe-api/
│   ├── build-contract/
│   ├── ingest-projects/
│   └── ...
├── prepare/
│   ├── normalise-parameters/
│   ├── generate-mcp-server/
│   └── ...
└── ...
```

### Activity Interface

```python
# Core/activities/base.py

from typing import Dict, Any, Optional
from pathlib import Path

class Activity:
    """Base class for all SPECTRA activities."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.inputs = {}
        self.outputs = {}
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the activity.
        
        Args:
            inputs: Activity inputs (from upstream activities or files)
            
        Returns:
            Activity outputs (to downstream activities or files)
        """
        raise NotImplementedError
    
    def validate(self) -> bool:
        """Validate activity configuration."""
        raise NotImplementedError
    
    def get_dependencies(self) -> list[str]:
        """Get list of activity IDs this activity depends on."""
        return self.config.get("dependencies", [])
```

### Example Activity

```python
# Core/activities/discover/create-project/activity.py

from pathlib import Path
from typing import Dict, Any
from ..base import Activity
from ...integrations.github import create_repository
from ...integrations.project_v2 import create_project_v2
from ...templates import instantiate_template

class CreateProjectActivity(Activity):
    """Create complete project structure: repo, Project v2, initial files."""
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        service_name = inputs["service_name"]
        idea_type = inputs.get("idea_type", "service")
        contract_data = inputs.get("contract_data", {})
        
        # 1. Instantiate template
        project_path = instantiate_template(
            source_key=service_name,
            template_path="Core/operations/templates/fabric-project",
            contract_data=contract_data
        )
        
        # 2. Create GitHub repository
        repo_url = create_repository(
            org="SPECTRADataSolutions",
            name=service_name,
            description=contract_data.get("description", f"{service_name} pipeline")
        )
        
        # 3. Create GitHub Project v2
        project_id = create_project_v2(
            org="SPECTRADataSolutions",
            name=f"{service_name} Development",
            description=f"Development backlog for {service_name}"
        )
        
        # 4. Generate issues from playbooks
        playbooks_path = Path(project_path) / "docs" / "playbooks"
        issues = self._generate_issues_from_playbooks(playbooks_path)
        self._create_project_issues(project_id, issues)
        
        # 5. Commit & push
        self._commit_and_push(repo_url, project_path)
        
        return {
            "project_path": str(project_path),
            "repo_url": repo_url,
            "project_id": project_id,
            "status": "created"
        }
```

### Activity CLI

```python
# Core/activities/discover/create-project/cli.py

import click
import json
from pathlib import Path
from .activity import CreateProjectActivity

@click.command()
@click.option("--service-name", required=True, help="Service name (kebab-case)")
@click.option("--idea-type", default="service", help="Idea type (service, feature, tool)")
@click.option("--contract-data", type=click.Path(exists=True), help="Path to contract data JSON")
@click.option("--output", type=click.Path(), help="Output file for activity results")
def main(service_name: str, idea_type: str, contract_data: str, output: str):
    """Create complete project structure."""
    
    # Load contract data if provided
    inputs = {"service_name": service_name, "idea_type": idea_type}
    if contract_data:
        with open(contract_data) as f:
            inputs["contract_data"] = json.load(f)
    
    # Execute activity
    config = {}  # Activity config (can come from file, env, etc.)
    activity = CreateProjectActivity(config)
    results = activity.execute(inputs)
    
    # Output results
    if output:
        with open(output, "w") as f:
            json.dump(results, f, indent=2)
    else:
        click.echo(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
```

---

## 🔧 Invocation Methods

### 1. Direct CLI Invocation

```bash
# Invoke activity directly
python -m activities.discover.create-project \
  --service-name zephyr \
  --idea-type service \
  --contract-data contract.json \
  --output results.json
```

### 2. Python Module Invocation

```python
from activities.discover.create_project import CreateProjectActivity

activity = CreateProjectActivity(config={})
results = activity.execute({
    "service_name": "zephyr",
    "idea_type": "service",
    "contract_data": {...}
})
```

### 3. Playbook-Driven Orchestration

```yaml
# Core/operations/playbooks/fabric/0-setup/setup.001-create-project.md

activity:
  id: "create-project"
  module: "activities.discover.create_project"
  config: {}
  
  inputs:
    service_name: "{{ sourceKey }}"
    idea_type: "service"
    contract_data: "{{ contract.yaml }}"
  
  outputs:
    repo_url: "{{ repo_url }}"
    project_id: "{{ project_id }}"
```

### 4. Manifest-Driven Orchestration

```json
{
  "activities": [
    {
      "id": "createProject",
      "activityType": "discover.create-project",
      "inputs": {
        "service_name": "zephyr",
        "contract_data": "contract.yaml"
      },
      "outputs": ["repo_url", "project_id"],
      "dependencies": []
    },
    {
      "id": "discoverEndpoints",
      "activityType": "source.discover-endpoints",
      "inputs": {
        "contract": "createProject.contract"
      },
      "outputs": ["endpoints"],
      "dependencies": ["createProject"]
    }
  ]
}
```

### 5. Workflow Orchestration (GitHub Actions, etc.)

```yaml
# .github/workflows/create-project.yml

- name: Create Project
  run: |
    python -m activities.discover.create-project \
      --service-name ${{ inputs.service-name }} \
      --contract-data contract.json \
      --output results.json
```

---

## 🎭 Orchestration Patterns

### Pattern 1: Sequential (Playbook)

```yaml
# Playbook defines sequence
activities:
  - discover.validate-idea
  - discover.create-project
  - source.discover-endpoints
  - source.build-contract
```

### Pattern 2: Dependency Graph (Manifest)

```json
{
  "activities": [
    {"id": "a", "dependencies": []},
    {"id": "b", "dependencies": ["a"]},
    {"id": "c", "dependencies": ["a"]},
    {"id": "d", "dependencies": ["b", "c"]}
  ]
}
```

### Pattern 3: Conditional (Workflow)

```yaml
- if: needs.discover.outputs.should-create-project == 'true'
  run: python -m activities.discover.create-project ...
```

### Pattern 4: Parallel (DAG)

```python
# Activities can run in parallel if no dependencies
activities = [
    Activity("source.discover-endpoints"),
    Activity("source.probe-api"),
    Activity("source.build-contract")  # depends on above two
]
execute_dag(activities)  # Runs first two in parallel
```

---

## 📋 Activity Registry

**Location:** `Core/activities/registry.yaml`

```yaml
activities:
  discover:
    validate-idea:
      module: "activities.discover.validate_idea"
      description: "Validate idea meets SPECTRA standards"
      inputs: ["idea_name", "idea_type"]
      outputs: ["validation_status", "service_name"]
      
    create-project:
      module: "activities.discover.create_project"
      description: "Create GitHub repo, Project v2, initial structure"
      inputs: ["service_name", "contract_data"]
      outputs: ["repo_url", "project_id", "project_path"]
      dependencies: ["discover.validate-idea"]
  
  source:
    discover-endpoints:
      module: "activities.source.discover_endpoints"
      description: "Discover API endpoints from source system"
      inputs: ["contract", "api_base_url"]
      outputs: ["endpoints_catalog"]
      
    build-contract:
      module: "activities.source.build_contract"
      description: "Build contract.yaml from discovery"
      inputs: ["endpoints_catalog", "source_metadata"]
      outputs: ["contract_yaml"]
      dependencies: ["source.discover-endpoints"]
  
  prepare:
    generate-mcp-server:
      module: "activities.prepare.generate_mcp_server"
      description: "Generate MCP server from Source contract"
      inputs: ["contract_yaml"]
      outputs: ["mcp_server_code"]
      dependencies: ["source.build-contract"]
```

---

## 🎯 Benefits

### 1. Flexibility
- ✅ Activities can be invoked from anywhere (CLI, Python, workflows, AI agents)
- ✅ Can compose activities in any order
- ✅ Can skip activities if needed
- ✅ Can run activities independently

### 2. Testability
- ✅ Each activity can be tested in isolation
- ✅ No need for full orchestrator to test activities
- ✅ Easy to mock dependencies
- ✅ Fast test execution

### 3. Reusability
- ✅ Activities work across contexts (Zephyr, Jira, Xero, etc.)
- ✅ Activities can be shared across projects
- ✅ Activities can be versioned independently

### 4. Composability
- ✅ Activities compose naturally (outputs → inputs)
- ✅ Can build complex workflows from simple activities
- ✅ Playbooks define activity sequences
- ✅ Manifest defines activity dependencies

### 5. Evolution
- ✅ Activities can evolve independently
- ✅ Can add new activities without breaking existing ones
- ✅ Can replace activities with better implementations
- ✅ Can deprecate activities gracefully

---

## 🚀 Migration Path

### Phase 1: Extract Activities from Solution Engine

1. **Identify activities** in solution-engine
2. **Extract activity logic** to standalone modules
3. **Create activity CLI** entry points
4. **Test activities independently**

### Phase 2: Create Activity Registry

1. **Define activity registry** structure
2. **Register all activities** with metadata
3. **Document activity interfaces** (inputs, outputs, config)

### Phase 3: Build Orchestration Layer

1. **Playbook orchestrator** - Reads playbooks, executes activities
2. **Manifest orchestrator** - Reads manifest, executes activity DAG
3. **CLI orchestrator** - Executes activity sequences from CLI
4. **Workflow orchestrator** - Executes activities in CI/CD

### Phase 4: Update Playbooks

1. **Define activities** in playbooks
2. **Link playbooks to activities**
3. **Generate GitHub Project v2** from playbook activities

---

## 📚 Example: Zephyr Project Creation Flow

### Using Activities Directly

```bash
# 1. Validate idea
python -m activities.discover.validate-idea \
  --idea-name "zephyr pipeline" \
  --idea-type service

# 2. Create project
python -m activities.discover.create-project \
  --service-name zephyr \
  --contract-data contract.json

# 3. Discover endpoints
python -m activities.source.discover-endpoints \
  --contract Data/zephyr/contract.yaml \
  --api-base-url https://velonetic.yourzephyr.com

# 4. Build contract
python -m activities.source.build-contract \
  --endpoints-catalog endpoints.json \
  --source-metadata metadata.json

# 5. Generate MCP server
python -m activities.prepare.generate-mcp-server \
  --contract Data/zephyr/contract.yaml
```

### Using Playbook Orchestration

```bash
# Execute playbook sequence
python -m orchestrators.playbook \
  --playbook Core/operations/playbooks/fabric/0-setup/setup.000-create-project.md \
  --context Data/zephyr
```

### Using Manifest Orchestration

```bash
# Execute manifest DAG
python -m orchestrators.manifest \
  --manifest Data/zephyr/manifest.json \
  --stage Source
```

---

## 🎨 Orchestration Options

### Option 1: Playbook Executor
- Reads playbook markdown
- Extracts activity definitions
- Executes activities in sequence
- Captures outputs for next activity

### Option 2: Manifest Executor
- Reads manifest.json
- Builds dependency graph
- Executes activities topologically
- Handles parallel execution

### Option 3: CLI Orchestrator
- Simple sequential execution
- Passes outputs between activities
- Good for ad-hoc workflows

### Option 4: Workflow Orchestrator
- Integrates with CI/CD
- Handles errors, retries
- Good for automated pipelines

**Recommendation:** Support all four - use what fits the context.

---

## ✅ Next Steps

1. **Extract first activity** (validate-idea or create-project)
2. **Define activity interface** (base class, CLI pattern)
3. **Create activity registry** structure
4. **Build simple orchestrator** (playbook executor)
5. **Test with Zephyr** as proof of concept

---

**Status:** Ready for implementation  
**Recommendation:** Start with extracting one activity (create-project) and build from there




