# Error Handling & Quarantining - SPECTRA Standards

**Date:** 2025-12-08  
**Status:** 🎯 SPECTRA Standard Analysis  
**Purpose:** Define how error handling and quarantining work together in SPECTRA

---

## 🎯 Two Complementary Systems

### Error Handling (Operational Failures)
**When:** API/network/operational errors  
**What:** Retry logic, graceful degradation, error classification  
**Where:** Source stage (API calls), any stage (operational failures)  
**Purpose:** Handle transient failures, prevent cascading errors

### Quarantining (Data Quality Failures)
**When:** Data validation/quality checks fail  
**What:** Split valid/invalid records, isolate bad data  
**Where:** Clean/Transform/Refine stages (data processing)  
**Purpose:** Never drop data, preserve bad records for analysis

**They work together but serve different purposes!**

---

## 📐 SPECTRA Quarantine Standard

### From Jira Pipeline Standards

**Standard:** "Never silently drop or ignore error records"

**Pattern:**
1. Split valid/invalid records during data quality checks
2. Write invalid records to quarantine table
3. Log error metadata to error log
4. Continue processing with valid records only

**Path Pattern:** `Tables/quarantine_{stage}_{entityName}`

**Example from Jira:**
```python
# Split valid/invalid
dfInvalid = dfWithReasons.filter(combined_error_condition).withColumn("quarantineAt", F.lit(quarantine_time))
dfValid = dfWithReasons.filter(~combined_error_condition)

# Write quarantine
if writeQuarantine and dfInvalid.count() > 0:
    qp = f"Tables/quarantine_{stage}_{entityName}"
    dfInvalid.write.format("delta").mode("append").option("mergeSchema", "true").save(qp)

# Continue with valid
dfTransformedEntities[ent] = dfValid
```

---

## 🔧 How They Work Together

### Scenario 1: API Error → No Data to Quarantine
```python
# API call fails
result, error = APIRequestHandler.execute_with_retry(...)
if error:
    # Operational error - no data to quarantine
    error_collector.add(error, critical=True)
    # Stage fails, no quarantine needed
```

### Scenario 2: API Success → Data Quality Failure
```python
# API call succeeds
result, error = APIRequestHandler.execute_with_retry(...)
if error is None:
    # Process data
    df = spark.createDataFrame(result)
    
    # Data quality checks
    dfValid, dfInvalid, error_breakdown, warn_breakdown = run_data_quality_checks(df)
    
    # Quarantine invalid records
    if dfInvalid.count() > 0:
        quarantine_path = f"Tables/quarantine_source_{entityName}"
        dfInvalid.write.format("delta").mode("append").save(quarantine_path)
        
        # Create data quality error (not operational)
        dq_error = ValidationError(
            message=f"{dfInvalid.count()} records failed validation",
            category="data",
            context={
                "quarantine_path": quarantine_path,
                "error_breakdown": error_breakdown,
                "entity": entityName
            },
            retryable=False,
            stage="source",
            source_system="zephyr"
        )
        error_collector.add(dq_error, critical=False)  # Non-critical - valid records continue
    
    # Continue with valid records
    process_valid_data(dfValid)
```

### Scenario 3: Partial API Response → Quarantine Partial Data
```python
# API returns partial/invalid response
result, error = APIRequestHandler.execute_with_retry(...)
if error is None:
    # Try to parse response
    try:
        df = spark.createDataFrame(result)
        # Process normally
    except Exception as e:
        # Data parsing error - quarantine raw response
        dfRaw = spark.createDataFrame([{"raw_response": str(result), "parse_error": str(e)}])
        quarantine_path = "Tables/quarantine_source_apiResponse"
        dfRaw.write.format("delta").mode("append").save(quarantine_path)
        
        # Create validation error
        parse_error = ValidationError(
            message=f"Failed to parse API response: {str(e)}",
            category="data",
            context={"quarantine_path": quarantine_path},
            retryable=False
        )
        error_collector.add(parse_error, critical=True)
```

---

