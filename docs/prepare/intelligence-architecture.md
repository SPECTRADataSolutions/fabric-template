# Zephyr Intelligence Architecture

**Date:** 2025-12-11  
**Status:** ✅ Active  
**Purpose:** Explain how Zephyr API intelligence is discovered, stored, embedded, and used

---

## Overview

Zephyr intelligence is the **knowledge base** about the Zephyr API that drives the Prepare stage. It contains schemas, dependencies, constraints, and endpoint information discovered through investigation and embedded into the SDK for runtime use.

---

## Architecture Flow

```
Investigation Scripts → Intelligence Files → SDK Embedding → Prepare Stage → Schema Tables
```

### 1. **Investigation Phase** (Complete ✅)

**Location:** `Data/zephyr/scripts/`

**Purpose:** One-time discovery of Zephyr API structure

**Key Scripts:**
- `discover_endpoints.py` - Found all 224 API endpoints
- `probe_schemas.py` - Discovered entity schemas from API responses
- `discover_api_hierarchy.py` - Mapped entity dependencies
- `comprehensive_api_validation.py` - Tested all endpoints
- `validate_intelligence.py` - Validated intelligence completeness
- `sequence_creation_order.py` - Determined correct creation order

**Output:** Knowledge about:
- All available endpoints (224 total)
- Entity schemas (cycle, release, requirement, testcase, etc.)
- Dependency relationships (Projects → Releases → Cycles → Executions)
- API bugs, blockers, and workarounds
- Correct endpoint patterns and parameters

**Status:** ✅ **Complete** - Investigation done, scripts kept for reference/history

---

### 2. **Intelligence Storage** (Active 🔧)

**Location:** `Data/zephyr/intelligence/`

**Purpose:** Store discovered knowledge in structured format

**Structure:**

```
intelligence/
├── intelligence.py          # ZephyrIntelligence class (main entry point)
├── schemas/                 # JSON schemas per entity
│   ├── cycle.json
│   ├── release.json
│   ├── requirement.json
│   └── ...
├── endpoints.yaml           # Full API endpoint catalog (224 endpoints)
├── dependencies.yaml        # Entity dependency graph
├── quirks.yaml             # API bugs, blockers, workarounds
├── creation-order.yaml      # Correct entity creation sequence
└── manual-overrides.yaml    # Manual corrections to discovered data
```

**ZephyrIntelligence Class:**

```python
class ZephyrIntelligence:
    # Schemas from intelligence/schemas/*.json
    SCHEMAS = {
        "cycle": {...},
        "release": {...},
        ...
    }
    
    # READ endpoints for production mode (GET endpoints)
    READ_ENDPOINTS = {
        "project": {"endpoint": "/project", "method": "GET", ...},
        "release": {"endpoint": "/release", "query_params": ["projectId"], ...},
        "cycle": {"endpoint": "/cycle/release/{releaseid}", "path_params": ["releaseid"], ...},
        ...
    }
    
    # Dependencies from intelligence/dependencies.yaml
    DEPENDENCIES = {...}
    
    # Constraints from intelligence/quirks.yaml
    CONSTRAINTS = {...}
    
    @classmethod
    def get_read_endpoint_path(cls, entity: str, **params):
        """Get READ endpoint path with parameters filled in."""
        ...
```

**Current Status:** 🔧 **Being Fixed**
- ✅ Schemas, dependencies, constraints complete
- 🔧 READ_ENDPOINTS being corrected (GET endpoints for production data)
- 🔧 Endpoint paths being fixed (e.g., `/cycle/release/{releaseid}` instead of `/cycle`)

---

### 3. **SDK Embedding** (Active 🔧)

**Location:** `Data/zephyr/scripts/append_intelligence_to_sdk.py`

**Purpose:** Embed intelligence into SDK for runtime use

**Process:**

1. Read `intelligence/intelligence.py`
2. Append to `spectraSDK.Notebook/notebook_content.py`
3. Wrap in Fabric notebook cell structure

**Result:** After `%run spectraSDK`, `ZephyrIntelligence` is available in global namespace

**Status:** 🔧 **Active** - Script exists, needs to be run after intelligence updates

---

### 4. **Prepare Stage Usage** (Active 🔧)

**Location:** `Data/zephyr/prepareZephyr.Notebook/notebook_content.py`

**Purpose:** Use intelligence to build schema tables from production data

**Flow:**

```
1. Load Project (verify exists)
   ↓
2. List Releases (fetch all releases for project)
   ↓
3. Select Release (prioritize releases 112, 106 - known to have cycles)
   ↓
4. Fetch Cycles (use READ_ENDPOINTS from intelligence)
   ↓
5. Build Schema (analyze JSON structure, extract fields)
   ↓
6. Write to Tables (prepare.schema, prepare.dependencies, prepare.constraints)
```

**Intelligence Usage:**

