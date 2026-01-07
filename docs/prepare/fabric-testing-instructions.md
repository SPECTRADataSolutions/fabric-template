# Fabric Testing Instructions - prepareZephyr Intelligence-Powered

> **Date:** 2025-12-09  
> **Status:** ✅ Ready for Fabric Testing  
> **Pre-requisite:** Git sync complete

---

## 🎯 What You're

**First intelligence-powered Prepare stage notebook that loads API Intelligence Framework artifacts.**

---

## 📋 Step-by-Step Testing Instructions

### **Step 1: Sync Workspace (5 min)**

1. Open Fabric workspace: **Zephyr** (`16490dde-33b4-446e-8120-c12b0a68ed88`)
2. Navigate to workspace settings
3. Click **Git integration** → **Sync now**
4. Wait for sync to complete

**Expected:** `prepareZephyr.Notebook` should appear in workspace

---

### **Step 2: Verify Notebook Structure (2 min)**

1. Open `prepareZephyr` notebook in Fabric
2. Verify cells are present:
   - Cell 1: `%run spectraSDK`
   - Cell 2: Parameters (bootstrap, test)
   - Cell 3: Context (NotebookSession)
   - Cell 4: Execute (Load intelligence + create tables)
   - Cell 5: Validate
   - Cell 6: Record
   - Cell 7: Finalise

**Expected:** 7 cells following SPECTRA pattern

---

### **Step 3: Update Pipeline with Real Notebook ID (5 min)**

1. Copy notebook ID from `prepareZephyr` notebook URL in Fabric

   - URL format: `...notebooks/{notebook-id}?...`
   - Copy the GUID between `/notebooks/` and `?`

2. Open `zephyrPipeline.DataPipeline` in Fabric

3. Click **Edit** → Open JSON view

4. Find the `prepareZephyr` activity:

   ```json
   {
     "name": "prepareZephyr",
     "notebookId": "00000000-0000-0000-0000-000000000000" // Replace this
   }
   ```

5. Replace placeholder with real notebook ID

6. **Save pipeline**

**Alternative (Easier):**

- Open pipeline in visual editor
- Click `prepareZephyr` activity
- In settings, select `prepareZephyr` notebook from dropdown
- Fabric auto-populates the ID
- Save

---

### **Step 4: Verify Intelligence Files Present (2 min)**

In Fabric, navigate to workspace Files and verify:

```
intelligence/
├── schemas/
│   ├── release.json ✅
│   ├── cycle.json ✅
│   ├── requirement.json ✅
│   ├── requirement_folder.json ✅
│   └── testcase_folder.json ✅
├── dependencies.yaml ✅
└── quirks.yaml ✅
```

**If missing:** Run git sync again

---

### **Step 5: Run Pipeline (10 min)**

1. Open `zephyrPipeline.DataPipeline`
2. Click **Run**
3. Set parameters:
   - `bootstrap`: `true`
   - `backfill`: `false`
   - `test`: `false`
4. Click **Run**
5. Monitor execution

**Expected Duration:** ~5-10 minutes

---

### **Step 6: Verify Outputs (5 min)**

Once pipeline succeeds, verify tables were created:

1. Open **zephyrLakehouse**
2. Navigate to **Tables**
3. Verify these tables exist:

**Source tables (from sourceZephyr):**

- `source.portfolio` ✅
- `source.config` ✅
- `source.credentials` ✅
- `source.endpoints` ✅
- `source.sampleProjects` ✅
- `source.sampleReleases` ✅
- `source.sampleCycles` ✅

**Prepare tables (from prepareZephyr):** 👈 **NEW!**

- `prepare._schema` ✅ (Field metadata from intelligence)
- `prepare._dependencies` ✅ (Entity relationships from networkx)
- `prepare._constraints` ✅ (API limitations from quirks)

---

### **Step 7: Query Prepare Tables (5 min)**

Run these queries in Fabric to validate:

```sql
-- Check schema fields loaded from intelligence
SELECT entity, COUNT(*) as field_count
FROM prepare._schema
GROUP BY entity
ORDER BY entity;

-- Expected: 5 entities (release, cycle, requirement, requirement_folder, testcase_folder)
-- Expected: ~10-15 fields per entity

-- Check dependencies loaded from networkx
SELECT entity, dependsOn, requiredBy, isIndependent
FROM prepare._dependencies
ORDER BY entity;

-- Expected: 9 entities with dependency relationships

-- Check constraints loaded from quirks
SELECT constraintId, constraintType, entity, severity, workaroundStatus
FROM prepare._constraints
ORDER BY severity, constraintId;

-- Expected: 3 blockers, 1 bug, ~3 quirks
```

---

## ✅ Success Criteria

**Pipeline Run Successful If:**

1. ✅ Both `sourceZephyr` and `prepareZephyr` activities succeed
2. ✅ All 3 prepare tables created (`_schema`, `_dependencies`, `_constraints`)
3. ✅ Intelligence artifacts loaded (log shows: "Intelligence loaded: X fields, Y entities, Z constraints")
4. ✅ Tables queryable in Lakehouse
5. ✅ Row counts > 0 for all tables

---

## ❌ Troubleshooting

### **If prepareZephyr Fails:**

**Error: "FileNotFoundError: intelligence/schemas not found"**

- **Cause:** Intelligence artifacts not synced to Fabric
- **Fix:** Check git sync, verify files in workspace Files

**Error: "No module named 'yaml'"**

- **Cause:** PyYAML not installed in environment
- **Fix:** Add to environment: `%pip install pyyaml`

**Error: "Module 'pathlib' has no attribute..."**

- **Cause:** Path handling in Fabric vs local
- **Fix:** Notebook has `/Workspace` fallback logic

**Error: "Table 'prepare.\_schema' not found"**

- **Cause:** Validation trying to read table before creation
- **Fix:** Ensure `bootstrap=True` parameter

---

## 📊 What This Proves

**First intelligence-powered pipeline stage in SPECTRA:**

- ✅ API Intelligence Framework outputs feed Prepare stage
- ✅ No hardcoded schemas (loads from `genson` auto-generated files)
- ✅ No manual dependencies (loads from `networkx` graph)
- ✅ No scattered quirks (loads from consolidated `quirks.yaml`)
- ✅ Extract stage will have complete intelligence to work with

---

## 🚀 After Successful Test

**Once pipeline runs successfully:**

1. Update `pipeline-content.json` with real notebook ID
2. Commit updated pipeline to git
3. Create completion milestone
4. Ready to build Extract stage using Prepare intelligence!

---

**Status:** ✅ Ready for Fabric testing  
**Expected Duration:** 30-40 minutes total  
**Next:** Build Extract stage using intelligence from Prepare tables





