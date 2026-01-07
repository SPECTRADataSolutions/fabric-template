# Pipeline Validation Mode - End-to-End Testing
**Date:** 2025-12-02  
**Purpose:** Validate entire 7-stage pipeline with sample data

---

## Concept: Pipeline Validation Run

### The Problem

Each stage runs independently:
- Source extracts data
- Prepare transforms it
- Extract loads it
- Clean validates it
- Transform enriches it
- Refine models it
- Analyse visualizes it

**But how do we know:**
- Data flows correctly through all stages?
- Transformations don't corrupt data?
- Foreign keys stay intact?
- Expected values appear at each stage?
- Quality gates pass throughout?

**Answer:** **Pipeline Validation Mode** ✅

---

## Pipeline Validation Mode

### Concept

**A special run mode that:**
1. Starts with known sample data (e.g., Project 44, Release 106, Cycle 164)
2. Traces it through ALL 7 stages
3. Validates expected values at each stage
4. Checks data integrity at stage boundaries
5. Generates end-to-end validation report

**Flag:** `validate_pipeline=True`

---

## How It Works

### Stage-by-Stage Validation

```
Source Stage:
  Input: Project 44
  Expected Output: 
    - dimProject: 1 row (projectId=44)
    - dimRelease: 2 rows (releaseId=106, 112)
    - dimCycle: 13 rows
    - factTestExecution: 100+ rows
  Validation: ✅ All expected records present

Prepare Stage:
  Input: Tables/source/sample_*
  Expected Output:
    - Schema definitions for gold tables
    - Transformation rules documented
    - Data quality rules defined
  Validation: ✅ All schemas match source structure

Extract Stage:
  Input: Zephyr API + Prepare schemas
  Expected Output:
    - Tables/bronze/raw_projects (37 rows)
    - Tables/bronze/raw_releases (77 rows)
    - All raw data extracted
  Validation: ✅ Row counts match source
              ✅ No data loss

Clean Stage:
  Input: Tables/bronze/*
  Expected Output:
    - Tables/silver/clean_projects (37 rows, quality checked)
    - Tables/silver/clean_releases (77 rows, validated)
    - Data quality report
  Validation: ✅ All dirty data flagged
              ✅ Quality rules applied
              ✅ Row counts preserved

Transform Stage:
  Input: Tables/silver/*
  Expected Output:
    - Tables/gold/dimProject (37 rows with surrogate keys)
    - Tables/gold/dimRelease (77 rows with FK to dimProject)
    - Transformed dimensions
  Validation: ✅ Surrogate keys generated
              ✅ Foreign keys resolve
              ✅ SCD Type 2 working

Refine Stage:
  Input: Tables/gold/dim* + fact*
  Expected Output:
    - Calculated columns added
    - Business rules applied
    - Aggregations computed
  Validation: ✅ Calculations correct
              ✅ Business rules applied

Analyse Stage:
  Input: Tables/gold/* (refined)
  Expected Output:
    - Power BI model loaded
    - Relationships working
    - Measures calculating correctly
  Validation: ✅ Dashboards render
              ✅ Metrics accurate
```

---

## Validation Checkpoints

### At Each Stage Boundary

**Checkpoint 1: Source → Prepare**
```python
validate_checkpoint("source_to_prepare"):
  - Check: sample_dimProject exists
  - Check: 37 rows present
  - Check: projectId=44 in dataset
  - Check: All 5 tables present
  - Check: Foreign keys resolve
```

**Checkpoint 2: Prepare → Extract**
```python
validate_checkpoint("prepare_to_extract"):
  - Check: Schema DDL generated
  - Check: Transformation rules defined
  - Check: Source tables readable
```

**Checkpoint 3: Extract → Clean**
```python
validate_checkpoint("extract_to_clean"):
  - Check: Row count matches source (37 projects)
  - Check: No duplicate keys
  - Check: All foreign key values present
```

**Checkpoint 4: Clean → Transform**
```python
validate_checkpoint("clean_to_transform"):
  - Check: Quality flags applied
  - Check: Invalid rows flagged
  - Check: Data types correct
```

**Checkpoint 5: Transform → Refine**
```python
validate_checkpoint("transform_to_refine"):
  - Check: Surrogate keys generated
  - Check: Lookups applied
  - Check: Date dimensions joined
  - Check: SCD Type 2 working
```

