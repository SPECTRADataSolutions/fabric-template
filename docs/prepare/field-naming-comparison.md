# Field Naming Comparison: Current vs Proposed

## Summary of Changes

**4 fields proposed for rename based on semantic clarity analysis:**

| Current (Jira) | Proposed (SPECTRA) | Reason |
|----------------|-------------------|--------|
| `rawField` | `sourceFieldPath` | More explicit: "raw" is ambiguous, "source path" is clear |
| `dataType` | `targetDataType` | Pairs with `targetField` (both are target/output) |
| `group` | `fieldGroup` | Avoids confusion with permission groups, user groups |
| `intelligenceStatus` | `apiStatus` | Clearer: API probe status, not ML/AI intelligence |

---

## Detailed Comparison

### **Change 1: rawField → sourceFieldPath**

#### **Current (Jira):**
```python
"rawField": ["fields", "status", "name"]
```

**Issues:**
- "raw" could mean unparsed string, raw bytes, unprocessed data
- Doesn't indicate it's a PATH (array of strings)
- Asymmetric with `targetField` (raw vs target? input vs output?)

#### **Proposed (SPECTRA):**
```python
"sourceFieldPath": ["fields", "status", "name"]
```

**Benefits:**
- ✅ "source" clearly indicates origin (API response)
- ✅ "Path" indicates it's a nested navigation path
- ✅ Pairs with `targetField` (source → target)
- ✅ Standard ETL terminology (source, target, transform)

**Example Usage:**
```python
# Navigate from source to target
source_value = api_response[sourceFieldPath[0]][sourceFieldPath[1]][sourceFieldPath[2]]
target_table[targetField[0]] = transform(source_value)
```

**Clarity Score:** 7/10 → 9/10

---

### **Change 2: dataType → targetDataType**

#### **Current (Jira):**
```python
"dataType": ["int64", "text"]
```

**Issues:**
- Ambiguous: Is this the SOURCE type or TARGET type?
- API returns JSON types, we cast to Delta types
- Doesn't pair with `targetField` naming

#### **Proposed (SPECTRA):**
```python
"targetDataType": ["int64", "text"]
```

**Benefits:**
- ✅ Explicit: These are OUTPUT types after transformation
- ✅ Pairs with `targetField` (both describe the target/output)
- ✅ Clear pipeline direction: source → target

**Full Example:**
```python
# Clear pipeline flow
"sourceFieldPath": ["cyclePhases"],           # INPUT (array of objects)
"targetField": ["cyclePhaseIds", "cyclePhaseNames"],  # OUTPUT (flattened)
"targetDataType": ["array<int64>", "array<text>"]    # OUTPUT TYPES
```

**Alternative Considered:**
- `outputDataType` - Good, but "output" is too generic
- `destinationDataType` - Too verbose
- `fieldDataType` - Still ambiguous

**Clarity Score:** 6/10 → 9/10

---

### **Change 3: group → fieldGroup**

#### **Current (Jira):**
```python
"group": "issueIdentifier"
```

**Issues:**
- "group" is overloaded term: permission groups, user groups, row groups
- Generic - what's being grouped?
- Could confuse with SQL GROUP BY

#### **Proposed (SPECTRA):**
```python
"fieldGroup": "issueIdentifier"
```

**Benefits:**
- ✅ Explicit: Grouping FIELDS, not users/permissions
- ✅ Unambiguous in any context
- ✅ Pairs with `fieldName`, `fieldId` (field prefix pattern)

**Example Values:**
```python
"fieldGroup": "identity"         # ID, key fields
"fieldGroup": "timestamps"       # Created, updated, deleted dates
"fieldGroup": "relationships"    # Foreign keys, arrays
"fieldGroup": "metadata"         # Descriptions, notes, tags
"fieldGroup": "status"           # Status, state, flags
```

**Alternative Considered:**
- `category` - Too generic (could be business category)
- `fieldFamily` - Too biological
- `fieldSet` - Too technical (implies Set data structure)

**Clarity Score:** 7/10 → 9/10

---

### **Change 4: intelligenceStatus → apiStatus**

#### **Current (Proposed for Zephyr):**
```python
"intelligenceStatus": "working"
```

