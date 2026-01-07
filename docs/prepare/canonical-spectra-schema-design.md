# Canonical SPECTRA Schema Design

**Purpose:** Define the standard schema structure for ALL SPECTRA pipelines (Jira, Zephyr, Xero, UniFi, etc.)

---

## Complete Field Catalog from Jira

### **Category 1: Entity Organization**

#### **1. `group` (StringType, NOT NULL)**
```python
"group": "issueIdentifier"
```
**What it does:** Logical grouping of related fields for documentation/UI  
**Examples:** "issueIdentifier", "timestamps", "relationships", "metadata"  
**Used by:** Documentation generation, Power BI report organization  
**Jira usage:** Groups ~150 fields into ~15 logical categories  
**Zephyr need:** Would help organize 45+ fields  
**Recommendation:** ✅ **INCLUDE in canonical** - Useful for all pipelines with 20+ fields

---

#### **2. `groupSortOrder` (IntegerType, NOT NULL)**
```python
"groupSortOrder": 1
```
**What it does:** Display order of groups  
**Examples:** 1 = Identity first, 2 = Timestamps second, etc.  
**Used by:** Report generation, documentation structure  
**Jira usage:** Ensures consistent field ordering across stages  
**Zephyr need:** Moderate - helps with documentation  
**Recommendation:** ✅ **INCLUDE in canonical** - Low cost, high consistency value

---

#### **3. `entity` (StringType, NOT NULL)**
```python
"entity": "issue"
```
**What it does:** Entity/table name this field belongs to  
**Examples:** "issue", "user", "project", "cycle", "release"  
**Used by:** ALL stages - routing, table creation, code generation  
**Jira usage:** Critical - identifies which table to write to  
**Zephyr need:** Critical  
**Recommendation:** ✅ **INCLUDE in canonical** - MANDATORY

---

#### **4. `entitySortOrder` (IntegerType, NOT NULL)**
```python
"entitySortOrder": 1
```
**What it does:** Display order of entities within a group  
**Examples:** 1 = Main entity first, 2 = Related entities  
**Used by:** Report generation  
**Jira usage:** Minor - mostly for UI  
**Zephyr need:** Low - only 4 entities  
**Recommendation:** ⚠️ **OPTIONAL in canonical** - Defer to pipelines with 10+ entities

---

#### **5. `fieldId` (StringType, NOT NULL)**
```python
"fieldId": "issue.id"
```
**What it does:** Unique identifier for this field across the entire system  
**Format:** `{entity}.{fieldName}` or nested like `issue.fields.status.name`  
**Examples:** "issue.id", "user.emailAddress", "cycle.cyclePhases"  
**Used by:** Code references, logging, error messages, disambiguation  
**Jira usage:** Critical - prevents ambiguity (multiple entities have "id")  
**Zephyr need:** Critical  
**Recommendation:** ✅ **INCLUDE in canonical** - MANDATORY (prevents ambiguity)

---

### **Category 2: Structure & Transformation**

#### **6. `structureType` (StringType, NOT NULL)**
```python
"structureType": "scalar" | "array" | "object" | "objectDump"
```
**What it does:** Defines the structural complexity of the field  
**Values:**
- `scalar` - Single primitive value (id, name, date)
- `array` - Array of values (primitives or objects)
- `object` - Nested object that should be flattened
- `objectDump` - Unknown/complex structure → keep as JSON string

**Examples:**
```python
# Scalar
{"id": 123} → structureType: "scalar"

# Array of primitives
{"tags": ["urgent", "bug"]} → structureType: "array"

# Array of objects
{"assignees": [{"id": 1, "name": "Mark"}]} → structureType: "array"

# Nested object
{"user": {"id": 123, "name": "Mark"}} → structureType: "object"

# Unknown structure
{"customData": {...anything...}} → structureType: "objectDump"
```

