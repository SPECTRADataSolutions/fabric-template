# Zephyr Dimensional Model - Visual Diagram

**Status:** 🟢 Complete  
**Version:** 1.0.0  
**Date:** 2025-12-06  
**Objective:** Power BI-style visual representation of Zephyr dimensional model with relationships

---

## 📊 Model View Diagram

This diagram represents the dimensional model in a Power BI-style format, showing all fact tables, dimensions, and relationships.

```mermaid
erDiagram
    %% Fact Tables (Centre)
    factExecution ||--o{ dimProject : "references"
    factExecution ||--o{ dimRelease : "references"
    factExecution ||--o{ dimCycle : "references"
    factExecution ||--o{ dimTestcase : "references"
    factExecution ||--o{ dimTester : "references"
    factExecution ||--o{ dimDate : "references"
    factExecution ||--o{ dimExecutionStatus : "references"

    factRequirementCoverage ||--o{ dimProject : "references"
    factRequirementCoverage ||--o{ dimRequirement : "references"
    factRequirementCoverage ||--o{ dimTestcase : "references"
    factRequirementCoverage ||--o{ dimDate : "references"

    factCycleStatusHistory ||--o{ dimCycle : "references"
    factCycleStatusHistory ||--o{ dimDate : "references"

    %% Dimensions (Surrounding Facts)
    dimProject ||--o{ dimRelease : "contains"
    dimRelease ||--o{ dimCycle : "contains"
    dimProject ||--o{ dimTestcase : "contains"
    dimProject ||--o{ dimRequirement : "contains"
    dimProject ||--o{ dimFolder : "contains"
    dimFolder ||--o{ dimFolder : "parent"
    dimFolder ||--o{ dimTestcase : "contains"

    %% Bridge Tables
    bridgeTestcaseRequirement }o--|| dimTestcase : "links"
    bridgeTestcaseRequirement }o--|| dimRequirement : "links"
    bridgeTestcaseCycle }o--|| dimTestcase : "links"
    bridgeTestcaseCycle }o--|| dimCycle : "links"

    %% Fact Tables
    factExecution {
        bigint execution_key PK
        bigint execution_id
        int project_id FK
        int release_id FK
        int cycle_id FK
        bigint testcase_id FK
        int tester_id FK
        int execution_date_id FK
        int execution_status_id FK
        string execution_status
        datetime execution_date
        int duration_seconds
        int execution_order
        string comment
    }

    factRequirementCoverage {
        bigint allocation_id PK
        int project_id FK
        bigint requirement_id FK
        bigint testcase_id FK
        int allocation_date_id FK
        datetime allocation_date
        string coverage_status
    }

    factCycleStatusHistory {
        bigint transition_id PK
        int cycle_id FK
        int transition_date_id FK
        int from_status_id
        int to_status_id
        datetime transition_date
        int duration_in_status_days
    }

    %% Dimensions
    dimProject {
        int project_id PK
        string project_name
        string project_key
        string project_type
        date created_date
        boolean is_active
        string description
    }

    dimRelease {
        int release_id PK
        int project_id FK
        string release_name
        date start_date
        date end_date
        string status
        boolean is_global
        date created_date
    }

    dimCycle {
        int cycle_id PK
        int release_id FK
        string cycle_name
        date start_date
        date end_date
        string status
        string environment
        string build
        date created_date
    }

    dimTestcase {
        bigint testcase_id PK
        int project_id FK
        bigint folder_id FK
        string testcase_name
        string testcase_type
        string priority
        date created_date
        date last_modified_date
        string description
    }

    dimTester {
        int tester_id PK
        string tester_name
        string tester_email
        boolean is_active
        string role
    }

    dimRequirement {
        bigint requirement_id PK
        int project_id FK
        string requirement_name
        string requirement_type
        string priority
        date created_date
    }

    dimFolder {
        bigint folder_id PK
        int project_id FK
        bigint parent_folder_id FK
        string folder_name
        string folder_path
        int folder_level
    }

    dimDate {
        int date_id PK
        date date
        int year
        int quarter
        int month
        string month_name
        int week
        int day_of_week
        string day_name
        boolean is_weekend
        boolean is_holiday
    }

    dimExecutionStatus {
        int status_id PK
        string status_name
        string status_category
        int sort_order
    }

    %% Bridge Tables
    bridgeTestcaseRequirement {
        bigint testcase_id FK
        bigint requirement_id FK
        date allocation_date
        boolean is_active
    }

    bridgeTestcaseCycle {
        bigint testcase_id FK
        int cycle_id FK
        date assignment_date
        boolean is_active
    }
```

