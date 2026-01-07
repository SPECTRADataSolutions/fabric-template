# Burndown Direct Calculation (SPECTRA-Grade)

**Date**: 2025-12-10  
**Status**: ✅ SPECTRA-Grade Design  
**Purpose**: Calculate burndown charts directly from `factExecution` + `dimCycleDate` without aggregation tables

---

## Key Insight

**Instead of pre-aggregating, enrich `factExecution` with burndown context and calculate directly in DAX.**

**Why This is More Efficient:**
- ✅ No aggregation table = simpler architecture
- ✅ More flexible = can recalculate for any scenario
- ✅ Still performant = enrichment done once in Refine stage
- ✅ DAX is fast = with proper indexing and relationships

---

## Architecture

### **No Aggregation Table Needed**

**Old Approach (Legacy):**
```
factExecution → aggExecutionMetrics (pre-aggregated) → DAX measures
```

**New Approach (SPECTRA-Grade):**
```
factExecution (enriched) + dimCycleDate → DAX measures (direct calculation)
```

---

## Enrichment Strategy

### **1. Join `factExecution` to `dimCycleDate` (Refine Stage)**

**Purpose:** Add working day context to each execution

```python
# Join factExecution to dimCycleDate
fact_execution = factExecution.join(
    dimCycleDate.select(
        "cycleDateKey", 
        "cycleId", 
        "workingDayNumber", 
        "isWorkingDay",
        "dayOfCycle",
        "cycleStartDate",
        "cycleEndDate"
    ),
    on=["cycleId", "cycleDateKey"],
    how="left"
)
```

**Result:** Every execution row has `workingDayNumber` for that execution date.

---

### **2. Add Cycle-Level Context (Refine Stage)**

**Purpose:** Add cycle totals to each execution row (for DAX calculations)

```python
# Join to dimCycle to get cycle totals
fact_execution = fact_execution.join(
    dimCycle.select(
        "cycleId",
        "totalTestcases",           # Total testcases in cycle
        "cycleWorkingDays",          # Total working days in cycle
        "cycleStartDate",
        "cycleEndDate"
    ),
    on="cycleId",
    how="left"
)
```

**Result:** Every execution row knows:
- Total testcases in cycle
- Total working days in cycle
- Current working day number

---

### **3. Add Status Flags (Refine Stage)**

**Purpose:** Mark executions as completed/remaining for burndown

```python
# Status flags for burndown
fact_execution = fact_execution.withColumn(
    "isCompleted",
    F.when(F.col("executionStatusId").isin([1, 2, 3]), 1).otherwise(0)  # Passed, Failed, Blocked
).withColumn(
    "isRemaining",
    F.when(F.col("executionStatusId").isin([0, 2, 3, 4]), 1).otherwise(0)  # Not Executed, Failed, Blocked, etc.
)
```

**Result:** Every execution row has clear status flags.

---

## DAX Measures (Direct Calculation)

### **No Aggregation Table - Calculate Directly from `factExecution`**

**Key:** Use `workingDayNumber` from `dimCycleDate` to group/filter, but calculate from `factExecution` directly.

---

### **1. Tests Remaining (At Any Working Day)**

```dax
// Tests Remaining Count (at selected working day)
Tests Remaining Count = 
VAR SelectedWorkingDay = MAX(dimCycleDate[workingDayNumber])
RETURN
    CALCULATE(
        COUNTROWS(factExecution),
        factExecution[isRemaining] = 1,
        factExecution[workingDayNumber] <= SelectedWorkingDay,
        dimCycleDate[isWorkingDay] = TRUE
    )
```

**How it works:**
- Filters `factExecution` to executions up to selected working day
- Counts rows where `isRemaining = 1`
- No aggregation table needed!

---

### **2. Tests Completed (At Any Working Day)**

```dax
// Tests Completed Count (at selected working day)
Tests Completed Count = 
VAR SelectedWorkingDay = MAX(dimCycleDate[workingDayNumber])
RETURN
    CALCULATE(
        COUNTROWS(factExecution),
        factExecution[isCompleted] = 1,
        factExecution[workingDayNumber] <= SelectedWorkingDay,
        dimCycleDate[isWorkingDay] = TRUE
    )
```

---

### **3. Planned Tests Remaining (Ideal Burndown Line)**

```dax
// Planned Tests Remaining (ideal burndown)
Planned Tests Remaining = 
VAR SelectedWorkingDay = MAX(dimCycleDate[workingDayNumber])
VAR CycleTotal = MAX(factExecution[totalTestcases])
VAR CycleWorkingDays = MAX(factExecution[cycleWorkingDays])
VAR PlannedRemaining = CycleTotal - (CycleTotal / CycleWorkingDays) * SelectedWorkingDay
RETURN
    MAX(0, PlannedRemaining)  // Can't go negative
```

**How it works:**
- Gets cycle totals from `factExecution` (enriched in Refine stage)
- Calculates ideal burndown line: `total - (total / days) * day_num`
- No pre-aggregation needed!

---

### **4. Actual vs Planned Delta**

```dax
// Actual vs Planned Delta
Actual vs Planned Delta = 
[Tests Remaining Count] - [Planned Tests Remaining]
```

**Simple subtraction** - no aggregation table needed!

---

### **5. Burndown Velocity**

```dax
// Burndown Velocity (Tests per Working Day)
Burndown Velocity = 
VAR SelectedWorkingDay = MAX(dimCycleDate[workingDayNumber])
VAR Completed = [Tests Completed Count]
RETURN
    DIVIDE(Completed, SelectedWorkingDay)
```

**Calculates directly from `factExecution`** - no aggregation needed!

---

### **6. Forecast Completion (Based on Average Velocity)**

