# Quarantining - SPECTRA-Grade Design

**Date:** 2025-12-08  
**Status:** 🎯 SPECTRA-Grade Design  
**Purpose:** Define the most SPECTRA-grade way to handle data quality failures and quarantining

---

## 🎯 SPECTRA Principles Applied

1. **Never Drop Data** - Preserve all records, even invalid ones
2. **SDK-First** - Reusable helpers, not notebook-specific code
3. **Modular** - Works across all stages and sources
4. **Type-Safe** - Structured validation rules and errors
5. **Metadata-Driven** - Declarative validation, not imperative code
6. **Audit Trail** - Full observability of what was quarantined and why

---

## 📐 SPECTRA-Grade Architecture

### Core Principle

**Quarantining = Data Quality Failure Handling**

**Philosophy:**
- Operational failures → Error handling (retry, graceful degradation)
- Data quality failures → Quarantining (preserve bad data, continue with good)

**They're complementary, not overlapping!**

---

## 🏗️ SPECTRA-Grade Design

### 1. Validation Rule Definition (Metadata-Driven)

**Declarative, not imperative:**

```python
# Validation rules as metadata (could come from contract, manifest, or defined inline)
validation_rules = [
    {
        "name": "required_field_id",
        "condition": lambda df: F.col("id").isNull(),
        "message": "Missing required field: id",
        "severity": "error",  # or "warning"
        "retryable": False
    },
    {
        "name": "required_field_name",
        "condition": lambda df: F.col("name").isNull(),
        "message": "Missing required field: name",
        "severity": "error",
        "retryable": False
    },
    {
        "name": "future_date_check",
        "condition": lambda df: F.col("createdAt") > F.current_timestamp(),
        "message": "Created date is in the future",
        "severity": "warning",  # Warning - still quarantined but less critical
        "retryable": False
    }
]
```

**SPECTRA-Grade:** Rules are data, not code - can come from contracts, manifests, or config files.

---

### 2. DataQualityHelpers (SDK Helper Class)

**Location:** `spectraSDK.Notebook/notebook_content.py`

**Design Principles:**
- ✅ Generic - works for any entity, any stage
- ✅ Type-safe - returns structured results
- ✅ Integrates with SpectraError
- ✅ Follows SPECTRA naming conventions
- ✅ Modular - single responsibility

