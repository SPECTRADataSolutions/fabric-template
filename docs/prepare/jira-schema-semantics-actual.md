# Jira Schema Semantics - ACTUAL USAGE (From Code Analysis)

## ⚠️ CRITICAL FINDINGS

**I was misunderstanding `entity`! Let me correct this.**

---

## Real Example 1: Scalar Field (id → issueId)

```python
SchemaField(
    group="issueIdentifier",
    entity="issueId",              # ← TARGET field name (after rename)
    fieldId="id",                  # ← RAW field name in API
    structureType="scalar",
    rawField=["id"],               # ← Path in source JSON [just the field]
    targetField=["issueId"],       # ← ONE output field (renamed)
    dataType=["int64"],            # ← ONE output type
)
```

**API Response:**
```json
{
  "id": 12345,
  "key": "PROJ-123"
}
```

**Extraction:**
- Read: `api_response["id"]` (using `rawField[0]`)
- Write: `issueId = 12345` (using `targetField[0]`)

**Semantics:**
- `entity` = Target field name after transformation (`issueId`)
- `fieldId` = Raw field name in API (`id`)
- `rawField` = Path to value (`["id"]`)
- `targetField` = Output field name (`["issueId"]`)

---

## Real Example 2: Nested Object (issuetype → issueType, issueTypeId, issueTypeIconUrl)

```python
SchemaField(
    group="issueDetails",
    entity="issueType",                    # ← TARGET entity/concept
    fieldId="issuetype",                   # ← RAW field name in API
    structureType="record",                # ← Nested object
    rawField=["iconUrl", "id", "name"],    # ← THREE properties in object
    targetField=["issueTypeIconUrl", "issueTypeId", "issueType"],  # ← THREE output fields
    dataType=["text", "int64", "text"],    # ← THREE types
    dimensionName="dimIssueType",          # ← Creates dimension table
)
```

**API Response:**
```json
{
  "issuetype": {
    "iconUrl": "https://...",
    "id": 10001,
    "name": "Story"
  }
}
```

**Extraction:**
- Read: `api_response["issuetype"]["iconUrl"]` → Write: `issueTypeIconUrl`
- Read: `api_response["issuetype"]["id"]` → Write: `issueTypeId`
- Read: `api_response["issuetype"]["name"]` → Write: `issueType`

**Semantics:**
- `entity` = Target concept/dimension (`issueType`)
- `fieldId` = Raw field in API (`issuetype`)
- `rawField` = Array of properties to extract (`["iconUrl", "id", "name"]`)
- `targetField` = Array of output fields (ONE per rawField element)
- `dataType` = Array of types (ONE per targetField element)

---

## Real Example 3: Array of Objects (components → componentId, component)

```python
SchemaField(
    group="categorisation",
    entity="component",                    # ← TARGET dimension name
    fieldId="components",                  # ← RAW field name (plural)
    structureType="array",                 # ← Array of objects
    rawField=["id", "name"],               # ← TWO properties per array element
    targetField=["componentId", "component"], # ← TWO output fields (flattened)
    dataType=["int64", "text"],            # ← TWO types
    dimensionName="dimComponent",          # ← Dimension table
    bridgeName="bridgeComponent",          # ← Bridge table (many-to-many)
)
```

**API Response:**
```json
{
  "components": [
    {"id": 10100, "name": "Frontend"},
    {"id": 10101, "name": "Backend"},
    {"id": 10102, "name": "API"}
  ]
}
```

**Extraction (Extract Stage):**
- Read: `api_response["components"]` (array of objects)
- Extract: `componentId = [10100, 10101, 10102]` (array of IDs)
- Extract: `component = ["Frontend", "Backend", "API"]` (array of names)
- Write: Two array columns in extract table

**Refine (Refine Stage):**
- Creates `dimComponent` dimension table:
  ```
  componentId | component
  10100       | Frontend
  10101       | Backend
  10102       | API
  ```
- Creates `bridgeComponent` bridge table:
  ```
  issueId | componentId
  12345   | 10100
  12345   | 10101
  12345   | 10102
  ```

