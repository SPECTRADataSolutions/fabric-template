# Run Contract Validation - Quick Guide

**Purpose:** Query all Delta tables to see what's actually written and verify contract compliance

---

## 🚀 Quick Start

### Step 1: Sync Notebook to Fabric

The `contractValidation.Notebook` has been created. Sync it to Fabric:

1. **Push to Git:**
   ```bash
   cd Data/zephyr
   git add contractValidation.Notebook/
   git commit -m "feat: Add contract validation notebook"
   git push
   ```

2. **Sync in Fabric UI:**
   - Open Fabric workspace
   - Git sync will pull the new notebook
   - Or manually sync if needed

### Step 2: Run the Notebook

1. **Open Notebook in Fabric:**
   - Navigate to `contractValidation.Notebook` in your workspace
   - Click to open

2. **Run All Cells:**
   - Click "Run All" or run cells sequentially
   - The notebook will query all Delta tables

3. **View Results:**
   - Results printed to console
   - JSON output at the end for programmatic access

---

## 📊 What It Queries

The notebook checks:

1. **Core Tables:**
   - `source.portfolio` - Dashboard metadata
   - `source.config` - Runtime configuration
   - `source.credentials` - Masked credentials
   - `source.endpoints` - Endpoint catalog (228 endpoints)

2. **Preview Samples:**
   - `source.sampleProjects`
   - `source.sampleReleases`
   - `source.sampleCycles` ⚠️ (may be missing)
   - `source.sampleExecutions` ⚠️ (may be missing)
   - `source.sampleTestcases` ⚠️ (may be missing)

---

## 📋 Expected Output

The notebook will print:

```
================================================================================
📊 SOURCE STAGE CONTRACT VALIDATION
================================================================================
Contract: v3.0.0
Date: 2025-12-06T...

1️⃣  Checking source.portfolio...
   ✅ EXISTS: 1 row(s)
   📋 Sample: source_system=zephyr, total_endpoints=228

2️⃣  Checking source.config...
   ✅ EXISTS: 5 row(s)
   📋 Keys: base_url, api_token, ...

3️⃣  Checking source.credentials...
   ✅ EXISTS: 1 row(s)
   📋 Sample: type=apiToken, masked=***abc

4️⃣  Checking source.endpoints...
   ✅ EXISTS: 228 row(s)
   📊 Hierarchical: 25, Flat: 203
   📋 Top categories: {'testcases': 59, 'projects': 19, ...}

5️⃣  Checking preview sample tables...
   Checking source.sampleProjects...
      ✅ EXISTS: 10 row(s)
      📋 Sample ID: 45
   Checking source.sampleReleases...
      ✅ EXISTS: 10 row(s)
      📋 Sample ID: 123
   Checking source.sampleCycles...
      ❌ ERROR: Table or view not found: source.sampleCycles
   ...

================================================================================
📊 VALIDATION SUMMARY
================================================================================
Core Tables: ✅ ALL EXIST
  ✅ portfolio: 1 row(s)
  ✅ config: 5 row(s)
  ✅ credentials: 1 row(s)
  ✅ endpoints: 228 row(s)

Preview Samples: ⚠️  INCOMPLETE
  ✅ sampleProjects: 10 row(s)
  ✅ sampleReleases: 10 row(s)
  ❌ sampleCycles: Table or view not found: source.sampleCycles
  ❌ sampleExecutions: Table or view not found: source.sampleExecutions
  ❌ sampleTestcases: Table or view not found: source.sampleTestcases

❌ MISSING TABLES: sampleCycles, sampleExecutions, sampleTestcases
⚠️  EMPTY TABLES: (none)

================================================================================
```

---

## 🔍 What to Look For

### Contract Compliance Gaps:

1. **Missing Preview Samples:**
   - If `sampleCycles`, `sampleExecutions`, or `sampleTestcases` are missing
   - **Fix:** Complete preview extraction in `sourceZephyr.Notebook`

2. **Empty Tables:**
   - If any table exists but has 0 rows
   - **Fix:** Check extraction logic

3. **Schema Issues:**
   - If schema doesn't match expected structure
   - **Fix:** Review table creation logic

---

## 📤 Share Results

After running, you can:

1. **Copy the JSON output** from the notebook
2. **Share it with me** so I can see what's actually in the tables
3. **I'll analyze** and help debug any issues

---

## 🎯 Next Steps After Validation

Once we see the results:

1. **Identify gaps** - What tables are missing/empty?
2. **Fix extraction** - Complete preview samples
3. **Verify schemas** - Ensure all tables match contract
4. **Re-run validation** - Confirm compliance

---

**Version:** 1.0.0  
**Date:** 2025-12-06