```dax
// Forecast Completion Date (based on average velocity)
Forecast Completion Date = 
VAR AvgVelocity = [Burndown Velocity]
VAR Remaining = [Tests Remaining Count]
VAR WorkingDaysNeeded = DIVIDE(Remaining, AvgVelocity)
VAR LastWorkingDay = MAX(dimCycleDate[workingDayNumber])
VAR ForecastWorkingDay = LastWorkingDay + WorkingDaysNeeded
RETURN
    // Lookup date from dimCycleDate where workingDayNumber = ForecastWorkingDay
    CALCULATE(
        MAX(dimCycleDate[date]),
        dimCycleDate[workingDayNumber] = ForecastWorkingDay
    )
```

---

## Performance Optimization

### **Why This is Fast**

1. **Enrichment Done Once** (Refine stage)
   - `workingDayNumber` joined to `factExecution`
   - Cycle totals added to each row
   - Status flags calculated once

2. **DAX is Fast with Proper Indexing**
   - `factExecution` indexed on `cycleId`, `cycleDateKey`
   - `dimCycleDate` indexed on `workingDayNumber`
   - Relationships properly defined

3. **No Pre-Aggregation Overhead**
   - No aggregation table to maintain
   - No refresh bottleneck
   - Can recalculate for any scenario instantly

---

## Comparison: Legacy vs SPECTRA-Grade

### **Legacy Approach (Inefficient)**

```
factExecution → aggExecutionMetrics (pre-aggregated)
                              ↓
                    DAX measures (read from agg table)
```

**Problems:**
- ❌ Pre-aggregation = inflexible
- ❌ Refresh bottleneck
- ❌ Can't recalculate for different scenarios
- ❌ Working day logic baked into aggregation

### **SPECTRA-Grade Approach (Efficient)**

```
factExecution (enriched) + dimCycleDate
                    ↓
         DAX measures (direct calculation)
```

**Benefits:**
- ✅ No aggregation table = simpler
- ✅ More flexible = can filter/calculate for any scenario
- ✅ Still performant = enrichment done once
- ✅ Working day logic in `dimCycleDate` = clear and maintainable

---

## Implementation

### **Refine Stage: Enrich `factExecution`**

```python
# 1. Join to dimCycleDate
fact_execution = factExecution.join(
    dimCycleDate.select("cycleDateKey", "cycleId", "workingDayNumber", "isWorkingDay"),
    on=["cycleId", "cycleDateKey"],
    how="left"
)

# 2. Join to dimCycle for cycle totals
fact_execution = fact_execution.join(
    dimCycle.select("cycleId", "totalTestcases", "cycleWorkingDays"),
    on="cycleId",
    how="left"
)

# 3. Add status flags
fact_execution = fact_execution.withColumn(
    "isCompleted",
    F.when(F.col("executionStatusId").isin([1, 2, 3]), 1).otherwise(0)
).withColumn(
    "isRemaining",
    F.when(F.col("executionStatusId").isin([0, 2, 3, 4]), 1).otherwise(0)
)

# Write enriched factExecution
fact_execution.write.format("delta").save("Tables/refine/factExecution")
```

### **Analyse Stage: DAX Measures Only**

**No aggregation table needed!** Just create DAX measures that calculate directly from `factExecution`.

---

## Scope Change Handling

### **Track Scope Changes in `factExecution`**

```python
# Add scope change flag to factExecution
fact_execution = fact_execution.withColumn(
    "isScopeChange",
    F.when(F.col("testcasesAdded") > 0, 1)
     .when(F.col("testcasesRemoved") > 0, 1)
     .otherwise(0)
)
```

### **Adjust Planned Burndown in DAX**

```dax
// Planned Tests Remaining (with scope change adjustment)
Planned Tests Remaining (Adjusted) = 
VAR SelectedWorkingDay = MAX(dimCycleDate[workingDayNumber])
VAR CycleTotal = MAX(factExecution[totalTestcases])
VAR CycleWorkingDays = MAX(factExecution[cycleWorkingDays])

// Adjust for scope changes before selected day
VAR ScopeChanges = 
    CALCULATE(
        SUM(factExecution[testcasesAdded]) - SUM(factExecution[testcasesRemoved]),
        factExecution[isScopeChange] = 1,
        factExecution[workingDayNumber] <= SelectedWorkingDay
    )

VAR AdjustedTotal = CycleTotal + ScopeChanges
VAR PlannedRemaining = AdjustedTotal - (AdjustedTotal / CycleWorkingDays) * SelectedWorkingDay
RETURN
    MAX(0, PlannedRemaining)
```

**No aggregation table needed** - calculate scope changes on the fly!

---

## Benefits Summary

### **1. Simpler Architecture**
- No aggregation table to maintain
- One less table to refresh
- Clearer data flow

### **2. More Flexible**
- Can filter/calculate for any scenario
- Can adjust for scope changes dynamically
- Can add new burndown modes easily

### **3. Still Performant**
- Enrichment done once in Refine stage
- DAX is fast with proper indexing
- No refresh bottleneck

### **4. Easier to Maintain**
- Business logic in Refine stage (Python)
- DAX measures are simple (no complex pre-aggregation)
- Clear separation of concerns

---

## Migration from Legacy

### **Remove:**
- ❌ `aggExecutionMetrics` table
- ❌ Pre-aggregation logic
- ❌ Complex DAX reading from aggregation table

### **Add:**
- ✅ `workingDayNumber` enrichment in `factExecution`
- ✅ Cycle totals enrichment in `factExecution`
- ✅ Simple DAX measures calculating directly from `factExecution`

---

**Version**: 1.0  
**Last Updated**: 2025-12-10  
**Status**: ✅ SPECTRA-Grade Design





