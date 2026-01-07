# Central Logging Service - SPECTRA-Grade Design

**Service:** `monitor` (Observability)  
**Purpose:** Centralized pipeline activity logging and observability  
**Status:** Design Phase

---

## 🎯 The Vision

Instead of writing directly to Delta tables in each notebook, **pipeline activity logs should be sent to a central `monitor` service** that:
- ✅ Collects logs from all pipelines (Jira, Zephyr, Xero, etc.)
- ✅ Provides unified observability dashboard
- ✅ Stores in a central location (Delta Lake, PostgreSQL, or both)
- ✅ Enables cross-pipeline analytics
- ✅ Supports real-time monitoring and alerting

---

## 🏗️ Architecture Options

### Option 1: HTTP API Service (Recommended)

**Service:** `monitor` (Core/labs/monitor)  
**Protocol:** HTTP REST API  
**Storage:** PostgreSQL + Delta Lake (dual-write)

**Flow:**
```
Notebook → SDK → monitor service (HTTP) → PostgreSQL (operational)
                                      → Delta Lake (analytics)
```

**Benefits:**
- ✅ Real-time ingestion
- ✅ Centralized service (all logs in one place)
- ✅ Can add enrichment, validation, alerting
- ✅ Works across all environments (Fabric, Railway, local)
- ✅ Supports webhook notifications

**Drawbacks:**
- ⚠️ Network dependency (needs monitor service running)
- ⚠️ Requires HTTP client in SDK

---

### Option 2: Delta Lake Direct (Current Pattern)

**Storage:** `Tables/log/{stage}log` in each pipeline's lakehouse

**Flow:**
```
Notebook → SDK → Delta Lake (direct write)
              → Future: Sync to central lakehouse
```

**Benefits:**
- ✅ No network dependency
- ✅ Works offline
- ✅ Fast (local write)
- ✅ Fabric-native

**Drawbacks:**
- ❌ Logs scattered across lakehouses
- ❌ Hard to query across pipelines
- ❌ No real-time monitoring

---

### Option 3: Hybrid (Best of Both Worlds) ✨

**Local Write (Immediate):**
- Notebook writes to local Delta table (`Tables/log/{stage}log`)
- Fast, reliable, works offline

**Central Sync (Async):**
- SDK queues log to `monitor` service (async, non-blocking)
- Monitor service aggregates and stores centrally
- If monitor unavailable, logs still stored locally

**Flow:**
```
Notebook → SDK → Delta Lake (local, immediate)
              → monitor service (async, non-blocking)
                  → PostgreSQL (operational)
                  → Central Delta Lake (analytics)
```

**Benefits:**
- ✅ Best of both worlds
- ✅ Resilient (works even if monitor down)
- ✅ Fast local writes
- ✅ Central observability

**Drawbacks:**
- ⚠️ More complex (dual-write pattern)

---

## ✅ Recommended: Option 3 (Hybrid)

### Design: Local Write + Async Central Sync

**Phase 1: Local Delta Write (Now)**
- Notebook logs to local Delta table
- Fast, reliable, works offline
- Enables immediate pipeline debugging

**Phase 2: Async Central Sync (Future)**
- SDK sends log to `monitor` service (async, fire-and-forget)
- Monitor service stores in PostgreSQL + central Delta Lake
- If monitor unavailable, logs still in local Delta

**Phase 3: Central Dashboard (Future)**
- Monitor service provides unified dashboard
- Query across all pipelines
- Real-time monitoring and alerting

---

## 🔧 Implementation Strategy

### SDK Changes (Phase 1)

**Current (Direct Delta Write):**
```python
def record(self):
    # Write to local Delta table
    self.delta.write(df_log, f"log.{stage}log", log_table_path, mode="append")
```

**Future (Hybrid Pattern):**
```python
def record(self):
    # 1. Write to local Delta (immediate, reliable)
    self.delta.write(df_log, f"log.{stage}log", log_table_path, mode="append")
    
    # 2. Send to central service (async, non-blocking)
    try:
        self._send_to_monitor(log_record)  # Fire-and-forget
    except Exception:
        self.log.warning("⚠️ Monitor service unavailable, local log written")
```

**SDK Monitor Client:**
```python
class MonitorClient:
    """Client for sending logs to central monitor service."""
    
    def __init__(self, service_url: str = None):
        self.service_url = service_url or os.getenv("SPECTRA_MONITOR_URL")
        self.enabled = self.service_url is not None
    
    def log_activity(self, log_record: dict) -> None:
        """Send log to monitor service (async, non-blocking)."""
        if not self.enabled:
            return  # Silently skip if monitor not configured
        
        # Fire-and-forget (don't block pipeline)
        threading.Thread(
            target=self._send_async,
            args=(log_record,),
            daemon=True
        ).start()
    
    def _send_async(self, log_record: dict):
        """Actually send log (runs in background thread)."""
        try:
            requests.post(
                f"{self.service_url}/api/v1/logs",
                json=log_record,
                timeout=2,  # Short timeout, don't wait
            )
        except Exception:
            pass  # Silently fail, log already in local Delta
```