**Used by:** Extract (field promotion), Clean (flattening), Transform (normalization)  
**Jira usage:** Critical - drives extraction logic for 50+ nested fields  
**Zephyr need:** Critical - cyclePhases is array of objects  
**Recommendation:** ✅ **INCLUDE in canonical** - MANDATORY for nested data

---

#### **7. `rawField` (ArrayType(StringType), NOT NULL)**
```python
"rawField": ["fields", "status", "name"]
```
**What it does:** Path to the field in the raw API response (array = nested path)  
**Why array?** Handles nested JSON navigation  
**Examples:**
```python
# Top-level field
{"id": 123} → rawField: ["id"]

# Nested field
{"fields": {"status": {"name": "Done"}}} → rawField: ["fields", "status", "name"]

# Array element property
{"assignees": [{"id": 1}]} → rawField: ["assignees", "id"]
```

**Used by:** Extract stage - knows how to navigate JSON  
**Jira usage:** Critical - Jira API deeply nested (3-4 levels common)  
**Zephyr need:** Critical - cyclePhases is array  
**Recommendation:** ✅ **INCLUDE in canonical** - MANDATORY for nested APIs

---

#### **8. `targetField` (ArrayType(StringType), NOT NULL)**
```python
"targetField": ["status"]
```
**What it does:** Field name(s) after transformation/flattening (array = multiple outputs)  
**Why array?** ONE source field can map to MULTIPLE target fields  
**Examples:**
```python
# Simple mapping (1:1)
rawField: ["id"] → targetField: ["id"]

# Flattening (1:1 with rename)
rawField: ["fields", "status", "name"] → targetField: ["status"]

# Exploding array of objects (1:many)
rawField: ["assignees"] → targetField: ["assigneeIds", "assigneeNames"]
# FROM: [{"id": 1, "name": "Mark"}, {"id": 2, "name": "John"}]
# TO: assigneeIds: [1, 2], assigneeNames: ["Mark", "John"]
```

**Used by:** Extract (field naming), Clean (flattening), Transform (mapping)  
**Jira usage:** Critical - 40% of fields are flattened/renamed  
**Zephyr need:** Critical - cyclePhases needs flattening  
**Recommendation:** ✅ **INCLUDE in canonical** - MANDATORY for transformation planning

---

#### **9. `dataType` (ArrayType(StringType), NOT NULL)**
```python
"dataType": ["int64"]
```
**What it does:** Target data type(s) after transformation (array matches `targetField` length)  
**Why array?** One type per target field (when exploding objects)  
**Values:** `int64`, `float64`, `text`, `boolean`, `date`, `timestamp`, `array<type>`  
**Examples:**
```python
# Scalar (1 target = 1 type)
targetField: ["id"] → dataType: ["int64"]

# Flattening (1 target = 1 type)
targetField: ["status"] → dataType: ["text"]

# Exploding (2 targets = 2 types)
targetField: ["assigneeIds", "assigneeNames"] 
dataType: ["array<int64>", "array<text>"]
```

**Used by:** Extract (type casting), Clean (validation), Refine (schema definition)  
**Jira usage:** Critical - ensures correct Delta table schemas  
**Zephyr need:** Critical - prevents type errors in Extract  
**Recommendation:** ✅ **INCLUDE in canonical** - MANDATORY (must match targetField length)

---

### **Category 3: API Source Metadata**

#### **10. `isInApiIssue` (BooleanType, NULLABLE)**
```python
"isInApiIssue": True
```
**What it does:** Field appears in the main API endpoint (e.g., /issue, /cycle)  
**Examples:** `id`, `name`, `createdDate` = True; derived fields = False  
**Used by:** Extract stage - knows which endpoint to call  
**Jira usage:** Moderate - Jira has 3 endpoints per entity (/issue, /changelog, /comments)  
**Zephyr need:** Low - Zephyr has simpler endpoint structure  
**Jira-specific?** Yes - Jira has multiple endpoints per entity  
**Recommendation:** ⚠️ **OPTIONAL in canonical** - Replace with generic `sourceEndpoint` field

