# Naming Conventions - Extracted from Jira L6

## 🎯 Purpose
Document the EXACT naming conventions Jira uses so we can apply them to Zephyr (or override if needed).

---

## 📋 Jira's Actual Naming Patterns (From Code Analysis)

### **Pattern 1: Scalar Field → Target Column**

**Rule:** `fieldId` → `entity` (rename for clarity)

**Jira Examples:**
```python
# Simple rename
fieldId: "id"           → entity: "issueId"
fieldId: "key"          → entity: "jiraKey"
fieldId: "summary"      → entity: "summary"          # No change
fieldId: "description"  → entity: "description"      # No change

# Add context
fieldId: "created"      → entity: "dateTimeCreated"
fieldId: "updated"      → entity: "dateTimeUpdated"
```

**Convention:**
- IDs get prefixed: `id` → `{entity}Id`
- Keys get prefixed: `key` → `{entity}Key`
- Descriptive fields unchanged: `summary` → `summary`
- Dates get semantic prefix: `created` → `dateTimeCreated`

---

### **Pattern 2: Nested Object → Flattened Fields**

**Rule:** `fieldId.property` → `{fieldId}{PropertyCapitalized}`

**Jira Examples:**
```python
# issuetype object (line 324-338)
fieldId: "issuetype"
rawField: ["iconUrl", "id", "name"]
targetField: ["issueTypeIconUrl", "issueTypeId", "issueType"]

# priority object (line 343-360)
fieldId: "priority"
rawField: ["iconUrl", "id", "name"]
targetField: ["priorityIconUrl", "priorityId", "priority"]

# status object
fieldId: "status"
rawField: ["iconUrl", "id", "name"]
targetField: ["statusIconUrl", "statusId", "status"]
```

**Convention:**
- `{object}.iconUrl` → `{object}IconUrl` (capitalize property)
- `{object}.id` → `{object}Id`
- `{object}.name` → `{object}` (use object name only for the "main" field)

---

### **Pattern 3: Array Field → Dimension Name**

**Rule:** Pluralize API field → Singularize for dimension

**Jira Examples:**
```python
# components array (line 599-617)
fieldId: "components"      → entity: "component"      # SINGULAR!
rawField: ["id", "name"]
targetField: ["componentId", "component"]

# labels array (line 682-699)
fieldId: "labels"          → entity: "label"          # SINGULAR!
rawField: ["labels"]
targetField: ["label"]

# versions array (line 558-577)
fieldId: "versions"        → entity: "affectsVersion" # Semantic name!
rawField: ["id", "name", "released", "releaseDate"]
targetField: ["affectsVersionId", "affectsVersion", "released", "releaseDate"]

# fixVersions array (line 661-678)
fieldId: "fixVersions"     → entity: "fixVersion"     # SINGULAR!
rawField: ["id", "name", "released", "releaseDate"]
targetField: ["fixVersionId", "fixVersion", "released", "releaseDate"]
```

**Convention:**
- Pluralize → Singularize: `components` → `component`
- Keep semantic meaning: `versions` → `affectsVersion` (not just `version`)
- Array element properties: `{singular}{PropertyCapitalized}`

---

### **Pattern 4: Singularization Rules (From Jira)**

**Jira's singularization patterns:**
```python
# Standard -s removal
"components"    → "component"
"labels"        → "label"
"assignees"     → "assignee"
"watchers"      → "watcher"

# -es removal
"phases"        → "phase"

# -ies → -y
"categories"    → "category"

# Irregular (custom names)
"versions"      → "affectsVersion"  # Semantic naming
"fixVersions"   → "fixVersion"
"people"        → "person"          # Irregular plural
```

---

## 🔧 Applying to Zephyr

### **Example 1: cycle.id (Scalar)**

**Input (from probe):**
```json
{
  "entity": "cycle",
  "fieldName": "id",
  "type": "integer"
}
```

**Apply Jira Pattern:**
```python
fieldId: "id"
entity: "cycleId"           # ← Pattern 1: id → {entity}Id
rawField: ["id"]
targetField: ["cycleId"]
dataType: ["int64"]
```

**Decision:** Follow Jira (add `cycle` prefix for clarity)

---

### **Example 2: cycle.cyclePhases (Array of Objects)**

**Input (from probe):**
```json
{
  "entity": "cycle",
  "fieldName": "cyclePhases",
  "type": "array",
  "items": {
    "properties": {
      "id": {"type": "integer"},
      "name": {"type": "string"},
      "startDate": {"type": "string"},
      "endDate": {"type": "string"}
    }
  }
}
```

