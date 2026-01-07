# Local Source Notebook Runner - Quick Start

Run the Zephyr Source notebook locally with a Fabric runtime mock.

## Prerequisites

1. **Install PySpark:**
   ```powershell
   pip install pyspark
   ```

2. **Install SPECTRA framework (optional, for logging):**
   ```powershell
   cd ../fabric-sdk
   pip install -e .
   cd ../zephyr
   ```

3. **Create `.env` file** with:
   ```
   DXC_ZEPHYR_BASE_URL=https://velonetic.yourzephyr.com
   DXC_ZEPHYR_BASE_PATH=/flex/services/rest/latest
   DXC_ZEPHYR_API_TOKEN=your_actual_token_here
   ```

## Quick Start

### Option 1: PowerShell Wrapper (Easiest)

```powershell
cd Data/zephyr
.\scripts\test-local.ps1
```

This will:
- Load `.env` variables
- Run Source notebook with `--init-mode`
- Health check all GET endpoints
- Generate quality gate report

### Option 2: Direct Python

```powershell
# Generate endpoints module (one-time)
python scripts/generate_endpoints_module.py

# Run Source notebook
python scripts/run_source_local.py --init-mode

# With debug output
python scripts/run_source_local.py --init-mode --debug
```

## What It Does

1. **Creates local Spark session** (mimics Fabric `synapse_pyspark` kernel)
2. **Bootstraps endpoints.json** (if `--init-mode` or file missing)
3. **Loads all 228 endpoints** into mock Delta table
4. **Health checks all GET endpoints** (76+ endpoints)
5. **Generates quality gate report** with readiness status

## Outputs

All outputs are written to local directories (mocking Fabric):

- **Endpoints table:** `local_fabric_tables/source_zephyr_endpoints/` (parquet)
- **Health check results:** `local_fabric_tables/source_zephyr_endpoint_health/` (parquet)
- **Endpoints JSON:** `local_fabric_files/config_zephyr_endpoints.json`
- **Quality gate report:** `local_fabric_files/config_zephyr_quality_gate_report.json`

## What's Mocked

- ✅ **Spark session** - Local PySpark (same as Fabric)
- ✅ **Delta tables** - Written as Parquet locally
- ✅ **Files area** - Written as JSON locally
- ✅ **Notebook logic** - Runs exactly as in Fabric
- ❌ **Fabric workspace** - Not needed (local execution)
- ❌ **Fabric lakehouse** - Mocked with local directories

## Benefits

- **Test before deploying** - Validate logic locally
- **Faster iteration** - No Fabric deployment needed
- **Full Source stage** - Runs complete notebook logic
- **Quality gates** - Generates same reports as Fabric
- **Debug friendly** - Easy to inspect local outputs

## Troubleshooting

### "Module not found: pyspark"
```powershell
pip install pyspark
```

### "Module not found: spectra"
```powershell
cd ../fabric-sdk
pip install -e .
```

### "endpoints_module.py not found"
```powershell
python scripts/generate_endpoints_module.py
```

### "Environment variable not found"
- Check `.env` file exists in `Data/zephyr/`
- Or set environment variables directly

## Next Steps

After local testing passes:
1. Commit `endpoints_module.py` to repo
2. Deploy to Fabric
3. Run pipeline with `init_mode=true` (first time)
4. Run pipeline normally (subsequent runs)