---

#### **11. `isInChangelog` (BooleanType, NULLABLE)**
```python
"isInChangelog": False
```
**What it does:** Field appears in changelog endpoint (history tracking)  
**Jira usage:** Moderate - tracks historical changes to fields  
**Zephyr need:** None - no changelog endpoint  
**Jira-specific?** Yes  
**Recommendation:** ❌ **EXCLUDE from canonical** - Too specific to Jira

---

### **Category 4: Data Quality & Validation**

#### **12. `isNullable` (BooleanType, NULLABLE)**
```python
"isNullable": False
```
**What it does:** Field can be `null` even if present in response  
**Difference from `isRequired`:**
- `isRequired`: Field must be in the response
- `isNullable`: Field can be `null` if present

**Examples:**
```python
# Required and not nullable
{"id": 123} ✅
{"id": null} ❌
{} ❌

# Required but nullable
{"description": "text"} ✅
{"description": null} ✅
{} ❌

# Optional and nullable
{"optional": "text"} ✅
{"optional": null} ✅
{} ✅
```

**Used by:** Clean stage - validation logic, schema enforcement  
**Jira usage:** Moderate - 30% of fields are nullable  
**Zephyr need:** Moderate - API returns nulls for some fields  
**Recommendation:** ✅ **INCLUDE in canonical** - Important for data quality

---

#### **13. `defaultValue` (StringType, NULLABLE)**
```python
"defaultValue": "0"
```
**What it does:** Default value to use if field is missing or null  
**Examples:** `defaultValue: "0"` for counts, `defaultValue: "unknown"` for statuses  
**Used by:** Clean stage - fills missing values  
**Jira usage:** Low - ~10% of fields have defaults  
**Zephyr need:** Low  
**Recommendation:** ⚠️ **OPTIONAL in canonical** - Useful but not critical for L1-L3

---

### **Category 5: Documentation**

#### **14. `description` (StringType, NULLABLE)**
```python
"description": "Issue unique identifier"
```
**What it does:** Human-readable description of the field  
**Examples:** "Issue ID", "User email address", "Cycle start date"  
**Used by:** Documentation, code comments, schema catalogs, data dictionary  
**Jira usage:** High - every field has description  
**Zephyr need:** High  
**Recommendation:** ✅ **INCLUDE in canonical** - MANDATORY for maintainability

---

#### **15. `notes` (StringType, NULLABLE)**
```python
"notes": "Primary key. Required for all operations. Never null."
```
**What it does:** Additional technical notes, warnings, gotchas  
**Examples:** "Use existing release (newly created releases are locked)", "API returns 403 for this endpoint"  
**Used by:** Developer guidance, troubleshooting, edge case handling  
**Jira usage:** Moderate - ~20% of fields have notes  
**Zephyr need:** High - API has many quirks!  
**Recommendation:** ✅ **INCLUDE in canonical** - Critical for API quirks documentation

---

#### **16. `initialDataType` (StringType, NULLABLE)**
```python
"initialDataType": "array<object>"
```
**What it does:** Original data type from API before transformation  
**Examples:** `array<object>` before flattening to `array<int64>`  
**Used by:** Audit trail, debugging transformations, rollback scenarios  
**Jira usage:** Low - used for documentation  
**Zephyr need:** Moderate - tracks transformation decisions  
**Recommendation:** ⚠️ **OPTIONAL in canonical** - Useful for L3+ (transformation tracking)

---

#### **17. `type` (StringType, NULLABLE)**
```python
"type": "system"
```
**What it does:** Field category/family in source system  
**Jira values:** "system" (built-in), "custom" (user-defined)  
**Jira usage:** Moderate - differentiates system vs custom fields  
**Zephyr equivalent:** "identity", "timestamp", "relationship", "metadata"?  
**Jira-specific?** Somewhat  
**Recommendation:** ⚠️ **OPTIONAL in canonical** - Could be replaced by `group`

