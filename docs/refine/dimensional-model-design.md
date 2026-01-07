# Zephyr Dimensional Model Design

**Status:** 🟡 In Progress  
**Version:** 1.0.0  
**Date:** 2025-12-06  
**Objective:** Design dimensional model (star schema) for Zephyr test management analytics

---

## 🎯 Purpose

The Refine stage transforms normalized data into a dimensional model optimized for analytics and reporting. This document defines:

- **Fact Tables:** Business activities/events (what happened)
- **Dimension Tables:** Descriptive entities (who, what, when, where)
- **Bridge Tables:** Many-to-many relationships

**Principle:** Fact tables represent **business activities** (test executions, requirement allocations), while dimensions provide **context** (projects, releases, cycles, testcases).

---

## 📊 Business Activities Analysis

### Core Business Activities

**1. Test Execution (Primary Activity)**

- **Event:** Testcase executed in a cycle
- **Granularity:** One execution per testcase-cycle assignment
- **Measures:** Status (Pass/Fail/Blocked), duration, execution date
- **Dimensions:** Project, Release, Cycle, Testcase, Tester, Execution Date

**2. Requirement Coverage**

- **Event:** Testcase allocated to requirement
- **Granularity:** One allocation per testcase-requirement pair
- **Measures:** Coverage status, allocation date
- **Dimensions:** Project, Requirement, Testcase

**3. Test Cycle Progression**

- **Event:** Cycle status changes
- **Granularity:** One record per cycle-status transition
- **Measures:** Status, transition date, duration in status
- **Dimensions:** Project, Release, Cycle, Cycle Status

**4. Testcase Lifecycle**

- **Event:** Testcase created/modified/assigned
- **Granularity:** One record per testcase-state change
- **Measures:** Change type, change date, previous/new values
- **Dimensions:** Project, Testcase, Folder, Change Type

---

## 🏗️ Fact Tables

### `factExecution`

**Purpose:** Test execution results - the core fact table

**Business Activity:** Testcase executed in a test cycle

**Grain:** One row per testcase-cycle execution

**Measures:**

- `execution_id` (PK): Unique execution identifier
- `execution_status_id`: Status ID (1=Passed, 2=Failed, 3=Blocked, 4=Not Executed)
- `execution_status`: Status name (for convenience)
- `execution_date`: Date/time execution occurred
- `duration_seconds`: Execution duration (if available)
- `execution_order`: Order within cycle
- `comment`: Execution comments/notes

**Dimensions (Foreign Keys):**

- `project_id` → `dimProject.project_id`
- `release_id` → `dimRelease.release_id`
- `cycle_id` → `dimCycle.cycle_id`
- `testcase_id` → `dimTestcase.testcase_id`
- `tester_id` → `dimTester.tester_id`
- `execution_date_id` → `dimDate.date_id` (date dimension)

**Degenerate Dimensions:**

- `execution_comment`: Text comment (stored in fact, not dimension)

**Surrogate Keys:**

- `execution_key` (PK, surrogate): Auto-incrementing key
- All dimension FKs are natural keys (project_id, cycle_id, etc.)

**Example Query:**

```sql
-- Test execution rate by project and cycle
SELECT
    p.project_name,
    c.cycle_name,
    COUNT(*) as total_executions,
    SUM(CASE WHEN f.execution_status_id = 1 THEN 1 ELSE 0 END) as passed,
    SUM(CASE WHEN f.execution_status_id = 2 THEN 1 ELSE 0 END) as failed
FROM factExecution f
JOIN dimProject p ON f.project_id = p.project_id
JOIN dimCycle c ON f.cycle_id = c.cycle_id
GROUP BY p.project_name, c.cycle_name
```

---

### `factRequirementCoverage` (Future)

**Purpose:** Requirement-testcase allocation tracking

**Business Activity:** Testcase allocated to requirement

**Grain:** One row per testcase-requirement allocation

**Measures:**

- `allocation_id`: Unique allocation identifier
- `allocation_date`: Date allocation created
- `coverage_status`: Covered/Not Covered/Partial

**Dimensions:**

- `project_id` → `dimProject.project_id`
- `requirement_id` → `dimRequirement.requirement_id`
- `testcase_id` → `dimTestcase.testcase_id`
- `allocation_date_id` → `dimDate.date_id`

**Note:** This fact table may be replaced by bridge table `bridgeTestcaseRequirement` if no measures are needed.

