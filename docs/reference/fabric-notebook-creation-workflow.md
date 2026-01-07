# Fabric Notebook Creation Workflow - SPECTRA-Grade

**Status:** 🟢 Canonical  
**Date:** 2025-12-08  
**Purpose:** Define the correct workflow for creating Fabric notebooks that Fabric will recognize

---

## ⚠️ Problem: Direct Git Creation Fails

**Error from Fabric:**
```
Missing or corrupted files
DirectoryNames [/2-prepare/prepareZephyr.Notebook|/contractValidation.Notebook]
```

**Root Cause:** Notebooks created directly in Git have placeholder `logicalId: "00000000-0000-0000-0000-000000000000"` which Fabric doesn't recognize as valid artifacts.

---

## ✅ SPECTRA-Grade Solution: Create in Fabric First

**The ONLY way to create notebooks that Fabric recognizes:**

### Step 1: Create Notebook in Fabric (CLI or UI)

**Option A: Via Fabric CLI (Recommended - Automated)**

```powershell
# Set workspace and notebook name
$workspace = "zephyr.Workspace"
$notebookName = "prepareZephyr"  # or "contractValidation"

# Create the notebook in Fabric
fab mkdir "$workspace/$notebookName.Notebook"
```

**Option B: Via Fabric UI (Manual)**

1. Open Fabric workspace: `zephyr.Workspace`
2. Click **New** → **Notebook**
3. Name it: `prepareZephyr` (or `contractValidation`)
4. Click **Create**
5. **Important:** Don't add content yet - we'll sync from Git first

---

### Step 2: Sync from Fabric to Git

**This imports the proper `.platform` file with real `logicalId`:**

1. In Fabric UI, open the workspace
2. Click **Source Control** (Git icon in top bar)
3. Click **Sync** or **Pull** to download Fabric artifacts to Git
4. Verify `.platform` file now has a real `logicalId` (not all zeros)

**Expected `.platform` structure after sync:**

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "Notebook",
    "displayName": "prepareZephyr"
  },
  "config": {
    "version": "2.0",
    "logicalId": "a744c881-065a-8e92-4cbb-2f6620f5ce36"  // ← Real ID from Fabric
  }
}
```

---

### Step 3: Edit Content in Git

**Now that Fabric recognizes the notebook, edit the content:**

1. Edit `notebook_content.py` in Git with your code
2. Edit `.platform` if needed (but **never change `logicalId`**)
3. Commit changes to Git

---

### Step 4: Sync Back to Fabric

**Push your changes back to Fabric:**

1. In Fabric UI, click **Source Control**
2. Click **Sync** or **Push** to upload Git changes to Fabric
3. Verify notebook content appears in Fabric UI

---

## 🔧 Fixing Corrupted Notebooks

**If you already have notebooks with placeholder IDs:**

### Option 1: Delete and Recreate (Recommended)

```powershell
# 1. Delete from Git (they're corrupted anyway)
cd Data/zephyr
git rm -r 2-prepare/prepareZephyr.Notebook
git rm -r contractValidation.Notebook

# 2. Commit deletion
git commit -m "fix: remove corrupted notebooks, will recreate in Fabric"

# 3. Create properly in Fabric
$workspace = "zephyr.Workspace"
fab mkdir "$workspace/prepareZephyr.Notebook"
fab mkdir "$workspace/contractValidation.Notebook"

# 4. Sync from Fabric to Git (gets proper IDs)
# (Do this in Fabric UI: Source Control → Sync)

# 5. Edit content in Git and sync back
```

### Option 2: Manual ID Fix (Not Recommended)

**⚠️ Warning:** This is risky - Fabric may still reject if other system files are missing.

```powershell
# 1. Create notebook in Fabric first to get real ID
fab mkdir "zephyr.Workspace/prepareZephyr.Notebook"

# 2. Get the logicalId from Fabric
$fabricId = fab get "zephyr.Workspace/prepareZephyr.Notebook" -q id

# 3. Update .platform file in Git with real ID
# Edit: 2-prepare/prepareZephyr.Notebook/.platform
# Replace: "logicalId": "00000000-0000-0000-0000-000000000000"
# With:    "logicalId": "$fabricId"

# 4. Commit and sync to Fabric
```

**Note:** Even with correct `logicalId`, Fabric may still complain if other system files (like `definition.dib`) are missing. **Option 1 is safer.**

---

## 📋 SPECTRA-Grade Notebook Creation Checklist

**For every new notebook:**

- [ ] ✅ Create in Fabric first (`fab mkdir` or UI)
- [ ] ✅ Sync from Fabric to Git (gets proper `.platform` with real `logicalId`)
- [ ] ✅ Verify `.platform` has real `logicalId` (not all zeros)
- [ ] ✅ Edit `notebook_content.py` in Git
- [ ] ✅ Commit to Git
- [ ] ✅ Sync back to Fabric
- [ ] ✅ Verify notebook appears correctly in Fabric UI

**❌ Never:**
- Create `.platform` files manually with placeholder IDs
- Create notebook folders directly in Git without Fabric creation first
- Change `logicalId` after Fabric creates it

---

## 🔗 References

- **Playbook:** `Core/operations/playbooks/fabric/1-source/source.001-createSourceNotebook.md`
- **Fabric CLI Docs:** `fab mkdir` command
- **Git Integration:** Fabric Source Control sync workflow

---

## 💡 Why This Happens

**Fabric's artifact system requires:**

1. **`logicalId`** - Unique identifier assigned by Fabric (not user-generated)
2. **System files** - Internal metadata files Fabric manages (e.g., `definition.dib`)
3. **Fabric registration** - Artifact must exist in Fabric's metadata store

**Creating notebooks directly in Git:**
- ❌ No `logicalId` from Fabric → placeholder zeros
- ❌ Missing system files → Fabric can't recognize artifact
- ❌ Not registered in Fabric → sync fails

**Creating in Fabric first:**
- ✅ Fabric assigns real `logicalId`
- ✅ Fabric creates all system files
- ✅ Fabric registers artifact → sync works perfectly

---

**Version:** 1.0.0  
**Status:** 🟢 Canonical SPECTRA Pattern

