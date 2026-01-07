# Preview Samples vs SpectraTestProject - Clarification

**Date:** 2025-12-08  
**Question:** Should source stage deal with preview samples, or use SpectraTestProject instead?

---

## 🔍 What We Did Last Week

### SpectraTestProject Creation (Synthetic Data)

**What we built:**
- **Project ID 45** locked as `SpectraTestProject` in Variable Library
- Created synthetic test project via POST/PUT API endpoints
- Purpose: Deterministic test fixture, schema discovery, integration testing
- Location: `scripts/discover_schemas_via_creation.py`
- Documentation: `docs/SPECTRA-TEST-PROJECT-DESIGN.md`

**Key Points:**
- ✅ Synthetic data we **create** (via API)
- ✅ Perfect, deterministic structure
- ✅ Used for schema discovery via creation
- ✅ Locked project ID 45 (environment-specific)

---

## 🤔 Current Confusion

### Preview Samples (Current Implementation)

**What source stage does:**
- Extracts **real production data** from Zephyr API
- Only when `preview=True` parameter
- Purpose: "Preview samples for Prepare stage schema design"
- Creates: `source.sampleProjects`, `source.sampleReleases`, etc.

**The Question:**
- Should source stage extract **real** production data as samples?
- OR should it use **SpectraTestProject** (synthetic, deterministic)?

---

## 🎯 Two Different Purposes

### Option A: Preview Samples = Real Production Data

**Pros:**
- ✅ Real-world examples
- ✅ Actual data structures in production
- ✅ See real edge cases

**Cons:**
- ❌ Production data might be messy/incomplete
- ❌ Different structure each time
- ❌ Might not have all hierarchy levels
- ❌ Privacy/security concerns?

### Option B: Preview Samples = SpectraTestProject Data

**Pros:**
- ✅ Deterministic, perfect structure
- ✅ Always has all hierarchy levels
- ✅ Known good state
- ✅ No production data exposure
- ✅ Faster (already created)

**Cons:**
- ⚠️ Synthetic data (might not match production exactly)
- ⚠️ Need to ensure SpectraTestProject is populated

---

## 💡 My Recommendation

### Use SpectraTestProject for Preview Samples

**Rationale:**
1. **You already have it** - Project ID 45 is locked and created
2. **Perfect structure** - Always has all hierarchy levels
3. **Deterministic** - Same data every time
4. **Purpose aligned** - "For Prepare stage schema design" → need perfect examples
5. **No production concerns** - Synthetic data, no privacy issues

**Implementation:**
```python
# In sourceZephyr.Notebook, replace preview extraction:
if session.params["preview"]:
    test_project_id = session.variables.get("TEST_PROJECT_ID")  # 45
    
    resources = [
        {"name": "projects", "endpoint": f"/project/{test_project_id}", "table": "source.sampleProjects"},
        {"name": "releases", "endpoint": f"/release/project/{test_project_id}", "table": "source.sampleReleases"},
        {"name": "cycles", "endpoint": f"/cycle/release/{release_id}", "table": "source.sampleCycles"},
        {"name": "executions", "endpoint": f"/execution/cycle/{cycle_id}", "table": "source.sampleExecutions"},
        {"name": "testcases", "endpoint": f"/testcase/project/{test_project_id}", "table": "source.sampleTestcases"}
    ]
    
    # Extract from SpectraTestProject (ID 45)
    table_count = SourceStageHelpers.extract_preview_sample(...)
```

---

## 🔍 Check: Does SpectraTestProject Exist?

**From Variable Library:**
- `TEST_PROJECT_ID = 45` (locked)
- Should be `SpectraTestProject`

**From your execution log:**
- First project ID discovered: `44`
- So project 45 exists and should be `SpectraTestProject`

---

## 📋 Decision Needed

**Should preview samples:**

**A) Extract from SpectraTestProject (ID 45)?**
- ✅ Deterministic
- ✅ Perfect structure
- ✅ All hierarchy levels guaranteed

**B) Extract from first available project (current)?**
- Real production data
- Might be incomplete
- Different each time

**C) Extract from both?**
- SpectraTestProject as primary
- Real project as backup
- Compare structure

---

## 🎯 Next Steps

1. **Verify SpectraTestProject exists:**
   - Check project ID 45 in Zephyr
   - Confirm it's populated with releases/cycles/executions/testcases

2. **If exists → Use for preview samples:**
   - Update `sourceZephyr.Notebook` to extract from project 45
   - All 5 hierarchy levels guaranteed

3. **If doesn't exist → Create it:**
   - Use `scripts/discover_schemas_via_creation.py`
   - Or create via `createSpectraTestProject.Notebook` (if we built it)

---

**My recommendation: Use SpectraTestProject (ID 45) for preview samples. It's what we built for exactly this purpose - deterministic, perfect structure for schema design.**

**What do you think?**

