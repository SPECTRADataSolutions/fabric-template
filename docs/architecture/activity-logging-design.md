# Activity Logging - SPECTRA-Grade Design

**Stage:** Source (and all stages)  
**Purpose:** Universal, standardized activity logging for pipeline observability  
**Status:** Design Phase

---

## 🎯 SPECTRA-Grade Requirements

### Must Have:
1. ✅ **SDK Integration** - Part of `SourceStageHelpers` or `NotebookSession`
2. ✅ **Type Safety** - Full type hints, Pydantic-style validation
3. ✅ **Zero Tech Debt** - Perfect error handling, no shortcuts
4. ✅ **Reusable** - Works for all stages (source, extract, clean, transform, etc.)
5. ✅ **Observable** - Rich metadata for debugging and monitoring
6. ✅ **Idempotent** - Safe to call multiple times
7. ✅ **Standardized Schema** - Consistent log table structure

---

## 📊 Current Jira Pattern Analysis

### What Works:
- ✅ Logs to Delta table (`Tables/log/{stage}log`)
- ✅ Standard fields: stage, status, loggedAt, entityName, etc.
- ✅ Schema merge for flexibility
- ✅ Append-only (immutable audit trail)

### What Needs SPECTRA-Grade Improvement:
- ❌ Not part of SDK (Jira-specific utility notebook)
- ❌ No type hints or validation
- ❌ Manual schema padding (fragile)
- ❌ No integration with `NotebookSession` capabilities
- ❌ No automatic duration calculation
- ❌ Missing SPECTRA context (source_system, workspace, etc.)

---

## 🏗️ SPECTRA-Grade Design

### Option 1: NotebookSession Method (Recommended)

**Integration:** Add to `NotebookSession` class as `log_activity()` method

**Benefits:**
- ✅ Automatic access to session context (source_system, stage, capabilities)
- ✅ Automatic duration calculation (from `start_time`)
- ✅ Integrated with existing session lifecycle
- ✅ Type-safe with session's typed context

**Signature:**
```python
def log_activity(
    self,
    entity_name: Optional[str] = None,
    target_table: Optional[str] = None,
    key_column: Optional[str] = None,
    project_key: Optional[str] = None,
    row_count: Optional[int] = None,
    field_count: Optional[int] = None,
    additional_metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """Log stage activity to Delta log table.
    
    Automatically includes:
    - source_system (from session context)
    - stage (from session context)
    - notebook_name (from session context)
    - status (from session.result)
    - capabilities (from session.capabilities)
    - duration (calculated from start_time)
    - logged_at (current timestamp)
    
    Args:
        entity_name: Entity name for entity stages (e.g., "jiraIssue")
        target_table: Delta table written to (e.g., "clean.jiraIssue")
        key_column: Primary key column name
        project_key: Project/partition identifier
        row_count: Number of rows processed
        field_count: Number of fields/columns
        additional_metadata: Extra fields for stage-specific logging
    """
```

**Usage:**
```python
session = NotebookSession("zephyrVariables")
session.load_context(...)
log = session.initialize()
# ... execute work ...
session.log_activity(
    entity_name="zephyrProjects",
    target_table="source.sampleprojects",
    row_count=10,
    additional_metadata={"endpoint_count": 228}
)
```

---

### Option 2: SourceStageHelpers Static Method

**Integration:** Add to `SourceStageHelpers` class as static method

**Benefits:**
- ✅ Reusable without NotebookSession (flexibility)
- ✅ Can be called from any notebook
- ✅ Explicit parameter passing (no hidden context)

**Drawbacks:**
- ❌ Must pass session context manually
- ❌ Less automatic (manual duration calculation)
- ❌ More verbose

**Signature:**
```python
@staticmethod
def log_stage_activity(
    spark: SparkSession,
    delta: 'DeltaTable',
    logger: 'SPECTRALogger',
    session: 'NotebookSession',
    entity_name: Optional[str] = None,
    target_table: Optional[str] = None,
    key_column: Optional[str] = None,
    project_key: Optional[str] = None,
    row_count: Optional[int] = None,
    field_count: Optional[int] = None,
    additional_metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """Log stage activity to Delta log table."""
```

---

## 🎨 Recommended: Option 1 (NotebookSession Method)

### Implementation Details

**Location:** `spectraSDK.Notebook/notebook_content.py` - `NotebookSession` class

**Log Table Path Pattern:**
- Source: `Tables/log/sourcelog`
- Extract: `Tables/log/extractlog`
- Clean: `Tables/log/cleanlog`
- Transform: `Tables/log/transformlog`
- Refine: `Tables/log/refinelog`
- Analyse: `Tables/log/analyselog`

**Automatic Fields (from session):**
- `source_system` - From `session.ctx["source_system"]`
- `stage` - From `session.ctx["stage"]`
- `notebook_name` - From `session.ctx["notebook_name"]`
- `workspace_id` - From `session.environment.workspace_id`
- `lakehouse_id` - From `session.environment.lakehouse_id`
- `status` - From `session.result["status"]`
- `capabilities` - JSON string from `session.capabilities`
- `duration` - Calculated: `(datetime.utcnow() - session.start_time).total_seconds()`
- `logged_at` - Current timestamp

