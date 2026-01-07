# Jira Schema Semantics - COMPLETE USAGE ANALYSIS

## 🔬 How Jira ACTUALLY Uses Schema Fields

### **Extract Stage Usage:**

```python
# From extractUtils.py line 158-212
def create_extract_config(schema_df, entity_name: str):
    """
    Uses fieldId (not targetField) for Jira API calls.
    """
    required_fields = (
        schema_df
        .filter(F.col("isInApiIssue") == True)  # ← Filter: Only API fields
        .select("fieldId")                       # ← Use: fieldId for API request
        .distinct()
        .collect()
    )
    return {"fieldIds": api_fields}  # ← Returns fieldIds for API
```

**What Extract does:**
1. Filters schema by `isInApiIssue == True`
2. Extracts `fieldId` column
3. Uses `fieldId` values for API request parameter: `fields=id,key,issuetype,components,...`
4. Returns raw JSON with nested structure intact

**Example:**
```python
# Schema row:
fieldId="issuetype"
isInApiIssue=True

# API Request:
GET /issue?fields=id,key,issuetype,components

# API Response:
{
  "id": 123,
  "key": "PROJ-1",
  "issuetype": {
    "id": 10001,
    "name": "Story",
    "iconUrl": "..."
  }
}
```

---

### **Clean Stage Usage (Part 1: Filter):**

```python
# From cleanUtils.py line 94-109
def filterEntityFromSchema(dfPromoted, dfSchema):
    """
    Filters dfPromoted to retain only fieldIds defined in dfSchema.
    """
    schemaFields = [row["fieldId"] for row in dfSchema.select("fieldId").distinct().collect()]
    requested = [field for field in schemaFields if field in dfPromoted.columns]
    return dfPromoted.select(requested)
```

**What Filter does:**
1. Gets all `fieldId` values from schema
2. Keeps only columns that match `fieldId`
3. Drops any columns not in schema

---

### **Clean Stage Usage (Part 2: Rename):**

```python
# From cleanUtils.py line 161-175
def renameEntityFromSchema(dfFiltered, dfSchema):
    """
    Renames columns using fieldId → entity mapping.
    """
    schemaRows = dfSchema.select("fieldId", "entity").distinct().collect()
    renameMap = {}
    for row in schemaRows:
        src = row["fieldId"]   # ← SOURCE: API field name
        tgt = row["entity"]    # ← TARGET: Clean column name
        if src in dfFiltered.columns:
            renameMap[src] = tgt
    # Apply renames
    renamedCols = [f"`{c}` as `{renameMap[c]}`" for c in dfFiltered.columns]
    return dfFiltered.selectExpr(renamedCols)
```

**What Rename does:**
1. Creates map: `fieldId → entity`
2. Renames columns using this map
3. Result: `issuetype` becomes `issueType`

**Example:**
```python
# Before Clean:
{
  "id": 123,
  "key": "PROJ-1",
  "issuetype": {...}
}

# After filterEntityFromSchema (keeps fieldId columns):
{
  "id": 123,
  "key": "PROJ-1",
  "issuetype": {...}
}

# After renameEntityFromSchema (fieldId → entity):
{
  "issueId": 123,        # id → issueId
  "jiraKey": "PROJ-1",   # key → jiraKey
  "issueType": {...}     # issuetype → issueType
}
```

---

## 🔑 THE KEY SEMANTIC: `entity` = TARGET COLUMN/DIMENSION NAME

### **For Scalars:**
```python
{
    "fieldId": "id",           # ← RAW API field
    "entity": "issueId",       # ← TARGET column name
    "structureType": "scalar",
    "rawField": ["id"],
    "targetField": ["issueId"],
}
```

**Flow:**
```
API: {"id": 123}
  ↓ Extract (keep raw fieldId)
Extract: {"id": 123}
  ↓ Clean (rename fieldId → entity)
Clean: {"issueId": 123}
```

---

### **For Nested Objects (Records):**
```python
{
    "fieldId": "issuetype",                      # ← RAW API field (nested object)
    "entity": "issueType",                       # ← TARGET dimension name
    "structureType": "record",
    "rawField": ["iconUrl", "id", "name"],       # ← Properties to extract
    "targetField": ["issueTypeIconUrl", "issueTypeId", "issueType"],  # ← Flattened outputs
}
```

