# Sync Template from Fabric Workspace

**Purpose:** Create template by syncing zephyr from Fabric workspace back to this repo.

This ensures the template has the exact structure Fabric expects (real IDs, proper metadata, etc.).

---

## Process

### Step 1: Sync Zephyr to Fabric Workspace

1. Go to Fabric workspace
2. Connect Git integration to zephyr repo
3. Sync zephyr repo to workspace
4. Fabric will create/update all notebooks with real IDs

### Step 2: Switch Git Integration to Template Repo

1. In Fabric workspace, go to Git integration settings
2. Change Git repository to: `SPECTRADataSolutions/fabric-template`
3. Fabric will sync workspace content to template repo

### Step 3: Verify Template Structure

After sync completes:
- All notebooks should have real `logicalId` values (not placeholders)
- Structure should match what Fabric created
- Ready to use as template

---

## Benefits

- ✅ Template has real Fabric IDs (not placeholders)
- ✅ Structure matches exactly what Fabric expects
- ✅ Any Fabric-specific metadata is correct
- ✅ Guaranteed to sync successfully

---

**Note:** This process creates the baseline. After this, we can add template features (placeholders, setup scripts, etc.) programmatically.

