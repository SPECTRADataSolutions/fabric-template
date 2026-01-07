# Running and Monitoring Zephyr Pipeline from CLI

**Date:** 2025-01-29  
**Status:** Active Guide  
**Purpose:** Run and monitor Fabric pipeline executions from command line

---

## Prerequisites

1. **Fabric CLI (`fab`)** installed and authenticated
   ```powershell
   fab --version  # Should show version 1.2.0+
   fab auth login -u <client_id> -p <client_secret> --tenant <tenant_id>
   ```

2. **SPECTRA CLI (`spectra`)** installed (optional, for simpler interface)
   ```powershell
   cd Core/cli
   pip install -e .
   ```

3. **Environment Variables** set (from `.env` in SPECTRA root):
   ```powershell
   $env:SPECTRA_FABRIC_TENANT_ID = "..."
   $env:SPECTRA_FABRIC_CLIENT_ID = "..."
   $env:SPECTRA_FABRIC_CLIENT_SECRET = "..."
   ```

4. **Pipeline synced to Fabric** - The pipeline must exist in Fabric before you can run it via CLI
   - Sync your Git changes to Fabric workspace
   - Get the actual pipeline ID from Fabric UI (URL or properties)
   - Update environment variable or pass via `--pipeline-id` flag

5. **Service Principal Permissions** - The service principal needs execute permissions
   - Grant **Member** or **Contributor** role in Fabric workspace
   - Or grant **DataPipeline.Execute** permission specifically
   - **Note**: If you get 404 on `/run` endpoint, check workspace permissions

---

## Option 1: Using `fab` CLI (Fabric CLI)

### Run Pipeline

**Basic run:**
```powershell
fab pipeline run zephyr/zephyrPipeline.DataPipeline
```

**With parameters:**
```powershell
fab pipeline run zephyr/zephyrPipeline.DataPipeline `
  --parameters '{"init_mode": true, "debug_mode": true}'
```

**Note:** Replace `zephyr` with your workspace name if different.

### Check Pipeline Status

**List recent runs:**
```powershell
fab pipeline runs zephyr/zephyrPipeline.DataPipeline
```

**Get specific run status:**
```powershell
fab pipeline run-status zephyr/zephyrPipeline.DataPipeline --run-id <runId>
```

**Note:** Check `fab pipeline --help` for exact command syntax (may vary by version).

---

## Option 2: Using `spectra` CLI (SPECTRA Wrapper) ✅ RECOMMENDED

### Run Pipeline

**Basic run:**
```powershell
cd C:\Users\markm\OneDrive\SPECTRA
spectra pipeline refresh zephyr dxc
```

**With parameters:**
```powershell
# Run with init_mode=true (bootstrap endpoints)
spectra pipeline refresh zephyr dxc --init-mode

# Run with debug logging
spectra pipeline refresh zephyr dxc --debug-mode

# Run with multiple parameters
spectra pipeline refresh zephyr dxc --init-mode --debug-mode
```

**With monitoring (auto-monitor until completion):**
```powershell
# Run and monitor (checks every 10s, max 10 minutes)
spectra pipeline refresh zephyr dxc --init-mode --monitor

# Custom monitoring interval
spectra pipeline refresh zephyr dxc --init-mode --monitor --monitor-interval 5 --monitor-max-wait 300
```

**How it works:**
- Resolves workspace/pipeline IDs from `Data/zephyr/tenants/dxc.yaml` (or environment variables)
- Calls Fabric REST API to trigger pipeline
- Returns run ID and status
- Optionally monitors until completion

**Environment Variables (if tenant file missing):**
```powershell
$env:SPECTRA_DXC_ZEPHYR_FABRIC_WORKSPACE_ID = "<workspace-id>"
$env:SPECTRA_ZEPHYR_FABRIC_PIPELINE_ID = "<pipeline-id>"
```

---

## Option 3: Direct Fabric REST API

### Run Pipeline

```powershell
# Get access token
$token = (az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken -o tsv)

# Or use service principal
$body = @{
    client_id = $env:SPECTRA_FABRIC_CLIENT_ID
    client_secret = $env:SPECTRA_FABRIC_CLIENT_SECRET
    scope = "https://api.fabric.microsoft.com/.default"
    grant_type = "client_credentials"
} | ConvertTo-Json

