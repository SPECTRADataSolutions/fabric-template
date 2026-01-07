# Source Notebook Rebuild Context

**Date:** 2025-12-04  
**Action:** Rebuilding sourceZephyr notebook following SPECTRA-Grade Source Stage Standard  
**Backup:** `sourceZephyr.Notebook/notebook-content.BACKUP-*.py`

---

## 🎯 Why Rebuild?

**Problems with old implementation:**
1. ❌ 2549 lines (too complex)
2. ❌ Hardcoded workspace/lakehouse IDs
3. ❌ Missing metadata declarations
4. ❌ Missing stage activity logging
5. ❌ Missing vendor-specific health checks
6. ❌ Embedded 228 endpoints in code (1159 lines)
7. ❌ Complex credential loading logic
8. ❌ No clear separation of concerns

**New approach:**
- ✅ Start minimal (skeleton with TODOs)
- ✅ Build step-by-step following standard
- ✅ Use Fabric runtime context (not hardcoded)
- ✅ Use Variable Library for source config
- ✅ Implement each section incrementally
- ✅ Test as we go

---

## 📋 New Notebook Structure (11 Cells)

### Cell 1: Parameters
- `bootstrap`, `backfill`, `preview`, `debug`
- SPECTRA-Grade parameter family
- Must be toggled as "parameters" in Fabric

### Cell 2: Fabric Runtime Context
- Load from `spark.conf.get("trident.*")`
- workspace_id, lakehouse_id, lakehouse_name
- **Zero hardcoding**

### Cell 3: Source System Configuration
- Load from Variable Library
- source_system, source_name, base_url, api_token
- **From contract → Variable Library**

### Cell 4: Notebook Metadata (Inferred)
- notebook_name from `mssparkutils.env.getNotebookName()`
- stage from notebook_name
- _running_locally detection

### Cell 5: Initialize Logger
- Smart debug mode (auto-enable locally)
- Structured logging
- Start time tracking

### Cell 6: Validate Parameters
- Contradiction checking
- Auto-enable rules (bootstrap → preview)
- Parameter logging

### Cell 7: Create Configuration Tables
- TODO: Implement `create_source_tables()`
- Tables: _source, _credentials, _config

### Cell 8: Health Checks
- TODO: Implement `check_zephyr_auth()`
- TODO: Implement `check_zephyr_project_access()`
- TODO: Implement `check_zephyr_hierarchical_access()`
- runtime_cache for results

### Cell 9: Endpoint Bootstrap
- TODO: Implement endpoint bootstrap
- Only if `bootstrap=True`
- Load ENDPOINTS_DATA, write to Delta

### Cell 10: Preview Sample
- TODO: Implement sample extraction
- Only if `preview=True`
- Extract ~100 rows per dimension

### Cell 11: Stage Activity Logging
- TODO: Implement `log_stage_activity()`
- Write to Tables/log/sourcelog

### Cell 12: Summary
- Duration calculation
- Status reporting
- Completion message

---

## 🔧 Implementation Components to Add

### 1. Endpoint Bootstrap (from old notebook)

**Location:** Old notebook lines 99-1327 (ENDPOINTS_DATA)

**Pattern:**
```python
ENDPOINTS_DATA = {
    "source": "zephyrenterprisev3.apib",
    "count": 228,
    "endpoints": [...]
}

if bootstrap:
    # Convert to DataFrame
    # Write to Delta
    # Register table
```

**Status:** ✅ Pattern proven, needs to be re-added

---

### 2. Health Check Functions

**Pattern from Jira:**
```python
def check_zephyr_auth(base_url, api_token, runtime_cache):
    """Verify Zephyr API authentication."""
    # Test /serverInfo or /project endpoint
    # Update runtime_cache["result"]["capabilities"]
    pass

def check_zephyr_project_access(base_url, api_token, runtime_cache):
    """Verify can access projects."""
    # Test /project/details
    # Update runtime_cache["result"]["capabilities"]
    pass

def check_zephyr_hierarchical_access(base_url, api_token, runtime_cache):
    """Verify hierarchical access (project → release → cycle)."""
    # Test multi-level traversal
    # Update runtime_cache["result"]["capabilities"]
    pass
```

**Location:** Old notebook lines 1400-1600 (hierarchical validation)

**Status:** ⚠️ Needs refactoring to match Jira pattern

