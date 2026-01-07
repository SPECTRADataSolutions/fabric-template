# Setup Local Testing - Quick Guide

**Goal:** Install dependencies for local Zephyr notebook testing

---

## Option 1: Minimal Setup (Recommended)

**For API testing only (no Spark):**

```bash
pip install python-dotenv requests pyyaml
```

**What you get:**
- ✅ Load credentials from .env
- ✅ Test all REST API calls
- ✅ Run endpoint validation scripts
- ❌ No Spark/Delta (not needed for API testing)

**Time:** 30 seconds

---

## Option 2: Notebook Testing

**For Jupyter notebook testing:**

```bash
pip install python-dotenv requests pyyaml pandas jupyter
```

**What you get:**
- ✅ Everything from Option 1
- ✅ Jupyter notebook interface
- ✅ Pandas for data manipulation
- ❌ No Spark/Delta (use pandas instead)

**Time:** 2 minutes

---

## Option 3: Full Local Development

**For complete local Spark testing:**

```bash
pip install python-dotenv requests pyyaml pandas pyspark delta-spark jupyterlab pytest ruff
```

**What you get:**
- ✅ Everything from Option 2
- ✅ PySpark for DataFrame operations
- ✅ Delta Lake format support
- ✅ JupyterLab (modern interface)
- ✅ Testing and linting tools

**Time:** 5 minutes (PySpark is ~300MB)

---

## Quick Test

**After installing:**

```powershell
# 1. Set credentials
$env:DXC_ZEPHYR_BASE_URL="https://velonetic.yourzephyr.com"
$env:DXC_ZEPHYR_BASE_PATH="/flex/services/rest/latest"
$env:DXC_ZEPHYR_API_TOKEN="your-token-here"

# 2. Test python-dotenv is installed
python -c "import dotenv; print('✓ python-dotenv installed')"

# 3. Run test script
cd Data/zephyr
python scripts/test_all_endpoints.py
```

**Expected output:**
```
✓ python-dotenv installed
🔧 LOCAL TESTING MODE DETECTED
   Loading credentials from environment variables...
   ✓ base_url: SET
   ✓ base_path: SET
   ✓ api_token: SET
```

---

## Using requirements.txt

**Install from file:**

```bash
cd Data/zephyr
pip install -r requirements.txt
```

**Or install only essentials:**

```bash
pip install requests python-dotenv
```

---

## Conda Environment (Alternative)

**If using conda:**

```bash
# Create environment from Jira's env.yml (has python-dotenv)
conda env create -f ../jira/env.yml
conda activate spectraFramework

# Or install just python-dotenv
conda install -c conda-forge python-dotenv
```

---

## Verify Installation

```python
# Test all required packages
python -c "
import dotenv
import requests
import yaml
print('✓ All core packages installed')
print(f'  python-dotenv: {dotenv.__version__}')
print(f'  requests: {requests.__version__}')
print(f'  pyyaml: {yaml.__version__}')
"
```

---

## What Each Package Does

| Package | Purpose | Required For |
|---------|---------|--------------|
| **python-dotenv** | Load .env files | Local credential loading |
| **requests** | HTTP/REST API calls | All API testing |
| **pyyaml** | YAML parsing | Contract/manifest reading |
| **pandas** | Data manipulation | Local data testing |
| **jupyter** | Notebook interface | Interactive testing |
| **pyspark** | Spark operations | DataFrame testing |
| **delta-spark** | Delta Lake format | Delta table testing |

---

## Troubleshooting

### "No module named 'dotenv'"

```bash
pip install python-dotenv
```

### "No module named 'requests'"

```bash
pip install requests
```

### Already have some packages?

```bash
# Check what's installed
pip list | grep -E "dotenv|requests|pyyaml"

# Install only missing ones
pip install python-dotenv  # if missing
```

---

## Next Steps

1. **Install packages** (choose option above)
2. **Set environment variables** (see LOCAL-TESTING-GUIDE.md)
3. **Run test script** to verify setup
4. **Open Jupyter** for interactive testing (if installed)

---

**Recommended:** Start with Option 1 (minimal), add more as needed.

**Documentation:** See `docs/LOCAL-TESTING-GUIDE.md` for complete guide.

