# Data Quality Quarantining - Usage Guide

**Date:** 2025-12-08  
**SDK Version:** 0.3.0  
**Status:** ✅ Implemented

---

## 📋 Overview

The `DataQualityHelpers` class in `spectraSDK` provides metadata-driven data quality validation and quarantining following SPECTRA standards.

**Key Principles:**
- **Never Drop Data** - Invalid records preserved in quarantine tables
- **Metadata-Driven** - Validation rules as data, not code
- **Integrates with Error Handling** - Returns `SpectraError` instances
- **Reusable** - Works across all stages and source systems

---

## 🏗️ Architecture

### Quarantine Path Convention
```
Tables/quarantine/{stage}/{entityName}
```

### Quarantine Table Naming
```
quarantine.{stage}{EntityName}
```
**Example:** `quarantine.sourceProjects` (camelCase, stage prefix)

### Required Columns
- `quarantineReason` - Why record was quarantined (string)
- `quarantineAt` - Timestamp when quarantined (timestamp)
- All original data columns (preserve full record)

---

## 🔧 Basic Usage

### 1. Define Validation Rules

```python
from pyspark.sql import functions as F

validation_rules = [
    {
        "name": "required_id",
        "condition": lambda df: F.col("id").isNull(),
        "message": "Missing required field: id",
        "severity": "error"
    },
    {
        "name": "required_name",
        "condition": lambda df: F.col("name").isNull(),
        "message": "Missing required field: name",
        "severity": "error"
    },
    {
        "name": "future_date_check",
        "condition": lambda df: F.col("createdAt") > F.current_timestamp(),
        "message": "Created date is in the future",
        "severity": "warning"  # Warning - less critical
    }
]
```

### 2. Validate and Quarantine

```python
# Validate DataFrame against rules
df_valid, df_invalid, errors, summary = DataQualityHelpers.validate_and_quarantine(
    spark=spark,
    delta=session.delta,
    df=df_projects,
    entity_name="projects",
    stage="source",
    validation_rules=validation_rules,
    logger=log,
    quarantine_enabled=True,
    source_system="zephyr"
)

# Process valid records
if df_valid.count() > 0:
    delta.write(df_valid, "source.projects", "Tables/source/projects", mode="overwrite")

# Collect errors for reporting
for error in errors:
    error_collector.add(error, critical=False)  # Non-critical - valid records continue
```

### 3. Review Quarantined Records

```sql
-- Query quarantine table
SELECT * FROM quarantine.sourceProjects
ORDER BY quarantineAt DESC;

-- Summary by reason
SELECT quarantineReason, COUNT(*) as count
FROM quarantine.sourceProjects
GROUP BY quarantineReason
ORDER BY count DESC;
```

---

## 📊 Return Values

### `df_valid` (DataFrame)
- Records that passed all validation rules
- Original schema (no quarantine columns)
- Ready for downstream processing

### `df_invalid` (DataFrame)
- Records that failed at least one validation rule
- Original schema + quarantine columns:
  - `errorReason` - Error-level validation failure reason
  - `warningReason` - Warning-level validation failure reason
  - `quarantineReason` - Combined reason (coalesced from error/warning)
  - `quarantineAt` - Timestamp when quarantined

### `errors` (List[SpectraError])
- List of `ValidationError` instances
- One error per unique quarantine reason
- Includes count of records for each reason
- Integrates with `ErrorCollector`

### `summary` (Dict)
- Validation metrics:
  - `entity` - Entity name
  - `stage` - Pipeline stage
  - `total_records` - Total input records
  - `valid_records` - Records that passed validation
  - `quarantined_records` - Records that failed validation
  - `quarantine_rate` - Percentage quarantined (0.0-1.0)
  - `errors` - Count of error-level failures
  - `warnings` - Count of warning-level failures

---

## 🎯 Use Cases

### Use Case 1: Required Field Validation

```python
# Validate required fields
validation_rules = [
    {
        "name": "required_id",
        "condition": lambda df: F.col("id").isNull(),
        "message": "Missing required field: id",
        "severity": "error"
    },
    {
        "name": "required_name",
        "condition": lambda df: F.col("name").isNull(),
        "message": "Missing required field: name",
        "severity": "error"
    }
]

df_valid, df_invalid, errors, summary = DataQualityHelpers.validate_and_quarantine(
    spark=spark, delta=session.delta,
    df=df_projects, entity_name="projects", stage="extract",
    validation_rules=validation_rules, logger=log
)

log.info(f"✅ {summary['valid_records']} valid, {summary['quarantined_records']} quarantined")
```

### Use Case 2: Data Type Validation

```python
# Validate data types and ranges
validation_rules = [
    {
        "name": "invalid_priority",
        "condition": lambda df: ~F.col("priority").isin([1, 2, 3, 4, 5]),
        "message": "Priority must be 1-5",
        "severity": "error"
    },
    {
        "name": "negative_id",
        "condition": lambda df: F.col("id") < 0,
        "message": "ID cannot be negative",
        "severity": "error"
    }
]
```

### Use Case 3: Business Rule Validation

```python
# Validate business rules
validation_rules = [
    {
        "name": "end_before_start",
        "condition": lambda df: F.col("endDate") < F.col("startDate"),
        "message": "End date before start date",
        "severity": "error"
    },
    {
        "name": "missing_release_for_cycle",
        "condition": lambda df: (F.col("releaseId").isNull()) & (F.col("cycleType") == "Release"),
        "message": "Release cycles must have releaseId",
        "severity": "error"
    }
]
```

### Use Case 4: Warning-Level Validation