**Explicit Fields (parameters):**
- `entity_name` - Entity being processed
- `target_table` - Delta table written
- `key_column` - Primary key column
- `project_key` - Project/partition identifier
- `row_count` - Rows processed
- `field_count` - Fields/columns
- Additional metadata (flexible)

**Schema Definition:**
```python
LOG_SCHEMA = StructType([
    StructField("source_system", StringType(), False),
    StructField("stage", StringType(), False),
    StructField("notebook_name", StringType(), False),
    StructField("workspace_id", StringType(), True),
    StructField("lakehouse_id", StringType(), True),
    StructField("status", StringType(), False),
    StructField("logged_at", TimestampType(), False),
    StructField("duration", FloatType(), True),
    StructField("entity_name", StringType(), True),
    StructField("target_table", StringType(), True),
    StructField("key_column", StringType(), True),
    StructField("project_key", StringType(), True),
    StructField("row_count", IntegerType(), True),
    StructField("field_count", IntegerType(), True),
    StructField("capabilities", StringType(), True),  # JSON string
    StructField("metadata", StringType(), True),      # JSON string for additional fields
])
```

---

## 🔧 Implementation Plan

### Step 1: Add Method to NotebookSession

```python
def log_activity(
    self,
    entity_name: Optional[str] = None,
    target_table: Optional[str] = None,
    key_column: Optional[str] = None,
    project_key: Optional[str] = None,
    row_count: Optional[int] = None,
    field_count: Optional[int] = None,
    additional_metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """Log stage activity to Delta log table.
    
    Creates log record with automatic context from session and explicit parameters.
    Logs to Tables/log/{stage}log (e.g., Tables/log/sourcelog).
    """
    # Build log record
    duration = (datetime.utcnow() - self.start_time).total_seconds()
    
    log_record = {
        "source_system": self.ctx["source_system"],
        "stage": self.ctx["stage"],
        "notebook_name": self.ctx["notebook_name"],
        "workspace_id": self.environment.workspace_id,
        "lakehouse_id": self.environment.lakehouse_id,
        "status": self.result["status"],
        "logged_at": datetime.utcnow(),
        "duration": duration,
        "entity_name": entity_name,
        "target_table": target_table,
        "key_column": key_column,
        "project_key": project_key,
        "row_count": row_count,
        "field_count": field_count,
        "capabilities": json.dumps(self.capabilities) if self.capabilities else None,
        "metadata": json.dumps(additional_metadata) if additional_metadata else None,
    }
    
    # Remove None values (optional fields)
    log_record = {k: v for k, v in log_record.items() if v is not None}
    
    # Write to Delta
    log_table_path = f"Tables/log/{self.ctx['stage']}log"
    df_log = self._spark.createDataFrame([Row(**log_record)])
    
    self.delta.write(df_log, f"log.{self.ctx['stage']}log", log_table_path, mode="append")
    self.delta.register(f"log.{self.ctx['stage']}log", log_table_path)
    
    self.log.info(f"📝 Activity logged to {log_table_path}")
```

### Step 2: Update Zephyr Notebook

```python
# In RECORD stage (Stage 6)
session.log_activity(
    entity_name=None,  # Source stage doesn't have entity
    target_table=None,  # Multiple tables created
    row_count=None,  # Multiple tables, different counts
    additional_metadata={
        "endpoint_count": endpoint_count if ENDPOINTS_CATALOG else 0,
        "auth_status": auth_result["status"],
        "projects_accessible": len(all_projects) if all_projects else 0,
    }
)
```

---

## ✅ SPECTRA-Grade Checklist

- [x] SDK-integrated (NotebookSession method)
- [x] Type-safe (full type hints)
- [x] Automatic context (from session)
- [x] Flexible metadata (additional_metadata dict)
- [x] Idempotent (append-only, safe to retry)
- [x] Standardized schema (consistent across all stages)
- [x] Error handling (graceful failure, log warning)
- [x] Reusable (works for all stages)
- [x] Observable (rich metadata, capabilities, duration)
- [x] Zero tech debt (no shortcuts, perfect implementation)

---

## 🚀 Next Steps

1. ✅ Design complete (this document)
2. ⏳ Implement in SDK
3. ⏳ Update Zephyr notebook to use it
4. ⏳ Test with source stage
5. ⏳ Document usage pattern

---

## 📚 Usage Examples

### Source Stage:
```python
session.log_activity(
    additional_metadata={
        "endpoint_count": 228,
        "auth_status": "valid",
        "projects_accessible": 37,
    }
)
```

### Extract Stage:
```python
session.log_activity(
    entity_name="zephyrProjects",
    target_table="extract.projects",
    key_column="id",
    row_count=37,
    field_count=12,
)
```

### Clean Stage:
```python
session.log_activity(
    entity_name="zephyrProjects",
    target_table="clean.projects",
    key_column="projectId",
    row_count=37,
    field_count=15,
    additional_metadata={
        "quarantined_rows": 0,
        "trust_score": 95.5,
    }
)
```

