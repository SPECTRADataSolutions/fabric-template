# Burndown Chart Design (Zephyr)

**Date**: 2025-12-10  
**Status**: ✅ Active Standard  
**Purpose**: Design burndown charts and required enrichment for Zephyr test management

---

## Overview

Burndown charts show work remaining over time, comparing planned vs actual progress. For Zephyr, we need:

1. **Execution Burndown** - Tests remaining in cycle over time
2. **Cycle Progress Burndown** - Cycle completion over time
3. **Requirement Coverage Burndown** - Requirements covered over time

---

## Burndown Chart Types

### **1. Execution Burndown (Primary)**

**Purpose:** Show test execution progress through cycle

**X-Axis:** Working days (from `dimCycleDate`)  
**Y-Axis:** Tests remaining (unexecuted + failed + blocked)

**Lines:**
- **Planned:** Ideal burndown (linear from start to end)
- **Actual:** Actual burndown (based on execution dates)
- **Scope Change:** When testcases added/removed from cycle

**Measures:**
- `Tests Remaining Count` = Total testcases - Completed executions
- `Tests Completed Count` = Executions with status = Passed
- `Tests Remaining %` = (Tests Remaining / Total Testcases) * 100
- `Burndown Velocity` = Tests completed per working day
- `Days Behind/Ahead` = Actual vs planned comparison

---

### **2. Cycle Progress Burndown**

**Purpose:** Show cycle completion progress

**X-Axis:** Working days (from `dimCycleDate`)  
**Y-Axis:** Work remaining (percentage or count)

**Lines:**
- **Planned:** Ideal cycle completion
- **Actual:** Actual cycle completion
- **Status Transitions:** Cycle status changes

**Measures:**
- `Cycle Completion %` = (Completed executions / Total testcases) * 100
- `Cycle Progress %` = Days elapsed / Total cycle days
- `Cycle Health Score` = Composite score (completion, velocity, quality)

---

### **3. Requirement Coverage Burndown**

**Purpose:** Show requirement coverage progress

**X-Axis:** Working days  
**Y-Axis:** Requirements remaining (uncovered)

**Lines:**
- **Planned:** Ideal coverage progress
- **Actual:** Actual coverage progress

**Measures:**
- `Requirements Covered Count` = Requirements with testcases allocated
- `Requirements Remaining Count` = Total requirements - Covered
- `Coverage %` = (Covered / Total) * 100

---

## Required Enrichment Fields

### **For `factExecution` (Execution Burndown)**

#### **Cycle Context (Critical for Burndown)**

```python
# Cycle boundaries
"cycleStartDate": date,              # Cycle start date
"cycleEndDate": date,                 # Cycle end date
"cycleDurationDays": integer,         # Total cycle days (calendar)
"cycleWorkingDays": integer,          # Total working days (excludes weekends/holidays)
"cycleDateKey": integer,              # Join key to dimCycleDate (YYYYMMDD)

# Execution position in cycle
"daysSinceCycleStart": integer,        # Days from cycle start to execution
"workingDaysSinceCycleStart": integer, # Working days from cycle start
"daysUntilCycleEnd": integer,         # Days from execution to cycle end
"workingDaysUntilCycleEnd": integer,   # Working days until cycle end
"cycleProgressPct": float,            # % through cycle when executed (0-100)

# Burndown calculations
"testsRemainingAtExecution": integer,  # Tests remaining when this execution occurred
"testsCompletedAtExecution": integer,  # Tests completed when this execution occurred
"burndownVelocity": float,             # Tests completed per working day (at this point)
"plannedTestsRemaining": integer,      # Planned tests remaining (ideal burndown)
"actualVsPlannedDelta": integer,       # Actual - Planned (negative = ahead, positive = behind)
"isAheadOfSchedule": boolean,          # Actual < Planned
"isBehindSchedule": boolean,           # Actual > Planned
```

#### **Scope Change Tracking**

```python
# Scope changes (testcases added/removed from cycle)
"scopeChangeDate": date,              # Date scope changed
"testcasesAdded": integer,             # Testcases added to cycle
"testcasesRemoved": integer,           # Testcases removed from cycle
"scopeChangeReason": string,           # Reason for scope change
"isScopeChange": boolean,              # True if scope changed on this date
```

#### **Execution Status for Burndown**

```python
# Status categories (for burndown)
"isCompleted": boolean,                # Status = Passed (counts as done)
"isRemaining": boolean,                # Status = Not Executed, Failed, Blocked (counts as remaining)
"isBlocked": boolean,                  # Status = Blocked (special case)
"isOutOfScope": boolean,               # Out of scope (excluded from burndown)
```

---

### **For `dimCycleDate` (Working Day Dimension)**

**Purpose:** Track working days for cycle (excludes weekends/holidays)

**Key Fields:**

