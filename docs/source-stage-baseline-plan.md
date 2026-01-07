# Source Stage Baseline & Contract Compliance Plan

**Date:** 2025-12-06  
**Status:** 🎯 Active  
**Purpose:** Ensure source stage passes contract v3.0.0 with SPECTRA-grade quality

---

## 🎯 Objective

**Goal:** Achieve 100% contract compliance for source stage v3.0.0

**Current Status:** ~75% compliant (identified gaps below)

---

## 📋 Contract Compliance Audit

### ✅ Passing Requirements

1. ✅ **Authentication** - Validates API auth, fails fast if failed
2. ✅ **Endpoint Catalog** - 228 endpoints embedded in SDK, bootstrap creates table
3. ✅ **Dynamic Project Discovery** - No hardcoded IDs, gets from API
4. ✅ **Portfolio Table** - Dashboard-ready metadata created
5. ✅ **Config Table** - Runtime configuration snapshot
6. ✅ **Credentials Table** - Masked credential validation
7. ✅ **Endpoints Table** - Complete catalog (when bootstrap=True)

### ⚠️ Gap 1: Incomplete Preview Samples

**Contract Requirement:**
> "Visibility demonstrated across all hierarchy levels with preview samples"

**Expected (5 tables):**
- ✅ source.sampleProjects
- ✅ source.sampleReleases
- ❌ source.sampleCycles
- ❌ source.sampleExecutions
- ❌ source.sampleTestcases

**Current Implementation:**
- Only extracts projects and releases
- Missing cycles, executions, testcases

**Fix Required:**
- Add cycles extraction (requires releaseId)
- Add executions extraction (requires cycleId)
- Add testcases extraction (requires testcaseId from execution)

---

### ⚠️ Gap 2: Incomplete Hierarchical Validation

**Contract Requirement:**
> "Hierarchical access validated: Projects → Releases → Cycles → Executions → Test Cases"

**Current Implementation:**
- ✅ Projects → Releases (validated)
- ❌ Releases → Cycles (missing)
- ❌ Cycles → Executions (missing)
- ❌ Executions → Test Cases (missing)

**Fix Required:**
- Add Releases → Cycles validation
- Add Cycles → Executions validation
- Add Executions → Test Cases validation

---

### ⚠️ Gap 3: Testing & Quality Not Verified

**Contract Requirement:**
> "Comprehensive test suite with >75% coverage (pytest + GitHub Actions)"

**What to Verify:**
- [ ] Run test suite: `pytest --cov`
- [ ] Check coverage percentage (target >75%)
- [ ] Verify CI/CD pipeline runs tests automatically
- [ ] Fix any failing tests
- [ ] Document coverage results

---

### ⚠️ Gap 4: Data Validation Not Used

**Contract Requirement:**
> "Data validation functions for API responses, schemas, row counts, nulls, duplicates"

**Status:**
- `DataValidation` class exists in SDK
- Not called in notebook execution

**Fix Required:**
- Add validation calls after API responses
- Validate schema of extracted data
- Check row counts, nulls, duplicates

---

### ⚠️ Gap 5: Error Handling Not Verified

**Contract Requirement:**
> "Error handling with retry logic, graceful degradation, structured reporting"

**Status:**
- Need to verify retry logic in SDK
- Need to verify graceful degradation
- Need to verify error reporting

**Fix Required:**
- Review SDK retry implementation
- Test error scenarios
- Verify graceful degradation paths

---

## 🔧 Implementation Plan

### Phase 1: Fix Critical Gaps (Contract Compliance)

#### Task 1.1: Complete Preview Samples

**Action:**
```python
# In sourceZephyr.Notebook, expand preview extraction:
if session.params["preview"]:
    resources = [
        {"name": "projects", "endpoint": "/project/details", "table": "source.sampleProjects"}
    ]
    if first_project_id:
        # Get first release ID
        releases_response = SourceStageHelpers._call_api(...)
        first_release_id = releases_response[0].get("id") if releases_response else None
        
        resources.append({
            "name": "releases", 
            "endpoint": f"/release/project/{first_project_id}", 
            "table": "source.sampleReleases"
        })
        
        if first_release_id:
            # Get first cycle ID
            cycles_response = SourceStageHelpers._call_api(...)
            first_cycle_id = cycles_response[0].get("id") if cycles_response else None
            
            resources.append({
                "name": "cycles",
                "endpoint": f"/cycle/release/{first_release_id}",
                "table": "source.sampleCycles"
            })
            
            if first_cycle_id:
                # Get first execution
                executions_response = SourceStageHelpers._call_api(...)
                first_execution = executions_response[0] if executions_response else None
                first_testcase_id = first_execution.get("testcase", {}).get("id") if first_execution else None
                
                resources.append({
                    "name": "executions",
                    "endpoint": f"/execution/cycle/{first_cycle_id}",
                    "table": "source.sampleExecutions"
                })
                
                if first_testcase_id:
                    resources.append({
                        "name": "testcases",
                        "endpoint": f"/testcase/{first_testcase_id}",
                        "table": "source.sampleTestcases"
                    })
    
    table_count = SourceStageHelpers.extract_preview_sample(...)
```