```python
class DataQualityHelpers:
    """SPECTRA-grade data quality and quarantine helpers."""
    
    @staticmethod
    def validate_and_quarantine(
        spark: SparkSession,
        delta: "DeltaTable",
        df: DataFrame,
        entity_name: str,
        stage: str,
        validation_rules: List[Dict[str, Any]],
        logger: Optional["SPECTRALogger"] = None,
        quarantine_enabled: bool = True,
    ) -> Tuple[DataFrame, DataFrame, List[SpectraError], Dict[str, Any]]:
        """Validate DataFrame against rules, quarantine invalid records.
        
        SPECTRA-Grade Pattern:
        - Metadata-driven validation (rules are data, not code)
        - Preserves all records (never drops)
        - Returns structured errors (SpectraError instances)
        - Integrates with error handling system
        
        Args:
            spark: Spark session
            delta: DeltaTable helper
            df: Input DataFrame to validate
            entity_name: Entity name (e.g., "projects", "releases")
            stage: Pipeline stage (e.g., "source", "clean")
            validation_rules: List of validation rule dicts
            logger: Logger instance
            quarantine_enabled: Whether to write quarantine table (default: True)
            
        Returns:
            Tuple of:
            - df_valid: Valid records (pass all error rules)
            - df_invalid: Invalid records (fail at least one error rule)
            - errors: List of SpectraError instances for quarantined records
            - summary: Validation summary dict
        """
        from pyspark.sql import functions as F
        from datetime import datetime
        from spectra_core.errors import ValidationError
        
        if df.count() == 0:
            return df, spark.createDataFrame([], df.schema), [], {}
        
        # Build error condition expression
        error_condition = F.lit(False)
        warning_condition = F.lit(False)
        error_reason = F.lit(None).cast("string")
        warning_reason = F.lit(None).cast("string")
        
        error_rules = [r for r in validation_rules if r.get("severity") == "error"]
        warning_rules = [r for r in validation_rules if r.get("severity") == "warning"]
        
        # Build error conditions
        for rule in error_rules:
            condition = rule["condition"](df) if callable(rule["condition"]) else rule["condition"]
            error_condition = error_condition | condition
            error_reason = F.when(
                condition & error_reason.isNull(),
                F.lit(rule["message"])
            ).otherwise(error_reason)
        
        # Build warning conditions (warnings also quarantined but less critical)
        for rule in warning_rules:
            condition = rule["condition"](df) if callable(rule["condition"]) else rule["condition"]
            warning_condition = warning_condition | condition
            warning_reason = F.when(
                condition & warning_reason.isNull(),
                F.lit(rule["message"])
            ).otherwise(warning_reason)
        
        # Combine error and warning conditions (both result in quarantine)
        quarantine_condition = error_condition | warning_condition
        quarantine_reason = F.coalesce(error_reason, warning_reason)
        
        # Add reason columns
        df_with_reasons = df.withColumn("errorReason", error_reason) \
                           .withColumn("warningReason", warning_reason) \
                           .withColumn("quarantineReason", quarantine_reason) \
                           .withColumn("quarantineAt", F.current_timestamp())
        
        # Split valid/invalid
        df_invalid = df_with_reasons.filter(quarantine_condition)
        df_valid = df_with_reasons.filter(~quarantine_condition)
        
        # Remove DQ tracking columns from valid DataFrame (keep clean)
        dq_columns = ["errorReason", "warningReason", "quarantineReason", "quarantineAt"]
        df_valid = df_valid.drop(*[col for col in dq_columns if col in df_valid.columns])
        
        # Create SpectraError instances for quarantined records
        errors = []
        invalid_count = df_invalid.count()
        
        if invalid_count > 0:
            # Group by error reason for summary
            error_summary = df_invalid.groupBy("quarantineReason").count().collect()
            
            for row in error_summary:
                reason = row["quarantineReason"]
                count = row["count"]
                
                error = ValidationError(
                    message=f"{count} {entity_name} records failed validation: {reason}",
                    category="data",
                    context={
                        "entity": entity_name,
                        "stage": stage,
                        "reason": reason,
                        "count": count,
                        "quarantine_table": f"quarantine.{stage}{entity_name.capitalize()}"
                    },
                    retryable=False,
                    stage=stage,
                    source_system=kwargs.get("source_system")
                )
                errors.append(error)
            
            # Quarantine invalid records
            if quarantine_enabled:
                quarantine_table = DataQualityHelpers._write_quarantine_table(
                    spark=spark,
                    delta=delta,
                    df_invalid=df_invalid,
                    entity_name=entity_name,
                    stage=stage,
                    logger=logger
                )
        
        # Validation summary
        valid_count = df_valid.count()
        summary = {
            "entity": entity_name,
            "stage": stage,
            "total_records": df.count(),
            "valid_records": valid_count,
            "quarantined_records": invalid_count,
            "quarantine_rate": invalid_count / df.count() if df.count() > 0 else 0.0,
            "errors": len([e for e in errors if "error" in e.context.get("reason", "").lower()]),
            "warnings": len([e for e in errors if "warning" in e.context.get("reason", "").lower()]),
        }
        
        if logger:
            logger.info(f"📊 Validation: {valid_count} valid, {invalid_count} quarantined {entity_name} records")
        
        return df_valid, df_invalid, errors, summary
    
    @staticmethod
    def _write_quarantine_table(
        spark: SparkSession,
        delta: "DeltaTable",
        df_invalid: DataFrame,
        entity_name: str,
        stage: str,
        logger: Optional["SPECTRALogger"] = None,
    ) -> str:
        """Write invalid records to quarantine table following SPECTRA standard.
        
        SPECTRA Standard:
        - Path: Tables/quarantine/{stage}/{entityName}
        - Table: quarantine.{stage}{EntityName} (camelCase)
        - Mode: append (preserve history)
        - Schema: mergeSchema=true (handle evolution)
        """
        quarantine_path = f"Tables/quarantine/{stage}/{entityName}"
        table_name = f"quarantine.{stage}{entity_name.capitalize()}"  # camelCase
        
        delta.write(
            df_invalid,
            table_name,
            quarantine_path,
            mode="append",
            merge_schema=True
        )
        delta.register(table_name, quarantine_path)
        
        if logger:
            logger.warning(f"⚠️ Quarantined {df_invalid.count()} {entity_name} records to {table_name}")
        
        return table_name
```

