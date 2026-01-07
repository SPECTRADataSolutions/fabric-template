# Business Process Mapping (Zephyr)

**Date**: 2025-12-10  
**Status**: ✅ Active Standard  
**Purpose**: Map Zephyr entities to business processes and fact tables

---

## Business Process → Fact Table Mapping

### **Core Business Activities (Fact Tables)**

| Business Process | Entity | Fact Table | Grain | Status |
|-----------------|--------|------------|-------|--------|
| Test execution | `execution` | `factExecution` | One row per testcase-cycle execution | ✅ Primary |
| Requirement allocation | `requirement` | `factRequirementCoverage` | One row per testcase-requirement allocation | ⏳ Future |
| Cycle status change | `cycle` (changelog) | `factCycleStatusHistory` | One row per status transition | ⏳ Future |

### **Dimensions (Not Fact Tables)**

| Entity | Dimension Table | Purpose | Status |
|--------|-----------------|---------|--------|
| `cycle` | `dimCycle` | Cycle dimension (context) | ✅ |
| `project` | `dimProject` | Project dimension (context) | ✅ |
| `release` | `dimRelease` | Release dimension (context) | ✅ |
| `testcase` | `dimTestcase` | Testcase dimension (context) | ✅ |
| `tester` | `dimTester` | Tester dimension (context) | ✅ |
| `requirement` | `dimRequirement` | Requirement dimension (context) | ✅ |
| `folder` | `dimFolder` | Folder dimension (context) | ✅ |

---

## Key Principle

**Fact tables = Business activities (measurable events)**  
**Dimensions = Context (descriptive entities)**

**Example:**
- ❌ **Wrong**: `cycle` → `factCycle` (cycle is context, not an activity)
- ✅ **Right**: `execution` → `factExecution` (test execution is a measurable business activity)

---

## Modeling Logic Location

### **Prepare Stage: Define Business Processes**

**Responsibility:** Map entities to business processes

**How:**
1. Schema discovery detects entity type
2. Maps to business process:
   - `execution` → Business activity: "Test execution" → `factExecution`
   - `cycle` → Dimension: "Cycle context" → `dimCycle` (NOT fact table)
   - `project` → Dimension: "Project context" → `dimProject` (NOT fact table)
3. Sets `factTableName` and `factGrain` only for business activities
4. Output: `prepare._schema` with business process metadata

### **Clean Stage: Build Fact Tables**

**Responsibility:** Build fact tables from business process metadata

**How:**
1. Load schema from `prepare._schema`
2. Filter by business process:
   ```python
   # Get all fields for factExecution (test execution business process)
   fact_execution_fields = schema.filter(F.col("factTableName") == "factExecution")
                                  .filter(F.col("isInFactIssue") == True)
   ```
3. Build fact table:
   - Load anchor (dateTimeCreated from execution entity)
   - Join all fact fields
   - Ensure grain: "one row per testcase-cycle execution"
4. Write: `Tables/clean/factExecution`

---

## Business Process Detection Rules

### **1. Is it a Business Activity?**

**Test:** Can you measure it? Does it happen over time?

- ✅ **Test execution** - Measurable event (happened at a point in time)
- ✅ **Requirement allocation** - Measurable event (allocation happened)
- ✅ **Cycle status change** - Measurable event (status transition happened)
- ❌ **Cycle** - Not an event (it's a container/context)
- ❌ **Project** - Not an event (it's a container/context)
- ❌ **Release** - Not an event (it's a container/context)

### **2. What's the Grain?**

**Test:** What does one row represent?

- `factExecution`: One row = one testcase executed in one cycle
- `factRequirementCoverage`: One row = one testcase allocated to one requirement
- `factCycleStatusHistory`: One row = one cycle status transition

### **3. What Fields Belong?**

**Test:** Which fields are part of this business activity?

- `factExecution`: executionId, cycleId, testcaseId, statusId, executionDate, durationSeconds
- `factRequirementCoverage`: requirementId, testcaseId, allocationDate, coverageStatus
- `factCycleStatusHistory`: cycleId, fromStatusId, toStatusId, transitionDate, durationInStatusDays

---

## Implementation

### **Schema Discovery Logic:**

```python
# Business process mapping
business_processes = {
    "execution": {
        "factTableName": "factExecution",
        "factGrain": "one row per testcase-cycle execution",
        "isBusinessActivity": True
    },
    "cycle": {
        "factTableName": "",  # Dimension, not fact
        "factGrain": "",
        "isBusinessActivity": False
    },
    # ... etc
}

# Only assign to fact table if business activity
is_in_fact = (process_info["isBusinessActivity"] and 
             is_key_field and 
             structure_type == "scalar")
```

### **Clean Stage Logic:**

```python
# Build factExecution (test execution business process)
fact_execution_fields = schema.filter(F.col("factTableName") == "factExecution")
fact_execution = build_fact_table(fact_execution_fields, grain="one row per testcase-cycle execution")
```

---

## References

- **Dimensional Model Design**: `docs/refine/dimensional-model-design.md`
- **Model Diagram**: `docs/refine/dimensional-model-diagram.md`
- **Enrichment Items**: `docs/refine/dimensional-model-enrichment.md`

---

**Version**: 1.0  
**Last Updated**: 2025-12-10  
**Status**: ✅ Active Standard





