# Prepare Stage - Next Steps

**Date:** 2025-12-11  
**Status:** 🎯 Ready for Testing  
**Priority:** High

---

## Current Status

✅ **Completed:**
- Intelligence READ_ENDPOINTS defined with correct paths
- Prepare stage updated to load project → list releases → prioritize 112/106
- Local API testing script created and verified
- Architecture documentation complete

🔧 **In Progress:**
- Testing in Fabric to verify end-to-end flow
- Embedding latest intelligence into SDK

---

## Immediate Next Steps

### 1. Embed Intelligence into SDK ⚠️ **REQUIRED**

**Action:** Run the embedding script to update SDK with latest intelligence

```bash
cd Data/zephyr
python scripts/append_intelligence_to_sdk.py
```

**Why:** Prepare stage needs `ZephyrIntelligence` with `READ_ENDPOINTS` in SDK

**Verify:** Check `spectraSDK.Notebook/notebook_content.py` contains `ZephyrIntelligence` class

---

### 2. Test in Fabric 🧪 **CRITICAL**

**Action:** Run `prepareZephyr` notebook in Fabric with `bootstrap=True`

**Expected Flow:**
1. ✅ Load project 44 (verify exists)
2. ✅ List all releases (should show 80 releases)
3. ✅ Prioritize releases 112 and 106
4. ✅ Fetch cycles from release 112 or 106
5. ✅ Build schema from cycle data
6. ✅ Write to `prepare.schema`, `prepare.dependencies`, `prepare.constraints` tables

**Success Criteria:**
- No errors during execution
- Schema tables created with data
- Schema contains fields from cycle entity
- Dependencies table populated
- Constraints table populated

**If Issues:**
- Check logs for API errors
- Verify `ZephyrIntelligence` is available from SDK
- Verify `READ_ENDPOINTS` paths are correct
- Check if releases 112/106 actually have cycles in Fabric

---

### 3. Verify Schema Tables 📊

**Action:** Query the schema tables to verify they're populated correctly

**Tables to Check:**
- `prepare.schema` - Should have rows for cycle entity with all fields
- `prepare.dependencies` - Should have dependency relationships
- `prepare.constraints` - Should have constraints from intelligence

**Queries:**
```sql
-- Check schema table
SELECT * FROM prepare.schema WHERE entity = 'cycle';

-- Check dependencies
SELECT * FROM prepare.dependencies;

-- Check constraints
SELECT * FROM prepare.constraints;
```

---

### 4. Fix Any Issues 🐛

**If Schema is Empty:**
- Check if cycles were actually fetched
- Verify API responses contain data
- Check if fallback to testcases is needed

**If Intelligence Not Found:**
- Verify SDK embedding worked
- Check if `%run spectraSDK` executed before Prepare code
- Verify `ZephyrIntelligence` is in global namespace

**If API Errors:**
- Check endpoint paths match actual API
- Verify authentication is working
- Check if project 44 is accessible
- Verify releases 112/106 exist and have cycles

---

## Future Enhancements

### Short Term (Next Session)

1. **Add More Entities**
   - Currently only fetching cycles
   - Add releases, projects, testcases to schema discovery
   - Use intelligence dependencies to fetch in correct order

2. **Improve Error Handling**
   - Better fallback logic if cycles empty
   - Retry logic for API calls
   - Clearer error messages

3. **Add Validation**
   - Verify schema completeness
   - Check for required fields
   - Validate dependency relationships

### Medium Term

1. **Automate Intelligence Updates**
   - Script to sync intelligence changes to SDK
   - Validation before embedding
   - Version tracking

2. **Expand Schema Discovery**
   - Fetch multiple entity types
   - Build comprehensive schema
   - Handle nested structures

3. **Add Monitoring**
   - Track schema changes over time
   - Alert on schema drift
   - Log API usage

---

## Testing Checklist

Before running in Fabric, verify locally:

- [x] API endpoints work (tested with `test_zephyr_api_intelligence.py`)
- [x] Releases 112 and 106 have cycles (confirmed)
- [x] Intelligence READ_ENDPOINTS have correct paths
- [ ] Intelligence embedded in SDK (run `append_intelligence_to_sdk.py`)
- [ ] Prepare notebook code is correct
- [ ] Variable Library has required variables (BASE_URL, API_TOKEN, BASE_PATH)

In Fabric:

- [ ] `%run spectraSDK` executes successfully
- [ ] `ZephyrIntelligence` is available in global namespace
- [ ] Project 44 loads successfully
- [ ] Releases list correctly (80 releases)
- [ ] Release 112 or 106 selected
- [ ] Cycles fetched successfully
- [ ] Schema built from cycle data
- [ ] Tables created: `prepare.schema`, `prepare.dependencies`, `prepare.constraints`
- [ ] Tables contain data

---

## Rollback Plan

If issues occur:

1. **Check Logs:** Review Fabric notebook execution logs
2. **Verify SDK:** Ensure `ZephyrIntelligence` is in SDK
3. **Test Locally:** Run `test_zephyr_api_intelligence.py` to verify API
4. **Check Variables:** Verify Variable Library has correct values
5. **Fallback:** Use testcases if cycles don't work

---

## Success Criteria

✅ **Prepare stage is successful when:**
- Schema tables created with data
- Schema contains all fields from cycle entity
- Dependencies table shows relationships
- Constraints table shows API limitations
- No errors during execution
- Can be run repeatedly (idempotent)

---

## Related Documents

- `INTELLIGENCE-ARCHITECTURE.md` - How intelligence works
- `PREPARE-STAGE-PURPOSE.md` - Prepare stage design
- `PREPARE-STAGE-FLOW.md` - Detailed flow
- `tests/test_zephyr_api_intelligence.py` - Local API testing

---

**Last Updated:** 2025-12-11  
**Next Review:** After Fabric testing

