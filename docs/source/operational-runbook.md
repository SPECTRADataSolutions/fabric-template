# Source Stage Operational Runbook

**Date:** 2025-12-08  
**Stage:** Source  
**Source System:** Zephyr Enterprise  
**Contract Version:** 3.0.0  
**SDK Version:** 0.3.0

---

## 📋 Quick Reference

| Item | Value |
|------|-------|
| **Notebook** | `sourceZephyr.Notebook` |
| **Pipeline** | `zephyrPipeline.DataPipeline` |
| **Lakehouse** | `zephyrLakehouse` |
| **Workspace ID** | `16490dde-33b4-446e-8120-c12b0a68ed88` |
| **Discord Channel** | `#zephyr-source` (notifications) |
| **Owner** | Data Platform Team |

---

## ✅ Health Checklist

**Before every run, verify:**

- [ ] Variable Library `zephyrVariables` exists and is accessible
- [ ] Required variables populated: `BASE_URL`, `API_TOKEN`, `BASE_PATH`, `SOURCE_SYSTEM`, `CONTRACT_VERSION`
- [ ] API token valid (not expired, has required permissions)
- [ ] Network reachability to Zephyr API base URL
- [ ] Lakehouse accessible (`zephyrLakehouse`)
- [ ] SDK notebook `spectraSDK.Notebook` synced to Git

**After every run, verify:**

- [ ] Activity log entry created in `log.source` with `status='Success'`
- [ ] All output tables exist: `source.portfolio`, `source.config`, `source.credentials`, `source.endpoints`
- [ ] `source.portfolio.auth_status = 'Success'`
- [ ] `source.endpoints` has 224 rows (endpoint catalog complete)
- [ ] Discord notification received (if configured)
- [ ] No critical errors in activity log

---

## 🔍 Troubleshooting Common Failures

### 1. Authentication Failure

**Symptom:**
- Stage fails with `AuthenticationError`
- Discord notification: "Zephyr Enterprise Stage Failed"
- Activity log: `status='Failed'`, `error_message` contains authentication error

**Diagnosis:**
```sql
-- Check credentials table
SELECT * FROM source.credentials;

-- Check activity log for error details
SELECT execution_id, status, error_message, error_summary 
FROM log.source 
WHERE status = 'Failed' 
ORDER BY recorded_at DESC 
LIMIT 1;
```

**Common Causes:**
- API token expired or revoked
- API token missing required permissions
- Base URL incorrect (Variable Library: `BASE_URL`)
- Base path incorrect (Variable Library: `BASE_PATH`)
- Network connectivity issue

**Resolution:**
1. Verify API token in Variable Library (`zephyrVariables.API_TOKEN`)
2. Test token manually:
   ```bash
   curl -H "Authorization: Bearer {TOKEN}" {BASE_URL}{BASE_PATH}/project/details
   ```
3. If token invalid, generate new token in Zephyr UI
4. Update Variable Library with new token
5. Re-run Source stage

**Escalation:** If token valid but authentication fails, check Zephyr API status or escalate to Zephyr support.

---

### 2. Endpoint Validation Failure

**Symptom:**
- Validation warnings: "Endpoint validation failed: X errors"
- Duplicate endpoints reported
- Missing endpoints reported

**Diagnosis:**
```sql
-- Check endpoint catalog
SELECT COUNT(*) as total, 
       COUNT(DISTINCT full_path || http_method) as unique,
       COUNT(*) - COUNT(DISTINCT full_path || http_method) as duplicates
FROM source.endpoints;

-- Check portfolio for endpoint metrics
SELECT total_endpoints, hierarchical_endpoints, endpoint_success_rate
FROM source.portfolio;
```

**Common Causes:**
- Endpoint catalog contains duplicates (SDK issue)
- Endpoint count mismatch (SDK version mismatch)
- Validation logic too strict

**Resolution:**
1. Check SDK version in `source.config` (should be `0.3.0`)
2. Verify `spectraSDK.Notebook` is up-to-date in Git
3. Check validation errors in activity log `error_summary` field
4. If duplicates found, check SDK endpoint catalog (should be 224 unique endpoints)

**Escalation:** If SDK issue, check Git for latest SDK version or create GitHub issue.

---

### 3. Table Creation/Registration Failure

**Symptom:**
- Warning: "Registration failed: source.xxx - Invalid root directory"
- Tables exist but not queryable via Spark SQL
- Delta table paths incorrect

**Diagnosis:**
```sql
-- Check if tables exist in metastore
SHOW TABLES IN source;

-- Check table paths
DESCRIBE DETAIL source.portfolio;
DESCRIBE DETAIL source.config;
DESCRIBE DETAIL source.credentials;
DESCRIBE DETAIL source.endpoints;
```

