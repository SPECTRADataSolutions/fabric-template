# Prepare Stage Testing Strategy

**Date:** 2025-12-11  
**Status:** 🎯 Active  
**Coverage Target:** >80%  
**Priority:** High

---

## Testing Philosophy

**SPECTRA-Grade Testing:** Test locally first, verify in Fabric second.

1. **Unit Tests** - Test logic in isolation (local)
2. **Integration Tests** - Test API interactions (local with mocks)
3. **End-to-End Tests** - Test full flow (local with real API)
4. **Fabric Validation** - Verify in actual Fabric environment

---

## Test Layers

### Layer 1: Unit Tests (Local) ✅ **REQUIRED BEFORE FABRIC**

**Location:** `tests/test_prepare_stage_*.py`

**Purpose:** Test individual functions and logic

**Coverage Required:**

1. **Intelligence Import** (`test_prepare_stage_imports.py`) ✅
   - [x] Import from SDK global namespace
   - [x] Fallback when not in SDK
   - [x] Error handling

2. **Intelligence Structure** (`test_prepare_stage_intelligence.py`) 🔧 **TODO**
   - [ ] `READ_ENDPOINTS` structure validation
   - [ ] `get_read_endpoint()` method
   - [ ] `get_read_endpoint_path()` with path params
   - [ ] `get_read_endpoint_path()` with query params
   - [ ] Missing entity handling

3. **Schema Building** (`test_prepare_stage_schema_building.py`) 🔧 **TODO**
   - [ ] Parse scalar fields from JSON
   - [ ] Parse array fields (objects)
   - [ ] Parse array fields (scalars)
   - [ ] Parse nested objects
   - [ ] Entity grouping logic
   - [ ] Field name generation
   - [ ] Data type inference

4. **Endpoint Construction** (`test_prepare_stage_endpoints.py`) 🔧 **TODO**
   - [ ] Release endpoint with projectId
   - [ ] Cycle endpoint with releaseId path param
   - [ ] Fallback when READ_ENDPOINTS missing
   - [ ] URL construction edge cases

5. **Release Prioritization** (`test_prepare_stage_release_selection.py`) 🔧 **TODO**
   - [ ] Prioritize releases 112 and 106
   - [ ] Fallback to first release if prioritized not found
   - [ ] Handle empty releases list

---

### Layer 2: Integration Tests (Local with Mocks) ✅ **REQUIRED BEFORE FABRIC**

**Location:** `tests/test_prepare_stage_integration.py`

**Purpose:** Test component interactions with mocked dependencies

**Coverage Required:**

1. **API Interaction** (`test_prepare_stage_api_integration.py`) 🔧 **TODO**
   - [ ] Mock project fetch
   - [ ] Mock releases fetch
   - [ ] Mock cycles fetch
   - [ ] Handle API errors
   - [ ] Handle empty responses
   - [ ] Handle nested response structures

2. **Table Operations** (`test_prepare_stage_tables.py`) 🔧 **TODO**
   - [ ] Table creation (bootstrap mode)
   - [ ] Table writing (schema data)
   - [ ] Table reading (rebuild mode)
   - [ ] Delta table operations

3. **SDK Integration** (`test_prepare_stage_sdk_integration.py`) 🔧 **TODO**
   - [ ] SDK session initialization
   - [ ] Variable Library access
   - [ ] Context loading
   - [ ] Logging integration

---

### Layer 3: End-to-End Tests (Local with Real API) ✅ **RECOMMENDED**

**Location:** `tests/test_zephyr_api_intelligence.py` ✅ **EXISTS**

**Purpose:** Test against real Zephyr API (read-only)

**Coverage:**

- [x] Project loading
- [x] Releases listing
- [x] Cycles fetching (releases 112, 106)
- [x] Endpoint path construction
- [x] Response structure handling

**Status:** ✅ **Complete** - Tests all API endpoints locally

---