$tokenResponse = Invoke-RestMethod -Uri "https://login.microsoftonline.com/$($env:SPECTRA_FABRIC_TENANT_ID)/oauth2/v2.0/token" `
    -Method Post -Body $body -ContentType "application/json"
$token = $tokenResponse.access_token

# Trigger pipeline run
$headers = @{
    Authorization = "Bearer $token"
    ContentType = "application/json"
}

$workspaceId = "16490dde-33b4-446e-8120-c12b0a68ed88"
$pipelineId = "be9d0663-d383-4fe6-a0aa-8ed4781e9e87"

$runBody = @{
    parameters = @{
        init_mode = $true
        debug_mode = $false
        full_run_mode = $false
    }
} | ConvertTo-Json

$runResponse = Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/workspaces/$workspaceId/dataPipelines/$pipelineId/run" `
    -Method Post -Headers $headers -Body $runBody

$runId = $runResponse.id
Write-Host "Pipeline triggered. Run ID: $runId"
```

### Monitor Pipeline Run

```powershell
# Check run status
$statusResponse = Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/workspaces/$workspaceId/dataPipelines/$pipelineId/runs/$runId" `
    -Method Get -Headers $headers

Write-Host "Status: $($statusResponse.status)"
Write-Host "Start Time: $($statusResponse.startTime)"
Write-Host "End Time: $($statusResponse.endTime)"
```

**Poll for completion:**
```powershell
$runId = "<run-id-from-trigger>"
$maxWait = 600  # 10 minutes
$interval = 10  # Check every 10 seconds

$elapsed = 0
while ($elapsed -lt $maxWait) {
    $statusResponse = Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/workspaces/$workspaceId/dataPipelines/$pipelineId/runs/$runId" `
        -Method Get -Headers $headers
    
    $status = $statusResponse.status
    Write-Host "[$elapsed s] Status: $status"
    
    if ($status -eq "Succeeded" -or $status -eq "Failed" -or $status -eq "Cancelled") {
        Write-Host "Pipeline completed with status: $status"
        break
    }
    
    Start-Sleep -Seconds $interval
    $elapsed += $interval
}
```

---

## Option 4: Standalone Monitoring Script

**Run and monitor:**
```powershell
cd Data/zephyr
python scripts/monitor_pipeline.py --init-mode --debug-mode
```

**Monitor existing run:**
```powershell
python scripts/monitor_pipeline.py --run-id <run-id-from-previous-run>
```

**With custom settings:**
```powershell
python scripts/monitor_pipeline.py --init-mode --interval 5 --max-wait 300
```

**Available options:**
- `--init-mode` - Set init_mode=true
- `--debug-mode` - Set debug_mode=true
- `--full-run-mode` - Set full_run_mode=true
- `--run-id` - Monitor existing run (skip triggering)
- `--interval` - Status check interval (default: 10s)
- `--max-wait` - Maximum wait time (default: 600s)
- `--workspace-id` - Override workspace ID
- `--pipeline-id` - Override pipeline ID
```

---

## Recommended Approach ✅

**For quick runs:** `spectra pipeline refresh zephyr dxc`  
**For runs with monitoring:** `spectra pipeline refresh zephyr dxc --init-mode --monitor`  
**For standalone monitoring:** `python scripts/monitor_pipeline.py --run-id <id>`

**All options now support:**
- ✅ Parameter passing (`--init-mode`, `--debug-mode`, `--full-run-mode`)
- ✅ Run monitoring (`--monitor` flag)
- ✅ Status polling until completion

---

## Quick Reference

| Task | Command |
|------|---------|
| Run pipeline | `spectra pipeline refresh zephyr dxc` |
| Run with init_mode | `spectra pipeline refresh zephyr dxc --init-mode` |
| Run and monitor | `spectra pipeline refresh zephyr dxc --init-mode --monitor` |
| Monitor existing run | `python scripts/monitor_pipeline.py --run-id <id>` |
| Check status (manual) | Fabric UI or REST API (see Option 3) |

---

## Example Workflow

**1. Run pipeline with init_mode and monitor:**
```powershell
cd C:\Users\markm\OneDrive\SPECTRA
spectra pipeline refresh zephyr dxc --init-mode --monitor
```

**Output:**
```
Triggered zephyr pipeline for tenant 'dxc' in workspace 16490dde-33b4-446e-8120-c12b0a68ed88. runId=abc123 status=submitted

🔍 Monitoring pipeline run (checking every 10s)...
[14:30:15] Status: Running
[14:30:25] Status: Running
[14:30:35] Status: Succeeded

✅ Pipeline succeeded
📊 View details: https://app.fabric.microsoft.com/workspaces/.../runs/abc123
```

**2. Run without monitoring (get run ID, monitor separately):**
```powershell
# Trigger run
spectra pipeline refresh zephyr dxc --init-mode
# Output: runId=abc123

# Monitor separately
python Data/zephyr/scripts/monitor_pipeline.py --run-id abc123
```

