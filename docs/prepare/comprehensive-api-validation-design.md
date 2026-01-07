# Comprehensive API Validation Design

> **Purpose:** Systematic round-trip testing of all Zephyr API endpoints  
> **Status:** 🟡 Proposed  
> **Last Updated:** 2025-12-08

---

## 🎯 Concept

**Round-Trip Testing Pattern:**
1. **GET** (baseline) → Check endpoint returns empty/baseline in test project
2. **POST/PUT** → Create/update test data
3. **GET** (validation) → Retrieve created data
4. **COMPARE** → Validate response matches expectations
5. **CAPTURE** → Document full schema from response

**Scale this to ALL endpoints systematically.**

---

## 📊 Endpoint Categories

### **1. CRUD Endpoints (Core Entities)**

| Entity | GET | POST | PUT | DELETE |
|--------|-----|------|-----|--------|
| Releases | `/release/{projectId}` | `/release` | `/release/{id}` | `/release/{id}` |
| Cycles | `/cycle/{projectId}` | `/cycle` | `/cycle/{id}` | `/cycle/{id}` |
| Testcases | `/testcase/{projectId}` | `/testcase` | `/testcase/{id}` | `/testcase/{id}` |
| Executions | `/execution/{id}` | `/execution` | `/execution/{id}` | `/execution/{id}` |
| Requirements | `/requirement/{id}` | `/requirement` | `/requirement/{id}` | ❌ Broken |
| Folders (Test Repo) | `/testcasetree/{projectId}` | ❌ Broken | `/testcasetree/{id}` | `/testcasetree/{id}` |
| Folders (Requirements) | `/requirementtree/{projectId}` | `/requirementtree/add` | `/requirementtree/{id}` | `/requirementtree/{id}` |

### **2. Specialized Endpoints**

| Operation | Endpoint | Type |
|-----------|----------|------|
| Allocate testcase to requirement | `/allocation` | POST |
| Link testcase to folder | `/testcasetree/{id}/testcase/{testcaseId}` | PUT |
| Clone testcase | `/testcase/{id}/clone` | POST |
| Bulk create | `/testcase/bulk`, `/execution/bulk` | POST |
| Search | `/testcase/search`, `/requirement/search` | POST |

---

## 🔄 Round-Trip Testing Algorithm

### **Phase 1: Baseline Check**

```python
def get_baseline(endpoint, project_id):
    """GET endpoint to establish baseline (should be empty for new test project)."""
    response = requests.get(
        f"{base_url}{endpoint}",
        headers=headers,
        params={"projectId": project_id}
    )
    
    # Document baseline state
    return {
        "endpoint": endpoint,
        "baseline_count": len(response.json()),
        "baseline_data": response.json()
    }
```

### **Phase 2: Create Test Data**

```python
def create_test_entity(endpoint, payload):
    """POST/PUT to create test entity."""
    response = requests.post(
        f"{base_url}{endpoint}",
        headers=headers,
        json=payload
    )
    
    # Capture response
    return {
        "status": response.status_code,
        "created_entity": response.json(),
        "entity_id": response.json().get("id")
    }
```

### **Phase 3: Validate Creation**

```python
def validate_creation(get_endpoint, entity_id):
    """GET entity by ID to validate creation."""
    response = requests.get(
        f"{base_url}{get_endpoint}/{entity_id}",
        headers=headers
    )
    
    # Compare to POST payload
    return {
        "status": response.status_code,
        "retrieved_entity": response.json(),
        "schema": extract_schema(response.json())
    }
```

### **Phase 4: Compare and Document**

```python
def compare_payload_vs_response(post_payload, get_response):
    """Compare what we sent vs what we got back."""
    
    differences = {
        "fields_added_by_api": [],  # Fields API added (id, createdBy, createdOn, etc.)
        "fields_modified_by_api": [],  # Fields API changed (e.g., dates normalized)
        "fields_missing_in_response": [],  # Fields we sent but not returned
        "fields_with_different_types": []  # Type mismatches
    }
    
    # Deep comparison logic
    # ...
    
    return differences
```

---

## 🚀 Implementation Strategy

### **Approach 1: Sequential Entity Testing (Current)**