---

### `factCycleStatusHistory` (Future)

**Purpose:** Cycle status transition tracking

**Business Activity:** Cycle status changes

**Grain:** One row per cycle-status transition

**Measures:**

- `transition_id`: Unique transition identifier
- `from_status_id`: Previous status
- `to_status_id`: New status
- `transition_date`: Date transition occurred
- `duration_in_status_days`: Days in previous status

**Dimensions:**

- `cycle_id` → `dimCycle.cycle_id`
- `transition_date_id` → `dimDate.date_id`

**Note:** Requires changelog or audit trail. May not be available in initial implementation.

---

## 📐 Dimension Tables

### `dimProject`

**Purpose:** Project dimension

**Natural Key:** `project_id`

**Attributes:**

- `project_id` (PK): Zephyr project ID
- `project_name`: Project name
- `project_key`: Project key (if available)
- `project_type`: Type/category
- `created_date`: Project creation date
- `is_active`: Active status flag
- `description`: Project description

**Slowly Changing:** Type 2 (historical tracking if needed)

---

### `dimRelease`

**Purpose:** Release dimension

**Natural Key:** `release_id`

**Attributes:**

- `release_id` (PK): Zephyr release ID
- `release_name`: Release name
- `project_id` (FK): → `dimProject.project_id`
- `start_date`: Release start date
- `end_date`: Release end date
- `status`: Release status (Active, Closed, etc.)
- `is_global`: Global release flag
- `created_date`: Release creation date

**Hierarchy:** Project → Release

---

### `dimCycle`

**Purpose:** Test cycle dimension

**Natural Key:** `cycle_id`

**Attributes:**

- `cycle_id` (PK): Zephyr cycle ID
- `cycle_name`: Cycle name
- `release_id` (FK): → `dimRelease.release_id`
- `start_date`: Cycle start date
- `end_date`: Cycle end date
- `status`: Cycle status
- `environment`: Environment name
- `build`: Build version
- `created_date`: Cycle creation date

**Hierarchy:** Project → Release → Cycle

---

### `dimTestcase`

**Purpose:** Testcase dimension

**Natural Key:** `testcase_id`

**Attributes:**

- `testcase_id` (PK): Zephyr testcase ID
- `testcase_name`: Testcase name
- `project_id` (FK): → `dimProject.project_id`
- `folder_id` (FK): → `dimFolder.folder_id`
- `testcase_type`: Type/category
- `priority`: Priority level
- `created_date`: Testcase creation date
- `last_modified_date`: Last modification date
- `description`: Testcase description

**Hierarchy:** Project → Folder → Testcase

---

### `dimTester`

**Purpose:** Tester/user dimension

**Natural Key:** `tester_id` (user ID)

**Attributes:**

- `tester_id` (PK): Zephyr user ID
- `tester_name`: User name
- `tester_email`: User email
- `is_active`: Active status flag
- `role`: User role

**Note:** May be sourced from Zephyr users endpoint or execution data.

---

### `dimRequirement`

**Purpose:** Requirement dimension

**Natural Key:** `requirement_id`

**Attributes:**

- `requirement_id` (PK): Zephyr requirement ID
- `requirement_name`: Requirement name
- `project_id` (FK): → `dimProject.project_id`
- `requirement_type`: Type/category
- `priority`: Priority level
- `created_date`: Requirement creation date

---

### `dimFolder`

**Purpose:** Test Repository folder dimension

**Natural Key:** `folder_id` (tcrCatalogTreeId)

**Attributes:**

- `folder_id` (PK): Folder tree node ID
- `folder_name`: Folder name
- `project_id` (FK): → `dimProject.project_id`
- `parent_folder_id` (FK): → `dimFolder.folder_id` (self-referencing)
- `folder_path`: Full folder path (for easy querying)
- `folder_level`: Depth in tree

**Hierarchy:** Project → Folder → ... → Folder (tree structure)

---

### `dimDate`

**Purpose:** Date dimension (standard star schema pattern)

**Natural Key:** `date_id` (YYYYMMDD format)

**Attributes:**

- `date_id` (PK): Date ID (YYYYMMDD)
- `date`: Actual date
- `year`: Year
- `quarter`: Quarter (1-4)
- `month`: Month (1-12)
- `month_name`: Month name
- `week`: Week number
- `day_of_week`: Day of week (1-7)
- `day_name`: Day name
- `is_weekend`: Weekend flag
- `is_holiday`: Holiday flag (if available)

