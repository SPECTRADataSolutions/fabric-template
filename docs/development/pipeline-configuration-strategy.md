# Pipeline Configuration Strategy

**Date:** 2025-12-05  
**Status:** 📋 Proposal  
**Purpose:** Standardize how we configure different pipeline execution modes (production, test, debug) without using Git branches

---

## 🎯 Objective

Instead of using Git branches for different configurations, use **pipeline parameters** and **different pipeline definitions** to enable:
- **Production pipelines** - Clean execution, minimal logging
- **Test pipelines** - Full validation suite, comprehensive checks
- **Debug pipelines** - Verbose logging, centralized log aggregation

---

## ✅ Recommended Approach: Pipeline Parameters (Not Branches)

### Why Not Branches?

**Branches are problematic:**
- ❌ Branch management overhead
- ❌ Risk of divergence
- ❌ Fabric sync complexity
- ❌ Configuration should be runtime, not compile-time
- ❌ Harder to compare/test different modes

**Pipeline parameters are better:**
- ✅ Single source of truth (main branch)
- ✅ Runtime configuration flexibility
- ✅ Easy to switch modes in Fabric UI
- ✅ Can override parameters per run
- ✅ No Git complexity

---

## 🏗️ Architecture

### 1. Single Notebook, Multiple Configurations

**Notebook stays on `main` branch:**
```python
# Parameters (defaults for interactive mode)
bootstrap: bool = True
backfill: bool = False  
preview: bool = False
test: bool = False  # Comprehensive validation
```

**Pipeline passes parameters:**
```json
{
  "parameters": {
    "bootstrap": { "type": "bool", "defaultValue": true },
    "backfill": { "type": "bool", "defaultValue": false },
    "preview": { "type": "bool", "defaultValue": false },
    "test": { "type": "bool", "defaultValue": false }
  }
}
```

### 2. Pipeline Configurations

Create **multiple pipeline definitions** for different purposes:

#### **2.1. Production Pipeline** (`zephyrPipeline.DataPipeline/pipeline-content.json`)
```json
{
  "parameters": {
    "bootstrap": { "defaultValue": false },  // Don't bootstrap in prod
    "backfill": { "defaultValue": false },
    "preview": { "defaultValue": false },
    "test": { "defaultValue": false }  // No tests in prod
  }
}
```

#### **2.2. Test Pipeline** (`zephyrPipeline-test.DataPipeline/pipeline-content.json`)
```json
{
  "parameters": {
    "bootstrap": { "defaultValue": true },
    "backfill": { "defaultValue": false },
    "preview": { "defaultValue": true },  // Include preview samples
    "test": { "defaultValue": true }  // Run full validation suite
  }
}
```

#### **2.3. Debug Pipeline** (`zephyrPipeline-debug.DataPipeline/pipeline-content.json`)
```json
{
  "parameters": {
    "bootstrap": { "defaultValue": true },
    "backfill": { "defaultValue": false },
    "preview": { "defaultValue": true },
    "test": { "defaultValue": false },
    "centralized_logging": { "defaultValue": true }  // Send to central service
  }
}
```

---

## 📊 Parameter Matrix

| Parameter | Production | Test | Debug | Interactive |
|-----------|-----------|------|-------|-------------|
| `bootstrap` | ❌ false | ✅ true | ✅ true | ✅ true |
| `backfill` | ❌ false | ❌ false | ❌ false | ⚙️ manual |
| `preview` | ❌ false | ✅ true | ✅ true | ⚙️ manual |
| `test` | ❌ false | ✅ true | ❌ false | ⚙️ manual |
| `debug` | ❌ auto-off | ❌ auto-off | ✅ auto-on* | ✅ auto-on* |
| `centralized_logging` | ❌ false | ❌ false | ✅ true | ❌ false |

*Debug mode is automatically enabled in interactive mode, disabled in pipeline mode

---

## 🔧 Implementation

### Step 1: Update Notebook Parameter Handling

