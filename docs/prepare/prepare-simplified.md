# Prepare Stage - Simplified Approach

## Overview

The prepare stage has been simplified from complex metadata generation (488 lines) to simple data extraction (~250 lines).

**New Approach:** Extract actual data samples from API endpoints and save to Delta tables.

---

## Table Naming Convention

All tables are saved to `Tables/prepare/` with table names derived from endpoint paths:

| Endpoint | Table Path | Table Name |
|----------|------------|------------|
| `/project/details` | `Tables/prepare/project_details` | `prepare.project_details` |
| `/release` | `Tables/prepare/release` | `prepare.release` |
| `/cycle/release/{id}` | `Tables/prepare/cycle_release` | `prepare.cycle_release` |

**Conversion Logic:**
- Remove leading `/`
- Replace `/` with `_`
- Remove parameter placeholders like `{id}`

---

## Current Endpoints (Phase 1)

Starting with **2 independent endpoints** (no dependencies):

1. **`/project/details`** → `Tables/prepare/project_details`
   - Extracts all projects
   - Independent (no dependencies)

2. **`/release`** → `Tables/prepare/release`
   - Extracts all releases
   - Independent (no dependencies)

---

## Notebook Structure

### Cell 1: SDK & Context
- Loads spectraSDK
- Sets up NotebookSession
- Loads credentials from Variable Library

### Cell 2: Imports & Helper Functions
- `endpoint_to_table_name()` - Converts endpoint to table name
- `call_zephyr_api()` - Makes API requests
- `extract_and_save()` - Extracts data and saves to Delta table

### Cell 3: API Configuration
- Builds authentication headers

### Cell 4: Extraction
- Loops through endpoints
- Calls `extract_and_save()` for each
- Adds extraction metadata (`_extracted_at`, `_source_endpoint`)

### Cell 5: Summary
- Shows extraction results
- Reports record counts

---

## Adding More Endpoints

To add more endpoints, simply add to the `endpoints_to_extract` list:

```python
endpoints_to_extract = [
    "/project/details",  # All projects
    "/release",           # All releases
    "/cycle/release/{releaseId}",  # Add cycles (needs release ID)
]
```

**Note:** For endpoints with parameters (like `{releaseId}`), you'll need to:
1. Get IDs from previous tables (e.g., get release IDs from `prepare.release`)
2. Loop through IDs and call endpoint for each
3. Union results before saving

---

## Next Steps

### Phase 2: Add Level 1 Endpoints

Once Phase 1 works, add endpoints that depend on Phase 1:

- `/cycle/release/{releaseId}` - Need release IDs from `prepare.release`
- `/testcasetree/projectrepository/{projectId}` - Need project IDs from `prepare.project_details`
- `/requirementtree/project/{projectId}` - Need project IDs (once endpoint is fixed)

### Phase 3: Continue Hierarchy

Add Level 2 and Level 3 endpoints as dependencies are met.

---

## Benefits of Simplified Approach

✅ **Much simpler** - ~250 lines vs 488 lines  
✅ **Actual data** - Can inspect, query, analyse  
✅ **Schema discovery** - Spark infers schema from real data  
✅ **Incremental** - Easy to add endpoints one at a time  
✅ **No complex dependencies** - Doesn't require intelligence artifacts  
✅ **Clear naming** - Table names match endpoints

---

## Testing

Run notebook with `test=True` to limit records:

```python
test: bool = True  # Limits to 10 records per endpoint
```

This helps:
- Fast iteration
- Lower API usage during development
- Easier debugging

---

## File Location

**Notebook:** `2-prepare/prepareZephyr.Notebook/notebook_content.py`

**Tables:** `Tables/prepare/{endpoint_name}`

