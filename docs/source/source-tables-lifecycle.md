# Source Stage Tables Lifecycle

> **Date:** 2025-12-08  
> **Purpose:** Document which tables are recreated and when

---

## Table Creation Summary

| Table | Created Every Run? | Condition | Mode | Purpose |
|-------|-------------------|-----------|------|---------|
| `source.config` | ✅ **YES** | Always | `overwrite` | Runtime execution context |
| `source.credentials` | ✅ **YES** | Always | `overwrite` | Masked authentication tokens |
| `source.portfolio` | ✅ **YES** | Always | `overwrite` | Dashboard metadata (preserves `discovery_date`) |
| `source.endpoints` | ⚠️ **CONDITIONAL** | Only if `bootstrap=True` | `overwrite` | Endpoint catalog |
| `source.sampleProjects` | ⚠️ **CONDITIONAL** | Only if `preview=True` | `overwrite` | Preview sample data |
| `source.sampleReleases` | ⚠️ **CONDITIONAL** | Only if `preview=True` | `overwrite` | Preview sample data |

---

## Always Recreated (Every Run)

### 1. `source.config`

**Purpose:** Runtime execution context and configuration

**Recreated:** ✅ **Every run** (always overwritten)

**Contains:**
- `execution_mode` - "pipeline" or "interactive"
- `operation_type` - Pipeline operation type
- `notebook_name` - Current notebook name
- `stage` - Current stage (e.g., "source")
- `sdk_version` - SDK version
- `bootstrap_enabled` - Whether bootstrap ran
- `preview_enabled` - Whether preview extraction ran
- `last_updated` - Timestamp

**Why always recreated:** Contains runtime state that changes every execution.

---

### 2. `source.credentials`

**Purpose:** Masked authentication credentials

**Recreated:** ✅ **Every run** (always overwritten)

**Contains:**
- `credential_type` - "api_token"
- `credential_value` - Masked token (e.g., "***abc")
- `last_validated` - Timestamp
- `validation_status` - "Success" or "Failed"

**Why always recreated:** Contains current auth status and validation timestamp.

---

### 3. `source.portfolio`

**Purpose:** Dashboard-ready metadata summary

**Recreated:** ✅ **Every run** (always overwritten, but preserves `discovery_date`)

**Contains:**
- `source_system` - Source system identifier
- `contract_version` - Contract version
- `discovery_date` - **Preserved from first run** (not overwritten)
- `total_endpoints` - Count of endpoints
- `endpoint_categories` - JSON of category counts
- `hierarchical_endpoints` - Count of hierarchical endpoints
- `auth_method` - Authentication method
- `auth_status` - Current auth status
- `last_auth_check` - Timestamp
- `hierarchical_access_validated` - Boolean
- `endpoint_success_rate` - Success rate (0.0-1.0)
- `supports_incremental` - Boolean
- `status` - "active" or "inactive"
- `is_enabled` - Boolean
- `last_updated` - Timestamp

**Why always recreated:** Contains current state metrics that change every run.

**Special behavior:** Preserves `discovery_date` from first run (checks existing table before overwriting).

---

## Conditionally Recreated

### 4. `source.endpoints`

**Purpose:** Complete catalog of API endpoints

**Recreated:** ⚠️ **Only if `bootstrap=True`**

**Contains:**
- `endpoint_path` - Base path (e.g., "/project")
- `full_path` - Full path with parameters (e.g., "/project{?key}")
- `http_method` - HTTP method (GET, POST, etc.)
- `category` - Endpoint category
- `description` - Endpoint description
- `requires_auth` - Boolean
- `hierarchical` - Boolean
- `query_parameters` - List of query param names
- `path_parameters` - List of path param names
- `resource` - Full resource string

**When recreated:**
- First run (bootstrap=True)
- When endpoint catalog changes (bootstrap=True)
- When schema needs updating (bootstrap=True)

**Why conditional:** Endpoint catalog is static metadata that doesn't change between runs. Only needs updating when:
- Initial setup
- Catalog structure changes (e.g., adding new metadata fields)
- Endpoints are added/removed