**Make parameters safe for pipeline string inputs:**
```python
# ══ 1. PARAMETERS ═══════════════════════════════════════════════════ SPECTRA

# Handle both bool and string inputs from pipeline
_bootstrap = globals().get("bootstrap", True)
bootstrap = _bootstrap if isinstance(_bootstrap, bool) else str(_bootstrap).lower() in ("true", "1", "yes")

_backfill = globals().get("backfill", False)
backfill = _backfill if isinstance(_backfill, bool) else str(_backfill).lower() in ("true", "1", "yes")

_preview = globals().get("preview", False)
preview = _preview if isinstance(_preview, bool) else str(_preview).lower() in ("true", "1", "yes")

_test = globals().get("test", False)
test = _test if isinstance(_test, bool) else str(_test).lower() in ("true", "1", "yes")
```

**Or keep current approach (Python type annotations work if Fabric passes proper types):**
```python
bootstrap: bool = True
backfill: bool = False
preview: bool = False
test: bool = False
```

### Step 2: Create Pipeline Variants

Create separate pipeline files:
- `zephyrPipeline.DataPipeline/pipeline-content.json` (production)
- `zephyrPipeline-test.DataPipeline/pipeline-content.json` (test)
- `zephyrPipeline-debug.DataPipeline/pipeline-content.json` (debug)

### Step 3: Centralized Logging Integration

**Add to SDK when `centralized_logging=True`:**
```python
class CentralizedLogger:
    """Send logs to central SPECTRA monitoring service."""
    
    @staticmethod
    def send_log_entry(
        level: str,
        message: str,
        context: dict,
        logger: 'SPECTRALogger'
    ):
        """Send log entry to central service (async, non-blocking)."""
        # Implementation: Discord webhook, Delta table, or central service
        pass
```

---

## 🚀 Usage in Fabric

### Running Different Modes

**1. Production Run:**
- Select `zephyrPipeline` in Fabric
- Parameters already set to production defaults
- Run pipeline

**2. Test Run:**
- Select `zephyrPipeline-test` in Fabric
- Parameters already set to test defaults
- Validation suite runs automatically

**3. Debug Run:**
- Select `zephyrPipeline-debug` in Fabric
- Verbose logging + centralized log aggregation
- All diagnostic outputs enabled

**4. Override Parameters (Any Pipeline):**
- Click "Run with parameters"
- Override any parameter for one-off runs
- Example: Run production pipeline with `test=True` for validation

---

## 📝 Alternative: Environment-Based Configuration

If you prefer environments over multiple pipelines:

**Fabric Environment Variables:**
- Set `PIPELINE_MODE=production` in production environment
- Set `PIPELINE_MODE=test` in test environment
- Set `PIPELINE_MODE=debug` in debug environment

**Notebook reads from environment:**
```python
import os
pipeline_mode = os.getenv("PIPELINE_MODE", "production")

if pipeline_mode == "test":
    test = True
    preview = True
elif pipeline_mode == "debug":
    test = False
    preview = True
    # Enable centralized logging
```

---

## 🔍 Centralized Logging Integration

### Option 1: Discord Webhooks (Quick)

**When `centralized_logging=True` or `debug=True`:**
- Send critical logs to Discord channel
- Non-blocking async operation
- Immediate alerts for failures

### Option 2: Delta Table Logging (Structured)

**Store all logs in `monitor.logs` table:**
- Structured log entries
- Queryable via SQL
- Historical analysis

### Option 3: Central SPECTRA Service (Future)

**Dedicated `monitor` service:**
- Centralized log aggregation
- Real-time dashboards
- Alert management

---

## 🎯 Recommendation

**Use Pipeline Parameters + Multiple Pipeline Definitions:**

✅ **Advantages:**
- Single notebook codebase (no branch complexity)
- Easy to switch modes in Fabric UI
- Parameters can be overridden per run
- Clear separation of concerns
- SPECTRA-grade organization

✅ **Implementation:**
1. Keep current notebook on `main` branch
2. Create 3 pipeline variants (production, test, debug)
3. Add `centralized_logging` parameter support
4. Implement Discord webhook integration for critical events

---

## 📋 Next Steps

1. ✅ Update notebook to handle `test` parameter (DONE)
2. ⏳ Update pipeline to pass `test` parameter (IN PROGRESS)
3. ⏳ Create pipeline variants (production, test, debug)
4. ⏳ Add centralized logging support to SDK
5. ⏳ Implement Discord webhook integration
6. ⏳ Document pipeline usage in README

