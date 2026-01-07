# SPECTRA Fabric Template - Project Setup Script
# Replaces all {PROJECT} placeholders with actual project name

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,
    
    [Parameter(Mandatory=$false)]
    [string]$SourceSystem = "",
    
    [Parameter(Mandatory=$false)]
    [string]$SourceDisplayName = ""
)

$ErrorActionPreference = "Stop"

Write-Host "========================================================================"
Write-Host "SPECTRA Fabric Template - Project Setup"
Write-Host "========================================================================"
Write-Host ""
Write-Host "Project Name: $ProjectName"
Write-Host "Source System: $SourceSystem"
Write-Host ""

# Validate project name
if ($ProjectName -notmatch '^[a-z][a-z0-9]*$') {
    Write-Error "Project name must be lowercase alphanumeric, starting with a letter"
    exit 1
}

# Set defaults
if ([string]::IsNullOrWhiteSpace($SourceSystem)) {
    $SourceSystem = $ProjectName
}
if ([string]::IsNullOrWhiteSpace($SourceDisplayName)) {
    $SourceDisplayName = $ProjectName.Substring(0,1).ToUpper() + $ProjectName.Substring(1)
}

Write-Host "Replacing placeholders..."
Write-Host "  {PROJECT} → $ProjectName"
Write-Host "  {PROJECT_UPPER} → $($ProjectName.ToUpper())"
Write-Host "  {PROJECT_TITLE} → $($ProjectName.Substring(0,1).ToUpper() + $ProjectName.Substring(1))"
Write-Host ""

# Get all files (excluding .git, __pycache__, etc.)
$files = Get-ChildItem -Path . -Recurse -File | Where-Object {
    $_.FullName -notmatch '\.git|__pycache__|\.pyc|node_modules|\.DS_Store'
}

$replacements = 0

foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
        if ($null -eq $content) { continue }
        
        $originalContent = $content
        
        # Replace placeholders
        $content = $content -replace '\{PROJECT\}', $ProjectName
        $content = $content -replace '\{PROJECT_UPPER\}', $ProjectName.ToUpper()
        $content = $content -replace '\{PROJECT_TITLE\}', ($ProjectName.Substring(0,1).ToUpper() + $ProjectName.Substring(1))
        $content = $content -replace '\{SOURCE_SYSTEM\}', $SourceSystem
        $content = $content -replace '\{SOURCE_DISPLAY_NAME\}', $SourceDisplayName
        
        if ($content -ne $originalContent) {
            Set-Content -Path $file.FullName -Value $content -NoNewline -Encoding UTF8
            $replacements++
            Write-Host "  ✓ Updated: $($file.FullName.Replace($PWD.Path + '\', ''))"
        }
    }
    catch {
        Write-Warning "  ⚠ Could not process: $($file.FullName)"
    }
}

Write-Host ""
Write-Host "Renaming directories and files..."

# Rename directories
$dirsToRename = @(
    @{Old = "zephyr"; New = $ProjectName}
)

foreach ($dir in $dirsToRename) {
    if (Test-Path $dir.Old) {
        Rename-Item -Path $dir.Old -NewName $dir.New -ErrorAction SilentlyContinue
        Write-Host "  ✓ Renamed directory: $($dir.Old) → $($dir.New)"
    }
}

# Rename files with {PROJECT} in name
Get-ChildItem -Path . -Recurse -File | Where-Object {
    $_.Name -match '\{PROJECT\}'
} | ForEach-Object {
    $newName = $_.Name -replace '\{PROJECT\}', $ProjectName
    Rename-Item -Path $_.FullName -NewName $newName
    Write-Host "  ✓ Renamed file: $($_.Name) → $newName"
}

Write-Host ""
Write-Host "========================================================================"
Write-Host "Setup Complete!"
Write-Host "========================================================================"
Write-Host ""
Write-Host "✓ Replaced placeholders in $replacements files"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Review and update config/contracts/source.contract.yaml"
Write-Host "2. Create {PROJECT}Intelligence.Notebook with your source intelligence"
Write-Host "3. Configure Fabric workspace and Variable Library"
Write-Host "4. Test Source stage connectivity"
Write-Host ""
Write-Host "========================================================================"

