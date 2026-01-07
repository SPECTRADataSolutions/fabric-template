# Zephyr Dimensional Model - Enrichment Items

**Status:** 🟢 Complete  
**Version:** 1.0.0  
**Date:** 2025-12-06  
**Objective:** Potential enrichment fields for each dimension and fact table

---

## 🎯 Purpose

This document outlines potential enrichment items for each dimension and fact table in the Zephyr dimensional model. Enrichments enhance analytical capabilities, enable advanced reporting, and support business intelligence features.

**Enrichment Categories:**

- **Calculated Columns:** Derived from existing fields
- **Classification Fields:** Business categorisation and grouping
- **Temporal Fields:** Time-based analysis enhancements
- **Performance Fields:** Optimization and aggregation helpers
- **Quality Fields:** Data quality indicators
- **Business Logic Fields:** Domain-specific enrichments

---

## 📝 Naming Convention

**SPECTRA Naming Convention Boundary:**

This document follows SPECTRA's naming convention standard:

- **Python Code / Internal Processing:** `snake_case` (e.g., `execution_status_id`)
- **Fabric-Visible / Power BI Fields:** `camelCase` (e.g., `executionStatusId`)
- **Power BI Measures (User-Facing):** `Proper Case` (e.g., `Execution Rate %`, `Pass Rate %`)

**Boundary:**

- When fields are visible in Fabric (Delta tables, Power BI columns), they use `camelCase`
- Delta tables use schema prefixes (stage names): `source.portfolio`, `prepare.schema`, `refine.factExecution`
- Power BI measures use `Proper Case` because they are user-facing and should be readable labels
- When referenced in Python code or internal processing, they use `snake_case`

**Reference:** See `docs/standards/NAMING-CONVENTION-BOUNDARY.md` for full specification.

**Note:**

- All enrichment field names in this document use `camelCase` because they are intended for Fabric/Power BI visibility
- All measure names use `Proper Case` because they are user-facing elements in Power BI reports

---

## 📊 Fact Tables

### `refine.factExecution`

#### Calculated Measures (Power BI DAX)

**Note:** Table names in DAX formulas reference tables by name (e.g., `factExecution`). The schema prefix (`refine.`) is part of the Delta table name and is handled by the Power BI connection. In Power BI, tables are typically imported into a flat namespace, so DAX formulas use the table name without the schema prefix.

**Execution Rate Measures:**

- `Execution Rate %` = `COUNTROWS(factExecution) / COUNTROWS(ALL(factExecution))`
- `Pass Rate %` = `DIVIDE(SUM(factExecution[isPassed]), COUNTROWS(factExecution))`
- `Fail Rate %` = `DIVIDE(SUM(factExecution[isFailed]), COUNTROWS(factExecution))`
- `Block Rate %` = `DIVIDE(SUM(factExecution[isBlocked]), COUNTROWS(factExecution))`

**Duration Measures:**

- `Average Execution Duration (seconds)` = `AVERAGE(factExecution[durationSeconds])`
- `Total Execution Time (hours)` = `SUM(factExecution[durationSeconds]) / 3600`
- `Execution Time Variance` = `VAR(factExecution[durationSeconds])`

**Trend Measures:**

- `Executions This Week` = `CALCULATE(COUNTROWS(factExecution), DATESBETWEEN(dimDate[date], TODAY() - 7, TODAY()))`
- `Executions This Month` = `CALCULATE(COUNTROWS(factExecution), DATESBETWEEN(dimDate[date], EOMONTH(TODAY(), -1) + 1, TODAY()))`
- `Execution Growth Rate` = `(COUNTROWS(factExecution) - COUNTROWS(FILTER(factExecution, dimDate[date] < DATEADD(TODAY(), -30, DAY)))) / COUNTROWS(FILTER(factExecution, dimDate[date] < DATEADD(TODAY(), -30, DAY)))`

#### Enrichment Fields (Added to Table)

