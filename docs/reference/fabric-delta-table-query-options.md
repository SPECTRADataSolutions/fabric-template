# Querying Delta Tables in Fabric - Complete Guide

**Date:** 2025-12-06  
**Purpose:** How to read/query Delta tables from Fabric Lakehouse (CLI, REST API, UI)

---

## 🎯 Answer: Limited Options

**Short answer:** Fabric REST API does **NOT** have direct SQL query endpoints. However, you have these options:

---

## ✅ Option 1: Fabric UI - SQL Analytics Endpoint (EASIEST)

**Best for:** Quick verification, manual checks, contract validation

### Steps:

1. **Open Fabric Workspace:**
   ```
   https://app.fabric.microsoft.com
   ```

2. **Navigate to Lakehouse:**
   - Workspace → `zephyr.Workspace`
   - Open `zephyrLakehouse`
   - Click "SQL Analytics" endpoint

3. **Run SQL Queries:**
   ```sql
   -- Verify contract compliance
   SELECT * FROM source.portfolio;
   SELECT COUNT(*) FROM source.endpoints;
   SELECT COUNT(*) FROM source.sampleProjects;
   SELECT COUNT(*) FROM source.sampleReleases;
   SELECT COUNT(*) FROM source.sampleCycles;
   SELECT COUNT(*) FROM source.sampleExecutions;
   SELECT COUNT(*) FROM source.sampleTestcases;
   ```

**Advantages:**
- ✅ Direct SQL execution
- ✅ Visual results
- ✅ No authentication complexity
- ✅ Works immediately

**Disadvantages:**
- ❌ Manual process
- ❌ Not automatable

---

## ⚠️ Option 2: Fabric REST API (LIMITED)

**Status:** ❌ **No direct SQL query endpoint found**

### What REST API Supports:

```bash
# ✅ Workspace management
GET /v1/workspaces/{workspaceId}

# ✅ Lakehouse metadata
GET /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}

# ✅ Pipeline execution
POST /v1/workspaces/{workspaceId}/dataPipelines/{pipelineId}/run

# ❌ SQL queries - NOT AVAILABLE
POST /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/sqlQuery  # Does not exist

# ❌ Table listing - NOT AVAILABLE
GET /v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/tables  # Does not exist
```

### Tested Endpoints:

```python
import requests
import os

# Get token
token_url = f"https://login.microsoftonline.com/{os.getenv('SPECTRA_FABRIC_TENANT_ID')}/oauth2/v2.0/token"
token_data = {
    "client_id": os.getenv("SPECTRA_FABRIC_CLIENT_ID"),
    "client_secret": os.getenv("SPECTRA_FABRIC_CLIENT_SECRET"),
    "scope": "https://api.fabric.microsoft.com/.default",
    "grant_type": "client_credentials"
}
response = requests.post(token_url, data=token_data)
access_token = response.json()["access_token"]

workspace_id = "16490dde-33b4-446e-8120-c12b0a68ed88"
lakehouse_id = "5cb93b81-8923-a984-4c5b-a9ec9325ae26"
headers = {"Authorization": f"Bearer {access_token}"}

# ✅ This works - Get lakehouse metadata
api_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}"
response = requests.get(api_url, headers=headers)
print(response.json())  # Shows lakehouse info, but not tables

# ❌ This does NOT work - SQL query endpoint doesn't exist
sql_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/sqlQuery"
response = requests.post(sql_url, headers=headers, json={"query": "SELECT * FROM source.portfolio"})
# Returns 404 or method not allowed
```

---

## ✅ Option 3: Execute Notebook with Query (WORKAROUND)

**Best for:** Automated verification

### Approach:

Create a validation notebook that:
1. Queries all required tables
2. Validates contract compliance
3. Returns results as JSON/output

**Example Notebook Cell:**
```python
# Contract validation queries
validation_results = {}

# Check portfolio table
portfolio_df = spark.sql("SELECT * FROM source.portfolio")
validation_results["portfolio"] = {
    "exists": True,
    "row_count": portfolio_df.count(),
    "has_data": portfolio_df.count() > 0
}

# Check endpoints table
endpoints_df = spark.sql("SELECT COUNT(*) as count FROM source.endpoints")
validation_results["endpoints"] = {
    "exists": True,
    "row_count": endpoints_df.first()["count"]
}

# Check preview samples
for table in ["sampleProjects", "sampleReleases", "sampleCycles", "sampleExecutions", "sampleTestcases"]:
    try:
        df = spark.sql(f"SELECT COUNT(*) as count FROM source.{table}")
        validation_results[table] = {
            "exists": True,
            "row_count": df.first()["count"]
        }
    except Exception as e:
        validation_results[table] = {
            "exists": False,
            "error": str(e)
        }

# Print results
import json
print(json.dumps(validation_results, indent=2))
```