---

### **Category 6: Display & Reporting**

#### **18. `columnOrder` (ArrayType(IntegerType), NULLABLE)**
```python
"columnOrder": [1]
```
**What it does:** Display order in tables/reports (array for exploded fields)  
**Why array?** Matches `targetField` length (one order per target)  
**Examples:**
```python
# Single field
targetField: ["id"] → columnOrder: [1]

# Exploded fields
targetField: ["assigneeIds", "assigneeNames"] 
columnOrder: [5, 6]
```

**Used by:** Power BI reports, data previews, dimensional modeling  
**Jira usage:** Moderate - ensures consistent column ordering  
**Zephyr need:** Low for L1-L3, higher for L5+ (reports)  
**Recommendation:** ⚠️ **OPTIONAL in canonical** - Useful for mature pipelines (L4+)

---

### **Category 7: Security & Privacy**

#### **19. `piiLevel` (ArrayType(StringType), NULLABLE)**
```python
"piiLevel": [None] | ["email"] | ["phone"] | ["name"]
```
**What it does:** Marks personally identifiable information for GDPR/compliance  
**Why array?** Matches `targetField` length (one PII level per target)  
**Values:** `None`, `"email"`, `"phone"`, `"name"`, `"ip"`, `"address"`  
**Examples:**
```python
# Non-PII
targetField: ["id"] → piiLevel: [None]

# PII
targetField: ["email"] → piiLevel: ["email"]

# Exploded with mixed PII
targetField: ["userId", "userEmail"] 
piiLevel: [None, "email"]
```

**Used by:** Data masking, access control, compliance reporting  
**Jira usage:** High - GDPR compliance critical  
**Zephyr need:** Moderate - test management has assignee names  
**Recommendation:** ✅ **INCLUDE in canonical** - Important for production (L5+), defer to L5

---

### **Category 8: Dimensional Modeling** (Refine/Analyse Stages)

#### **20. `isInFactIssue` (ArrayType(BooleanType), NULLABLE)**
```python
"isInFactIssue": [True]
```
**What it does:** Field is included in the fact table (vs dimension table)  
**Why array?** Matches `targetField` length  
**Used by:** Refine stage - star schema construction  
**Jira usage:** High - builds fact_issue, fact_changelog tables  
**Zephyr need:** Low - won't reach Refine for months  
**Recommendation:** ⚠️ **OPTIONAL in canonical** - Defer to L4+

---

#### **21. `keyField` (ArrayType(BooleanType), NULLABLE)**
```python
"keyField": [True]
```
**What it does:** Field is a key (primary or foreign key)  
**Why array?** Matches `targetField` length  
**Used by:** Refine stage - relationship mapping  
**Jira usage:** Moderate - identifies PKs/FKs  
**Zephyr need:** Low - defer to L4+  
**Recommendation:** ⚠️ **OPTIONAL in canonical** - Defer to L4+

---

#### **22. `dimensionName` (StringType, NULLABLE)**
```python
"dimensionName": "dim_user"
```
**What it does:** Foreign key reference to dimension table  
**Examples:** "dim_user", "dim_status", "dim_project"  
**Used by:** Refine stage - builds dimension references  
**Jira usage:** High - creates star schema relationships  
**Zephyr need:** None - defer to L6  
**Recommendation:** ⚠️ **OPTIONAL in canonical** - Defer to L6 (dimensional modeling)

---

#### **23. `bridgeName` (StringType, NULLABLE)**
```python
"bridgeName": "bridge_issue_assignee"
```
**What it does:** Many-to-many relationship bridge table  
**Examples:** Issue has multiple assignees → bridge table  
**Used by:** Refine stage - handles many-to-many  
**Jira usage:** Moderate - 10+ bridge tables  
**Zephyr need:** None - defer to L6  
**Recommendation:** ⚠️ **OPTIONAL in canonical** - Defer to L6

---