```python
# Non-blocking warnings (still quarantined for review)
validation_rules = [
    {
        "name": "suspicious_name_length",
        "condition": lambda df: F.length(F.col("name")) > 200,
        "message": "Name unusually long (>200 chars)",
        "severity": "warning"  # Warning - may be valid
    },
    {
        "name": "old_record",
        "condition": lambda df: F.col("lastModified") < F.date_sub(F.current_date(), 365),
        "message": "Record not modified in over 1 year",
        "severity": "warning"  # Warning - may be stale
    }
]
```

---

## 🔗 Integration with Error Handling

### Pattern: Collect Quarantine Errors

```python
from spectra_core.errors import ValidationError

# Initialize error collector
error_collector = ErrorCollector()

# Validate and quarantine
df_valid, df_invalid, dq_errors, summary = DataQualityHelpers.validate_and_quarantine(
    spark=spark, delta=session.delta,
    df=df_projects, entity_name="projects", stage="extract",
    validation_rules=validation_rules, logger=log
)

# Add data quality errors to collector (non-critical - valid records continue)
for dq_error in dq_errors:
    error_collector.add(dq_error, critical=False)

# Continue with valid records
if df_valid.count() > 0:
    process_valid_data(df_valid)

# Store summary in session result
session.result["validation_summary"] = summary

# Check for critical errors
if error_collector.has_critical_errors():
    raise error_collector.critical_errors[0]
```

---

## 📈 Monitoring Quarantine Health

### Query Quarantine Rate

```sql
-- Quarantine rate by entity over time
SELECT 
    DATE(quarantineAt) as quarantine_date,
    quarantineReason,
    COUNT(*) as records_quarantined
FROM quarantine.extractProjects
GROUP BY DATE(quarantineAt), quarantineReason
ORDER BY quarantine_date DESC, records_quarantined DESC;
```

### Dashboard Metrics

```sql
-- Total quarantined by stage
SELECT 
    'source' as stage,
    COUNT(*) as quarantined_count
FROM quarantine.sourceProjects
UNION ALL
SELECT 
    'extract' as stage,
    COUNT(*) as quarantined_count
FROM quarantine.extractProjects
UNION ALL
SELECT 
    'clean' as stage,
    COUNT(*) as quarantined_count
FROM quarantine.cleanProjects;
```

---

## ⚠️ Best Practices

### 1. Start with Error Rules Only
- Begin with critical validation (required fields, data types)
- Add warnings incrementally
- Monitor quarantine rate (aim for <5%)

### 2. Review Quarantine Tables Regularly
- Weekly review of quarantined records
- Identify patterns (same reason recurring)
- Update validation rules if needed

### 3. Handle Quarantined Records
- Option 1: Manual review and re-process
- Option 2: Automated retry after source fix
- Option 3: Accept as invalid and document

### 4. Don't Over-Validate
- Focus on blocking issues (missing required fields, type mismatches)
- Avoid business logic validation in Source/Extract (save for Transform/Refine)
- Use warnings for suspicious but potentially valid data

### 5. Integrate with Activity Log
- Include quarantine summary in `session.result`
- Log quarantine metrics to activity tables
- Alert on high quarantine rates (>10%)

---

## 🎓 Advanced: Custom Validation Rules

### Conditional Validation

```python
# Validate releaseId only if cycleType is "Release"
validation_rules = [
    {
        "name": "missing_release_id_for_release_cycle",
        "condition": lambda df: (
            (F.col("cycleType") == "Release") & 
            F.col("releaseId").isNull()
        ),
        "message": "Release cycles must have releaseId",
        "severity": "error"
    }
]
```

### Multi-Column Validation

```python
# Validate combination of fields
validation_rules = [
    {
        "name": "inconsistent_dates",
        "condition": lambda df: (
            F.col("startDate").isNotNull() &
            F.col("endDate").isNotNull() &
            (F.col("endDate") < F.col("startDate"))
        ),
        "message": "End date cannot be before start date",
        "severity": "error"
    }
]
```

### Reference Data Validation

```python
# Validate against reference data
valid_statuses = ["New", "In Progress", "Completed", "Cancelled"]
validation_rules = [
    {
        "name": "invalid_status",
        "condition": lambda df: ~F.col("status").isin(valid_statuses),
        "message": f"Status must be one of: {', '.join(valid_statuses)}",
        "severity": "error"
    }
]
```

---

## 🔍 Troubleshooting

### Issue: High Quarantine Rate

**Symptom:** >10% of records quarantined

**Diagnosis:**
```sql
SELECT quarantineReason, COUNT(*) as count
FROM quarantine.extractProjects
GROUP BY quarantineReason
ORDER BY count DESC;
```

**Resolution:**
1. Identify most common reason
2. Check if validation rule too strict
3. Verify source data quality
4. Update validation rules if needed

### Issue: Quarantine Table Not Created

**Symptom:** Validation succeeds but no quarantine table

**Diagnosis:**
- Check `quarantine_enabled=True` in function call
- Verify Delta write permissions
- Check schema `quarantine` exists

**Resolution:**
```python
# Ensure quarantine schema exists
spark.sql("CREATE SCHEMA IF NOT EXISTS quarantine")

# Enable quarantine
df_valid, df_invalid, errors, summary = DataQualityHelpers.validate_and_quarantine(
    ...,
    quarantine_enabled=True  # Must be True
)
```

---

## 📚 Related Documentation

- **Design Document:** [`docs/QUARANTINING-SPECTRA-GRADE-DESIGN.md`](QUARANTINING-SPECTRA-GRADE-DESIGN.md)
- **Error Handling:** [`docs/ERROR-HANDLING-FINAL-DESIGN.md`](ERROR-HANDLING-FINAL-DESIGN.md)
- **SDK Documentation:** [`spectraSDK.Notebook`](../spectraSDK.Notebook/)

---

**Last Updated:** 2025-12-08  
**Maintained By:** Data Platform Team

