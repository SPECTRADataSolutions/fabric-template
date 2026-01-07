# Config Table Purpose

**Table:** `source.config`  
**Purpose:** Runtime execution context and operational metadata

---

## 📋 Purpose

The `source.config` table stores **runtime execution metadata** that is critical for:
- **Debugging** pipeline vs interactive execution
- **Auditing** how notebooks were executed
- **Troubleshooting** execution context issues
- **Operational visibility** into SPECTRA pipeline runs

---

## 🔍 Current Fields

### `execution_mode`
- **Values:** `"pipeline"` or `"interactive"`
- **Source:** Derived from `session.pipeline.is_active`
- **Purpose:** Track whether notebook ran in automated pipeline or manual execution
- **Use Case:** Distinguish automated runs from ad-hoc testing

### `operation_type`
- **Values:** `"SessionCreation"`, `"ManualRun"`, etc.
- **Source:** `session.pipeline.operation_type`
- **Purpose:** Track the specific type of operation that triggered execution
- **Use Case:** Understand execution trigger (scheduled, manual, test, etc.)

### `last_updated`
- **Values:** UTC timestamp
- **Purpose:** Track when config was last updated
- **Use Case:** Audit trail for config changes

---

## 💡 Why This Table Matters

### 1. **Operational Debugging**
When a pipeline fails, you need to know:
- Was it a scheduled run or manual test?
- What operation type triggered it?
- When did it last execute successfully?

### 2. **Pipeline vs Interactive Behaviour**
Different execution contexts may behave differently:
- Variable Library access may differ
- Authentication may differ
- Performance characteristics may differ

### 3. **Audit Trail**
Track execution patterns:
- How often are pipelines running?
- Are manual runs interfering with scheduled runs?
- What's the typical execution mode?

---

## 🔮 Recommended Enhancements

### Additional Fields to Add:

```python
Row(
    config_key="notebook_name",
    config_value=session.ctx["notebook_name"],
    last_updated=datetime.utcnow(),
),
Row(
    config_key="stage",
    config_value=session.ctx["stage"],
    last_updated=datetime.utcnow(),
),
Row(
    config_key="sdk_version",
    config_value="0.3.0",  # From SDK
    last_updated=datetime.utcnow(),
),
Row(
    config_key="fabric_environment_id",
    config_value=session.environment.environment_id,
    last_updated=datetime.utcnow(),
),
Row(
    config_key="bootstrap_enabled",
    config_value=str(session.params["bootstrap"]),
    last_updated=datetime.utcnow(),
),
Row(
    config_key="preview_enabled",
    config_value=str(session.params["preview"]),
    last_updated=datetime.utcnow(),
),
```

---

## 📊 Example Usage

### Query Execution Context:
```sql
SELECT 
    config_key,
    config_value,
    last_updated
FROM source.config
ORDER BY last_updated DESC
```

**Output:**
```
execution_mode     | pipeline        | 2025-12-05 10:00:00
operation_type     | SessionCreation | 2025-12-05 10:00:00
notebook_name      | sourceZephyr    | 2025-12-05 10:00:00
stage              | source          | 2025-12-05 10:00:00
sdk_version        | 0.3.0           | 2025-12-05 10:00:00
bootstrap_enabled  | False           | 2025-12-05 10:00:00
```

### Check Last Pipeline Run:
```sql
SELECT config_value
FROM source.config
WHERE config_key = 'execution_mode'
  AND config_value = 'pipeline'
ORDER BY last_updated DESC
LIMIT 1
```

---

## ✅ Summary

**Config table is IMPORTANT** - it provides operational visibility into:
- Execution context (pipeline vs interactive)
- Runtime parameters (bootstrap, preview flags)
- System metadata (SDK version, environment)
- Audit trail (last updated timestamps)

**Keep and enhance** - don't remove, just add more context fields!

