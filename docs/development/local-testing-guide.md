# Local Testing Guide for Zephyr Notebooks
**Date:** 2025-01-29  
**Purpose:** Test notebooks locally without logging into Fabric

---

## Overview

You can test Zephyr notebooks locally using:
1. **Environment variables** - Already supported in notebook
2. **Local Spark session** - Run with local Spark
3. **Test scripts** - Extract logic into testable functions
4. **Mock testing** - Test API calls without Spark

---

## Method 1: Environment Variables + Local Spark

### Setup

1. **Create `.env` file** (gitignored) in `Data/zephyr/`:

```bash
# Zephyr API Configuration
DXC_ZEPHYR_BASE_URL=https://velonetic.yourzephyr.com
DXC_ZEPHYR_BASE_PATH=/flex/services/rest/latest
DXC_ZEPHYR_API_TOKEN=your_actual_token_here
```

2. **Load environment variables** (PowerShell):

```powershell
# From repo root
Get-Content .env | Where-Object { $_ -notmatch '^[\s#]' -and $_ -match '=' } | ForEach-Object { 
    $k,$v = $_ -split '=',2; 
    Set-Item -Path ('Env:' + $k.Trim()) -Value $v.Trim() 
}
```

3. **Install dependencies locally**:

```powershell
# Install SPECTRA Fabric SDK in editable mode
cd Data/fabric-sdk
pip install -e .

# Install additional dependencies
pip install pyspark requests
```

### Run Notebook Locally

The notebook already supports local runs via environment variables:

```python
# This code already exists in sourceZephyr.Notebook/notebook_content.py
# It will automatically use environment variables if pipeline parameters are empty

import os
if not zephyr_base_url:
    zephyr_base_url = os.environ.get("DXC_ZEPHYR_BASE_URL", zephyr_base_url)
if not zephyr_base_path:
    zephyr_base_path = os.environ.get("DXC_ZEPHYR_BASE_PATH", zephyr_base_path)
if not zephyr_api_token:
    zephyr_api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN", zephyr_api_token)
```

**To run:**
1. Load environment variables (see above)
2. Open notebook in Jupyter/VSCode
3. Run cells - Spark will use local session

---

## Method 2: Extract Logic to Test Script

Create a test script that extracts the notebook logic:

### Create `scripts/test_source_local.py`

```python
"""Local test script for Source stage - can run without Fabric."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import notebook logic (extract functions from notebook)
from sourceZephyr.Notebook.notebook_content import fetch_projects, fetch_releases, fetch_cycles, fetch_executions

def test_source_health_checks():
    """Test all Source stage health checks locally."""
    
    base_url = os.environ.get("DXC_ZEPHYR_BASE_URL", "")
    base_path = os.environ.get("DXC_ZEPHYR_BASE_PATH", "")
    api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN", "")
    
    if not all([base_url, base_path, api_token]):
        raise ValueError("Missing required environment variables")
    
    full_url = f"{base_url.rstrip('/')}{base_path}"
    
    print(f"Testing Zephyr Source stage health checks...")
    print(f"Base URL: {full_url}")
    print()
    
    # Test 1: Projects endpoint
    print("✅ Testing /project endpoint...")
    projects = fetch_projects(full_url, api_token)
    print(f"   Found {len(projects)} projects")
    print(f"   Sample: {projects[0]['name'] if projects else 'None'}")
    print()
    
    # Test 2: Releases endpoint (for each active project)
    active_projects = [40, 44]  # From discovery
    for project_id in active_projects:
        print(f"✅ Testing /release endpoint for project {project_id}...")
        releases = fetch_releases(full_url, api_token, project_id)
        print(f"   Found {len(releases)} releases")
        print()
    
    # Test 3: Cycles endpoint
    # ... (similar pattern)
    
    # Test 4: Executions endpoint
    # ... (similar pattern)
    
    print("✅ All health checks passed!")

if __name__ == "__main__":
    test_source_health_checks()
```

**Run:**
```powershell
cd Data/zephyr
python scripts/test_source_local.py
```

---

## Method 3: Mock Testing (No API Calls)

Test the logic without making actual API calls:

### Create `tests/test_source_mock.py`

