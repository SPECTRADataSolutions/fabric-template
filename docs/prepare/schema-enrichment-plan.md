# Schema Enrichment Plan - Zephyr → Jira Pattern

## 🎯 Goal
Enrich Zephyr's basic API intelligence with Jira's proven L6 schema pattern for full pipeline support.

---

## 📊 Before/After Comparison

### **BEFORE (Current Zephyr - 7 fields):**

```python
{
    "entity": "cycle",              # ❌ Source entity (wrong semantic!)
    "fieldName": "cyclePhases",     # ❌ Redundant with fieldId
    "fieldType": "array",           # ⚠️ Basic type, no flattening info
    "isRequired": False,
    "description": "Cycle phases",
    "sourceEndpoint": "/cycle",
    "intelligenceStatus": "working"
}
```

**Problems:**
- No flattening specification (how to extract array elements?)
- `entity` means source (should mean target dimension)
- No `rawField`/`targetField` mapping
- `fieldName` redundant
- Can't drive Clean/Transform/Refine stages

---

### **AFTER (Jira Pattern - 15+ fields):**

```python
{
    # === Identity (Jira-validated) ===
    "fieldId": "cyclePhases",       # ✅ RAW API field (plural)
    "entity": "cyclePhase",         # ✅ TARGET dimension (SINGULAR!)
    
    # === Structure (Jira-validated) ===
    "structureType": "array",       # ✅ Array of objects
    "rawField": ["id", "name", "startDate", "endDate"],  # ✅ Properties per element
    "targetField": ["cyclePhaseId", "cyclePhaseName", "cyclePhaseStartDate", "cyclePhaseEndDate"],
    "dataType": ["array<int64>", "array<text>", "array<date>", "array<date>"],
    
    # === Metadata ===
    "description": "Cycle phases array",
    "isRequired": False,
    "isNullable": True,
    "notes": "Array of phase objects. Can be empty for cycles without phases.",
    
    # === Organization ===
    "group": "relationships",       # ✅ NEW: Logical grouping
    "groupSortOrder": 3,            # ✅ NEW: Display order
    
    # === API Intelligence ===
    "sourceEndpoint": "/cycle",
    "apiStatus": "working",         # ✅ RENAMED: was intelligenceStatus
    
    # === Dimensional Modeling (L4+) ===
    "dimensionName": "dimCyclePhase",   # ✅ NEW: Refine stage
    "bridgeName": "bridgeCyclePhase",   # ✅ NEW: Many-to-many
}
```

**Benefits:**
- ✅ Clean stage knows how to flatten
- ✅ Transform knows target column names
- ✅ Refine knows how to build dimensions
- ✅ Matches Jira L6 pattern exactly

---

## 🔧 Enrichment Process

### **Step 1: Generate Enriched Intelligence**
```bash
cd Data/zephyr
python scripts/enrich_intelligence_with_jira_pattern.py
```

**Output:** `intelligence/enriched-intelligence.yaml`

---

### **Step 2: Validate Enrichment**

**Check for each entity:**
- ✅ `fieldId` is RAW API field (no entity prefix)
- ✅ `entity` is target dimension (singular for arrays)
- ✅ `rawField` lists properties to extract
- ✅ `targetField` has same length as `rawField`
- ✅ `dataType` has same length as `targetField`
- ✅ `structureType` is correct (scalar/array/record/objectDump)

---

### **Step 3: Update ZephyrIntelligence Class**
```bash
python scripts/generate_intelligence_python.py  # Regenerate with enriched data
python scripts/append_intelligence_to_sdk.py    # Update SDK
```

---

### **Step 4: Update prepareZephyr Notebook**

**Changes needed:**
```python
# OLD (7 fields):
schema_data.append({
    "entity": entity_name,
    "fieldName": field_name,
    "fieldType": field_spec.get("type"),
    "isRequired": is_required,
    "description": description,
    "sourceEndpoint": endpoint,
    "intelligenceStatus": status
})

# NEW (15 fields - Jira pattern):
schema_data.append({
    "fieldId": field_id,
    "entity": entity_target,
    "structureType": structure_type,
    "rawField": raw_field_array,
    "targetField": target_field_array,
    "dataType": data_type_array,
    "description": description,
    "isRequired": is_required,
    "isNullable": is_nullable,
    "notes": notes,
    "group": group,
    "groupSortOrder": group_sort_order,
    "sourceEndpoint": endpoint,
    "apiStatus": status,
    "dimensionName": dimension_name,  # For arrays
    "bridgeName": bridge_name,        # For arrays
})
```

---

### **Step 5: Update prepareZephyr Delta Schema**

