# Prepare Stage SDK Playbook - Zephyr

**Version:** 1.0.0  
**Date:** 2025-12-08  
**Status:** 🟢 Ready for Prepare Stage Development  
**Stage:** Prepare (Stage 2 of 7)

---

## 🎯 Purpose

This playbook documents **what has been completed** for the Prepare stage in the SDK and **what's ready** for Prepare stage development. This is a **handoff document** for the Prepare stage chat.

---

## ✅ What's Been Completed (Source Stage Chat)

### **1. SDK Helper Classes Available**

#### **`SchemaDiscoveryHelpers` (NEW - Reusable)**
**Location:** `spectraSDK.Notebook/notebook_content.py`

**Status:** ✅ **Complete and Reusable**

Generic schema discovery helpers that work for **any source system** (not just Zephyr):

- ✅ `create_entity_comprehensively()` - Generic entity creation (any REST API)
- ✅ `analyze_field_structure()` - Generic field analysis (scalar, record, array)
- ✅ `compare_payload_response()` - Compare sent vs received (infer transformations)
- ✅ `discover_schema_from_responses()` - Generic schema discovery
- ✅ `test_validation_rules()` - Test validation rules with invalid data

**Usage:**
```python
from SchemaDiscoveryHelpers import SchemaDiscoveryHelpers

# Works for any REST API
entity_data, entity_id, error = SchemaDiscoveryHelpers.create_entity_comprehensively(
    base_url=base_url,
    endpoint="/release",
    payload=payload,
    headers=headers,
    logger=log
)

# Generic field analysis
schema = SchemaDiscoveryHelpers.analyze_field_structure("fieldName", field_value)

# Discover schema from responses
schemas = SchemaDiscoveryHelpers.discover_schema_from_responses(
    responses=[response1, response2, ...],
    entity_type="release",
    logger=log
)
```

---

### **2. Comprehensive Test Data Builder (Reusable)**

**Files:**
- ✅ `scripts/build_comprehensive_test_data_reusable.py` - Template-driven builder
- ✅ `scripts/discover_schema_from_comprehensive_data.py` - Schema discovery
- ✅ `scripts/data/comprehensive_test_data.yaml` - Zephyr template

**Status:** ✅ **Complete and Reusable**

**Purpose:** Build comprehensive synthetic test data for schema discovery

**Features:**
- ✅ Template-driven (works for any source system)
- ✅ Uses SDK `SchemaDiscoveryHelpers`
- ✅ Variable resolution (environment/Variable Library)
- ✅ Captures all API responses for analysis

**Usage:**
```bash
# Build comprehensive test data
python scripts/build_comprehensive_test_data_reusable.py \
  --template scripts/data/zephyr_comprehensive_test_data.yaml

# Discover schemas from captured responses
python scripts/discover_schema_from_comprehensive_data.py
```

---

### **3. Prepare Stage Architecture Decisions**

#### **Sample Extraction Ownership**

**Decision:** ✅ **Prepare Stage Owns Sample Extraction**

