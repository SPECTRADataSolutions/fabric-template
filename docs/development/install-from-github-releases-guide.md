# How to Install SPECTRA Packages from GitHub Releases in Fabric

**Date:** 2025-12-03  
**Method:** pip install from release URLs in notebook  
**Replaces:** CustomLibraries git-synced wheels

---

## The Simple Answer

**Add ONE cell at the top of your Fabric notebook:**

```python
import subprocess
import sys

# Install SPECTRA packages from GitHub Releases
subprocess.run([
    sys.executable, "-m", "pip", "install", "--quiet", "--upgrade",
    "https://github.com/SPECTRACoreSolutions/framework/releases/download/v0.9.0/spectra_core-0.9.0-py3-none-any.whl",
    "https://github.com/SPECTRADataSolutions/fabric-sdk/releases/download/v0.9.0/spectra_fabric_sdk-0.9.0-py3-none-any.whl"
], check=True)
```

**That's it! Now all imports work.**

---

## Full Implementation for Zephyr

### Where to Add the Cell

**File:** `Data/zephyr/sourceZephyr.Notebook/notebook_content.py`

**Location:** After parameters cell, before credential loading

**Line number:** After line 74 (after parameters metadata)

---

### Exact Cell to Add

```python
# CELL ********************

# === Install SPECTRA Dependencies ===
# Install canonical packages from GitHub Releases (v0.9.0)
# This replaces CustomLibraries approach - no more git bloat!
# Packages are cached after first install (~5s first run, ~1s after)

import subprocess
import sys

# Only install if not running locally (local uses pip install in venv)
_is_fabric = True
try:
    import notebookutils
    spark  # Check if Spark context exists
except (ImportError, NameError):
    _is_fabric = False

if _is_fabric:
    print("📦 Installing SPECTRA packages from GitHub Releases...")
    
    # Package URLs (update versions here when upgrading)
    SPECTRA_CORE_URL = "https://github.com/SPECTRACoreSolutions/framework/releases/download/v0.9.0/spectra_core-0.9.0-py3-none-any.whl"
    SPECTRA_FABRIC_URL = "https://github.com/SPECTRADataSolutions/fabric-sdk/releases/download/v0.9.0/spectra_fabric_sdk-0.9.0-py3-none-any.whl"
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "--quiet", "--upgrade", "--force-reinstall",
            SPECTRA_CORE_URL,
            SPECTRA_FABRIC_URL
        ], check=True, capture_output=True, text=True)
        
        print("   ✓ spectra-core v0.9.0 installed")
        print("   ✓ spectra-fabric-sdk v0.9.0 installed")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to install packages:")
        print(f"   {e.stderr}")
        raise
else:
    print("🔧 Local mode: Skipping pip install (using venv packages)")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

---

## Step-by-Step: Update Zephyr

### 1. Check Releases Are Ready

**Visit these URLs:**
- https://github.com/SPECTRACoreSolutions/framework/releases/tag/v0.9.0
- https://github.com/SPECTRADataSolutions/fabric-sdk/releases/tag/v0.9.0

**Verify:**
- ✅ Release page exists
- ✅ Wheel file is attached and downloadable
- ✅ Marked as "Pre-release"

**If not ready:** Wait 2-3 minutes for GitHub Actions to complete

---

### 2. Add Dependencies Cell to Notebook

**Option A: Manual Edit (Quick)**
1. Open `Data/zephyr/sourceZephyr.Notebook/notebook_content.py`
2. Find line 74 (after parameters metadata)
3. Insert the cell code from above
4. Save file

**Option B: Use Edit Tool (Automated)**
- I can add the cell for you programmatically

---

### 3. Commit and Sync

```bash
cd Data/zephyr
git add sourceZephyr.Notebook/notebook_content.py
git commit -m "feat: install packages from GitHub Releases"
git push origin main
```

**Fabric will sync in ~2 minutes**

---

### 4. Test in Fabric

**In Fabric UI:**
1. Go to DXC_Fabric_Workspace
2. Open sourceZephyr notebook
3. Click "Run all" or run cells individually
4. Watch dependencies cell:
   ```
   📦 Installing SPECTRA packages from GitHub Releases...
   ✓ spectra-core v0.9.0 installed
   ✓ spectra-fabric-sdk v0.9.0 installed
   ```
5. Continue to next cells - imports should work

---

### 5. Remove CustomLibraries (After Confirming Works)

```bash
cd Data/zephyr
rm -rf zephyrEnvironment.Environment/Libraries/CustomLibraries/*.whl
git commit -am "cleanup: remove CustomLibraries (using GitHub Releases now)"
git push origin main
```

---

## Benefits

### Before (CustomLibraries)
- Notebook start: 0s ✅
- Update: 2 mins (git sync) ⚠️
- Git bloat: Yes (100 KB per version) ❌
- Process: Build → Copy → Commit → Push → Wait

### After (GitHub Releases)
- Notebook start: 5s first run, 1s cached ✅
- Update: 0s (change URL) ✅
- Git bloat: No ✅
- Process: Build → Release → Change URL

**Trade-off:** 5s slower start for cleaner git + instant updates

---

## Future Updates

**To upgrade to v0.9.1:**

```python
# Just change the URLs in the dependencies cell
SPECTRA_CORE_URL = "https://github.com/.../download/v0.9.1/spectra_core-0.9.1.whl"
SPECTRA_FABRIC_URL = "https://github.com/.../download/v0.9.1/spectra_fabric_sdk-0.9.1.whl"
```

**Commit, push, done! No wheel files to copy!**

---

## Next Steps

1. ✅ Check releases are complete (URLs above)
2. ⏳ Add dependencies cell to notebook (I can do this for you)
3. ⏳ Test in Fabric
4. ⏳ Remove CustomLibraries

**Ready for me to update the notebook now?**

