# Local testing script for Zephyr notebooks
# Loads environment variables and runs test script

param(
    [switch]$Help
)

if ($Help) {
    Write-Host @"
Zephyr Local Testing Script

Usage:
    .\scripts\test-local.ps1

Requirements:
    - .env file in Data/zephyr/ with:
      DXC_ZEPHYR_BASE_URL
      DXC_ZEPHYR_BASE_PATH
      DXC_ZEPHYR_API_TOKEN

    - Python with requests library installed
    - SPECTRA Fabric SDK installed (optional, for logging)

Examples:
    .\scripts\test-local.ps1
"@
    exit 0
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$envFile = Join-Path $repoRoot ".env"

# Load environment variables from .env file
if (Test-Path $envFile) {
    Write-Host "Loading environment variables from .env..." -ForegroundColor Cyan
    Get-Content $envFile | Where-Object { 
        $_ -notmatch '^[\s#]' -and $_ -match '=' 
    } | ForEach-Object { 
        $k, $v = $_ -split '=', 2
        Set-Item -Path ('Env:' + $k.Trim()) -Value $v.Trim()
        Write-Host "  Loaded: $($k.Trim())" -ForegroundColor Gray
    }
} else {
    Write-Host "Warning: .env file not found at $envFile" -ForegroundColor Yellow
    Write-Host "Using environment variables from system..." -ForegroundColor Yellow
}

# Check required variables
$required = @("DXC_ZEPHYR_BASE_URL", "DXC_ZEPHYR_BASE_PATH", "DXC_ZEPHYR_API_TOKEN")
$missing = @()
foreach ($var in $required) {
    if (-not (Get-Item "Env:$var" -ErrorAction SilentlyContinue)) {
        $missing += $var
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Error: Missing required environment variables:" -ForegroundColor Red
    foreach ($var in $missing) {
        Write-Host "  - $var" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Create .env file with these variables, or set them in your environment." -ForegroundColor Yellow
    exit 1
}

# Run test script
Write-Host ""
Write-Host "Zephyr Local Testing Options:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Quick API tests (no Spark):" -ForegroundColor Yellow
Write-Host "   python scripts/test_source_local.py" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Full Source notebook (local Spark + Fabric mock):" -ForegroundColor Yellow
Write-Host "   python scripts/run_source_local.py [--init-mode] [--debug]" -ForegroundColor Gray
Write-Host ""
Write-Host "3. All endpoints test:" -ForegroundColor Yellow
Write-Host "   python scripts/test_all_endpoints.py --category all" -ForegroundColor Gray
Write-Host ""

# Default to full Source notebook runner
$runnerScript = Join-Path $scriptDir "run_source_local.py"
if (-not (Test-Path $runnerScript)) {
    Write-Host "Error: Runner script not found at $runnerScript" -ForegroundColor Red
    exit 1
}

Write-Host "Running Source notebook locally (with Spark + Fabric mock)..." -ForegroundColor Cyan
Write-Host ""

python $runnerScript --init-mode

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Tests failed. Check output above for details." -ForegroundColor Red
    exit $LASTEXITCODE
}

