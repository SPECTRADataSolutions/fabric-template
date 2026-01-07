# Canonical Test Project Design

**Date:** 2025-12-05  
**Status:** 💡 Concept Design  
**Purpose:** Create a comprehensive, best-practice test project in Zephyr using POST/PUT endpoints for automated validation, integration testing, and data quality enforcement

---

## 🎯 Vision

Create a **canonical test project** in Zephyr that serves as:

- ✅ **Deterministic test fixture** - Known good state for validation
- ✅ **Best practices reference** - Demonstrates proper Zephyr configuration
- ✅ **Integration test harness** - Validates bug-Jira ticket links, complete cycles
- ✅ **Automated data generation** - Creates testcases, fills cycles automatically
- ✅ **Quality gate baseline** - Detects missing fields, incomplete hierarchies

---

## 🏗️ Architecture

### Project Structure

```
SPECTRA-Canonical-Project (or "SPECTRA-Test-Canonical")
├── Project Metadata
│   ├── Name: "SPECTRA Canonical Test Project"
│   ├── Key: "SPECTRA-GOLDEN"
│   ├── Description: "Comprehensive test project for SPECTRA pipeline validation"
│   └── Best practices: ✅ All fields populated
│
├── Releases (3-5 releases covering different scenarios)
│   ├── Release 1: "Baseline Release" (Completed, all cycles finished)
│   ├── Release 2: "In-Progress Release" (Active cycles)
│   ├── Release 3: "Future Release" (Planned, no cycles)
│   ├── Release 4: "Regression Release" (Linked to Jira tickets)
│   └── Release 5: "Automation Release" (Synthetic data generation)
│
├── Cycles (Per Release)
│   ├── Cycle: "Smoke Tests" (Quick validation)
│   ├── Cycle: "Regression Tests" (Full suite)
│   ├── Cycle: "Integration Tests" (Jira-linked bugs)
│   └── Cycle: "Performance Tests" (Load scenarios)
│
├── Test Cases (Comprehensive coverage)
│   ├── Test Case: "User Login Flow" (Linked to Jira USER-123)
│   ├── Test Case: "Payment Processing" (Linked to Jira PAY-456)
│   ├── Test Case: "API Validation" (No Jira link - for validation)
│   ├── Test Case: "UI Component Tests" (Hierarchical structure)
│   └── Test Case: "End-to-End Workflows" (Complex scenarios)
│
└── Executions (All states represented)
    ├── Status: Passed (60%)
    ├── Status: Failed (20%) - Linked to Jira bugs
    ├── Status: Blocked (10%) - Linked to Jira blockers
    └── Status: Not Executed (10%)
```

---

## 🔧 Implementation Strategy

### Phase 1: SDK Helper Class - `CanonicalProjectBuilder`

**Location:** `spectraSDK.Notebook` → New class: `CanonicalProjectBuilder`

**Purpose:** Orchestrates creation of canonical project with all components

```python
class CanonicalProjectBuilder:
    """Build and manage the SPECTRA Canonical Test Project in Zephyr."""

    PROJECT_NAME = "SPECTRA Canonical Test Project"
    PROJECT_KEY = "SPECTRA-CANONICAL"

    @staticmethod
    def create_canonical_project(
        base_url: str,
        api_token: str,
        logger: 'SPECTRALogger',
        recreate: bool = False
    ) -> dict:
        """
        Create the complete canonical test project.

        Returns:
            dict: Project metadata including all created IDs
        """
        pass

    @staticmethod
    def create_project(
        base_url: str,
        api_token: str,
        name: str,
        key: str,
        description: str,
        logger: 'SPECTRALogger'
    ) -> dict:
        """Create a new project using POST /project"""
        pass

    @staticmethod
    def create_release(
        base_url: str,
        api_token: str,
        project_id: int,
        name: str,
        start_date: str,
        end_date: str,
        logger: 'SPECTRALogger'
    ) -> dict:
        """Create a new release using POST /release"""
        pass

    @staticmethod
    def create_cycle(
        base_url: str,
        api_token: str,
        release_id: int,
        name: str,
        start_date: str,
        end_date: str,
        logger: 'SPECTRALogger'
    ) -> dict:
        """Create a new cycle using POST /cycle"""
        pass

    @staticmethod
    def create_testcase(
        base_url: str,
        api_token: str,
        project_id: int,
        release_id: int,
        name: str,
        description: str,
        jira_key: str = None,  # Link to Jira ticket
        logger: 'SPECTRALogger'
    ) -> dict:
        """Create a new testcase using POST /testcase"""
        pass

    @staticmethod
    def create_bulk_testcases(
        base_url: str,
        api_token: str,
        project_id: int,
        release_id: int,
        testcases: list[dict],
        logger: 'SPECTRALogger'
    ) -> dict:
        """Create multiple testcases using POST /testcase/bulk"""
        pass
```

