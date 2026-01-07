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

# # Extract Stage — Zephyr Sample Extraction
# ### Level 0: Independent Endpoints
# 
# Extracts sample data from Zephyr API independent endpoints (no dependencies) and saves to lakehouse Delta tables.
# 
# **Endpoints:**
# - `/project/details` - All projects
# - `/release` - All releases
# 
# **Outputs:**
# - `extract.projects_sample` - Projects Delta table
# - `extract.releases_sample` - Releases Delta table
# 
# ---
# 
# **Status:** Phase 1 - Independent endpoints only
# **Note:** Requirement folders endpoint needs investigation (returns 404)


# CELL ********************

%run spectraSDK

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Parameters
mode: str = "run"
project: int = 0
bootstrap: bool = True
rebuild: bool = False
backfill: bool = False
test: bool = False
debug: bool = False

# Context
session = NotebookSession("zephyrVariables").load_context(
    bootstrap=bootstrap,
    backfill=backfill,
    project=project,
    rebuild=rebuild,
    debug=debug,
    mode=mode,
    spark=spark,
    preview=False,
    test=test,
)

# Initialise
log = session.initialize()

# Zephyr API base URL (SPECTRA-grade: prefer ctx full_url)
full_url = session.ctx.get("full_url", "")
api_token = session.variables.get_secret("API_TOKEN", "")

if not full_url or not api_token:
    raise ValueError("Missing Zephyr API configuration: ctx.full_url and variable API_TOKEN are required")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Import required libraries
import requests
import json
from typing import Dict, Any, List
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit
from pyspark.sql.types import StringType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

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

log.info("API headers configured")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Extract Projects
log.info("Extracting projects from /project/details...")
projects_result = call_zephyr_api("/project/details", headers)

if projects_result["status"] == "success":
    log.info(f"Successfully extracted {projects_result['count']} projects")
    projects_data = projects_result["data"]
    
    # Convert to DataFrame
    projects_df = spark.createDataFrame(projects_data)
    
    # Add extraction metadata
    from datetime import datetime
    projects_df = projects_df.withColumn("_extracted_at", lit(datetime.now().isoformat()))
    projects_df = projects_df.withColumn("_source_endpoint", lit("/project/details"))
    
    log.info("Projects DataFrame created")
    
else:
    log.error(f"Failed to extract projects: {projects_result.get('error')}")
    projects_df = None

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Save Projects to Delta Table
if projects_df is not None:
    if test:
        projects_df = projects_df.limit(10)
        log.info("Test mode: Limited projects to 10 records")

    table_name = "extract.projects_sample"
    table_path = "Tables/extract/projects_sample"
    session.delta.write(projects_df, table_name, table_path, mode="overwrite")
    session.delta.register(table_name, table_path)
    log.info(f"Wrote {table_name}")
else:
    log.error("Cannot write projects - extraction failed")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Extract Releases
log.info("Extracting releases from /release...")
releases_result = call_zephyr_api("/release", headers)

if releases_result["status"] == "success":
    log.info(f"Successfully extracted {releases_result['count']} releases")
    releases_data = releases_result["data"]
    
    # Convert to DataFrame
    releases_df = spark.createDataFrame(releases_data)
    
    # Add extraction metadata
    from datetime import datetime
    releases_df = releases_df.withColumn("_extracted_at", lit(datetime.now().isoformat()))
    releases_df = releases_df.withColumn("_source_endpoint", lit("/release"))
    
    log.info("Releases DataFrame created")
    
else:
    log.error(f"Failed to extract releases: {releases_result.get('error')}")
    releases_df = None

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Save Releases to Delta Table
if releases_df is not None:
    if test:
        releases_df = releases_df.limit(10)
        log.info("Test mode: Limited releases to 10 records")

    table_name = "extract.releases_sample"
    table_path = "Tables/extract/releases_sample"
    session.delta.write(releases_df, table_name, table_path, mode="overwrite")
    session.delta.register(table_name, table_path)
    log.info(f"Wrote {table_name}")
else:
    log.error("Cannot write releases - extraction failed")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Summary
log.info("=" * 80)
log.info("EXTRACTION SUMMARY")
log.info("=" * 80)

try:
    projects_count = spark.read.format("delta").load("Tables/extract/projects_sample").count()
    log.info(f"Projects: {projects_count} rows")
except Exception:
    pass

try:
    releases_count = spark.read.format("delta").load("Tables/extract/releases_sample").count()
    log.info(f"Releases: {releases_count} rows")
except Exception:
    pass

session.add_capability("extractSampleComplete")
session.finalise()