---

## 🔧 Integration Pattern

### Source Stage Integration

```python
def execute_source_stage(...):
    """Execute source stage with error handling + quarantining."""
    from spectra_core.errors import ValidationError
    
    error_collector = ErrorCollector()
    request_handler = APIRequestHandler(max_attempts=3, logger=log)
    
    # 1. API call (error handling)
    result, error = request_handler.execute_with_retry(...)
    if error:
        error_collector.add(error, critical=True)
        return
    
    # 2. Parse response
    try:
        df = spark.createDataFrame(result)
    except Exception as e:
        # Parsing error - quarantine raw response
        dfRaw = spark.createDataFrame([{"raw_response": str(result), "parse_error": str(e)}])
        _, _, parse_errors, _ = DataQualityHelpers.validate_and_quarantine(
            spark=spark, delta=session.delta,
            df=dfRaw, entity_name="apiResponse", stage="source",
            validation_rules=[],  # No rules - just quarantine raw response
            logger=log
        )
        error_collector.add(parse_errors[0], critical=True)
        return
    
    # 3. Data quality validation (quarantining)
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
    
    df_valid, df_invalid, dq_errors, summary = DataQualityHelpers.validate_and_quarantine(
        spark=spark, delta=session.delta,
        df=df, entity_name="projects", stage="source",
        validation_rules=validation_rules,
        logger=log
    )
    
    # 4. Add data quality errors to collector
    for dq_error in dq_errors:
        error_collector.add(dq_error, critical=False)  # Non-critical - valid records continue
    
    # 5. Continue with valid records
    if df_valid.count() > 0:
        process_valid_data(df_valid)
    
    # 6. Store summary in session
    session.result["validation_summary"] = summary
```

---

## ✅ SPECTRA-Grade Principles

### 1. Metadata-Driven Validation
- ✅ Rules are data (dict/list), not code
- ✅ Can come from contracts, manifests, or config
- ✅ Reusable across all entities/stages

### 2. Never Drop Data
- ✅ All records preserved (valid → process, invalid → quarantine)
- ✅ Full audit trail (quarantineReason, quarantineAt)
- ✅ Can recover quarantined records later

### 3. SDK-First
- ✅ `DataQualityHelpers` in SDK
- ✅ Reusable across all stages/sources
- ✅ Not notebook-specific

### 4. Integrates with Error Handling
- ✅ Returns `SpectraError` instances
- ✅ Works with `ErrorCollector`
- ✅ Unified error tracking

### 5. Type-Safe & Structured
- ✅ Validation rules have clear structure
- ✅ Returns structured summary
- ✅ Errors are SpectraError instances

### 6. SPECTRA Naming Conventions
- ✅ Table: `quarantine.{stage}{EntityName}` (camelCase)
- ✅ Path: `Tables/quarantine/{stage}/{entityName}`
- ✅ Columns: `quarantineReason`, `quarantineAt` (camelCase)

---

## 📋 SPECTRA Standard Summary

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

### Write Mode
- Always `append` - Preserve history (never overwrite)
- Use `mergeSchema=true` - Handle schema evolution

### Integration
- ✅ Returns `SpectraError` instances
- ✅ Works with `ErrorCollector`
- ✅ Logged to activity tables
- ✅ Summary in session.result

---

## 🎯 Benefits

1. **Reusable** - Same pattern for all stages/sources
2. **Metadata-Driven** - Rules are data, not code
3. **Type-Safe** - Structured validation and errors
4. **Audit Trail** - Full observability
5. **Never Drops Data** - All records preserved
6. **Integrates** - Works with error handling system
7. **SPECTRA-Grade** - Follows all SPECTRA principles

---

**Version:** 1.0.0  
**Date:** 2025-12-08

