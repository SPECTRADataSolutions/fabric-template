# Zephyr Source Stage Readiness Requirements
**Date:** 2025-01-29  
**Status:** ❌ **NOT READY FOR PREPARE**

---

## Executive Summary

The Zephyr Source stage currently only performs a **handshake validation** (tests `/project` endpoint). This is **insufficient** for Prepare stage to proceed.

**The Source stage must prove full environment readiness** by validating that ALL 228 endpoints are accessible and that authentication has access to everything needed. The Prepare stage will sample every endpoint to build the schema - Source must ensure they're all reachable.

---

## Current State

### What's Working ✅

- ✅ Contract files exist (`contract.yaml`, `contracts/source.contract.yaml`)
- ✅ `/project` endpoint tested and working
- ✅ Authentication validated for `/project` endpoint
- ✅ Manifest entry created with run evidence

### What's Missing ❌

- ❌ **Only 1 of 228 endpoints tested** (`/project` only)
- ❌ **No environment health check for all 228 endpoints**
- ❌ **Cannot prove auth has access to all endpoints**
- ❌ **Cannot prove environment is configured correctly**
- ❌ **Endpoints table not populated** (all 228 endpoints should be catalogued)

---

## Required: Complete Endpoint Health Check

**IMPORTANT:** Zephyr has **228 endpoints** documented in `docs/endpoints.json`. The Source stage must validate that **ALL endpoints are accessible** and that authentication works for all of them. The Prepare stage will sample every endpoint to build the schema - Source must ensure they're all reachable.

**Key Principle:** Don't scope down - understand what Zephyr provides and design perfect model for ALL data required for reporting.

### Health Check Strategy

The Source stage should:
1. **Populate endpoints table** with all 228 endpoints (via `init_mode`)
2. **Health check all GET endpoints** (76+ data extraction endpoints)
3. **Validate auth works** for all accessible endpoints
4. **Document endpoint status** (accessible, requires auth, not accessible, etc.)
5. **Identify data extraction endpoints** (for Prepare stage to sample)

### Example: Core Data Extraction Endpoints

While we need to validate ALL endpoints, these are examples of critical data extraction endpoints:

### 1. `/project` Endpoint ✅ (Already Done)

- **Status:** ✅ Tested
- **Purpose:** Project catalogue required to scope every downstream request
- **Method:** GET
- **Incremental:** No
- **Validation Required:**
  - ✅ Auth works
  - ✅ Endpoint accessible
  - ✅ Returns expected data structure
  - ✅ Sample data retrieved

### 2. `/release` Endpoint ❌ (MISSING)

- **Status:** ❌ Not tested
- **Purpose:** Release metadata (versions, start/end dates)
- **Method:** GET
- **Incremental:** Yes (field: `lastModifiedOn`)
- **Validation Required:**
  - ❌ Auth works for this endpoint
  - ❌ Endpoint accessible
  - ❌ Returns expected data structure
  - ❌ Sample data retrieved
  - ❌ Incremental field (`lastModifiedOn`) exists in response
  - ❌ Can query with project dependency

### 3. `/cycle` Endpoint ❌ (MISSING)

- **Status:** ❌ Not tested
- **Purpose:** Test cycles tied to releases and projects
- **Method:** GET
- **Incremental:** Yes (field: `lastModifiedOn`)
- **Validation Required:**
  - ❌ Auth works for this endpoint
  - ❌ Endpoint accessible
  - ❌ Returns expected data structure
  - ❌ Sample data retrieved
  - ❌ Incremental field (`lastModifiedOn`) exists in response
  - ❌ Can query with release dependency

### 4. `/execution` Endpoint ❌ (MISSING)

### Additional Endpoints (To Be Validated in Prepare)

**Note:** Prepare stage will sample ALL endpoints to build schema. Source stage should validate that endpoints are accessible, but full discovery happens in Prepare.

**Key Principle:** Don't scope down - understand what Zephyr provides and design perfect model for ALL data required for reporting.