**Apply Jira Pattern:**
```python
fieldId: "cyclePhases"                # RAW API field (plural)
entity: "cyclePhase"                  # ← Pattern 3: Singularize
rawField: ["id", "name", "startDate", "endDate"]
targetField: [
    "cyclePhaseId",                   # ← Pattern 3: {singular}Id
    "cyclePhaseName",                 # ← Pattern 3: {singular}Name (or just name?)
    "cyclePhaseStartDate",            # ← Pattern 3: {singular}StartDate
    "cyclePhaseEndDate"               # ← Pattern 3: {singular}EndDate
]
dataType: ["array<int64>", "array<text>", "array<date>", "array<date>"]
```

**Decision Points:**
- ✅ Singularize: `cyclePhases` → `cyclePhase` (Jira pattern)
- ❓ Property naming: `cyclePhaseName` or just `name`?

**Jira precedent:**
```python
# Jira DOES prefix for clarity
"componentId", "component"           # id gets prefix, name doesn't
"affectsVersionId", "affectsVersion" # id gets prefix, name doesn't
```

**But also:**
```python
# Jira KEEPS property names when flattening dates
"releaseDate"  # NOT "affectsVersionReleaseDate"
```

**Recommendation for Zephyr:**
```python
targetField: [
    "cyclePhaseId",        # ✅ Prefix for ID
    "cyclePhaseName",      # ⚠️ Could be "name" (like Jira)
    "startDate",           # ✅ Keep short (like Jira's releaseDate)
    "endDate"              # ✅ Keep short
]
```

**OR (more explicit):**
```python
targetField: [
    "cyclePhaseId",        # ✅ Prefix for ID
    "cyclePhaseName",      # ✅ Explicit
    "cyclePhaseStartDate", # ✅ Explicit
    "cyclePhaseEndDate"    # ✅ Explicit
]
```

---

### **Example 3: requirement.releaseIds (Array of Scalars)**

**Input (from probe):**
```json
{
  "entity": "requirement",
  "fieldName": "releaseIds",
  "type": "array",
  "items": {"type": "integer"}
}
```

**Apply Jira Pattern:**
```python
fieldId: "releaseIds"          # RAW API field (plural)
entity: "releaseId"            # ← Singularize (dimension name)
rawField: ["releaseIds"]       # The field itself
targetField: ["releaseId"]     # ← Singular
dataType: ["array<int64>"]
```

---

## 🎯 Naming Convention Decision Matrix

| Scenario | API Field | Entity (Target) | Example |
|----------|-----------|-----------------|---------|
| **Scalar ID** | `id` | `{parent}Id` | `id` → `cycleId` |
| **Scalar field** | `name` | `{parent}Name` or `name` | `name` → `cycleName` or `name` |
| **Scalar date** | `created` | `dateTime{Field}` | `created` → `dateTimeCreated` |
| **Object** | `status` | `status` | `status` (dimension name) |
| **Object.id** | `status.id` | `statusId` | Flattened |
| **Object.name** | `status.name` | `status` | Flattened (main field) |
| **Array (plural)** | `cyclePhases` | `cyclePhase` | Singular |
| **Array[].id** | `cyclePhases[].id` | `cyclePhaseId` | Prefix + Id |
| **Array[].prop** | `cyclePhases[].name` | `cyclePhaseName` or `name` | ❓ Decision needed |

---

## ❓ Decisions Needed for Zephyr

### **Decision 1: Array Property Naming**

**Option A: Full Prefix (Explicit)**
```python
targetField: ["cyclePhaseId", "cyclePhaseName", "cyclePhaseStartDate", "cyclePhaseEndDate"]
```
**Pro:** Crystal clear, no ambiguity  
**Con:** Verbose