**Common Causes:**
- Schema not created (`source` schema missing)
- Path format incorrect (must start with `Tables/`)
- Lakehouse not accessible
- Permission issue

**Resolution:**
1. Create schema if missing:
   ```sql
   CREATE SCHEMA IF NOT EXISTS source;
   CREATE SCHEMA IF NOT EXISTS log;
   ```
2. Verify table paths start with `Tables/` (not `Files/`)
3. Check lakehouse permissions
4. Re-run Source stage (tables overwritten on each run)

**Escalation:** If schema creation fails, check Fabric lakehouse permissions or escalate to Fabric support.

---

### 4. Variable Library Access Failure

**Symptom:**
- Error: "Variable not found: BASE_URL"
- Error: "Required variable missing"
- Variable Library not accessible

**Diagnosis:**
```python
# Check Variable Library in notebook
from notebookutils import variableLibrary
vars = variableLibrary.get_variable("zephyrVariables_BASE_URL")
print(vars)
```

**Common Causes:**
- Variable Library name incorrect (`zephyrVariables` must match)
- Variable not set in Variable Library
- Variable Library not linked to pipeline/environment
- Permission issue

**Resolution:**
1. Verify Variable Library name matches in notebook: `NotebookSession("zephyrVariables")`
2. Check Variable Library in Fabric UI:
   - Workspace → Variable Libraries → `zephyrVariables`
   - Verify all required variables exist
3. Required variables:
   - `BASE_URL` (Zephyr API base URL)
   - `API_TOKEN` (Zephyr API token)
   - `BASE_PATH` (API base path, e.g., `/flex/services/rest/latest`)
   - `SOURCE_SYSTEM` (must be `zephyr`)
   - `CONTRACT_VERSION` (must be `3.0.0`)
   - `SOURCE_NAME` (e.g., `Zephyr Enterprise`)
   - `STAGE` (must be `source`)
   - `NOTEBOOK_NAME` (e.g., `sourceZephyr`)
4. Link Variable Library to pipeline/environment if not linked

**Escalation:** If Variable Library inaccessible, check Fabric workspace permissions.

---

### 5. Activity Log Registration Failure

**Symptom:**
- Warning: "Registration failed: log.source - Invalid root directory"
- Activity log data written but not queryable
- Schema `log` not found

**Diagnosis:**
```sql
-- Check if log schema exists
SHOW SCHEMAS LIKE 'log';

-- Check if table exists
SHOW TABLES IN log;

-- Query by path directly
SELECT * FROM delta.`Tables/log/sourcelog` ORDER BY recorded_at DESC LIMIT 1;
```

**Common Causes:**
- Schema `log` not created
- Path format issue (must be `Tables/log/...`)
- Registration retry failed

**Resolution:**
1. Activity log registration failure is **non-critical** (data still written)
2. Query by path if registration failed: `SELECT * FROM delta.\`Tables/log/sourcelog\``
3. Create schema manually if needed:
   ```sql
   CREATE SCHEMA IF NOT EXISTS log;
   ```
4. Re-run Source stage (registration retries automatically)

**Note:** Activity log registration failures don't fail the stage - data is still accessible by path.

---

### 6. SDK Not Found

**Symptom:**
- Error: "ZEPHYR_ENDPOINTS_CATALOG not found"
- Error: "Ensure %run spectraSDK is executed before this block"

**Diagnosis:**
- Check notebook structure - `%run spectraSDK` must be in separate cell before main code
- Verify `spectraSDK.Notebook` exists in workspace
- Check Git sync status

**Resolution:**
1. Verify `spectraSDK.Notebook` exists in Fabric workspace
2. Ensure `%run spectraSDK` is in its own cell (no other code in that cell)
3. Ensure `%run spectraSDK` cell executes before main code cell
4. Sync `spectraSDK.Notebook` from Git if missing

**Escalation:** If SDK notebook missing, check Git repository or recreate from `Data/zephyr/spectraSDK.Notebook/`.

---

## 🚨 Escalation Paths

### Severity 1 (Critical - Pipeline Blocked)
**Criteria:**
- Authentication completely broken (no valid token)
- All Source runs failing for >2 hours
- Critical bug preventing Source execution

**Escalation:**
1. Discord: `#spectra-data-pipelines` (mention @Data Platform)
2. Create GitHub issue with label `severity:critical`
3. Check Discord notifications for automatic alerts

### Severity 2 (High - Degraded Functionality)
**Criteria:**
- Non-critical validation errors
- Partial endpoint failures
- Table registration warnings (non-blocking)

**Escalation:**
1. Discord: `#zephyr-source` channel
2. Create GitHub issue with label `severity:high`
3. Document in activity log `error_summary`

### Severity 3 (Medium - Operational Issues)
**Criteria:**
- Variable Library configuration issues
- SDK version mismatches
- Documentation gaps