- **Status:** ❌ Not tested
- **Purpose:** Execution level detail for analytics + AI scoring
- **Method:** GET
- **Incremental:** Yes (field: `lastTestedOn`)
- **Validation Required:**
  - ❌ Auth works for this endpoint
  - ❌ Endpoint accessible
  - ❌ Returns expected data structure
  - ❌ Sample data retrieved
  - ❌ Incremental field (`lastTestedOn`) exists in response
  - ❌ Can query with cycle dependency

---

## Additional Considerations

### Project Configuration Risk

- **2 Active Projects:** Only using 2 of 37 projects, but they can be configured differently
- **Risk:** Different configurations = schema inconsistencies, data quality issues
- **Mitigation:** Source stage should test with both active projects, identify configuration differences
- **See:** `docs/risks/project-configuration-risks.md` for full analysis

### Data Quality Assumption

- **Key Assumption:** Users of Zephyr and Jira don't understand how to structure data well
- **Implication:** Need robust validation, cleaning, and guardrails
- **Source Stage:** Should validate data quality basics (structure, required fields, etc.)

## Implementation Requirements

### 1. Update Source Notebook

The `sourceZephyr.Notebook/notebook_content.py` must:

1. **Populate endpoints table** with all 228 endpoints (via `init_mode`)
2. **Health check all GET endpoints** (validate they're accessible)
3. **Validate auth works** for all accessible endpoints
4. **Document endpoint status** (accessible, auth required, not accessible)
5. **Generate comprehensive health check report** for all endpoints

### 2. Update Manifest

The `manifests/source.manifest.yaml` must include:

```yaml
endpoints_tested:
  - endpoint: "/project"
    status: "success"
    http_status: "200"
    count: 37
    sample: [...]
  - endpoint: "/release"
    status: "success|fail"
    http_status: "200|4xx|5xx"
    count: 0
    sample: [...]
    incremental_field_validated: true|false
  - endpoint: "/cycle"
    status: "success|fail"
    http_status: "200|4xx|5xx"
    count: 0
    sample: [...]
    incremental_field_validated: true|false
  - endpoint: "/execution"
    status: "success|fail"
    http_status: "200|4xx|5xx"
    count: 0
    sample: [...]
    incremental_field_validated: true|false

readiness:
  all_endpoints_accessible: true|false
  auth_has_full_access: true|false
  environment_configured: true|false
  ready_for_prepare: true|false
```

### 3. Update Contract

The `contracts/source.contract.yaml` obligations should include:

```yaml
obligations:
  - "Auth succeeds against Zephyr base URL + path."
  - "All 228 endpoints catalogued in Tables/source/zephyr_endpoints."
  - "Endpoint reachability proven for all GET endpoints (health check completed)."
  - "Visibility demonstrated for accessible endpoints (status documented)."
  - "Environment health check passed - all accessible endpoints validated."
  - "No data landing in Source stage (reference tables only)."
  - "Log/manifest entry recorded for each run with endpoint health check results."
```

---

## Success Criteria

The Source stage is ready for Prepare when:

- ✅ **All 228 endpoints catalogued** in `Tables/source/zephyr_endpoints`
- ✅ **Health check completed** for all GET endpoints (76+ data extraction endpoints)
- ✅ **Auth validated** for all accessible endpoints
- ✅ **Endpoint status documented** (accessible, auth required, not accessible)
- ✅ **Environment health check passed** - all accessible endpoints validated
- ✅ **Manifest updated** with endpoint health check results
- ✅ **Readiness status**: `ready_for_prepare: true`

---

## Next Steps

1. **Generate endpoints module** and populate endpoints table (all 228 endpoints)
2. **Update Source Notebook** to health check all GET endpoints
3. **Add health check logic** to validate environment readiness for all endpoints
4. **Update manifest** with comprehensive endpoint health check results
5. **Update contract** obligations to reflect validation of all endpoints
6. **Run Source stage** and verify all accessible endpoints pass health check
7. **Only then** can Prepare stage proceed

---

**Status:** 🔴 **BLOCKED** - Source stage must complete full endpoint validation before Prepare can proceed.