```python
# After %run spectraSDK, ZephyrIntelligence is available
ZephyrIntelligence = globals().get('ZephyrIntelligence')

# Get READ endpoint for releases
releases_path = ZephyrIntelligence.get_read_endpoint_path("release", projectId=44)
# Returns: "/release?projectId=44"

# Get READ endpoint for cycles
cycles_path = ZephyrIntelligence.get_read_endpoint_path("cycle", releaseid=112)
# Returns: "/cycle/release/112"

# Use schemas to understand structure
cycle_schema = ZephyrIntelligence.get_schema("cycle")

# Use dependencies to know order
dependencies = ZephyrIntelligence.get_dependencies("cycle")
# Returns: {"depends_on": ["release"], ...}
```

**Current Status:** 🔧 **Being Fixed**
- ✅ Project loading added
- ✅ Release listing added
- ✅ Release prioritization (112, 106) added
- 🔧 Cycle fetching using correct endpoints
- 🔧 Schema building from actual data

---

## Current Work

### What We're Fixing

1. **READ_ENDPOINTS** - Correct GET endpoints for production data
   - ✅ Added `READ_ENDPOINTS` dictionary
   - ✅ Added `get_read_endpoint()` and `get_read_endpoint_path()` methods
   - 🔧 Fixing endpoint paths (e.g., cycles need `/cycle/release/{releaseid}`)

2. **Prepare Stage Flow** - Proper hierarchical data fetching
   - ✅ Load project first
   - ✅ List all releases
   - ✅ Prioritize releases 112 and 106 (known to have cycles)
   - 🔧 Fetch cycles using correct endpoint
   - 🔧 Build schema from actual data

3. **Local Testing** - Verify before Fabric
   - ✅ Created `tests/test_zephyr_api_intelligence.py`
   - ✅ Tests all API endpoints locally
   - ✅ Confirms releases 112 and 106 have cycles
   - ✅ Validates endpoint paths work

---

## File Locations

### Intelligence Files
- `Data/zephyr/intelligence/intelligence.py` - Main intelligence class
- `Data/zephyr/intelligence/schemas/*.json` - Entity schemas
- `Data/zephyr/intelligence/endpoints.yaml` - Endpoint catalog
- `Data/zephyr/intelligence/dependencies.yaml` - Dependency graph
- `Data/zephyr/intelligence/quirks.yaml` - Bugs/blockers/workarounds

### Investigation Scripts (Reference Only)
- `Data/zephyr/scripts/discover_endpoints.py` - Endpoint discovery
- `Data/zephyr/scripts/probe_schemas.py` - Schema discovery
- `Data/zephyr/scripts/discover_api_hierarchy.py` - Dependency mapping
- `Data/zephyr/scripts/comprehensive_api_validation.py` - Endpoint testing
- `Data/zephyr/scripts/validate_intelligence.py` - Intelligence validation
- `Data/zephyr/scripts/append_intelligence_to_sdk.py` - SDK embedding script

### Runtime Files
- `Data/zephyr/spectraSDK.Notebook/notebook_content.py` - SDK with embedded intelligence
- `Data/zephyr/prepareZephyr.Notebook/notebook_content.py` - Prepare stage using intelligence
- `Data/zephyr/tests/test_zephyr_api_intelligence.py` - Local API testing

---

## Key Concepts

### Intelligence vs. Scripts

**Intelligence:**
- ✅ Runtime knowledge (used by Prepare stage)
- ✅ Embedded in SDK
- ✅ Updated when API changes
- ✅ Part of pipeline execution

**Scripts:**
- ✅ Investigation tools (one-time discovery)
- ✅ Reference/history
- ✅ Not part of runtime pipeline
- ✅ Kept for documentation

### READ_ENDPOINTS vs. SCHEMAS

**READ_ENDPOINTS:**
- GET endpoints for reading production data
- Used by Prepare stage to fetch samples
- Example: `/cycle/release/{releaseid}`

**SCHEMAS:**
- JSON structure definitions
- Used to understand data format
- Example: `{"id": "integer", "name": "string", ...}`

### Production Mode vs. Creation Mode

**Production Mode (READ_ENDPOINTS):**
- GET requests only
- Read from project 44 (READ-ONLY)
- Used by Prepare stage
- No writes to Zephyr API

**Creation Mode (SCHEMAS + DEPENDENCIES):**
- POST requests for creating entities
- Used by test data scripts
- Requires correct creation order
- Has blockers (some APIs broken)

---

## Next Steps

1. ✅ Fix READ_ENDPOINTS endpoint paths
2. ✅ Update Prepare stage to use correct endpoints
3. ✅ Test locally with `test_zephyr_api_intelligence.py`
4. 🔧 Run in Fabric and verify schema tables build correctly
5. 🔧 Run `append_intelligence_to_sdk.py` to embed latest intelligence
6. 🔧 Document any new discoveries in intelligence files

---

## Related Documents

- `docs/prepare/PREPARE-STAGE-PURPOSE.md` - Prepare stage design
- `docs/prepare/PREPARE-STAGE-FLOW.md` - Detailed flow documentation
- `docs/bug-and-blocker-registry.md` - API issues discovered
- `intelligence/validation-report.md` - Intelligence validation results

---

**Last Updated:** 2025-12-11  
**Maintainer:** Data Platform Team