**Flow:**
```
API: {"issuetype": {"iconUrl": "...", "id": 10001, "name": "Story"}}
  ↓ Extract (keep raw fieldId, nested structure)
Extract: {"issuetype": {"iconUrl": "...", "id": 10001, "name": "Story"}}
  ↓ Clean (promote nested fields using rawField → targetField)
Clean: {
  "issueTypeIconUrl": "...",    # issuetype.iconUrl → issueTypeIconUrl
  "issueTypeId": 10001,         # issuetype.id → issueTypeId
  "issueType": "Story"          # issuetype.name → issueType
}
```

**Note:** Clean stage doesn't just rename - it FLATTENS using `rawField`/`targetField`!

---

### **For Arrays (Multiple Objects):**
```python
{
    "fieldId": "components",                  # ← RAW API field (array)
    "entity": "component",                    # ← TARGET dimension (SINGULAR!)
    "structureType": "array",
    "rawField": ["id", "name"],               # ← Properties from EACH array element
    "targetField": ["componentId", "component"],  # ← Flattened to array columns
    "dimensionName": "dimComponent",
    "bridgeName": "bridgeComponent",
}
```

**Flow:**
```
API: {"components": [{"id": 10100, "name": "Frontend"}, {"id": 10101, "name": "Backend"}]}
  ↓ Extract (keep raw)
Extract: {"components": [{"id": 10100, "name": "Frontend"}, {"id": 10101, "name": "Backend"}]}
  ↓ Clean (flatten using rawField → targetField)
Clean: {
  "componentId": [10100, 10101],         # Extract .id from each element
  "component": ["Frontend", "Backend"]   # Extract .name from each element
}
  ↓ Refine (create dimension + bridge)
dimComponent:
  componentId | component
  10100       | Frontend
  10101       | Backend

bridgeComponent:
  issueId | componentId
  123     | 10100
  123     | 10101
```

---

## ❓ CRITICAL QUESTION: What About Entity Filtering?

**Found in `_extract_required_fields` (line 484):**
```python
entity_fields = (
    schema_df
    .filter(F.col("entity") == entity_name)  # ← FILTERS by entity!
```

**BUT:** This function is NOT used by extractJiraIssue! It's only used by extractJiraField, extractJiraUser, etc.

**For extractJiraIssue:**
- Does NOT filter by entity
- Uses ALL fields where `isInApiIssue == True`
- Extracts everything in one call

**For extractJiraField, extractJiraUser (dimension extracts):**
- DOES filter by `entity == entity_name`
- Extracts specific dimension separately

---

## 🎯 THE COMPLETE SEMANTIC MODEL

### **Field Definitions:**

| Field | Purpose | Used By | Example Values |
|-------|---------|---------|----------------|
| **fieldId** | RAW API field name | Extract (API request), Clean (filter) | "id", "issuetype", "components" |
| **entity** | TARGET column/dimension name | Clean (rename), Refine (dimension name) | "issueId", "issueType", "component" |
| **structureType** | Data structure type | Clean (flattening logic), Transform | "scalar", "record", "array" |
| **rawField** | Properties to extract (array) | Clean (nested field navigation) | ["id"], ["iconUrl","id","name"], ["id","name"] |
| **targetField** | Output column names (array) | Clean (flattened column names) | ["issueId"], ["issueTypeIconUrl","issueTypeId","issueType"] |
| **dataType** | Output data types (array) | Clean (type casting) | ["int64"], ["text","int64","text"] |
| **isInApiIssue** | Field comes from API | Extract (request filter) | true, false |

---

### **Key Patterns:**

#### **1. Scalar Field:**
```python
fieldId: "id"           # API field
entity: "issueId"       # Target column
rawField: ["id"]        # Path (single element)
targetField: ["issueId"] # Output (single element)
```

#### **2. Nested Object (Record):**
```python
fieldId: "issuetype"    # API field (object)
entity: "issueType"     # Dimension name
rawField: ["iconUrl", "id", "name"]  # THREE properties
targetField: ["issueTypeIconUrl", "issueTypeId", "issueType"]  # THREE outputs
```

#### **3. Array of Objects:**
```python
fieldId: "components"   # API field (array)
entity: "component"     # Dimension name (SINGULAR!)
rawField: ["id", "name"] # TWO properties per element
targetField: ["componentId", "component"]  # TWO array outputs
```

#### **4. Array of Scalars:**
```python
fieldId: "labels"       # API field (array of strings)
entity: "label"         # Dimension name (SINGULAR!)
rawField: ["labels"]    # The field itself
targetField: ["label"]  # Single array output
```

---

## 🔧 IMPLICATIONS FOR ZEPHYR

