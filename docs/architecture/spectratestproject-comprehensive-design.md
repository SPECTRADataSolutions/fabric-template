# SpectraTestProject - Comprehensive Synthetic Data Builder

**Date:** 2025-12-08  
**Objective:** Build comprehensive synthetic test data to reverse-engineer schema, validations, and data structures

---

## 🎯 Purpose

**Use comprehensive synthetic data to discover:**
1. **Data Validations** - What constraints exist? (required fields, enum values, format rules, ranges)
2. **Data Structures** - Scalar, record, array, nested objects, relationships
3. **Schema Definitions** - Complete field-level metadata (types, nullability, constraints)
4. **API Behaviours** - What fields are accepted? What triggers validation errors?

---

## 🏗️ SPECTRA-Grade Approach

### Core Principle:
> **"Create comprehensive test data → Observe API responses → Reverse-engineer schema and validations"**

By creating entities with **every possible field populated**, we can:
- ✅ See what fields the API accepts
- ✅ Infer which fields are required vs optional
- ✅ Discover enum values (status types, etc.)
- ✅ Understand nested structures (records, arrays)
- ✅ Identify validation rules (format, ranges, relationships)

---

## 📋 Entity Coverage Plan

### Hierarchy to Build:
1. **Project** (SpectraTestProject - ID 45)
   - ✅ Already exists
   - 🔄 Populate with ALL fields

2. **Releases** (Multiple releases per project)
   - Different status values (draft, active, completed)
   - Different date configurations
   - All optional fields populated

3. **Cycles** (Multiple cycles per release)
   - Different phase configurations
   - All status types
   - All metadata fields

4. **Test Repository Folders** (Folder tree structure)
   - Nested folder hierarchy
   - All folder metadata

5. **Testcases** (Multiple testcases per folder)
   - Different testcase types
   - All custom fields
   - All metadata

6. **Executions** (Multiple executions per testcase)
   - All execution status types (Passed, Failed, Blocked, Not Executed)
   - All execution metadata
   - Different date configurations

7. **Requirements** (If applicable)
   - Requirement entities
   - Links to testcases

---

## 🎨 Synthetic Data Strategy

### Field Coverage:
- **Every field** populated (if possible)
- **All enum values** tested (create multiple entities with different values)
- **All nested structures** explored (records, arrays)
- **Edge cases** included (nulls where allowed, boundary values)

### Data Quality:
- **Realistic** - Data that makes sense
- **Deterministic** - Same data every time
- **Comprehensive** - Covers all variations
- **Appropriately configured** - Respects relationships and constraints

---

## 🔧 Implementation Design

### Phase 1: Comprehensive Test Data Builder

**Tool:** `scripts/build_comprehensive_spectra_test_project.py`

**Process:**
1. **Delete existing SpectraTestProject** (if rebuild needed)
2. **Create fresh project** with ALL fields populated
3. **Create multiple entities** for each type (to test enum variations)
4. **Capture ALL API responses** (creation responses, GET responses)
5. **Store responses** for schema analysis

### Phase 2: Schema Discovery via Creation

**Tool:** `scripts/discover_schema_via_comprehensive_data.py`

**Process:**
1. **Create entities** with comprehensive data
2. **Capture creation responses** (what API returns)
3. **Try variations** (different enum values, optional fields)
4. **Analyze responses** to infer:
   - Field types
   - Required vs optional
   - Enum values
   - Nested structures
   - Validation rules

### Phase 3: Validation Rule Discovery

**Tool:** `scripts/discover_validations_via_errors.py`

**Process:**
1. **Try invalid data** (wrong types, missing required fields, invalid enum values)
2. **Capture validation errors**
3. **Analyze error messages** to infer validation rules
4. **Document constraints** (min/max values, format requirements, etc.)

### Phase 4: Schema Generation

**Tool:** `scripts/generate_schema_from_comprehensive_data.py`

**Process:**
1. **Analyze all captured responses**
2. **Infer schema definitions**:
   - Field types (scalar, record, array)
   - Nullability (required vs optional)
   - Enum values
   - Nested structures
3. **Generate Prepare stage schema** format
4. **Document validation rules**

---

## 📊 Entity-Specific Strategies

### Project (SpectraTestProject):
```python
project_data = {
    "name": "SpectraTestProject",
    "description": "Comprehensive test project for SPECTRA schema discovery",
    "key": "SPECTRA",
    # ... ALL fields populated
    # Test variations:
    # - Different project types
    # - Different status values
    # - All metadata fields
}
```

### Releases:
```python
releases = [
    {
        "name": "Release 1 - Draft",
        "status": "DRAFT",  # Test enum value
        "startDate": "2025-01-01",
        "releaseDate": "2025-12-31",
        # ... ALL fields
    },
    {
        "name": "Release 2 - Active",
        "status": "ACTIVE",  # Different enum value
        # ... ALL fields
    },
    # ... More variations to test all enum values
]
```

### Cycles:
```python
cycles = [
    {
        "name": "Cycle 1 - All Phases",
        "status": "ACTIVE",
        "cyclePhases": [  # Test array structure
            {"name": "Phase 1", "status": "PASSED"},
            {"name": "Phase 2", "status": "FAILED"},
        ],
        # ... ALL fields
    },
    # ... More variations
]
```

### Testcases:
```python
testcases = [
    {
        "name": "Testcase 1 - Manual",
        "testcaseType": "MANUAL",  # Test enum
        "priority": "HIGH",  # Test enum
        "customFields": {  # Test record structure
            "field1": "value1",
            "field2": 123,
        },
        # ... ALL fields
    },
    # ... More variations for all testcase types
]
```

