# Pipeline Run Permissions Issue

**Date:** 2025-01-29  
**Status:** Identified Issue  
**Error:** `404 EntityNotFound: The requested resource could not be found` when POSTing to `/run` endpoint

---

## Problem

The service principal can **read** the pipeline (GET succeeds) but cannot **execute** it (POST to `/run` returns 404).

**Test Results:**
- ✅ GET `/workspaces/{id}/dataPipelines/{id}` → 200 OK
- ❌ POST `/workspaces/{id}/dataPipelines/{id}/run` → 404 EntityNotFound

---

## Possible Causes

1. **Missing Permissions**: Service principal needs `DataPipeline.Execute` permission on the workspace
2. **API Endpoint Change**: The `/run` endpoint might have changed or require different path
3. **Pipeline State**: Pipeline might need to be in a specific state (published, enabled, etc.)

---

## Solutions

### Option 1: Grant Execute Permission (Recommended)

1. Open Fabric workspace in UI
2. Go to workspace settings → **Access**
3. Find your service principal (app registration)
4. Grant **Member** or **Contributor** role (includes execute permission)
5. Or grant specific **DataPipeline.Execute** permission if available

### Option 2: Use `fab` CLI Instead

The `fab` CLI might handle authentication/permissions differently:

```powershell
fab auth login -u <client_id> -p <client_secret> --tenant <tenant_id>
fab cd zephyr.Workspace
fab job run zephyrPipeline.DataPipeline
```

### Option 3: Check API Documentation

Verify the correct endpoint format:
- Current: `POST /v1/workspaces/{workspaceId}/dataPipelines/{pipelineId}/run`
- Alternative: `POST /v1/workspaces/{workspaceId}/dataPipelines/{pipelineId}/runs` (note plural)

---

## Next Steps

1. ✅ Verify pipeline exists (GET works)
2. ⏳ Check service principal permissions in Fabric workspace
3. ⏳ Try using `fab` CLI as alternative
4. ⏳ Verify API endpoint format with Fabric REST API docs

---

## References

- [Fabric REST API Documentation](https://learn.microsoft.com/en-us/rest/api/fabric/)
- [Fabric CLI Documentation](https://microsoft.github.io/fabric-cli/)