**Rationale:**
- Source stage: Validates connectivity and access (doesn't need samples)
- Prepare stage: Needs samples for schema introspection (core responsibility)
- Clear separation of concerns
- Self-contained stages

**Documentation:**
- ✅ `docs/SPECTRA-GRADE-SAMPLE-EXTRACTION.md` - Complete architecture decision
- ✅ `docs/PREPARE-STAGE-SAMPLE-EXTRACTION-DESIGN.md` - Design analysis

**Implication for Prepare Stage:**
```python
# Prepare stage extracts samples for schema introspection
test_project_id = session.variables.get("TEST_PROJECT_ID")  # 45 (SpectraTestProject)

samples = PrepareStageHelpers.extract_introspection_samples(
    spark=spark,
    delta=session.delta,
    logger=log,
    base_url=base_url,
    api_token=api_token,
    test_project_id=test_project_id,
    sample_limit=10
)

# Creates: prepare.sampleProjects, prepare.sampleReleases, 
#          prepare.sampleCycles, prepare.sampleExecutions, prepare.sampleTestcases
```

---

### **4. Prepare Stage Documentation**

**Status:** ✅ **Design Documents Complete**

**Documents:**
- ✅ `docs/prepare/README.md` - Prepare stage overview
- ✅ `docs/prepare/PREPARE-STAGE-SCHEMA-DESIGN.md` - Complete schema design specification
- ✅ `docs/prepare/PREPARE-STAGE-FRESH-DESIGN.md` - Fresh design approach
- ✅ `docs/prepare/PREPARE-STAGE-COMPARISON.md` - Comparison with Jira pattern
- ✅ `docs/prepare/PREPARE-STAGE-COMPLETE.md` - Completion status

**Key Design Decisions:**
- Schema table structure defined
- Entity hierarchy & grouping specified
- Structure type patterns (scalar, record, array) documented
- Schema generation workflow designed
- Validation rules documented

---

### **5. Test Project Configuration**

**Status:** ✅ **Ready for Use**

**SpectraTestProject (ID 45):**
- ✅ Locked in Variable Library (`TEST_PROJECT_ID = 45`)
- ✅ Created via API (see `scripts/build_comprehensive_spectra_test_project.py`)
- ✅ Comprehensive synthetic data ready
- ✅ All hierarchy levels populated

**Variable Library:**
- ✅ `TEST_PROJECT_ID` - Locked to 45
- ✅ Environment-specific constant (not pipeline parameter)

---

## 📋 What's Ready for Prepare Stage Development

### **1. SDK Helpers to Create**

**Required for Prepare Stage:**

#### **`PrepareStageHelpers` Class**
**Location:** Add to `spectraSDK.Notebook/notebook_content.py`

**Methods Needed:**
```python
class PrepareStageHelpers:
    @staticmethod
    def extract_introspection_samples(
        spark: SparkSession,
        delta: 'DeltaTable',
        logger: 'SPECTRALogger',
        base_url: str,
        api_token: str,
        test_project_id: int,
        sample_limit: int = 10
    ) -> Dict[str, int]:
        """Extract samples from SpectraTestProject for schema introspection.
        
        Creates:
        - prepare.sampleProjects
        - prepare.sampleReleases
        - prepare.sampleCycles
        - prepare.sampleExecutions
        - prepare.sampleTestcases
        """
        # Uses SchemaDiscoveryHelpers.create_entity_comprehensively()
        # Or SourceStageHelpers.validate_api_resource_access() to fetch samples
        
    @staticmethod
    def introspect_schema_from_samples(
        spark: SparkSession,
        samples_tables: List[str],
        logger: 'SPECTRALogger'
    ) -> List[Dict[str, Any]]:
        """Introspect schema from sample Delta tables.
        
        Uses SchemaDiscoveryHelpers.analyze_field_structure() for each field.
        """
        # Analyze Delta table schemas
        # Infer field types, nullability, arrays, nested objects
        # Generate Prepare stage schema format
        
    @staticmethod
    def create_prepare_schema_table(
        spark: SparkSession,
        delta: 'DeltaTable',
        schema_data: List[Dict[str, Any]],
        logger: 'SPECTRALogger'
    ) -> None:
        """Create prepare._schema Delta table from introspected schema."""
        # Write schema data to Delta table
        # Register in Spark metastore
        
    @staticmethod
    def create_prepare_endpoints_table(
        spark: SparkSession,
        delta: 'DeltaTable',
        source_endpoints: DataFrame,
        logger: 'SPECTRALogger'
    ) -> None:
        """Create prepare._endpoints table from source.endpoints."""
        # Filter/transform source.endpoints for Extract stage
        # Write to prepare._endpoints
        
    @staticmethod
    def create_prepare_status_map_table(
        spark: SparkSession,
        delta: 'DeltaTable',
        logger: 'SPECTRALogger'
    ) -> None:
        """Create prepare._statusMap table with status mappings."""
        # Define status mappings for Zephyr
        # Write to prepare._statusMap
```

---

### **2. Prepare Stage Notebook**

**Notebook:** `2-prepare/prepareZephyr.Notebook/notebook_content.py`

**Status:** ⚠️ **Needs Update** (was excluded from Source stage push due to errors)

**Structure (SPECTRA 7-Stage Pattern):**
```python
# ══ 1. PARAMETERS ═══════════════════════════════════════════════════ SPECTRA
bootstrap: bool = True
backfill: bool = False
test: bool = False

# ══ 2. CONTEXT ═══════════════════════════════════════════════════════ SPECTRA
session = NotebookSession("zephyrVariables")
session.load_context(bootstrap, backfill, test=test)

# ══ 3. INITIALIZE ═══════════════════════════════════════════════════ SPECTRA
log = session.initialize()

# ══ 4. EXECUTE ══════════════════════════════════════════════════════ SPECTRA
# Extract introspection samples
test_project_id = session.variables.get("TEST_PROJECT_ID")  # 45

samples = PrepareStageHelpers.extract_introspection_samples(
    spark=spark,
    delta=session.delta,
    logger=log,
    base_url=session.ctx["full_url"],
    api_token=session.variables.get_secret("API_TOKEN"),
    test_project_id=test_project_id
)

# Introspect schema
schema_data = PrepareStageHelpers.introspect_schema_from_samples(
    spark=spark,
    samples_tables=["prepare.sampleProjects", "prepare.sampleReleases", ...],
    logger=log
)

# Create Prepare stage tables
PrepareStageHelpers.create_prepare_schema_table(...)
PrepareStageHelpers.create_prepare_endpoints_table(...)
PrepareStageHelpers.create_prepare_status_map_table(...)

# ══ 5. VALIDATE ═════════════════════════════════════════════════════ SPECTRA
session.validate()

# ══ 6. RECORD ═══════════════════════════════════════════════════════ SPECTRA
session.record()

# ══ 7. FINALISE ═════════════════════════════════════════════════════ SPECTRA
session.finalise()
```

---

### **3. Prepare Stage Contracts**

**Status:** ⚠️ **Needs Creation**

**Required Files:**
- ✅ `contracts/prepare.contract.yaml` - Prepare stage contract
- ✅ `manifests/prepare.manifest.yaml` - Prepare stage manifest

**Design Ready:**
- See `docs/SPECTRA-GRADE-SAMPLE-EXTRACTION.md` for contract structure

---

## 🔗 Dependencies from Source Stage

### **Source Stage Outputs (Ready for Prepare Stage):**

1. **`source.endpoints`** - Complete endpoint catalog (228 endpoints)
   - Used to create `prepare._endpoints`

2. **`source.portfolio`** - Source system metadata
   - Used for context and validation

3. **`source.config`** - Runtime configuration
   - Used for context

4. **`source.credentials`** - Auth status
   - Used for API calls

### **Variable Library (Ready):**
- ✅ `TEST_PROJECT_ID` = 45 (SpectraTestProject)
- ✅ `API_TOKEN` - Auth token
- ✅ `BASE_URL` - API base URL
- ✅ `BASE_PATH` - API base path

---

## 📚 Key References for Prepare Stage

### **Design Documents:**
- `docs/prepare/PREPARE-STAGE-SCHEMA-DESIGN.md` - Complete schema specification
- `docs/SPECTRA-GRADE-SAMPLE-EXTRACTION.md` - Sample extraction architecture
- `docs/prepare/PREPARE-STAGE-COMPLETE.md` - Previous completion status

### **SDK Documentation:**
- `spectraSDK.Notebook/notebook_content.py` - SDK source code
- `docs/REUSABLE-TEST-DATA-BUILDER-COMPLETE.md` - Comprehensive test data builder

### **Jira Pattern (Reference):**
- `Data/jira/2-prepare/prepareJiraConfig.Notebook/notebook_content.py`
- Compare patterns, avoid bad practices

---

## ✅ SPECTRA-Grade Checklist for Prepare Stage

### **SDK Helpers:**
- [ ] Create `PrepareStageHelpers` class in SDK
- [ ] Implement `extract_introspection_samples()`
- [ ] Implement `introspect_schema_from_samples()`
- [ ] Implement `create_prepare_schema_table()`
- [ ] Implement `create_prepare_endpoints_table()`
- [ ] Implement `create_prepare_status_map_table()`

### **Notebook:**
- [ ] Update `prepareZephyr.Notebook` with SDK helpers
- [ ] Follow SPECTRA 7-stage pattern
- [ ] Use `TEST_PROJECT_ID` from Variable Library
- [ ] Extract samples from SpectraTestProject
- [ ] Introspect schema from samples
- [ ] Create Prepare stage tables

### **Contracts:**
- [ ] Create `contracts/prepare.contract.yaml`
- [ ] Create `manifests/prepare.manifest.yaml`
- [ ] Define inputs/outputs clearly
- [ ] Document obligations

### **Validation:**
- [ ] Validate schema coherence
- [ ] Validate row counts
- [ ] Validate table registration
- [ ] Test in Fabric

---

## 🎯 Next Steps (For Prepare Stage Chat)

1. **Review this playbook** - Understand what's ready
2. **Create `PrepareStageHelpers`** - Add to SDK
3. **Update Prepare notebook** - Use SDK helpers
4. **Create contracts** - Define Prepare stage contract
5. **Test in Fabric** - Validate complete workflow

---

**Version:** 1.0.0  
**Date:** 2025-12-08  
**Status:** 🟢 **Ready for Prepare Stage Development**  
**Handoff:** ✅ Complete

