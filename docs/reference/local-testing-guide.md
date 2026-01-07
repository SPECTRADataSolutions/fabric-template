# Local Testing Guide - Zephyr Notebooks

**Date:** 2025-12-02  
**Purpose:** Run Fabric notebooks locally for development and testing

---

## Quick Start

### 1. Set Environment Variables

```bash
# Windows PowerShell
$env:DXC_ZEPHYR_BASE_URL="https://velonetic.yourzephyr.com"
$env:DXC_ZEPHYR_BASE_PATH="/flex/services/rest/latest"
$env:DXC_ZEPHYR_API_TOKEN="your-token-here"

# Windows CMD
set DXC_ZEPHYR_BASE_URL=https://velonetic.yourzephyr.com
set DXC_ZEPHYR_BASE_PATH=/flex/services/rest/latest
set DXC_ZEPHYR_API_TOKEN=your-token-here

# Linux/Mac
export DXC_ZEPHYR_BASE_URL="https://velonetic.yourzephyr.com"
export DXC_ZEPHYR_BASE_PATH="/flex/services/rest/latest"
export DXC_ZEPHYR_API_TOKEN="your-token-here"
```

### 2. Or Use .env File

Create/edit `.env` in SPECTRA root (`C:\Users\markm\OneDrive\SPECTRA\.env`):

```env
DXC_ZEPHYR_BASE_URL=https://velonetic.yourzephyr.com
DXC_ZEPHYR_BASE_PATH=/flex/services/rest/latest
DXC_ZEPHYR_API_TOKEN=your-token-here
```

**Install python-dotenv (optional, for .env support):**

```bash
pip install python-dotenv
```

### 3. Run Notebook in Jupyter

```bash
# Navigate to notebook directory
cd Data/zephyr/sourceZephyr.Notebook

# Start Jupyter
jupyter notebook

# Or JupyterLab
jupyter lab

# Open notebook_content.py or convert to .ipynb
```

---

## Environment Detection

The notebook **automatically detects** if it's running locally or in Fabric:

- **Local Mode:** Loads from environment variables or .env file
- **Fabric Mode:** Uses pipeline-injected credentials

**No code changes needed** - just set environment variables!

---

## What Works Locally

### ✅ Fully Supported

1. **API Testing**

   - All REST API calls work
   - Endpoint health checks
   - Hierarchical validation

2. **Data Extraction**

   - Fetch projects, releases, cycles
   - Extract test cases
   - Sample data extraction

3. **Validation Logic**
   - Parameter validation
   - Data quality checks
   - Error handling

### ⚠️ Limited (Requires Spark)

1. **Delta Lake Writes**

   - `spark.write.format("delta").save(...)` requires Spark
   - **Workaround:** Save to CSV/JSON instead

2. **PySpark Operations**
   - DataFrame transformations
   - Spark SQL queries
   - **Workaround:** Use pandas for local testing

---

## Local Testing Workflow

### Option A: Full Notebook Test (API Only)

**Test all API logic without Spark:**

```python
# At top of notebook (after imports)
RUNNING_LOCALLY = True  # Set manually if needed

# Modify Delta writes to CSV for local testing
if RUNNING_LOCALLY:
    df.toPandas().to_csv("output/test.csv", index=False)
else:
    df.write.format("delta").mode("overwrite").save("Tables/test")
```

### Option B: Unit Test Scripts

**Test individual functions:**

```bash
# Run endpoint test script
python scripts/test_all_endpoints.py

# Run sample extraction
python scripts/extract_sample_100_rows.py

# Test hierarchical access
python scripts/extract_hierarchy_sample.py
```

### Option C: Jupyter + Mock Spark

**For full notebook testing:**

