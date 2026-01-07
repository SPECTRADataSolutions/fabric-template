# Test prepareZephyr Pipeline - Quick Guide

**Date:** 2025-12-10  
**Status:** ✅ Ready for testing  
**Branch:** `fabric-sync-fix`

---

## 🎯 What Was Done

1. ✅ Created `prepareZephyr` notebook in Fabric UI
2. ✅ Fabric committed it to Git with real notebook ID: `2797eaec-7a04-a62b-4b96-ce0e0249b31b`
3. ✅ Added `prepareZephyr` to pipeline (runs after `sourceZephyr`)
4. ✅ Pushed updated pipeline to Git

---

## 📋 Testing Steps

### **Step 1: Sync Fabric** (2 min)

1. Go to Fabric workspace: **Zephyr**
2. **Git integration** → **Source control** → **Sync**
3. Fabric will pull the updated pipeline

**Expected:** Pipeline now shows 2 activities: `sourceZephyr` → `prepareZephyr`

---

### **Step 2: Run Pipeline** (10 min)

1. Open `zephyrPipeline`
2. Click **Run**
3. Set parameters:
   - `bootstrap`: `true`
   - `backfill`: `false`
   - `test`: `false`
4. Click **Run**
5. Monitor execution

**Expected Duration:** ~5-10 minutes

---

### **Step 3: Verify Outputs** (5 min)

Once pipeline succeeds, verify tables:

```sql
-- Check Source tables
SELECT * FROM source.config LIMIT 5;
SELECT * FROM source.endpoints LIMIT 5;

-- Check Prepare tables (NEW!)
SELECT entity, COUNT(*) as field_count
FROM prepare._schema
GROUP BY entity
ORDER BY entity;

SELECT entity, dependsOn, isIndependent
FROM prepare._dependencies
ORDER BY entity;

SELECT constraintId, constraintType, entity, severity
FROM prepare._constraints
ORDER BY severity, constraintId;
```

**Expected:**
- ✅ `prepare._schema` has 5 entities (release, cycle, requirement, requirement_folder, testcase_folder)
- ✅ `prepare._dependencies` has 9 entities with relationships
- ✅ `prepare._constraints` has blockers, bugs, quirks documented

---

## ✅ Success Criteria

**Pipeline run successful if:**

1. ✅ Both `sourceZephyr` and `prepareZephyr` activities succeed
2. ✅ All 3 prepare tables created
3. ✅ Tables queryable in Lakehouse
4. ✅ Row counts > 0 for all tables
5. ✅ Intelligence loaded (log shows: "Intelligence loaded: X fields, Y entities, Z constraints")

---

## 🎉 What This Proves

**First intelligence-powered pipeline stage working end-to-end:**

- ✅ API Intelligence Framework outputs feed Prepare stage
- ✅ No hardcoded schemas (loads from `genson` auto-generated files)
- ✅ No manual dependencies (loads from `networkx` graph)
- ✅ No scattered quirks (loads from consolidated constraints)
- ✅ Extract stage will have complete intelligence to work with

---

## 📖 Next Steps After Success

1. ⏭️ Build Extract stage using prepare intelligence
2. ⏭️ Query `prepare._schema` for field metadata
3. ⏭️ Query `prepare._dependencies` for relationships
4. ⏭️ Query `prepare._constraints` for known issues
5. ⏭️ Document completion milestone

---

**Status:** ✅ Ready for pipeline test  
**Confidence:** High - Fabric-native workflow, real notebook IDs, tested pattern







