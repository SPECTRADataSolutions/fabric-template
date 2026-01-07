# Local Fabric Runtime

**Purpose:** Local testing environment for Fabric notebooks to catch errors before deployment  
**Type:** Tool/Infrastructure Service  
**Priority:** Critical (blocks fast iteration)  
**Target Maturity:** MVP (Level 1)  
**Built Using:** Core Innovation Engine methodology  
**Date:** 2025-12-04

---

## Phase 1: Discover 🔍

**Goal:** Define the problem, scope, and success criteria

### Existing Solutions Analysis

**Microsoft Tools (Not Applicable):**

- **Fabric CLI (`fab`)**: CLI for exploring Fabric environment (not notebook testing)
- **Fabric Extensibility Toolkit**: For building custom Fabric workloads/extensions (not notebook testing)
- **Workload Development Kit**: For building new Fabric features (not notebook testing)
- **Azurite Emulator**: For OneLake API testing (not notebook execution)

**Verdict**: Microsoft tools focus on **building Fabric extensions**, not **testing notebooks**.

**Generic Tools:**

- **pytest**: General Python testing framework ✅ (can be adapted)
- **delta-spark**: Delta Lake for local PySpark ✅ (exactly what we need)
- **unittest.mock**: Python mocking library ✅ (for Fabric APIs)
- **Databricks patterns**: Community has similar needs but no standard framework

**Gap Identified**: **NO existing tool for local Fabric notebook testing**. We must build it.

**Competitive Advantage**: First-mover. This could be open-sourced and become THE standard for Fabric notebook testing.

### Problem Statement

- Current workflow: write → commit → push → Fabric sync → test → fail → repeat
- 5-10 minute cycle time per iteration
- Errors only caught in Fabric runtime
- No way to validate locally before deployment

### Success Criteria (MVP)

- ✅ Run Zephyr Source notebook locally in Cursor terminal
- ✅ Validate syntax, imports, and basic logic
- ✅ Mock Fabric-specific APIs (mssparkutils, notebookutils)
- ✅ Simulate Delta Lake writes to local filesystem
- ✅ Catch 80%+ of deployment errors locally
- ✅ < 30 seconds test execution time

### Out of Scope (MVP)

- ❌ Full Spark cluster simulation
- ❌ Exact Fabric catalog behavior replication
- ❌ Performance testing at scale
- ❌ Multi-notebook orchestration
- ❌ Fabric UI preview

### Key Questions

1. Which Fabric APIs are most critical to mock?
2. Can we use pytest for notebook testing?
3. How do we handle notebook cell structure in tests?
4. Should we test the `.py` export or parse `.ipynb`?

### Dependencies

- PySpark (already installed)
- Delta Lake Python package
- pytest
- Mock/unittest.mock

---

## Phase 2: Design 🎨

**Goal:** Architecture, patterns, and technical approach

### Architecture: Hybrid Approach

```text
┌─────────────────────────────────────────────────┐
│  Cursor IDE (Development)                       │
│  ┌───────────────────────────────────────────┐  │
│  │  Fabric Notebook (.py export)             │  │
│  │  - sourceZephyr.Notebook/notebook-content │  │
│  └───────────────────────────────────────────┘  │
│                    ↓                             │
│  ┌───────────────────────────────────────────┐  │
│  │  Local Test Runner                        │  │
│  │  - tests/test_source_notebook.py          │  │
│  │  - Mocks Fabric APIs                      │  │
│  │  - Real PySpark + Delta                   │  │
│  └───────────────────────────────────────────┘  │
│                    ↓                             │
│  ┌───────────────────────────────────────────┐  │
│  │  Local Lakehouse                          │  │
│  │  - tests/.lakehouse/Files/                │  │
│  │  - tests/.lakehouse/Tables/               │  │
│  │  - tests/.lakehouse/metastore/            │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  Fabric (Deployment)                            │
│  - Real runtime, real catalog                   │
│  - Confident deployment after local validation  │
└─────────────────────────────────────────────────┘
```

### Component Design

#### 1. Mock Fabric APIs (`tests/fabric_mocks.py`)