### **Current Zephyr Schema (WRONG):**
```python
{
    "entity": "cycle",              # ❌ Source entity (not target!)
    "fieldName": "cyclePhases",     # ❌ Redundant with fieldId?
    "fieldId": "cycle.cyclePhases", # ❌ Should be just "cyclePhases"
    "rawField": ["cyclePhases"],    # ❌ Should be properties: ["id","name",...]
    "targetField": [...]            # ❌ Missing!
}
```

### **Correct Zephyr Schema (Jira Pattern):**
```python
{
    "fieldId": "cyclePhases",       # ✅ RAW API field
    "entity": "cyclePhase",         # ✅ Target dimension (SINGULAR!)
    "structureType": "array",
    "rawField": ["id", "name", "startDate", "endDate"],  # ✅ Properties per element
    "targetField": ["cyclePhaseId", "cyclePhaseName", "cyclePhaseStartDate", "cyclePhaseEndDate"],
    "dataType": ["int64", "text", "date", "date"],
    "dimensionName": "dimCyclePhase",
    "bridgeName": "bridgeCyclePhase",
}
```

---

## ❓ STILL UNANSWERED: What is `fieldName`?

**Jira doesn't have `fieldName` - only `fieldId` and `entity`!**

**Hypothesis:** 
- We added `fieldName` thinking it was the field within the entity
- But Jira uses `fieldId` for this purpose
- `fieldName` is REDUNDANT with `fieldId`!

---

## 🎯 CANONICAL SPECTRA SCHEMA (Jira-Validated)

### **Tier 1 Fields (Validated from Jira):**

```python
{
    # === Field Identity ===
    "fieldId": StringType(),        # ✅ RAW API field name (Extract, Clean)
    "entity": StringType(),         # ✅ TARGET column/dimension (Clean, Refine)
    
    # === Structure ===
    "structureType": StringType(),  # ✅ scalar|record|array|objectDump
    "rawField": ArrayType(StringType()),   # ✅ Properties to extract
    "targetField": ArrayType(StringType()), # ✅ Output column names
    "dataType": ArrayType(StringType()),    # ✅ Output types
    
    # === Metadata ===
    "description": StringType(),    # ✅ Documentation
    "isRequired": BooleanType(),    # ✅ Must be in API
    
    # === API Intelligence ===
    "sourceEndpoint": StringType(), # NEW: Which endpoint provides this
    "apiStatus": StringType(),      # NEW: working|broken|blocked
    
    # === API Source (Jira has this) ===
    "isInApiIssue": BooleanType(),  # ✅ Field comes from main API
}
```

**Total: 11 fields (NO fieldName!)**

---

## 🚨 CRITICAL DECISION NEEDED

**Should we:**

**Option A: Follow Jira Exactly** (Proven Pattern)
- Use `fieldId` + `entity` (no `fieldName`)
- `fieldId` = RAW API field ("cyclePhases")
- `entity` = TARGET dimension ("cyclePhase" - singular!)
- **Pro:** Matches proven L6 pipeline
- **Con:** `entity` is confusing (not source, target!)

**Option B: Add Parent Context** (More Intuitive)
- Keep `fieldId` + `entity`
- Add `parentEntity` = "cycle" (source context)
- `entity` = "cyclePhase" (target dimension)
- **Pro:** Clearer what we're extracting FROM
- **Con:** Jira doesn't need this (extracts everything from /issue)

**Option C: Clarify Names** (Most SPECTRA-grade?)
- `sourceFieldId` = "cyclePhases" (RAW API field)
- `targetDimension` = "cyclePhase" (target dimension)
- `parentEntity` = "cycle" (source entity)
- **Pro:** Crystal clear semantics
- **Con:** Different from Jira (breaks parity)

---

## 📊 Recommendation: Option A (Jira Pattern)

**Why:**
- ✅ Proven at L6 (Jira is production)
- ✅ Clean/Transform/Refine already built for this pattern
- ✅ Minimal cognitive load (reuse existing code)
- ✅ `entity` semantic is understood (target dimension)

**Accept:**
- ⚠️ `entity` is not intuitive (means target, not source)
- ⚠️ Need good documentation

**Remove:**
- ❌ `fieldName` (redundant with `fieldId`)

**Final Schema:**
```python
{
    "fieldId": "cyclePhases",       # RAW API field
    "entity": "cyclePhase",         # TARGET dimension (singular!)
    # ... rest of Tier 1 fields
}
```