**Checkpoint 6: Refine → Analyse**
```python
validate_checkpoint("refine_to_analyse"):
  - Check: Business rules applied
  - Check: Calculated columns present
  - Check: Aggregations correct
```

**Checkpoint 7: Analyse (Final)**
```python
validate_checkpoint("analyse_final"):
  - Check: Power BI can read tables
  - Check: Dashboards render
  - Check: Metrics calculate
  - Check: Filters work
```

---

## Trace Sample Data

### Trace a Specific Execution Through Pipeline

**Known sample:**
- Project: 44 (1.BP2 Test Management)
- Release: 106 (BUAT)
- Cycle: 164 (BUAT - Cycle 1)
- Execution: 33023
- Test Case: 80360
- Tester: Preethi Samuel (testerId=38)

**Expected at each stage:**

**Source:**
```
sample_factTestExecution:
  executionId: 33023
  cycleId: 164
  testCaseId: 80360
  testerId: 38
  testerName: "Preethi Samuel"
  status: "1"
```

**Extract:**
```
bronze/raw_executions:
  executionId: 33023
  cycleId: 164
  testCaseId: 80360
  [same as source, just in bronze zone]
```

**Clean:**
```
silver/clean_executions:
  executionId: 33023
  cycleId: 164
  testCaseId: 80360
  status: "1"
  quality_flags: []  # No issues
  is_valid: true
```

**Transform:**
```
gold/factTestExecution:
  executionKey: 1001 (surrogate)
  executionId: 33023 (business key)
  cycleKey: FK to dimCycle
  testCaseKey: FK to dimTestCase
  testerKey: FK to dimUser
  statusKey: FK to dimExecutionStatus
  status_name: "Pass" (mapped from "1")
  actualTimeMinutes: 0
  estimatedTimeMinutes: 0
```

**Refine:**
```
gold/factTestExecution (enriched):
  [all Transform columns]
  timeVarianceMinutes: 0 (calculated)
  isOnTime: true (business rule)
  executionMonth: "2024-12"
```

**Analyse:**
```
Power BI:
  Execution visible in dashboard ✅
  Tester "Preethi Samuel" shown ✅
  Status "Pass" displayed ✅
  Project "1.BP2 Test Management" linked ✅
```

---

## Implementation: Pipeline-Level Flag

### Option 1: Pipeline Orchestration Flag

**In pipeline parameters:**
```yaml
# zephyrPipeline.DataPipeline parameters
validate_pipeline: false

stages:
  - source:
      validate_pipeline: ${validate_pipeline}
  - prepare:
      validate_pipeline: ${validate_pipeline}
  - extract:
      validate_pipeline: ${validate_pipeline}
  # ... etc
```

**When `validate_pipeline=True`:**
- Each stage validates its inputs/outputs
- Each stage writes validation results
- Pipeline collects all validations
- Final report shows end-to-end lineage

---

### Option 2: Stage-Specific Validation Flags

**Each stage has:**
```python
# Source stage
validate_source = True  # Validate source outputs
trace_sample = True     # Include trace markers

# Prepare stage
validate_prepare = True  # Validate transformations
trace_sample = True      # Continue tracing

# And so on...
```

---

### Option 3: Validation Contract per Stage

**Each stage publishes a validation contract:**

```yaml
# source.validation.yaml
stage: "source"
outputs:
  - table: "sample_dimProject"
    expected_rows: 37
    expected_columns: 7
    trace_record:
      projectId: 44
      projectName: "1.BP2 Test Management"
      
# prepare.validation.yaml
inputs:
  - table: "sample_dimProject"
    validate_from: "source.validation.yaml"
outputs:
  - schema: "gold_dimProject.ddl"
    trace_record_preserved: true
```

---

## Recommended Approach

### Phase 1: Source Stage Validation (Now)

**Add to Source notebook:**