```python
class MockMSSparkUtils:
    class fs:
        @staticmethod
        def ls(path): ...
        @staticmethod
        def mkdirs(path): ...

    class notebook:
        @staticmethod
        def exit(value): ...

class MockNotebookUtils:
    @staticmethod
    def get(param, default): ...
```

#### 2. Local SparkSession Factory (`tests/spark_factory.py`)

```python
def create_local_spark():
    """Create SparkSession with Delta Lake support."""
    return SparkSession.builder \
        .appName("FabricLocalTest") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.sql.warehouse.dir", "tests/.lakehouse/warehouse") \
        .master("local[*]") \
        .getOrCreate()
```

#### 3. Notebook Test Harness (`tests/test_source_notebook.py`)

```python
def test_bootstrap_mode():
    """Test notebook with bootstrap=True."""
    # Setup
    spark = create_local_spark()
    inject_mocks(globals())
    set_parameters(bootstrap=True, preview=True, debug=True)

    # Execute notebook
    exec(open("sourceZephyr.Notebook/notebook_content.py").read())

    # Assert
    assert spark.catalog.tableExists("source.endpoints")
    df = spark.read.table("source.endpoints")
    assert df.count() == 228
```

#### 4. Parameter Injection (`tests/param_injector.py`)

```python
def set_parameters(**params):
    """Inject notebook parameters into globals."""
    for key, value in params.items():
        globals()[key] = value
```

### Design Patterns

1. **Test Isolation:** Each test gets fresh SparkSession + clean lakehouse
2. **Mock Injection:** Replace Fabric APIs before notebook execution
3. **Assertion Layer:** Validate Delta tables, counts, schemas
4. **Fast Feedback:** Run in < 30 seconds, fail fast

### File Structure

```text
Data/zephyr/
├── sourceZephyr.Notebook/
│   └── notebook_content.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures
│   ├── fabric_mocks.py          # Mock Fabric APIs
│   ├── spark_factory.py         # Local Spark setup
│   ├── test_source_notebook.py  # Main tests
│   └── .lakehouse/              # Local data (gitignored)
│       ├── Files/
│       ├── Tables/
│       └── warehouse/
├── pytest.ini                   # pytest config
└── requirements-test.txt        # Test dependencies
```

---

## Phase 3: Build 🔨

**Goal:** Implement MVP components

### Build Order (TDD Approach)

1. **Day 1: Foundation**

   - Create test structure
   - Install dependencies (delta-spark, pytest)
   - Build `spark_factory.py`
   - Build `fabric_mocks.py`

2. **Day 2: Test Harness**

   - Build `conftest.py` (fixtures)
   - Build `test_source_notebook.py` skeleton
   - Test mock injection works

3. **Day 3: First Test**

   - Test: bootstrap mode loads 228 endpoints
   - Fix any import/execution issues
   - Validate Delta write locally

4. **Day 4: Full Coverage**

   - Test: preview mode (sample tables)
   - Test: backfill mode
   - Test: parameter validation

5. **Day 5: CI/CD**
   - Add GitHub Actions workflow
   - Test on push to main
   - Document usage in README

### Key Implementation Details

#### Mock Strategy

```python
# Before notebook execution:
sys.modules['notebookutils'] = MockNotebookUtils()
mssparkutils = MockMSSparkUtils()

# Notebook sees mocked versions
from notebookutils import mssparkutils  # → MockMSSparkUtils
```

#### Delta Local Pattern

```python
# Real Delta Lake, just local filesystem
df.write.format("delta").save("tests/.lakehouse/Tables/source/endpoints")
```

#### Catalog Handling

```python
# Mock catalog with local Hive metastore
spark.sql("CREATE DATABASE IF NOT EXISTS source")
```

---

## Phase 4: Test 🧪

**Goal:** Validate the test framework itself

### Test the Tests

1. **Smoke Test:** Can we create SparkSession locally?
2. **Mock Test:** Do mocks get injected correctly?
3. **Execution Test:** Can notebook execute without errors?
4. **Assertion Test:** Can we validate Delta tables?
5. **Isolation Test:** Do tests not interfere with each other?