```python
# Mock Spark context for local testing
class MockSpark:
    def __init__(self):
        self.conf = MockConfig()
        self.sparkContext = MockSparkContext()

class MockConfig:
    def set(self, key, value):
        pass

class MockSparkContext:
    def defaultParallelism(self):
        return 1

# Set mock if running locally
if is_running_locally():
    spark = MockSpark()
    # Note: Delta writes still won't work, but DataFrame operations might
```

---

## Credentials Source Priority

The notebook checks credentials in this order:

1. **Pipeline Injection** (Fabric mode)

   - From Variable Library via `@pipeline().libraryVariables.*`

2. **Environment Variables** (Local mode)

   - `DXC_ZEPHYR_BASE_URL`
   - `DXC_ZEPHYR_BASE_PATH`
   - `DXC_ZEPHYR_API_TOKEN`

3. **`.env` File** (Local mode, if python-dotenv installed)

   - Loads from SPECTRA root `.env` file

4. **Parameter Defaults** (Last resort)
   - Empty strings (will fail validation)

---

## Example: Local Test Session

```bash
# 1. Set credentials
export DXC_ZEPHYR_BASE_URL="https://velonetic.yourzephyr.com"
export DXC_ZEPHYR_BASE_PATH="/flex/services/rest/latest"
export DXC_ZEPHYR_API_TOKEN="ccef8f5b690eb973d5d8ef191a8f1d65f9b85860"

# 2. Start Jupyter
cd Data/zephyr/sourceZephyr.Notebook
jupyter notebook

# 3. Open notebook
# - Convert notebook_content.py to .ipynb if needed
# - Or create new notebook and copy cells

# 4. Run cells
# - Cell 1: Parameters (auto-detects local mode)
# - Cell 2: Loads credentials from environment
# - Cell 3+: Run API tests, extraction, etc.

# 5. Test results
# - API calls succeed
# - Data extracted correctly
# - Validation passes
```

---

## Troubleshooting

### Error: "Missing credentials"

**Cause:** Environment variables not set

**Fix:**

```bash
# Check if variables are set
echo $DXC_ZEPHYR_BASE_URL  # Linux/Mac
echo $env:DXC_ZEPHYR_BASE_URL  # PowerShell

# Set them if missing
export DXC_ZEPHYR_BASE_URL="..."
```

---

### Error: "NameError: name 'spark' is not defined"

**Cause:** Spark context doesn't exist locally

**Fix:**

- **Option 1:** Comment out Spark-dependent code
- **Option 2:** Use pandas instead of PySpark
- **Option 3:** Test API logic only (no Delta writes)

---

### Error: "ImportError: No module named 'notebookutils'"

**Cause:** Running locally (this is expected!)

**Fix:** This is normal - notebook auto-detects local mode

---

### Credentials Still Empty After Setting Environment Variables

**Cause:** Environment variables not in current session

**Fix:**

```bash
# Verify they're set
env | grep DXC_ZEPHYR  # Linux/Mac
Get-ChildItem Env: | Where-Object {$_.Name -like "*ZEPHYR*"}  # PowerShell

# Restart terminal/Jupyter after setting
# Or set in Jupyter notebook directly:
import os
os.environ["DXC_ZEPHYR_BASE_URL"] = "..."
```

---

## Fabric vs Local Differences

| Feature              | Fabric             | Local                 |
| -------------------- | ------------------ | --------------------- |
| **Credentials**      | Pipeline injection | Environment variables |
| **Spark**            | Available          | Not available         |
| **Delta Lake**       | Full support       | Use CSV/JSON          |
| **Variable Library** | Available          | N/A                   |
| **Lakehouse**        | Available          | N/A                   |
| **API Calls**        | Works              | Works                 |
| **Data Extraction**  | Works              | Works (no Delta)      |

---

## Recommended Local Testing Strategy

### Phase 1: API Logic Testing (No Spark)

**Test all REST API operations:**

```python
# Focus on these cells:
# - Endpoint health checks
# - Hierarchical validation
# - Data extraction
# - Error handling

# Skip/comment out:
# - Spark DataFrame operations
# - Delta Lake writes
# - Lakehouse connections
```