**Status Flags:**

- `isPassed` (boolean): `execution_status_id = 1`
- `isFailed` (boolean): `execution_status_id = 2`
- `isBlocked` (boolean): `execution_status_id = 3`
- `isNotExecuted` (boolean): `execution_status_id = 4`
- `isCompleted` (boolean): `execution_status_id IN (1, 2, 3)` (excludes "Not Executed")

**Duration Classifications:**

- `durationCategory` (string): "Fast" (< 60s), "Normal" (60-300s), "Slow" (> 300s)
- `durationPercentile` (integer): Percentile rank of duration within cycle
- `isDurationOutlier` (boolean): Duration exceeds 3 standard deviations

**Temporal Enrichments:**

- `executionHour` (integer): Hour of day (0-23)
- `executionDayOfWeek` (string): Monday, Tuesday, etc.
- `executionWeekNumber` (integer): ISO week number
- `executionMonthName` (string): January, February, etc.
- `isWeekendExecution` (boolean): Execution occurred on weekend
- `isAfterHoursExecution` (boolean): Execution outside business hours (9-5)

**Cycle Context:**

- `daysSinceCycleStart` (integer): Days from cycle start to execution
- `daysUntilCycleEnd` (integer): Days from execution to cycle end
- `cycleProgressPct` (float): Percentage through cycle when executed
- `isLateExecution` (boolean): Execution date > cycle end date
- `cycleDateKey` (integer): Join key to dimCycleDate (YYYYMMDD format)
- `workingDaysSinceCycleStart` (integer): Working days from cycle start (excludes weekends/holidays)
- `workingDaysUntilCycleEnd` (integer): Working days until cycle end

**Burndown Context (Critical for Burndown Charts):**

- `testsRemainingAtExecution` (integer): Tests remaining when this execution occurred
- `testsCompletedAtExecution` (integer): Tests completed when this execution occurred
- `plannedTestsRemaining` (integer): Planned tests remaining (ideal burndown line)
- `actualVsPlannedDelta` (integer): Actual - Planned (negative = ahead, positive = behind)
- `isAheadOfSchedule` (boolean): Actual < Planned
- `isBehindSchedule` (boolean): Actual > Planned
- `burndownVelocity` (float): Tests completed per working day (at this point)
- `cycleStartDate` (date): Cycle start date (for context)
- `cycleEndDate` (date): Cycle end date (for context)
- `cycleDurationDays` (integer): Total cycle days (calendar)
- `cycleWorkingDays` (integer): Total working days (excludes weekends/holidays)

**Scope Change Tracking:**

- `scopeChangeDate` (date): Date scope changed (if applicable)
- `testcasesAdded` (integer): Testcases added to cycle
- `testcasesRemoved` (integer): Testcases removed from cycle
- `scopeChangeReason` (string): Reason for scope change
- `isScopeChange` (boolean): True if scope changed on this date

**Tester Performance:**

- `testerTotalExecutions` (integer): Total executions by this tester
- `testerPassRate` (float): Historical pass rate for tester
- `testerAvgDuration` (float): Average duration for tester

**Testcase Context:**

- `testcaseExecutionCount` (integer): Total executions of this testcase
- `testcaseFailCount` (integer): Total failures for this testcase
- `testcaseStabilityScore` (float): Pass rate over last 10 executions

**Quality Indicators:**

- `hasComment` (boolean): Execution has a comment
- `commentLength` (integer): Character count of comment
- `isRepeatExecution` (boolean): Testcase executed multiple times in cycle

---

### `refine.factRequirementCoverage`

#### Enrichment Fields

**Coverage Metrics:**

- `coveragePercentage` (float): Percentage of requirements covered
- `isFullyCovered` (boolean): Requirement has testcases allocated
- `isPartiallyCovered` (boolean): Requirement has some testcases
- `coverageGapCount` (integer): Number of requirements without testcases

**Temporal Enrichments:**