### Validation Scenarios

- ✅ Fresh project (no lakehouse exists)
- ✅ Existing lakehouse (tables already exist)
- ✅ Invalid parameters (should fail gracefully)
- ✅ Missing credentials (should fail with clear error)
- ✅ Network unavailable (if bootstrap uses API)

### Success Metrics

- All tests pass locally in < 30 seconds
- Catches same errors as Fabric would
- Zero false positives (passes locally = passes in Fabric)
- Clear error messages when tests fail

---

## Phase 5: Deploy 🚀

**Goal:** Make available for use

### Deployment Steps

1. **Documentation**

   - `tests/README.md` - How to run tests
   - Update main `README.md` with test instructions
   - Add to Zephyr development workflow

2. **Developer Setup**

   ```bash
   # Install test dependencies
   pip install -r requirements-test.txt

   # Run tests
   pytest tests/ -v

   # Run specific test
   pytest tests/test_source_notebook.py::test_bootstrap_mode -v
   ```

3. **CI/CD Integration**

   ```yaml
   # .github/workflows/test.yml
   name: Test Notebooks
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
         - run: pip install -r requirements-test.txt
         - run: pytest tests/ -v
   ```

4. **IDE Integration**
   - Add VS Code test discovery
   - Add pytest markers for quick smoke tests
   - Add pre-commit hook (optional)

### Rollout Strategy

1. **Phase 1:** Developer only (you test it first)
2. **Phase 2:** Add to Zephyr development workflow
3. **Phase 3:** Template for other Fabric projects (Jira, Xero, etc.)
4. **Phase 4:** Promote to `spectra-fabric-sdk` as reusable framework

---

## Phase 6: Optimise ⚡

**Goal:** Improve speed, coverage, and developer experience

### Optimization Targets

#### Speed (Current: ~30s, Target: <10s)

- Cache SparkSession between tests
- Parallelize test execution
- Use in-memory Delta Lake for faster writes
- Skip expensive operations in test mode

#### Coverage (Current: ~80%, Target: 95%+)

- Add integration tests (multi-notebook workflows)
- Test error handling paths
- Test edge cases (empty data, schema changes)
- Add performance regression tests

#### Developer Experience

- Add `make test` shortcut
- Add VS Code launch config for debugging
- Add test report dashboard
- Add auto-fix for common failures

### Metrics to Track

- Test execution time (per test, total suite)
- Test coverage percentage
- False positive rate (passes locally, fails in Fabric)
- False negative rate (fails locally, passes in Fabric)
- Developer adoption rate

### Future Enhancements

1. **Visual Test Reports**

   ```bash
   pytest tests/ --html=report.html
   # Opens in browser with results
   ```

2. **Data Diff Tool**

   ```python
   # Compare local vs Fabric results
   compare_delta_tables(local_path, fabric_path)
   ```

3. **Mock Replay**

   ```python
   # Record Fabric API calls, replay locally
   with fabric_recorder():
       # Runs in Fabric, records all API calls

   # Later, in local test:
   with fabric_replay("recording.json"):
       # Uses recorded responses
   ```

---

## Phase 7: Commit 🎯

**Goal:** SPECTRAfy the solution - make it SPECTRA-grade and universally reusable

### What Does "SPECTRAfy" Mean?

**SPECTRAfy** (verb) = To transform a working solution into a SPECTRA-grade component by:

- Extracting to reusable packages
- Integrating with SPECTRA infrastructure
- Adding to Universal Tool Registry
- Documenting patterns in doctrine
- Making it autonomous and composable

This phase elevates the MVP from "works for Zephyr" to "works for all Fabric workspaces across SPECTRA."

### Documentation Updates

1. **Add to Source Phase Patterns**

   - `Data/framework/docs/standards/SOURCE-PHASE-PATTERNS.md`
   - Section: "Local Testing Pattern for Fabric Notebooks"

2. **Add to Testing Standards**

   - `Data/framework/docs/standards/TESTING-STANDARDS.md`
   - Section: "Fabric Notebook Testing"

