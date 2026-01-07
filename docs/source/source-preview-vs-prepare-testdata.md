# Source Preview Samples vs Prepare Test Data

> **Date:** 2025-12-08  
> **Purpose:** Clarify the distinction between Source preview samples and Prepare test data creation

---

## The Confusion

**Question:** "Samples are taken in Prepare, right? So why does Source have `source.sampleProjects` and `source.sampleReleases`?"

**Answer:** They serve **different purposes** and are **different types of samples**.

---

## Two Different Types of "Samples"

### 1. **Source Preview Samples** (Optional, Quick Validation)

**Tables:** `source.sampleProjects`, `source.sampleReleases`

**Purpose:** Quick connectivity and API validation

**What they do:**
- ✅ Read **existing data** from the API (doesn't create anything)
- ✅ Extract small samples (default: 10 records) from existing entities
- ✅ Validate API connectivity and response structure
- ✅ Quick sanity check that authentication works

**When used:**
- First-time setup (validate API access)
- Troubleshooting connectivity issues
- Quick validation before full pipeline runs

**Example:**
```python
# Source notebook
preview: bool = True  # Extract 10 existing projects, 10 existing releases
```

**What happens:**
1. Calls `GET /project/details` → Gets first 10 projects
2. Calls `GET /release/project/{projectId}` → Gets first 10 releases
3. Stores in `source.sampleProjects` and `source.sampleReleases`
4. **No data is created** - just reads what already exists

---

### 2. **Prepare Test Data** (Required, Schema Discovery)

**Playbook:** `prepare.001-createTestData.md`

**Purpose:** Create comprehensive test data for schema introspection

**What they do:**
- ✅ **Creates new entities** in Zephyr's `SpectraTestProject`
- ✅ Creates releases, cycles, folders, testcases, executions
- ✅ Populates all fields with comprehensive test data
- ✅ Captures full API responses for schema discovery
- ✅ Used by `prepare.002` to introspect schemas

**When used:**
- Schema discovery (one-time or when schemas change)
- Building `prepare_schema_generated.json`
- Ensuring "perfectly enriched" test data for accurate schemas

**Example:**
```python
# prepare.001 script
python scripts/build_comprehensive_spectra_test_project.py
# Creates new Star Wars-themed test data in SpectraTestProject
```

**What happens:**
1. Creates new release: "The Death Star Project - Phase 1"
2. Creates new cycles, testcases, executions
3. Captures full API responses (all fields, all metadata)
4. Stores responses in `docs/schemas/discovered/comprehensive/`
5. **Data is created** - new entities in the source system

---

## Key Differences

| Aspect | Source Preview Samples | Prepare Test Data |
|--------|----------------------|-------------------|
| **Action** | Read existing data | Create new data |
| **Size** | Small (10 records) | Comprehensive (full test dataset) |
| **Purpose** | Quick validation | Schema discovery |
| **Location** | `source.sampleProjects`, `source.sampleReleases` | `SpectraTestProject` in Zephyr |
| **When** | Optional (preview=True) | Required for schema introspection |
| **Stage** | Source | Prepare |
| **Creates entities?** | ❌ No | ✅ Yes |

---

## Why Source Has Preview Samples

**Source preview samples are for:**
1. **Quick validation** - "Can I connect to the API?"
2. **Troubleshooting** - "Is authentication working?"
3. **Initial setup** - "Do I have access to projects/releases?"

**They're NOT for:**
- ❌ Schema discovery (that's Prepare's job)
- ❌ Comprehensive test data (that's Prepare's job)
- ❌ Production data extraction (that's Extract stage's job)

---

## Why Prepare Creates Test Data

**Prepare test data is for:**
1. **Schema introspection** - "What fields does the API return?"
2. **Field metadata discovery** - "What are the enum values? Validation rules?"
3. **Accurate schema generation** - "Generate `prepare_schema_generated.json` from real responses"

**It's required because:**
- ✅ You can't introspect schemas without data
- ✅ Existing production data may not have all fields populated
- ✅ Need comprehensive, "perfectly enriched" data to discover all possible fields

---

## The Flow

### Source Stage (Optional Preview)
```
Source notebook (preview=True)
  ↓
Read 10 existing projects from API
  ↓
Store in source.sampleProjects
  ↓
Purpose: Quick validation ✅
```

### Prepare Stage (Required Test Data)
```
prepare.001-createTestData
  ↓
Create comprehensive test data in SpectraTestProject
  ↓
Capture full API responses
  ↓
prepare.002-introspectSchemas
  ↓
Generate prepare_schema_generated.json
  ↓
Purpose: Schema discovery ✅
```

---

## Are Source Preview Samples Redundant?

**Short answer:** Possibly, but they serve a different purpose.

**Arguments for keeping them:**
- ✅ Quick validation without creating data
- ✅ Useful for troubleshooting
- ✅ Lightweight (just reads existing data)
- ✅ Doesn't require write permissions

**Arguments for removing them:**
- ⚠️ Prepare creates comprehensive test data anyway
- ⚠️ May be confusing (as you've identified)
- ⚠️ Not used by downstream stages
- ⚠️ Adds complexity

**Recommendation:**
- Keep for now (useful for quick validation)
- But clarify in documentation that they're **not** for schema discovery
- Consider deprecating if Prepare test data covers all use cases

---

## Current Status

**Source preview samples:**
- ✅ Implemented in SDK
- ✅ Optional (preview=True)
- ⚠️ Not currently used by downstream stages
- ⚠️ May be redundant with Prepare test data

**Prepare test data:**
- ✅ Implemented in `prepare.001`
- ✅ Required for schema discovery
- ✅ Creates comprehensive test data
- ✅ Used by `prepare.002` for schema introspection

---

## Summary

**Source preview samples** = Quick read of existing data (optional validation)  
**Prepare test data** = Create new comprehensive data (required for schema discovery)

They're **different things** serving **different purposes**, but the naming is confusing. Source preview samples are lightweight validation, while Prepare test data is comprehensive schema discovery.

**Your observation is correct:** The real "samples" for schema discovery happen in Prepare, not Source.

---

**Last Updated:** 2025-12-08

