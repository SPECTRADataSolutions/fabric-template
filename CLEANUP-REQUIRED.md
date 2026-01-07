# Cleanup Required - Zephyr to Template Conversion

This document lists all zephyr-specific code that needs to be removed/replaced to make this a generic template.

## Files to Rename

### Notebooks
- `sourceZephyr.Notebook/` → `source{PROJECT}.Notebook/`
- `prepareZephyr.Notebook/` → `prepare{PROJECT}Config.Notebook/`
- `extractZephyrSample.Notebook/` → `extract{PROJECT}Sample.Notebook/`

### Fabric Assets
- `zephyrPipeline.DataPipeline/` → `{PROJECT}Pipeline.DataPipeline/`
- `zephyrLakehouse.Lakehouse/` → `{PROJECT}Lakehouse.Lakehouse/`
- `zephyrVariables.VariableLibrary/` → `{PROJECT}Variables.VariableLibrary/`
- `zephyrEnvironment.Environment/` → `{PROJECT}Environment.Environment/`

### Intelligence
- Create `{PROJECT}Intelligence.Notebook/` (new, template)
- Remove `ZephyrIntelligence` from `spectraSDK.Notebook`

## Code Replacements

### Variable Library Names
- `"zephyrVariables"` → `"{PROJECT}Variables"` (all notebooks)
- `"zephyrLakehouse"` → `"{PROJECT}Lakehouse"` (METADATA sections)

### Source System References
- `"zephyr"` → `"{PROJECT}"` (contracts, manifests, variables)
- `"Zephyr Enterprise"` → `"{SOURCE_DISPLAY_NAME}"`

### Class Names
- `ZephyrIntelligence` → `{PROJECT}Intelligence`
- `call_zephyr_api()` → Generic `call_api()` or metadata-driven

## Hardcoded Values to Remove

### Endpoint Paths
- `/project/details` → Read from `Tables/source/endpoints`
- `/release` → Read from `Tables/source/endpoints`
- `/cycle/release/{id}` → Read from metadata

### API Functions
- `call_zephyr_api()` → Generic implementation or use SDK helpers
- Zephyr-specific error handling → Generic error handling

### Intelligence Data
- `ZEPHYR_ENDPOINTS_CATALOG` → Remove from SDK
- Move to `{PROJECT}Intelligence.Notebook`

## SDK Cleanup

### Remove from spectraSDK.Notebook
- `ZephyrIntelligence` class (all 3 instances)
- `ZEPHYR_ENDPOINTS_CATALOG` constant
- Any zephyr-specific helper functions

### Keep in spectraSDK.Notebook
- `NotebookSession` class
- `SourceStageHelpers` class
- `PrepareStageHelpers` class
- `DataValidation` class
- `DeltaTable` class
- `SPECTRALogger` class
- `VariableLibrary` class
- `Pipeline` class
- `Environment` class

## Intelligence Template Structure

Create `{PROJECT}Intelligence.Notebook/notebook_content.py`:

```python
# Fabric notebook source

class {PROJECT}Intelligence:
    """{PROJECT} API intelligence - schemas, dependencies, constraints."""
    
    SCHEMAS = {
        # Template structure - user fills in
    }
    
    READ_ENDPOINTS = {
        # Template structure - user fills in
    }
    
    DEPENDENCIES = {
        # Template structure - user fills in
    }
    
    CONSTRAINTS = {
        # Template structure - user fills in
    }
```

## Metadata-Driven Changes

### Prepare Stage
- Remove hardcoded endpoint list
- Read endpoints from `Tables/source/endpoints`
- Use intelligence from `{PROJECT}Intelligence` notebook

### Extract Stage
- Remove hardcoded endpoint calls
- Loop through endpoints from Source stage
- Use generic API call function

## Documentation Updates

- Update all references to "zephyr" → "{PROJECT}"
- Update examples to be generic
- Add template usage instructions
- Document intelligence creation process

## Testing Requirements

After cleanup:
- [ ] Setup script works correctly
- [ ] Placeholders replaced properly
- [ ] Notebooks sync to Fabric
- [ ] Source stage runs (with proper config)
- [ ] No zephyr-specific code remains

