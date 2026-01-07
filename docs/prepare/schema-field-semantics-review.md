# Schema Field Semantics Review

## Current Zephyr Schema (7 fields) ✅ WORKING

```python
{
    "entity": "cycle",              # Entity name (e.g., cycle, release, requirement)
    "fieldName": "id",              # Field name within the entity
    "fieldType": "integer",         # Basic type from JSON schema (string, integer, boolean, array, object)
    "isRequired": True,             # From JSON schema "required" array
    "description": "Cycle ID",      # From intelligence notes
    "sourceEndpoint": "/cycle",     # API endpoint that provides this field
    "intelligenceStatus": "working" # API probe status (working, broken, blocked)
}
```

**Purpose:** API discovery - what exists, what works  
**Maturity:** L1 (MVP)  
**Strengths:**
- ✅ Captures API intelligence status (unique to Zephyr)
- ✅ Links fields to source endpoints
- ✅ Simple, works for basic extraction

**Limitations:**
- ❌ Can't handle nested objects (e.g., `cycle.cyclePhases[].id`)
- ❌ No transformation planning (how to flatten/rename)
- ❌ No pipeline stage guidance (which stages need this field)

---

## Jira Schema (22 fields) - MATURE L6

### **Category 1: Organization & Grouping**

```python
"group": "issueIdentifier",      # Logical grouping of related fields
"groupSortOrder": 1,             # Display order of groups
"entitySortOrder": 1,            # Display order of entities within group
"columnOrder": [1],              # Display order in tables/reports (array for nested)
```

**Purpose:** UI organization, documentation structure, consistent field ordering  
**Semantic Question:** Do we need this for Zephyr?
- ✅ **`group`** - Useful for organizing 45+ fields (e.g., "identity", "timestamps", "relationships")
- ✅ **`groupSortOrder`** - Matters for documentation, Power BI reports
- ⚠️ **`entitySortOrder`** - Less critical (we only have 4 entities)
- ⚠️ **`columnOrder`** - Useful for dimensional modeling (L5+)

**Recommendation:** Add `group` and `groupSortOrder` for L2, defer others to L4+

---

### **Category 2: Field Identification**

```python
"fieldId": "issue.id",           # Unique identifier across all entities
```

**Purpose:** Unambiguous field reference across codebase  
**Example:** `cycle.id` vs `release.id` (both have "id", need unique key)

**Semantic Question:** Do we need this?
- ✅ **YES** - Disambiguation in code, logging, errors
- ✅ Format: `{entity}.{fieldName}` (e.g., "cycle.id", "cycle.cyclePhases")

**Recommendation:** Add for L1 (critical for code clarity)

---

### **Category 3: Structure Awareness** 🔥 CRITICAL

```python
"structureType": "scalar",       # scalar | array | object | objectDump
"rawField": ["id"],              # Source path as array (handles nesting)
"targetField": ["id"],           # Target path as array (handles flattening)
"dataType": ["int64"],           # Type array (handles nested objects with multiple types)
```

**Purpose:** Handle complex nested JSON structures  

**Examples:**

**Scalar:**
```python
# API: {"id": 123}
structureType: "scalar"
rawField: ["id"]
targetField: ["id"]
dataType: ["int64"]
```

**Array of Scalars:**
```python
# API: {"releaseIds": [1, 2, 3]}
structureType: "array"
rawField: ["releaseIds"]
targetField: ["releaseIds"]
dataType: ["array<int64>"]
```

**Array of Objects:**
```python
# API: {"cyclePhases": [{"id": 1, "name": "Phase 1"}]}
# FLATTEN to: cycle_phase_ids, cycle_phase_names
structureType: "array"
rawField: ["cyclePhases"]
targetField: ["cyclePhaseIds", "cyclePhaseNames"]  # Flattened
dataType: ["array<int64>", "array<text>"]          # One type per target field
```

**Nested Object:**
```python
# API: {"user": {"id": 123, "name": "Mark"}}
# FLATTEN to: user_id, user_name
structureType: "object"
rawField: ["user"]
targetField: ["userId", "userName"]
dataType: ["int64", "text"]
```

