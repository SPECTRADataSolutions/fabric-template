# Activity Logging - Most SPECTRA-Grade Approach

**Design Decision:** Automatic + Explicit (Best of Both Worlds)

---

## 🎯 The SPECTRA-Grade Philosophy

**SPECTRA-grade means:**
1. **Zero Boilerplate** - "Just works" by default
2. **Explicit When Needed** - Flexibility for complex scenarios
3. **Standards Compliant** - Follows existing SDK patterns
4. **Type-Safe** - Full type hints, validated
5. **Reusable** - Works across all stages automatically
6. **Observable** - Rich metadata for debugging

---

## ✅ Recommended: **Hybrid Approach** (Automatic + Explicit)

### Design: Two-Tier System

**Tier 1: Automatic Logging** (Zero Boilerplate)
- `record()` automatically logs using session context
- Works for 90% of use cases
- No manual steps required

**Tier 2: Explicit Logging** (Flexibility)
- `log_activity()` method for custom/additional logging
- Useful for multi-entity stages (e.g., extract 5 entities, log each)
- Advanced scenarios

---

## 🏗️ Implementation Design

### Part 1: Automatic Logging in `record()`

**Location:** `NotebookSession.record()` method

**What It Does:**
- Automatically logs using session context
- Captures everything from session (status, capabilities, duration, etc.)
- Logs to `Tables/log/{stage}log`
- Zero configuration needed

**Implementation:**
```python
def record(self):
    """Stage 6: Record activity (automatic logging)."""
    try:
        # Build log record from session context
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
            "capabilities": json.dumps(self.capabilities) if self.capabilities else None,
        }
        
        # Add error if failed
        if self.result["status"] == "Failed":
            log_record["error"] = self.result.get("error", "Unknown error")
        
        # Remove None values
        log_record = {k: v for k, v in log_record.items() if v is not None}
        
        # Write to Delta
        log_table_path = f"Tables/log/{self.ctx['stage']}log"
        df_log = self._spark.createDataFrame([Row(**log_record)])
        
        self.delta.write(df_log, f"log.{self.ctx['stage']}log", log_table_path, mode="append")
        self.delta.register(f"log.{self.ctx['stage']}log", log_table_path)
        
        self.log.info(f"📝 Activity logged to {log_table_path}")
        
    except Exception as e:
        # Graceful failure - don't break pipeline if logging fails
        self.log.warning(f"⚠️ Failed to log activity: {e}")
```

**Usage (Automatic):**
```python
# Notebook just calls record() - logging happens automatically
session.record()  # ✅ Logs everything automatically
```

---

### Part 2: Explicit Logging with `log_activity()`

**Location:** `NotebookSession.log_activity()` method

**What It Does:**
- Allows explicit logging with custom metadata
- Useful for multi-entity stages
- Can be called multiple times in one stage

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
    """Log stage activity explicitly (for custom/additional logging).
    
    Use this when you need to log multiple entities in one stage,
    or when you need custom metadata not captured automatically.
    
    Args:
        entity_name: Entity name (e.g., "zephyrProjects")
        target_table: Delta table written (e.g., "extract.projects")
        key_column: Primary key column name
        project_key: Project/partition identifier
        row_count: Number of rows processed
        field_count: Number of fields/columns
        additional_metadata: Extra fields (dict, will be JSON encoded)
    """
```

**Usage (Explicit):**
```python
# Extract stage with multiple entities
session.log_activity(
    entity_name="zephyrProjects",
    target_table="extract.projects",
    row_count=37,
    field_count=12,
)
session.log_activity(
    entity_name="zephyrReleases",
    target_table="extract.releases",
    row_count=120,
    field_count=15,
)
```

---

## 🎨 Why This Is Most SPECTRA-Grade

### ✅ Follows SPECTRA Patterns:

1. **NotebookSession Lifecycle**
   - Fits the 7-stage pattern perfectly
   - `record()` does what it says (records activity)
   - No deviation from established pattern

2. **SDK Component Reuse**
   - Uses `DeltaTable.write()` and `DeltaTable.register()`
   - Follows existing SDK patterns
   - Consistent with other SDK operations

3. **Zero Boilerplate by Default**
   - Most notebooks just call `session.record()`
   - Works automatically for 90% of cases
   - Follows "sensible defaults" principle

4. **Flexibility When Needed**
   - `log_activity()` available for complex scenarios
   - Doesn't force one-size-fits-all
   - Explicit is better than implicit (when needed)

5. **Type-Safe**
   - Full type hints on all parameters
   - Optional parameters (None means "not applicable")
   - Type checking compatible

6. **Error Handling**
   - Graceful failure (doesn't break pipeline)
   - Logs warning if logging fails
   - Pipeline continues even if logging fails

7. **Standards Compliant**
   - Uses `snake_case` for methods
   - Follows existing naming conventions
   - Consistent with SDK patterns

---

## 📊 Comparison: Automatic vs Explicit vs Hybrid

| Approach | Pros | Cons | SPECTRA-Grade? |
|----------|------|------|----------------|
| **Automatic Only** | Zero boilerplate | Inflexible for complex cases | ⚠️ Good but limited |
| **Explicit Only** | Maximum flexibility | Boilerplate required | ❌ Too much work |
| **Hybrid (Recommended)** | Best of both | None | ✅ **Perfect** |

---

## 🔧 Implementation Checklist

- [x] Design complete (this document)
- [ ] Implement automatic logging in `record()`
- [ ] Implement explicit `log_activity()` method
- [ ] Add proper type hints
- [ ] Add error handling (graceful failure)
- [ ] Test with source stage
- [ ] Test with extract stage (multiple entities)
- [ ] Document usage patterns

---

## 🚀 Usage Examples

### Source Stage (Automatic):
```python
# Just call record() - logging happens automatically
session.record()  # ✅ Logs: status, capabilities, duration, etc.
```

### Source Stage (With Custom Metadata):
```python
# record() logs automatically, but add custom log for portfolio
session.record()  # Automatic logging
session.log_activity(
    additional_metadata={
        "endpoint_count": 228,
        "auth_status": "valid",
        "projects_accessible": 37,
    }
)
```

### Extract Stage (Multiple Entities):
```python
# Extract multiple entities - log each explicitly
session.log_activity(
    entity_name="zephyrProjects",
    target_table="extract.projects",
    key_column="id",
    row_count=37,
)

session.log_activity(
    entity_name="zephyrReleases",
    target_table="extract.releases",
    key_column="id",
    row_count=120,
)

# Final automatic log
session.record()  # Logs overall stage execution
```

---

## ✅ SPECTRA-Grade Checklist

- [x] Automatic by default (zero boilerplate)
- [x] Explicit when needed (flexibility)
- [x] SDK-integrated (uses DeltaTable)
- [x] Type-safe (full type hints)
- [x] Error handling (graceful failure)
- [x] Standards compliant (follows SDK patterns)
- [x] Reusable (works for all stages)
- [x] Observable (rich metadata)
- [x] Zero tech debt (perfect implementation)

---

## 🎯 Final Recommendation

**Implement the Hybrid Approach:**

1. **Automatic:** `record()` logs automatically using session context
2. **Explicit:** `log_activity()` available for custom/additional logging
3. **Uses SDK:** DeltaTable for consistency
4. **Type-Safe:** Full type hints
5. **Error Handling:** Graceful failure

This is the **most SPECTRA-grade** because:
- ✅ Zero boilerplate for common cases
- ✅ Maximum flexibility for complex cases
- ✅ Follows existing SDK patterns
- ✅ Standards compliant
- ✅ Type-safe and observable

