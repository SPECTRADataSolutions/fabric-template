# Zephyr API Page Size Recommendations
**Date:** 2025-01-29  
**Status:** 🟡 Testing Required

---

## Current Configuration

- **Default Page Size:** 500 (per `manifest.json`)
- **Maximum Value:** NOT documented by Zephyr
- **Jira Reference:** Jira pipeline uses 1000, but different API

---

## Why Not Use Maximum?

Even if the maximum were documented (e.g., 1000), using it is **NOT recommended**:

### 1. Performance & Timeouts
- **Risk:** Large responses take longer to generate/transfer
- **Impact:** Higher timeout risk (30s default)
- **Mitigation:** Smaller pages = faster responses = fewer timeouts

### 2. Memory Usage
- **Risk:** Large responses consume more Spark/Fabric memory
- **Impact:** OOM errors, pipeline instability
- **Mitigation:** Smaller pages = lower memory footprint

### 3. Error Recovery
- **Risk:** Large page failure = lose more data
- **Impact:** Need to retry larger dataset
- **Mitigation:** Smaller pages = smaller blast radius

### 4. Progress Visibility
- **Risk:** Large pages = less granular progress
- **Impact:** Harder to track/debug extraction
- **Mitigation:** Smaller pages = better observability

### 5. Rate Limiting
- **Risk:** Large payloads may hit different limits
- **Impact:** Harder to respect rate limits
- **Mitigation:** Moderate pages = predictable rate limiting

### 6. Server Load
- **Risk:** Large queries impact Zephyr server
- **Impact:** May affect other users
- **Mitigation:** Moderate pages = better "citizenship"

---

## Testing Strategy

### Source Stage Health Checks

Test different page sizes for each endpoint:

| Page Size | Use Case | Expected Behavior |
|-----------|----------|-------------------|
| **100** | Testing, low-risk | Fast, low memory, many requests |
| **500** | Current default | Balanced, moderate requests |
| **1000** | Maximum test | May timeout, high memory, few requests |

### Metrics to Monitor

For each page size, measure:
- ✅ Response time (ms)
- ✅ Memory usage (MB)
- ✅ Error rate (%)
- ✅ Timeout frequency
- ✅ Records per second
- ✅ Total extraction time

### Decision Criteria

Choose page size based on:
1. **Stability** (fewer timeouts/errors) - PRIMARY
2. **Performance** (records per second) - SECONDARY
3. **Resource usage** (memory) - TERTIARY
4. **Request count** (rate limiting) - QUATERNARY

---

## Recommendations by Endpoint

### Projects
- **Current:** 500
- **Rationale:** Small dataset (37 projects, only 2 active)
- **Recommendation:** 500 is fine, could use 1000 if needed

### Releases
- **Current:** 500
- **Rationale:** Moderate dataset per project
- **Recommendation:** Test 500 vs 1000, choose based on stability

### Cycles
- **Current:** 500
- **Rationale:** Moderate dataset per release
- **Recommendation:** Test 500 vs 1000, choose based on stability

### Executions
- **Current:** 500
- **Rationale:** Largest dataset, most records
- **Recommendation:** Test 100, 500, 1000 - likely need 500-1000 range

---

## Implementation

### Per-Endpoint Configuration

```yaml
# In source.plan.yaml or manifest.json
ingestionUnits:
  - name: "projects"
    pagination:
      pageSize: 1000  # Small dataset, can use larger
  - name: "releases"
    pagination:
      pageSize: 500  # Balanced
  - name: "cycles"
    pagination:
      pageSize: 500  # Balanced
  - name: "executions"
    pagination:
      pageSize: 500  # Test and adjust based on volume
```

### Dynamic Testing

During Source stage, implement:
1. Test with 100, 500, 1000
2. Measure metrics
3. Document findings
4. Choose optimal per endpoint
5. Update contract/manifest

---

## Next Steps

1. **Source Stage:** Test page sizes (100, 500, 1000) for each endpoint
2. **Document:** Record response times, memory, errors per page size
3. **Decide:** Choose optimal page size per endpoint
4. **Update:** Contract and manifest with chosen values
5. **Monitor:** Track performance in production, adjust if needed

---

**Last Updated:** 2025-01-29

