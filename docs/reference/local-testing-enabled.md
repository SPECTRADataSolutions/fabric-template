# Local Testing Enabled ✅

**Date:** 2025-12-02  
**Status:** Notebook now supports local testing!

---

## What Changed

### ✅ Automatic Environment Detection

The notebook **automatically detects** if it's running:

- **In Fabric:** Uses pipeline-injected credentials
- **Locally:** Loads from environment variables or `.env` file

**No code changes needed** - just set environment variables!

---

## Quick Start

### 1. Set Environment Variables

```powershell
# PowerShell
$env:DXC_ZEPHYR_BASE_URL="https://velonetic.yourzephyr.com"
$env:DXC_ZEPHYR_BASE_PATH="/flex/services/rest/latest"
$env:DXC_ZEPHYR_API_TOKEN="your-token-here"
```

### 2. Run Notebook Locally

**Option A: Jupyter Notebook**

```bash
cd Data/zephyr/sourceZephyr.Notebook
jupyter notebook
# Open notebook_content.py or convert to .ipynb
```

**Option B: Python Script**

```bash
python sourceZephyr.Notebook/notebook_content.py
```

**Option C: Run Test Scripts**

```bash
python scripts/test_all_endpoints.py
python scripts/extract_sample_100_rows.py
```

---

## How It Works

### Environment Detection

```python
# Automatically detects:
# - Fabric: Has notebookutils and Spark context
# - Local: Missing notebookutils or Spark

if running_locally:
    # Load from environment variables
    zephyr_base_url = os.environ.get("DXC_ZEPHYR_BASE_URL")
else:
    # Use pipeline-injected credentials
    pass  # Already injected
```

### Credential Loading Priority

1. **Fabric Mode:** Pipeline injection (Variable Library)
2. **Local Mode:** Environment variables (`DXC_ZEPHYR_*`)
3. **Local Mode (fallback):** `.env` file (if python-dotenv installed)

---

## What Works Locally

### ✅ Fully Supported

- **API Testing** - All REST API calls work perfectly
- **Endpoint Health Checks** - Test connectivity
- **Data Extraction** - Fetch projects, releases, cycles, test cases
- **Hierarchical Validation** - Test API dependencies
- **Error Handling** - All validation logic works

### ⚠️ Limited (Requires Spark)

- **Delta Lake Writes** - Requires Spark/Delta runtime
- **PySpark Operations** - DataFrame transformations
- **Lakehouse Integration** - Fabric-specific

**Workaround:** For local testing, focus on API logic. Use CSV/JSON for data storage if needed.

---

## Example Local Test

```bash
# 1. Set credentials
$env:DXC_ZEPHYR_BASE_URL="https://velonetic.yourzephyr.com"
$env:DXC_ZEPHYR_BASE_PATH="/flex/services/rest/latest"
$env:DXC_ZEPHYR_API_TOKEN="ccef8f5b690eb973d5d8ef191a8f1d65f9b85860"

# 2. Run notebook (or test scripts)
cd Data/zephyr
python scripts/test_all_endpoints.py

# 3. Output shows:
# 🔧 LOCAL TESTING MODE DETECTED
#    Loading credentials from environment variables...
#    ✓ base_url: SET
#    ✓ base_path: SET
#    ✓ api_token: SET
```

---

## Troubleshooting

### Error: "Missing credentials"

**Fix:** Set environment variables:

```powershell
$env:DXC_ZEPHYR_BASE_URL="..."
$env:DXC_ZEPHYR_BASE_PATH="..."
$env:DXC_ZEPHYR_API_TOKEN="..."
```

### Error: "NameError: name 'spark' is not defined"

**Cause:** Spark not available locally (expected!)

**Fix:** This is normal - notebook handles it gracefully. Spark operations are skipped in local mode.

### Credentials Not Loading

**Check:**

1. Variables set in current session? `echo $env:DXC_ZEPHYR_BASE_URL`
2. Restart terminal/Jupyter after setting variables
3. Check `.env` file exists and has correct values

---

## Parameter Tag Warning

**⚠️ Important:** When syncing git → Fabric, you MUST re-toggle the parameter cell tag!

**After every git sync:**

1. Open notebook in Fabric UI
2. Click Cell 1 (...) menu
3. Select "Toggle parameter cell"
4. Verify "parameters" tag appears

**Local testing doesn't need this** - tag is only for Fabric pipeline injection.

---

## Full Documentation

See **`Data/zephyr/docs/LOCAL-TESTING-GUIDE.md`** for:

- Complete setup instructions
- Jupyter configuration
- Converting .py to .ipynb
- Spark limitations and workarounds
- Best practices

---

## Next Steps

1. **Set environment variables** (see Quick Start above)
2. **Run test script** to verify credentials work:
   ```bash
   python scripts/test_all_endpoints.py
   ```
3. **Open in Jupyter** for interactive testing
4. **Test API calls** - all REST operations work locally
5. **Push to Fabric** for final validation (with Spark/Delta)

---

**Status:** ✅ Ready for local testing!  
**Documentation:** `docs/LOCAL-TESTING-GUIDE.md`  
**Support:** See troubleshooting section above
