# Local Source Runner Architecture

## Current Location

**Project-specific:** `Data/zephyr/scripts/run_source_local.py`

## Why Project-Specific?

Following SPECTRA's **Rule of Three**:
- Currently only used by Zephyr (1 project)
- Not yet proven across multiple projects
- Project-specific configuration (endpoints.json, contract.yaml)

## Future: Shared Framework Tool

When used by 3+ projects (Jira, Xero, etc.), move to:

**Shared location:** `Data/fabric-sdk/scripts/run_source_stage_local.py`

### Migration Path

1. **Extract generic logic** to `Data/fabric-sdk/scripts/run_source_stage_local.py`:
   - Spark session creation
   - Fabric Files/Delta mocking
   - Health check framework
   - Quality gate generation

2. **Keep project-specific wrapper** in `Data/zephyr/scripts/run_source_local.py`:
   - Loads Zephyr-specific config (contract.yaml, endpoints.json)
   - Calls shared runner with project context
   - Handles Zephyr-specific logic

3. **Other projects** create similar wrappers:
   - `Data/jira/scripts/run_source_local.py`
   - `Data/xero/scripts/run_source_local.py`

## Design for Shareability

The current runner is designed to be easily shareable:

- ✅ **Generic Spark setup** - Works for any project
- ✅ **Configurable paths** - Reads from project root
- ✅ **Project-agnostic health checks** - Works with any API
- ✅ **Standard quality gates** - Reusable across projects

## When to Share?

Move to `Data/fabric-sdk/scripts/` when:
- ✅ Used by 3+ projects (Jira, Zephyr, Xero)
- ✅ Pattern proven and stable
- ✅ Generic enough for all projects

## Alternative: Core Operations Tool

If it becomes a general development tool (not Fabric-specific), could move to:
- `Core/operations/scripts/run-fabric-source-local.py`

But this is less likely since it's Fabric-specific.




