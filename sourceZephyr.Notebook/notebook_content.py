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

# # 🔗 Source Stage — Zephyr Enterprise
# ### Connectivity • Authentication • Endpoint Intelligence
# 
# Establishes secure connectivity, validates authentication, and catalogs all available API endpoints for downstream SPECTRA pipeline stages.
# 
# ---
# 
# ## Outputs
# - `source.portfolio` — Dashboard-ready system overview & metrics
# - `source.config` — Canonical configuration settings
# - `source.credentials` — Masked authentication materials
# - `source.endpoints` — Full API catalog


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

# Execute
SourceStageHelpers.execute_source_stage(spark=spark, session=session)

# Validate
session.validate()

# Record
session.record(spark=spark)

# Finalise
session.finalise()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