## Proposed Canonical SPECTRA Schema

### **Tier 1: MANDATORY (All Pipelines, All Stages)**

**L1 (MVP) - Must Have:**
```python
{
    # Entity & Field Identity (3 fields)
    "entity": StringType(),              # NOT NULL - Entity name
    "fieldName": StringType(),           # NOT NULL - Field name
    "fieldId": StringType(),             # NOT NULL - Unique identifier (entity.fieldName)
    
    # Structure & Transformation (4 fields)
    "structureType": StringType(),       # NOT NULL - scalar|array|object|objectDump
    "rawField": ArrayType(StringType()), # NOT NULL - Source path
    "targetField": ArrayType(StringType()), # NOT NULL - Target path(s)
    "dataType": ArrayType(StringType()), # NOT NULL - Target type(s)
    
    # Basic Metadata (2 fields)
    "description": StringType(),         # NOT NULL - Human-readable description
    "isRequired": BooleanType(),         # NOT NULL - Must be in API response
}
```

**Total: 9 mandatory fields**

---

### **Tier 2: RECOMMENDED (Most Pipelines)**

**L2 (Alpha) - Add Soon:**
```python
{
    # Organization (2 fields)
    "group": StringType(),               # NOT NULL - Logical grouping
    "groupSortOrder": IntegerType(),     # NOT NULL - Group display order
    
    # Data Quality (1 field)
    "isNullable": BooleanType(),         # NULLABLE - Can be null if present
    
    # Documentation (1 field)
    "notes": StringType(),               # NULLABLE - Technical notes, gotchas
}
```

**Total: 13 fields (9 + 4)**

---

### **Tier 3: OPTIONAL (Mature Pipelines)**

**L3 (Beta) - Transformation Tracking:**
```python
{
    "initialDataType": StringType(),     # NULLABLE - Original type before transform
    "defaultValue": StringType(),        # NULLABLE - Default if missing
}
```

**L4 (Live) - Reporting:**
```python
{
    "columnOrder": ArrayType(IntegerType()), # NULLABLE - Display order
    "entitySortOrder": IntegerType(),    # NULLABLE - Entity display order
}
```

**L5 (Reactive) - Security:**
```python
{
    "piiLevel": ArrayType(StringType()), # NULLABLE - PII classification
}
```

**L6 (Proactive) - Dimensional Modeling:**
```python
{
    "isInFactTable": ArrayType(BooleanType()), # NULLABLE - In fact table?
    "keyField": ArrayType(BooleanType()),      # NULLABLE - Is key field?
    "dimensionName": StringType(),             # NULLABLE - Dimension reference
    "bridgeName": StringType(),                # NULLABLE - Bridge table name
}
```

---

## Fields Excluded from Canonical (Too Specific)

**Jira-specific fields NOT in canonical:**
- ❌ `isInApiIssue` - Too Jira-specific (replace with generic `sourceEndpoint`)
- ❌ `isInChangelog` - Too Jira-specific (not all APIs have changelog)
- ❌ `type` - Too Jira-specific (covered by `group`)

---

## New Fields for Canonical (Not in Jira)

**Add these to improve on Jira:**

```python
{
    # API Intelligence (Zephyr innovation!)
    "sourceEndpoint": StringType(),      # NOT NULL - API endpoint (e.g., "/cycle")
    "intelligenceStatus": StringType(),  # NULLABLE - "working"|"broken"|"blocked"
}
```

**Rationale:** 
- `sourceEndpoint` - Generic replacement for `isInApiIssue`/`isInChangelog`
- `intelligenceStatus` - Zephyr innovation! Tracks API probe status

---

## Final Canonical SPECTRA Schema (L1)