---

### 3. Preview Sample Extraction

**Location:** Old notebook lines 1800-2200

**Pattern:**
```python
if preview:
    # Extract dimProject (max 100)
    # Extract dimRelease (max 100)
    # Extract dimCycle (max 100)
    # Extract dimTestCase (max 100)
    # Extract factTestExecution (max 100)
    
    # Write to Delta: Tables/source/sample_*
    # Register tables
```

**Status:** ✅ Pattern proven, needs to be re-added

---

### 4. Configuration Table Creation

**Pattern from Jira:**
```python
def create_source_tables(
    source_system, base_url, workspace_name,
    workspace_id, lakehouse_id, semantic_model_id
):
    """Create source configuration tables."""
    # Create Tables/source/_source
    # Create Tables/source/_credentials (empty schema)
    # Create Tables/source/_config
```

**Status:** ✅ Available in Jira, needs to be imported or recreated

---

### 5. Stage Activity Logging

**Pattern from Jira:**
```python
def log_stage_activity(
    result, stage, log_table_path,
    source_system=None, project_key=None
):
    """Log stage execution to Delta."""
    # Enrich result with standard fields
    # Write to Tables/log/sourcelog
```

**Status:** ✅ Available in Jira, needs to be imported or recreated

---

### 6. Credential Storage

**Pattern from Jira:**
```python
def write_auth_credentials(
    source_system, auth_token, workspace_name
):
    """Write validated credentials to table."""
    # Write to Tables/source/_credentials
    # Only after successful validation
```

**Status:** ✅ Available in Jira, needs to be imported or recreated

---

### 7. Delta Table Registration

**Pattern (proven):**
```python
def register_delta_table(table_name: str, path: str) -> None:
    """Register Delta table in metastore."""
    spark.sql(f"CREATE TABLE IF NOT EXISTS {table_name} USING DELTA LOCATION '{path}'")
    log.info(f"  📋 Registered: {table_name}")
```

**Status:** ✅ Pattern proven, needs to be re-added

---

## 🚀 Build Order

**Phase 1: Infrastructure (NOW)**
- ✅ Fabric runtime context
- ✅ Variable Library loading
- ✅ Notebook metadata inference
- ✅ Logger initialization
- ✅ Parameter validation

**Phase 2: Configuration (NEXT)**
- [ ] Create configuration tables
- [ ] Register Delta tables

**Phase 3: Health Checks**
- [ ] Implement `check_zephyr_auth()`
- [ ] Implement `check_zephyr_project_access()`
- [ ] Implement `check_zephyr_hierarchical_access()`

**Phase 4: Bootstrap**
- [ ] Re-add ENDPOINTS_DATA
- [ ] Implement endpoint bootstrap
- [ ] Register endpoints table

**Phase 5: Preview**
- [ ] Implement sample extraction
- [ ] Write sample tables
- [ ] Register sample tables

**Phase 6: Logging**
- [ ] Implement stage activity logging
- [ ] Implement credential storage

---

## 📊 Line Count Reduction

| Version | Lines | Status |
|---------|-------|--------|
| **Old** | 2549 | ❌ Too complex |
| **New (skeleton)** | ~300 | ✅ Clean start |
| **New (complete)** | ~800 (est) | 🎯 Target |

**Reduction:** ~70% fewer lines by:
- Using SDK utilities (not embedded code)
- Removing hardcoded values
- Clear separation of concerns
- Eliminating duplication

---

## 🔗 References

- **Old notebook:** `sourceZephyr.Notebook/notebook-content.BACKUP-*.py`
- **Standard:** `Core/framework/standards/SOURCE-STAGE-STANDARD.md`
- **Jira pattern:** `Data/jira/1-source/sourceJira(1).Notebook/notebook_content.py`

---

## 📝 Key Improvements

1. **Zero hardcoded values** - All from runtime/Variable Library
2. **Contract-driven** - Variable Library populated from contract.yaml
3. **Fabric-native** - Uses spark.conf for infrastructure context
4. **Modular** - Clear cell boundaries
5. **Testable** - Each section can be tested independently
6. **Documented** - Clear comments and structure
7. **Standard-compliant** - Follows SOURCE-STAGE-STANDARD.md

---

**Status:** 🚧 **In Progress** - Skeleton complete, building incrementally

**Next:** Implement configuration tables (Phase 2)


