# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "9325ae26-a9ec-4c5b-a984-89235cb93b81",
# META       "default_lakehouse_name": "zephyrLakehouse",
# META       "default_lakehouse_workspace_id": "16490dde-33b4-446e-8120-c12b0a68ed88",
# META       "known_lakehouses": [
# META         {
# META           "id": "9325ae26-a9ec-4c5b-a984-89235cb93b81"
# META         }
# META       ]
# META     },
# META     "environment": {
# META       "environmentId": "92a8349b-6a62-b2e9-40bf-1ac52e9ab184",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Prepare Stage — Zephyr Data Extraction
# ### Extract data samples from independent endpoints
# 
# Extracts data samples from Zephyr API endpoints and saves to `Tables/prepare/` Delta tables.
# Table names match endpoint paths (e.g., `/project/details` → `Tables/prepare/project_details`).
# 
# **Current Endpoints:**
# - `/project/details` → `Tables/prepare/project_details`
# - `/release` → `Tables/prepare/release`
# 
# **Approach:** Start slow, build endpoints incrementally.

# CELL ********************

%run spectraSDK

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Parameters
bootstrap: bool = True
test: bool = False  # Set to True to limit records for testing

# Load context
session = NotebookSession("zephyrVariables").load_context(
    bootstrap=bootstrap,
    backfill=False,
    spark=spark,
    preview=False,
    test=test
)

# Get credentials
base_url = session.get_variable("BASE_URL")
base_path = session.get_variable("BASE_PATH")
api_token = session.get_variable("API_TOKEN")
full_url = f"{base_url}{base_path}"

print(f"[*] Base URL: {base_url}")
print(f"[*] Base Path: {base_path}")
print(f"[*] Full URL: {full_url}")
print(f"[*] Test Mode: {test}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Import required libraries
import requests
import json
from typing import Dict, Any
from datetime import datetime
from pyspark.sql.functions import lit

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def endpoint_to_table_name(endpoint: str) -> str:
    """
    Convert endpoint path to table name.
    
    Examples:
    /project/details -> project_details
    /release -> release
    /cycle/release/{id} -> cycle_release
    """
    # Remove leading slash
    name = endpoint.lstrip("/")
    # Replace path separators and parameters with underscores
    name = name.replace("/", "_").replace("{", "").replace("}", "")
    # Remove any trailing underscores
    name = name.rstrip("_")
    return name

def call_zephyr_api(endpoint: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Call Zephyr API endpoint and return JSON response.
    
    Args:
        endpoint: API endpoint path (e.g., "/project/details")
        headers: Request headers with authentication
        
    Returns:
        Dict with status, data, and metadata
    """
    url = f"{full_url}{endpoint}"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return {
            "status": "success",
            "data": data,
            "count": len(data) if isinstance(data, list) else 1,
            "endpoint": endpoint
        }
    except requests.exceptions.HTTPError as e:
        return {
            "status": "error",
            "error": str(e),
            "status_code": e.response.status_code if e.response else None,
            "endpoint": endpoint
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "endpoint": endpoint
        }

def extract_and_save(endpoint: str, headers: Dict[str, str], test_mode: bool = False):
    """
    Extract data from endpoint and save to Delta table.
    
    Args:
        endpoint: API endpoint path
        headers: Request headers
        test_mode: If True, limit to 10 records
    """
    table_name = endpoint_to_table_name(endpoint)
    table_path = f"Tables/prepare/{table_name}"
    
    print(f"\n{'=' * 80}")
    print(f"[*] Extracting: {endpoint}")
    print(f"[*] Table: {table_path}")
    print(f"{'=' * 80}")
    
    # Call API
    result = call_zephyr_api(endpoint, headers)
    
    if result["status"] != "success":
        print(f"[ERROR] Failed to extract {endpoint}")
        print(f"   Error: {result.get('error')}")
        return False
    
    data = result["data"]
    count = result["count"]
    
    print(f"[OK] Successfully extracted {count} records")
    
    # Convert to DataFrame
    df = spark.createDataFrame(data)
    
    # Add extraction metadata
    df = df.withColumn("_extracted_at", lit(datetime.now().isoformat()))
    df = df.withColumn("_source_endpoint", lit(endpoint))
    
    # Limit in test mode
    if test_mode:
        df = df.limit(10)
        print(f"[*] Test mode: Limited to 10 records")
    
    # Show schema
    print(f"\n[*] Schema:")
    df.printSchema()
    
    # Show sample
    print(f"\n[*] Sample data (first 3 rows):")
    df.show(3, truncate=False)
    
    # Write to Delta table
    print(f"\n[*] Writing to {table_path}...")
    
    try:
        # Drop table if exists (to avoid schema merge issues)
        spark.sql(f"DROP TABLE IF EXISTS delta.`{table_path}`")
    except:
        pass
    
    try:
        # Remove existing directory
        dbutils.fs.rm(table_path, recurse=True)
    except:
        pass
    
    # Write Delta table
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(table_path)
    
    # Register table
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS delta.`{table_path}`
        USING DELTA
        LOCATION '{table_path}'
    """)
    
    # Verify
    verify_count = spark.table(f"delta.`{table_path}`").count()
    print(f"[OK] Successfully wrote {verify_count} records to {table_path}")
    
    return True

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Build API headers
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print("[*] API headers configured")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Extract Level 0: Independent Endpoints
# Start with these 2 endpoints (no dependencies)

endpoints_to_extract = [
    "/project/details",  # All projects
    "/release"           # All releases
]

print(f"\n{'=' * 80}")
print(f"PREPARE STAGE: Extracting Independent Endpoints")
print(f"{'=' * 80}")
print(f"\n[*] Endpoints to extract: {len(endpoints_to_extract)}")
for ep in endpoints_to_extract:
    print(f"  - {ep} → Tables/prepare/{endpoint_to_table_name(ep)}")

results = {}

for endpoint in endpoints_to_extract:
    success = extract_and_save(endpoint, headers, test_mode=test)
    results[endpoint] = "success" if success else "error"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Summary
print(f"\n{'=' * 80}")
print("PREPARE STAGE SUMMARY")
print(f"{'=' * 80}")

for endpoint, status in results.items():
    table_name = endpoint_to_table_name(endpoint)
    table_path = f"Tables/prepare/{table_name}"
    
    if status == "success":
        count = spark.table(f"delta.`{table_path}`").count()
        print(f"\n[OK] {endpoint}")
        print(f"     Table: {table_path}")
        print(f"     Records: {count}")
    else:
        print(f"\n[ERROR] {endpoint}")
        print(f"     Status: Failed")

print(f"\n{'=' * 80}")
print("[OK] Prepare stage complete!")
print(f"{'=' * 80}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

