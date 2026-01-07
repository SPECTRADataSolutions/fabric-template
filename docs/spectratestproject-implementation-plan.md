# SpectraTestProject - Comprehensive Synthetic Data Implementation Plan

**Date:** 2025-12-08  
**Status:** 🟢 Ready to Implement  
**Objective:** Build comprehensive test data to reverse-engineer schema, validations, and structures

---

## 🎯 Goal

**Create comprehensive synthetic data in SpectraTestProject (ID 45) to discover:**
1. ✅ **Data Structures** - Scalar, record, array, nested objects
2. ✅ **Data Validations** - Required fields, enum values, format rules, constraints
3. ✅ **Complete Schema** - Field types, nullability, relationships
4. ✅ **API Behaviours** - What fields accepted, validation error patterns

---

## 🔄 Discovery Process

### Step 1: Create with Maximum Data
- Create entity with **ALL possible fields** populated
- Use realistic, comprehensive values
- Capture creation response

### Step 2: Analyze Response
- Compare sent vs received fields
- Identify what API accepts/transforms/ignores
- Discover nested structures

### Step 3: Test Variations
- Create multiple entities with different enum values
- Test optional fields (include vs omit)
- Test nested structures (arrays, records)

### Step 4: Test Validations
- Try invalid data (wrong types, missing required)
- Capture validation errors
- Infer constraints from error messages

### Step 5: Generate Schema
- Combine all discoveries
- Generate comprehensive schema definitions
- Document validation rules

---

## 📋 Implementation Strategy

### Phase 1: Comprehensive Test Data Templates

**File:** `scripts/data/comprehensive_test_data.yaml` (or JSON)

**Define:**
- All entity types with comprehensive field definitions
- Multiple variations for each entity (test enum values)
- Realistic synthetic data for all fields

### Phase 2: Builder Script

**File:** `scripts/build_comprehensive_spectra_test_project.py`

**Process:**
1. Load test data templates
2. Create entities with comprehensive data
3. Capture all API responses
4. Store responses for analysis

### Phase 3: Schema Discovery

**File:** `scripts/discover_schema_from_comprehensive_data.py`

**Process:**
1. Analyze all captured responses
2. Compare sent vs received fields
3. Infer field types, structures, validations
4. Generate schema definitions

### Phase 4: Validation Discovery

**File:** `scripts/discover_validations_via_errors.py`

**Process:**
1. Try invalid data combinations
2. Capture validation errors
3. Analyze error messages
4. Document constraints

---

## 🏗️ Entity Coverage

### 1. Project (SpectraTestProject - ID 45)
- ✅ Already exists
- 🔄 Populate all fields if editable
- 🔄 Test project-level configurations

### 2. Releases (Multiple)
- Create 3-5 releases with different configurations:
  - Different status values (DRAFT, ACTIVE, COMPLETED)
  - Different date ranges
  - All optional fields populated
  - Different metadata

### 3. Cycles (Multiple per Release)
- Create 3-5 cycles per release:
  - Different phase configurations (test array structure)
  - Different status values
  - All optional fields
  - Different date configurations

### 4. Test Repository Folders (Folder Tree)
- Create nested folder hierarchy:
  - Root folder
  - Multiple levels deep
  - All folder metadata
  - Test folder structure

### 5. Testcases (Multiple per Folder)
- Create 5-10 testcases:
  - Different testcase types (MANUAL, AUTOMATED)
  - Different priorities (HIGH, MEDIUM, LOW)
  - All custom fields
  - All metadata fields
  - Links to requirements (if applicable)

### 6. Executions (Multiple per Testcase)
- Create executions for all status types:
  - PASSED
  - FAILED
  - BLOCKED
  - NOT_EXECUTED
  - Different date configurations
  - All execution metadata

### 7. Requirements (If applicable)
- Create requirements:
  - Link to testcases
  - All requirement metadata
  - Test requirement relationships

---

## 📊 Data Structure Discovery

### Scalar Fields:
- ✅ String - `"name": "Test Name"`
- ✅ Integer - `"id": 123`
- ✅ Boolean - `"isActive": true`
- ✅ Date - `"startDate": "2025-01-01"`
- ✅ DateTime - `"createdOn": "2025-12-08T10:00:00Z"`
- ✅ Enum - `"status": "ACTIVE"` (discover all valid values)

### Record Fields (Nested Objects):
- ✅ Single Record - `"dates": {"start": "...", "end": "..."}`
- ✅ Nested Records - `"owner": {"id": 123, "name": "User"}`
- ✅ Deep Nesting - Test how deep structures can go

### Array Fields:
- ✅ Array of Scalars - `"tags": ["tag1", "tag2"]`
- ✅ Array of Records - `"cyclePhases": [{"name": "Phase 1"}, ...]`
- ✅ Nested Arrays - `"testSuites": [{"tests": [...]}]`

### Discovery Method:
1. Create entity with comprehensive nested structures
2. Analyze response to see what's accepted
3. Test variations to find limits

---

## 🎯 Validation Discovery

### Required Fields:
- Create entity **without** field → Error if required
- Create entity **with** field → Success if optional or required

### Enum Values:
- Try all suspected values → See which accepted
- Try invalid value → Error shows valid options

### Format Rules:
- Try invalid date format → Error shows expected format
- Try invalid email/URL → Error shows validation rule

### Range Constraints:
- Try value too high/low → Error shows valid range
- Try negative when not allowed → Error message

### Relationship Constraints:
- Try invalid foreign key → Error shows valid relationships
- Try circular reference → Error shows constraint

---

## 🔧 Next Steps

### Immediate Actions:

1. **Design Test Data Templates**
   - Create YAML/JSON templates for all entity types
   - Define comprehensive field values
   - Include variations for enum testing

2. **Build Comprehensive Builder Script**
   - `scripts/build_comprehensive_spectra_test_project.py`
   - Create all entities with comprehensive data
   - Capture all responses

3. **Build Schema Discovery Script**
   - `scripts/discover_schema_from_comprehensive_data.py`
   - Analyze responses
   - Generate schema definitions

4. **Build Validation Discovery Script**
   - `scripts/discover_validations_via_errors.py`
   - Test invalid data
   - Document constraints

---

## ✅ Success Criteria

1. **Complete Coverage:**
   - All entity types have comprehensive test data
   - All enum values tested
   - All nested structures explored

2. **Schema Discovered:**
   - Field types identified (scalar, record, array)
   - Nullability determined (required vs optional)
   - Enum values documented

3. **Validations Discovered:**
   - Validation rules identified
   - Constraints documented
   - Error patterns understood

4. **Prepare Stage Ready:**
   - Schema generated automatically
   - Prepare stage uses comprehensive schema
   - No manual schema entry needed

---

**Ready to implement?** Let's start with test data templates, then build the comprehensive builder script!

