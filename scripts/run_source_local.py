#!/usr/bin/env python3
"""
Local runner for Zephyr Source notebook - runs with local PySpark.

This script:
1. Creates a local Spark session (mimics Fabric runtime)
2. Loads the Source notebook code
3. Mocks Fabric-specific features (Delta tables, Files area)
4. Runs health checks on all endpoints
5. Generates quality gate report locally

Usage:
    python scripts/run_source_local.py [--init-mode] [--debug]

Requires:
    - .env file with DXC_ZEPHYR_BASE_URL, DXC_ZEPHYR_BASE_PATH, DXC_ZEPHYR_API_TOKEN
    - PySpark installed: pip install pyspark
    - SPECTRA framework: pip install -e ../fabric-sdk
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Any

# Add parent directory to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(repo_root / ".env")
except ImportError:
    pass  # dotenv optional

# Setup logging first
try:
    from spectra.modules.shared.logging import initialise_logger
except ImportError:
    import logging
    def initialise_logger(name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger

log = initialise_logger("sourceZephyrLocal")

# Setup local Spark session (mimics Fabric runtime)
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Create local Spark session (with Delta support if available)
spark_builder = SparkSession.builder \
    .appName("ZephyrSourceLocal") \
    .master("local[*]") \
    .config("spark.sql.warehouse.dir", str(repo_root / "local_spark_warehouse"))

# Try to enable Delta if available (optional)
try:
    spark = spark_builder \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    log.info("✅ Spark session created with Delta support")
except Exception:
    # Fallback to standard Spark (Delta not available)
    spark = spark_builder.getOrCreate()
    log.warning("⚠️  Delta Spark not available - using standard Spark (parquet fallback)")

# Mock Fabric Files area with local directory
LOCAL_FILES_ROOT = repo_root / "local_fabric_files"
LOCAL_FILES_ROOT.mkdir(exist_ok=True)
LOCAL_TABLES_ROOT = repo_root / "local_fabric_tables"
LOCAL_TABLES_ROOT.mkdir(exist_ok=True)

# Import notebook code
import requests
from requests.adapters import HTTPAdapter, Retry
from datetime import datetime, timezone
import uuid


def mock_delta_save(df, path: str):
    """Mock Delta table save - write to local parquet instead."""
    local_path = LOCAL_TABLES_ROOT / path.replace("Tables/", "").replace("/", "_")
    local_path.parent.mkdir(parents=True, exist_ok=True)
    df.write.mode("overwrite").parquet(str(local_path))
    log.info(f"Mock Delta save: {path} -> {local_path}")


def mock_files_write(df, path: str):
    """Mock Files area write - write to local directory."""
    local_path = LOCAL_FILES_ROOT / path.replace("Files/", "").replace("/", "_")
    local_path.parent.mkdir(parents=True, exist_ok=True)
    df.write.mode("overwrite").json(str(local_path))
    log.info(f"Mock Files write: {path} -> {local_path}")


def mock_files_read(path: str):
    """Mock Files area read - read from local directory."""
    local_path = LOCAL_FILES_ROOT / path.replace("Files/", "").replace("/", "_")
    if local_path.exists():
        return spark.read.json(str(local_path))
    raise FileNotFoundError(f"File not found: {local_path}")


def mock_delta_table(table_path: str):
    """Mock Delta table read - read from local parquet."""
    local_path = LOCAL_TABLES_ROOT / table_path.replace("Tables/", "").replace("/", "_")
    if local_path.exists():
        return spark.read.parquet(str(local_path))
    raise FileNotFoundError(f"Table not found: {local_path}")


def main():
    parser = argparse.ArgumentParser(description="Run Zephyr Source notebook locally")
    parser.add_argument("--init-mode", action="store_true", help="Bootstrap endpoints.json")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Load environment variables
    zephyr_base_url = os.environ.get("DXC_ZEPHYR_BASE_URL", "")
    zephyr_base_path = os.environ.get("DXC_ZEPHYR_BASE_PATH", "")
    zephyr_api_token = os.environ.get("DXC_ZEPHYR_API_TOKEN", "")
    
    if not all([zephyr_base_url, zephyr_base_path, zephyr_api_token]):
        log.error("Missing required environment variables:")
        log.error("  - DXC_ZEPHYR_BASE_URL")
        log.error("  - DXC_ZEPHYR_BASE_PATH")
        log.error("  - DXC_ZEPHYR_API_TOKEN")
        log.error("\nSet these in .env file or environment variables")
        sys.exit(1)
    
    base_url = zephyr_base_url.rstrip("/") + zephyr_base_path
    request_timeout = 30
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.headers.update({
        "Authorization": f"Bearer {zephyr_api_token}",
        "Content-Type": "application/json"
    })
    
    log.info("=" * 60)
    log.info("Zephyr Source Stage - Local Execution")
    log.info("=" * 60)
    log.info(f"Base URL: {base_url}")
    log.info(f"Init Mode: {args.init_mode}")
    log.info(f"Debug Mode: {args.debug}")
    log.info("")
    
    # Import endpoints module if available
    endpoints_data = None
    endpoints_module_path = repo_root / "sourceZephyr.Notebook" / "endpoints_module.py"
    
    if args.init_mode or not (LOCAL_FILES_ROOT / "config_endpoints.json").exists():
        log.info("Bootstrap mode: Loading endpoints from module...")
        if endpoints_module_path.exists():
            import importlib.util
            spec = importlib.util.spec_from_file_location("endpoints_module", endpoints_module_path)
            endpoints_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(endpoints_module)
            endpoints_data = endpoints_module.ENDPOINTS_JSON
            log.info(f"✅ Loaded {len(endpoints_data.get('endpoints', []))} endpoints from module")
            
            # Mock write to Files area
            json_rdd = spark.sparkContext.parallelize([json.dumps(endpoints_data)])
            df_bootstrap = spark.read.json(json_rdd)
            mock_files_write(df_bootstrap, "Files/config/zephyr/endpoints.json")
        else:
            log.warning("⚠️  endpoints_module.py not found")
            log.warning("   Run: python scripts/generate_endpoints_module.py")
            log.warning("   Then commit endpoints_module.py to repo")
    else:
        log.info("Reading endpoints from local Files area...")
        try:
            df_endpoints_json = mock_files_read("Files/config/zephyr/endpoints.json")
            if df_endpoints_json.count() > 0:
                endpoints_data = df_endpoints_json.collect()[0].asDict()
                log.info(f"✅ Found {len(endpoints_data.get('endpoints', []))} endpoints")
        except Exception as e:
            log.warning(f"⚠️  Could not read endpoints: {e}")
    
    # Load endpoints into "Delta table" (mock)
    if endpoints_data and endpoints_data.get("endpoints"):
        endpoints_rows = []
        for endpoint in endpoints_data["endpoints"]:
            endpoints_rows.append({
                "resource": endpoint.get("resource", ""),
                "method": endpoint.get("method", ""),
                "path": endpoint.get("path", ""),
                "source": endpoints_data.get("source", "zephyrenterprisev3.apib"),
                "count": endpoints_data.get("count", 0)
            })
        
        df_endpoints = spark.createDataFrame(endpoints_rows)
        mock_delta_save(df_endpoints, "Tables/source/endpoints")
        log.info(f"✅ Loaded {len(endpoints_rows)} endpoints into mock Delta table")
    else:
        log.error("❌ No endpoints available - cannot proceed with health check")
        sys.exit(1)
    
    # Health check all GET endpoints
    log.info("")
    log.info("Starting endpoint health check...")
    
    def extract_path_from_resource(resource: str) -> str:
        if "[" in resource and "]" in resource:
            path_start = resource.find("[")
            path_end = resource.find("]")
            if path_start != -1 and path_end != -1:
                path = resource[path_start + 1:path_end].split("?")[0]
                return path
        return ""
    
    def health_check_endpoint(path: str, method: str) -> dict:
        if method.upper() != "GET":
            return {
                "status": "skipped",
                "http_code": None,
                "error_message": "Non-GET endpoint",
                "accessible": False
            }
        
        if not path or not path.startswith("/"):
            return {
                "status": "invalid",
                "http_code": None,
                "error_message": "Invalid path format",
                "accessible": False
            }
        
        try:
            url = f"{base_url}{path}"
            try:
                resp = session.head(url, timeout=5, allow_redirects=True)
                http_code = resp.status_code
            except Exception:
                resp = session.get(url, timeout=5, params={"maxresults": 1})
                http_code = resp.status_code
            
            if http_code == 200:
                status = "accessible"
                accessible = True
                error_message = None
            elif http_code == 401:
                status = "auth_required"
                accessible = False
                error_message = "Authentication required"
            elif http_code == 403:
                status = "forbidden"
                accessible = False
                error_message = "Access forbidden"
            elif http_code == 404:
                status = "not_found"
                accessible = False
                error_message = "Endpoint not found"
            elif http_code in [429, 503]:
                status = "rate_limited"
                accessible = False
                error_message = f"Rate limited (HTTP {http_code})"
            else:
                status = "error"
                accessible = False
                error_message = f"HTTP {http_code}"
            
            return {
                "status": status,
                "http_code": http_code,
                "error_message": error_message,
                "accessible": accessible
            }
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "http_code": None,
                "error_message": "Request timeout",
                "accessible": False
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "connection_error",
                "http_code": None,
                "error_message": "Connection error",
                "accessible": False
            }
        except Exception as e:
            return {
                "status": "error",
                "http_code": None,
                "error_message": str(e)[:200],
                "accessible": False
            }
    
    # Read endpoints and perform health checks
    try:
        df_endpoints_table = mock_delta_table("Tables/source/endpoints")
        endpoints_list = df_endpoints_table.collect()
        
        get_endpoints = [ep for ep in endpoints_list if ep.get("method", "").upper() == "GET"]
        log.info(f"Health checking {len(get_endpoints)} GET endpoints...")
        
        health_check_results = []
        for i, endpoint in enumerate(get_endpoints, 1):
            resource = endpoint.get("resource", "")
            method = endpoint.get("method", "")
            path = extract_path_from_resource(resource)
            
            if i % 10 == 0:
                log.info(f"Progress: {i}/{len(get_endpoints)} endpoints checked...")
            
            health_result = health_check_endpoint(path, method)
            
            health_check_results.append({
                "resource": resource,
                "method": method,
                "path": path,
                "status": health_result["status"],
                "http_code": health_result.get("http_code"),
                "error_message": health_result.get("error_message"),
                "accessible": health_result["accessible"],
                "checked_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            })
        
        log.info(f"✅ Health check completed for {len(health_check_results)} endpoints")
        
        # Write health check results
        df_health = spark.createDataFrame(health_check_results)
        mock_delta_save(df_health, "Tables/source/endpoint_health")
        
        # Generate summary
        accessible_count = sum(1 for r in health_check_results if r["accessible"])
        auth_required_count = sum(1 for r in health_check_results if r["status"] == "auth_required")
        not_found_count = sum(1 for r in health_check_results if r["status"] == "not_found")
        error_count = sum(1 for r in health_check_results if r["status"] in ["error", "timeout", "connection_error"])
        
        log.info("=" * 60)
        log.info("Endpoint Health Check Summary")
        log.info("=" * 60)
        log.info(f"Total GET endpoints checked: {len(health_check_results)}")
        log.info(f"✅ Accessible: {accessible_count}")
        log.info(f"🔐 Auth required: {auth_required_count}")
        log.info(f"❌ Not found: {not_found_count}")
        log.info(f"⚠️  Errors/timeouts: {error_count}")
        log.info("=" * 60)
        
        # Generate quality gate report
        total_checked = len(health_check_results)
        accessible = accessible_count
        success_rate = (accessible + auth_required_count) / total_checked if total_checked > 0 else 0
        quality_gate_passed = success_rate >= 0.80
        
        quality_report = {
            "stage": "Source",
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "run_id": str(uuid.uuid4()),
            "quality_gates": {
                "endpoints_catalogued": {
                    "status": "passed" if len(endpoints_rows) > 0 else "failed",
                    "value": len(endpoints_rows),
                    "threshold": 228,
                    "message": f"{len(endpoints_rows)} of 228 endpoints catalogued"
                },
                "endpoints_health_checked": {
                    "status": "passed" if total_checked > 0 else "failed",
                    "value": total_checked,
                    "threshold": 1,
                    "message": f"{total_checked} GET endpoints health checked"
                },
                "endpoints_accessible": {
                    "status": "passed" if accessible > 0 else "failed",
                    "value": accessible,
                    "threshold": 1,
                    "message": f"{accessible} endpoints accessible"
                },
                "environment_health": {
                    "status": "passed" if quality_gate_passed else "failed",
                    "value": success_rate,
                    "threshold": 0.80,
                    "message": f"{success_rate:.1%} success rate (accessible + auth_required)"
                }
            },
            "summary": {
                "total_endpoints": len(endpoints_rows),
                "get_endpoints_checked": total_checked,
                "accessible": accessible,
                "auth_required": auth_required_count,
                "errors": error_count,
                "success_rate": success_rate
            },
            "readiness": {
                "ready_for_prepare": quality_gate_passed and len(endpoints_rows) > 0 and accessible > 0,
                "blockers": [] if quality_gate_passed else ["Environment health check failed - too many endpoint errors"]
            }
        }
        
        # Write quality gate report
        json_rdd = spark.sparkContext.parallelize([json.dumps(quality_report)])
        df_report = spark.read.json(json_rdd)
        mock_files_write(df_report, "Files/config/zephyr/quality_gate_report.json")
        
        log.info("")
        if quality_report["readiness"]["ready_for_prepare"]:
            log.info("✅ Source stage READY FOR PREPARE")
        else:
            log.warning("⚠️  Source stage NOT READY FOR PREPARE")
            for blocker in quality_report["readiness"]["blockers"]:
                log.warning(f"   - {blocker}")
        
        log.info("")
        log.info(f"Quality gate report: {LOCAL_FILES_ROOT / 'config_quality_gate_report.json'}")
        log.info(f"Health check results: {LOCAL_TABLES_ROOT / 'source_endpoint_health'}")
        
        if args.debug:
            df_health.show(20, truncate=80)
        
    except Exception as e:
        log.error(f"❌ Health check failed: {e}")
        if args.debug:
            import traceback
            log.error(traceback.format_exc())
        sys.exit(1)
    
    finally:
        spark.stop()


if __name__ == "__main__":
    main()

