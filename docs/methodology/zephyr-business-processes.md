# Zephyr Business Processes & Fact Tables

**Date**: 2025-12-10  
**Status**: ✅ Canonical Reference  
**Purpose**: Complete inventory of Zephyr business processes and required fact tables

---

## Business Process Count

**Total Business Processes: 3**

1. ✅ **Test Execution** → `factExecution` (Primary - MVP)
2. ⏳ **Requirement Coverage** → `factRequirementCoverage` (Future)
3. ⏳ **Cycle Status History** → `factCycleStatusHistory` (Future - requires changelog)

---

## Fact Tables Required

### **1. `factExecution` (Primary - MVP)**

**Business Process:** Test execution  
**Status:** ✅ Primary fact table  
**Grain:** One row per testcase-cycle execution

**Business Activity:**
- Testcase executed in a test cycle
- Measurable event (happened at a point in time)
- Core activity for test management analytics

**Measures:**
- `executionId` (PK)
- `executionStatusId` (1=Passed, 2=Failed, 3=Blocked, 4=Not Executed)
- `executionDate` (when execution occurred)
- `durationSeconds` (execution duration)
- `executionOrder` (order within cycle)

**Dimensions:**
- `projectId` → `dimProject`
- `releaseId` → `dimRelease`
- `cycleId` → `dimCycle`
- `testcaseId` → `dimTestcase`
- `testerId` → `dimTester`
- `executionDateId` → `dimDate`

**Enrichment (Refine Stage):**
- Burndown context (`workingDayNumber`, `testsRemainingAtExecution`, etc.)
- Status flags (`isCompleted`, `isRemaining`)
- Cycle totals (`totalTestcases`, `cycleWorkingDays`)

**Usage:**
- Burndown charts (primary data source)
- Execution metrics
- Pass/fail rates
- Tester performance

---

### **2. `factRequirementCoverage` (Future)**

**Business Process:** Requirement allocation  
**Status:** ⏳ Future enhancement  
**Grain:** One row per testcase-requirement allocation

**Business Activity:**
- Testcase allocated to requirement
- Measurable event (allocation happened)
- Tracks requirement coverage

**Measures:**
- `allocationId` (PK)
- `allocationDate` (when allocation created)
- `coverageStatus` (Covered/Not Covered/Partial)

**Dimensions:**
- `projectId` → `dimProject`
- `requirementId` → `dimRequirement`
- `testcaseId` → `dimTestcase`
- `allocationDateId` → `dimDate`

**Note:** May be replaced by bridge table `bridgeRequirementTestcase` if no measures are needed.

**Usage:**
- Requirement coverage tracking
- Traceability matrix
- Coverage reporting

---

### **3. `factCycleStatusHistory` (Future)**

**Business Process:** Cycle status change  
**Status:** ⏳ Future enhancement (requires changelog)  
**Grain:** One row per cycle-status transition

**Business Activity:**
- Cycle status changes
- Measurable event (status transition happened)
- Tracks cycle progression

**Measures:**
- `transitionId` (PK)
- `fromStatusId` (previous status)
- `toStatusId` (new status)
- `transitionDate` (when transition occurred)
- `durationInStatusDays` (days in previous status)

**Dimensions:**
- `cycleId` → `dimCycle`
- `transitionDateId` → `dimDate`

**Note:** Requires changelog or audit trail. May not be available in initial implementation.

**Usage:**
- Cycle progression tracking
- Status duration analysis
- Cycle health monitoring

---

## Dimensions (Not Fact Tables)

**Key Principle:** Dimensions = Context, not activities

| Entity | Dimension Table | Purpose | Status |
|--------|-----------------|---------|--------|
| `cycle` | `dimCycle` | Cycle dimension (context) | ✅ |
| `project` | `dimProject` | Project dimension (context) | ✅ |
| `release` | `dimRelease` | Release dimension (context) | ✅ |
| `testcase` | `dimTestcase` | Testcase dimension (context) | ✅ |
| `tester` | `dimTester` | Tester dimension (context) | ✅ |
| `requirement` | `dimRequirement` | Requirement dimension (context) | ✅ |
| `folder` | `dimFolder` | Folder dimension (context) | ✅ |
| `phase` | `dimPhase` | Phase dimension (context) | ✅ |

**Why Not Fact Tables:**
- ❌ `cycle` → NOT `factCycle` (cycle is context, not an activity)
- ❌ `project` → NOT `factProject` (project is context, not an activity)
- ❌ `release` → NOT `factRelease` (release is context, not an activity)

**These are containers/context, not measurable business activities.**

---

## Business Process Detection Rules

### **Is it a Business Activity?**

**Test:** Can you measure it? Does it happen over time?

✅ **Business Activities (Fact Tables):**
- Test execution → `factExecution` (testcase executed in cycle)
- Requirement allocation → `factRequirementCoverage` (testcase allocated to requirement)
- Cycle status change → `factCycleStatusHistory` (cycle status transition)

❌ **Not Business Activities (Dimensions):**
- Cycle → `dimCycle` (container/context)
- Project → `dimProject` (container/context)
- Release → `dimRelease` (container/context)
- Testcase → `dimTestcase` (descriptive entity)
- Tester → `dimTester` (descriptive entity)

---

## MVP Fact Tables (Phase 1)

**For MVP, we only need:**

1. ✅ **`factExecution`** - Primary fact table
   - Core business activity
   - Drives burndown charts
   - Execution metrics
   - Pass/fail rates

**All other fact tables are future enhancements.**

---

## Future Fact Tables (Phase 2+)

**Additional fact tables for enhanced analytics:**

2. ⏳ **`factRequirementCoverage`** - Requirement allocation tracking
3. ⏳ **`factCycleStatusHistory`** - Cycle status transition tracking

**Note:** These may not be needed if:
- Requirement allocation can be handled by bridge table
- Cycle status history not available (no changelog)

---

## Summary

| Business Process | Fact Table | Grain | Priority | Status |
|-----------------|------------|-------|----------|--------|
| Test execution | `factExecution` | One row per testcase-cycle execution | P1 (MVP) | ✅ Primary |
| Requirement allocation | `factRequirementCoverage` | One row per testcase-requirement allocation | P2 (Future) | ⏳ Future |
| Cycle status change | `factCycleStatusHistory` | One row per status transition | P2 (Future) | ⏳ Future |

**Total Fact Tables: 3** (1 primary, 2 future)

---

## Implementation Priority

### **Phase 1: MVP (Current Focus)**
- ✅ `factExecution` - Primary fact table
- ✅ All dimensions (dimCycle, dimProject, dimRelease, etc.)
- ✅ Burndown charts from `factExecution`

### **Phase 2: Enhanced Analytics**
- ⏳ `factRequirementCoverage` (if requirement allocation data available)
- ⏳ `factCycleStatusHistory` (if changelog/audit trail available)

---

## References

- **Dimensional Model Design**: `docs/refine/dimensional-model-design.md`
- **Business Process Mapping**: `docs/methodology/BUSINESS-PROCESS-MAPPING.md`
- **Fact Table Modeling**: `docs/methodology/FACT-TABLE-MODELING.md`
- **Model Diagram**: `docs/refine/dimensional-model-diagram.md`

---

**Version**: 1.0  
**Last Updated**: 2025-12-10  
**Status**: ✅ Canonical Reference