**Execute via REST API:**
```python
# Run notebook via pipeline
pipeline_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/dataPipelines/{pipeline_id}/run"
payload = {
    "notebookPath": "validationNotebook",
    "parameters": {}
}
response = requests.post(pipeline_url, headers=headers, json=payload)
```

---

## ❌ Option 4: Fabric CLI (`fab`)

**Status:** ❌ **Does NOT support querying tables**

**Available Commands:**
```bash
fab auth status          # Check auth
fab dir                  # List workspaces
fab exists zephyr        # Check if workspace exists
fab open zephyr          # Open in browser
```

**Missing:**
- ❌ `fab query` - Does not exist
- ❌ `fab sql` - Does not exist
- ❌ `fab table list` - Does not exist

---

## 🎯 Recommended Approach for Contract Validation

### For Manual Verification:

**Use Fabric UI SQL Analytics:**
1. Open lakehouse → SQL Analytics
2. Run verification queries
3. Document results

### For Automated Verification:

**Option A: Create Validation Notebook**
- Create `contractValidation.Notebook`
- Query all required tables
- Validate contract compliance
- Execute via REST API or UI

**Option B: Enhance Source Notebook**
- Add validation cell at end
- Query all tables and print results
- Run with `test=True` parameter
- Results visible in execution logs

**Option C: Use SDK Validation**
- `SourceStageValidation.validate_all_source_tables()` already exists
- Enhance to query actual table data
- Add to test suite

---

## 📋 Quick Contract Verification Script

**For Manual Use:**

```sql
-- Run in Fabric UI SQL Analytics

-- 1. Verify portfolio table
SELECT 
    'portfolio' as table_name,
    COUNT(*) as row_count,
    MAX(last_updated) as last_updated
FROM source.portfolio;

-- 2. Verify endpoints table
SELECT 
    'endpoints' as table_name,
    COUNT(*) as total_endpoints
FROM source.endpoints;

-- 3. Verify preview samples (contract requires all 5)
SELECT 'sampleProjects' as table_name, COUNT(*) as row_count FROM source.sampleProjects
UNION ALL
SELECT 'sampleReleases', COUNT(*) FROM source.sampleReleases
UNION ALL
SELECT 'sampleCycles', COUNT(*) FROM source.sampleCycles
UNION ALL
SELECT 'sampleExecutions', COUNT(*) FROM source.sampleExecutions
UNION ALL
SELECT 'sampleTestcases', COUNT(*) FROM source.sampleTestcases;

-- 4. Verify config and credentials
SELECT 'config' as table_name, COUNT(*) as row_count FROM source.config
UNION ALL
SELECT 'credentials', COUNT(*) FROM source.credentials;
```

---

## ✅ Summary

| Method | SQL Queries | Automation | Status |
|--------|------------|------------|--------|
| **Fabric UI (SQL Analytics)** | ✅ Yes | ❌ Manual | ✅ Available |
| **Fabric REST API** | ❌ No | ❌ N/A | ❌ Not available |
| **Fabric CLI** | ❌ No | ❌ N/A | ❌ Not available |
| **Notebook Execution** | ✅ Yes | ✅ Yes | ✅ Recommended |
| **SDK Validation** | ✅ Yes | ✅ Yes | ✅ Best for automation |

---

## 🎯 Recommendation

**For Contract Validation:**

1. **Quick Check:** Use Fabric UI SQL Analytics (manual)
2. **Automated:** Enhance `SourceStageValidation` class to:
   - Query all tables via Spark SQL
   - Validate row counts
   - Verify schema compliance
   - Return structured results

**Best Practice:**
- Add validation queries to source notebook's VALIDATE stage
- Run with `test=True` parameter
- Results logged and visible in execution output

---

**Version:** 1.0.0  
**Date:** 2025-12-06

