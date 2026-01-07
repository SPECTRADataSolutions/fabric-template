# Querying Delta Tables from Fabric - Options Guide

**Date:** 2025-12-06  
**Purpose:** How to read/query Delta tables in Fabric Lakehouse from CLI or REST API

---

## 🎯 Options for Querying Delta Tables

### Option 1: Fabric UI (Easiest)

**Location:** Fabric Workspace → Lakehouse → SQL Analytics Endpoint

1. Navigate to your lakehouse in Fabric UI
2. Open "SQL Analytics" endpoint
3. Write SQL queries directly:
   ```sql
   SELECT * FROM source.portfolio
   SELECT COUNT(*) FROM source.endpoints
   ```

**Advantages:**
- ✅ Visual interface
- ✅ No authentication needed
- ✅ Direct SQL execution
- ✅ Results in table format

---

### Option 2: Fabric REST API (Programmatic)

**Endpoint Pattern:**
```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/lakehouses/{lakehouseId}/sqlQuery
```

**Note:** Fabric REST API for SQL queries may require:
- SQL Analytics endpoint ID (different from lakehouse ID)
- Specific authentication scopes
- Query format in request body

**Status:** ⚠️ **NEEDS VERIFICATION** - SQL query endpoints may not be fully documented in public REST API

---

### Option 3: Fabric CLI (Limited)

**Fabric CLI (`fab`) commands:**
```bash
# List workspaces
fab dir

# Check if workspace exists
fab exists zephyr.Workspace

# Open workspace in browser
fab open zephyr.Workspace
```

**Limitations:**
- ❌ No direct SQL query execution
- ❌ No table listing command
- ❌ No data retrieval command

**Status:** ⚠️ **CLI does NOT support querying tables** - Only workspace/item management

---

### Option 4: Azure Synapse Spark REST API (If Available)

Fabric uses Synapse Spark under the hood. You might be able to:
- Execute Spark SQL via REST API
- Access Spark endpoints

**Status:** ⚠️ **NEEDS VERIFICATION** - May require Spark endpoint access

---

## 🔍 Current Fabric REST API Endpoints

**Base URL:** `https://api.fabric.microsoft.com/v1`

### Available Endpoints (from codebase):

```bash
# Workspace management
GET /workspaces
GET /workspaces/{workspaceId}

# Lakehouse management
GET /workspaces/{workspaceId}/lakehouses
GET /workspaces/{workspaceId}/lakehouses/{lakehouseId}
POST /workspaces/{workspaceId}/lakehouses
DELETE /workspaces/{workspaceId}/lakehouses/{lakehouseId}

# Pipeline management
GET /workspaces/{workspaceId}/dataPipelines
POST /workspaces/{workspaceId}/dataPipelines/{pipelineId}/run
GET /workspaces/{workspaceId}/dataPipelines/{pipelineId}/runs/{runId}

# Items
GET /workspaces/{workspaceId}/items
```

### Not Found (Need to Verify):

```bash
# SQL Query execution (may exist but not documented)
POST /workspaces/{workspaceId}/lakehouses/{lakehouseId}/sqlQuery
POST /workspaces/{workspaceId}/sqlAnalytics/{endpointId}/query

# Table listing (may exist)
GET /workspaces/{workspaceId}/lakehouses/{lakehouseId}/tables
GET /workspaces/{workspaceId}/lakehouses/{lakehouseId}/tables/{tableName}/data
```

---

## ✅ Recommended Approach for Contract Validation

### For Quick Verification: Use Fabric UI

**Steps:**
1. Open Fabric workspace: `https://app.fabric.microsoft.com`
2. Navigate to `zephyr.Workspace` → `zephyrLakehouse`
3. Click "SQL Analytics" endpoint
4. Run queries to verify tables:

```sql
-- Verify portfolio table
SELECT * FROM source.portfolio;

-- Verify endpoints table
SELECT COUNT(*) as total_endpoints FROM source.endpoints;

-- Verify preview samples
SELECT COUNT(*) as project_count FROM source.sampleProjects;
SELECT COUNT(*) as release_count FROM source.sampleReleases;
SELECT COUNT(*) as cycle_count FROM source.sampleCycles;
SELECT COUNT(*) as execution_count FROM source.sampleExecutions;
SELECT COUNT(*) as testcase_count FROM source.sampleTestcases;

-- Verify config table
SELECT * FROM source.config;

-- Verify credentials table (masked)
SELECT * FROM source.credentials;
```

### For Automated Verification: Create Python Script

**Option:** Use Fabric REST API to get lakehouse metadata, then verify tables exist:

```python
import requests
import os

# Get access token
token_url = f"https://login.microsoftonline.com/{os.getenv('SPECTRA_FABRIC_TENANT_ID')}/oauth2/v2.0/token"
token_data = {
    "client_id": os.getenv("SPECTRA_FABRIC_CLIENT_ID"),
    "client_secret": os.getenv("SPECTRA_FABRIC_CLIENT_SECRET"),
    "scope": "https://api.fabric.microsoft.com/.default",
    "grant_type": "client_credentials"
}
response = requests.post(token_url, data=token_data)
access_token = response.json()["access_token"]

# Get lakehouse metadata
workspace_id = "16490dde-33b4-446e-8120-c12b0a68ed88"
lakehouse_id = "5cb93b81-8923-a984-4c5b-a9ec9325ae26"
headers = {"Authorization": f"Bearer {access_token}"}

# Check if lakehouse exists and get metadata
api_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}"
response = requests.get(api_url, headers=headers)
print(response.json())
```

---

## 🔬 Testing SQL Query Endpoint

**Let's test if SQL query endpoint exists:**

```python
# Test SQL query endpoint (may or may not exist)
sql_endpoint_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/sqlQuery"
payload = {
    "query": "SELECT * FROM source.portfolio LIMIT 10"
}
response = requests.post(sql_endpoint_url, headers=headers, json=payload)
print(f"Status: {response.status_code}")
print(response.json())
```

---

## 📋 Summary

| Method | Capability | Ease | Automation |
|--------|-----------|------|------------|
| **Fabric UI (SQL Analytics)** | ✅ Full SQL queries | ⭐⭐⭐⭐⭐ | ❌ Manual |
| **Fabric REST API** | ⚠️ Unknown (need to test) | ⭐⭐⭐ | ✅ Possible |
| **Fabric CLI** | ❌ Not available | ❌ N/A | ❌ N/A |
| **Python Script** | ✅ Via UI automation or REST | ⭐⭐⭐⭐ | ✅ Yes |

---

## 🎯 Recommendation for Contract Validation

**Best Approach:**

1. **Quick Check:** Use Fabric UI SQL Analytics to verify tables exist and have data
2. **Automated Check:** Create a Python script that:
   - Runs notebook in Fabric (via REST API)
   - Waits for completion
   - Then queries tables via SQL Analytics (if REST API supports it)
   - Or uses Spark SQL via notebook execution

**Alternative:**
- Run notebook with `preview=True` and `test=True` parameters
- Check notebook execution logs/outputs
- Verify tables are created via SDK validation

---

**Next Steps:**
1. Test SQL query REST API endpoint (if it exists)
2. Document actual endpoint if found
3. Create utility script for automated table verification

---

**Version:** 1.0.0  
**Date:** 2025-12-06

