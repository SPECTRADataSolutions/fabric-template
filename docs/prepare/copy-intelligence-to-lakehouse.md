# Copy Intelligence to Lakehouse Files

## Problem
The `intelligence/` folder is in Git but Fabric doesn't sync it to `/Workspace` because it only syncs Fabric **items** (notebooks, lakehouses, pipelines), not regular folders.

## Solution
Copy intelligence files into the lakehouse Files folder where notebooks can access them.

## Steps

### 1. Upload intelligence files to lakehouse

**In Fabric:**
1. Open `zephyrLakehouse`
2. Go to **"Files"** section (left sidebar)
3. Create folder: `intelligence`
4. Create subfolder: `intelligence/schemas`
5. Upload files:
   - `dependencies.yaml` → `Files/intelligence/`
   - `quirks.yaml` → `Files/intelligence/`
   - `creation-order.yaml` → `Files/intelligence/`
   - `entities.yaml` → `Files/intelligence/`
   - `endpoints.yaml` → `Files/intelligence/`
   - All `*.json` files → `Files/intelligence/schemas/`

### 2. Update notebook path

Change the notebook to look in lakehouse Files instead of /Workspace:

```python
# OLD (doesn't work - /Workspace doesn't have non-item folders)
intelligence_path = Path("/Workspace/intelligence")

# NEW (works - lakehouse Files accessible)
intelligence_path = Path("/lakehouse/default/Files/intelligence")
```

### 3. Test

Run `prepareZephyr` notebook. Should see:
```
✅ Using Fabric workspace path: /lakehouse/default/Files/intelligence
📊 Loaded 40+ fields from 5 schema files
```

## Alternative: Keep in Git, use script to sync

Create a notebook cell that copies from workspace to lakehouse on first run.






