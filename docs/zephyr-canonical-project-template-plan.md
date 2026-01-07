# Zephyr Canonical Project Template Plan

> **Purpose:** Establish Zephyr as the canonical template for all SPECTRA source projects, with parameterised structure, playbook-driven GitHub Project v2 generation, and MCP server auto-generation from source stage endpoints.

**Status:** Planning  
**Date:** 2025-12-05  
**Owner:** Data Platform

---

## 🎯 Vision

**Zephyr becomes the reference implementation** that drives:

1. **Parameterised Project Template** - Reusable structure for any source (Jira, Xero, UniFi, etc.)
2. **Playbook-Driven Project Generation** - Playbooks define canonical GitHub Project v2 issues automatically
3. **MCP Server Auto-Generation** - Source stage endpoints automatically generate MCP servers for AI interaction
4. **Complete Documentation Ecosystem** - All lifecycle documentation captured and templated

---

## 📋 Current State Assessment

### ✅ What We Have (Zephyr)

#### Source Stage (Complete)
- ✅ SPECTRA-grade implementation with SDK (v0.3.0)
- ✅ Contract-driven architecture (`contracts/source.contract.yaml`)
- ✅ 228 endpoints catalogued and embedded in SDK
- ✅ Hierarchical access validated (Projects → Releases → Cycles → Executions)
- ✅ Comprehensive test suite (>75% coverage)
- ✅ Dashboard-ready portfolio tables
- ✅ Preview samples for all resource types

#### Documentation (123 files)
- ✅ Deep research summary (`ZEPHYR-RESEARCH-SUMMARY.md`)
- ✅ Complete API discovery (endpoints, pagination, rate limits)
- ✅ Source stage documentation (procedures, design, quality gates)
- ✅ Prepare stage documentation (schema design, metadata)
- ✅ Refine stage documentation (dimensional model)
- ✅ Development guides (local testing, pipeline configuration)
- ✅ Architecture documentation
- ✅ Playbook assessments

#### Playbooks (Started, Not Complete)
- ✅ Playbook structure assessment (`docs/playbooks/PLAYBOOK-ASSESSMENT.md`)
- ✅ Recommendations for SPECTRA-grade playbooks
- ❌ Actual playbooks not yet created

#### Project Structure
- ✅ Manifest-driven (`manifest.json`)
- ✅ Contract-driven (`contracts/source.contract.yaml`)
- ✅ Source plan (`source/source.plan.yaml`)
- ✅ Notebook-based execution (`sourceZephyr.Notebook/`)

### ❌ What's Missing

1. **Parameterised Template** - Can't yet instantiate for new sources
2. **Playbook Completion** - Playbooks defined but not executed
3. **GitHub Project v2 Integration** - No automated project generation
4. **MCP Server Generation** - Endpoints exist but no MCP server yet
5. **Template Documentation** - No template documentation structure

---

## 🏗️ Proposed Architecture

### 1. Parameterised Project Template

**Structure:**
```
{source}-template/
├── .spectra/
│   ├── template.yaml          # Template metadata and parameter definitions
│   └── generator.py           # Template instantiation script
├── contracts/
│   └── source.contract.yaml.template   # Parameterised contract template
├── source/
│   ├── source.plan.yaml.template       # Parameterised plan template
│   └── source{Source}.Notebook/        # Template notebook structure
├── docs/
│   ├── {source}-research-summary.md.template
│   ├── source/
│   ├── prepare/
│   └── ...                    # All documentation templates
├── manifest.json.template     # Parameterised manifest
└── README.md.template         # Template README
```

**Parameters:**
```yaml
source_name: "zephyr"              # Lowercase, kebab-case
source_display_name: "Zephyr"      # Title case
source_description: "Test management analytics"
source_org: "SPECTRADataSolutions"
api_base_url_template: "https://{tenant}.yourzephyr.com"
api_base_path: "/flex/services/rest/latest"
auth_method: "apiToken"
variable_library: "{source}Variables"
endpoint_count: 228                # Discovered endpoints
hierarchical_levels: 5            # Projects → Releases → Cycles → Executions → Test Cases
```

### 2. Playbook-Driven GitHub Project v2