```python
# New flag
validate_outputs = False  # Validate sample data integrity

if validate_outputs and extract_sample:
    log.info("=" * 60)
    log.info("Validating Sample Data Integrity")
    log.info("=" * 60)
    
    # Read back what we just wrote
    df_projects = spark.read.format("delta").load("Tables/source/sample_dimProject")
    df_releases = spark.read.format("delta").load("Tables/source/sample_dimRelease")
    df_cycles = spark.read.format("delta").load("Tables/source/sample_dimCycle")
    df_executions = spark.read.format("delta").load("Tables/source/sample_factTestExecution")
    
    # Validate row counts
    assert df_projects.count() == 37, "dimProject should have 37 rows"
    assert df_releases.count() >= 40, "dimRelease should have 40+ rows"
    
    # Validate foreign keys
    # All releaseIds in dimRelease should exist in dimProject.projectId
    fk_check = df_releases.join(df_projects, "projectId", "left_anti")
    orphans = fk_check.count()
    assert orphans == 0, f"Found {orphans} orphan releases (FK violation)"
    
    # Validate trace record exists
    trace_execution = df_executions.filter(col("executionId") == 33023)
    assert trace_execution.count() == 1, "Trace execution 33023 should exist"
    
    log.info("✅ All validation checks passed")
    log.info("   - Row counts correct")
    log.info("   - Foreign keys resolve")
    log.info("   - Trace record present")
```

---

### Phase 2: Prepare Stage Validation

**Prepare reads Source outputs and validates:**
```python
# Prepare notebook
if validate_pipeline:
    # Read Source outputs
    df_source_projects = spark.read.format("delta").load("Tables/source/sample_dimProject")
    
    # Validate schema matches expectations
    assert "projectId" in df_source_projects.columns
    assert "projectName" in df_source_projects.columns
    
    # Design transformations
    # Test transformations on sample
    # Validate results
```

---

### Phase 3: End-to-End Validation

**Pipeline orchestration:**
```python
# Run entire pipeline in validation mode
# Collect checkpoints from each stage
# Generate lineage report
# Show trace record path: Source → Prepare → ... → Analyse
```

---

## What Should We Implement Now?

### Immediate (Source Stage Only)

Add to Source notebook:
1. ✅ `test_all_endpoints` (already added)
2. ✅ `extract_sample` (already added)
3. ✨ `validate_outputs` - NEW: Validate sample data integrity after extraction
4. ✨ `trace_record` - NEW: Mark specific record to trace (e.g., executionId=33023)

**Duration:** 30 minutes

---

### Short-term (Contract Enhancement)

Define validation contract:
```yaml
# source.validation.yaml
outputs:
  sample_dimProject:
    expected_rows: 37
    expected_columns: [projectId, projectName, ...]
    foreign_keys: []
    trace_record: {projectId: 44}
    
  sample_factTestExecution:
    expected_rows: 100
    foreign_keys:
      - {column: cycleId, references: sample_dimCycle}
      - {column: testCaseId, references: sample_dimTestCase}
    trace_record: {executionId: 33023}
```

**Duration:** 1 hour

---

### Long-term (Pipeline Orchestration)

Build pipeline validation framework:
- Each stage reads previous stage's validation contract
- Each stage validates inputs match contract
- Each stage validates outputs against own contract
- Pipeline collects all checkpoints
- Generates end-to-end lineage report

**Duration:** 4-8 hours (separate project)

---

## Immediate Recommendation

### Add 2 New Flags to Source Notebook Now

**1. `validate_outputs` (Default: False)**
```python
validate_outputs = get_bool_param("validate_outputs", "DXC_ZEPHYR_VALIDATE_OUTPUTS", False)

# After extract_sample completes:
if validate_outputs and extract_sample:
    # Read back sample tables
    # Validate row counts
    # Validate foreign keys
    # Validate trace record present
    # Assert all checks pass
```

**2. `trace_execution_id` (Default: None)**
```python
trace_execution_id = globals().get("trace_execution_id") or os.environ.get("DXC_ZEPHYR_TRACE_EXECUTION_ID")

# During extraction:
if trace_execution_id:
    # Mark trace record
    # Log when trace record is extracted
    # Prepare stage can continue tracing
```

---

**This is a great idea! Should I:**
1. Add `validate_outputs` and `trace_execution_id` flags to Source notebook now?
2. Design the complete pipeline validation contract system?
3. Both?

This would give us **end-to-end data lineage validation** through the entire pipeline!

---

*Concept: 2025-12-02 21:45 GMT*  
*Pipeline validation mode - trace sample data through all 7 stages*