**Example:**
```python
# In Source notebook
bootstrap: bool = True  # ← Set to True to recreate endpoints table
```

---

### 5. `source.sampleProjects` & `source.sampleReleases`

**Purpose:** Preview sample data for validation

**Recreated:** ⚠️ **Only if `preview=True`**

**Contains:** Sample records from API (limited to `sample_limit`, default 10)

**When recreated:**
- When preview extraction is requested (preview=True)
- For validation and schema discovery

**Why conditional:** Preview samples are for validation only, not required for normal pipeline runs.

**Example:**
```python
# In Source notebook
preview: bool = True  # ← Set to True to extract preview samples
```

---

## Execution Flow

### Normal Run (bootstrap=False, preview=False)

```
1. Create source.config          ✅ (overwrite)
2. Validate authentication     ✅
3. Create source.credentials    ✅ (overwrite)
4. Skip endpoints bootstrap     ⏭️ (bootstrap=False)
5. Create source.portfolio      ✅ (overwrite)
6. Skip preview extraction      ⏭️ (preview=False)
```

**Tables created:** 3 (config, credentials, portfolio)

---

### Bootstrap Run (bootstrap=True, preview=False)

```
1. Create source.config          ✅ (overwrite)
2. Validate authentication     ✅
3. Create source.credentials    ✅ (overwrite)
4. Bootstrap source.endpoints   ✅ (overwrite) ← NEW
5. Create source.portfolio      ✅ (overwrite)
6. Skip preview extraction      ⏭️ (preview=False)
```

**Tables created:** 4 (config, credentials, portfolio, endpoints)

---

### Full Run (bootstrap=True, preview=True)

```
1. Create source.config          ✅ (overwrite)
2. Validate authentication     ✅
3. Create source.credentials    ✅ (overwrite)
4. Bootstrap source.endpoints   ✅ (overwrite)
5. Create source.portfolio      ✅ (overwrite)
6. Extract preview samples      ✅ (overwrite) ← NEW
   - source.sampleProjects
   - source.sampleReleases
```

**Tables created:** 6 (config, credentials, portfolio, endpoints, sampleProjects, sampleReleases)

---

## Key Points

### ✅ Always Recreated
- **Config, credentials, portfolio** are always recreated because they contain:
  - Runtime state (execution mode, timestamps)
  - Current auth status
  - Current metrics (endpoint counts, success rates)

### ⚠️ Conditionally Recreated
- **Endpoints** only recreated when `bootstrap=True` (static metadata)
- **Preview samples** only recreated when `preview=True` (validation only)

### 🔄 Overwrite Behavior
- All tables use `mode="overwrite"` (no append mode)
- This ensures clean state every run
- No incremental updates - full replacement

### 💾 Data Preservation
- **Portfolio table** preserves `discovery_date` from first run
- All other tables are fully replaced

---

## When to Use Bootstrap

**Set `bootstrap=True` when:**
- ✅ First time running Source stage
- ✅ Endpoint catalog structure changed (e.g., added new metadata fields)
- ✅ Endpoints were added/removed from catalog
- ✅ Need to update `source.endpoints` table schema

**Set `bootstrap=False` when:**
- ✅ Normal pipeline runs (endpoints already bootstrapped)
- ✅ Only need to update config/credentials/portfolio
- ✅ Don't want to overwrite endpoints table

---

## When to Use Preview

**Set `preview=True` when:**
- ✅ First time setting up pipeline
- ✅ Need sample data for schema discovery
- ✅ Validating API connectivity
- ✅ Testing data extraction

**Set `preview=False` when:**
- ✅ Normal pipeline runs (no need for samples)
- ✅ Only need metadata tables (config, credentials, portfolio)

---

## Summary

**Most tables are recreated every run** (config, credentials, portfolio), but **endpoints and preview samples are conditional** based on `bootstrap` and `preview` parameters.

This design ensures:
- ✅ Runtime state is always current
- ✅ Static metadata (endpoints) is only updated when needed
- ✅ Preview samples are optional (for validation only)

---

**Last Updated:** 2025-12-08

