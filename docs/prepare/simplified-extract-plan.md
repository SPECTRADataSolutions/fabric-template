# Simplified Zephyr Extract Plan

## Current State

**Prepare Stage Status:** Needs rollback to simple approach  
**Goal:** Extract data samples for endpoints WITHOUT dependencies first, save to lakehouse

---

## Endpoint Dependency Analysis

Based on `intelligence/dependencies.yaml` and `intelligence/creation-order.yaml`:

### Level 0: Independent Endpoints (No Dependencies)
These can be extracted immediately without any prerequisites:

1. **project** → GET `/project` or `/project/details`
2. **release** → GET `/release` (all releases) or `/release/project/{projectId}`
3. **requirement_folder** → GET `/requirementtree/project/{projectId}`

### Level 1: First-Level Dependencies
These need Level 0 entities to exist:

4. **testcase_folder** → GET `/testcasetree/projectrepository/{projectId}` (needs: project)
5. **cycle** → GET `/cycle/release/{releaseId}` (needs: release)
6. **requirement** → GET `/requirementtree/{folderId}` or `/requirementtree/project/{projectId}` (needs: requirement_folder)

### Level 2: Second-Level Dependencies

7. **testcase** → GET `/testcase/project/{projectId}` or `/testcase/{id}` (needs: testcase_folder)

### Level 3: Leaf Dependencies

8. **allocation** → GET `/allocation/project/{projectId}` (needs: testcase)
9. **execution** → GET `/execution` or `/execution/project/{projectId}` (needs: testcase + cycle)

---

## Simplified Approach

### Phase 1: Extract Independent Endpoints (Start Here)

**Goal:** Extract samples from the 3 independent endpoints, save to lakehouse tables.

**Endpoints to extract:**
1. `/project` or `/project/details` → `extract.projects`
2. `/release` → `extract.releases` 
3. `/requirementtree/project/{projectId}` → `extract.requirement_folders`

**Approach:**
- Simple notebook that:
  1. Calls each endpoint
  2. Converts JSON response to Spark DataFrame
  3. Writes to Delta table in lakehouse (e.g., `extract.projects_sample`, `extract.releases_sample`, etc.)
  4. Shows sample data and schema

**Notebook:** `extractZephyrSample.Notebook`

### Phase 2: Extract Level 1 (After Phase 1 works)

Once Phase 1 tables exist, extract Level 1:
- Use project IDs from `extract.projects` to get testcase folders
- Use release IDs from `extract.releases` to get cycles
- Use project IDs from `extract.projects` to get requirements

### Phase 3: Continue Up the Hierarchy

Continue with Level 2 and Level 3 endpoints using IDs from previous levels.

---

## Endpoint Mapping Reference

| Entity | GET Endpoint | Dependencies | Notes |
|--------|--------------|--------------|-------|
| project | `/project` or `/project/details` | None | Returns all projects |
| release | `/release` or `/release/project/{projectId}` | None | Can get all or filtered by project |
| requirement_folder | `/requirementtree/project/{projectId}` | None | Gets folder tree for project |
| testcase_folder | `/testcasetree/projectrepository/{projectId}` | project | Gets testcase folder tree |
| cycle | `/cycle/release/{releaseId}` | release | Gets cycles for a release |
| requirement | `/requirementtree/project/{projectId}` or `/requirementtree/{folderId}` | requirement_folder | Gets requirements in tree |
| testcase | `/testcase/project/{projectId}` | testcase_folder | Gets testcases for project |
| allocation | `/allocation/project/{projectId}` | testcase | Gets allocations for project |
| execution | `/execution` or `/execution/project/{projectId}` | testcase + cycle | Gets executions |

---

## Perfect Extraction Order (Topological Sort)

Based on dependencies, extract in this order:

1. **project** (independent)
2. **release** (independent)
3. **requirement_folder** (independent)
4. **testcase_folder** (needs project)
5. **cycle** (needs release)
6. **requirement** (needs requirement_folder)
7. **testcase** (needs testcase_folder)
8. **allocation** (needs testcase)
9. **execution** (needs testcase + cycle)

---

## Next Steps

1. **Roll back current prepare stage** - Remove complex schema generation
2. **Create simple extract notebook** - Just hit the 3 independent endpoints
3. **Save to lakehouse** - Create Delta tables with sample data
4. **Review results** - Check table schemas and data quality
5. **Expand gradually** - Add Level 1, then Level 2, etc.

---

## Reference Files

- `intelligence/dependencies.yaml` - Dependency graph
- `intelligence/creation-order.yaml` - Perfect order (topological sort)
- `source/source.plan.yaml` - Source stage plan with endpoints
- `intelligence/endpoints.yaml` - Full endpoint catalog

