# SPECTRA Playbook Assessment & Recommendations

## Current State

### Existing SPECTRA Playbook Structure

**Location**: `Core/operations/playbooks/fabric/`

**Structure**:
```
fabric/
├── 0-setup/          # Initial pipeline setup
│   ├── setup.000-createInitialArtifacts.md
│   ├── setup.001-createGithubRepository.md
│   ├── setup.002-createFabricWorkspace.md
│   ├── setup.003-createFabricEnvironment.md
│   ├── setup.004-createFabricLakehouse.md
│   ├── setup.005-createFabricPipeline.md
│   └── setup.006-createFabricVariableLibrary.md
└── 1-source/         # Source stage setup
    ├── source.001-createSourceNotebook.md
    └── source.002-addNotebookToPipeline.md
```

### Zephyr Playbook Status

**Current**: No Zephyr-specific playbooks exist yet. Zephyr was built using the generic Fabric playbooks.

**Gap**: Missing playbooks for:
- Endpoints discovery/bootstrap (init_mode)
- Source stage endpoints table population
- SPECTRA methodology stage progression (Prepare, Extract, Clean, etc.)

## SPECTRA-Grade Playbook Principles

### 1. **Methodology-Driven Structure**

Playbooks should align with SPECTRA's seven-stage lifecycle:

```
Source → Prepare → Extract → Clean → Transform → Refine → Analyse
```

**Recommendation**: Organize playbooks by stage, not by tool:

```
fabric/
├── 0-setup/              # Infrastructure (workspace, lakehouse, pipeline)
├── 1-source/             # Source stage (cataloguing, endpoints, auth)
├── 2-prepare/            # Prepare stage (parameters, schema, controls)
├── 3-extract/            # Extract stage (raw data landing)
├── 4-clean/              # Clean stage (standardization, DQ)
├── 5-transform/          # Transform stage (enrichment, joins)
├── 6-refine/             # Refine stage (facts/dims, semantic model)
└── 7-analyse/            # Analyse stage (measures, reports)
```

### 2. **AI-Optimized Format**

Each playbook should be:
- **Machine-readable**: Clear structure, no ambiguity
- **Idempotent**: Can be run multiple times safely
- **Evidence-driven**: Captures outputs for automation
- **Contract-aligned**: References `contract.yaml` and methodology docs

**Current Format** (Good):
```markdown
## 🎯 purpose
## 📋 required parameters
## 🤖 ai-optimised procedure
## 🧪 produces
## 🔗 dependencies
## ⏭️ next procedure
```

**Enhancement**: Add quality gates and validation steps.

### 3. **Stage-Specific Playbooks**

Each SPECTRA stage should have:
- **Setup playbooks**: Create artifacts (notebooks, tables, configs)
- **Execution playbooks**: Run the stage, validate outputs
- **Quality gate playbooks**: Verify stage completion

**Example for Source Stage**:
```
1-source/
├── source.001-createSourceNotebook.md
├── source.002-addNotebookToPipeline.md
├── source.003-bootstrapEndpoints.md          # NEW: init_mode endpoints
├── source.004-populateEndpointsTable.md      # NEW: load to Delta
├── source.005-validateSourceStage.md         # NEW: quality gates
└── source.006-sourceStageHandoff.md          # NEW: handoff to Prepare
```

### 4. **Contract-Driven**

Playbooks should:
- Read from `contract.yaml` (source system contract)
- Reference `manifest.json` (pipeline activities)
- Use `source.plan.yaml` (stage-specific plan)
- Never hardcode values

**Example**:
```yaml
# Playbook reads from contract.yaml
sourceKey: "{{ contract.sourceSystem.key }}"
workspaceName: "{{ contract.artifacts.fabric.workspaceName }}"
```

### 5. **Evidence & Journaling**

Every playbook should:
- Capture outputs in `.spectra/evidence/{stage}/{playbook}/{date}/`
- Log to `Core/memory/journal/` for Chronicle
- Store machine-readable results (JSON/YAML)
- Include screenshots for UI-only steps

## Recommended Zephyr Playbook Structure

### Immediate Needs

1. **Update `setup.005-createFabricPipeline.md`**
   - Add `init_mode` parameter
   - Document when to use init_mode