**Issues:**
- "intelligence" suggests AI/ML
- Could be confused with business intelligence, data intelligence
- Not immediately clear what kind of intelligence

#### **Proposed (SPECTRA):**
```python
"apiStatus": "working"
```

**Benefits:**
- ✅ Explicit: Status from API probe/test
- ✅ Clear purpose: Is this API endpoint working?
- ✅ Immediate understanding for new developers
- ✅ Pairs with `sourceEndpoint` (both about API)

**Example Values:**
```python
"apiStatus": "working"   # ✅ API endpoint works
"apiStatus": "broken"    # ❌ API returns 500/403
"apiStatus": "blocked"   # ⚠️ API works but has dependencies
"apiStatus": "unknown"   # ⚠️ Not yet probed
```

**Alternative Considered:**
- `probeStatus` - Accurate but too technical
- `endpointStatus` - Good alternative
- `validationStatus` - Too generic

**Clarity Score:** 7/10 → 9/10

---

## Fields That STAY THE SAME ✅

### **entity** (Keep)
```python
"entity": "cycle"
```
✅ Standard, universally understood, no ambiguity

---

### **fieldName** (Keep)
```python
"fieldName": "id"
```
✅ Clear, standard terminology

---

### **fieldId** (Keep)
```python
"fieldId": "cycle.id"
```
✅ Pairs with `fieldName`, unambiguous

---

### **structureType** (Keep)
```python
"structureType": "scalar" | "array" | "object" | "objectDump"
```
✅ Standard data engineering term, widely understood

**Why not `fieldStructure`?**
- "structureType" is more standard
- Matches `dataType` pattern (thing + Type)
- Widely used in schema definitions

---

### **targetField** (Keep)
```python
"targetField": ["cyclePhaseIds", "cyclePhaseNames"]
```
✅ Clear, pairs with proposed `sourceFieldPath`

**Why not `outputField` or `destinationField`?**
- "target" is standard ETL terminology
- Pairs perfectly with "source"
- Concise and clear

---

### **description** (Keep)
```python
"description": "Cycle phase array containing phase metadata"
```
✅ Universal, no ambiguity

---

### **isRequired** (Keep)
```python
"isRequired": True
```
✅ Standard schema term (JSON Schema, SQL, etc.)

---

### **isNullable** (Keep)
```python
"isNullable": False
```
✅ Standard SQL/schema term

---

### **notes** (Keep)
```python
"notes": "API returns 403 for this endpoint. Use workaround X."
```
✅ Clear, standard documentation field

---

### **sourceEndpoint** (Keep)
```python
"sourceEndpoint": "/cycle"
```
✅ Clear, explicit, unambiguous

**Why not `apiEndpoint` or just `endpoint`?**
- "sourceEndpoint" is more specific
- Pairs with "source" theme (`sourceFieldPath`)
- Clear that it's WHERE THE DATA COMES FROM

---

## Complete Schema with New Names

### **Tier 1: MANDATORY (11 fields)**

```python
canonical_spectra_schema_tier1 = {
    # Entity & Field Identity
    "entity": StringType(),                     # ✅ KEEP
    "fieldName": StringType(),                  # ✅ KEEP
    "fieldId": StringType(),                    # ✅ KEEP
    
    # Structure & Transformation
    "structureType": StringType(),              # ✅ KEEP
    "sourceFieldPath": ArrayType(StringType()), # ✨ NEW (was rawField)
    "targetField": ArrayType(StringType()),     # ✅ KEEP
    "targetDataType": ArrayType(StringType()),  # ✨ NEW (was dataType)
    
    # Basic Metadata
    "description": StringType(),                # ✅ KEEP
    "isRequired": BooleanType(),                # ✅ KEEP
    
    # API Intelligence
    "sourceEndpoint": StringType(),             # ✅ KEEP
    "apiStatus": StringType(),                  # ✨ NEW (was intelligenceStatus)
}
```

### **Tier 2: RECOMMENDED (4 fields)**

```python
canonical_spectra_schema_tier2 = {
    # Organization
    "fieldGroup": StringType(),                 # ✨ NEW (was group)
    "groupSortOrder": IntegerType(),            # ✅ KEEP
    
    # Data Quality
    "isNullable": BooleanType(),                # ✅ KEEP
    
    # Documentation
    "notes": StringType(),                      # ✅ KEEP
}
```

