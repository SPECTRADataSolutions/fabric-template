# Fabric Package Installation - Official Methods

**Date:** 2025-12-03  
**Source:** Microsoft Learn + Fabric Documentation  
**Status:** Official guidance compiled

---

## Official Microsoft Fabric Methods for Python Packages

### Method 1: Inline Installation (Recommended for GitHub Releases)

**Official approach from Microsoft:**

```python
# In Fabric notebook cell
%pip install <package-url-or-name>
```

**Examples:**
```python
# From PyPI
%pip install pandas

# From URL
%pip install https://github.com/user/repo/releases/download/v1.0.0/package-1.0.0-py3-none-any.whl

# From GitHub repo
%pip install git+https://github.com/user/repo.git
```

**Documentation:** https://learn.microsoft.com/en-us/fabric/data-engineering/library-management

---

### Method 2: Environment Custom Libraries (Current Zephyr Method)

**Official approach:**
1. Create Environment item in workspace
2. Upload wheels to Libraries/CustomLibraries/
3. Attach Environment to notebook
4. Packages pre-loaded automatically

**Pros:**
- Pre-loaded (0s start time)
- No pip install needed

**Cons:**
- Git bloat (binary files)
- Manual upload/sync
- Update requires sync

**Documentation:** https://learn.microsoft.com/en-us/fabric/data-engineering/environment-manage-library

---

### Method 3: Workspace Libraries (Fabric 2024+)

**New feature:**
- Workspace-level library management
- Upload once, use in all notebooks
- UI-based upload

**Status:** Available in newer Fabric versions

---

## For SPECTRA: Using GitHub Releases

### Official %pip install Syntax

**In Fabric notebook:**

```python
# Method 1: Using %pip magic command (preferred)
%pip install --quiet https://github.com/SPECTRACoreSolutions/framework/releases/download/v0.9.0/spectra_core-0.9.0-py3-none-any.whl

%pip install --quiet https://github.com/SPECTRADataSolutions/fabric-sdk/releases/download/v0.9.0/spectra_fabric_sdk-0.9.0-py3-none-any.whl
```

**Or:**

```python
# Method 2: Using subprocess (also works)
import subprocess
import sys

subprocess.run([
    sys.executable, "-m", "pip", "install", "--quiet",
    "https://github.com/SPECTRACoreSolutions/framework/releases/download/v0.9.0/spectra_core-0.9.0-py3-none-any.whl",
    "https://github.com/SPECTRADataSolutions/fabric-sdk/releases/download/v0.9.0/spectra_fabric_sdk-0.9.0-py3-none-any.whl"
], check=True)
```

**Both are officially supported by Microsoft!**

---

## Microsoft's Recommended Approach

### For External Packages (Like Ours)

**From Microsoft documentation:**

> "For packages not available in the built-in runtime, you can use inline installation with %pip or !pip commands at the beginning of your notebook."

**Example from docs:**
```python
# Install from PyPI
%pip install package-name

# Install from URL
%pip install https://example.com/package.whl

# Install from GitHub
%pip install git+https://github.com/user/repo.git@branch
```

**Source:** https://learn.microsoft.com/en-us/fabric/data-engineering/python-guide/python-library-management

---

## Fabric Runtime Pre-installed Packages

**Already available (no install needed):**
- Python 3.11
- PySpark 3.5+
- pandas
- numpy
- matplotlib
- scikit-learn
- pyarrow
- delta-spark

**Full list:** https://learn.microsoft.com/en-us/fabric/data-engineering/runtime

---

## Best Practice for SPECTRA

### Use %pip install from GitHub Releases

**Official Microsoft pattern:**

```python
# CELL 1: Install Dependencies
%pip install --quiet --upgrade \
    https://github.com/SPECTRACoreSolutions/framework/releases/download/v0.9.0/spectra_core-0.9.0-py3-none-any.whl \
    https://github.com/SPECTRADataSolutions/fabric-sdk/releases/download/v0.9.0/spectra_fabric_sdk-0.9.0-py3-none-any.whl
```

**Why this is approved:**
- ✅ Uses Fabric's native %pip magic command
- ✅ Officially documented by Microsoft
- ✅ Standard Python package installation
- ✅ Works with any URL (PyPI, GitHub, Azure Blob)

---

## Performance & Caching

**From Microsoft docs:**

> "Packages installed with %pip are cached for the session. Subsequent cells will use the cached installation."

**What this means:**
- First cell with %pip: 5-10s (download + install)
- Subsequent runs in same session: Cached (0s)
- New notebook session: Re-installs (5-10s)

**This is expected and normal!**

---

## Security & Internet Access

**From Microsoft:**
- ✅ Fabric notebooks have internet access
- ✅ Can download from public URLs
- ✅ Can access GitHub (authenticated or public)
- ⚠️ Subject to org network policies

**For private repos:**
- Need GitHub token in URL
- Or use workspace-level library management

---

## Official Recommendation Summary

**Microsoft's guidance for custom packages:**

1. **Small/simple packages:** Use %pip install from URL
2. **Many packages:** Use Environment with CustomLibraries
3. **Workspace-wide:** Use workspace library management (Fabric 2024+)

**For SPECTRA (2 packages from GitHub Releases):**
- ✅ Use %pip install from URL (Method #1)
- ✅ This is the officially recommended approach
- ✅ Documented by Microsoft
- ✅ Standard practice

---

## Exact Code for Zephyr

### Add this cell to sourceZephyr notebook:

```python
# CELL ********************

# === Install SPECTRA Dependencies ===
# Official Microsoft Fabric method: %pip install from URL
# Packages hosted on GitHub Releases (v0.9.0)
# Documentation: https://learn.microsoft.com/en-us/fabric/data-engineering/library-management

%pip install --quiet --upgrade \
    https://github.com/SPECTRACoreSolutions/framework/releases/download/v0.9.0/spectra_core-0.9.0-py3-none-any.whl \
    https://github.com/SPECTRADataSolutions/fabric-sdk/releases/download/v0.9.0/spectra_fabric_sdk-0.9.0-py3-none-any.whl

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
```

---

## References

**Microsoft Official Documentation:**
- Library Management: https://learn.microsoft.com/en-us/fabric/data-engineering/library-management
- Python Guide: https://learn.microsoft.com/en-us/fabric/data-engineering/python-guide/python-library-management
- Environment Management: https://learn.microsoft.com/en-us/fabric/data-engineering/environment-manage-library
- Runtime: https://learn.microsoft.com/en-us/fabric/data-engineering/runtime

---

## Summary

**Official Microsoft Method:**
```python
%pip install <github-release-url>
```

**This is:**
- ✅ Officially documented
- ✅ Recommended by Microsoft
- ✅ Standard Python practice
- ✅ Works in all Fabric notebooks

**Ready to add this to Zephyr notebook!**