## 🏗️ SPECTRA-Grade Quarantine Helper

### New SDK Helper Class

```python
class DataQualityHelpers:
    """SPECTRA-grade data quality and quarantine helpers."""
    
    @staticmethod
    def quarantine_invalid_records(
        spark: SparkSession,
        delta: "DeltaTable",
        df_invalid: DataFrame,
        entity_name: str,
        stage: str,
        error_reason_column: str = "errorReason",
        logger: Optional["SPECTRALogger"] = None,
    ) -> str:
        """Quarantine invalid records following SPECTRA standard.
        
        Args:
            spark: Spark session
            delta: DeltaTable helper
            df_invalid: DataFrame with invalid records
            entity_name: Entity name (e.g., "projects", "releases")
            stage: Pipeline stage (e.g., "source", "clean", "transform")
            error_reason_column: Column name containing error reason
            logger: Logger instance
            
        Returns:
            Quarantine table path
        """
        if df_invalid.count() == 0:
            return None
        
        from pyspark.sql.functions import current_timestamp, lit
        from datetime import datetime
        
        # Ensure quarantineAt column exists
        if "quarantineAt" not in df_invalid.columns:
            df_invalid = df_invalid.withColumn("quarantineAt", current_timestamp())
        
        # Quarantine path: Tables/quarantine_{stage}_{entityName}
        quarantine_path = f"Tables/quarantine/{stage}/{entityName}"
        table_name = f"quarantine.{stage}{entity_name.capitalize()}"
        
        # Write to quarantine (append - preserve history)
        delta.write(
            df_invalid,
            table_name,
            quarantine_path,
            mode="append"
        )
        delta.register(table_name, quarantine_path)
        
        if logger:
            logger.warning(f"⚠️ Quarantined {df_invalid.count()} invalid {entity_name} records to {table_name}")
        
        return table_name
    
    @staticmethod
    def run_data_quality_checks(
        df: DataFrame,
        validation_rules: List[Dict[str, Any]],
        entity_name: str,
        logger: Optional["SPECTRALogger"] = None,
    ) -> Tuple[DataFrame, DataFrame, Dict[str, Any]]:
        """Run data quality checks and split valid/invalid records.
        
        Args:
            df: Input DataFrame
            validation_rules: List of validation rules
            entity_name: Entity name
            logger: Logger instance
            
        Returns:
            Tuple of (df_valid, df_invalid, error_breakdown)
        """
        from pyspark.sql import functions as F
        
        # Build error condition expression
        error_condition = F.lit(False)
        error_reason = F.lit(None).cast("string")
        
        for rule in validation_rules:
            rule_condition = rule["condition"]
            rule_message = rule.get("message", rule.get("name", "Validation failed"))
            
            error_condition = error_condition | rule_condition
            error_reason = F.when(
                rule_condition & error_reason.isNull(),
                F.lit(rule_message)
            ).otherwise(error_reason)
        
        # Add error reason column
        df_with_reasons = df.withColumn("errorReason", error_reason)
        
        # Split valid/invalid
        df_invalid = df_with_reasons.filter(error_condition)
        df_valid = df_with_reasons.filter(~error_condition)
        
        # Error breakdown
        error_breakdown = {}
        for rule in validation_rules:
            count = df_with_reasons.filter(rule["condition"]).count()
            error_breakdown[rule.get("name", "unknown")] = {
                "count": int(count),
                "message": rule.get("message", "")
            }
        
        if logger:
            invalid_count = df_invalid.count()
            valid_count = df_valid.count()
            logger.info(f"📊 Data quality check: {valid_count} valid, {invalid_count} invalid records")
        
        return df_valid, df_invalid, error_breakdown
```

---

## 📊 Integration Pattern

### Source Stage with Error Handling + Quarantining

