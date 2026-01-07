# Fabric Notebook Linting Strategy

**Date:** 2025-12-03  
**Issue:** Syntax errors in notebook not caught until Fabric runtime  
**Solution:** Pre-commit linting workflow

---

## The Problem

**What happened today:**
- Multiple syntax errors in notebook
- Not caught until running in Fabric
- Slow feedback loop (~2 min sync per fix)
- Frustrating debugging experience

**Root cause:** No linting before commit

---

## Recommended Linter: Ruff

**Why Ruff:**
- ✅ Already configured in `Core/fabric-sdk/pyproject.toml`
- ✅ Fast (written in Rust)
- ✅ Comprehensive (replaces 10+ tools)
- ✅ Python 3.11 compatible (Fabric runtime)
- ✅ SPECTRA standard

**Fabric doesn't officially recommend a specific linter**, but Ruff is industry standard for modern Python.

---

## Solution: Pre-Commit Linting

### Option 1: Manual Lint Before Commit

```bash
# From Data/zephyr directory
cd C:\Users\markm\OneDrive\SPECTRA\Data\zephyr

# Lint the notebook
ruff check sourceZephyr.Notebook/notebook_content.py

# If errors, fix them, then:
git add sourceZephyr.Notebook/notebook_content.py
git commit -m "fix: ..."
git push origin main
```

### Option 2: Pre-Commit Hook (Automatic)

**Create:** `.git/hooks/pre-commit`
```bash
#!/bin/sh
# Lint Fabric notebooks before commit

echo "🔍 Linting Fabric notebooks..."

ruff check sourceZephyr.Notebook/notebook_content.py

if [ $? -ne 0 ]; then
    echo "❌ Linting failed! Fix errors before committing."
    exit 1
fi

echo "✅ Linting passed!"
```

**Make executable:**
```bash
chmod +x .git/hooks/pre-commit
```

### Option 3: VS Code Extension

**Install:** Ruff extension for VS Code
- Auto-lints as you type
- Shows errors inline
- No commit needed to see issues

---

## Quick Fix: Validate Before Commit

**Add to your workflow:**

```bash
# Before committing notebook changes
python -m py_compile sourceZephyr.Notebook/notebook_content.py

# If no output → syntax is valid
# If error → fix before committing
```

**Even better with Ruff:**
```bash
ruff check sourceZephyr.Notebook/notebook_content.py --fix
# Auto-fixes many issues!
```

---

## Ruff Configuration for Notebooks

**Create:** `Data/zephyr/pyproject.toml`

```toml
[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # Pyflakes (catches undefined names!)
    "W",    # pycodestyle warnings
]

# Ignore notebook-specific issues
ignore = [
    "E402",  # Module import not at top (notebooks have cells)
    "F821",  # Undefined name (Spark objects injected by Fabric)
]

[tool.ruff.lint.per-file-ignores]
"*.Notebook/*.py" = [
    "E402",  # Imports not at top
    "F821",  # Undefined names (spark, notebookutils, etc.)
]
```

---

## Immediate Action

**Install Ruff (if not already):**
```bash
pip install ruff
```

**Lint the notebook:**
```bash
cd Data/zephyr
ruff check sourceZephyr.Notebook/notebook_content.py
```

**This would have caught:**
- ✅ Indentation errors
- ✅ Missing try blocks
- ✅ Undefined variables
- ✅ All syntax errors

---

## Long-term Solution

### 1. Add Ruff to Tooling
```bash
# Core/tooling/python-packages.json
{
  "linting": {
    "ruff": ">=0.5.0"
  }
}
```

### 2. Create Lint Script
**File:** `Data/zephyr/scripts/lint-notebook.ps1`
```powershell
#!/usr/bin/env pwsh
# Lint Fabric notebook before commit

Write-Host "`n🔍 Linting sourceZephyr notebook...`n" -ForegroundColor Cyan

# Syntax check
python -m py_compile sourceZephyr.Notebook/notebook_content.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Syntax errors found!`n" -ForegroundColor Red
    exit 1
}

# Ruff check
ruff check sourceZephyr.Notebook/notebook_content.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Linting errors found!`n" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Notebook is clean!`n" -ForegroundColor Green
```

### 3. Use Before Every Commit
```bash
.\scripts\lint-notebook.ps1
# If passes → commit
# If fails → fix then commit
```

---

## Recommended Workflow

**Before committing notebook changes:**

1. **Syntax check:**
   ```bash
   python -m py_compile sourceZephyr.Notebook/notebook_content.py
   ```

2. **Lint check:**
   ```bash
   ruff check sourceZephyr.Notebook/notebook_content.py
   ```

3. **If clean → commit:**
   ```bash
   git add sourceZephyr.Notebook/notebook_content.py
   git commit -m "..."
   git push origin main
   ```

**This prevents syntax errors reaching Fabric!**

---

## Should I Create?

1. **pyproject.toml** with Ruff config for notebooks
2. **lint-notebook.ps1** script
3. **Pre-commit hook** (optional)

**This would prevent today's frustration!** 🎯

