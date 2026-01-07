# Fabric Schema & Table Registration Assessment

**Date:** 2025-12-04  
**Issue:** `CREATE SCHEMA` fails in Fabric, but Jira tables work fine

---

## Microsoft Fabric Recommendations

1. **Schemas organize tables logically** but `CREATE SCHEMA` is blocked in Fabric runtime
2. **Schema shortcuts** are supported for external data integration
3. **Best practice:** Let Fabric auto-create schemas through table registration

---

## Jira Pattern (WORKING)

### Physical Location
```
Tables/prepare/_schema
Tables/prepare/_endpoints  
Tables/prepare/_statusmap
```

### Registration Code
```python
def _ensure_table(tbl: str, path: str):
    spark.sql(f"CREATE TABLE IF NOT EXISTS {tbl} USING DELTA LOCATION '{path}'")

_ensure_table("prepare._schema", "Tables/prepare/_schema")
_ensure_table("prepare._endpoints", "Tables/prepare/_endpoints")
_ensure_table("prepare._statusmap", "Tables/prepare/_statusmap")
```

### Key Observations
- **NO explicit `CREATE SCHEMA prepare`** command
- **Schema auto-creates** when first table is registered
- **Pattern:** `Tables/{schema}/{table}` → registers as `{schema}.{table}`
- **Idempotent:** `CREATE TABLE IF NOT EXISTS` is safe to repeat

---

## Zephyr Current Pattern (BROKEN)

### What We Did Wrong
```python
# ❌ THIS FAILS - Fabric blocks CREATE SCHEMA
spark.sql("CREATE SCHEMA IF NOT EXISTS source")

# Then tried to register
register_delta_table("source.endpoints", "Tables/source/endpoints")
```

### Error
```
Py4JJavaError: Feature not supported on Apache Spark in Microsoft Fabric
RuntimeError: java.lang.reflect.InvocationTargetException
at com.microsoft.azure.trident.spark.TridentCoreProxy.failCreateDbIfTrident
```

---

## Root Cause

**We explicitly called `CREATE SCHEMA` which Fabric blocks.**  
**Jira never does this - it lets `CREATE TABLE` auto-create the schema.**

---

## Solution: Match Jira Pattern Exactly

### Fix 1: Remove Explicit Schema Creation

**Remove these lines:**
```python
# ❌ DELETE THIS
spark.sql("CREATE SCHEMA IF NOT EXISTS source")
log.info("  📂 Schema 'source' ready")
```

### Fix 2: Keep Simple Table Registration

**Keep this (it's correct):**
```python
def register_delta_table(table_name: str, path: str) -> None:
    """Register existing Delta table location in Spark metastore/catalog."""
    spark.sql(f"CREATE TABLE IF NOT EXISTS {table_name} USING DELTA LOCATION '{path}'")
    log.info(f"  📋 Registered: {table_name}")

# Register tables (schema auto-creates on first call)
register_delta_table("source.endpoints", "Tables/source/endpoints")
register_delta_table("source.sample_dimProject", "Tables/source/sample_dimProject")
# ... etc
```

---

## Implementation Checklist

- [ ] Remove `spark.sql("CREATE SCHEMA IF NOT EXISTS source")` from bootstrap section (line ~1550)
- [ ] Remove `spark.sql("CREATE SCHEMA IF NOT EXISTS source")` from sample tables section (line ~2426)
- [ ] Update `register_delta_table()` docstring to clarify schema auto-creation
- [ ] Test in Fabric
- [ ] Update `FABRIC-DELTA-TABLE-PATTERN.md` with correct pattern
- [ ] Commit & push

---

## Expected Behavior After Fix

1. **First table registration:** `source` schema auto-creates
2. **Subsequent registrations:** Use existing `source` schema
3. **Fabric UI:** Tables appear under "source" schema (not "Unidentified")
4. **Idempotent:** Safe to re-run without errors

---

## Documentation Updates Needed

1. **`FABRIC-DELTA-TABLE-PATTERN.md`**: Remove incorrect "schema creation" step
2. **`register_delta_table()` docstring**: Update to reflect auto-creation behavior
3. **Source stage patterns**: Add "schema auto-creation through table registration" as doctrine

---

## Lessons Learned

**Platform Lesson:** Fabric has opinionated schema management  
- **Don't try:** Explicit `CREATE SCHEMA` (blocked)
- **Do instead:** Let `CREATE TABLE schema.table` auto-create schema
- **Pattern:** Trust the platform's automatic behavior over manual control

