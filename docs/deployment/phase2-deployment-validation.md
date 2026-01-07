# Phase 2: Deployment Validation Plan

**Date:** 2025-12-05  
**Status:** 🟡 Ready to Start  
**Dependencies:** Phase 1 Complete ✅

---

## 🎯 Objective

Validate the Zephyr source stage in **all execution modes and parameter combinations** to ensure SPECTRA-grade reliability across all scenarios.

---

## 📋 Test Scenarios

### 1. Parameter Combination Testing

**Test 1.1: Bootstrap Only**
```python
bootstrap = True
backfill = False
preview = False
```
**Expected:**
- ✅ `source.config` created
- ✅ `source.credentials` created
- ✅ `source.endpoints` created (228 rows)
- ✅ `source.portfolio` created
- ❌ No preview sample tables

**Test 1.2: Bootstrap + Preview**
```python
bootstrap = True
backfill = False
preview = True
```
**Expected:**
- ✅ All bootstrap tables created
- ✅ `source.sample_projects` created (2 rows)
- ✅ `source.sample_releases` created (2 rows)
- ✅ `source.sample_cycles` created (2 rows)
- ✅ `source.sample_executions` created (2 rows)
- ✅ `source.sample_testcases` created (2 rows)

**Test 1.3: Preview Only (No Bootstrap)**
```python
bootstrap = False
backfill = False
preview = True
```
**Expected:**
- ✅ Existing tables remain
- ✅ Preview sample tables created
- ⚠️ Should handle gracefully if endpoints table missing

**Test 1.4: Backfill Mode**
```python
bootstrap = False
backfill = True
preview = False
```
**Expected:**
- ✅ Watermark reset logic executed
- ✅ All data extracted from epoch
- ⚠️ May take longer - validate timeout settings

### 2. Execution Mode Testing

**Test 2.1: Interactive Mode (Fabric UI)**
- ✅ Debug logging enabled (verbose)
- ✅ Enhanced diagnostics visible
- ✅ All tables appear in Fabric UI

**Test 2.2: Pipeline Mode (Scheduled Execution)**
- ✅ Clean INFO-level logs (no DEBUG noise)
- ✅ Execution completes successfully
- ✅ Tables accessible to downstream stages

### 3. Schema Validation

**Test 3.1: Portfolio Table Schema**
```sql
DESCRIBE source.portfolio
```
**Validate:**
- ✅ All 15 fields present
- ✅ Correct data types
- ✅ Nullable fields properly marked
- ✅ Primary key considerations

**Test 3.2: Endpoints Table Schema**
```sql
SELECT COUNT(*) FROM source.endpoints
-- Should be 228
```
**Validate:**
- ✅ All 228 endpoints present
- ✅ All required fields populated
- ✅ Category distribution matches catalog

**Test 3.3: Config Table Schema**
```sql
SELECT * FROM source.config
```
**Validate:**
- ✅ All 7 config rows present
- ✅ Values match execution context
- ✅ SDK version correct (0.3.0)

**Test 3.4: Credentials Table Schema**
```sql
SELECT credential_value FROM source.credentials
```
**Validate:**
- ✅ Token masked correctly (`***_XXX` format)
- ✅ Validation status = "Success"
- ✅ No plaintext tokens

### 4. Data Quality Validation

**Test 4.1: Portfolio Data Quality**
- ✅ Single row per source system
- ✅ `discovery_date` preserved on updates
- ✅ `last_updated` updates on each run
- ✅ `endpoint_categories` JSON is valid
- ✅ `endpoint_success_rate` between 0.0-1.0

**Test 4.2: Endpoints Data Quality**
- ✅ No duplicate endpoints
- ✅ All endpoints have required fields
- ✅ `hierarchical` flag accuracy
- ✅ Category distribution reasonable

**Test 4.3: Preview Samples Quality**
- ✅ All sample tables have exactly 2 rows
- ✅ Data structure matches API response
- ✅ No null values in critical fields

### 5. Error Handling Validation

**Test 5.1: Invalid API Token**
- ⚠️ Graceful failure handling
- ✅ Error logged clearly
- ✅ Partial tables created (config, endpoints catalog)
- ✅ Credentials table shows "Failed" status

**Test 5.2: Network Timeout**
- ⚠️ Timeout handling
- ✅ Retry logic executes
- ✅ Partial success reported

**Test 5.3: Missing Variable Library Variables**
- ⚠️ Clear error message
- ✅ Lists missing variables
- ✅ No partial execution

### 6. Integration Testing

**Test 6.1: Multiple Sequential Runs**
- Run 1: `bootstrap=True, preview=True`
- Run 2: `bootstrap=False, preview=True`
- Run 3: `bootstrap=False, preview=False`
- **Validate:** Each run completes successfully, tables update correctly

**Test 6.2: Schema Evolution**
- Run 1: Current schema
- Run 2: Modified schema (add field to portfolio)
- **Validate:** Schema evolution handled gracefully

**Test 6.3: Table Cleanup and Recreation**
- Drop all `source.*` tables
- Run with `bootstrap=True`
- **Validate:** All tables recreated successfully

---

## 📊 Success Criteria

### Phase 2 Complete When:

- ✅ All 6 test scenarios pass
- ✅ All parameter combinations validated
- ✅ Both execution modes tested
- ✅ Schema validation complete
- ✅ Data quality checks pass
- ✅ Error handling validated
- ✅ Integration tests pass
- ✅ Documentation updated

### SPECTRA-Grade Checklist:

- ✅ Zero execution errors
- ✅ Zero schema mismatches
- ✅ Zero data quality issues
- ✅ Zero missing tables
- ✅ Zero hardcoded values
- ✅ Zero tech debt

---

## 🔧 Testing Tools

1. **Fabric Notebook Execution**
   - Test all parameter combinations interactively
   - Verify logs and outputs

2. **SQL Validation**
   - Use Fabric SQL editor for schema checks
   - Run data quality queries

3. **Pipeline Execution**
   - Create test pipeline
   - Validate scheduled execution

4. **Data Validation SDK**
   - Use `DataValidation` class for automated checks
   - Run validation methods post-execution

---

## 📝 Documentation Updates

After Phase 2 completion:

1. Update `manifests/source.manifest.yaml` with:
   - All validated parameter combinations
   - Execution mode behavior
   - Schema documentation
   - Error handling patterns

2. Update `contracts/source.contract.yaml` with:
   - Validated outputs
   - Parameter requirements
   - Success criteria

3. Create `docs/DEPLOYMENT-GUIDE.md`:
   - Parameter reference
   - Execution mode differences
   - Troubleshooting guide
   - Best practices

---

## ⏱️ Estimated Time

- **Parameter Testing:** 30 minutes
- **Execution Mode Testing:** 20 minutes
- **Schema Validation:** 20 minutes
- **Data Quality:** 30 minutes
- **Error Handling:** 30 minutes
- **Integration Testing:** 30 minutes
- **Documentation:** 30 minutes

**Total:** ~3 hours

---

## 🚀 Next Steps

1. ✅ Phase 1 documented
2. 🟡 Begin Phase 2 testing
3. ⏳ Validate each scenario
4. ⏳ Document results
5. ⏳ Update contracts/manifests
6. ⏳ Phase 2 completion document

