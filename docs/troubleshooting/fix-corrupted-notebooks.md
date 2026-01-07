# Fix Corrupted Notebooks - Immediate Action Plan

**Status:** 🔴 Action Required  
**Date:** 2025-12-08  
**Issue:** Fabric reports "Missing or corrupted files" for:
- `/2-prepare/prepareZephyr.Notebook`
- `/contractValidation.Notebook`

---

## 🎯 Quick Fix Steps

### Step 1: Remove Corrupted Notebooks from Git

```powershell
cd Data/zephyr

# Remove corrupted notebooks
git rm -r 2-prepare/prepareZephyr.Notebook
git rm -r contractValidation.Notebook

# Commit deletion
git commit -m "fix: remove corrupted notebooks (will recreate properly in Fabric)"
git push
```

---

### Step 2: Create Notebooks Properly in Fabric

**Option A: Via Fabric CLI**

```powershell
# Load environment variables
$envFile = Join-Path (Resolve-Path ..).Path '.env'
Get-Content $envFile | Where-Object { $_ -notmatch '^\s*#' -and $_ -match '\S' } | ForEach-Object {
    $parts = $_ -split '=',2
    if ($parts.Length -eq 2) {
        Set-Item -Path ("Env:" + $parts[0].Trim()) -Value $parts[1]
    }
}

# Authenticate Fabric CLI
fab auth login `
  -u $env:SPECTRA_FABRIC_CLIENT_ID `
  -p $env:SPECTRA_FABRIC_CLIENT_SECRET `
  -t $env:SPECTRA_FABRIC_TENANT_ID

# Create notebooks
fab mkdir "zephyr.Workspace/prepareZephyr.Notebook"
fab mkdir "zephyr.Workspace/contractValidation.Notebook"
```

**Option B: Via Fabric UI**

1. Open Fabric workspace: `zephyr.Workspace`
2. Click **New** → **Notebook**
3. Create `prepareZephyr`
4. Repeat for `contractValidation`

---

### Step 3: Sync from Fabric to Git

1. In Fabric UI, open `zephyr.Workspace`
2. Click **Source Control** (Git icon)
3. Click **Sync** to download Fabric artifacts to Git
4. Verify notebooks now have proper `.platform` files with real `logicalId`

---

### Step 4: Restore Content to Notebooks

**Now that notebooks exist properly in Fabric, restore content:**

```powershell
# Copy content from backup or recreate from scratch
# Edit: 2-prepare/prepareZephyr.Notebook/notebook_content.py
# Edit: contractValidation.Notebook/notebook_content.py

# Commit content
git add 2-prepare/prepareZephyr.Notebook/notebook_content.py
git add contractValidation.Notebook/notebook_content.py
git commit -m "feat: restore notebook content after proper Fabric creation"
git push
```

---

### Step 5: Sync Back to Fabric

1. In Fabric UI, click **Source Control**
2. Click **Sync** to upload Git changes to Fabric
3. Verify notebooks appear correctly in Fabric UI

---

## ✅ Verification

**Check that notebooks are properly recognized:**

1. Open Fabric workspace
2. Verify `prepareZephyr` and `contractValidation` notebooks exist
3. Open each notebook - content should be visible
4. Check `.platform` file has real `logicalId` (not all zeros)

**Success criteria:**
- ✅ No "Missing or corrupted files" error
- ✅ Notebooks appear in Fabric UI
- ✅ `.platform` files have real `logicalId`
- ✅ Content is visible in notebooks

---

## 📝 Notes

- **Why this happened:** Notebooks were created directly in Git with placeholder IDs
- **Prevention:** Always create notebooks in Fabric first, then sync to Git
- **Reference:** See `docs/FABRIC-NOTEBOOK-CREATION-WORKFLOW.md` for canonical process

---

**Status:** 🔴 Action Required  
**Next Step:** Execute Step 1 (remove corrupted notebooks from Git)