### Phase 2: Full Notebook Test (With Mock Spark)

**If you need to test DataFrame logic:**

```python
# Install PySpark locally
pip install pyspark

# Create local Spark session
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()

# Note: Delta format still requires Delta Lake library
# Use CSV/Parquet instead for local testing
```

### Phase 3: Fabric Integration Test

**Final validation in Fabric:**

1. Push code to git
2. Sync to Fabric
3. Run from pipeline
4. Verify credentials injected correctly

---

## Converting .py to .ipynb for Jupyter

**Manual conversion:**

1. Create new Jupyter notebook
2. Copy each cell from `notebook_content.py`
3. Convert `# CELL ********************` markers to cell separators
4. Convert `# METADATA` comments (ignore for local testing)

**Or use converter script:**

```python
# convert_notebook.py
import json

def py_to_ipynb(py_file, ipynb_file):
    cells = []
    with open(py_file, 'r') as f:
        content = f.read()

    # Split by CELL markers
    cell_contents = content.split("# CELL ********************\n")

    for cell_content in cell_contents:
        if not cell_content.strip():
            continue
        # Determine cell type (code vs markdown)
        if cell_content.strip().startswith("# MARKDOWN"):
            cell_type = "markdown"
            cell_content = cell_content.replace("# MARKDOWN ********************\n", "")
        else:
            cell_type = "code"

        cells.append({
            "cell_type": cell_type,
            "metadata": {},
            "source": cell_content.splitlines(keepends=True)
        })

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open(ipynb_file, 'w') as f:
        json.dump(notebook, f, indent=2)

# Usage
py_to_ipynb("notebook_content.py", "notebook.ipynb")
```

---

## Best Practices

### 1. Test API Logic Locally First

**Before pushing to Fabric:**

- ✅ Run endpoint tests
- ✅ Validate data extraction
- ✅ Check error handling
- ✅ Test parameter combinations

### 2. Use Environment Variables

**Never hardcode credentials:**

- ❌ Bad: `zephyr_api_token = "abc123"`
- ✅ Good: `zephyr_api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN", "")`

### 3. Skip Spark-Dependent Code Locally

**Add conditional execution:**

```python
if not is_running_locally():
    # Spark/Delta operations
    df.write.format("delta").save(...)
else:
    # Local testing (CSV/JSON)
    df.toPandas().to_csv("output/test.csv")
```

### 4. Validate Credentials Early

**Fail fast if credentials missing:**

```python
if not zephyr_api_token:
    raise ValueError("Missing credentials - check environment variables")
```

---

## Quick Reference

### Environment Variables

```bash
DXC_ZEPHYR_BASE_URL      # Zephyr API base URL
DXC_ZEPHYR_BASE_PATH     # API path prefix
DXC_ZEPHYR_API_TOKEN     # Authentication token
```

### Local Testing Checklist

- [ ] Credentials set in environment or .env
- [ ] Jupyter installed and running
- [ ] Notebook opens successfully
- [ ] Parameters load from environment
- [ ] API calls succeed
- [ ] Data extraction works
- [ ] Spark-dependent code skipped/commented

### When to Test in Fabric

- Final validation after local testing
- Testing Spark/Delta operations
- Validating pipeline parameter injection
- Testing Variable Library integration

---

## Additional Resources

- **Notebook Parameters Standard:** `Core/framework/standards/NOTEBOOK-PARAMETERS-STANDARD.md`
- **Fabric Git Sync Guide:** `Data/zephyr/docs/FABRIC-GIT-SYNC-PROCEDURE.md` (coming soon)
- **Endpoint Testing:** `Data/zephyr/scripts/test_all_endpoints.py`
- **Sample Extraction:** `Data/zephyr/scripts/extract_sample_100_rows.py`

---

**Questions?** Check the troubleshooting section or review the notebook code comments.
