# Recreate zephyrLakehouse with Schema Support

**Why:** Current zephyrLakehouse was created without "Enable Schemas" flag. To use proper `source._config` notation without backticks, need to recreate with schemas enabled.

---

## Prerequisites

- ✅ Backup current data (if any critical data exists)
- ✅ Note current lakehouse ID: `5cb93b81-8923-a984-4c5b-a9ec9325ae26`
- ✅ Workspace: `zephyr` (`16490dde-33b4-446e-8120-c12b0a68ed88`)

---

## Procedure

### Step 1: Delete Current Lakehouse (in Fabric UI)

1. Open Fabric → `zephyr` workspace
2. Find `zephyrLakehouse`
3. Right-click → **Delete**
4. Confirm deletion

### Step 2: Create New Lakehouse with Schemas

1. In `zephyr` workspace → **+ New** → **Lakehouse**
2. **Name:** `zephyrLakehouse` (exact same name)
3. **Description:** Copy from contract or use:
   ```
   Lakehouse that stores Zephyr raw landings and curated tables for downstream models and dashboards; populated by zephyrPipeline and governed by docs/source/procedures.md and manifest.json.
   ```
4. ⚠️  **CRITICAL:** Check **"Enable Schemas"** checkbox ← This is the key!
5. Click **Create**

### Step 3: Verify Schema Support

Create a test notebook cell:

```python
# Test schema creation
try:
    spark.sql("CREATE SCHEMA IF NOT EXISTS testsource")
    spark.sql("CREATE TABLE IF NOT EXISTS testsource.testconfig USING DELTA LOCATION 'Tables/test'")
    print("✅ Schema support ENABLED!")
except Exception as e:
    print(f"❌ Schema support NOT enabled: {e}")
```

Should see: `✅ Schema support ENABLED!`

### Step 4: Commit New Lakehouse to Git

1. In Fabric → **Git sync** → **Commit**
2. This updates `zephyrLakehouse.Lakehouse/.platform` with new `logicalId`
3. Pull changes locally

### Step 5: Update Notebook Dependencies

Update all notebooks that reference the old lakehouse ID:

```python
# Find notebooks with old ID
git grep "1d58e7f6-c136-432d-abed-57db0f6603af"

# Get new ID from .platform
cat zephyrLakehouse.Lakehouse/.platform | Select-String "logicalId"

# Update notebook metadata blocks
```

### Step 6: Update SDK (Remove Backticks)

Once schemas are enabled, update `spectraSDK.Notebook/notebook_content.py`:

```python
# OLD (with backticks - for non-schema lakehouses)
escaped_name = f"`{table_name}`"
spark.sql(f"CREATE TABLE IF NOT EXISTS {escaped_name} USING DELTA...")

# NEW (without backticks - for schema-enabled lakehouses)
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
spark.sql(f"CREATE TABLE IF NOT EXISTS {table_name} USING DELTA...")
```

### Step 7: Test End-to-End

1. Git sync all changes to Fabric
2. Run `sourceZephyr` with `bootstrap=True`
3. Verify tables appear under `dbo > source > _config`, `_source`, etc.
4. No schema errors should occur

---

## Rollback

If issues occur, the backtick pattern (current implementation) works fine without schemas. You can revert and continue using:

```python
CREATE TABLE IF NOT EXISTS `source._config` USING DELTA...
```

---

## Evidence

Document:
- Screenshots of schema checkbox during creation
- Test results showing `CREATE SCHEMA` success
- Updated notebook metadata with new lakehouse ID
- Successful `sourceZephyr` run with proper table registration

---

## Next

Follow standard Git workflow to sync new lakehouse and updated notebooks back to local repo.

