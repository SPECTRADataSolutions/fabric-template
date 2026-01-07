# Prepare Stage Testing Plan

**Status:** 🚧 In Progress  
**Coverage Target:** >80%  
**Priority:** High (critical bugs found in production)

---

## Current Issues Found

1. ✅ **Fixed:** `__file__` not available in Fabric notebooks (import error)
2. ✅ **Fixed:** `ZephyrIntelligence.ENTITIES` doesn't exist (should be `SCHEMAS`)
3. ⚠️ **Needs Testing:** SDK fallback logic (JSON schema parsing)
4. ⚠️ **Needs Testing:** Schema building from API samples
5. ⚠️ **Needs Testing:** Bootstrap mode table creation
6. ⚠️ **Needs Testing:** Rebuild mode API fetching

---

## Test Coverage Required

### 1. Import Logic (`test_prepare_stage_imports.py`) ✅ Created

- [x] Import from SDK (success case)
- [x] Fallback to file loading
- [x] Error handling when not found
- [ ] Test in Fabric notebook environment (requires Fabric runtime)

### 2. Intelligence Structure (`test_prepare_stage_intelligence.py`) 🚧 TODO

- [ ] `SCHEMAS` structure validation
- [ ] `READ_ENDPOINTS` structure validation
- [ ] `get_read_endpoint()` method
- [ ] `get_read_endpoint_path()` with path params
- [ ] `get_read_endpoint_path()` with query params
- [ ] Missing entity handling

### 3. Schema Building from Samples (`test_prepare_stage_schema_building.py`) 🚧 TODO

- [ ] Parse scalar fields
- [ ] Parse array fields (objects)
- [ ] Parse array fields (scalars)
- [ ] Parse nested objects (records)
- [ ] Entity grouping (entity+structureType)
- [ ] Field name generation (targetField)
- [ ] Data type inference
- [ ] Fact table metadata
- [ ] Dimension/bridge naming

### 4. SDK Fallback (`test_prepare_stage_sdk_fallback.py`) 🚧 TODO

- [ ] Parse JSON schema `properties`
- [ ] Handle `required` fields
- [ ] Group by structure type
- [ ] Map JSON types to SPECTRA types
- [ ] Handle missing fields gracefully

### 5. Bootstrap Mode (`test_prepare_stage_bootstrap.py`) 🚧 TODO

- [ ] Create `prepare.schema` table
- [ ] Create `prepare.dependencies` table
- [ ] Create `prepare.constraints` table
- [ ] Table schema validation
- [ ] Data validation
- [ ] Overwrite mode handling

### 6. Rebuild Mode (`test_prepare_stage_rebuild.py`) 🚧 TODO

- [ ] API credential loading
- [ ] Fetch releases (GET endpoint)
- [ ] Fetch cycles (GET endpoint with path params)
- [ ] Error handling (405, 404, timeout)
- [ ] Sample data parsing
- [ ] Schema building from samples
- [ ] Write sample tables

### 7. Integration Tests (`test_prepare_stage_integration.py`) 🚧 TODO

- [ ] Full bootstrap flow
- [ ] Full rebuild flow
- [ ] Fallback from tables to SDK
- [ ] Table creation → table reading
- [ ] End-to-end: bootstrap → rebuild → validate

---

## Test Execution

```bash
# Run all Prepare stage tests
pytest tests/test_prepare_stage*.py -v

# Run with coverage
pytest tests/test_prepare_stage*.py --cov=prepareZephyr.Notebook --cov-report=html

# Run specific test
pytest tests/test_prepare_stage_imports.py::TestZephyrIntelligenceImport -v
```

---

## Priority Order

1. **High Priority (Critical Bugs):**
   - Import logic ✅
   - Intelligence structure
   - Schema building from samples
   - SDK fallback

2. **Medium Priority (Functionality):**
   - Bootstrap mode
   - Rebuild mode
   - Error handling

3. **Low Priority (Edge Cases):**
   - Integration tests
   - Performance tests
   - Edge case handling

---

## Notes

- Tests should mock Fabric notebook environment (no `__file__`, no direct file access)
- Use `unittest.mock` for API calls
- Use `pytest.fixture` for shared test data
- Test both success and failure paths
- Test edge cases (empty data, missing fields, etc.)




