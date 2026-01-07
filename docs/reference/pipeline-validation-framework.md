# SPECTRA Pipeline Validation Framework
**Date:** 2025-12-02  
**Purpose:** End-to-end validation across all 7 stages  
**Scope:** SPECTRA methodology enhancement (applies to all pipelines)

---

## The Big Idea

### Problem Statement

**How do we know the pipeline works end-to-end?**

Each stage runs independently:
- Source validates API access ✅
- Prepare designs schemas ✅
- Extract loads data ✅
- ... but does data flow correctly through ALL stages?

**Questions we can't answer:**
- Does Project 44 make it from Source → Analyse?
- Do transformations corrupt data?
- Do foreign keys stay intact through all stages?
- Do expected values appear at each stage?
- Can we trace one execution through the entire pipeline?

---

## Solution: Pipeline Validation Mode

### Single Flag: `validate_pipeline`

**When set:**
```python
validate_pipeline = True
```

**What happens:**
1. **Source:** Extracts sample + marks trace record
2. **Prepare:** Validates source outputs + designs schemas
3. **Extract:** Loads data + validates row counts match source
4. **Clean:** Cleans data + validates trace record survives
5. **Transform:** Transforms + validates FK integrity
6. **Refine:** Refines + validates calculations
7. **Analyse:** Visualizes + validates trace record renders

**Result:** End-to-end lineage report showing trace record's journey through all 7 stages

---

## Stage-by-Stage Validation

### Source Stage (When validate_pipeline=True)

**Extra actions:**
```python
if validate_pipeline:
    # 1. Extract sample database (always)
    extract_sample = True
    
    # 2. Mark trace record
    trace_execution_id = 33023  # Or from parameter
    log.info(f"📍 TRACE: Marking execution {trace_execution_id}")
    
    # 3. Validate outputs
    assert sample_dimProject.count() == 37
    assert trace_execution in sample_factTestExecution
    
    # 4. Write validation contract
    write_to_delta("Tables/validation/source_outputs", {
        "stage": "source",
        "timestamp": now(),
        "tables": {
            "sample_dimProject": {
                "rows": 37,
                "trace_record": {"projectId": 44}
            },
            "sample_factTestExecution": {
                "rows": 100,
                "trace_record": {"executionId": 33023}
            }
        },
        "checkpoints_passed": ["row_counts", "fk_integrity", "trace_present"]
    })
```

---

### Prepare Stage (When validate_pipeline=True)

**Extra actions:**
```python
if validate_pipeline:
    # 1. Read Source validation contract
    source_contract = spark.read.format("delta").load("Tables/validation/source_outputs")
    
    # 2. Validate inputs match contract
    df_projects = spark.read.format("delta").load("Tables/source/sample_dimProject")
    assert df_projects.count() == source_contract["tables"]["sample_dimProject"]["rows"]
    
    # 3. Test transformations on sample
    # Apply status mapping: "1" → "Pass"
    df_transformed = df_executions.withColumn("statusName", 
        when(col("status") == "1", "Pass").otherwise("Unknown"))
    
    # Validate trace record transformed correctly
    trace_row = df_transformed.filter(col("executionId") == 33023).collect()[0]
    assert trace_row["statusName"] == "Pass"
    log.info(f"📍 TRACE: Execution 33023 transformed to statusName='Pass'")
    
    # 4. Write validation contract for next stage
    write_validation_contract("prepare", {
        "inputs_validated": true,
        "transformations_tested": ["status_mapping", "date_conversion"],
        "trace_record_transformed": true
    })
```

---

### Extract Stage (When validate_pipeline=True)

**Extra actions:**
```python
if validate_pipeline:
    # 1. Extract full dataset
    # 2. Validate row counts >= sample
    assert bronze_projects.count() >= 37  # At least sample size
    
    # 3. Validate trace record present
    trace_exec = bronze_executions.filter(col("executionId") == 33023)
    assert trace_exec.count() == 1
    log.info(f"📍 TRACE: Execution 33023 extracted to bronze")
    
    # 4. Validate FK values present
    # All cycleIds in factTestExecution should exist in dimCycle
    fk_check = bronze_executions.join(bronze_cycles, "cycleId", "left_anti")
    assert fk_check.count() == 0, "FK violation: orphan cycleIds"
```

---

### Clean → Transform → Refine → Analyse

**Similar validation at each stage:**
- Read previous stage's validation contract
- Validate inputs match expectations
- Apply stage transformations
- Validate trace record survives
- Validate data quality
- Write validation contract for next stage

---

## Validation Contract Schema

### Each Stage Publishes