```python
canonical_spectra_schema = StructType([
    # === TIER 1: MANDATORY (9 fields) ===
    # Entity & Field Identity
    StructField("entity", StringType(), False),
    StructField("fieldName", StringType(), False),
    StructField("fieldId", StringType(), False),
    
    # Structure & Transformation
    StructField("structureType", StringType(), False),
    StructField("rawField", ArrayType(StringType()), False),
    StructField("targetField", ArrayType(StringType()), False),
    StructField("dataType", ArrayType(StringType()), False),
    
    # Basic Metadata
    StructField("description", StringType(), False),
    StructField("isRequired", BooleanType(), False),
    
    # === TIER 2: RECOMMENDED (4 fields) ===
    # Organization
    StructField("group", StringType(), False),           # Add in L2
    StructField("groupSortOrder", IntegerType(), False), # Add in L2
    
    # Data Quality
    StructField("isNullable", BooleanType(), True),      # Add in L2
    
    # Documentation
    StructField("notes", StringType(), True),            # Add in L2
    
    # === SPECTRA Innovation (2 fields) ===
    StructField("sourceEndpoint", StringType(), False),
    StructField("intelligenceStatus", StringType(), True),
])
```

**Total: 15 fields for L1+L2**

---

## Decision Matrix

| Field | Jira | Zephyr | Xero | UniFi | Canonical? | Tier |
|-------|------|--------|------|-------|------------|------|
| entity | ✅ | ✅ | ✅ | ✅ | ✅ MANDATORY | 1 |
| fieldName | ✅ | ✅ | ✅ | ✅ | ✅ MANDATORY | 1 |
| fieldId | ✅ | ✅ | ✅ | ✅ | ✅ MANDATORY | 1 |
| structureType | ✅ | ✅ | ✅ | ✅ | ✅ MANDATORY | 1 |
| rawField | ✅ | ✅ | ✅ | ✅ | ✅ MANDATORY | 1 |
| targetField | ✅ | ✅ | ✅ | ✅ | ✅ MANDATORY | 1 |
| dataType | ✅ | ✅ | ✅ | ✅ | ✅ MANDATORY | 1 |
| description | ✅ | ✅ | ✅ | ✅ | ✅ MANDATORY | 1 |
| isRequired | ✅ | ✅ | ✅ | ✅ | ✅ MANDATORY | 1 |
| group | ✅ | ✅ | ✅ | ✅ | ✅ RECOMMENDED | 2 |
| groupSortOrder | ✅ | ✅ | ✅ | ✅ | ✅ RECOMMENDED | 2 |
| isNullable | ✅ | ✅ | ✅ | ✅ | ✅ RECOMMENDED | 2 |
| notes | ✅ | ✅ | ✅ | ✅ | ✅ RECOMMENDED | 2 |
| sourceEndpoint | ❌ | ✅ | ✅ | ✅ | ✅ INNOVATION | 1 |
| intelligenceStatus | ❌ | ✅ | ✅ | ✅ | ✅ INNOVATION | 1 |
| initialDataType | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ OPTIONAL | 3 |
| defaultValue | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ OPTIONAL | 3 |
| columnOrder | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ OPTIONAL | 4 |
| piiLevel | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ OPTIONAL | 5 |
| dimensionName | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ OPTIONAL | 6 |
| isInApiIssue | ✅ | ❌ | ❌ | ❌ | ❌ TOO SPECIFIC | - |
| isInChangelog | ✅ | ❌ | ❌ | ❌ | ❌ TOO SPECIFIC | - |
| type | ✅ | ❌ | ❌ | ❌ | ❌ REDUNDANT | - |

---

## Questions for You

1. **Tier 1 (9 mandatory fields)** - Agree these are essential for L1?
2. **Tier 2 (4 recommended fields)** - Should we add these immediately or defer to L2?
3. **SPECTRA innovations** - Like `sourceEndpoint` and `intelligenceStatus` as additions to Jira pattern?
4. **Field names** - Any you'd rename? (e.g., `structureType` vs `fieldStructure`?)
5. **Missing anything?** - Any critical fields we're missing?

**This will become the standard for ALL SPECTRA pipelines!** 🎯