---

## 📐 Visual Layout (Power BI Style)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ZEPHYR DIMENSIONAL MODEL                     │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │    dimExecutionStatus│
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │   factExecution      │ ◄─── CENTRE (Fact)
                    │  (Core Fact Table)   │
                    └──┬──┬──┬──┬──┬──┬───┘
                       │  │  │  │  │  │
    ┌──────────────────┘  │  │  │  │  └──────────────────┐
    │                     │  │  │  │                      │
┌───▼────┐        ┌───────▼──┘  │  │        ┌────────────▼──┐
│dimDate │        │  dimProject  │  │        │  dimTestcase  │
└────────┘        └───────┬──────┘  │        └───────────────┘
                          │         │
                    ┌─────▼─────┐   │    ┌──────────────┐
                    │dimRelease │   │    │  dimTester   │
                    └─────┬─────┘   │    └──────────────┘
                          │         │
                    ┌─────▼─────┐   │
                    │ dimCycle  │───┘
                    └───────────┘

                    ┌──────────────────────┐
                    │factRequirementCoverage│
                    └──┬──────────────┬─────┘
                       │              │
              ┌────────▼────┐  ┌─────▼─────────┐
              │dimRequirement│  │bridgeTestcase │
              └──────────────┘  │  Requirement  │
                                └───────┬───────┘
                                        │
                              ┌─────────▼──────────┐
                              │bridgeTestcaseCycle │
                              └────────────────────┘

                    ┌──────────────────────┐
                    │factCycleStatusHistory│
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │     dimCycle         │
                    └──────────────────────┘
```

---

## 🔗 Relationship Summary

### One-to-Many Relationships

| From Dimension       | To Fact         | Relationship                   |
| -------------------- | --------------- | ------------------------------ |
| `dimProject`         | `factExecution` | One project → Many executions  |
| `dimRelease`         | `factExecution` | One release → Many executions  |
| `dimCycle`           | `factExecution` | One cycle → Many executions    |
| `dimTestcase`        | `factExecution` | One testcase → Many executions |
| `dimTester`          | `factExecution` | One tester → Many executions   |
| `dimDate`            | `factExecution` | One date → Many executions     |
| `dimExecutionStatus` | `factExecution` | One status → Many executions   |

### Hierarchical Relationships

| Parent       | Child            | Relationship                           |
| ------------ | ---------------- | -------------------------------------- |
| `dimProject` | `dimRelease`     | Project contains releases              |
| `dimRelease` | `dimCycle`       | Release contains cycles                |
| `dimProject` | `dimTestcase`    | Project contains testcases             |
| `dimProject` | `dimRequirement` | Project contains requirements          |
| `dimProject` | `dimFolder`      | Project contains folders               |
| `dimFolder`  | `dimFolder`      | Folder contains subfolders (recursive) |
| `dimFolder`  | `dimTestcase`    | Folder contains testcases              |

### Many-to-Many Relationships (Bridge Tables)

| Bridge Table                | Entities Linked        |
| --------------------------- | ---------------------- |
| `bridgeTestcaseRequirement` | Testcase ↔ Requirement |
| `bridgeTestcaseCycle`       | Testcase ↔ Cycle       |

---

## 📊 Table Counts

- **Fact Tables:** 3 (`factExecution`, `factRequirementCoverage`, `factCycleStatusHistory`)
- **Dimensions:** 8 (`dimProject`, `dimRelease`, `dimCycle`, `dimTestcase`, `dimTester`, `dimRequirement`, `dimFolder`, `dimDate`, `dimExecutionStatus`)
- **Bridge Tables:** 2 (`bridgeTestcaseRequirement`, `bridgeTestcaseCycle`)
- **Total Tables:** 13

---

## 🎯 Relationship Cardinality

All relationships follow standard star schema patterns:

- **Fact → Dimension:** Many-to-One (N:1)
- **Dimension → Dimension (Hierarchy):** One-to-Many (1:N)
- **Bridge Tables:** Many-to-Many (M:N)

---

## 📚 References

- **Full Design:** `Data/zephyr/docs/refine/DIMENSIONAL-MODEL-DESIGN.md`
- **Enrichment Items:** See enrichment section below
