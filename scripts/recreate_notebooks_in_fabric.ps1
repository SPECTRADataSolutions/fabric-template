# Recreate Notebooks in Fabric - Proper Workflow
# This script creates notebooks in Fabric first, then you sync from Fabric to Git

param(
    [string]$Workspace = "zephyr.Workspace"
)

Write-Host "================================================================================"
Write-Host "🔧 Recreate Notebooks in Fabric - SPECTRA-Grade Workflow"
Write-Host "================================================================================"
Write-Host ""

# Load environment variables from SPECTRA root
$spectraRoot = (Get-Item $PSScriptRoot).Parent.Parent.Parent.FullName
$envFile = Join-Path $spectraRoot '.env'
if (Test-Path $envFile) {
    Write-Host "✅ Loading environment variables from: $envFile"
    Get-Content $envFile | Where-Object { $_ -notmatch '^\s*#' -and $_ -match '\S' } | ForEach-Object {
        $parts = $_ -split '=',2
        if ($parts.Length -eq 2) {
            Set-Item -Path ("Env:" + $parts[0].Trim()) -Value $parts[1]
        }
    }
} else {
    Write-Warning "⚠️  .env file not found at: $envFile"
    Write-Warning "   Ensure Fabric credentials are in environment or .env file exists."
}

# Authenticate Fabric CLI
Write-Host ""
Write-Host "🔐 Authenticating Fabric CLI..."
$clientId = $env:SPECTRA_FABRIC_CLIENT_ID.Trim('"')
$clientSecret = $env:SPECTRA_FABRIC_CLIENT_SECRET.Trim('"')
$tenantId = $env:SPECTRA_FABRIC_TENANT_ID.Trim('"')
fab auth login -u $clientId -p $clientSecret -t $tenantId

Write-Host ""
$status = fab auth status
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Fabric CLI authentication failed. Check credentials."
    exit 1
}

Write-Host "✅ Authentication successful"
Write-Host ""

# Verify workspace exists
Write-Host "🔍 Verifying workspace exists: $Workspace"
$workspaceExists = fab exists $Workspace
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Workspace $Workspace not found. Check workspace name."
    exit 1
}
Write-Host "✅ Workspace found"
Write-Host ""

# Create notebooks
$notebooks = @(
    "prepareZephyr",
    "contractValidation"
)

foreach ($notebookName in $notebooks) {
    $notebookPath = "$Workspace/$notebookName.Notebook"
    
    Write-Host "================================================================================"
    Write-Host "📓 Creating notebook: $notebookName"
    Write-Host "================================================================================"
    
    # Check if notebook already exists
    $exists = fab exists $notebookPath
    if ($LASTEXITCODE -eq 0) {
        Write-Warning "⚠️  Notebook $notebookName already exists. Skipping creation."
        Write-Host "   To recreate, delete it first in Fabric UI or via: fab rm $notebookPath"
        Write-Host ""
        continue
    }
    
    # Create notebook
    Write-Host "Creating: $notebookPath"
    fab mkdir $notebookPath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Notebook created: $notebookName"
        
        # Get the logicalId
        $logicalId = fab get $notebookPath -q id
        Write-Host "   logicalId: $logicalId"
    } else {
        Write-Error "❌ Failed to create notebook: $notebookName"
    }
    
    Write-Host ""
}

Write-Host "================================================================================"
Write-Host "✅ Notebook Creation Complete"
Write-Host "================================================================================"
Write-Host ""
Write-Host "📋 Next Steps:"
Write-Host ""
Write-Host "1. Open Fabric UI: $Workspace"
Write-Host "2. Click Source Control (Git icon)"
Write-Host "3. Click Sync to download notebooks to Git (gets proper .platform files)"
Write-Host "4. Verify .platform files have real logicalId (not all zeros)"
Write-Host "5. Restore notebook content from backup or recreate"
Write-Host "6. Commit and push to Git"
Write-Host "7. Sync back to Fabric"
Write-Host ""
Write-Host "📚 Reference: docs/FABRIC-NOTEBOOK-CREATION-WORKFLOW.md"
Write-Host ""