**Note:** Standard dimension table for time-based analysis.

---

### `dimExecutionStatus`

**Purpose:** Execution status dimension

**Natural Key:** `status_id`

**Attributes:**

- `status_id` (PK): Status ID (1, 2, 3, 4)
- `status_name`: Status name (Passed, Failed, Blocked, Not Executed)
- `status_category`: Category (Success, Failure, Blocked, Pending)
- `sort_order`: Display order

---

## 🔗 Bridge Tables

### `bridgeTestcaseRequirement`

**Purpose:** Many-to-many relationship between testcases and requirements

**Natural Keys:** `testcase_id`, `requirement_id`

**Attributes:**

- `testcase_id` (FK): → `dimTestcase.testcase_id`
- `requirement_id` (FK): → `dimRequirement.requirement_id`
- `allocation_date`: Date allocation created
- `is_active`: Active allocation flag

**Use Case:** Traceability matrix - which testcases cover which requirements

---

### `bridgeTestcaseCycle`

**Purpose:** Many-to-many relationship between testcases and cycles

**Natural Keys:** `testcase_id`, `cycle_id`

**Attributes:**

- `testcase_id` (FK): → `dimTestcase.testcase_id`
- `cycle_id` (FK): → `dimCycle.cycle_id`
- `assignment_date`: Date testcase assigned to cycle
- `is_active`: Active assignment flag

**Note:** This relationship is implicit in `factExecution`, but bridge table provides explicit assignment tracking.

---

## 📊 Fact Table Summary

| Fact Table                | Business Activity      | Grain                            | Primary Measures                  |
| ------------------------- | ---------------------- | -------------------------------- | --------------------------------- |
| `factExecution`           | Test execution         | One per testcase-cycle execution | Status, duration, execution date  |
| `factRequirementCoverage` | Requirement allocation | One per testcase-requirement     | Coverage status, allocation date  |
| `factCycleStatusHistory`  | Cycle status change    | One per status transition        | Status, transition date, duration |

**MVP Focus:** `factExecution` is the primary fact table for MVP. Other fact tables are future enhancements.

---

## 🎯 Dimensional Model Principles Applied

1. **Grain Clarity:** Each fact table has explicit grain (one row = one business event)
2. **Natural Keys:** Dimensions use natural keys (project_id) with surrogate keys only where needed
3. **Conformed Dimensions:** Shared dimensions (dimProject, dimDate) across all facts
4. **Degenerate Dimensions:** Text fields stored in fact when not needed in dimension
5. **Bridge Tables:** Many-to-many relationships via bridge tables
6. **Slowly Changing:** Type 2 SCD for historical tracking (if needed)

---

## 🚀 Implementation Roadmap

### Phase 1: MVP (Current Focus)

**Fact Tables:**

- ✅ `factExecution` (primary)

**Dimensions:**

- ✅ `dimProject`
- ✅ `dimRelease`
- ✅ `dimCycle`
- ✅ `dimTestcase`
- ✅ `dimTester` (if available)
- ✅ `dimExecutionStatus`
- ✅ `dimDate`

**Bridge Tables:**

- ⏳ `bridgeTestcaseRequirement` (if requirement allocation data available)

### Phase 2: Enhanced Analytics

**Additional Fact Tables:**

- `factRequirementCoverage`
- `factCycleStatusHistory`

**Additional Dimensions:**

- `dimFolder` (Test Repository structure)

**Additional Bridge Tables:**

- `bridgeTestcaseCycle` (explicit assignments)

---

## 📊 Visual Resources

- **Model Diagram:** `Data/zephyr/docs/refine/DIMENSIONAL-MODEL-DIAGRAM.md` — Power BI-style visual representation with Mermaid diagram
- **Enrichment Items:** `Data/zephyr/docs/refine/DIMENSIONAL-MODEL-ENRICHMENT.md` — Comprehensive enrichment fields for each table

---

## 📚 References

- **Zephyr Research:** `Data/zephyr/docs/ZEPHYR-RESEARCH-SUMMARY.md`
- **Prepare Schema:** `Data/zephyr/docs/prepare/PREPARE-STAGE-SCHEMA-DESIGN.md`
- **Jira Pattern:** `Data/jira/docs/methodology/6-refine/refine.md` (if exists)