```python
"""Mock tests for Source stage - no API calls needed."""

import pytest
from unittest.mock import Mock, patch
from sourceZephyr.Notebook.notebook_content import fetch_projects

def test_fetch_projects_success():
    """Test fetch_projects with mocked API response."""
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": 40, "name": "Vendor Testing POC"},
        {"id": 44, "name": "BP2 Test Management"}
    ]
    
    with patch('requests.Session.get', return_value=mock_response):
        result = fetch_projects("https://test.com", "fake-token")
        
    assert len(result) == 2
    assert result[0]["id"] == 40
    assert result[1]["name"] == "BP2 Test Management"

def test_fetch_projects_error():
    """Test fetch_projects with API error."""
    
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    
    with patch('requests.Session.get', return_value=mock_response):
        with pytest.raises(RuntimeError):
            fetch_projects("https://test.com", "fake-token")
```

**Run:**
```powershell
pytest tests/test_source_mock.py -v
```

---

## Method 4: Full Source Notebook Runner (Recommended)

### Setup

```powershell
# Install PySpark (required for local Spark session)
pip install pyspark

# Install SPECTRA framework (optional, for logging)
cd ../fabric-sdk
pip install -e .
cd ../zephyr
```

### Run Source Notebook Locally

Use the local runner script that mimics Fabric runtime:

```powershell
# Generate endpoints module first (one-time)
python scripts/generate_endpoints_module.py

# Run Source notebook locally with init_mode
python scripts/run_source_local.py --init-mode

# Or with debug output
python scripts/run_source_local.py --init-mode --debug
```

**What it does:**
- Creates local Spark session (mimics Fabric `synapse_pyspark` kernel)
- Mocks Fabric Files area (`local_fabric_files/`)
- Mocks Fabric Delta tables (`local_fabric_tables/`)
- Runs full Source notebook logic (endpoints bootstrap, health checks, quality gates)
- Generates quality gate report locally

**Outputs:**
- `local_fabric_files/config_zephyr_endpoints.json` - Bootstrapped endpoints
- `local_fabric_files/config_zephyr_quality_gate_report.json` - Quality gate report
- `local_fabric_tables/source_zephyr_endpoints/` - Endpoints table (parquet)
- `local_fabric_tables/source_zephyr_endpoint_health/` - Health check results (parquet)

### Quick Start

```powershell
# From Data/zephyr directory
.\scripts\test-local.ps1
```

This will:
1. Load `.env` variables
2. Run `run_source_local.py --init-mode`
3. Perform health checks on all GET endpoints
4. Generate quality gate report

---

## Recommended Approach

**For Full Source Stage Testing:** Use Method 4 (Full Source Notebook Runner) ⭐ **RECOMMENDED**
- Runs complete Source notebook logic
- Mocks Fabric runtime (Spark + Delta + Files)
- Tests all endpoints with health checks
- Generates quality gate report
- Closest to actual Fabric execution

**For Quick API Testing:** Use Method 1 (Test Script)
- Fastest setup
- Tests API connectivity
- No Spark required

**For Development:** Use Method 2 (Test Script)
- Faster iteration
- Can test individual functions
- Easier debugging

**For CI/CD:** Use Method 3 (Mock Testing)
- No API dependencies
- Fast execution
- Reliable tests

---

## Quick Start Script

Use `scripts/test-local.ps1` (already created):

```powershell
cd Data/zephyr
.\scripts\test-local.ps1
```

**For comprehensive testing of all endpoints:**
```powershell
python scripts/test_all_endpoints.py --category all
```

**For specific categories:**
```powershell
python scripts/test_all_endpoints.py --category testcase
python scripts/test_all_endpoints.py --category requirement
python scripts/test_all_endpoints.py --category execution
```

---

## Testing Checklist

- [ ] Environment variables loaded
- [ ] API token valid
- [ ] Can connect to Zephyr API
- [ ] `/project` endpoint works
- [ ] `/release` endpoint works (for both projects)
- [ ] `/cycle` endpoint works
- [ ] `/execution` endpoint works
- [ ] Pagination works (`firstresult`/`maxresults`)
- [ ] Error handling works
- [ ] Logging works

---

## Troubleshooting

### "spark is not defined"
- **Solution:** Create local Spark session (see Method 4)

### "Module not found: spectra"
- **Solution:** Install Fabric SDK: `pip install -e ../fabric-sdk`

### "Environment variable not found"
- **Solution:** Load `.env` file (see Method 1)

### "API connection failed"
- **Solution:** Check token, base URL, network connectivity

---

**Last Updated:** 2025-01-29