- `daysSinceAllocation` (integer): Days since testcase allocated to requirement
- `allocationWeekNumber` (integer): Week when allocation occurred
- `isRecentAllocation` (boolean): Allocation within last 30 days

**Traceability:**

- `traceabilityScore` (float): Quality score based on requirement-testcase links
- `hasRequirementLink` (boolean): Testcase is linked to requirement

---

### `refine.factCycleStatusHistory`

#### Enrichment Fields

**Status Transition Analysis:**

- `transitionDurationHours` (float): Hours in previous status
- `transitionDurationDays` (float): Days in previous status
- `isStatusStuck` (boolean): Status duration > 7 days
- `statusChangeReason` (string): Reason for status change (if available)

**Cycle Progress:**

- `cycleCompletionPct` (float): Percentage of cycle completed
- `daysBehindSchedule` (integer): Negative if ahead, positive if behind
- `isOnTrack` (boolean): Cycle progressing as expected

---

## 📐 Dimension Tables

### `refine.dimProject`

#### Enrichment Fields

**Organisational Context:**

- `projectCategory` (string): "Internal", "Client", "Maintenance", "Strategic"
- `projectPriority` (string): "Critical", "High", "Medium", "Low"
- `projectOwner` (string): Project owner/lead name
- `projectManager` (string): Project manager name
- `businessUnit` (string): Business unit or division
- `projectStatusCategory` (string): "Active", "On Hold", "Completed", "Cancelled"

**Temporal Enrichments:**

- `projectAgeDays` (integer): Days since project creation
- `projectAgeMonths` (integer): Months since project creation
- `projectAgeYears` (float): Years since project creation
- `isRecentProject` (boolean): Created within last 90 days
- `isMatureProject` (boolean): Created more than 1 year ago

**Performance Indicators:**

- `totalTestcases` (integer): Total testcases in project
- `totalExecutions` (integer): Total executions for project
- `avgPassRate` (float): Average pass rate across all cycles
- `projectHealthScore` (float): Composite health score (0-100)

**Classification:**

- `projectSizeCategory` (string): "Small" (< 100 testcases), "Medium" (100-500), "Large" (> 500)
- `projectComplexity` (string): "Simple", "Moderate", "Complex" (based on testcase count, cycles, etc.)
- `projectTypeClassification` (string): Derived from project_type

**Business Context:**

- `revenueImpact` (string): "High", "Medium", "Low" (if available)
- `customerFacing` (boolean): Project is customer-facing
- `regulatoryRequired` (boolean): Required for compliance

---

### `refine.dimRelease`

#### Enrichment Fields

**Release Planning:**

- `releaseDurationDays` (integer): Days between start and end date
- `releaseDurationWeeks` (integer): Weeks between start and end date
- `isActiveRelease` (boolean): Current date between start and end
- `isPastRelease` (boolean): End date < today
- `isFutureRelease` (boolean): Start date > today
- `releaseProgressPct` (float): Percentage of release completed

**Temporal Classifications:**

- `releaseQuarter` (string): "Q1 2025", "Q2 2025", etc.
- `releaseMonth` (string): "January 2025", etc.
- `releaseYear` (integer): Year of release

**Release Characteristics:**

- `releaseType` (string): "Major", "Minor", "Patch", "Hotfix"
- `isGlobalRelease` (boolean): Matches is_global field
- `releasePriority` (string): Derived from project priority or explicit field

**Performance Context:**

- `totalCycles` (integer): Number of cycles in release
- `totalExecutions` (integer): Total executions across all cycles
- `releasePassRate` (float): Overall pass rate for release

---

### `refine.dimCycle`

#### Enrichment Fields

**Cycle Timing:**

