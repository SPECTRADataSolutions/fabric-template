# Add Zephyr Configuration to Fabric Environment

**NEW PATTERN:** One Fabric Environment with prefixed variables (not Variable Libraries)

**Environment:** Your Fabric Environment artifact (e.g., `fabricEnvironment`)

---

## 🎯 Variables to Add

**Add these 7 variables to Fabric Environment:**

### Metadata (Required)
```
ZEPHYR_SOURCE_SYSTEM = zephyr
ZEPHYR_SOURCE_NAME = Zephyr Enterprise
ZEPHYR_STAGE = source
ZEPHYR_NOTEBOOK_NAME = sourceZephyr
```

### API Configuration (Required)
```
ZEPHYR_BASE_URL = https://velonetic.yourzephyr.com
ZEPHYR_BASE_PATH = /flex/services/rest/latest
ZEPHYR_API_TOKEN = ccef8f5b690eb973d5d8ef191a8f1d65f9b85860
```

---

## 📋 Steps in Fabric UI

1. **Open Fabric** workspace
2. **Navigate** to your **Environment** artifact (not Variable Library!)
3. Click **"Environment variables"** or **"Configuration"**
4. Click **"+ New variable"** for each of the 7 variables above
5. Enter Name, Value for each
6. **Save** the Environment
7. **Restart Spark session** for changes to take effect

---

## 🎯 Why This Pattern?

**Before (Variable Library):**
```
zephyrVariables (artifact) - Zephyr config
jiraVariables (artifact) - Jira config
xeroVariables (artifact) - Xero config
```
❌ Multiple artifacts to manage
❌ Redundant metadata

**After (Environment Variables):**
```
One Fabric Environment:
  ZEPHYR_* - Zephyr config
  JIRA_* - Jira config (future)
  XERO_* - Xero config (future)
```
✅ Single source of truth
✅ One contract per source
✅ Easier to manage

**Prefix provides namespace isolation!**

---

## 🔄 Contract-Driven Population (Future)

Eventually, a script will populate these from `contract.yaml`:

```bash
# Read contract.yaml → Set Fabric Environment variables
python scripts/sync_contract_to_fabric.py --source zephyr
```

**For now:** Manual setup in Fabric UI.

---

## ✅ After Setup

**Notebook usage:**
```python
session = NotebookSession("ZEPHYR")  # Reads ZEPHYR_* env vars
session.load_context(bootstrap, backfill, preview, debug)
```

**SDK automatically reads:**
- `ZEPHYR_SOURCE_SYSTEM`
- `ZEPHYR_BASE_URL`
- `ZEPHYR_API_TOKEN`
- etc.

**Clean, consistent, SPECTRA-grade!** ✨