```python
"cycleDateKey": integer,              # Primary key (YYYYMMDD)
"cycleId": integer,                   # Foreign key to dimCycle
"date": date,                         # Actual date
"isWorkingDay": boolean,              # Excludes weekends/holidays
"workingDayNumber": integer,          # Sequential working day (1, 2, 3...)
"dayOfCycle": integer,                # Day number in cycle (1, 2, 3...)
"isWeekend": boolean,                 # Saturday/Sunday
"isHoliday": boolean,                 # Bank holiday (if available)
"isCycleStart": boolean,              # First day of cycle
"isCycleEnd": boolean,                # Last day of cycle
```

**Usage:**
- Join `factExecution` to `dimCycleDate` on `cycleDateKey`
- Filter by `isWorkingDay = True` for burndown calculations
- Use `workingDayNumber` for X-axis in burndown charts

---

### **For `dimCycle` (Cycle Context)**

**Enrichment Fields:**

```python
# Cycle planning
"totalTestcases": integer,            # Total testcases in cycle
"plannedExecutions": integer,         # Planned execution count
"cycleStartDate": date,               # Cycle start
"cycleEndDate": date,                 # Cycle end
"cycleDurationDays": integer,         # Calendar days
"cycleWorkingDays": integer,          # Working days (excludes weekends/holidays)

# Burndown targets
"plannedCompletionDate": date,        # Planned completion date
"idealBurndownVelocity": float,       # Tests per working day (planned)
"actualBurndownVelocity": float,      # Tests per working day (actual)

# Progress tracking
"executionsCompleted": integer,       # Completed executions
"executionsRemaining": integer,       # Remaining executions
"cycleCompletionPct": float,         # % complete
"cycleProgressPct": float,           # % through cycle timeline

# Health indicators
"isOnTrack": boolean,                 # On track vs planned
"daysBehindSchedule": integer,        # Days behind (negative = ahead)
"burndownHealthScore": float,         # Composite health score (0-100)
```

---

## Burndown Construction Logic

### **1. Build `dimCycleDate` (Refine Stage)**

**Purpose:** Create working day dimension for each cycle

**Logic:**
```python
# For each cycle
cycle_start = dimCycle.cycleStartDate
cycle_end = dimCycle.cycleEndDate

# Generate all dates in cycle
all_dates = generate_date_range(cycle_start, cycle_end)

# Mark working days (exclude weekends/holidays)
cycle_dates = []
working_day_num = 0
for date in all_dates:
    is_working = not (is_weekend(date) or is_holiday(date))
    if is_working:
        working_day_num += 1
    
    cycle_dates.append({
        "cycleDateKey": date_to_key(date),  # YYYYMMDD
        "cycleId": cycle.cycleId,
        "date": date,
        "isWorkingDay": is_working,
        "workingDayNumber": working_day_num if is_working else None,
        "dayOfCycle": (date - cycle_start).days + 1,
        "isWeekend": is_weekend(date),
        "isHoliday": is_holiday(date),
        "isCycleStart": date == cycle_start,
        "isCycleEnd": date == cycle_end
    })

# Write dimCycleDate
dimCycleDate.write.format("delta").save("Tables/refine/dimCycleDate")
```

---

### **2. Enrich `factExecution` (Refine Stage)**

**Purpose:** Add burndown context to each execution

**Logic:**
```python
# Join factExecution to dimCycleDate
fact_execution = factExecution.join(
    dimCycleDate.select("cycleDateKey", "cycleId", "workingDayNumber", "isWorkingDay"),
    on=["cycleId", "cycleDateKey"],
    how="left"
)

# Calculate burndown metrics
fact_execution = fact_execution.withColumn(
    "testsRemainingAtExecution",
    calculate_tests_remaining("executionDate", "cycleId")
).withColumn(
    "testsCompletedAtExecution",
    calculate_tests_completed("executionDate", "cycleId")
).withColumn(
    "plannedTestsRemaining",
    calculate_planned_remaining("workingDayNumber", "cycleId")
).withColumn(
    "actualVsPlannedDelta",
    F.col("testsRemainingAtExecution") - F.col("plannedTestsRemaining")
)

# Write enriched factExecution
fact_execution.write.format("delta").save("Tables/refine/factExecution")
```

---

### **3. DAX Measures (Analyse Stage) - NO AGGREGATION TABLE NEEDED**

**Purpose:** Calculate burndown directly from enriched `factExecution` + `dimCycleDate`

**Key Insight:** No pre-aggregation needed! Enrich `factExecution` with `workingDayNumber` and cycle totals, then calculate directly in DAX.

**See:** `docs/refine/burndown-direct-calculation.md` for complete SPECTRA-grade approach

**Benefits:**
- ✅ No aggregation table = simpler architecture
- ✅ More flexible = can recalculate for any scenario
- ✅ Still performant = enrichment done once in Refine stage
- ✅ DAX is fast = with proper indexing and relationships

