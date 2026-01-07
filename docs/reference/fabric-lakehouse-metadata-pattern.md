# Fabric Lakehouse Metadata Pattern

**Date:** 2025-12-04  
**Discovery:** Lakehouse metadata configuration controls schema auto-creation behavior

---

## The Problem

Attempting to register Delta tables with schema-qualified names fails:

```python
spark.sql("CREATE TABLE IF NOT EXISTS source.endpoints USING DELTA LOCATION 'Tables/source/endpoints'")
# Error: [SCHEMA_NOT_FOUND] The schema `source` cannot be found
```

---

## The Root Cause

**Lakehouse metadata must have `defaultSchema` configured.**

### Jira (WORKING)

```json
{"defaultSchema":"dbo"}
```

### Zephyr (BROKEN - BEFORE FIX)

```json
{}
```

---

## The Solution

**Set `defaultSchema` in `lakehouse.metadata.json`:**

```json
{"defaultSchema":"dbo"}
```

**File Location:** `{workspace}/{lakehouseName}.Lakehouse/lakehouse.metadata.json`

---

## Why This Matters

With `defaultSchema` configured:
- ✅ `CREATE TABLE schema.table` can auto-create schemas dynamically
- ✅ Schema namespaces work correctly
- ✅ Tables register in metastore properly
- ✅ Fabric UI shows tables under correct schemas (not "Unidentified")

Without `defaultSchema`:
- ❌ All schema operations fail with `SCHEMA_NOT_FOUND`
- ❌ Can't create schemas programmatically
- ❌ Can't register tables with schema qualification
- ❌ Tables show as "Unidentified" folders

---

## Implementation Pattern

### 1. Configure Lakehouse (ONE TIME)

**File:** `{lakehouse}.Lakehouse/lakehouse.metadata.json`

```json
{"defaultSchema":"dbo"}
```

### 2. Write Delta Tables

```python
# Physical location matches schema structure
df.write.format("delta").save("Tables/source/endpoints")
df.write.format("delta").save("Tables/prepare/_schema")
df.write.format("delta").save("Tables/refine/dimProject")
```

### 3. Register in Metastore

```python
# Simple SQL registration works after defaultSchema is set
spark.sql("CREATE TABLE IF NOT EXISTS source.endpoints USING DELTA LOCATION 'Tables/source/endpoints'")
spark.sql("CREATE TABLE IF NOT EXISTS prepare._schema USING DELTA LOCATION 'Tables/prepare/_schema'")
spark.sql("CREATE TABLE IF NOT EXISTS refine.dimProject USING DELTA LOCATION 'Tables/refine/dimProject'")
```

**Schema auto-creates on first table registration** when `defaultSchema` is configured.

---

## Verification

Check your lakehouse metadata:

```bash
cat {workspace}/{lakehouse}.Lakehouse/lakehouse.metadata.json
```

**Expected:** `{"defaultSchema":"dbo"}`  
**If empty `{}`:** Add `defaultSchema` configuration

---

## SPECTRA Standard

**ALL Fabric lakehouses MUST have `defaultSchema` configured.**

**New Workspace Checklist:**
1. Create lakehouse in Fabric UI
2. Clone to local Git repo
3. **Add `{"defaultSchema":"dbo"}` to `lakehouse.metadata.json`**
4. Commit & push
5. Fabric syncs
6. Schema auto-creation enabled ✅

---

## Why `dbo`?

- **`dbo`** = "database owner" (SQL Server convention)
- Standard default schema in SQL databases
- Fabric inherits this from SQL Server lineage
- Could theoretically be any name, but `dbo` is the Fabric convention

---

## Related Patterns

- **Physical Path Structure:** `Tables/{schema}/{table}` 
- **Metastore Registration:** `CREATE TABLE {schema}.{table} USING DELTA LOCATION`
- **Schema Auto-Creation:** First table registration creates schema automatically

---

## Files Updated

- `Data/jira/jiraLakeHouseDev.Lakehouse/lakehouse.metadata.json` (already had this)
- `Data/zephyr/zephyrLakehouse.Lakehouse/lakehouse.metadata.json` (fixed)

---

## Lesson Learned

**Platform Lesson:** Fabric lakehouse metadata configuration is CRITICAL  
- Not documented clearly in Microsoft docs
- Easy to miss when creating new lakehouses
- Causes cryptic `SCHEMA_NOT_FOUND` errors
- **ONE-LINE FIX** that unblocks everything

**Add to onboarding checklist:** Every new lakehouse needs `defaultSchema` configured.


