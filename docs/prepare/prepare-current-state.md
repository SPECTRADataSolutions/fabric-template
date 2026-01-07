# Prepare Stage - Current State Analysis

## What Prepare Currently Does

Based on `temp-prepareZephyr-content.py` (488 lines), the prepare stage:

### Purpose
Creates **metadata configuration tables** that drive downstream stages (Extract, Clean, Transform, Refine).

### Current Workflow

#### 1. **Loads Intelligence Artifacts**
- Reads `intelligence/schemas/*.json` - Auto-generated entity schemas
- Reads `intelligence/dependencies.yaml` - Entity dependency relationships
- Reads `intelligence/quirks.yaml` - API constraints, blockers, bugs, workarounds

#### 2. **Creates 3 Delta Tables**

**`prepare._schema`**
- Field-level metadata for all Zephyr entities
- Columns: `entity`, `fieldName`, `fieldType`, `isRequired`, `description`, `sourceEndpoint`, `intelligenceStatus`
- Purpose: Tells Extract stage what fields to extract and their types

**`prepare._dependencies`**
- Entity dependency relationships
- Columns: `entity`, `dependsOn`, `requiredBy`, `dependencyCount`, `dependentCount`, `isIndependent`, `isLeaf`
- Purpose: Tells Transform stage entity relationships

**`prepare._constraints`**
- API limitations, blockers, bugs, workarounds
- Columns: `constraintId`, `constraintType`, `entity`, `endpoint`, `severity`, `issue`, `impact`, `workaround`, `workaroundStatus`
- Purpose: Tells Extract stage what endpoints have issues and how to work around them

#### 3. **Validation**
- Validates row counts
- Validates required columns exist
- Uses SDK session validation

---

## Complexity Assessment

**Current Approach:**
- ✅ Uses intelligence artifacts (good - leverages existing work)
- ❌ Creates complex metadata tables (overkill for MVP)
- ❌ No actual data extraction (schema-only)
- ❌ Heavy dependency on intelligence artifacts

**Lines of Code:** ~488 lines

---

## Proposed Simplified Approach

**Instead of:** Creating complex metadata tables

**Do this:** Extract actual data samples from endpoints and save to lakehouse

### Simplified Workflow

1. **Call API Endpoints**
   - `/project/details` → Extract projects data
   - `/release` → Extract releases data
   - `/requirementtree/project/{id}` → Extract requirement folders (once endpoint is fixed)

2. **Save to Delta Tables**
   - `prepare.projects_sample` - Actual project data
   - `prepare.releases_sample` - Actual release data
   - `prepare.requirement_folders_sample` - Actual requirement folder data

3. **Benefits**
   - ✅ Much simpler (~100 lines vs 488 lines)
   - ✅ Actual data in lakehouse (can inspect, query)
   - ✅ Schema discovery from real data (infer from DataFrame)
   - ✅ No dependency on complex intelligence artifacts
   - ✅ Aligns with user's goal: "start small with prepare taking the first endpoint and attempting to get samples in the lakehouse"

---

## Recommendation

**Simplify prepare to:**
1. Extract data from independent endpoints (projects, releases)
2. Save as Delta tables (e.g., `prepare.projects_sample`)
3. Let Spark infer schema from actual data
4. Review results before building complex metadata

This is exactly what we built in `extractZephyrSample.Notebook` - but we can adapt prepare to do this instead!

---

## Next Steps

1. **Move extraction logic to prepare** - Replace complex metadata generation with simple data extraction
2. **Use the local test script as template** - We already have working extraction code
3. **Start with 2-3 endpoints** - Projects and releases (independent, no dependencies)
4. **Gradually expand** - Add more endpoints as needed

---

## Files to Update

- `2-prepare/prepareZephyr.Notebook/notebook_content.py` - Replace with simplified extraction logic
- Or use `temp-prepareZephyr-content.py` as reference for structure, but replace intelligence loading with API calls