2. **Create `source.003-bootstrapEndpoints.md`**
   - Generate endpoints_module.py
   - Bootstrap endpoints.json to Files area
   - Load into Delta table

3. **Create `source.004-validateSourceStage.md`**
   - Quality gates for Source stage
   - Verify endpoints table populated
   - Validate handshake audit

### Future Playbooks (Per Stage)

**Prepare Stage**:
```
2-prepare/
├── prepare.001-createPrepareNotebook.md
├── prepare.002-generateSchemaMetadata.md
├── prepare.003-createParameterPacks.md
└── prepare.004-validatePrepareStage.md
```

**Extract Stage**:
```
3-extract/
├── extract.001-createExtractNotebooks.md
├── extract.002-configureExtractionPlan.md
├── extract.003-validateExtractStage.md
└── extract.004-extractStageHandoff.md
```

## SPECTRA-Grade Playbook Template

```markdown
# {stage}.{number} - {kebab-case-description}

version: 1.0.0
status: active
stage: {Source|Prepare|Extract|Clean|Transform|Refine|Analyse}

## 🎯 purpose

Clear, single-sentence purpose aligned with SPECTRA methodology stage responsibilities.

## 📋 required parameters

List all inputs (from contract.yaml, manifest.json, or previous playbooks):
- `sourceKey` (from contract.yaml)
- `workspaceName` (from contract.yaml)
- `{parameter}` (description, source)

## 🤖 ai-optimised procedure

### step 0 — validate prerequisites

1. Check contract.yaml exists and is valid
2. Verify previous playbooks completed (check evidence)
3. Confirm credentials available

### step 1 — {action}

Clear, numbered steps. Use code blocks for commands.
Reference contract values: `{{ contract.sourceSystem.key }}`

### step 2 — {validation}

Verify outputs, check quality gates.

## 🧪 produces

Machine-readable outputs:
```yaml
artifacts:
  - name: "{artifact}"
    path: "{path}"
    type: "{type}"
qualityGates:
  - name: "{gate}"
    status: "passed|failed"
    evidence: "{path}"
```

## 🔗 dependencies

- `{previous-playbook}` (must complete first)
- `contract.yaml` (must exist)
- `{resource}` (must be available)

## ⏭️ next procedure

`{next-stage}.{next-number} - {description}`

## 📚 references

- SPECTRA Methodology: `Data/fabric-sdk/docs/methodology/{stage}/{stage}.md`
- Contract: `contract.yaml`
- Manifest: `manifest.json`
```

## Comparison: Current vs SPECTRA-Grade

| Aspect | Current | SPECTRA-Grade |
|--------|--------|---------------|
| **Organization** | Tool-based (setup, source) | Stage-based (0-setup, 1-source, 2-prepare...) |
| **Methodology Alignment** | Implicit | Explicit (references methodology docs) |
| **Contract Integration** | Manual | Automated (reads from contract.yaml) |
| **Quality Gates** | Missing | Explicit validation steps |
| **Evidence** | Ad-hoc | Structured (`.spectra/evidence/`) |
| **Stage Progression** | Unclear | Clear handoff between stages |
| **AI Optimization** | Good | Enhanced with validation |

## Recommendations

### Immediate Actions

1. ✅ **Update `setup.005`** to include `init_mode` parameter
2. ✅ **Create `source.003-bootstrapEndpoints.md`** for endpoints discovery
3. ✅ **Create `source.004-validateSourceStage.md`** for quality gates
4. ✅ **Document playbook standards** in `Core/operations/playbooks/STRUCTURE.md`

### Long-Term Vision

1. **Stage-based organization**: Reorganize playbooks by SPECTRA stage
2. **Automated validation**: Playbooks validate their own outputs
3. **Contract-driven**: All values read from contract.yaml
4. **Quality gates**: Every stage has explicit pass/fail criteria
5. **Evidence automation**: Auto-capture outputs to `.spectra/evidence/`

## Conclusion

Current playbooks are **good foundation** but need:
- **Methodology alignment**: Explicit SPECTRA stage references
- **Quality gates**: Validation steps for each playbook
- **Contract integration**: Read from contract.yaml automatically
- **Stage progression**: Clear handoff between stages

**SPECTRA-Grade Approach**: Playbooks should be **stage-driven, contract-aligned, evidence-capturing, and quality-gated**.




