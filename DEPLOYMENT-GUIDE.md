# Template Deployment Guide

## Current Status

### Git Repository
- ✅ **Local repository initialized**
- ⚠️ **Not pushed to GitHub yet**
- ⚠️ **No remote configured**

### Fabric Workspace
- ⚠️ **Not created yet** (template is local only)
- Will be created when template is used for a new project

### Git Integration
- ⚠️ **Cannot be done programmatically**
- Must be done via Fabric UI: Workspace Settings → Git integration

## Deployment Steps

### Step 1: Push to GitHub

#### Option A: Using GitHub CLI (if available)
```powershell
cd "C:\Users\markm\OneDrive\SPECTRA\Data\spectra-fabric-template"

# Create repository on GitHub
gh repo create SPECTRADataSolutions/fabric-template \
  --public \
  --description "SPECTRA-grade template for Microsoft Fabric workspaces with 7-stage pipeline methodology" \
  --template=false

# Add remote and push
git remote add origin https://github.com/SPECTRADataSolutions/fabric-template.git
git branch -M main
git push -u origin main
```

#### Option B: Manual GitHub Creation
1. Go to https://github.com/SPECTRADataSolutions
2. Click "New repository"
3. Name: `fabric-template`
4. Description: "SPECTRA-grade template for Microsoft Fabric workspaces"
5. **Don't initialize** (we already have files)
6. Click "Create repository"
7. Then run:
```powershell
git remote add origin https://github.com/SPECTRADataSolutions/fabric-template.git
git branch -M main
git push -u origin main
```

### Step 2: Mark as Template Repository

1. Go to repository on GitHub
2. Click **Settings**
3. Scroll to **Template repository** section
4. Check **"Template repository"** checkbox
5. Save

Now users can click **"Use this template"** button!

### Step 3: Create Fabric Workspace (Per Project)

**Note**: The template itself doesn't need a workspace. Workspaces are created when users create new projects from the template.

For testing the template:
1. Create new workspace in Fabric UI
2. Connect to Git (point to template repo or a test repo)
3. Sync notebooks
4. Verify structure works

## Git Integration Limitations

### What CAN Be Done Programmatically
- ✅ Create workspace: `fab mkdir {PROJECT}.Workspace`
- ✅ Create lakehouse: `fab mkdir {PROJECT}.Workspace/{PROJECT}Lakehouse.Lakehouse`
- ✅ Create pipeline: `fab mkdir {PROJECT}.Workspace/{PROJECT}Pipeline.DataPipeline`
- ✅ Upload notebooks: Via Git sync (after connection)

### What CANNOT Be Done Programmatically
- ❌ Connect workspace to GitHub (Fabric UI only)
- ❌ Configure Git integration settings (Fabric UI only)
- ❌ Set up authentication tokens (Fabric UI only)

### Workaround
1. Create workspace via CLI
2. Guide user to connect Git via UI (one-time setup)
3. After connection, everything syncs automatically

## Testing the Template

### Local Testing
```powershell
# Test setup script
.\scripts\setup-new-project.ps1 -ProjectName "testproject" -SourceSystem "TestAPI"

# Verify placeholders replaced
grep -r "{PROJECT}" . --exclude-dir=.git
```

### Fabric Testing
1. Create test repository from template
2. Create Fabric workspace
3. Connect workspace to test repo (UI)
4. Sync notebooks
5. Verify structure loads correctly

## Next Steps

1. **Push to GitHub** (see Step 1 above)
2. **Mark as template** (see Step 2 above)
3. **Test in new workspace** (verify structure works)
4. **Complete cleanup** (strip zephyr code after testing)
5. **Update documentation** (add any missing guides)