**Option B: Selective Prefix (Jira-like)**
```python
targetField: ["cyclePhaseId", "name", "startDate", "endDate"]
```
**Pro:** Shorter, Jira does this for some fields  
**Con:** Ambiguous (which entity's name?)

**Recommendation:** **Option A** for arrays (explicit), **Option B** for objects (Jira pattern)

---

### **Decision 2: Date Field Naming**

**Option A: Keep API Names**
```python
"startDate", "endDate"
```

**Option B: Add Semantic Prefix**
```python
"cyclePhaseStartDate", "cyclePhaseEndDate"
```

**Jira does BOTH:**
- `releaseDate` (short - no prefix)
- `dateTimeCreated`, `dateTimeUpdated` (semantic prefix)

**Recommendation:** **Add prefix for clarity** (arrays have multiple entities)

---

### **Decision 3: Singularization Rules**

**Zephyr-specific terms to define:**
```python
"cyclePhases"  → "cyclePhase"       # ✅ Standard -s removal
"requirements" → "requirement"      # ✅ Standard -s removal
"categories"   → "category"         # ✅ -ies → -y
"releases"     → "release"          # ✅ Standard -s removal
```

**Custom/semantic names?**
```python
"cyclePhases"  → "phase" or "cyclePhase"?
"requirements" → "testRequirement" or "requirement"?
```

**Recommendation:** Keep entity context: `cyclePhase`, `requirement` (not just `phase`)

---

## 📋 Proposed Zephyr Naming Standard

### **Rule Set:**

1. **Scalar ID:** `id` → `{entity}Id`
2. **Scalar Field:** Keep semantic: `name` → `{entity}Name`, `description` → `description`
3. **Dates:** Keep short for scalars, prefix for array elements
4. **Objects:** `{object}.property` → `{object}{Property}`
5. **Arrays:** Pluralize → Singularize for dimension name
6. **Array Elements:** `{array}[].property` → `{singular}{Property}` (full prefix for clarity)

### **Examples Applied:**

```python
# cycle.id (scalar)
fieldId: "id" → entity: "cycleId"

# cycle.name (scalar)
fieldId: "name" → entity: "cycleName"

# cycle.cyclePhases[].id (array element)
fieldId: "cyclePhases" → entity: "cyclePhase"
rawField: ["id"] → targetField: ["cyclePhaseId"]

# cycle.cyclePhases[].name (array element)
rawField: ["name"] → targetField: ["cyclePhaseName"]

# cycle.cyclePhases[].startDate (array element)
rawField: ["startDate"] → targetField: ["cyclePhaseStartDate"]
```

---

## 🎯 Implementation Approach

### **Option A: Hardcode Jira Conventions** (Automated)
```python
def generate_target_field(entity, field_name, property_name=None):
    """Apply Jira conventions automatically."""
    if property_name:
        # Array element property
        singular = singularize(field_name)
        if property_name == "id":
            return f"{singular}Id"
        elif property_name == "name":
            return f"{singular}Name"  # or just "name"?
        else:
            return f"{singular}{property_name.capitalize()}"
    else:
        # Scalar field
        if field_name == "id":
            return f"{entity}Id"
        elif field_name == "name":
            return f"{entity}Name"
        else:
            return field_name
```

### **Option B: Convention File + Override** (Flexible)
```yaml
# conventions.yaml
naming_rules:
  scalar_id: "{entity}Id"
  scalar_name: "{entity}Name"
  array_singularize: true
  array_element_prefix: true
  
overrides:
  cyclePhases:
    entity: "cyclePhase"  # Override if needed
    properties:
      id: "cyclePhaseId"
      name: "phaseName"   # Override: shorter name
```

### **Option C: User Review Required** (Manual)
```python
# Generate defaults, user reviews/edits
enriched = generate_with_defaults()
print_for_review(enriched)
# User edits YAML, then re-import
```

---

## 🎯 My Recommendation

**Use Option A (Jira conventions) with these specific rules:**

```python
NAMING_RULES = {
    # Scalars
    "scalar_id": "{entity}Id",           # id → cycleId
    "scalar_name": "{entity}Name",       # name → cycleName
    "scalar_date": "{field}",            # keep as-is
    
    # Arrays
    "array_entity": "singularize",       # cyclePhases → cyclePhase
    "array_element_id": "{singular}Id",  # cyclePhase + id → cyclePhaseId
    "array_element_name": "{singular}Name",  # EXPLICIT
    "array_element_date": "{singular}{Property}",  # EXPLICIT
}
```

**Result for cycle.cyclePhases:**
```python
fieldId: "cyclePhases"
entity: "cyclePhase"
rawField: ["id", "name", "startDate", "endDate"]
targetField: ["cyclePhaseId", "cyclePhaseName", "cyclePhaseStartDate", "cyclePhaseEndDate"]
```

---

## ❓ Your Decision

**Do you want:**

**A)** Follow Jira conventions exactly (automated, proven)  
**B)** Define custom Zephyr conventions (more control)  
**C)** Generate defaults, you review/edit manually (safest)

**What feels most SPECTRA-grade to you?** 🎯