**ObjectDump (Unknown Structure):**
```python
# API: {"metadata": {...unknown...}}
# KEEP as JSON string
structureType: "objectDump"
rawField: ["metadata"]
targetField: ["metadata"]
dataType: ["text"]  # Store as JSON string
```

**Semantic Questions:**
- ✅ **`structureType`** - Absolutely critical for Extract stage
- ✅ **`rawField`** - Must be array to handle nested paths
- ✅ **`targetField`** - Plans flattening/renaming (array handles multiple targets)
- ✅ **`dataType`** - Must be array to match `targetField` (one type per target)

**Key Insight:** Why arrays?
- `rawField: ["cyclePhases"]` → ONE source field
- `targetField: ["cyclePhaseIds", "cyclePhaseNames"]` → TWO target fields (flattened)
- `dataType: ["array<int64>", "array<text>"]` → TWO types (one per target)

**Recommendation:** Add ALL FOUR for L1 (critical for array handling)

---

### **Category 4: Data Lineage**

```python
"isInApiIssue": True,            # Field appears in /issue endpoint
"isInChangelog": False,          # Field appears in /changelog endpoint
"initialDataType": "integer",    # Original type before transformation
```

**Purpose:** Track where fields come from, how they're transformed  

**Zephyr Equivalent:**
```python
"isInApiCycle": True,            # Field appears in /cycle endpoint
"isInApiRelease": False,         # Field appears in /release endpoint (for relationships)
"initialDataType": "array",      # Original type before flattening
```

**Semantic Question:** Do we need multiple `isInApi*` fields?
- ⚠️ **Maybe later** - Zephyr has simpler endpoint structure than Jira
- ✅ **`sourceEndpoint`** already captures this (e.g., "/cycle")
- ✅ **`initialDataType`** - Useful for auditing transformations (L3+)

**Recommendation:** Keep `sourceEndpoint`, add `initialDataType` for L3

---

### **Category 5: Transform Planning**

```python
# Already covered by rawField → targetField above
# Example: ["fields", "status", "name"] → ["status"]
```

**Purpose:** Extract/Clean stages know how to flatten/rename  
**Recommendation:** Covered by `structureType`, `rawField`, `targetField`

---

### **Category 6: Nullability & Defaults**

```python
"isNullable": False,             # Can be null
"defaultValue": None,            # Default value if missing
```

**Purpose:** Data validation, schema enforcement  

**Semantic Question:** Do we need this?
- ⚠️ **`isNullable`** - Jira uses this, but JSON schema has "required" (we have `isRequired`)
- ⚠️ **`defaultValue`** - Useful for Clean stage (L3+)

**Key Difference:**
- `isRequired` = Must be present in API response
- `isNullable` = Can be `null` even if present

**Example:**
```python
# Field can be present but null
isRequired: False  # Can be absent
isNullable: True   # Can be {"name": null}
```

**Recommendation:** Add `isNullable` for L2, `defaultValue` for L3

---

### **Category 7: PII & Privacy** 🔐

```python
"piiLevel": [None],              # None | "email" | "phone" | "name" | "ip"
```

**Purpose:** GDPR compliance, data masking, security  
**Example:** Email fields need masking in dev/test environments

**Semantic Question:** Do we need this for Zephyr?
- ⚠️ **Later (L5+)** - Important for production, not critical for L1-L3
- ✅ Keep in mind for future (test management might have assignee names)

**Recommendation:** Defer to L5

---

### **Category 8: Pipeline Stage Flags**

```python
"isInFactIssue": [True],         # Used in fact_issue table (Refine stage)
"keyField": [True],              # Is a key field (primary/foreign)
```

**Purpose:** Refine stage knows which fields go where  

**Semantic Question:** Do we need this?
- ⚠️ **Later (L4+)** - For dimensional modeling (fact tables, dimensions)
- ✅ Useful pattern, not critical for Extract/Clean

**Recommendation:** Defer to L4

---

### **Category 9: Dimensional Modeling** 📊