---

## Real-World Example: cyclePhases

### **With OLD Names (Jira):**
```python
{
    "entity": "cycle",
    "fieldName": "cyclePhases",
    "fieldId": "cycle.cyclePhases",
    "structureType": "array",
    "rawField": ["cyclePhases"],                # ⚠️ "raw" ambiguous
    "targetField": ["cyclePhaseIds", "cyclePhaseNames"],
    "dataType": ["array<int64>", "array<text>"], # ⚠️ source or target?
    "description": "Cycle phase array",
    "isRequired": False,
    "sourceEndpoint": "/cycle",
    "intelligenceStatus": "working",            # ⚠️ what kind of intelligence?
    "group": "relationships",                   # ⚠️ could be user groups
    "groupSortOrder": 3,
    "isNullable": True,
    "notes": "Array of phase objects"
}
```

### **With NEW Names (SPECTRA):**
```python
{
    "entity": "cycle",
    "fieldName": "cyclePhases",
    "fieldId": "cycle.cyclePhases",
    "structureType": "array",
    "sourceFieldPath": ["cyclePhases"],          # ✅ Clear: path in source
    "targetField": ["cyclePhaseIds", "cyclePhaseNames"],
    "targetDataType": ["array<int64>", "array<text>"], # ✅ Clear: output types
    "description": "Cycle phase array",
    "isRequired": False,
    "sourceEndpoint": "/cycle",
    "apiStatus": "working",                      # ✅ Clear: API works
    "fieldGroup": "relationships",               # ✅ Clear: grouping fields
    "groupSortOrder": 3,
    "isNullable": True,
    "notes": "Array of phase objects"
}
```

---

## Impact Analysis

### **Code Changes Required:**

#### **Jira (Existing L6 Pipeline):**
```python
# OLD (22 fields)
"rawField"           → "sourceFieldPath"      # Rename
"dataType"           → "targetDataType"       # Rename  
"group"              → "fieldGroup"           # Rename
+ "apiStatus"                                 # ADD (new innovation)
- "isInApiIssue"                              # REMOVE (too specific)
- "isInChangelog"                             # REMOVE (too specific)
- "type"                                      # REMOVE (redundant with fieldGroup)

# Result: 20 fields (cleaned up + added apiStatus)
```

#### **Zephyr (New L1 Pipeline):**
```python
# Implement directly with new names (11 fields Tier 1)
# No migration needed!
```

---

## Migration Strategy

### **Option 1: Clean Break (Recommended)**
- Zephyr uses NEW names from day 1
- Jira migrates to NEW names in next refactor
- Both pipelines end up with same canonical schema

### **Option 2: Gradual Migration**
- Zephyr uses OLD names (Jira parity)
- Both migrate together later
- More consistent short-term, but delays improvement

### **Option 3: Aliasing**
- Support BOTH names temporarily
- `rawField` → alias for `sourceFieldPath`
- Deprecated old names over time

---

## Recommendation

**✅ Use NEW names for canonical SPECTRA schema:**

**Why?**
1. ✅ Clearer semantics (9/10 vs 6-7/10)
2. ✅ Better for new developers
3. ✅ Sets SPECTRA standard (Jira can adopt too)
4. ✅ No migration burden for Zephyr (starting fresh)
5. ✅ Jira can migrate gradually

**Names Summary:**
- ✨ 4 renamed: `sourceFieldPath`, `targetDataType`, `fieldGroup`, `apiStatus`
- ✅ 11 kept: `entity`, `fieldName`, `fieldId`, `structureType`, `targetField`, `description`, `isRequired`, `isNullable`, `notes`, `sourceEndpoint`, `groupSortOrder`

---

## Your Decision

**A) ✅ Use NEW names** (SPECTRA-grade clarity)
- `sourceFieldPath`, `targetDataType`, `fieldGroup`, `apiStatus`

**B) Keep OLD names** (Jira consistency)
- `rawField`, `dataType`, `group`, `intelligenceStatus`

**C) Mix approach** (Pragmatic)
- Keep 3, change 1 (e.g., only change `intelligenceStatus` → `apiStatus`)

**Which feels right?** 🎯