- `cycleDurationDays` (integer): Days between start and end date
- `cycleDurationWeeks` (integer): Weeks between start and end date
- `isActiveCycle` (boolean): Current date between start and end
- `isPastCycle` (boolean): End date < today
- `isFutureCycle` (boolean): Start date > today
- `cycleProgressPct` (float): Percentage of cycle completed
- `daysRemaining` (integer): Days until cycle end (negative if past)
- `daysElapsed` (integer): Days since cycle start

**Cycle Performance:**

- `totalTestcases` (integer): Total testcases in cycle
- `totalExecutions` (integer): Total executions in cycle
- `completedExecutions` (integer): Executions with status Passed/Failed/Blocked
- `pendingExecutions` (integer): Executions with status Not Executed
- `cyclePassRate` (float): Pass rate for cycle
- `cycleCompletionRate` (float): Percentage of testcases executed

**Burndown Planning:**

- `plannedExecutions` (integer): Planned execution count
- `plannedCompletionDate` (date): Planned completion date
- `idealBurndownVelocity` (float): Tests per working day (planned)
- `actualBurndownVelocity` (float): Tests per working day (actual)
- `executionsRemaining` (integer): Remaining executions (for burndown)
- `cycleCompletionPct` (float): % complete (executionsCompleted / totalTestcases)
- `cycleProgressPct` (float): % through cycle timeline (daysElapsed / cycleDurationDays)
- `isOnTrack` (boolean): On track vs planned burndown
- `daysBehindSchedule` (integer): Days behind (negative = ahead)
- `burndownHealthScore` (float): Composite health score (0-100)

**Environment & Build:**

- `environmentCategory` (string): "Development", "Testing", "Staging", "Production"
- `buildVersionMajor` (integer): Major version number (if semantic versioning)
- `buildVersionMinor` (integer): Minor version number
- `buildVersionPatch` (integer): Patch version number
- `isProductionBuild` (boolean): Environment = "Production"

**Cycle Classification:**

- `cycleType` (string): "Smoke Test", "Regression", "Full", "Targeted"
- `cycleSizeCategory` (string): "Small" (< 50 testcases), "Medium" (50-200), "Large" (> 200)
- `cyclePriority` (string): "Critical", "High", "Medium", "Low"

**Quality Indicators:**

- `blockedCount` (integer): Number of blocked executions
- `blockRate` (float): Percentage of executions blocked
- `avgExecutionDuration` (float): Average duration of executions
- `cycleHealthScore` (float): Composite health score (0-100)

---

### `refine.dimTestcase`

#### Enrichment Fields

**Testcase Characteristics:**

- `testcaseNameLength` (integer): Character count of name
- `testcaseDescriptionLength` (integer): Character count of description
- `hasDescription` (boolean): Testcase has description
- `testcaseAgeDays` (integer): Days since creation
- `testcaseAgeMonths` (integer): Months since creation
- `isRecentTestcase` (boolean): Created within last 30 days
- `isMatureTestcase` (boolean): Created more than 6 months ago

**Testcase Performance:**

- `totalExecutions` (integer): Total executions across all cycles
- `passCount` (integer): Number of passing executions
- `failCount` (integer): Number of failing executions
- `blockCount` (integer): Number of blocked executions
- `passRate` (float): Historical pass rate
- `failRate` (float): Historical fail rate
- `stabilityScore` (float): Consistency score (higher = more stable)

**Testcase Classification:**

- `testcasePriorityNumeric` (integer): 1=Critical, 2=High, 3=Medium, 4=Low
- `testcaseTypeCategory` (string): Categorised type
- `testcaseComplexity` (string): "Simple", "Moderate", "Complex" (based on description, history)

**Relationship Context:**

- `requirementCount` (integer): Number of requirements linked to testcase
- `hasRequirementLink` (boolean): Testcase linked to at least one requirement
- `folderDepth` (integer): Depth in folder hierarchy
- `folderPathDisplay` (string): Human-readable folder path

**Quality Indicators:**

