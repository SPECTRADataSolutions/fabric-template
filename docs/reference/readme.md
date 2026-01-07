# SPECTRA Zephyr Source Stage Test Suite

Comprehensive test suite for the Zephyr source stage notebook and SDK helpers.

## 📋 Test Structure

```
tests/
├── conftest.py                    # pytest fixtures and test configuration
├── test_source_stage_helpers.py   # Unit tests for SourceStageHelpers
├── test_validation.py             # Validation logic tests
├── test_error_handling.py         # Error handling and retry tests
├── test_integration.py            # End-to-end integration tests
├── coverage/                      # HTML coverage reports
├── coverage.json                  # JSON coverage data
├── coverage.xml                   # XML coverage data (for CI/CD)
└── pytest.ini                     # pytest configuration
```

## 🎯 Coverage Targets

| Component               | Target  | Current |
| ----------------------- | ------- | ------- |
| SDK Helpers             | >80%    | TBD     |
| Validation Functions    | >90%    | TBD     |
| Error Handling          | >80%    | TBD     |
| Notebook Logic          | >60%    | TBD     |
| **Overall**             | **75%** | **TBD** |

## 🚀 Running Tests

### Run all tests

```bash
cd Data/zephyr
pytest
```

### Run specific test file

```bash
pytest tests/test_source_stage_helpers.py -v
```

### Run tests with coverage

```bash
pytest --cov=spectraSDK.Notebook \
       --cov=sourceZephyr.Notebook \
       --cov-report=term-missing \
       --cov-report=html:tests/coverage
```

### Run tests by marker

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# API tests only
pytest -m api

# Validation tests only
pytest -m validation
```

### Generate coverage report

```bash
pytest --cov --cov-report=html
# Open tests/coverage/index.html in browser
```

## 📊 Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Unit tests for individual functions
- `@pytest.mark.integration` - Integration tests with mocked APIs
- `@pytest.mark.slow` - Tests that take >1 second
- `@pytest.mark.api` - Tests that mock API calls
- `@pytest.mark.validation` - Data validation tests
- `@pytest.mark.error_handling` - Error handling and retry tests

## 🔧 Test Configuration

Configuration is managed via `pytest.ini`:

- **Coverage threshold**: 75% minimum
- **Test timeout**: 30 seconds per test
- **Coverage reports**: Terminal, HTML, JSON, XML
- **Test discovery**: `test_*.py` files, `Test*` classes, `test_*` functions

## 🧪 Writing Tests

### Example: Unit Test

```python
@pytest.mark.unit
def test_create_portfolio_table(spark, mock_delta_table, mock_logger):
    """Test portfolio table creation."""
    from spectraSDK import SourceStageHelpers
    
    SourceStageHelpers.create_source_portfolio_table(
        spark=spark,
        delta=mock_delta_table,
        logger=mock_logger,
        session=mock_notebook_session,
        contract_version="1.0.0",
    )
    
    mock_delta_table.write.assert_called_once()
    mock_logger.info.assert_called()
```

### Example: Validation Test

```python
@pytest.mark.validation
def test_validates_required_fields():
    """Test validation of required fields in API response."""
    data = {"id": 1, "name": "Test"}
    required_fields = ["id", "name"]
    
    for field in required_fields:
        assert field in data
```

### Example: Error Handling Test

```python
@pytest.mark.error_handling
def test_retry_on_failure(mock_requests_get):
    """Test retry mechanism on API failure."""
    mock_requests_get.side_effect = [
        requests.exceptions.RequestException("Fail"),
        "Success"
    ]
    
    @simple_retry(attempts=2)
    def api_call():
        return mock_requests_get()
    
    result = api_call()
    assert result == "Success"
    assert mock_requests_get.call_count == 2
```

## 🔨 Fixtures

Key fixtures available in `conftest.py`:

### Spark Session

- `spark` - Mock Spark session
- `mock_delta_table` - Mock DeltaTable class
- `mock_logger` - Mock SPECTRALogger
- `mock_notebook_session` - Mock NotebookSession

### Sample Data

- `sample_endpoint_catalog` - Sample Zephyr endpoint catalog
- `sample_projects_response` - Sample API projects response
- `sample_releases_response` - Sample API releases response

### Mocks

- `mock_requests_get` - Mock requests.get for API calls
- `MockDataFrame` - Simple mock for Spark DataFrame
- `MockDataFrameWriter` - Simple mock for Spark DataFrameWriter

## 📈 Coverage Reports

### Terminal Output

```bash
pytest --cov --cov-report=term-missing
```

Shows coverage with line numbers for missing coverage.

### HTML Report

```bash
pytest --cov --cov-report=html
open tests/coverage/index.html
```

Interactive HTML report with line-by-line coverage highlighting.

### JSON Report

```bash
pytest --cov --cov-report=json:tests/coverage.json
```

Machine-readable coverage data for CI/CD pipelines.

### XML Report (Codecov)

```bash
pytest --cov --cov-report=xml:tests/coverage.xml
```

Coverage data in Cobertura format for Codecov integration.

## 🤖 CI/CD Integration

Tests run automatically on:

- ✅ Push to `main`, `master`, or `develop` branches
- ✅ Pull requests to `main`, `master`, or `develop` branches
- ✅ Manual workflow dispatch

### GitHub Actions Workflow

See `.github/workflows/test.yml` for full CI/CD pipeline:

1. **Test Job**: Runs tests with coverage on Python 3.10 and 3.11
2. **Lint Job**: Runs Black, isort, Flake8, and Pylint (non-blocking)
3. **Notify Job**: Reports success/failure status

### Coverage Threshold

- **Minimum**: 75% overall coverage
- **Target**: 80%+ for critical components
- **CI/CD**: Fails if below 75%

### Artifacts

CI/CD uploads coverage reports as artifacts:

- `tests/coverage/` - HTML coverage report
- `tests/coverage.json` - JSON coverage data
- `tests/coverage.xml` - XML coverage data (Codecov)
- `tests/junit.xml` - JUnit test results

## 🐛 Troubleshooting

### Tests Failing Locally

1. **Check Python version**: Requires Python 3.10+
2. **Install dependencies**: `pip install -r requirements-dev.txt`
3. **Check Spark**: Ensure PySpark is installed correctly
4. **Check fixtures**: Review `conftest.py` for fixture dependencies

### Coverage Not Updating

1. **Clear cache**: `pytest --cache-clear`
2. **Regenerate reports**: `rm -rf tests/coverage && pytest --cov`
3. **Check source paths**: Verify `--cov` paths match actual code structure

### Slow Tests

1. **Run with `-m "not slow"`**: Skip slow tests during development
2. **Use `-n auto`**: Parallel test execution (requires `pytest-xdist`)
3. **Increase timeout**: Modify `timeout = 30` in `pytest.ini`

## 📚 References

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Codecov documentation](https://docs.codecov.io/)
- [SPECTRA testing standards](../../Core/standards/TESTING-STANDARDS.md)

## 🏆 SPECTRA-Grade Testing

This test suite implements SPECTRA-grade testing practices:

- ✅ **Comprehensive coverage** (>75% overall)
- ✅ **Isolated unit tests** (mocked dependencies)
- ✅ **Integration tests** (end-to-end scenarios)
- ✅ **Automated CI/CD** (GitHub Actions)
- ✅ **Coverage reporting** (Codecov integration)
- ✅ **Structured error handling** (graceful degradation tests)
- ✅ **Data validation** (schema and quality tests)

---

**Version**: 0.3.0 (Build/MVP Phase)  
**Last Updated**: 2025-12-05  
**Maintainer**: SPECTRA Data Solutions