---

## Burndown Calculations

### **Planned Burndown (Ideal Line)**

```python
def calculate_planned_remaining(working_day_num, cycle_id):
    """Calculate planned tests remaining (ideal burndown)."""
    cycle = dimCycle.filter(F.col("cycleId") == cycle_id).first()
    total_tests = cycle.totalTestcases
    total_working_days = cycle.cycleWorkingDays
    
    # Linear burndown: remaining = total - (total / days) * day_num
    planned_remaining = total_tests - (total_tests / total_working_days) * working_day_num
    return max(0, planned_remaining)  # Can't go negative
```

### **Actual Burndown**

```python
def calculate_actual_remaining(execution_date, cycle_id):
    """Calculate actual tests remaining at execution date."""
    # Count unexecuted + failed + blocked at this point in time
    remaining = (factExecution
        .filter(F.col("cycleId") == cycle_id)
        .filter(F.col("executionDate") <= execution_date)
        .filter(F.col("isRemaining") == True)
        .count()
    )
    return remaining
```

### **Burndown Velocity**

```python
def calculate_velocity(cycle_id, working_day_num):
    """Calculate tests completed per working day."""
    completed = (factExecution
        .filter(F.col("cycleId") == cycle_id)
        .filter(F.col("workingDayNumber") <= working_day_num)
        .filter(F.col("isCompleted") == True)
        .count()
    )
    return completed / working_day_num if working_day_num > 0 else 0
```

---

## Scope Change Handling

### **Track Scope Changes**

```python
# Detect scope changes (testcases added/removed from cycle)
scope_changes = (factExecution
    .groupBy("cycleId", "cycleDateKey")
    .agg(
        F.countDistinct("testcaseId").alias("testcaseCount")
    )
    .withColumn("prevTestcaseCount", F.lag("testcaseCount").over(
        Window.partitionBy("cycleId").orderBy("cycleDateKey")
    ))
    .filter(F.col("testcaseCount") != F.col("prevTestcaseCount"))
    .withColumn("testcasesAdded", F.col("testcaseCount") - F.col("prevTestcaseCount"))
    .withColumn("isScopeChange", F.lit(True))
)
```

### **Adjust Burndown for Scope Changes**

```python
# When scope changes, adjust planned burndown
# Option 1: Recalculate from change point
# Option 2: Show scope change as vertical line on chart
# Option 3: Adjust ideal line to account for scope change
```

---

## Power BI Measures (Analyse Stage)

### **Burndown Measures**

```dax
// Tests Remaining Count
Tests Remaining Count = 
CALCULATE(
    COUNTROWS(factExecution),
    factExecution[isRemaining] = TRUE,
    dimCycleDate[isWorkingDay] = TRUE
)

// Tests Completed Count
Tests Completed Count = 
CALCULATE(
    COUNTROWS(factExecution),
    factExecution[isCompleted] = TRUE,
    dimCycleDate[isWorkingDay] = TRUE
)

// Burndown Velocity (Tests per Working Day)
Burndown Velocity = 
DIVIDE(
    [Tests Completed Count],
    MAX(dimCycleDate[workingDayNumber])
)

// Days Behind/Ahead Schedule
Days Behind Schedule = 
AVERAGE(factExecution[actualVsPlannedDelta])

// Burndown Health Score (0-100)
Burndown Health Score = 
VAR VelocityScore = IF([Burndown Velocity] >= 1, 100, [Burndown Velocity] * 100)
VAR ScheduleScore = IF([Days Behind Schedule] <= 0, 100, 100 - ABS([Days Behind Schedule]) * 10)
RETURN (VelocityScore + ScheduleScore) / 2
```

---

## Implementation Roadmap

### **Phase 1: Core Burndown (MVP)**

**Refine Stage:**
- ✅ Build `dimCycleDate` (working day dimension)
- ✅ Enrich `factExecution` with cycle context
- ✅ Calculate `testsRemainingAtExecution`
- ✅ Calculate `plannedTestsRemaining`

**Analyse Stage:**
- ✅ Build burndown aggregates
- ✅ Create Power BI measures

### **Phase 2: Enhanced Burndown**

**Refine Stage:**
- ⏳ Add scope change tracking
- ⏳ Add burndown velocity calculation
- ⏳ Add health score calculation

**Analyse Stage:**
- ⏳ Advanced burndown visualizations
- ⏳ Predictive burndown (ML-based)

---

## References

- **Jira Metric Standards**: `Data/jira/docs/standards/metric-standards.md`
- **Dimensional Model**: `docs/refine/dimensional-model-design.md`
- **Enrichment Items**: `docs/refine/dimensional-model-enrichment.md`

---

**Version**: 1.0  
**Last Updated**: 2025-12-10  
**Status**: ✅ Active Standard

