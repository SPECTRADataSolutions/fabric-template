# Schema Comparison: Jira vs Zephyr

## Current State

### **Zephyr prepare._schema** (Intelligence-Powered, Basic)
```python
{
    "entity": "release",           # Entity name
    "fieldName": "id",             # Field name
    "fieldType": "integer",        # Data type
    "isRequired": True,            # Required flag
    "description": "Release ID",   # Notes
    "sourceEndpoint": "/release",  # API endpoint
    "intelligenceStatus": "working" # API status
}
```

**Fields:** 7 columns  
**Focus:** API discovery (what exists, what works)  
**Maturity:** L1 (MVP) - Captures basic schema from API Intelligence

---

### **Jira prepare._schema** (Mature, Rich Metadata)
```python
{
    # Organization
    "group": "issueIdentifier",      # Logical grouping
    "groupSortOrder": 1,             # Group display order
    "entity": "issue",               # Entity name
    "entitySortOrder": 1,            # Entity display order
    "fieldId": "issue.id",           # Unique field identifier
    
    # Structure
    "structureType": "scalar",       # scalar|record|array|objectDump
    "rawField": ["id"],              # Source field path (array for nested)
    "targetField": ["id"],           # Target field path (transformed)
    "dataType": ["int64"],           # Data type (array for nested)
    
    # Metadata
    "isInApiIssue": True,            # Appears in API /issue endpoint
    "isInChangelog": False,          # Appears in changelog endpoint
    "isNullable": False,             # Can be null
    "defaultValue": None,            # Default value
    "description": "Issue ID",       # Documentation
    "notes": "Primary key",          # Additional notes
    "initialDataType": "integer",    # Original type before transform
    "type": "system",                # Jira field family
    
    # Pipeline
    "columnOrder": [1],              # Display order in tables
    "piiLevel": [None],              # Privacy classification
    "isInFactIssue": [True],         # Used in fact table
    "keyField": [True],              # Is a key field
    
    # Dimensional Modeling (Analyse stage)
    "dimensionName": None,           # Maps to dimension table
    "bridgeName": None               # Maps to bridge table
}
```

**Fields:** 22 columns  
**Focus:** End-to-end pipeline metadata (Extract → Clean → Transform → Refine → Analyse)  
**Maturity:** L6 (Proactive) - Plans entire pipeline from Prepare stage

---

## Key Differences

### **What Jira Has That Zephyr Doesn't:**

1. **🎯 Grouping & Organization**
   - `group`, `groupSortOrder` - Logical field grouping
   - `entitySortOrder` - Entity display order
   - **Impact:** Better UI, documentation, and code organization

2. **🏗️ Structure Awareness**
   - `structureType` - Knows scalar vs array vs nested object
   - `rawField` / `targetField` - Handles nested fields as arrays
   - **Impact:** Can handle complex nested JSON automatically

3. **📊 Multiple Data Types per Field**
   - `dataType` is an **array** - handles nested objects with multiple types
   - **Example:** `{"user": {"id": 123, "name": "Mark"}}` → `["int64", "text"]`
   - **Impact:** Accurate type handling for nested structures

4. **🔄 Data Lineage**
   - `isInApiIssue`, `isInChangelog` - Tracks where fields appear
   - `initialDataType` - Records original type before transformation
   - **Impact:** Knows which endpoints to call, tracks transformations

5. **🎨 Transform Planning**
   - `rawField` → `targetField` - Plans field renaming/flattening
   - **Example:** `["fields", "status", "name"]` → `["status"]`
   - **Impact:** Extract/Clean stages know how to flatten nested data

6. **🔐 PII & Privacy**
   - `piiLevel` - Marks sensitive data (e.g., email, phone)
   - **Impact:** Compliance, security, masking in non-prod environments

7. **📈 Dimensional Modeling**
   - `dimensionName`, `bridgeName` - Plans Analyse stage star schema
   - `isInFactIssue`, `keyField` - Marks fact vs dimension fields
   - **Impact:** Refine stage knows how to build dimensional model

8. **🎯 Column Ordering**
   - `columnOrder` - Display order in tables/reports
   - **Impact:** Consistent field ordering across all stages

---

## What Zephyr Has That Jira Doesn't:

1. **✅ API Intelligence Status**
   - `intelligenceStatus` - "working", "broken", "blocked"
   - **Impact:** Knows which endpoints work (Jira assumes all work)

2. **✅ Source Endpoint**
   - `sourceEndpoint` - Which API endpoint provides this field
   - **Impact:** Extract stage knows where to get each field

---

## Recommendations for Zephyr

### **Short-term (Keep Current Schema for L1-MVP)**
- ✅ Current schema is perfect for L1 (API discovery phase)
- Focus on getting Extract working with basic schema
- Build momentum and prove the pattern

### **Medium-term (Enhance for L2-L3)**
- Add `structureType` - Handle nested objects/arrays
- Add `rawField`/`targetField` arrays - Plan transformations
- Add `isInApiIssue` - Track which endpoints have which fields

### **Long-term (L4-L6 - Full Jira Parity)**
- Add grouping (`group`, `groupSortOrder`) - Organization
- Add PII tracking (`piiLevel`) - Compliance
- Add dimensional modeling (`dimensionName`, `bridgeName`) - Star schema planning
- Add lineage (`initialDataType`) - Transformation tracking

---

## Schema Evolution Path

```
L1 (Current): Basic API schema
  ↓
L2: Add structure types (scalar/array/object)
  ↓
L3: Add transform planning (rawField → targetField)
  ↓
L4: Add data lineage (initialDataType, isInChangelog)
  ↓
L5: Add PII tracking (piiLevel)
  ↓
L6: Add dimensional modeling (dimensionName, bridgeName)
  ↓
L7: Fully autonomous schema evolution
```

---

## Action: Keep or Evolve?

**Option 1: Keep current schema (Recommended for L1)**
- ✅ Simpler, faster to implement Extract stage
- ✅ Proves intelligence framework works
- ✅ Can enhance later (additive changes)

**Option 2: Enhance to Jira-level now**
- ⚠️ Requires regenerating intelligence
- ⚠️ More complex Extract stage logic
- ✅ Future-proofs for L4+ features

**Recommendation:** Keep current schema, add `structureType` and `rawField`/`targetField` when we hit Extract nested objects.






