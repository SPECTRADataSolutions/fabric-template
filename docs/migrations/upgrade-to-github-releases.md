# Upgrade Zephyr to Use GitHub Releases

**Date:** 2025-12-03  
**Goal:** Replace CustomLibraries with pip install from GitHub Releases

---

## What We're Changing

### Before (CustomLibraries)
```
zephyrEnvironment.Environment/Libraries/CustomLibraries/
├── spectra_core-0.9.0.whl          # Git-synced (bloat)
└── spectra_fabric_sdk-0.9.0.whl    # Git-synced (bloat)
```

**Issues:**
- Git bloat (100 KB binaries)
- Manual sync required
- 2-minute delay

---

### After (GitHub Releases)
```python
# In notebook: pip install from URLs
import subprocess
subprocess.run(["pip", "install", "--quiet",
    "https://github.com/SPECTRACoreSolutions/framework/releases/download/v0.9.0/spectra_core-0.9.0-py3-none-any.whl",
    "https://github.com/SPECTRADataSolutions/fabric-sdk/releases/download/v0.9.0/spectra_fabric_sdk-0.9.0-py3-none-any.whl"
])
```

**Benefits:**
- No git bloat
- Instant updates (change URL)
- Professional versioning

---

## Step-by-Step Guide

### Step 1: Wait for GitHub Releases (~2 mins)

**Check these URLs:**
- https://github.com/SPECTRACoreSolutions/framework/releases/tag/v0.9.0
- https://github.com/SPECTRADataSolutions/fabric-sdk/releases/tag/v0.9.0

**Look for:**
- ✅ Release page exists
- ✅ Wheel file attached
- ✅ "Pre-release" badge

**If not ready yet:** Wait for GitHub Actions to complete

---

### Step 2: Add Dependencies Cell to Notebook

**Location:** `Data/zephyr/sourceZephyr.Notebook/notebook_content.py`

**Add NEW CELL after parameters cell (after line 74):**

```python
# CELL ********************

# === Install SPECTRA Packages from GitHub Releases ===
# This cell installs the canonical SPECTRA packages from GitHub Releases
# Replaces CustomLibraries approach (no more git bloat!)

import subprocess
import sys

print("📦 Installing SPECTRA packages from GitHub Releases...")

# Package URLs
SPECTRA_CORE_URL = "https://github.com/SPECTRACoreSolutions/framework/releases/download/v0.9.0/spectra_core-0.9.0-py3-none-any.whl"
SPECTRA_FABRIC_URL = "https://github.com/SPECTRADataSolutions/fabric-sdk/releases/download/v0.9.0/spectra_fabric_sdk-0.9.0-py3-none-any.whl"

# Install packages
try:
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "--quiet", "--upgrade",
        SPECTRA_CORE_URL,
        SPECTRA_FABRIC_URL
    ], check=True)
    print("✓ spectra-core v0.9.0 installed")
    print("✓ spectra-fabric-sdk v0.9.0 installed")
except Exception as e:
    print(f"❌ Failed to install packages: {e}")
    raise

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

---

### Step 3: Test Locally (Optional)

```bash
# Test the install URLs work
pip install --quiet \
  "https://github.com/SPECTRACoreSolutions/framework/releases/download/v0.9.0/spectra_core-0.9.0-py3-none-any.whl" \
  "https://github.com/SPECTRADataSolutions/fabric-sdk/releases/download/v0.9.0/spectra_fabric_sdk-0.9.0-py3-none-any.whl"

python -c "from spectra_core import get_utc_now; print('✓ Works!')"
```

---

### Step 4: Commit and Sync to Fabric

```bash
cd Data/zephyr
git add sourceZephyr.Notebook/notebook_content.py
git commit -m "feat: install packages from GitHub Releases instead of CustomLibraries"
git push origin main
```

**Fabric will auto-sync in ~2 minutes**

---

### Step 5: Test in Fabric

**In Fabric UI:**
1. Open zephyrLakehouse workspace
2. Open sourceZephyr notebook
3. Run the dependencies cell
4. Should see:
   ```
   📦 Installing SPECTRA packages from GitHub Releases...
   ✓ spectra-core v0.9.0 installed
   ✓ spectra-fabric-sdk v0.9.0 installed
   ```
5. Run rest of notebook - imports should work

---

### Step 6: Remove CustomLibraries (Optional)

**Once confirmed working:**

```bash
cd Data/zephyr
rm -rf zephyrEnvironment.Environment/Libraries/CustomLibraries/*.whl
git commit -am "cleanup: remove CustomLibraries wheels (now using GitHub Releases)"
git push origin main
```

**Benefits:**
- Clean git history
- No more binary bloat
- Professional setup

---

## Troubleshooting

### Issue: pip install fails
**Symptoms:** "Could not find a version that satisfies the requirement..."

**Solutions:**
1. Check GitHub Releases exist (URLs above)
2. Check internet access in Fabric (should have it)
3. Try installing one at a time
4. Check for typos in URLs

---

### Issue: Import fails after install
**Symptoms:** "ModuleNotFoundError: No module named 'spectra_core'"

**Solutions:**
1. Check pip install succeeded (look for "✓" messages)
2. Restart Python kernel
3. Check wheel was actually installed: `!pip list | grep spectra`

---

### Issue: Slow notebook start
**Symptoms:** Dependencies cell takes 10-15 seconds

**Solutions:**
1. This is normal (pip install from internet)
2. Add caching (see Advanced section below)
3. Or keep CustomLibraries if speed critical

---

## Advanced: Caching

**Cache wheels in Lakehouse to speed up installs:**

```python
from pathlib import Path
import subprocess
import sys

CACHE_DIR = Path("/lakehouse/default/Files/wheels_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def install_with_cache(package_name, version, github_url):
    """Install wheel with lakehouse caching."""
    cache_file = CACHE_DIR / f"{package_name}-{version}-py3-none-any.whl"
    
    if cache_file.exists():
        # Install from cache (fast)
        subprocess.run([sys.executable, "-m", "pip", "install", str(cache_file)], check=True)
        print(f"✓ {package_name} v{version} (cached)")
    else:
        # Download to cache, then install
        subprocess.run([sys.executable, "-m", "pip", "download", "--dest", str(CACHE_DIR), github_url], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", str(cache_file)], check=True)
        print(f"✓ {package_name} v{version} (downloaded & cached)")

# Usage
install_with_cache("spectra-core", "0.9.0", SPECTRA_CORE_URL)
install_with_cache("spectra-fabric-sdk", "0.9.0", SPECTRA_FABRIC_URL)
```

**Performance:**
- First run: 5-10s (download)
- Subsequent runs: 1-2s (cached)

---

## Comparison

| Method | Start Time | Update Time | Git Bloat | Best For |
|--------|------------|-------------|-----------|----------|
| **CustomLibraries** | 0s (pre-loaded) | 2 mins (git sync) | Yes | Development |
| **GitHub Releases** | 5s (pip install) | 0s (change URL) | No | Production |
| **With Cache** | 1s (cached) | 0s (change URL) | No | Best of both |

---

## Recommendation

**Use GitHub Releases with caching:**
- ✅ Clean git history
- ✅ Fast after first run (cached)
- ✅ Easy updates
- ✅ Professional

---

## Summary

**To use GitHub Releases in Fabric:**
1. ✅ Wait for releases to complete (check URLs above)
2. ✅ Add dependencies cell to notebook (pip install from URLs)
3. ✅ Commit and sync to Fabric
4. ✅ Test in Fabric
5. ✅ Remove CustomLibraries (optional)

**Next:** I'll show you the exact cell to add once releases are complete!