---

### Phase 2: Canonical Project Definition (YAML)

**Location:** `Data/zephyr/config/canonical-project.yaml`

**Purpose:** Define the complete structure declaratively

```yaml
project:
  name: "SPECTRA Canonical Test Project"
  key: "SPECTRA-GOLDEN"
  description: "Comprehensive test project for SPECTRA pipeline validation and integration testing"
  best_practices:
    - "All fields populated"
    - "Proper hierarchy"
    - "Jira integration"
    - "Complete cycles"

releases:
  - name: "Baseline Release"
    description: "Completed release with all cycles finished"
    start_date: "2024-01-01"
    end_date: "2024-03-31"
    status: "completed"
    cycles:
      - name: "Smoke Tests"
        description: "Quick validation suite"
        start_date: "2024-01-15"
        end_date: "2024-01-20"
        testcases:
          - name: "User Login Flow"
            description: "Validate user authentication"
            jira_key: "USER-123" # Linked to Jira ticket
            priority: "High"
            steps:
              - step: "Navigate to login page"
                expected: "Login form displayed"
              - step: "Enter valid credentials"
                expected: "User authenticated"
          - name: "Payment Processing"
            description: "Test payment gateway integration"
            jira_key: "PAY-456"
            priority: "Critical"
      - name: "Regression Tests"
        description: "Full regression suite"
        testcases:
          - name: "API Validation"
            description: "Test all API endpoints"
            jira_key: null # No Jira link - for validation testing
            priority: "Medium"

  - name: "In-Progress Release"
    description: "Active release with ongoing cycles"
    start_date: "2024-04-01"
    end_date: "2024-06-30"
    status: "in_progress"
    cycles:
      - name: "Integration Tests"
        description: "Tests with Jira-linked bugs"
        testcases:
          - name: "Bug Integration Test"
            description: "Validates bug-Jira ticket linkage"
            jira_key: "BUG-789"
            expected_links: ["BUG-789", "REL-012"]
          - name: "UI Component Tests"
            description: "Hierarchical test structure"
            priority: "High"
```

---

### Phase 3: Validation Against Canonical Project

**Location:** `spectraSDK.Notebook` → New class: `CanonicalProjectValidator`

**Purpose:** Compare real projects against the canonical standard

```python
class CanonicalProjectValidator:
    """Validate real projects against the canonical test project standard."""

    @staticmethod
    def validate_project_structure(
        real_project: dict,
        canonical_project: dict,
        logger: 'SPECTRALogger'
    ) -> dict:
        """Compare project structure against canonical standard."""
        issues = []

        # Check required fields
        if not real_project.get("description"):
            issues.append("Missing project description")

        # Check best practices
        if not real_project.get("lead"):
            issues.append("Missing project lead (best practice)")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "score": (len(required_fields) - len(issues)) / len(required_fields)
        }

    @staticmethod
    def validate_jira_integration(
        executions: list[dict],
        logger: 'SPECTRALogger'
    ) -> dict:
        """
        Validate that failed executions are linked to Jira tickets.

        Returns:
            dict: {
                "total_failures": 10,
                "linked_failures": 8,
                "unlinked_failures": 2,
                "unlinked_execution_ids": [123, 456],
                "compliance_rate": 0.80
            }
        """
        pass

    @staticmethod
    def validate_cycle_completeness(
        release: dict,
        logger: 'SPECTRALogger'
    ) -> dict:
        """
        Validate that cycles are properly completed.

        Checks:
        - All testcases executed
        - All executions have status
        - No orphaned testcases
        """
        pass
```