- `lastExecutionDate` (datetime): Date of most recent execution
- `daysSinceLastExecution` (integer): Days since last execution
- `isStaleTestcase` (boolean): Not executed in last 90 days
- `executionFrequency` (string): "Daily", "Weekly", "Monthly", "Rarely"

---

### `refine.dimTester`

#### Enrichment Fields

**Tester Performance:**

- `totalExecutions` (integer): Total executions by tester
- `passCount` (integer): Total passing executions
- `failCount` (integer): Total failing executions
- `blockCount` (integer): Total blocked executions
- `passRate` (float): Historical pass rate
- `avgExecutionDuration` (float): Average duration of executions
- `testerProductivityScore` (float): Composite productivity score

**Tester Activity:**

- `lastExecutionDate` (datetime): Date of most recent execution
- `daysSinceLastExecution` (integer): Days since last execution
- `executionsThisMonth` (integer): Executions in current month
- `executionsThisWeek` (integer): Executions in current week
- `isActiveTester` (boolean): Has executed tests in last 30 days

**Organisational Context:**

- `testerDepartment` (string): Department or team
- `testerLocation` (string): Geographic location (if available)
- `testerExperienceLevel` (string): "Junior", "Mid", "Senior", "Lead"
- `isExternalTester` (boolean): Tester is external contractor

---

### `refine.dimRequirement`

#### Enrichment Fields

**Requirement Characteristics:**

- `requirementNameLength` (integer): Character count of name
- `requirementAgeDays` (integer): Days since creation
- `requirementAgeMonths` (integer): Months since creation
- `isRecentRequirement` (boolean): Created within last 30 days

**Coverage Analysis:**

- `linkedTestcaseCount` (integer): Number of testcases linked to requirement
- `isCovered` (boolean): Has at least one linked testcase
- `coverageScore` (float): Quality score based on testcase links
- `hasPassingTestcase` (boolean): Has at least one passing testcase

**Requirement Classification:**

- `requirementPriorityNumeric` (integer): 1=Critical, 2=High, 3=Medium, 4=Low
- `requirementTypeCategory` (string): Categorised type
- `requirementComplexity` (string): "Simple", "Moderate", "Complex"

**Business Context:**

- `requirementStatus` (string): "Draft", "Approved", "Implemented", "Validated"
- `isBusinessCritical` (boolean): Priority = "Critical"
- `isRegulatoryRequirement` (boolean): Required for compliance

---

### `refine.dimFolder`

#### Enrichment Fields

**Hierarchy Analysis:**

- `folderPathLength` (integer): Character count of full path
- `folderDepth` (integer): Depth in hierarchy (level)
- `isRootFolder` (boolean): folder_level = 0
- `isLeafFolder` (boolean): No child folders
- `childFolderCount` (integer): Number of child folders
- `descendantFolderCount` (integer): Total descendants

**Folder Content:**

- `testcaseCount` (integer): Number of testcases in folder
- `totalTestcasesInSubtree` (integer): Testcases in folder and all descendants
- `isEmptyFolder` (boolean): No testcases in folder or descendants
- `folderDensityScore` (float): Testcases per folder depth level

**Folder Organisation:**

- `folderCategory` (string): Derived from folder path patterns
- `folderNamingPattern` (string): Pattern detection (e.g., "Feature-_", "Module-_")
- `folderCompletenessScore` (float): Quality score based on organisation

---

### `refine.dimDate`

#### Enrichment Fields

**Extended Temporal Attributes:**

- `fiscalYear` (integer): Fiscal year (if different from calendar)
- `fiscalQuarter` (integer): Fiscal quarter
- `fiscalMonth` (integer): Fiscal month
- `isoWeek` (integer): ISO week number
- `isoYear` (integer): ISO year
- `dayOfMonth` (integer): Day number (1-31)
- `dayOfYear` (integer): Day number (1-365/366)

**Business Calendar:**

