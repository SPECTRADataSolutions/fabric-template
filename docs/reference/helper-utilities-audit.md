# Helper & Utility Functions Audit

**Purpose:** Assess all helpers for SDK promotion, naming conventions, and shareability  
**Created:** 2025-12-04  
**Status:** 🔍 Audit In Progress

## 📋 Audit Criteria

### Naming Convention

✅ **Verb-first naming** (e.g., `ensure_delta_table`, `fetch_projects`, `validate_config`)

- Describes action clearly
- Self-documenting intent
- Consistent across SPECTRA

### SDK Promotion Criteria

1. **Universal utility** - useful across multiple projects
2. **No project-specific logic** - generic implementation
3. **Well-documented** - clear docstring with examples
4. **Battle-tested** - proven in at least one project
5. **Stable interface** - unlikely to change frequently

---

## 🔍 Current Helpers in sourceZephyr.Notebook

### 1. `is_running_locally()` → Line 1183

**Current Name:** ✅ Verb-first  
**Purpose:** Detect if notebook is running locally vs in Fabric  
**Used:** Parameter block (dynamic debug mode)

**SDK Candidate:** ✅ YES - Universal utility

- **Reason:** Every Fabric notebook could use this
- **Target Module:** `spectra_fabric_sdk.runtime` or `spectra_fabric_sdk.notebook_utils`
- **Rename:** Keep as-is ✅
- **Documentation:** Add examples of local vs Fabric detection patterns

---

### 2. `fetch_projects()` → Line 1396

**Current Name:** ✅ Verb-first  
**Purpose:** Fetch Zephyr projects from API  
**Used:** Bootstrap phase

**SDK Candidate:** ❌ NO - Zephyr-specific

- **Reason:** Hardcoded to Zephyr `/project` endpoint
- **Action:** Keep in notebook
- **Consider:** Could extract generic `fetch_paginated_api()` pattern if needed 3+ times

---

### 3. `ensure_delta_table()` → Line 1469

**Current Name:** ✅ Verb-first  
**Purpose:** Register Delta location as managed table in metastore (idempotent)  
**Used:** 5 locations (endpoints, hierarchical_validation, endpoint_health, quality_gate_report, sample tables)  
**Pattern Source:** Data/jira/2-prepare/prepareJiraConfig.Notebook line 2698

**SDK Candidate:** ✅ YES - Universal Delta pattern

- **Reason:** Every Fabric project needs this for Delta table registration
- **Target Module:** `spectra_fabric_sdk.delta` or `spectra_fabric_sdk.table_utils`
- **Name:** ✅ `register_delta_table()` - Perfectly describes the action
- **Documentation:**
  - Explain auto-schema creation
  - Show example usage
  - Link to FABRIC-DELTA-TABLE-PATTERN.md
- **Enhancement:** Add optional `properties` dict for TBLPROPERTIES
- **Enhancement:** Add return value (True if created, False if existed)

---

### 4. `extract_path_from_resource()` → Line 1795

**Current Name:** ✅ Verb-first  
**Purpose:** Extract API path from API Blueprint resource description  
**Format:** `"Get Projects [/project]"` → `"/project"`  
**Used:** Health check phase

**SDK Candidate:** ❌ NO - API Blueprint specific

- **Reason:** Specific to API Blueprint format `[/path]`
- **Action:** Keep in notebook
- **Consider:** If we use API Blueprint in 3+ projects, extract to shared utility

---

### 5. `health_check_endpoint()` → Line 1811

**Current Name:** ✅ Verb-first  
**Purpose:** Perform health check on a single REST API endpoint  
**Returns:** Dict with status, http_code, error_message, accessible, etc.  
**Used:** Comprehensive health check phase

**SDK Candidate:** ⚠️ MAYBE - Generic but coupled to Zephyr auth