```python
"dimensionName": None,           # Maps to dim_user, dim_status, etc.
"bridgeName": None,              # Maps to bridge tables
```

**Purpose:** Analyse stage star schema planning  
**Recommendation:** Defer to L6 (not needed until Analyse stage)

---

### **Category 10: Documentation**

```python
"description": "Issue ID",       # Human-readable description
"notes": "Primary key",          # Additional notes
"type": "system",                # Jira field family (system, custom, etc.)
```

**Purpose:** Documentation, code comments, understanding  

**Zephyr Equivalent:**
```python
"description": "Cycle ID",
"notes": "Primary key. Required for all cycle operations.",
"fieldFamily": "identity"        # identity | timestamp | relationship | metadata
```

**Recommendation:** Keep `description`, add `notes` for L1

---

## Summary: What to Add to Zephyr Schema

### **L1 (MVP) - Must Have Now** 🔥

```python
{
    # Current (keep)
    "entity": "cycle",
    "fieldName": "id",
    "fieldType": "integer",
    "isRequired": True,
    "description": "Cycle ID",
    "sourceEndpoint": "/cycle",
    "intelligenceStatus": "working",
    
    # ADD NOW (L1)
    "fieldId": "cycle.id",          # ← Unique identifier
    "structureType": "scalar",      # ← scalar|array|object|objectDump
    "rawField": ["id"],             # ← Source path (array)
    "targetField": ["id"],          # ← Target path (array)
    "dataType": ["int64"],          # ← Type array (one per target)
    "notes": "Primary key"          # ← Additional context
}
```

**Total: 13 fields for L1**

---

### **L2 (Alpha) - Add Soon**

```python
{
    # Add for organization
    "group": "identity",            # Logical grouping
    "groupSortOrder": 1,            # Group display order
    "isNullable": False,            # Can be null even if present
}
```

**Total: 16 fields for L2**

---

### **L3 (Beta) - Add Later**

```python
{
    # Add for transformation tracking
    "initialDataType": "array",     # Type before transformation
    "defaultValue": None,           # Default if missing
    "columnOrder": [1],             # Display order
}
```

**Total: 19 fields for L3**

---

### **L4-L6 - Much Later**

- `isInFactCycle`, `keyField` (L4)
- `piiLevel` (L5)
- `dimensionName`, `bridgeName` (L6)

---

## Semantic Validation Checklist

**Before implementing, verify:**

1. ✅ **`structureType`** - Does "array" mean array of anything, or just primitives?
   - **Answer:** Array of anything (scalar, object)
   - **Validated:** Jira uses it for both

2. ✅ **`rawField` vs `targetField`** - Why arrays?
   - **Answer:** ONE source field can map to MULTIPLE target fields (flattening)
   - **Example:** `cyclePhases` → `cyclePhaseIds`, `cyclePhaseNames`

3. ✅ **`dataType` array length** - Must match `targetField` length?
   - **Answer:** YES - one type per target field
   - **Example:** `["array<int64>", "array<text>"]` for two targets

4. ✅ **`fieldType` vs `dataType`** - What's the difference?
   - **`fieldType`:** Original JSON schema type (integer, string, array, object)
   - **`dataType`:** Target data types after transformation (int64, text, array<int64>)
   - **Keep both:** `fieldType` for API, `dataType` for pipeline

5. ✅ **`isRequired` vs `isNullable`** - Different?
   - **`isRequired`:** Field must be present in response
   - **`isNullable`:** Field can be `null` even if present
   - **Both needed:** Different concepts

---

## Next Steps

1. **Review semantics** - Does this make sense?
2. **Validate with examples** - Test with `cyclePhases` array
3. **Update intelligence** - Add new fields to `ZephyrIntelligence`
4. **Regenerate SDK** - Embed enhanced schema
5. **Update prepareZephyr** - Use enhanced schema

**Questions to answer before proceeding:**
- Is `structureType` the right name? (vs `fieldStructure`?)
- Should `dataType` be called `targetDataType`? (more explicit?)
- Do we need `fieldFamily` for grouping? (vs `group`?)