### Layer 4: Fabric Validation (Fabric Environment) ⚠️ **AFTER LOCAL TESTS PASS**

**Location:** `prepareZephyr.Notebook` in Fabric

**Purpose:** Verify in actual Fabric runtime

**Validation Checklist:**

- [ ] `%run spectraSDK` executes successfully
- [ ] `ZephyrIntelligence` available in global namespace
- [ ] Project 44 loads
- [ ] Releases list correctly
- [ ] Release 112 or 106 selected
- [ ] Cycles fetched successfully
- [ ] Schema built from cycle data
- [ ] Tables created: `prepare.schema`, `prepare.dependencies`, `prepare.constraints`
- [ ] Tables contain data

---

## Test Execution Strategy

### Before Pushing to Fabric

1. **Run Unit Tests**
   ```bash
   pytest tests/test_prepare_stage_*.py -v --cov
   ```
   **Target:** >80% coverage

2. **Run Integration Tests**
   ```bash
   pytest tests/test_prepare_stage_integration.py -v
   ```
   **Target:** All tests pass

3. **Run End-to-End API Tests**
   ```bash
   pytest tests/test_zephyr_api_intelligence.py -v
   ```
   **Target:** All API endpoints work

4. **Check Coverage**
   ```bash
   pytest --cov --cov-report=html
   ```
   **Target:** >80% coverage, review HTML report

### After Local Tests Pass

5. **Test in Fabric**
   - Run `prepareZephyr` notebook with `bootstrap=True`
   - Verify all steps execute
   - Check table contents

---

## Current Test Status

### ✅ Completed

- `test_prepare_stage_imports.py` - Import logic
- `test_prepare_stage_end_to_end.py` - End-to-end flow (mocked)
- `test_zephyr_api_intelligence.py` - Real API testing

### 🔧 TODO (Required Before Fabric)

1. **Intelligence Structure Tests**
   - Test `READ_ENDPOINTS` structure
   - Test `get_read_endpoint_path()` method
   - Test path/query param substitution

2. **Schema Building Tests**
   - Test JSON parsing
   - Test field extraction
   - Test entity grouping

3. **Release Selection Tests**
   - Test prioritization logic
   - Test fallback behavior

4. **API Integration Tests**
   - Mock API responses
   - Test error handling
   - Test nested response structures

---

## Coverage Goals

**Minimum:** 80% coverage before Fabric testing

**Target Areas:**
- Intelligence import logic: 100%
- Endpoint construction: 100%
- Schema building: >80%
- Release selection: 100%
- Error handling: >80%

---

## Test Data Strategy

### Mock Data

**Location:** `tests/fixtures/`

**Files:**
- `mock_project_response.json` - Project API response
- `mock_releases_response.json` - Releases API response
- `mock_cycles_response.json` - Cycles API response
- `mock_schema_data.json` - Expected schema output

### Real API Data (Read-Only)

**Source:** Project 44 (production, read-only)

**Used By:** `test_zephyr_api_intelligence.py`

**Safety:** GET requests only, no writes

---

## Continuous Integration

**CI Workflow:** `.github/workflows/ci.yml`

**Runs:**
- Linting (Ruff)
- Unit tests (pytest)
- Coverage reporting
- Multi-version testing (Python 3.11, 3.12)

**Coverage Upload:** Codecov integration

---

## Test Maintenance

### When to Add Tests

- New functionality added
- Bug found and fixed
- API changes discovered
- Logic refactored

### When to Update Tests

- API response structure changes
- Intelligence structure changes
- Endpoint paths change
- Schema format changes

---

## Related Documents

- `TESTING-PLAN-PREPARE-STAGE.md` - Detailed test plan
- `PREPARE-STAGE-FIXES-SUMMARY.md` - Bugs fixed
- `INTELLIGENCE-ARCHITECTURE.md` - Intelligence system
- `NEXT-STEPS.md` - Action plan

---

**Last Updated:** 2025-12-11  
**Next Review:** After test implementation

