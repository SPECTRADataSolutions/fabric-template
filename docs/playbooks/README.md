# Zephyr Playbooks

## Overview

This directory contains playbook assessments and recommendations for Zephyr pipeline development following SPECTRA methodology.

## Documents

- **`PLAYBOOK-ASSESSMENT.md`** - Comprehensive assessment of current playbook structure vs SPECTRA-grade approach, with recommendations

## SPECTRA Playbook Location

Zephyr uses the shared SPECTRA playbooks located at:
- `Core/operations/playbooks/fabric/0-setup/` - Infrastructure setup
- `Core/operations/playbooks/fabric/1-source/` - Source stage setup

## Key Playbooks for Zephyr

### Setup Phase
- `setup.005-createFabricPipeline.md` - **Updated** to include `init_mode` parameter

### Source Stage
- `source.001-createSourceNotebook.md` - Create Source notebook
- `source.002-addNotebookToPipeline.md` - Wire notebook to pipeline
- `source.003-bootstrapEndpoints.md` - **NEW** - Bootstrap endpoints.json (init_mode)

## Quick Reference

### Running with Init Mode

**First run (bootstrap endpoints)**:
```powershell
fab pipeline run zephyrWorkspace/zephyrPipeline.DataPipeline `
  --parameters '{"init_mode": true}'
```

**Normal runs**:
```powershell
fab pipeline run zephyrWorkspace/zephyrPipeline.DataPipeline
```

### Playbook Sequence

1. **Setup**: `setup.000` → `setup.006` (infrastructure)
2. **Source**: `source.001` → `source.003` (Source stage)
3. **Future**: `prepare.001` → `extract.001` → etc. (per SPECTRA methodology)

## SPECTRA-Grade Principles

1. **Stage-based organization** - Playbooks organized by SPECTRA stage
2. **Contract-driven** - Values read from `contract.yaml`
3. **Evidence-capturing** - Outputs saved to `.spectra/evidence/`
4. **Quality-gated** - Explicit validation steps
5. **AI-optimized** - Machine-readable, unambiguous procedures

## See Also

- SPECTRA Methodology: `Data/fabric-sdk/docs/methodology/`
- Playbook Standards: `Core/operations/playbooks/STRUCTURE.md`
- Source Stage Docs: `Data/zephyr/docs/source/`