**Flow:**
```
Playbooks (Core/operations/playbooks/fabric/{stage}/)
    ↓
Playbook Parser (extracts tasks, dependencies, quality gates)
    ↓
GitHub Project v2 Generator (creates issues, fields, views)
    ↓
GitHub Project v2 (canonical backlog)
```

**Playbook Structure Enhancement:**
```yaml
# Example: source.001-createSourceNotebook.md
---
playbook:
  id: "source.001"
  stage: "Source"
  title: "Create Source Notebook"
  description: "Create Fabric notebook for Source stage"
  
  # GitHub Project v2 generation metadata
  project:
    field_mappings:
      status: "Stage"
      priority: "Impact"
      stage: "Source"
    
  tasks:
    - id: "task-001"
      title: "Generate Source Notebook Structure"
      definition_of_done:
        - "Notebook created with proper metadata blocks"
        - "SDK imported and configured"
        - "Variable Library variables defined"
      acceptance_criteria:
        - "Notebook runs in interactive mode"
        - "Notebook runs in pipeline mode"
      dependencies: []
      quality_gates:
        - name: "notebook_structure"
          validator: "validate_notebook_structure"
```

### 3. MCP Server Auto-Generation

**Flow:**
```
Source Stage Endpoints (Tables/source/endpoints)
    ↓
Endpoint Parser (extracts endpoints, parameters, schemas)
    ↓
MCP Server Generator (creates MCP server with tools for each endpoint)
    ↓
MCP Server ({source}-mcp-server/)
    ↓
AI can interact with {source} perfectly
```

**MCP Server Structure:**
```python
# Auto-generated MCP server for Zephyr
# Generated from: Tables/source/zephyr_endpoints

tools = [
    {
        "name": "zephyr_get_projects",
        "description": "Get all Zephyr projects",
        "inputSchema": {
            "type": "object",
            "properties": {
                "projectKey": {"type": "string", "description": "Project key (optional)"}
            }
        }
    },
    {
        "name": "zephyr_get_releases",
        "description": "Get releases for a project",
        "inputSchema": {
            "type": "object",
            "properties": {
                "projectId": {"type": "string", "required": True}
            }
        }
    },
    # ... one tool per endpoint
]
```

---

## 📚 Complete Documentation Inventory

### Deep Research & Understanding (3 files)
- `ZEPHYR-RESEARCH-SUMMARY.md` - Comprehensive research document
- `ZEPHYR-ENTERPRISE-MASTER-KNOWLEDGE.md` - Master knowledge base
- `ZEPHYR-COMPLETE-UNDERSTANDING.md` - Complete understanding document

### Source Stage (15 files)
- `source/README.md` - Source stage overview
- `source/procedures.md` - Runbook/checklist
- `source/jira-alignment.md` - Jira lessons
- `source/SOURCE-DESIGN-READINESS.md` - Design readiness
- `SOURCE-STAGE-QUALITY-GATE-REPORT.md` - Quality gate report
- `SOURCE-CONTRACT-VS-NOTEBOOK-STATUS.md` - Contract vs notebook status
- `SOURCE-NOTEBOOK-CLEANUP-PLAN.md` - Cleanup plan
- `SOURCE-NOTEBOOK-CLEANUP-SUMMARY.md` - Cleanup summary
- `SOURCE-NOTEBOOK-COMPLETE-FLOW.md` - Complete flow documentation
- `SOURCE-NOTEBOOK-PRODUCTION-PLAN.md` - Production plan
- `SOURCE-NOTEBOOK-RUN-MODES.md` - Run modes
- `SOURCE-TABLE-PORTFOLIO-DESIGN.md` - Table portfolio design
- `SOURCE-BUILDS-SAMPLE-DATABASE.md` - Sample database
- `source-register.md` - Source registration
- `NEXT-STEPS-SOURCE-STAGE.md` - Next steps

### Prepare Stage (6 files)
- `prepare/README.md` - Prepare stage overview
- `prepare/PREPARE-STAGE-SCHEMA-DESIGN.md` - Schema design
- `prepare/PREPARE-STAGE-FRESH-DESIGN.md` - Fresh design
- `prepare/PREPARE-STAGE-COMPLETE.md` - Completion status
- `prepare/PREPARE-STAGE-COMPARISON.md` - Comparison document

### Refine Stage (3 files)
- `refine/DIMENSIONAL-MODEL-DESIGN.md` - Dimensional model design
- `refine/DIMENSIONAL-MODEL-ENRICHMENT.md` - Model enrichment
- `refine/DIMENSIONAL-MODEL-DIAGRAM.md` - Model diagram