```python
# OLD schema (7 fields):
schema_table_schema = StructType([
    StructField("entity", StringType(), False),
    StructField("fieldName", StringType(), False),
    StructField("fieldType", StringType(), False),
    StructField("isRequired", BooleanType(), False),
    StructField("description", StringType(), True),
    StructField("sourceEndpoint", StringType(), False),
    StructField("intelligenceStatus", StringType(), True),
])

# NEW schema (15 fields - Jira pattern):
schema_table_schema = StructType([
    # Identity
    StructField("fieldId", StringType(), False),
    StructField("entity", StringType(), False),
    
    # Structure
    StructField("structureType", StringType(), False),
    StructField("rawField", ArrayType(StringType()), False),
    StructField("targetField", ArrayType(StringType()), False),
    StructField("dataType", ArrayType(StringType()), False),
    
    # Metadata
    StructField("description", StringType(), False),
    StructField("isRequired", BooleanType(), False),
    StructField("isNullable", BooleanType(), True),
    StructField("notes", StringType(), True),
    
    # Organization
    StructField("group", StringType(), False),
    StructField("groupSortOrder", IntegerType(), False),
    
    # API Intelligence
    StructField("sourceEndpoint", StringType(), False),
    StructField("apiStatus", StringType(), True),
    
    # Dimensional Modeling (nullable - only for arrays)
    StructField("dimensionName", StringType(), True),
    StructField("bridgeName", StringType(), True),
])
```

---

## 📋 Entity-by-Entity Enrichment Examples

### **1. cycle (Scalar Fields):**

**Field: `id`**
```yaml
fieldId: "id"
entity: "cycleId"           # Target column name
structureType: "scalar"
rawField: ["id"]
targetField: ["cycleId"]
dataType: ["int64"]
group: "identity"
```

**Field: `name`**
```yaml
fieldId: "name"
entity: "cycleName"         # Target column name
structureType: "scalar"
rawField: ["name"]
targetField: ["cycleName"]
dataType: ["text"]
group: "identity"
```

**Field: `cyclePhases` (Array of Objects)**
```yaml
fieldId: "cyclePhases"
entity: "cyclePhase"        # SINGULAR! (target dimension)
structureType: "array"
rawField: ["id", "name", "startDate", "endDate"]  # Properties per element
targetField: ["cyclePhaseId", "cyclePhaseName", "cyclePhaseStartDate", "cyclePhaseEndDate"]
dataType: ["array<int64>", "array<text>", "array<date>", "array<date>"]
group: "relationships"
dimensionName: "dimCyclePhase"
bridgeName: "bridgeCyclePhase"
```

---

### **2. requirement (Array of Scalars):**

**Field: `releaseIds`**
```yaml
fieldId: "releaseIds"
entity: "releaseId"         # SINGULAR!
structureType: "array"
rawField: ["releaseIds"]    # The field itself
targetField: ["releaseId"]  # Singular
dataType: ["array<int64>"]
group: "relationships"
dimensionName: "dimRelease"
bridgeName: "bridgeRequirementRelease"
```

---

### **3. requirement (Nested Array of Objects):**

**Field: `requirements`**
```yaml
fieldId: "requirements"
entity: "requirement"       # SINGULAR!
structureType: "array"
rawField: ["id", "name", "description"]
targetField: ["requirementId", "requirementName", "requirementDescription"]
dataType: ["array<int64>", "array<text>", "array<text>"]
group: "relationships"
dimensionName: "dimRequirement"
bridgeName: "bridgeRequirementFolder"
```

---

## 🎯 Validation Checklist

After enrichment, verify:

- [ ] All `fieldId` values match RAW API field names (no entity prefix)
- [ ] All array `entity` values are SINGULAR (cyclePhase, not cyclePhases)
- [ ] All `rawField` arrays match actual JSON schema properties
- [ ] All `targetField` arrays have same length as `rawField`
- [ ] All `dataType` arrays have same length as `targetField`
- [ ] All arrays have `dimensionName` and `bridgeName`
- [ ] All fields have `group` and `groupSortOrder`
- [ ] `fieldName` is REMOVED (redundant)
- [ ] `intelligenceStatus` renamed to `apiStatus`
- [ ] Schema follows Jira pattern exactly

---

## 🚀 Next Steps

1. **Run enrichment script** → Generate `enriched-intelligence.yaml`
2. **Review enrichment** → Validate all fields
3. **Regenerate Python class** → Update `ZephyrIntelligence`
4. **Update SDK** → Embed enriched intelligence
5. **Update prepareZephyr** → Use new schema structure
6. **Test in Fabric** → Verify tables created correctly
7. **Document lessons** → Add to `Core/memory/lessons/`

---

## 📈 Impact on Pipeline

### **Extract Stage (Future):**
```python
# Will use fieldId for API request
schema_df.filter(F.col("apiStatus") == "working").select("fieldId")
→ ["id", "name", "cyclePhases", "releaseId"]
```

### **Clean Stage (Future):**
```python
# Will use rawField → targetField for flattening
for field in schema:
    if field["structureType"] == "array":
        for i, prop in enumerate(field["rawField"]):
            df = df.withColumn(
                field["targetField"][i],
                F.col(field["fieldId"]).getItem(prop)
            )
```

### **Refine Stage (Future):**
```python
# Will use dimensionName/bridgeName for star schema
for field in schema:
    if field["bridgeName"]:
        create_dimension_table(field["dimensionName"])
        create_bridge_table(field["bridgeName"])
```

---

**Ready to enrich? Run:** `python scripts/enrich_intelligence_with_jira_pattern.py` 🚀