**Semantics:**
- `entity` = Target dimension name (`component` - SINGULAR!)
- `fieldId` = Raw field in API (`components` - PLURAL!)
- `rawField` = Properties to extract from EACH array element
- `targetField` = Output fields (arrays of extracted properties)
- `dataType` = Types of output arrays
- `bridgeName` = Bridge table to explode array into rows

---

## Real Example 4: Array of Scalars (labels)

```python
SchemaField(
    group="categorisation",
    entity="label",                 # ← TARGET dimension name (singular)
    fieldId="labels",               # ← RAW field name (plural)
    structureType="array",
    rawField=["labels"],            # ← Just "labels" (it's an array of strings)
    targetField=["label"],          # ← ONE output field (singular)
    dataType=["text"],              # ← ONE type
    dimensionName="dimLabel",
    bridgeName="bridgeLabel",
)
```

**API Response:**
```json
{
  "labels": ["bug", "urgent", "frontend"]
}
```

**Extraction:**
- Read: `api_response["labels"]`
- Write: `label = ["bug", "urgent", "frontend"]` (array column)

**Refine:**
- Creates `dimLabel` dimension table and `bridgeLabel` bridge table

**Semantics:**
- `entity` = Target dimension (`label` - singular)
- `fieldId` = Raw field (`labels` - plural)
- `rawField` = `["labels"]` (the field itself - it's already an array)
- `targetField` = `["label"]` (singular output)

---

## THE CORRECTED SEMANTICS

### **`entity`**
**NOT** the source entity (like "issue" or "cycle")  
**IT IS** the target concept/dimension/field after transformation

**Examples:**
- `entity="issueId"` - Target is the issueId field
- `entity="issueType"` - Target is the issueType concept (dimension)
- `entity="component"` - Target is the component dimension (singular!)
- `entity="label"` - Target is the label dimension (singular!)

**Pattern:**
- Scalars: `entity` = target field name
- Objects: `entity` = target concept (becomes dimension)
- Arrays: `entity` = target dimension name (SINGULAR, even if source is plural)

---

### **`fieldId`**
**The raw field name in the API response**

**Examples:**
- `fieldId="id"` - API has `{"id": 123}`
- `fieldId="issuetype"` - API has `{"issuetype": {...}}`
- `fieldId="components"` - API has `{"components": [...]}`
- `fieldId="customfield_10309"` - API has custom field

---

### **`rawField`** (ARRAY)
**Path segments OR property names to extract**

**For scalars:**
```python
rawField=["id"]           # Just the field name
```

**For nested objects:**
```python
rawField=["iconUrl", "id", "name"]  # Properties to extract from object
```

**For arrays of objects:**
```python
rawField=["id", "name"]    # Properties to extract from EACH array element
```

**For arrays of scalars:**
```python
rawField=["labels"]        # The field itself (it's already an array)
```

---

### **`targetField`** (ARRAY)
**Output field names after transformation**

**Must have same length as `rawField` (1:1 mapping)**

**For scalars:**
```python
rawField=["id"]
targetField=["issueId"]    # Renamed
```

**For nested objects:**
```python
rawField=["iconUrl", "id", "name"]
targetField=["issueTypeIconUrl", "issueTypeId", "issueType"]  # Three outputs
```

**For arrays:**
```python
rawField=["id", "name"]
targetField=["componentId", "component"]  # Flattened to two array columns
```

---

### **`dataType`** (ARRAY)
**Output data types (one per `targetField` element)**

**Must have same length as `targetField`**

**Examples:**
```python
targetField=["issueId"]
dataType=["int64"]

targetField=["issueTypeIconUrl", "issueTypeId", "issueType"]
dataType=["text", "int64", "text"]

targetField=["componentId", "component"]
dataType=["int64", "text"]
```

---

### **`structureType`**
**Type of data structure:**

- `scalar` - Single primitive value
- `record` - Nested object (flattened to multiple fields)
- `array` - Array of values (objects or primitives)
- `objectDump` - Unknown structure (keep as JSON string)

---

## How Extract Stage Uses This

### **Step 1: Read source**
```python
source_value = api_response[fieldId]  # Read by fieldId
```

### **Step 2: Navigate/Extract based on structureType**

**If scalar:**
```python
output[targetField[0]] = source_value
```

**If record:**
```python
for i, prop in enumerate(rawField):
    output[targetField[i]] = source_value[prop]
```

**If array of objects:**
```python
for i, prop in enumerate(rawField):
    output[targetField[i]] = [item[prop] for item in source_value]
```

**If array of scalars:**
```python
output[targetField[0]] = source_value  # Already an array
```

---

## How Refine Stage Uses This

### **For arrays with `dimensionName` and `bridgeName`:**

**Step 1: Create dimension table**
```python
# dimComponent gets unique componentId + component values
```

**Step 2: Create bridge table**
```python
# bridgeComponent gets issueId → componentId rows (exploded)
```

---

## IMPLICATIONS FOR ZEPHYR

### **For cycle.cyclePhases:**

**API Response:**
```json
{
  "id": 45,
  "name": "Sprint 1",
  "cyclePhases": [
    {
      "id": 1,
      "name": "Phase 1",
      "startDate": "2025-01-01",
      "endDate": "2025-01-15"
    },
    {
      "id": 2,
      "name": "Phase 2"
    }
  ]
}
```

**Correct Schema:**
```python
{
    "entity": "cyclePhase",            # ← Target dimension (SINGULAR!)
    "fieldId": "cyclePhases",          # ← Raw field in API (PLURAL!)
    "fieldName": "cyclePhases",        # ← Same as fieldId
    "structureType": "array",
    "rawField": ["id", "name", "startDate", "endDate"],  # ← Four properties per element
    "targetField": ["cyclePhaseId", "cyclePhaseName", "cyclePhaseStartDate", "cyclePhaseEndDate"],
    "dataType": ["int64", "text", "date", "date"],
    "dimensionName": "dimCyclePhase",
    "bridgeName": "bridgeCyclePhase",
}
```

**Extract Stage Output:**
```
cycleId | cyclePhaseId    | cyclePhaseName      | cyclePhaseStartDate    | cyclePhaseEndDate
45      | [1, 2]          | ["Phase 1", "Phase 2"] | ["2025-01-01", null] | ["2025-01-15", null]
```

**Refine Stage Output:**

`dimCyclePhase`:
```
cyclePhaseId | cyclePhaseName | cyclePhaseStartDate | cyclePhaseEndDate
1            | Phase 1        | 2025-01-01          | 2025-01-15
2            | Phase 2        | null                | null
```

`bridgeCyclePhase`:
```
cycleId | cyclePhaseId
45      | 1
45      | 2
```

---

## CRITICAL CORRECTIONS TO MY EARLIER RECOMMENDATIONS

### **❌ WRONG (What I Said Before):**

I said `entity` = "cycle" (the source entity)  
I said it's ONE row per source field

### **✅ CORRECT (Actual Jira Usage):**

`entity` = "cyclePhase" (the target dimension - SINGULAR!)  
`fieldId` = "cyclePhases" (the raw API field - PLURAL!)  
It's ONE row per logical concept/dimension

---

## Questions to Answer

1. **Does `entity` represent source or target?**  
   ✅ **TARGET** - It's the output concept/dimension/field

2. **Why is `rawField` an array?**  
   ✅ For nested objects/arrays - extracts multiple properties  
   ✅ For scalars - just one element array

3. **Why is `targetField` an array?**  
   ✅ One output field per `rawField` element (1:1 mapping)  
   ✅ Allows flattening nested objects to multiple columns

4. **What does `fieldName` mean?** (We added this!)  
   ⚠️ **Need to check** - Is this redundant with `fieldId`?

---

## Next: Validate Our Zephyr Schema

**Current Zephyr schema has:**
```python
"entity": "cycle",              # ← Is this right?
"fieldName": "cyclePhases",     # ← What does this mean?
"fieldId": "cycle.cyclePhases", # ← Should this be just "cyclePhases"?
```

**Should be:**
```python
"entity": "cyclePhase",         # ← Target dimension (singular!)
"fieldName": ???,               # ← Do we need this?
"fieldId": "cyclePhases",       # ← Raw API field
```

**NEED TO ANSWER: What is `fieldName` for?**