**What we're doing now:**
- Manually create one entity at a time
- Validate each creation
- Document issues as we find them

**Pros:**
- Careful, methodical
- Good for initial discovery
- Catches blockers early

**Cons:**
- Slow
- Doesn't scale to 228 endpoints

---

### **Approach 2: Systematic Automated Sweep (Proposed)**

**What you're describing:**

```python
def comprehensive_api_validation(endpoints_catalog):
    """
    Systematically test ALL endpoints in catalog.
    """
    
    results = {
        "tested": [],
        "passed": [],
        "failed": [],
        "blocked": [],
        "schemas_captured": {}
    }
    
    # Group endpoints by entity
    entity_groups = group_by_entity(endpoints_catalog)
    
    for entity, endpoints in entity_groups.items():
        print(f"\n🧪 Testing {entity}...")
        
        # 1. Find GET endpoint (list or by ID)
        get_endpoint = find_endpoint(endpoints, method="GET")
        
        # 2. Check baseline (should be empty)
        baseline = get_baseline(get_endpoint, project_id)
        results["tested"].append(f"{entity}.GET.baseline")
        
        # 3. Find POST endpoint
        post_endpoint = find_endpoint(endpoints, method="POST")
        
        # 4. Create test entity
        try:
            created = create_test_entity(post_endpoint, generate_test_payload(entity))
            results["passed"].append(f"{entity}.POST")
            
            # 5. Validate creation via GET
            validated = validate_creation(get_endpoint, created["entity_id"])
            results["passed"].append(f"{entity}.GET.validate")
            
            # 6. Capture schema
            results["schemas_captured"][entity] = validated["schema"]
            
            # 7. Compare payload vs response
            diff = compare_payload_vs_response(
                generate_test_payload(entity), 
                validated["retrieved_entity"]
            )
            results["schemas_captured"][f"{entity}_diff"] = diff
            
        except Exception as e:
            results["failed"].append(f"{entity}: {str(e)}")
    
    return results
```

---

## 📋 Output Artifacts

### **1. Validation Report**

**Location:** `Data/zephyr/validation-reports/api-validation-YYYY-MM-DD.json`

```json
{
  "project": "SpectraTestProject",
  "timestamp": "2025-12-08T10:30:00Z",
  "summary": {
    "total_endpoints": 228,
    "endpoints_tested": 180,
    "endpoints_passed": 150,
    "endpoints_failed": 20,
    "endpoints_blocked": 10,
    "coverage": "78.9%"
  },
  "entity_results": {
    "releases": {
      "GET.baseline": "PASS",
      "POST": "PASS",
      "GET.validate": "PASS",
      "PUT": "PASS",
      "DELETE": "SKIP"
    },
    "requirements": {
      "GET.baseline": "PASS",
      "POST": "FAIL - HTTP 500",
      "GET.validate": "BLOCKED",
      "PUT": "PASS",
      "DELETE": "SKIP"
    }
  },
  "schemas_captured": {
    "release": { /* full schema */ },
    "cycle": { /* full schema */ },
    "testcase": { /* full schema */ }
  }
}
```

### **2. API Coverage Matrix**

**Location:** `Data/zephyr/docs/api-coverage-matrix.md`

| Entity | GET | POST | PUT | DELETE | Coverage | Status |
|--------|-----|------|-----|--------|----------|--------|
| Releases | ✅ | ✅ | ✅ | ⚠️ Skipped | 75% | PASS |
| Cycles | ✅ | ✅ | ✅ | ⚠️ Skipped | 75% | PASS |
| Testcases | ✅ | ✅ | ✅ | ⚠️ Skipped | 75% | PASS |
| Requirements | ✅ | ❌ Broken | ✅ | ⚠️ Skipped | 50% | BLOCKED |
| Folders (Test) | ✅ | ❌ Broken | ✅ | ⚠️ Skipped | 50% | BLOCKED |

### **3. Schema Catalog**

**Location:** `Data/zephyr/schemas/comprehensive-schemas.json`