### API Discovery (12 files)
- `api-discovery/ENDPOINT-TEST-SUMMARY.md` - Test summary
- `api-discovery/HIERARCHICAL-ACCESS-PROVEN.md` - Hierarchical access proof
- `api-discovery/ENDPOINT-CATALOG-DIMENSIONAL-MAPPING.md` - Dimensional mapping
- `api-discovery/ENDPOINT-FAILURE-ANALYSIS.md` - Failure analysis
- `api-discovery/COMPREHENSIVE-TEST-DIAGNOSIS.md` - Test diagnosis
- `api-discovery/FINAL-ENDPOINT-DIAGNOSIS.md` - Final diagnosis
- `api-discovery/SAMPLE-DIMENSIONAL-EXTRACTION.md` - Sample extraction
- `api-discovery/SAMPLE-100-EXTRACTION-REPORT.md` - Sample extraction report
- `api-discovery/pagination-rate-limits.md` - Pagination and rate limits
- `api-discovery/pagination-examples.md` - Pagination examples
- `api-discovery/page-size-recommendations.md` - Page size recommendations
- `api/embed-endpoints-solution.md` - Embed endpoints solution

### Development Guides (10 files)
- `development/local-testing-guide.md` - Local testing guide
- `development/local-runner-architecture.md` - Local runner architecture
- `development/pipeline-cli-guide.md` - Pipeline CLI guide
- `development/get-pipeline-id.md` - Get pipeline ID
- `development/fabric-variable-library-setup.md` - Variable library setup
- `development/fabric-package-installation-official.md` - Package installation
- `development/install-from-github-releases-guide.md` - GitHub releases guide
- `development/fabric-files-tables-quirk.md` - Files/tables quirk
- `development/pipeline-permissions-issue.md` - Permissions issue
- `development/setup-local-testing.md` - Setup local testing

### Architecture (4 files)
- `architecture/combined-data-platform-vision.md` - Platform vision
- `architecture/parameter-design-analysis.md` - Parameter design
- `architecture/parameter-redesign.md` - Parameter redesign
- `architecture/tomorrow-pipeline-validation-design.md` - Validation design

### Standards (4 files)
- `standards/NAMING-CONVENTION-BOUNDARY.md` - Naming conventions
- `standards/runtime-parameters-assessment.md` - Runtime parameters
- `standards/debug-logging-and-parameters.md` - Debug logging
- `standards/governance-clarifications.md` - Governance

### Reference (26 files)
- See `docs/reference/` for complete list

### Playbooks (3 files)
- `playbooks/README.md` - Playbooks overview
- `playbooks/PLAYBOOK-ASSESSMENT.md` - Playbook assessment
- `playbooks/RECREATE-LAKEHOUSE-WITH-SCHEMAS.md` - Lakehouse recreation

### Other Key Documents (25+ files)
- Configuration, testing, troubleshooting, risks, stakeholders, etc.

**Total:** 123 documentation files

---

## 🚀 Implementation Plan

### Phase 1: Template Parameterisation (Week 1)

**Goal:** Make Zephyr structure fully parameterised

1. **Create Template Structure**
   - Extract all hardcoded values to template variables
   - Create `.spectra/template.yaml` with parameter definitions
   - Create template instantiation script

2. **Parameterise Contracts**
   - `contracts/source.contract.yaml.template`
   - Replace hardcoded values with `{{variable}}` placeholders

3. **Parameterise Plans**
   - `source/source.plan.yaml.template`
   - Replace source-specific values

4. **Parameterise Documentation**
   - Create documentation templates
   - Replace source names, URLs, endpoints with placeholders

**Deliverable:** Working template that can instantiate a new source project

### Phase 2: Playbook Completion & GitHub Project v2 (Week 2)

**Goal:** Complete playbooks and auto-generate GitHub Project v2

1. **Complete Playbook Definitions**
   - Define all Source stage playbooks
   - Add GitHub Project v2 metadata to each playbook
   - Define task dependencies and quality gates

2. **Build Playbook Parser**
   - Parse playbook metadata
   - Extract tasks, dependencies, acceptance criteria
   - Generate GitHub Project v2 issue definitions