### Executions:
```python
executions = [
    {
        "status": "PASSED",  # Test enum
        "executedOn": "2025-12-08T10:00:00Z",
        "executedBy": "user_id",
        # ... ALL fields
    },
    {
        "status": "FAILED",  # Different enum
        # ... ALL fields
    },
    # ... All status types (Passed, Failed, Blocked, Not Executed)
]
```

---

## 🔍 Discovery Process

### Step 1: Create with Comprehensive Data
- Create entity with ALL fields populated
- Capture creation response
- Check what fields are returned (vs what we sent)

### Step 2: Analyze Response Structure
- **Fields present** → API accepts them
- **Fields missing** → Might be read-only or invalid
- **Different structure** → API transforms data

### Step 3: Test Variations
- Create multiple entities with different enum values
- Test optional fields (include vs omit)
- Test nested structures (arrays, records)

### Step 4: Test Validations
- Try invalid data (wrong types, missing required fields)
- Capture validation errors
- Infer constraints from error messages

### Step 5: Generate Schema
- Combine all discoveries
- Generate comprehensive schema definitions
- Document validation rules

---

## 📋 Data Structure Discovery

### Scalar Fields:
- **String** - `"name": "Test Name"`
- **Integer** - `"id": 123`
- **Boolean** - `"isActive": true`
- **Date** - `"startDate": "2025-01-01"`
- **DateTime** - `"createdOn": "2025-12-08T10:00:00Z"`

### Record Fields (Nested Objects):
- **Single Record** - `"dates": {"start": "2025-01-01", "end": "2025-12-31"}`
- **Nested Records** - `"owner": {"id": 123, "name": "User", "email": "user@example.com"}`

### Array Fields:
- **Array of Scalars** - `"tags": ["tag1", "tag2"]`
- **Array of Records** - `"cyclePhases": [{"name": "Phase 1"}, {"name": "Phase 2"}]`
- **Nested Arrays** - `"testSuites": [{"tests": [{"id": 1}]}]`

### Discovery Methods:
1. **Create entity** with comprehensive data
2. **Analyze response** structure
3. **Try variations** to test edge cases
4. **Document findings** in schema

---

## 🎯 Validation Discovery

### Required Fields:
- Try creating entity **without** field → Error if required
- Try creating entity **with** field → Success if optional or required

### Enum Values:
- Try different values → See which are accepted
- Try invalid value → Error message shows valid options

### Format Rules:
- Try invalid date format → Error shows expected format
- Try invalid email format → Error shows validation rule

### Range Constraints:
- Try value too high/low → Error shows valid range
- Try negative when not allowed → Error message

### Relationship Constraints:
- Try invalid foreign key → Error shows valid relationships
- Try circular reference → Error shows constraint

---

## 📊 Output: Comprehensive Schema

### Schema Definitions Include:
- **Field Types** - Scalar, record, array
- **Data Types** - String, int, bool, date, datetime, etc.
- **Nullability** - Required vs optional
- **Enum Values** - All valid options
- **Validation Rules** - Format, ranges, constraints
- **Nested Structures** - Records, arrays, relationships
- **Relationships** - Foreign keys, references

### Use Cases:
1. **Prepare Stage** - Generate `prepare._schema` table
2. **Extract Stage** - Know what fields to extract
3. **Clean Stage** - Validate against known constraints
4. **Transform Stage** - Understand relationships for joins

---

## 🔧 Implementation Files

### New Files:
1. **`scripts/build_comprehensive_spectra_test_project.py`**
   - Builds complete test project with all entities
   - Populates all fields with comprehensive data
   - Creates variations to test enum values

2. **`scripts/discover_schema_via_comprehensive_data.py`**
   - Analyzes created entities
   - Discovers field types, structures, validations
   - Generates schema definitions

3. **`scripts/discover_validations_via_errors.py`**
   - Tests invalid data
   - Captures validation errors
   - Documents constraints

4. **`scripts/generate_schema_from_comprehensive_data.py`**
   - Combines all discoveries
   - Generates Prepare stage schema format
   - Documents validation rules

### Updated Files:
1. **`spectraSDK.Notebook`**
   - Add `PrepareStageHelpers.extract_introspection_samples()`
   - Add `PrepareStageHelpers.introspect_schema_from_samples()`
   - Add comprehensive schema generation methods

---

## ✅ Success Criteria

1. **Complete Coverage:**
   - All entity types have comprehensive test data
   - All enum values tested
   - All nested structures explored

2. **Schema Discovery:**
   - Field types identified (scalar, record, array)
   - Nullability determined (required vs optional)
   - Enum values documented

3. **Validation Discovery:**
   - Validation rules identified
   - Constraints documented
   - Error patterns understood

4. **Prepare Stage Integration:**
   - Schema generated automatically from test data
   - Prepare stage uses comprehensive schema
   - No manual schema entry needed

---

## 🎯 Next Steps

1. **Design comprehensive test data templates** (YAML or JSON)
2. **Build entity creation scripts** (with all fields populated)
3. **Implement schema discovery logic** (analyze responses)
4. **Test validation rules** (try invalid data)
5. **Generate Prepare stage schema** (automatic from discoveries)

---

**Version:** 1.0.0  
**Date:** 2025-12-08  
**Status:** 🟡 Design Phase