- `isBusinessDay` (boolean): Not weekend and not holiday
- `isHoliday` (boolean): Public holiday
- `holidayName` (string): Name of holiday (if applicable)
- `businessDayNumber` (integer): Sequential business day number
- `weekOfMonth` (integer): Week number within month (1-5)

**Reporting Periods:**

- `reportingPeriod` (string): "Current Week", "Last Week", "Current Month", etc.
- `isCurrentPeriod` (boolean): Date is in current reporting period
- `isPreviousPeriod` (boolean): Date is in previous reporting period
- `periodLabel` (string): Human-readable period label

**Seasonal Attributes:**

- `season` (string): "Spring", "Summer", "Autumn", "Winter"
- `isMonthEnd` (boolean): Last day of month
- `isQuarterEnd` (boolean): Last day of quarter
- `isYearEnd` (boolean): Last day of year

---

### `refine.dimExecutionStatus`

#### Enrichment Fields

**Status Classification:**

- `statusSeverity` (integer): 1=Passed, 2=Not Executed, 3=Blocked, 4=Failed
- `statusCategoryDetailed` (string): More granular category
- `isSuccessStatus` (boolean): status_id = 1
- `isFailureStatus` (boolean): status_id = 2
- `isBlockedStatus` (boolean): status_id = 3
- `isPendingStatus` (boolean): status_id = 4

**Status Analytics:**

- `statusFrequency` (integer): How often this status occurs
- `statusPercentage` (float): Percentage of all executions with this status
- `statusTrend` (string): "Increasing", "Decreasing", "Stable"

---

## 🔗 Bridge Tables

### `refine.bridgeTestcaseRequirement`

#### Enrichment Fields

**Allocation Quality:**

- `allocationAgeDays` (integer): Days since allocation
- `isRecentAllocation` (boolean): Allocation within last 30 days
- `allocationStrength` (string): "Strong", "Weak" (based on testcase pass rate)

**Traceability Metrics:**

- `traceabilityScore` (float): Quality score for this link
- `isValidatedLink` (boolean): Link has been validated
- `linkConfidence` (float): Confidence score (0-1)

---

### `refine.bridgeTestcaseCycle`

#### Enrichment Fields

**Assignment Context:**

- `assignmentAgeDays` (integer): Days since assignment
- `isRecentAssignment` (boolean): Assignment within last 7 days
- `assignmentOrder` (integer): Order testcase was assigned to cycle

**Execution Context:**

- `hasBeenExecuted` (boolean): Testcase executed in this cycle
- `executionCount` (integer): Number of times executed in cycle
- `lastExecutionDate` (datetime): Date of last execution in cycle

---

## 📊 Enrichment Implementation Strategy

### Phase 1: MVP Enrichments

**Priority Enrichments (Quick Wins):**

- Status flags (`isPassed`, `isFailed`, etc.)
- Duration categories
- Temporal enrichments (hour, day of week)
- Cycle progress percentages
- Basic counts (total_executions, etc.)

### Phase 2: Performance Enrichments

**Analytical Enhancements:**

- Pass/fail rates
- Stability scores
- Productivity metrics
- Health scores

### Phase 3: Advanced Enrichments

**Business Intelligence:**

- Complex calculated measures
- Trend analysis fields
- Predictive indicators
- Quality scores

---

## 🎯 Enrichment Principles

1. **Derived, Not Stored:** Calculated fields should be computed at query time (Power BI measures) when possible
2. **Performance Aware:** Enrichments should not significantly impact query performance
3. **Business Value:** Every enrichment should serve a clear analytical purpose
4. **Maintainable:** Enrichments should be clearly documented and versioned
5. **Incremental:** Add enrichments incrementally based on business needs

---

## 📚 References

- **Dimensional Model:** `Data/zephyr/docs/refine/DIMENSIONAL-MODEL-DESIGN.md`
- **Model Diagram:** `Data/zephyr/docs/refine/DIMENSIONAL-MODEL-DIAGRAM.md`
- **Power BI Best Practices:** Microsoft Power BI documentation
