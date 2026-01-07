# Zephyr API Pagination & Rate Limits Discovery

**Date:** 2025-01-29  
**Status:** 🟡 Needs Testing/Verification  
**Source:** Contract + API Docs Scraping

---

## Current Information (From Contract)

### Pagination

- **Style:** `offset` (zero-based)
- **Offset Parameter:** `firstresult` (NOT `offset` - this is the actual parameter name)
- **Limit Parameter:** `maxresults` (NOT `maxRecords` - this is the actual parameter name)
- **Status:** ✅ Verified from API documentation
- **Source:** [Zephyr Enterprise REST API Documentation](https://support.smartbear.com/zephyr-enterprise/docs/en/zephyr-enterprise/zephyr-rest-api/search-api.html)
- **Maximum Value:** ⚠️ **NOT DOCUMENTED** - API docs don't specify maximum allowable value
- **Current Default:** 500 (per manifest.json)
- **Jira Reference:** Jira pipeline uses 1000 as default, but different API
- **Notes:**
  - `firstresult` is zero-based (0 = first record)
  - To get next page: increment `firstresult` by `maxresults` value
  - Example: `firstresult=0&maxresults=100` for first 100, then `firstresult=100&maxresults=100` for next 100
  - **Why not use maximum?** See "Page Size Considerations" below

### Rate Limits

- **Burst:** 60 requests (marked TBD - needs testing)
- **Sustained Per Minute:** 300 requests (marked TBD - needs testing)
- **Status:** ⚠️ Values are TBD, need to discover through testing

### Retry Strategy

- **Strategy:** `exponentialBackoff`
- **Max Attempts:** 3
- **Backoff Seconds:** [1, 2, 4]
- **Status:** ✅ Using SPECTRA defaults, may need adjustment

---

## API Documentation

- **URL:** https://zephyrenterprisev3.docs.apiary.io
- **Scraper Run:** ✅ Completed - extracted 228 endpoints
- **Pagination Info:** ❌ Not found in scraped content
- **Rate Limit Info:** ❌ Not found in scraped content

---

## Page Size Considerations

### Why Not Always Use Maximum?

**The maximum value for `maxresults` is NOT documented.** Even if it were (e.g., 1000), using the maximum is generally **NOT recommended** for several reasons:

1. **Performance & Timeouts**

   - Large responses take longer to generate and transfer
   - Higher risk of timeouts (30s default timeout)
   - Server load increases with larger payloads

2. **Memory Usage**

   - Larger responses consume more memory
   - Can cause OOM errors in Spark/Fabric notebooks
   - Impacts overall pipeline stability

3. **Error Recovery**

   - If a large page fails, you lose more data and need to retry more
   - Smaller pages = smaller blast radius on failures
   - Easier to resume from last successful page

4. **Progress Visibility**

   - Smaller pages provide better progress feedback
   - Easier to track extraction progress
   - Better observability and debugging

5. **Rate Limiting**

   - Fewer requests with larger pages, but each request is heavier
   - May hit different rate limits (payload size vs request count)
   - Harder to respect rate limits with variable response sizes

6. **Server Load**
   - Large queries can impact Zephyr server performance
   - May affect other users/processes
   - Better to be a "good citizen" with moderate page sizes

### Recommended Approach

- **Start with 500** (current default in manifest)
- **Test with 100, 500, 1000** during Source stage health checks
- **Monitor:**
  - Response times
  - Memory usage
  - Error rates
  - Timeout frequency
- **Choose based on:**
  - Data volume per endpoint
  - Response time vs page size
  - Stability (fewer timeouts/errors)
  - Balance between request count and payload size

### Testing Strategy

During Source stage, test different page sizes:

- Small (100): Good for testing, low risk
- Medium (500): Current default, balanced
- Large (1000): Test maximum, but expect potential issues
- Document findings and choose optimal value per endpoint

## Action Required

### Source Stage Health Checks

During Source stage health checks, we should:

1. **Test Pagination**

   - Verify `firstresult` and `maxresults` parameters work
   - Test with different page sizes (100, 500, 1000)
   - Measure response times and memory usage per page size
   - Verify pagination works across all endpoints
   - Document optimal page size per endpoint

2. **Discover Rate Limits**

   - Test burst capacity
   - Test sustained rate
   - Monitor for 429 (Too Many Requests) responses
   - Check response headers for rate limit info

3. **Test Retry Behavior**
   - Test with intentional failures
   - Verify exponential backoff works
   - Adjust if needed based on API behavior

### Prepare Stage

- Sample all endpoints to understand pagination requirements
- Document actual rate limits discovered
- Update contract with verified values

---

## Questions to Answer

- [x] Are `firstresult` and `maxresults` the correct parameter names? ✅ YES
- [ ] What is the maximum allowable value for `maxresults`? (NOT documented - need to test)
- [ ] What is the optimal page size per endpoint? (Test 100, 500, 1000)
- [ ] What is the actual burst capacity?
- [ ] What is the actual sustained rate per minute?
- [ ] Are there different limits for different endpoints?
- [ ] What headers indicate rate limit status?
- [ ] How should we handle 429 responses?

---

## Next Steps

1. Run Source stage health checks with rate limit testing
2. Document discovered values
3. Update contract with verified pagination/rate limit info
4. Implement rate limiting in Extract stage based on discovered values

---

**Last Updated:** 2025-01-29
