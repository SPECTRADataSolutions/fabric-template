# Template Usage Guide

## Creating a New Project from This Template

### Step 1: Create Repository from Template

1. Go to this repository on GitHub
2. Click **"Use this template"** button
3. Create new repository: `your-project-name`
4. Clone the new repository

### Step 2: Run Setup Script

```powershell
cd your-project-name
.\scripts\setup-new-project.ps1 -ProjectName "yourproject" -SourceSystem "YourSourceSystem" -SourceDisplayName "Your Source System"
```

This will:
- Replace all `{PROJECT}` placeholders
- Update Variable Library names
- Update lakehouse references
- Rename directories/files

### Step 3: Customize Intelligence

1. Create `{PROJECT}Intelligence.Notebook/notebook_content.py`
2. Add your source-specific intelligence class:

```python
# Fabric notebook source

class {PROJECT}Intelligence:
    """{PROJECT} API intelligence - schemas, dependencies, constraints."""
    
    SCHEMAS = {
        "entity1": {
            "entity": "entity1",
            "endpoint": "/entity1",
            "method": "GET",
            "schema": {...}
        }
    }
    
    READ_ENDPOINTS = {
        "entity1": {
            "endpoint": "/entity1",
            "method": "GET",
            ...
        }
    }
    
    DEPENDENCIES = {...}
    CONSTRAINTS = {...}
```

### Step 4: Configure Contract

Update `config/contracts/source.contract.yaml`:

```yaml
version: "1.0.0"
stage: "source"
source: "{PROJECT}"
purpose: "SPECTRA-grade source stage for {PROJECT}"

inputs:
  auth_method: "apiToken"  # or "oauth2", "basic", etc.
  variable_library: "{PROJECT}Variables"
  variables:
    - "base_url"
    - "api_token"
    - "base_path"
```

### Step 5: Setup Fabric Workspace

1. **Create Workspace** in Fabric UI
2. **Create Lakehouse** (enable Schema Support!)
3. **Connect to Git** (workspace settings → Git integration)
4. **Sync notebooks** (should happen automatically)

### Step 6: Configure Variables

Add to Fabric Variable Library (`{PROJECT}Variables`):

- `SOURCE_SYSTEM`: `{PROJECT}`
- `SOURCE_NAME`: `Your Source System`
- `BASE_URL`: `https://api.example.com`
- `BASE_PATH`: `/api/v1`
- `API_TOKEN`: `your-token-here` (secret)

### Step 7: Test Source Stage

1. Run `source{PROJECT}.Notebook`
2. Verify connectivity
3. Check `Tables/source/` tables created
4. Review `Tables/source/portfolio` for system overview

## Template Structure Explained

### Core Components

- **spectraSDK.Notebook**: Generic SPECTRA SDK (shared across all projects)
- **{PROJECT}Intelligence.Notebook**: Source-specific intelligence (you create this)
- **7-stage notebooks**: Minimal skeletons ready for customization

### What's Generic

- SDK classes (`NotebookSession`, `SourceStageHelpers`, etc.)
- Notebook structure (7-call pattern)
- Pipeline wiring
- Variable Library pattern
- Contract/manifest structure

### What You Customize

- Intelligence class (source-specific schemas, endpoints, dependencies)
- Contract files (source system configuration)
- API call implementations (if needed)
- Business logic in later stages

## Best Practices

1. **Keep SDK generic**: Don't add source-specific code to `spectraSDK.Notebook`
2. **Use intelligence notebook**: Put all source-specific knowledge in `{PROJECT}Intelligence.Notebook`
3. **Metadata-driven**: Prefer contracts/manifests over hardcoded values
4. **Test incrementally**: Start with Source, then Prepare, then Extract
5. **Document discoveries**: Update intelligence as you learn about the API

## Troubleshooting

### Git Sync Issues
- Ensure `.platform` files are present
- Check notebook prologue: `# Fabric notebook source`
- Remove any README.md files from notebook directories

### SDK Not Found
- Ensure `spectraSDK.Notebook` exists
- Check `%run spectraSDK` is at top of notebooks
- Verify SDK is synced to Fabric

### Variable Library Not Found
- Create Variable Library in Fabric UI
- Name must match: `{PROJECT}Variables`
- Add required variables

## Next Steps

After Source stage works:
1. Customize Prepare stage for your schemas
2. Build Extract stage based on endpoints
3. Implement Clean/Transform/Refine as needed
4. Create Analyse stage for reporting

See [7-STAGE-PIPELINE-GUIDE.md](docs/7-STAGE-PIPELINE-GUIDE.md) for detailed methodology.