---

## 🚀 Use Cases

### Use Case 1: Automated Test Case Generation

**Scenario:** Fill a cycle with testcases automatically

**Implementation:**

```python
# Generate testcases from a template
testcase_template = {
    "name": "Test Case {index}",
    "description": "Automated test case for cycle validation",
    "priority": "Medium",
    "steps": [
        {"step": "Step 1", "expected": "Result 1"},
        {"step": "Step 2", "expected": "Result 2"}
    ]
}

# Create 100 testcases for performance testing
testcases = [
    {**testcase_template, "name": f"Test Case {i}"}
    for i in range(1, 101)
]

CanonicalProjectBuilder.create_bulk_testcases(
    base_url=base_url,
    api_token=api_token,
    project_id=project_id,
    release_id=release_id,
    testcases=testcases,
    logger=log
)
```

### Use Case 2: Integration Validation

**Scenario:** Check if bugs are linked to Jira tickets

**Implementation:**

```python
# After extracting executions from source stage
validation_result = CanonicalProjectValidator.validate_jira_integration(
    executions=failed_executions,
    logger=log
)

if validation_result["compliance_rate"] < 0.90:
    log.warning(
        f"⚠️ Jira integration compliance below threshold: "
        f"{validation_result['compliance_rate']:.2%}"
    )
    log.warning(
        f"   Unlinked failures: {validation_result['unlinked_execution_ids']}"
    )

    # Optionally: Auto-create Jira tickets for unlinked failures
    # for execution_id in validation_result['unlinked_execution_ids']:
    #     create_jira_ticket_from_execution(execution_id)
```

### Use Case 3: Cycle Completion Automation

**Scenario:** Automatically fill out a cycle with testcases and executions

**Implementation:**

```python
# Create cycle
cycle = CanonicalProjectBuilder.create_cycle(...)

# Add testcases
testcases = load_testcases_from_template("regression_suite.yaml")
CanonicalProjectBuilder.create_bulk_testcases(...)

# Create executions (simulated test runs)
for testcase in testcases:
    execution = create_execution(
        cycle_id=cycle["id"],
        testcase_id=testcase["id"],
        status="Passed",  # or random distribution
        executed_by="automation",
        executed_on=datetime.now()
    )
```

### Use Case 4: Best Practices Enforcement

**Scenario:** Validate all projects match canonical standard

**Implementation:**

```python
# After extracting all projects in source stage
canonical_project = load_canonical_project_definition()

for project in all_projects:
    validation = CanonicalProjectValidator.validate_project_structure(
        real_project=project,
        canonical_project=canonical_project,
        logger=log
    )

    if validation["score"] < 0.80:
        log.warning(
            f"⚠️ Project {project['name']} does not meet best practices "
            f"(score: {validation['score']:.2%})"
        )
        log.warning(f"   Issues: {validation['issues']}")
```

---

## 📋 Integration with Source Stage

### New Notebook: `createCanonicalProject.Notebook`

**Purpose:** One-time setup to create the canonical project

**Parameters:**

- `recreate: bool = False` - Delete and recreate if exists
- `populate: bool = True` - Fill with test data

**Stages:**

1. **Check existence** - Does project already exist?
2. **Delete if recreate** - Remove existing project
3. **Create project** - POST /project
4. **Create releases** - POST /release (multiple)
5. **Create cycles** - POST /cycle (per release)
6. **Create testcases** - POST /testcase/bulk
7. **Create executions** - POST /execution (optional)
8. **Validate structure** - Verify all created correctly

### Integration with `sourceZephyr`

**Add validation step:**

