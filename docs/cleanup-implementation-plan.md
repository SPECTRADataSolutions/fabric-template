# Source Notebook Cleanup - Implementation Plan

**Date:** 2025-12-05  
**Status:** Ready for Implementation

---

## ✅ Completed

1. **Endpoint Catalog Generated** - All 228 endpoints parsed and categorised
2. **SDK Enhanced** - Added `DeltaTable.register()` method to SDK
3. **Analysis Complete** - All legacy fields and bad practices identified

---

## 🔧 Implementation Steps

### Step 1: Simplify Source Table

**Current:** 9 fields (mostly redundant)  
**New:** 3 fields (minimal audit trail)

```python
# OLD (9 fields - redundant)
df_source = spark.createDataFrame([
    Row(
        source_system=session.ctx["source_system"],
        source_name=session.ctx["source_name"],  # In Variable Library
        base_url=session.ctx["base_url"],        # In Variable Library
        base_path=session.ctx["base_path"],      # In Variable Library
        full_url=session.ctx["full_url"],        # Derived from above
        workspace_id=session.environment.workspace_id,  # Runtime
        lakehouse_id=session.environment.lakehouse_id,  # Runtime
        lakehouse_name=session.environment.lakehouse_name,  # Runtime
        last_updated=datetime.utcnow(),
    )
])

# NEW (3 fields - minimal audit)
df_source = spark.createDataFrame([
    Row(
        source_system=session.ctx["source_system"],
        contract_version="1.0.0",  # From contract
        last_updated=datetime.utcnow(),
    )
])
```

### Step 2: Enhance Config Table

**Current:** 2 fields  
**New:** 7 fields (comprehensive runtime context)

```python
df_config = spark.createDataFrame([
    Row(config_key="execution_mode", config_value="pipeline" if session.pipeline.is_active else "interactive", last_updated=datetime.utcnow()),
    Row(config_key="operation_type", config_value=session.pipeline.operation_type, last_updated=datetime.utcnow()),
    Row(config_key="notebook_name", config_value=session.ctx["notebook_name"], last_updated=datetime.utcnow()),
    Row(config_key="stage", config_value=session.ctx["stage"], last_updated=datetime.utcnow()),
    Row(config_key="sdk_version", config_value="0.3.0", last_updated=datetime.utcnow()),
    Row(config_key="bootstrap_enabled", config_value=str(session.params["bootstrap"]), last_updated=datetime.utcnow()),
    Row(config_key="preview_enabled", config_value=str(session.params["preview"]), last_updated=datetime.utcnow()),
])
```

### Step 3: Load All 228 Endpoints

**Current:** 5 hardcoded endpoints  
**New:** Load from generated catalog

```python
# Load from generated catalog
import sys
sys.path.append("/lakehouse/default/Files/scripts")  # Or load from notebook path
from endpoints_catalog import ENDPOINTS_CATALOG

# Write all 228 endpoints
df_endpoints = spark.createDataFrame([Row(**ep) for ep in ENDPOINTS_CATALOG])
session.delta.write(df_endpoints, "source.endpoints", "Tables/source/endpoints")
session.delta.register("source.endpoints", "Tables/source/endpoints")
```

### Step 4: Remove Inline Functions

**Remove:**
- `register_delta_table()` function (now in SDK)

**Replace with:**
- `session.delta.register(table_name, path)`

### Step 5: Remove Hardcoded Values

**Remove:**
- `first_project_id = 44` (hardcoded)

**Replace with:**
- Use first project from API response

```python
# Get first project dynamically
projects = response.json()
first_project = projects[0] if projects else None
if first_project:
    first_project_id = first_project['id']
```

### Step 6: Parameterise Sample Limits

**Current:** `[:10]` (magic number)  
**New:** Parameter from session params

```python
sample_limit = session.params.get("sample_limit", 10)
projects = response.json()[:sample_limit]
```

---

## 📊 Expected Outcomes

- **Source table:** 9 fields → 3 fields (67% reduction)
- **Config table:** 2 fields → 7 fields (250% increase in context)
- **Endpoints:** 5 → 228 (all endpoints catalogued)
- **Inline functions:** 1 → 0 (moved to SDK)
- **Hardcoded values:** 2 → 0 (all dynamic)

---

## 🎯 Success Criteria

- ✅ Source table minimal (3 fields only)
- ✅ Config table comprehensive (7 runtime context fields)
- ✅ All 228 endpoints in Delta
- ✅ Zero inline utility functions
- ✅ Zero hardcoded IDs/values
- ✅ SDK handles all shared logic

---

**Ready to implement!**