**Files to Modify:**
- `sourceZephyr.Notebook/notebook_content.py`

---

#### Task 1.2: Complete Hierarchical Validation

**Action:**
```python
# Add validation for all hierarchy levels:

# 1. Projects → Releases (already done)
if first_project_id:
    project_result = SourceStageHelpers.validate_api_resource_access(...)

# 2. Releases → Cycles (NEW)
if first_project_id:
    releases_response = SourceStageHelpers._call_api(...)
    first_release_id = releases_response[0].get("id") if releases_response else None
    if first_release_id:
        cycle_result = SourceStageHelpers.validate_api_resource_access(
            base_url=base_url,
            api_token=api_token,
            resource_endpoint="/cycle/release/{releaseId}",
            resource_id=first_release_id,
            logger=log,
            timeout=10
        )
        session.add_capability("cycleAccessVerified", **cycle_result)

# 3. Cycles → Executions (NEW)
if first_cycle_id:
    execution_result = SourceStageHelpers.validate_api_resource_access(
        base_url=base_url,
        api_token=api_token,
        resource_endpoint="/execution/cycle/{cycleId}",
        resource_id=first_cycle_id,
        logger=log,
        timeout=10
    )
    session.add_capability("executionAccessVerified", **execution_result)

# 4. Executions → Test Cases (NEW)
# Get testcase ID from execution and validate
```

**Files to Modify:**
- `sourceZephyr.Notebook/notebook_content.py`

---

### Phase 2: Verify Quality (Testing & Validation)

#### Task 2.1: Run Test Suite

**Action:**
```bash
cd Data/zephyr
pytest --cov=. --cov-report=html --cov-report=term
```

**Verify:**
- Coverage percentage >75%
- All tests pass
- Coverage report generated

**Fix:**
- Add missing test cases if coverage <75%
- Fix failing tests
- Document coverage in README

---

#### Task 2.2: Add Data Validation

**Action:**
```python
# After each API call, validate response:
if session.params["preview"]:
    table_count = SourceStageHelpers.extract_preview_sample(...)
    
    # Validate extracted data
    for resource in resources:
        table_name = resource["table"]
        df = spark.table(table_name)
        
        # Validate schema
        validation_result = DataValidation.validate_dataframe_schema(
            df=df,
            expected_schema=expected_schemas.get(table_name),
            logger=log
        )
        
        # Validate row count
        row_count_result = DataValidation.validate_row_count(
            df=df,
            min_rows=1,
            max_rows=sample_limit,
            logger=log
        )
        
        # Check for nulls in critical fields
        null_check = DataValidation.check_for_nulls(
            df=df,
            critical_fields=["id"],
            logger=log
        )
```

**Files to Modify:**
- `sourceZephyr.Notebook/notebook_content.py`

---

#### Task 2.3: Verify Error Handling

**Action:**
- Review SDK retry logic in `SourceStageHelpers.validate_api_authentication()`
- Test error scenarios (invalid token, network error, timeout)
- Verify graceful degradation (continues with valid data, logs errors)

**Files to Review:**
- `spectraSDK.Notebook/notebook_content.py` - SourceStageHelpers class

---

### Phase 3: Contract Compliance Verification

#### Task 3.1: Run Full Contract Validation

**Action:**
1. Execute source stage notebook in Fabric
2. Verify all outputs match contract:
   - ✅ source.portfolio exists
   - ✅ source.config exists
   - ✅ source.credentials exists
   - ✅ source.endpoints exists (when bootstrap=True)
   - ✅ source.sampleProjects exists (when preview=True)
   - ✅ source.sampleReleases exists (when preview=True)
   - ✅ source.sampleCycles exists (when preview=True)
   - ✅ source.sampleExecutions exists (when preview=True)
   - ✅ source.sampleTestcases exists (when preview=True)

3. Verify hierarchical validation:
   - ✅ Projects → Releases validated
   - ✅ Releases → Cycles validated
   - ✅ Cycles → Executions validated
   - ✅ Executions → Test Cases validated

4. Document results

---

#### Task 3.2: Update Manifest

**Action:**
- Ensure `manifests/source.manifest.yaml` reflects actual implementation
- Update preview samples section with all 5 tables
- Update hierarchical validation section with all 4 levels
- Add test coverage results

---

## 📊 Success Criteria

### Contract Compliance

- [ ] All 5 preview sample tables created (when preview=True)
- [ ] All 4 hierarchical validations pass
- [ ] Test coverage >75%
- [ ] All data outputs match contract
- [ ] Error handling verified
- [ ] Data validation implemented

### Quality Gates

- [ ] All tests pass
- [ ] Coverage >75%
- [ ] CI/CD pipeline runs successfully
- [ ] Documentation updated
- [ ] Manifest matches implementation

---

## 🎯 Next Steps

1. **Review this plan** - Confirm approach
2. **Start with Phase 1** - Fix critical gaps (preview samples + hierarchical validation)
3. **Verify Phase 2** - Run tests, add validation, verify error handling
4. **Complete Phase 3** - Full contract validation and manifest update

---

**Version:** 1.0.0  
**Date:** 2025-12-06

