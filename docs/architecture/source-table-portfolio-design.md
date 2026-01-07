# Source Portfolio Table - Dashboard Design

**Table:** `source.portfolio` (renamed from `source.source`)  
**Purpose:** Multi-source portfolio metadata for SPECTRA source dashboard  
**Version:** 2.0 (Portfolio-focused redesign)

---

## 🎯 Vision

The `source.portfolio` table should be the **single source of truth** for a **SPECTRA Source Portfolio Dashboard** showing:

- All SPECTRA sources (Jira, Zephyr, Xero, UniFi, etc.)
- Their capabilities (endpoint counts, categories, auth methods)
- Health/status metrics
- Discovery metadata
- Operational indicators

**Key Principle:** No duplication of Variable Library data (no credentials, no base URLs). Only metadata and aggregated metrics.

---

## 📊 Schema

```python
Row(
    # Identity
    source_system="zephyr",                    # Key reference (required)
    
    # Contract & Traceability
    contract_version="1.0.0",                  # From contract.yaml
    discovery_date="2025-12-02",              # First catalogued date
    
    # Endpoint Portfolio (aggregated from source.endpoints)
    total_endpoints=228,                       # Total endpoints discovered
    endpoint_categories='{"admin": 11, "projects": 19, ...}',  # JSON aggregation
    hierarchical_endpoints=25,                 # Count of hierarchical endpoints
    
    # Authentication Metadata (NOT credentials)
    auth_method="apiToken",                    # From contract (apiToken|oauth2|basic|pat)
    auth_status="valid",                       # Last health check result (valid|invalid|unknown)
    last_auth_check="2025-12-05T17:13:16Z",   # Timestamp of last successful auth
    
    # Capabilities (from health checks)
    hierarchical_access_validated=True,        # Projects → Releases → Cycles → Executions
    endpoint_success_rate=0.70,                # 84/120 endpoints tested (from contract)
    supports_incremental=False,                # Does API support incremental extraction?
    
    # Operational Status
    status="active",                           # active|inactive|error|maintenance
    is_enabled=True,                           # Can this source be used?
    
    # Audit Trail
    last_updated="2025-12-05T17:13:16Z",      # Last time source table updated
)
```

---

## 🔍 Field Definitions

### Identity Fields

| Field | Type | Source | Purpose |
|-------|------|--------|---------|
| `source_system` | string | Variable Library | Canonical identifier (zephyr, jira, xero, etc.) |
| `contract_version` | string | `contract.yaml` | Version traceability |

### Discovery Metadata

| Field | Type | Source | Purpose |
|-------|------|--------|---------|
| `discovery_date` | date | First Source run | When was this source first catalogued? |
| `total_endpoints` | int | Aggregated from `source.endpoints` | Total endpoints discovered |
| `endpoint_categories` | JSON string | Aggregated from `source.endpoints` | Count by category: `{"admin": 11, "projects": 19, ...}` |
| `hierarchical_endpoints` | int | Aggregated from `source.endpoints` | Count requiring parent IDs |

### Authentication Metadata (NOT Credentials)

| Field | Type | Source | Purpose |
|-------|------|--------|---------|
| `auth_method` | string | `contract.yaml` | Type: `apiToken`, `oauth2`, `basic`, `pat`, `jwt` |
| `auth_status` | string | Health check | Last status: `valid`, `invalid`, `unknown` |
| `last_auth_check` | timestamp | Health check | When was auth last validated? |

### Capabilities

| Field | Type | Source | Purpose |
|-------|------|--------|---------|
| `hierarchical_access_validated` | boolean | Health check | Can we traverse hierarchy? |
| `endpoint_success_rate` | float | Contract/Health check | Percentage of endpoints that work (0.0-1.0) |
| `supports_incremental` | boolean | Contract/Discovery | Does API support incremental extraction? |

### Operational Status

| Field | Type | Source | Purpose |
|-------|------|--------|---------|
| `status` | string | Derived | `active`, `inactive`, `error`, `maintenance` |
| `is_enabled` | boolean | Derived | Can this source be used for extraction? |

### Audit Trail

| Field | Type | Source | Purpose |
|-------|------|--------|---------|
| `last_updated` | timestamp | Runtime | When was this record last updated? |

---

## 📈 Dashboard Use Cases

### 1. **Source Portfolio Overview**

```sql
SELECT 
    source_system,
    total_endpoints,
    endpoint_categories,
    auth_method,
    auth_status,
    status,
    last_updated
FROM source.portfolio
ORDER BY source_system
```

**Shows:** All sources with key metrics at a glance.

### 2. **Health Status Dashboard**

```sql
SELECT 
    source_system,
    auth_status,
    endpoint_success_rate,
    hierarchical_access_validated,
    last_auth_check,
    status
FROM source.portfolio
WHERE status = 'active'
ORDER BY auth_status DESC, last_auth_check DESC
```

**Shows:** Which sources are healthy and ready for extraction.

### 3. **Endpoint Capabilities Comparison**

```sql
SELECT 
    source_system,
    total_endpoints,
    JSON_EXTRACT(endpoint_categories, '$.projects') as project_endpoints,
    JSON_EXTRACT(endpoint_categories, '$.releases') as release_endpoints,
    hierarchical_endpoints
FROM source.portfolio
```

**Shows:** Compare endpoint capabilities across sources.

### 4. **Discovery Timeline**

```sql
SELECT 
    source_system,
    discovery_date,
    total_endpoints,
    last_updated
FROM source.portfolio
ORDER BY discovery_date DESC
```

**Shows:** When sources were discovered and how they've evolved.

---

## 🔄 Implementation

### SDK Function

Uses `SourceStageHelpers.create_source_portfolio_table()` from SDK:

```python
SourceStageHelpers.create_source_portfolio_table(
    spark=spark,
    delta=session.delta,
    logger=log,
    session=session,
    contract_version="1.0.0",
    auth_method="apiToken",
    auth_status=auth_result["status"],
    endpoint_catalog=ENDPOINTS_CATALOG,
    endpoint_success_rate=0.70,
    supports_incremental=False,
)
```

### Front Page Display

The notebook automatically displays a formatted summary after execution, showing:
- Source system identity
- Endpoint portfolio (counts, categories)
- Authentication status
- Capabilities
- Metadata

---

## ✅ Benefits

### 1. **No Duplication**
- ✅ No credentials (in Variable Library)
- ✅ No base URLs (in Variable Library)
- ✅ No workspace/lakehouse IDs (in Fabric runtime)
- ✅ Only metadata and aggregated metrics

### 2. **Dashboard-Ready**
- ✅ Single table for all sources
- ✅ Rich metadata for comparisons
- ✅ Health/status indicators
- ✅ Operational visibility

### 3. **Multi-Source Portfolio**
- ✅ Jira: 100+ endpoints, OAuth2, incremental supported
- ✅ Zephyr: 228 endpoints, apiToken, hierarchical access
- ✅ Xero: TBD endpoints, OAuth2, incremental supported
- ✅ UniFi: TBD endpoints, apiKey, real-time supported

---

## 📋 Migration from `source.source`

The table has been renamed from `source.source` to `source.portfolio` to better reflect its purpose as a portfolio dashboard table.