```yaml
stage: "source"
timestamp: "2025-12-02T21:00:00Z"
status: "passed"

outputs:
  tables:
    - name: "sample_dimProject"
      path: "Tables/source/sample_dimProject"
      rows: 37
      columns: 7
      schema_hash: "abc123..."
      trace_records:
        - {projectId: 44, projectName: "1.BP2 Test Management"}
      
    - name: "sample_factTestExecution"
      path: "Tables/source/sample_factTestExecution"
      rows: 100
      columns: 11
      trace_records:
        - {executionId: 33023, cycleId: 164, testCaseId: 80360}
  
  foreign_keys:
    - source_table: "sample_dimRelease"
      source_column: "projectId"
      target_table: "sample_dimProject"
      target_column: "projectId"
      orphans: 0
      validated: true
  
  checkpoints:
    - name: "row_counts"
      status: "passed"
    - name: "fk_integrity"
      status: "passed"
    - name: "trace_present"
      status: "passed"
      trace_records: [33023]

next_stage: "prepare"
ready_for_next: true
```

---

## Runtime Flags Enhanced

### Complete SPECTRA-Grade Flag System

```python
# Core Execution Modes
init_mode = False               # Complete initialization
validate_only = False           # Validation without extraction
extract_sample = False          # Extract sample dimensional database
full_run = False                # Validate + extract

# Validation & Quality
validate_pipeline = False       # ✨ NEW: End-to-end pipeline validation
validate_outputs = False        # ✨ NEW: Validate outputs after extraction
test_all_endpoints = False      # Test 120 endpoints comprehensively

# Tracing & Debugging
trace_execution_id = None       # ✨ NEW: Trace specific execution through pipeline
debug_mode = False              # Enhanced diagnostics
dry_run = False                 # Preview without writes

# Control
force_refresh = False           # Ignore existing data
max_sample_rows = 100           # Sample size control
```

---

## Flag Relationships

### `validate_pipeline=True` Implies:

```python
if validate_pipeline:
    extract_sample = True        # Must have sample to validate
    validate_outputs = True      # Must validate what we extract
    test_all_endpoints = True    # Must test comprehensively
    trace_execution_id = 33023   # Use known trace record
```

**Duration:** ~5 minutes  
**Output:** Complete validation report + end-to-end lineage

---

### `init_mode=True` Implies:

```python
if init_mode:
    test_all_endpoints = True
    extract_sample = True
    force_refresh = True
    validate_outputs = True  # NEW
```

**Duration:** ~5 minutes  
**Output:** Complete initialization + validation

---

## Validation Report Structure

### Pipeline Validation Report

```yaml
validation_run_id: "val-20251202-210000"
pipeline: "zephyr"
mode: "validate_pipeline"
started: "2025-12-02T21:00:00Z"
completed: "2025-12-02T21:05:00Z"
duration_seconds: 300

trace_record:
  execution_id: 33023
  project: "1.BP2 Test Management"
  release: "BUAT"
  cycle: "BUAT - Cycle 1"
  tester: "Preethi Samuel"

stages:
  - stage: "source"
    status: "passed"
    duration: 90
    validations:
      - check: "sample_extracted"
        status: "passed"
        rows: 265
      - check: "fk_integrity"
        status: "passed"
        orphans: 0
      - check: "trace_present"
        status: "passed"
        found: true
    trace_record_status: "present_in_sample_factTestExecution"
    
  - stage: "prepare"
    status: "passed"
    duration: 30
    validations:
      - check: "inputs_valid"
        status: "passed"
      - check: "transformations_tested"
        status: "passed"
        transforms: ["status_mapping", "date_conversion"]
    trace_record_status: "transformation_rules_defined"
    
  - stage: "extract"
    status: "passed"
    duration: 60
    validations:
      - check: "full_extraction"
        status: "passed"
        rows: 50000
      - check: "trace_in_bronze"
        status: "passed"
    trace_record_status: "extracted_to_bronze"

  # ... remaining stages

overall:
  status: "passed"
  stages_passed: 7
  stages_failed: 0
  trace_record_preserved: true
  data_lineage_validated: true
```

---

## Recommendation

### Implement in Phases

**Phase 1: Source Stage (Now - 30 min)**

Add 3 new flags:
- `validate_outputs` - Validate sample data after extraction
- `trace_execution_id` - Mark specific execution to trace
- Rename `test_endpoints` → `test_all_endpoints` for clarity

**Phase 2: Validation Contract (Next - 1 hour)**

Create `source.validation.yaml`:
- Document expected outputs
- Include trace records
- Define checkpoints

**Phase 3: Prepare Stage Integration (Later - 2 hours)**

Prepare reads Source validation contract:
- Validates inputs match
- Tests transformations
- Publishes own validation contract

**Phase 4: Full Pipeline (Future - 4-8 hours)**

Complete end-to-end validation:
- All 7 stages participate
- Trace record flows through
- Lineage report generated

---

**Should I start with Phase 1 (add validation flags to Source notebook now)?**

---

*Design: 2025-12-02 21:50 GMT*  
*Pipeline validation framework - methodology enhancement for all SPECTRA pipelines*