3. **Update Labs Queue**
   - Mark idea as "completed"
   - Document lessons learned
   - Add to reusable patterns catalog

### Promotion Path (SPECTRAfy Process)

1. **Extract to SDK**

   ```python
   # Move from tests/ to spectra-fabric-sdk
   from spectra_fabric_sdk.testing import (
       create_local_spark,
       MockMSSparkUtils,
       run_notebook_test
   )
   ```

2. **Register in Universal Tool Registry**

   ```yaml
   tool_id: fabric_notebook_tester
   category: technical_intelligence
   provides: [notebook_validation, local_spark_execution, fabric_api_mocking]
   used_by: [data_ingestion_engine]
   maturity: mvp
   ```

3. **Integrate with Test Harness Service**

   - Local fallback pattern (works offline)
   - Can optionally call test-harness API
   - Reports results to central test intelligence

4. **Template Repository**

   - Create `fabric-notebook-template` with testing pre-configured
   - New projects start with tests built-in

5. **Framework Distribution**
   - Publish as separate package: `spectra-fabric-test-kit`
   - Used across all Fabric projects (Jira, Xero, UniFi, Graph)

### Success Criteria (Long-term)

- ✅ 100% of new Fabric notebooks have local tests
- ✅ CI/CD blocks deployment if tests fail
- ✅ Average iteration cycle < 2 minutes (was 10 minutes)
- ✅ 95%+ test accuracy (local pass = Fabric pass)
- ✅ Pattern adopted across SPECTRA Fabric workspaces

### Maturity Progression Path

**Current Target:** Level 1 (MVP)

- Works for Zephyr
- Catches 80%+ errors locally
- < 30 second tests

**Future Levels:**

- **Level 2 (Alpha):** Used by 2+ Fabric workspaces, basic CI/CD integration
- **Level 3 (Beta):** Published to PyPI, comprehensive test coverage, documented
- **Level 4 (Live):** Standard tool for all Fabric development, part of onboarding
- **Level 5-7:** Autonomous test generation, predictive failure detection, self-optimizing

### Lessons Captured

1. **Technical Lesson:** Mock Fabric APIs for local development
2. **Process Lesson:** Test notebooks before deployment
3. **Architecture Lesson:** Hybrid mock strategy (real Spark, mock Fabric)
4. **Platform Lesson:** Local testing unblocks fast iteration

---

## Summary: MVP → SPECTRA-Grade Journey

| Phase       | Duration | Deliverable                   | Success Metric                | Maturity Level  |
| ----------- | -------- | ----------------------------- | ----------------------------- | --------------- |
| 1. Discover | 2 hours  | Problem definition + scope    | Clear success criteria        | -               |
| 2. Design   | 4 hours  | Architecture + file structure | Reviewable design doc         | -               |
| 3. Build    | 3 days   | Working test framework        | First test passes             | MVP (Level 1)   |
| 4. Test     | 1 day    | Validated framework           | All validation scenarios pass | MVP (Level 1)   |
| 5. Deploy   | 1 day    | Documentation + CI/CD         | Other devs can use it         | MVP (Level 1)   |
| 6. Optimise | 1 week   | Fast, comprehensive tests     | <10s execution, 95%+ coverage | Alpha (Level 2) |
| 7. Commit   | 1 day    | SPECTRA-grade (SPECTRAfy'd)   | Reusable across projects      | Beta (Level 3)  |

**Total MVP Time:** ~1 week  
**Total SPECTRA-Grade:** ~2 weeks  
**ROI:** Infinite (unblocks autonomous development)

---

## Next Steps

**Status:** ✅ Phase 1 Complete | ✅ Phase 2 Complete | 🔨 Phase 3 Ready

**This Week:**

- Build MVP test framework (5 days)
- Test with Zephyr Source notebook
- Document usage

**Next Week:**

- Optimize for speed and coverage
- Extract to SDK (SPECTRAfy)
- Apply to other Fabric projects

---

**Decision Point:** Should we proceed with Phase 3 (Build)?  
**Estimated MVP:** 5 days to working local test framework  
**Benefit:** Fast iteration, catch errors locally, full Fabric autonomy