**Escalation:**
1. Update documentation
2. Create GitHub issue with label `severity:medium`
3. Fix in next development cycle

---

## 📊 Monitoring & Metrics

### Key Metrics

**Activity Log Query:**
```sql
-- Latest execution status
SELECT execution_id, status, duration_seconds, capabilities, error_message
FROM log.source
ORDER BY recorded_at DESC
LIMIT 1;

-- Success rate (last 7 days)
SELECT 
  COUNT(*) as total_runs,
  SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) as successful_runs,
  AVG(duration_seconds) as avg_duration_seconds
FROM log.source
WHERE recorded_at >= DATE_SUB(CURRENT_TIMESTAMP(), 7);
```

**Portfolio Health:**
```sql
-- Source system health snapshot
SELECT 
  source_system,
  auth_status,
  total_endpoints,
  endpoint_success_rate,
  hierarchical_access_validated,
  last_updated
FROM source.portfolio;
```

**Endpoint Catalog Health:**
```sql
-- Endpoint catalog completeness
SELECT 
  COUNT(*) as total_endpoints,
  COUNT(DISTINCT full_path || http_method) as unique_endpoints,
  COUNT(*) - COUNT(DISTINCT full_path || http_method) as duplicates
FROM source.endpoints;
```

---

## 🔄 Recovery Scenarios

### Scenario 1: Complete Re-run After Failure

**When:** Source stage failed, need to re-run

**Steps:**
1. Fix root cause (see Troubleshooting section)
2. Re-run notebook in Fabric UI or pipeline
3. Verify activity log shows `status='Success'`
4. Check all output tables exist and validated

**No manual cleanup required** - Source stage is idempotent (overwrites tables on each run).

---

### Scenario 2: Variable Library Update

**When:** API token rotated, base URL changed, etc.

**Steps:**
1. Update Variable Library in Fabric UI
2. Verify variable names match exactly (case-sensitive)
3. Re-run Source stage (no code changes needed)
4. Verify `source.credentials.validation_status = 'Success'`

**No code changes required** - Source stage reads from Variable Library at runtime.

---

### Scenario 3: SDK Update

**When:** SDK notebook updated in Git, need to sync to Fabric

**Steps:**
1. Pull latest SDK changes from Git
2. Sync `spectraSDK.Notebook` to Fabric workspace (Git sync)
3. Verify SDK version in `source.config.sdk_version` matches expected
4. Re-run Source stage to verify compatibility

**Note:** SDK changes may require Source stage re-run if breaking changes.

---

### Scenario 4: Lakehouse Schema Recreation

**When:** Schemas corrupted or deleted

**Steps:**
1. Recreate schemas:
   ```sql
   CREATE SCHEMA IF NOT EXISTS source;
   CREATE SCHEMA IF NOT EXISTS log;
   ```
2. Re-run Source stage (tables will be created automatically)
3. Verify all tables registered and queryable

**No data loss** - Source stage recreates all tables on each run (overwrite mode).

---

## 📝 Known Limitations

**Reference:** See [`docs/bug-and-blocker-registry.md`](../bug-and-blocker-registry.md) for complete registry.

**Critical Blockers:**
- BLOCKER-001: Requirement creation API broken (affects Prepare stage test data)
- BLOCKER-002: Folder creation API broken (affects Prepare stage test data)

**API Bugs:**
- BUG-001: `/requirementtree/add` creates folders, not requirements
- BUG-002: Cycle phase `startDate` required but not documented
- BUG-003: Release `globalRelease` vs `projectRelease` conflict
- BUG-004: Testcase payload must be wrapped
- BUG-005: Folder `parentId: null` rejected as string

**Workarounds:** All workarounds documented in bug registry.

---

## 🔗 Related Documentation

- **Contract:** [`contracts/source.contract.yaml`](../../contracts/source.contract.yaml)
- **Procedures:** [`docs/source/procedures.md`](procedures.md)
- **Bug Registry:** [`docs/bug-and-blocker-registry.md`](../bug-and-blocker-registry.md)
- **SDK Documentation:** [`spectraSDK.Notebook`](../../spectraSDK.Notebook/)
- **Enhancement Analysis:** [`docs/SOURCE-STAGE-ENHANCEMENT-ANALYSIS.md`](../SOURCE-STAGE-ENHANCEMENT-ANALYSIS.md)

---

## 📞 Support Contacts

| Role | Contact |
|------|---------|
| **Primary Owner** | Data Platform Team |
| **Discord Channel** | `#zephyr-source` |
| **Escalation Channel** | `#spectra-data-pipelines` |
| **GitHub Repository** | `SPECTRADataSolutions/zephyr` |

---

**Last Updated:** 2025-12-08  
**Maintained By:** Data Platform Team  
**Review Cycle:** Quarterly or on significant changes