3. **Build GitHub Project v2 Generator**
   - Use existing `simple_project_bootstrap.py` as base
   - Extend to support playbook-driven generation
   - Create Project fields, views, issues from playbooks

4. **Test with Zephyr**
   - Generate Zephyr GitHub Project v2 from playbooks
   - Verify all issues, dependencies, quality gates created

**Deliverable:** Automated GitHub Project v2 generation from playbooks

### Phase 3: MCP Server Generation (Week 3)

**Goal:** Auto-generate MCP server from source stage endpoints

1. **Build Endpoint Parser**
   - Read from `Tables/source/{source}_endpoints`
   - Extract endpoint metadata (method, path, parameters, schema)
   - Map to MCP tool definitions

2. **Build MCP Server Generator**
   - Generate MCP server structure
   - Create tools for each endpoint
   - Generate input schemas from endpoint parameters

3. **Implement MCP Server Runtime**
   - Handle authentication (Bearer token from Variable Library)
   - Execute API calls
   - Return structured responses

4. **Test with Zephyr**
   - Generate Zephyr MCP server
   - Verify all 228 endpoints available as MCP tools
   - Test AI interaction

**Deliverable:** Working MCP server for Zephyr with all endpoints

### Phase 4: Template Documentation & Validation (Week 4)

**Goal:** Complete template documentation and validate approach

1. **Template Documentation**
   - Document template structure
   - Create instantiation guide
   - Document parameter definitions

2. **Template Validation**
   - Test template with dummy source
   - Verify all artifacts generate correctly
   - Validate playbooks and MCP generation work

3. **Canonical Template Documentation**
   - Create comprehensive template guide
   - Document all features
   - Create migration guide from Zephyr

**Deliverable:** Complete template documentation and validation

---

## 🎯 Success Criteria

### Template Parameterisation
- ✅ Can instantiate new source project with single command
- ✅ All hardcoded values replaced with parameters
- ✅ Template validates before instantiation

### Playbook-Driven Project Generation
- ✅ GitHub Project v2 created from playbooks automatically
- ✅ All tasks, dependencies, quality gates represented
- ✅ Project views and fields configured correctly

### MCP Server Generation
- ✅ MCP server generated from source stage endpoints
- ✅ All endpoints available as MCP tools
- ✅ AI can interact with source system perfectly

### Documentation
- ✅ All 123 documentation files templated
- ✅ Template documentation complete
- ✅ Migration guide available

---

## 📖 Next Steps

### Immediate (This Week)

1. **Review & Approve Plan**
   - Review this document
   - Confirm approach
   - Adjust priorities if needed

2. **Start Phase 1**
   - Extract template variables from Zephyr
   - Create `.spectra/template.yaml`
   - Begin parameterisation

### Short-term (Next 2 Weeks)

1. Complete Phase 1 & 2
2. Generate first GitHub Project v2 from playbooks
3. Begin MCP server generation

### Long-term (Next Month)

1. Complete all phases
2. Validate template with new source (e.g., Xero)
3. Document template usage
4. Create migration guide

---

## 🤔 Questions & Considerations

1. **Template Location**
   - Should template live in `Core/operations/templates/` or `Data/.github/templates/`?
   - **Recommendation:** `Core/operations/templates/` (operations-level concern)

2. **Playbook Enhancement**
   - Should we extend playbook format or add separate metadata files?
   - **Recommendation:** Extend playbook frontmatter (YAML) - single source of truth

3. **MCP Server Location**
   - Should MCP servers live in source repos or separate MCP repo?
   - **Recommendation:** Separate `Core/mcp-servers/` repo (allows independent versioning)

4. **Template Updates**
   - How do we handle template updates for existing projects?
   - **Recommendation:** Migration scripts + versioned templates

---

## 🔗 References

- **Project Provisioning Plan:** `Data/.github/project-provisioning-plan.md`
- **Playbook Assessment:** `Data/zephyr/docs/playbooks/PLAYBOOK-ASSESSMENT.md`
- **Playbook Standards:** `Core/operations/playbooks/STRUCTURE.md`
- **Source Stage Contract:** `Data/zephyr/contracts/source.contract.yaml`
- **Zephyr Manifest:** `Data/zephyr/manifest.json`

---

**Status:** Ready for review and approval  
**Next Action:** Review this plan and confirm approach