```python
def execute_source_stage(...):
    """Execute source stage with error handling and quarantining."""
    error_collector = ErrorCollector()
    request_handler = APIRequestHandler(max_attempts=3, logger=log)
    
    # 1. API call with retry (error handling)
    result, error = request_handler.execute_with_retry(
        lambda: _call_api(...),
        context={"endpoint": "/projects"},
        service="Zephyr API"
    )
    
    if error:
        error_collector.add(error, critical=True)
        return  # Can't continue without data
    
    # 2. Parse response
    try:
        df = spark.createDataFrame(result)
    except Exception as e:
        # Parsing error - quarantine raw response
        dfRaw = spark.createDataFrame([{"raw_response": str(result), "error": str(e)}])
        DataQualityHelpers.quarantine_invalid_records(
            spark=spark, delta=session.delta,
            df_invalid=dfRaw, entity_name="apiResponse", stage="source", logger=log
        )
        
        parse_error = ValidationError(
            message=f"Failed to parse API response: {str(e)}",
            category="data",
            context={"quarantine_path": "Tables/quarantine/source/apiResponse"},
            retryable=False
        )
        error_collector.add(parse_error, critical=True)
        return
    
    # 3. Data quality checks (quarantining)
    validation_rules = [
        {"name": "missing_id", "condition": F.col("id").isNull(), "message": "Missing required field: id"},
        {"name": "invalid_format", "condition": F.col("name").isNull(), "message": "Missing required field: name"}
    ]
    
    df_valid, df_invalid, error_breakdown = DataQualityHelpers.run_data_quality_checks(
        df=df, validation_rules=validation_rules, entity_name="projects", logger=log
    )
    
    # 4. Quarantine invalid records
    if df_invalid.count() > 0:
        DataQualityHelpers.quarantine_invalid_records(
            spark=spark, delta=session.delta,
            df_invalid=df_invalid, entity_name="projects", stage="source", logger=log
        )
        
        dq_error = ValidationError(
            message=f"{df_invalid.count()} projects failed validation",
            category="data",
            context={"error_breakdown": error_breakdown},
            retryable=False
        )
        error_collector.add(dq_error, critical=False)  # Non-critical
    
    # 5. Continue with valid records
    process_valid_data(df_valid)
```

---

## ✅ SPECTRA Standard: Error Handling + Quarantining

### When to Use Error Handling
- ✅ API/network failures (timeout, connection error)
- ✅ Authentication/authorization failures
- ✅ Service unavailable (5xx errors)
- ✅ Operational errors (configuration, missing resources)

### When to Use Quarantining
- ✅ Data validation failures (missing required fields, invalid formats)
- ✅ Schema mismatches (unexpected columns, wrong types)
- ✅ Business rule violations (invalid values, constraint failures)
- ✅ Data quality issues (nulls in required fields, duplicates)

### They Work Together When:
- ✅ API succeeds but returns invalid data → Quarantine + ValidationError
- ✅ Partial API response → Quarantine partial + Operational error
- ✅ Data processing fails after API success → Quarantine + ValidationError

---

## 📋 SPECTRA Quarantine Standard

### Path Convention
```
Tables/quarantine/{stage}/{entityName}
```

**Examples:**
- `Tables/quarantine/source/projects`
- `Tables/quarantine/clean/jiraIssues`
- `Tables/quarantine/transform/releases`

### Table Naming
```
quarantine.{stage}{EntityName}
```

**Examples:**
- `quarantine.sourceProjects`
- `quarantine.cleanJiraIssues`
- `quarantine.transformReleases`

### Required Columns
- `errorReason` - Why record was quarantined
- `quarantineAt` - Timestamp when quarantined
- All original data columns (preserve full record)

### Write Mode
- Always `append` - Preserve history
- Use `mergeSchema=true` - Handle schema evolution

---

## 🎯 Recommendation

**Yes, error handling and quarantining go hand-in-hand!**

1. **Error Handling** - Operational failures (API, network, auth)
2. **Quarantining** - Data quality failures (validation, schema, business rules)
3. **Integration** - Use both: handle errors, quarantine bad data
4. **SPECTRA Standard** - Follow existing Jira pattern for consistency

---

**Version:** 1.0.0  
**Date:** 2025-12-08

