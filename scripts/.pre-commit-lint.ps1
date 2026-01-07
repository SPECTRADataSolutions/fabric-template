#!/usr/bin/env pwsh
# Pre-commit linting script for Zephyr Fabric notebook
# Usage: Run before every commit to catch syntax errors

Write-Host "`n🔍 Linting sourceZephyr notebook...`n" -ForegroundColor Cyan

# Step 1: Syntax check
Write-Host "Step 1: Syntax validation..." -ForegroundColor Yellow
python -m py_compile sourceZephyr.Notebook/notebook_content.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ SYNTAX ERRORS FOUND!`n" -ForegroundColor Red
    Write-Host "Fix syntax errors before committing.`n" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Syntax valid`n" -ForegroundColor Green

# Step 2: Ruff linting (optional - shows warnings but doesn't block)
Write-Host "Step 2: Ruff linting (warnings only)..." -ForegroundColor Yellow

# Check if ruff is installed
try {
    ruff --version | Out-Null
    
    # Run ruff check (non-blocking)
    ruff check sourceZephyr.Notebook/notebook_content.py --select F,E --ignore E402,F401
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n⚠️  Ruff found issues (non-blocking)`n" -ForegroundColor Yellow
    } else {
        Write-Host "  ✓ Ruff checks passed`n" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠️  Ruff not installed (skipping)`n" -ForegroundColor Yellow
    Write-Host "  Install: pip install ruff`n" -ForegroundColor Gray
}

# Success!
Write-Host "✅ NOTEBOOK IS CLEAN!`n" -ForegroundColor Green
Write-Host "Safe to commit.`n" -ForegroundColor White
exit 0

