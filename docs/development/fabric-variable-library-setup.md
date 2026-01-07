# Fabric Variable Library Setup

**FINAL PATTERN:** One Variable Library per source with clean variable names

**Variable Library:** `zephyrVariables`

---

## 🎯 All 7 Variables

### Metadata (4 variables)

| Name | Type | Value |
|------|------|-------|
| `SOURCE_SYSTEM` | String | `zephyr` |
| `SOURCE_NAME` | String | `Zephyr Enterprise` |
| `STAGE` | String | `source` |
| `NOTEBOOK_NAME` | String | `sourceZephyr` |

### API Configuration (3 variables)

| Name | Type | Value |
|------|------|-------|
| `BASE_URL` | String | `https://velonetic.yourzephyr.com` |
| `BASE_PATH` | String | `/flex/services/rest/latest` |
| `API_TOKEN` | String | `ccef8f5b690eb973d5d8ef191a8f1d65f9b85860` |

---

## 📋 Setup Steps

1. **Open Fabric** workspace
2. **Navigate** to `zephyrVariables` (Variable Library artifact)
3. **Sync from Git** (should create variables automatically from variables.json)
4. **Verify** all 7 variables appear
5. If not synced: **Manually add** using the table above

---

## ✨ Clean Namespace Pattern

```
zephyrVariables        ← Namespace
├── SOURCE_SYSTEM      ← Clean names (no prefixes!)
├── BASE_URL
└── API_TOKEN

jiraVariables          ← Separate namespace (future)
├── SOURCE_SYSTEM      ← Same clean names
├── BASE_URL
└── API_TOKEN
```

**SDK Usage:**
```python
session = NotebookSession("zephyrVariables")  # Picks the right library
```

**SPECTRA-grade: Clean, simple, obvious!** ✨