```python
# In Stage 5: VALIDATE

if test:
    # Existing validations...

    # NEW: Canonical project validation
    if session.params.get("validate_against_canonical"):
        canonical_validation = CanonicalProjectValidator.validate_all_projects(
            projects=all_projects,
            executions=all_executions,
            logger=log
        )

        session.add_capability(
            "canonicalProjectValidated",
            compliance_rate=canonical_validation["overall_compliance"]
        )
```

---

## 🔗 Jira Integration Pattern

### Link Testcases to Jira Tickets

**When creating testcase:**

```python
testcase = {
    "name": "Payment Gateway Test",
    "description": "Test payment processing integration",
    "customFields": {
        "jiraKey": "PAY-456",  # Link to Jira ticket
        "bugId": "BUG-789"     # Link to bug if exists
    }
}
```

### Validate Links After Extraction

**In validation stage:**

```python
# Extract all executions with failures
failed_executions = [
    e for e in all_executions
    if e["status"] == "Failed"
]

# Check Jira links
validation = CanonicalProjectValidator.validate_jira_integration(
    executions=failed_executions,
    logger=log
)

# Report compliance
if validation["compliance_rate"] < 0.90:
    # Alert: Missing Jira links
    send_alert(
        "Jira Integration Compliance Low",
        f"Only {validation['compliance_rate']:.2%} of failures linked to Jira"
    )
```

---

## 📊 Benefits

### 1. **Deterministic Testing**

- ✅ Known good state for validation
- ✅ Predictable test results
- ✅ Easy to detect regressions

### 2. **Best Practices Enforcement**

- ✅ Detect missing fields
- ✅ Validate proper hierarchy
- ✅ Ensure Jira integration
- ✅ Check cycle completeness

### 3. **Automation Enablement**

- ✅ Auto-generate testcases
- ✅ Auto-fill cycles
- ✅ Auto-create Jira tickets for unlinked bugs
- ✅ Auto-validate integration

### 4. **Quality Gates**

- ✅ Data quality checks (completeness)
- ✅ Integration checks (Jira links)
- ✅ Hierarchy checks (proper structure)
- ✅ Compliance scoring

---

## 🎯 Next Steps

1. ⏳ **Design API payload structures** - Document required fields for POST endpoints
2. ⏳ **Create `CanonicalProjectBuilder` class** - SDK implementation
3. ⏳ **Create `CanonicalProjectValidator` class** - Validation logic
4. ⏳ **Define canonical project YAML** - Declarative structure
5. ⏳ **Create `createCanonicalProject` notebook** - One-time setup
6. ⏳ **Integrate with source stage** - Add validation parameter
7. ⏳ **Document Jira linking patterns** - How to link testcases to tickets
8. ⏳ **Test in Fabric** - Create project and validate

---

## 🔍 Considerations

### Project Isolation

- ✅ Use dedicated test project (not production)
- ✅ Prefix: "SPECTRA-" to avoid conflicts
- ✅ Document project ID in config for reference

### Data Cleanup

- ⚠️ Consider cleanup strategy (delete old canonical projects?)
- ⚠️ Version management (multiple canonical projects for different scenarios?)

### Jira Integration

- ⚠️ Need Jira API access for auto-ticket creation?
- ⚠️ Handle cases where Jira ticket doesn't exist yet
- ⚠️ Validate Jira key format before linking

### Performance

- ⚠️ Bulk operations (POST /testcase/bulk) for efficiency
- ⚠️ Rate limiting consideration (60 req/min burst)
- ⚠️ Async execution for large datasets

---

## 💡 Future Enhancements

1. **Multiple Canonical Projects**

   - Different projects for different scenarios (regression, performance, integration)
   - Versioned canonical projects (v1, v2, etc.)

2. **Template System**

   - Reusable testcase templates
   - Cycle templates (smoke, regression, etc.)
   - Release templates (baseline, in-progress, etc.)

3. **Auto-Remediation**

   - Auto-create Jira tickets for unlinked bugs
   - Auto-fill missing fields with defaults
   - Auto-complete incomplete cycles

4. **Reporting**
   - Compliance dashboard
   - Best practices scorecard
   - Integration health metrics