---

## 📊 Monitor Service Design

### API Endpoints

**POST /api/v1/logs**
```json
{
  "source_system": "zephyr",
  "stage": "source",
  "notebook_name": "sourceZephyr",
  "workspace_id": "...",
  "lakehouse_id": "...",
  "status": "Success",
  "logged_at": "2025-12-05T10:30:00Z",
  "duration": 45.2,
  "capabilities": ["authVerified", "bootstrapped"],
  "entity_name": null,
  "target_table": null,
  "row_count": null,
  "additional_metadata": {...}
}
```

**GET /api/v1/logs?source_system=zephyr&stage=source**
- Query logs with filters
- Pagination support

**GET /api/v1/metrics?source_system=zephyr**
- Aggregated metrics
- Success rates, durations, etc.

---

### Storage Strategy

**PostgreSQL (Operational):**
- Fast queries
- Real-time dashboard
- Alerting triggers

**Delta Lake (Analytics):**
- Historical analysis
- Cross-pipeline analytics
- ML/BI workloads

**Dual-Write Pattern:**
```
Monitor Service → PostgreSQL (immediate)
              → Delta Lake (batch, every 5 minutes)
```

---

## 🎯 SPECTRA-Grade Requirements

### Must Have:
1. ✅ **Non-Blocking** - Doesn't slow down pipeline
2. ✅ **Resilient** - Works even if monitor unavailable
3. ✅ **Type-Safe** - Full type hints, validated
4. ✅ **Observable** - Can see what's happening
5. ✅ **Reusable** - Works for all pipelines
6. ✅ **Standards Compliant** - Follows SPECTRA patterns

### Implementation Phases:

**Phase 1 (Now):**
- ✅ Local Delta write (current pattern)
- ✅ SDK abstraction (prepare for central service)

**Phase 2 (Next):**
- ⏳ Build `monitor` service
- ⏳ Add async sync to SDK
- ⏳ Test with Zephyr pipeline

**Phase 3 (Future):**
- ⏳ Central dashboard
- ⏳ Alerting rules
- ⏳ Cross-pipeline analytics

---

## 🔄 Migration Path

### Step 1: SDK Abstraction (No Breaking Changes)

**Current Pattern:**
```python
def record(self):
    # Direct Delta write
    self.delta.write(df_log, ...)
```

**Abstracted Pattern:**
```python
def record(self):
    # Abstracted logging (still writes to Delta locally)
    self._log_activity_internal(log_record)
    
def _log_activity_internal(self, log_record: dict):
    """Internal logging method (can be enhanced later)."""
    # Local Delta write (Phase 1)
    self.delta.write(df_log, ...)
    
    # Future: Add async sync (Phase 2)
    # if self.monitor_client:
    #     self.monitor_client.log_activity(log_record)
```

### Step 2: Add Monitor Client (Optional)

**SDK Enhancement:**
```python
class NotebookSession:
    def __init__(self, variable_library_name: str):
        # ... existing init ...
        
        # Monitor client (optional, configured via env var)
        monitor_url = os.getenv("SPECTRA_MONITOR_URL")
        self.monitor_client = MonitorClient(monitor_url) if monitor_url else None
```

**Usage:**
```python
# If SPECTRA_MONITOR_URL set, logs sync to monitor service
# Otherwise, logs only in local Delta (backward compatible)
session.record()  # Works either way
```

---

## 📋 Decision: Hybrid Approach

**Recommendation:** Implement **Option 3 (Hybrid)**

**Rationale:**
1. ✅ **Local Delta write** = Fast, reliable, works offline
2. ✅ **Async central sync** = Unified observability when available
3. ✅ **Non-breaking** = Can add monitor sync later without changing notebooks
4. ✅ **Resilient** = Pipeline works even if monitor down
5. ✅ **SPECTRA-grade** = Best of both worlds

**Implementation:**
- **Phase 1 (Now):** Keep local Delta write, abstract in SDK
- **Phase 2 (Next):** Build monitor service, add async sync
- **Phase 3 (Future):** Central dashboard and analytics

---

## 🚀 Next Steps

1. ✅ Design complete (this document)
2. ⏳ Abstract logging in SDK (prepare for central service)
3. ⏳ Design monitor service API
4. ⏳ Build monitor service (Phase 2)
5. ⏳ Add async sync to SDK (Phase 2)
6. ⏳ Build central dashboard (Phase 3)