```json
{
  "release": {
    "fields": {
      "id": {"type": "integer", "source": "api_generated"},
      "name": {"type": "string", "source": "user_provided", "required": true},
      "description": {"type": "string", "source": "user_provided"},
      "startDate": {"type": "date", "source": "user_provided", "format": "YYYY-MM-DD"},
      "createdOn": {"type": "timestamp", "source": "api_generated"},
      "createdBy": {"type": "integer", "source": "api_generated"}
    }
  }
}
```

---

## 🎯 Integration with Prepare Stage

### **Current Prepare Flow:**

1. `prepare.000-discoverFieldMetadata.md` - Discover field metadata
2. `prepare.001-createTestData.md` - Create test data
3. `prepare.002-introspectSchemas.md` - Introspect schemas
4. `prepare.003-loadSchemaIntoNotebook.md` - Load into Fabric

### **Enhanced Flow with Comprehensive Validation:**

1. `prepare.000-discoverFieldMetadata.md` - Discover field metadata
2. **`prepare.001-comprehensiveApiValidation.md`** - **NEW: Systematic round-trip testing**
3. `prepare.002-createEnrichedTestData.md` - Create enriched test data (informed by validation)
4. `prepare.003-introspectSchemas.md` - Introspect schemas (from enriched data)
5. `prepare.004-loadSchemaIntoNotebook.md` - Load into Fabric

---

## ✅ Benefits

1. **Full API Coverage** - Test all 228 endpoints systematically
2. **Early Blocker Detection** - Find broken endpoints before manual testing
3. **Schema Completeness** - Capture schemas for all entities
4. **Validation Confidence** - Know exactly which endpoints work/fail
5. **Automated** - Run as a script, not manual
6. **Repeatable** - Re-run after API updates
7. **Documentation** - Auto-generate coverage reports

---

## 🚧 Implementation Steps

### **Step 1: Create Validation Script**

**Location:** `Data/zephyr/scripts/comprehensive_api_validation.py`

```python
#!/usr/bin/env python
"""
Comprehensive API validation through round-trip testing.
"""

import requests
import json
from pathlib import Path
from datetime import datetime

def main():
    # Load endpoints catalog
    catalog = load_endpoints_catalog()
    
    # Group by entity
    entity_groups = group_by_entity(catalog)
    
    # Run validation
    results = validate_all_entities(entity_groups)
    
    # Generate reports
    generate_validation_report(results)
    generate_coverage_matrix(results)
    generate_schema_catalog(results)
    
    print(f"✅ Validation complete: {results['summary']}")

if __name__ == "__main__":
    main()
```

### **Step 2: Create Playbook**

**Location:** `Core/operations/playbooks/fabric/2-prepare/prepare.001-comprehensive-api-validation.md`

### **Step 3: Run Validation**

```bash
cd Data/zephyr/scripts
python comprehensive_api_validation.py
```

### **Step 4: Review Reports**

- Check `validation-reports/api-validation-YYYY-MM-DD.json`
- Review `docs/api-coverage-matrix.md`
- Inspect `schemas/comprehensive-schemas.json`

### **Step 5: Address Blockers**

- Document failed endpoints in `bug-and-blocker-registry.md`
- Create workarounds for blocked operations
- Update playbooks with known limitations

---

## 🔑 Key Insight

**You're proposing to move from:**
- ❌ Manual, entity-by-entity testing
- ❌ Incomplete coverage
- ❌ Ad-hoc schema discovery

**To:**
- ✅ **Automated, systematic validation**
- ✅ **100% endpoint coverage**
- ✅ **Comprehensive schema capture**
- ✅ **Round-trip verification**

**This is SPECTRA-grade.**

---

## 📊 Next Steps

1. **Create `comprehensive_api_validation.py` script**
2. **Create `prepare.001-comprehensiveApiValidation.md` playbook**
3. **Run validation to generate baseline reports**
4. **Use reports to inform enriched test data creation**
5. **Re-run validation after test data creation to verify**

**This gives us:**
- Full API map
- Known blockers documented
- Validated schemas
- Confidence in coverage

---

**Status:** 🟡 Proposed  
**Blocked By:** None (can start immediately)  
**Depends On:** `source.endpoints` table (already exists)  
**Output:** Validation reports, coverage matrix, schema catalog

