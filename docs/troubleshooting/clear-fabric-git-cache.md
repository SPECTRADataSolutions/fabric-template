# Force Clear Fabric Git Cache - prepareZephyr

**Issue:** Fabric showing "missing or corrupted files" for prepareZephyr.Notebook
**Cause:** Cached old .platform schema in Fabric's Git integration
**Fix:** Force disconnect/reconnect Git to clear cache

---

## 🔧 Steps to Clear Fabric Git Cache

### **Option 1: Disconnect/Reconnect Git (Recommended)**

1. Open Fabric workspace: **Zephyr**
2. Navigate to **Workspace settings**
3. **Git integration** → **Disconnect**
4. **Confirm disconnect** (this does NOT delete anything in Git)
5. Wait 10 seconds
6. **Git integration** → **Connect to Git**
7. Re-select:
   - Organization: `SPECTRADataSolutions`
   - Repository: `zephyr`
   - Branch: `main`
   - Folder: `/` (root)
8. Click **Connect**
9. Wait for initial sync
10. **Sync now** to pull latest

**Expected:** Fresh sync will pull correct `.platform` file

---

### **Option 2: Force Update (Alternative)**

1. Open Fabric workspace: **Zephyr**
2. **Git integration** → **Source control**
3. Click **Undo all** (discards cached changes)
4. **Update all** (force pull from Git)

---

### **Option 3: Delete prepareZephyr in Fabric UI (Nuclear)**

1. Open Fabric workspace
2. Find `prepareZephyr` notebook (if it exists)
3. Delete it
4. **Git integration** → **Update all**
5. Fabric will recreate from Git

---

## ✅ Verification

After clearing cache and syncing:

1. ✅ No "missing or corrupted files" error
2. ✅ `prepareZephyr` notebook appears in workspace
3. ✅ Can open notebook in Fabric
4. ✅ Can add to pipeline

---

## 📋 What Was Fixed in Git

**Before (broken):**
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/platform/1.0.0/schema.json",
  "type": "Notebook",
  "displayName": "prepareZephyr",
  "logicalId": "00000000-0000-0000-0000-000000000000"
}
```

**After (working):**
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "Notebook",
    "displayName": "prepareZephyr",
    "description": "Prepare stage - Intelligence-powered schema and configuration tables"
  },
  "config": {
    "version": "2.0",
    "logicalId": "00000000-0000-0000-0000-000000000000"
  }
}
```

**Key Change:** Now matches `sourceZephyr` and `spectraSDK` schema format (gitIntegration 2.0.0)

---

**Status:** ✅ Git fixed, ready for Fabric cache clear  
**Recommendation:** Try Option 1 first (disconnect/reconnect)