- **Reason:** Logic is generic (HEAD/GET fallback), but uses notebook-level `session` and `base_url`
- **Action:** Refactor to accept `session` and `base_url` as parameters, then promote
- **Target Module:** `spectra_fabric_sdk.api_utils` or `spectra_fabric_sdk.health_check`
- **Rename:** Consider `check_endpoint_health()` for consistency
- **Enhancement:** Add timeout parameter (currently hardcoded to 5 seconds)
- **Enhancement:** Support POST/PUT/DELETE methods
- **Enhancement:** Support custom headers/auth

---

## 🎯 SDK Promotion Roadmap

### Phase 1: Immediate (After Current Fix)

1. ✅ `ensure_delta_table()` → `spectra_fabric_sdk.delta`

   - Already battle-tested in Jira + Zephyr
   - Clear interface, stable
   - Add to SDK with enhancements

2. ✅ `is_running_locally()` → `spectra_fabric_sdk.runtime`
   - Simple, universal
   - No dependencies
   - Add to SDK as-is

### Phase 2: Refactor Then Promote

3. ⚠️ `health_check_endpoint()` → `spectra_fabric_sdk.api_utils`
   - **Refactor:** Accept `session`, `base_url`, `timeout` as params
   - **Test:** Ensure works with different auth patterns
   - **Document:** Show examples with different API types
   - **Then:** Promote to SDK

### Phase 3: Monitor for Rule of Three

4. 🔍 `extract_path_from_resource()` - Watch for reuse

   - If API Blueprint used in 3+ projects → extract pattern
   - Otherwise keep project-specific

5. 🔍 `fetch_projects()` - Watch for reuse
   - If similar pagination pattern needed 3+ times → extract `fetch_paginated_api()`
   - Otherwise keep project-specific

---

## 📝 Naming Convention Standards

### ✅ Good Verb-First Names

- `register_delta_table()` - Registers location in metastore ✨ PERFECT
- `fetch_projects()` - Retrieves data
- `extract_path_from_resource()` - Parses and extracts
- `health_check_endpoint()` - Tests and validates
- `is_running_locally()` - Boolean check

### 📐 Verb Categories

- **ensure\_**: Idempotent creation/validation
- **fetch\_**: Retrieve data from external source
- **extract\_**: Parse and extract from data
- **check\_** / **validate\_**: Test/verify conditions
- **is\_** / **has\_**: Boolean predicates
- **create\_**: Non-idempotent creation
- **update\_**: Modify existing
- **delete\_** / **remove\_**: Destruction
- **transform\_**: Data transformation
- **calculate\_**: Compute value
- **build\_**: Construct complex object
- **parse\_**: Convert format
- **format\_**: Format output

---

## 🔄 Next Steps

1. ⏳ **Wait for current fix to deploy** - Test `ensure_delta_table()` in Fabric
2. 🧹 **Clean and promote** - Move `ensure_delta_table()` and `is_running_locally()` to SDK
3. 🔧 **Refactor** - Update `health_check_endpoint()` to accept params
4. 📚 **Document** - Update SDK docs with new utilities
5. 🔁 **Update Zephyr** - Import from SDK instead of local definitions
6. ✅ **Validate** - Ensure Zephyr notebook still works after SDK imports

---

## 📊 Summary

| Function                       | Verb-First? | SDK Candidate? | Action                | Priority |
| ------------------------------ | ----------- | -------------- | --------------------- | -------- |
| `is_running_locally()`         | ✅          | ✅ YES         | Promote to SDK        | High     |
| `fetch_projects()`             | ✅          | ❌ NO          | Keep in notebook      | -        |
| `register_delta_table()` ✨    | ✅          | ✅ YES         | Promote to SDK        | High     |
| `extract_path_from_resource()` | ✅          | ❌ NO          | Keep in notebook      | -        |
| `health_check_endpoint()`      | ✅          | ⚠️ MAYBE       | Refactor then promote | Medium   |

**Total Functions:** 5  
**Verb-First Compliant:** 5/5 (100%) ✅  
**SDK Promotion Ready:** 2/5 immediate, 1/5 after refactor
