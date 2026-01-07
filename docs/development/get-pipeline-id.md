# How to Get Fabric Pipeline ID

**Purpose:** Find the correct pipeline ID for CLI commands after syncing to Fabric

---

## Method 1: From Fabric UI URL

1. Open Fabric workspace in browser
2. Navigate to your pipeline (e.g., `zephyrPipeline`)
3. Look at the URL:
   ```
   https://app.fabric.microsoft.com/workspaces/{workspaceId}/dataPipelines/{pipelineId}/...
   ```
4. Copy the `pipelineId` from the URL

---

## Method 2: From Pipeline Properties

1. Open pipeline in Fabric UI
2. Click on pipeline name/settings
3. Look for "Pipeline ID" or "Resource ID" in properties
4. Copy the GUID

---

## Method 3: Using Fabric REST API

```powershell
# Get access token
$token = (az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken -o tsv)

# List pipelines in workspace
$workspaceId = "16490dde-33b4-446e-8120-c12b0a68ed88"
$headers = @{
    Authorization = "Bearer $token"
}

$pipelines = Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/workspaces/$workspaceId/dataPipelines" `
    -Method Get -Headers $headers

# Find your pipeline
$pipelines.value | Where-Object { $_.displayName -like "*zephyr*" } | Select-Object displayName, id
```

---

## Method 4: Using `fab` CLI (if available)

```powershell
fab pipeline list zephyr  # If this command exists
```

---

## Update Configuration

Once you have the pipeline ID, either:

**Option A: Set environment variable**
```powershell
$env:SPECTRA_ZEPHYR_FABRIC_PIPELINE_ID = "<actual-pipeline-id>"
```

**Option B: Pass via CLI**
```powershell
python scripts/monitor_pipeline.py --pipeline-id <actual-pipeline-id> ...
```

**Option C: Update tenant config**
Create `Data/zephyr/tenants/dxc.yaml`:
```yaml
workspace:
  id: "16490dde-33b4-446e-8120-c12b0a68ed88"
pipeline:
  id: "<actual-pipeline-id>"
```




