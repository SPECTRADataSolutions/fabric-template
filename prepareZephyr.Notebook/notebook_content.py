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

# # prepareZephyr - Prepare Stage (Schema Intelligence)
# 
# **SPECTRA Seven-Stage Pattern** - Schema Discovery & Intelligence Management
# 
# Builds and manages schema intelligence from API samples or existing Fabric tables.
# 
# **Last Updated:** 2025-12-11 (bootstrap + rebuild parameter upgrade)
# 
# **Parameters:**
# - `bootstrap` - Create/update Prepare stage configuration tables (one-time foundation)
#   - If tables don't exist, automatically enables `rebuild` to fetch full schema from API samples
#   - If tables exist, uses existing schema (or SDK fallback)
# - `rebuild` - Rebuild schema from API samples (for version updates)
#   - Fetches samples from production project 44 (READ-ONLY, GET requests only)
#   - Builds perfect L6 schema from actual API data
# - `test` - Run comprehensive validation tests
# 
# **Inputs:**
# - `source.endpoints` - Endpoint catalog from Source stage
# - `prepare.schema` - Existing schema (if tables exist, fallback to SDK)
# - `prepare.dependencies` - Entity relationships (if tables exist, fallback to SDK)
# - `prepare.constraints` - API constraints (if tables exist, fallback to SDK)
# 
# **Outputs:**
# - `prepare.schema` - Field-level metadata for Extract field promotion
# - `prepare.dependencies` - Entity relationships for Transform stage
# - `prepare.constraints` - API limitations & workarounds for Extract
# - `sample.{entity}` - Sample data tables (when rebuild=True)
# 
# **SDK:** spectra-fabric-sdk v0.3.0 (from spectraSDK.Notebook)

# CELL ********************

%run spectraSDK

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# == 1. PARAMETERS =================================================== SPECTRA

mode: str = "run"          # run | refresh | intelligence
project: int = 0            # Optional project override (0 = default for mode)
bootstrap: bool = True      # Create/update Prepare stage configuration tables
rebuild: bool = False       # Force rebuild schema/intelligence from samples
backfill: bool = False      # Full load intent (passed through for downstream stages)
test: bool = False          # Run comprehensive validation tests
debug: bool = False         # Enable verbose logging and intermediate outputs

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# == 2. CONTEXT ====================================================== SPECTRA

session = NotebookSession("zephyrVariables")  # Variable Library name
session.load_context(
    bootstrap=bootstrap,
    backfill=backfill,
    test=test,
    debug=debug,
    mode=mode,
    project=project,
    rebuild=rebuild,
    spark=spark,
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# == 3. INITIALIZE =================================================== SPECTRA

log = session.initialize()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# == 3.1 SAFETY GUARDRAILS ============================================ SPECTRA

mode_norm = (mode or "").strip().lower()
run = mode_norm == "run"
refresh = mode_norm == "refresh"
intelligence = mode_norm == "intelligence"

if mode_norm not in ("run", "refresh", "intelligence"):
    raise ValueError(f"SPECTRA Safety: Invalid mode='{mode}'. Expected one of: run, refresh, intelligence")

# Environment configuration (SPECTRA-grade: Variable Library owns environment constants)
prod_project_id = session.variables.get_int("PROD_PROJECT_ID", 44)
test_project_id = session.variables.get_int("TEST_PROJECT_ID", 45)

# Determine effective project ID based on mode
effective_project_id = project if project != 0 else (test_project_id if intelligence else prod_project_id)

# Production safety rules
if effective_project_id == prod_project_id and intelligence:
    raise ValueError(f"SPECTRA Safety: Intelligence mode cannot target PROD_PROJECT_ID={prod_project_id}. Use TEST_PROJECT_ID={test_project_id}")
if effective_project_id == prod_project_id:
    log.warning(f"SPECTRA Safety: READ-ONLY enforced for PROD_PROJECT_ID={prod_project_id}")

writes_allowed = bool(intelligence and effective_project_id == test_project_id)

# Log effective configuration
log.info(
    f"SPECTRA Configuration: mode={mode_norm}, project={effective_project_id}, "
    f"writes_allowed={writes_allowed}, backfill={backfill}, rebuild={rebuild}"
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# == 4. EXECUTE (Build Schema from Samples OR Load Intelligence) ===== SPECTRA

log.info("=" * 80)
# Mode-specific execution logic
if intelligence:
    log.info("INTELLIGENCE MODE: Write-capable probing to generate candidate intelligence...")
    # Intelligence mode will rebuild schema from samples with write capability
    rebuild = True
elif refresh:
    log.info("REFRESH MODE: Read-only drift detection and metadata rebuild...")
    # Refresh mode rebuilds metadata from production samples (GET-only)
    rebuild = True
else:  # run mode
    log.info("RUN MODE: Normal pipeline execution using canonical metadata...")
    # Check if tables exist for run mode
    if bootstrap:
        try:
            _ = spark.table("prepare.schema").count()
            log.info("Loading canonical metadata from Fabric tables...")
        except Exception:
            log.warning(
                "SPECTRA Bootstrap: prepare.schema table not found. "
                "Auto-enabling rebuild=True and bootstrap=True to create canonical metadata."
            )
            rebuild = True
            bootstrap = True
            try:
                session.params["rebuild"] = True
                session.params["bootstrap"] = True
            except Exception:
                pass
    else:
        log.info("Loading canonical metadata from Fabric tables...")
log.info("=" * 80)

from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, BooleanType,
    ArrayType, MapType
)

# Two paths: Build from samples OR load from intelligence
if rebuild:
    # PATH 1: Rebuild perfect schema FROM sample data
    # PRODUCTION DATA SAFETY: Project 44 - READ-ONLY mode
    # - Only GET requests (no POST/PUT/DELETE)
    # - No writes to Zephyr API
    # - Only reads sample data to infer schema
    log.info("  >> Fetching sample data to rebuild schema...")
    
    import requests
    from datetime import datetime
    
    # Import ZephyrIntelligence (available from spectraSDK via %run)
    # SPECTRA-grade: ZephyrIntelligence is defined directly in spectraSDK.Notebook
    # After %run spectraSDK, ZephyrIntelligence is available in global namespace
    try:
        # Check if ZephyrIntelligence is available (from %run spectraSDK)
        if 'ZephyrIntelligence' not in globals():
            raise NameError("ZephyrIntelligence not found in global namespace")
        
        # Verify it's the right class (SDK has ENTITIES, intelligence.py has SCHEMAS)
        # Check for either ENTITIES (SDK) or SCHEMAS (intelligence.py)
        has_entities = hasattr(ZephyrIntelligence, 'ENTITIES')
        has_schemas = hasattr(ZephyrIntelligence, 'SCHEMAS')
        
        if not has_entities and not has_schemas:
            raise AttributeError("ZephyrIntelligence missing ENTITIES or SCHEMAS attribute")
        
        # READ_ENDPOINTS is in intelligence.py (not in SDK yet)
        # If missing, we'll handle gracefully in the code
        if not hasattr(ZephyrIntelligence, 'READ_ENDPOINTS'):
            log.warning("  !! ZephyrIntelligence missing READ_ENDPOINTS - will use fallback logic")
        
        log.info("  OK ZephyrIntelligence available from spectraSDK")
    except (NameError, AttributeError) as e:
        log.error(f"  !! ZephyrIntelligence not available: {e}")
        log.error("  !! Ensure %run spectraSDK is executed before this cell")
        log.error("  !! ZephyrIntelligence is defined in spectraSDK.Notebook")
        raise ImportError(f"ZephyrIntelligence not found. Error: {e}. Ensure %run spectraSDK is executed first.")
    
    # Get API credentials (SPECTRA-grade: use session.variables.get_secret() for secrets, ctx for URLs)
    # Use full_url like sourceZephyr does (contains base_url + base_path already)
    base_url = session.ctx.get("full_url", "")
    api_token = session.variables.get_secret("API_TOKEN", "")
    base_path = session.ctx.get("base_path", "/flex/services/rest/latest")  # Default Zephyr API path
    
    if not base_url or not api_token:
        log.error("  !! Missing API credentials - cannot run rebuild mode")
        raise ValueError("rebuild=True requires base_url and api_token in Variable Library")
    
    # PRODUCTION SAFETY: Only GET requests allowed
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Fetch samples and build schema
    schema_data = []
    sample_data = {}
    
    # Mode-specific project targeting
    if intelligence:
        log.info(f"  INTELLIGENCE MODE: Targeting test project {effective_project_id} (write-capable probing)")
    else:
        log.info(f"  {'REFRESH' if refresh else 'RUN'} MODE: Targeting project {effective_project_id} (read-only)")
    
    # Fetch sample cycles (most complex entity with arrays)
    # SPECTRA-grade: Use intelligence READ endpoints
    # Cycles depend on releases (hierarchical dependency)
    log.info(f"  Fetching sample cycles from project {effective_project_id}...")
    try:
        # Step 0: Fetch project details first (verify project exists)
        log.info(f"  Step 0: Loading project {effective_project_id}...")
        if hasattr(ZephyrIntelligence, 'get_read_endpoint'):
            project_endpoint = ZephyrIntelligence.get_read_endpoint("project")
            if project_endpoint:
                project_path = ZephyrIntelligence.get_read_endpoint_path("project", projectId=effective_project_id)
                if project_path:
                    project_url = f"{base_url.rstrip('/')}{project_path}"
                else:
                    project_url = f"{base_url.rstrip('/')}/project?projectId={effective_project_id}"
            else:
                project_url = f"{base_url.rstrip('/')}/project?projectId={effective_project_id}"
        else:
            project_url = f"{base_url.rstrip('/')}/project?projectId={effective_project_id}"
        
        log.info(f"    DEBUG: Project URL: {project_url}")
        project_response = requests.get(project_url, headers=headers, timeout=10)
        project_response.raise_for_status()
        project_data = project_response.json()
        
        # Handle nested response
        if isinstance(project_data, dict):
            if "data" in project_data:
                project_data = project_data["data"]
            elif "items" in project_data:
                project_data = project_data["items"]
            elif "results" in project_data:
                project_data = project_data["results"]
        
        # If project_data is a list, get first item
        if isinstance(project_data, list) and len(project_data) > 0:
            project_data = project_data[0]
        
        if isinstance(project_data, dict):
            project_name = project_data.get("name", "Unknown")
            source_project_key = project_data.get("projectKey") or project_data.get("key")
            if source_project_key:
                log.info(f"    OK Project loaded: {project_name} (Key: {source_project_key}, ID: {effective_project_id})")
            else:
                log.info(f"    OK Project loaded: {project_name} (ID: {effective_project_id})")
            # Store project data for schema building
            sample_data["projects"] = [project_data]
        else:
            log.warning(f"    !! Project response format unexpected: {type(project_data)}")
            # Create minimal project data from context
            sample_data["projects"] = [{
                "id": effective_project_id,
                "name": "Sample Project"
            }]
        
        # Step 1: Fetch releases for project (READ-ONLY)
        # Use intelligence READ endpoint for releases (with fallback if not in SDK)
        if hasattr(ZephyrIntelligence, 'get_read_endpoint'):
            release_endpoint = ZephyrIntelligence.get_read_endpoint("release")
            if release_endpoint:
                releases_path = ZephyrIntelligence.get_read_endpoint_path("release", projectId=effective_project_id)
                if releases_path:
                    releases_url = f"{base_url.rstrip('/')}{releases_path}"
                else:
                    # Fallback: Use simple endpoint with query param
                    releases_url = f"{base_url.rstrip('/')}/release?projectId={effective_project_id}"
            else:
                # Fallback: Use simple endpoint with query param
                releases_url = f"{base_url.rstrip('/')}/release?projectId={effective_project_id}"
        else:
            # Fallback: SDK doesn't have READ_ENDPOINTS - use simple endpoint
            releases_url = f"{base_url.rstrip('/')}/release?projectId={effective_project_id}"
        log.info(f"    DEBUG: Releases URL: {releases_url}")
        # SPECTRA-grade: Shorter timeout to fail fast (10s) - prevents Livy session timeout
        releases_response = requests.get(releases_url, headers=headers, timeout=10)
        releases_response.raise_for_status()
        releases = releases_response.json()
        
        # Handle nested response structures
        if isinstance(releases, dict):
            if "data" in releases:
                releases = releases["data"]
            elif "items" in releases:
                releases = releases["items"]
            elif "results" in releases:
                releases = releases["results"]
        
        if not releases or len(releases) == 0:
            raise ValueError(f"No releases found for project {effective_project_id}")
        
        # Store releases in sample_data for hierarchical writing (projects → releases → cycles)
        sample_data["releases"] = releases
        
        # Step 1b: Take note of all releases found
        log.info(f"    OK Found {len(releases)} releases in project {effective_project_id}:")
        release_summary = []
        for idx, release in enumerate(releases[:20], 1):  # Log first 20 releases
            release_id_val = release.get("id", "N/A")
            release_name = release.get("name", "Unknown")
            release_summary.append(f"      {idx}. Release {release_id_val}: {release_name}")
        log.info("\n".join(release_summary))
        if len(releases) > 20:
            log.info(f"      ... and {len(releases) - 20} more releases")
        
        # Step 1c: Select release for schema discovery
        # SPECTRA-grade: Prioritize releases 112 and 106 (known to have cycles in project 44)
        prioritized_release_ids = [112, 106]
        release_id = None
        
        # Try to find prioritized releases first
        for priority_id in prioritized_release_ids:
            for release in releases:
                if release.get("id") == priority_id:
                    release_id = priority_id
                    release_name = release.get("name", "Unknown")
                    log.info(f"    Using prioritized release {release_id} ({release_name}) - known to have cycles...")
                    break
            if release_id:
                break
        
        # If prioritized releases not found, use first release
        if not release_id:
            for release in releases[:10]:  # Try first 10 releases
                candidate_id = release.get("id")
                if candidate_id:
                    release_id = candidate_id
                    release_name = release.get("name", "Unknown")
                    log.info(f"    Trying release {release_id} ({release_name})...")
                    break
        
        if not release_id:
            raise ValueError(f"No valid release ID found in releases")
        
        log.info(f"    Selected release {release_id} for schema discovery")
        
        # Step 2: Fetch cycles for this release (READ-ONLY)
        # SPECTRA-grade: Use intelligence READ endpoint for cycles (with fallback if not in SDK)
        log.info(f"    Step 2: Fetching cycles for release {release_id}...")
        if hasattr(ZephyrIntelligence, 'get_read_endpoint'):
            cycle_endpoint = ZephyrIntelligence.get_read_endpoint("cycle")
            if cycle_endpoint:
                cycles_path = ZephyrIntelligence.get_read_endpoint_path("cycle", releaseid=release_id)
                if cycles_path:
                    cycles_url = f"{base_url.rstrip('/')}{cycles_path}"
                else:
                    # Fallback: Use correct endpoint pattern /cycle/release/{releaseid}
                    cycles_url = f"{base_url.rstrip('/')}/cycle/release/{release_id}"
            else:
                # Fallback: Use correct endpoint pattern /cycle/release/{releaseid}
                cycles_url = f"{base_url.rstrip('/')}/cycle/release/{release_id}"
        else:
            # Fallback: SDK doesn't have READ_ENDPOINTS - use correct endpoint pattern
            cycles_url = f"{base_url.rstrip('/')}/cycle/release/{release_id}"
        log.info(f"    DEBUG: Cycles URL: {cycles_url}")
        # SPECTRA-grade: Shorter timeout to fail fast (10s) - prevents Livy session timeout
        response = requests.get(cycles_url, headers=headers, timeout=10)
        response.raise_for_status()
        cycles = response.json()
        
        log.info(f"    DEBUG: Cycles response type: {type(cycles)}, length: {len(cycles) if isinstance(cycles, (list, dict)) else 'N/A'}")
        if isinstance(cycles, dict):
            log.info(f"    DEBUG: Cycles response keys: {list(cycles.keys())}")
            # Some APIs return {"data": [...]} or {"items": [...]}
            if "data" in cycles:
                cycles = cycles["data"]
                log.info(f"    DEBUG: Extracted cycles from 'data' key: {len(cycles)} items")
            elif "items" in cycles:
                cycles = cycles["items"]
                log.info(f"    DEBUG: Extracted cycles from 'items' key: {len(cycles)} items")
            elif "results" in cycles:
                cycles = cycles["results"]
                log.info(f"    DEBUG: Extracted cycles from 'results' key: {len(cycles)} items")
        
        # If cycles is empty, try other releases
        if not cycles or len(cycles) == 0:
            log.warning(f"    !! No cycles found for release {release_id}")
            log.warning(f"    !! Trying other releases...")
            
            # Try next 5 releases
            for release in releases[1:6]:
                candidate_id = release.get("id")
                if not candidate_id:
                    continue
                
                log.info(f"    Trying release ID {candidate_id}...")
                try:
                    candidate_cycles_url = f"{base_url.rstrip('/')}/cycle/release/{candidate_id}"
                    candidate_response = requests.get(candidate_cycles_url, headers=headers, timeout=10)
                    candidate_response.raise_for_status()
                    candidate_cycles = candidate_response.json()
                    
                    # Handle nested response
                    if isinstance(candidate_cycles, dict):
                        if "data" in candidate_cycles:
                            candidate_cycles = candidate_cycles["data"]
                        elif "items" in candidate_cycles:
                            candidate_cycles = candidate_cycles["items"]
                        elif "results" in candidate_cycles:
                            candidate_cycles = candidate_cycles["results"]
                    
                    if candidate_cycles and len(candidate_cycles) > 0:
                        cycles = candidate_cycles
                        release_id = candidate_id
                        log.info(f"    OK Found {len(cycles)} cycles for release {release_id}")
                        break
                except Exception as e:
                    log.debug(f"    Release {candidate_id} failed: {e}")
                    continue
        
        # If still no cycles, try fetching without release filter (if API supports it)
        if not cycles or len(cycles) == 0:
            log.warning("    !! No cycles found for any release")
            log.warning("    !! Trying alternative: fetch cycles without release filter...")
            try:
                # Try direct cycles endpoint (might return all cycles for project)
                cycles_direct_url = f"{base_url.rstrip('/')}/cycle?projectId={effective_project_id}"
                log.info(f"    DEBUG: Direct cycles URL: {cycles_direct_url}")
                direct_response = requests.get(cycles_direct_url, headers=headers, timeout=10)
                direct_response.raise_for_status()
                cycles_direct = direct_response.json()
                
                # Handle nested response
                if isinstance(cycles_direct, dict):
                    if "data" in cycles_direct:
                        cycles_direct = cycles_direct["data"]
                    elif "items" in cycles_direct:
                        cycles_direct = cycles_direct["items"]
                    elif "results" in cycles_direct:
                        cycles_direct = cycles_direct["results"]
                
                if cycles_direct and len(cycles_direct) > 0:
                    cycles = cycles_direct
                    log.info(f"    OK Found {len(cycles)} cycles via direct endpoint")
            except Exception as e:
                log.debug(f"    Direct cycles endpoint failed: {e}")
        
        # If still no cycles, try testcases as fallback (they might have data)
        using_testcases = False  # Initialize flag
        if not cycles or len(cycles) == 0:
            log.warning("    !! Still no cycles found")
            log.warning("    !! Trying testcases as fallback entity for schema discovery...")
            try:
                testcases_url = f"{base_url.rstrip('/')}/testcase?projectId={effective_project_id}"
                log.info(f"    DEBUG: Testcases URL: {testcases_url}")
                testcases_response = requests.get(testcases_url, headers=headers, timeout=10)
                testcases_response.raise_for_status()
                testcases = testcases_response.json()
                
                # Handle nested response
                if isinstance(testcases, dict):
                    if "data" in testcases:
                        testcases = testcases["data"]
                    elif "items" in testcases:
                        testcases = testcases["items"]
                    elif "results" in testcases:
                        testcases = testcases["results"]
                
                if testcases and len(testcases) > 0:
                    # Use testcases instead of cycles for schema discovery
                    sample_data["testcases"] = testcases
                    log.info(f"  == Fetched {len(testcases)} sample testcases (using as fallback)")
                    # Set cycles to testcases so schema building logic works
                    cycles = testcases
                    # Mark that we're using testcases (will be checked in schema building)
                    using_testcases = True
                else:
                    using_testcases = False
            except Exception as e:
                log.debug(f"    Testcases endpoint failed: {e}")
                using_testcases = False
        else:
            using_testcases = False
        
        if cycles and len(cycles) > 0:
            sample_data["cycles"] = cycles
            log.info(f"  == Fetched {len(cycles)} sample cycles from release {release_id}")
            
            # SPECTRA-GRADE: Build perfect schema from sample (L6 Jira-proven pattern)
            sample_cycle = cycles[0].copy()  # Make a copy to avoid modifying original
            source_entity = "cycle"  # Source entity name (for context)
            
            # Add projectId from context (cycles might not have it directly)
            if "projectId" not in sample_cycle:
                sample_cycle["projectId"] = effective_project_id
                log.info(f"    Added projectId={effective_project_id} to cycle from context")
            
            # Debug: Log what fields are in the cycle
            log.info(f"    DEBUG: Cycle fields: {list(sample_cycle.keys())}")
            log.info(f"    DEBUG: Cycle sample: {json.dumps({k: v for k, v in list(sample_cycle.items())[:5]}, indent=2)}")
            
            # Helper: Generate target field name (SPECTRA explicit naming)
            def generate_target_name(field_name: str, prop_name: str = None, is_array: bool = False) -> str:
                """Generate target field name following SPECTRA explicit naming convention."""
                if prop_name:
                    # Nested property: cyclePhases[].id → cyclePhaseId
                    singular = field_name.rstrip('s') if field_name.endswith('s') else field_name
                    if prop_name == "id":
                        return f"{singular}Id"
                    elif prop_name == "name":
                        return singular
                    else:
                        return f"{singular}{prop_name.capitalize()}"
                else:
                    # Direct field: id → cycleId, name → cycleName
                    if field_name == "id":
                        return f"{source_entity}Id"
                    elif field_name == "name":
                        return f"{source_entity}Name"
                    else:
                        return field_name
            
            # Helper: Singularize for dimension names
            def singularize(name: str) -> str:
                """Convert plural to singular for dimension names."""
                if name.endswith('ies'):
                    return name[:-3] + 'y'
                elif name.endswith('s') and not name.endswith('ss'):
                    return name[:-1]
                return name
            
            # Helper: Infer SPECTRA data type
            def infer_spectra_type(value, is_array_element: bool = False) -> str:
                """Infer SPECTRA data type from Python value."""
                if isinstance(value, bool):
                    return "bool"
                elif isinstance(value, int):
                    return "int64"
                elif isinstance(value, float):
                    return "float64"
                else:
                    return "text"  # SPECTRA uses "text" not "string"
            
            # Helper: Determine group (logical grouping)
            def determine_group(field_name: str) -> tuple:
                """Determine logical group and sort order."""
                if field_name in ["id", "key", "name"]:
                    return ("cycleIdentifier", 1)
                elif "date" in field_name.lower() or "time" in field_name.lower():
                    return ("cycleTimestamps", 2)
                elif field_name.endswith("Id") or field_name.endswith("Ids"):
                    return ("cycleReferences", 3)
                elif isinstance(sample_cycle.get(field_name), dict):
                    return ("cycleDetails", 4)
                elif isinstance(sample_cycle.get(field_name), list):
                    return ("cycleArrays", 5)
                else:
                    return ("cycleAttributes", 6)
            
            group_sort_counter = {}  # Track sort order within each group
            entity_sort_counter = {}  # Track sort order for each entity (Jira pattern: one row per entity)
            
            # SPECTRA-GRADE: Group fields by entity+structureType (one row per entity+structureType)
            # Entity is the canonical SOURCE entity name (e.g., "cycle", "release", "requirement")
            # NOT the target field name - entity must be unique per row
            entity_fields = {}  # (entity, structureType) -> {rawField: [], targetField: [], dataType: [], fieldIds: [], ...}
            
            # Business process mapping (from dimensional model design)
            business_processes = {
                "execution": {
                    "factTableName": "factExecution",
                    "factGrain": "one row per testcase-cycle execution",
                    "isBusinessActivity": True
                },
                "cycle": {
                    "factTableName": "",
                    "factGrain": "",
                    "isBusinessActivity": False
                },
                "project": {
                    "factTableName": "",
                    "factGrain": "",
                    "isBusinessActivity": False
                },
                "release": {
                    "factTableName": "",
                    "factGrain": "",
                    "isBusinessActivity": False
                },
                "requirement": {
                    "factTableName": "factRequirementCoverage",
                    "factGrain": "one row per testcase-requirement allocation",
                    "isBusinessActivity": True
                }
            }
            
            process_info = business_processes.get(source_entity, {
                "factTableName": "",
                "factGrain": "",
                "isBusinessActivity": False
            })
            
            for field_name, field_value in sample_cycle.items():
                # Determine structure type (SPECTRA: scalar | record | array)
                if isinstance(field_value, list):
                    structure_type = "array"
                    is_array = True
                elif isinstance(field_value, dict):
                    structure_type = "record"  # SPECTRA uses "record" not "object"
                    is_array = False
                else:
                    structure_type = "scalar"
                    is_array = False
                
                # Get group
                group, group_base_order = determine_group(field_name)
                if group not in group_sort_counter:
                    group_sort_counter[group] = 0
                group_sort_counter[group] += 1
                group_sort_order = group_base_order * 100 + group_sort_counter[group]
                
                # SPECTRA-GRADE: Entity is the canonical SOURCE entity name (e.g., "cycle")
                entity = source_entity  # "cycle", "release", "requirement", etc.
                key = (entity, structure_type)
                
                # Initialize entity_fields dict for this (entity, structureType) combination
                if key not in entity_fields:
                    entity_fields[key] = {
                        "rawField": [],
                        "targetField": [],
                        "dataType": [],
                        "fieldIds": [],
                        "isInFactIssue": [],
                        "keyField": [],
                        "descriptions": [],
                        "isRequired": [],
                        "isNullable": [],
                        "group": group,
                        "groupSortOrder": group_sort_order
                    }
                
                # SPECTRA-GRADE: Build schema based on structure type
                if structure_type == "scalar":
                    # Scalar field: id → cycleId, name → cycleName
                    target_name = generate_target_name(field_name)
                    data_type = infer_spectra_type(field_value)
                    
                    # Key fields (id, key, name) and identifiers go in fact table
                    is_key_field = field_name in ["id", "key", "name"] or field_name.endswith("Id")
                    
                    # Only assign to fact table if:
                    # 1. It's a business activity (not just an entity)
                    # 2. It's a key field
                    # 3. It's a scalar (arrays go to dimensions/bridges)
                    is_in_fact = (process_info["isBusinessActivity"] and 
                                 is_key_field and 
                                 structure_type == "scalar")
                    
                    # Add to entity_fields dict (grouped by entity+structureType)
                    entity_fields[key]["rawField"].append(field_name)
                    entity_fields[key]["targetField"].append(target_name)
                    entity_fields[key]["dataType"].append(data_type)
                    entity_fields[key]["fieldIds"].append(field_name)
                    entity_fields[key]["isInFactIssue"].append(is_in_fact)
                    entity_fields[key]["keyField"].append(is_key_field)
                    entity_fields[key]["descriptions"].append(f"{entity}.{field_name}")
                    entity_fields[key]["isRequired"].append(field_value is not None)
                    entity_fields[key]["isNullable"].append(field_value is None)
                
                elif structure_type == "record":
                    # Nested object: extract properties (e.g., cyclePhases → cyclePhaseId, cyclePhase)
                    properties = list(field_value.keys())
                    raw_fields = [f"{field_name}.{prop}" for prop in properties]  # Full path: "cyclePhases.id"
                    target_fields = [generate_target_name(field_name, prop) for prop in properties]
                    data_types = [infer_spectra_type(field_value[prop]) for prop in properties]
                    
                    # Add to entity_fields dict (grouped by entity+structureType)
                    entity_fields[key]["rawField"].extend(raw_fields)
                    entity_fields[key]["targetField"].extend(target_fields)
                    entity_fields[key]["dataType"].extend(data_types)
                    entity_fields[key]["fieldIds"].append(field_name)  # Main fieldId
                    entity_fields[key]["isInFactIssue"].extend([False] * len(properties))  # Records don't go in fact table
                    entity_fields[key]["keyField"].extend([prop.endswith("Id") for prop in properties])
                    entity_fields[key]["descriptions"].append(f"{entity}.{field_name} (nested object)")
                    entity_fields[key]["isRequired"].append(False)  # Objects usually optional
                    entity_fields[key]["isNullable"].append(True)
                
                elif structure_type == "array":
                    # Array: determine if objects or scalars
                    if len(field_value) > 0:
                        first_element = field_value[0]
                        
                        if isinstance(first_element, dict):
                            # Array of objects: extract properties from each element
                            properties = list(first_element.keys())
                            raw_fields = [f"{field_name}[].{prop}" for prop in properties]  # Full path: "requirements[].id"
                            
                            # Generate target fields with explicit naming
                            target_fields = [generate_target_name(field_name, prop, is_array=True) for prop in properties]
                            data_types = [f"array<{infer_spectra_type(first_element[prop])}>" for prop in properties]
                            
                            # Add to entity_fields dict (grouped by entity+structureType)
                            entity_fields[key]["rawField"].extend(raw_fields)
                            entity_fields[key]["targetField"].extend(target_fields)
                            entity_fields[key]["dataType"].extend(data_types)
                            entity_fields[key]["fieldIds"].append(field_name)
                            entity_fields[key]["isInFactIssue"].extend([False] * len(properties))  # Arrays don't go in fact table
                            entity_fields[key]["keyField"].extend([prop.endswith("Id") for prop in properties])
                            entity_fields[key]["descriptions"].append(f"{entity}.{field_name} (array of objects)")
                            entity_fields[key]["isRequired"].append(False)
                            entity_fields[key]["isNullable"].append(True)
                        else:
                            # Array of scalars: labels → label
                            element_type = infer_spectra_type(first_element)
                            
                            # Add to entity_fields dict (grouped by entity+structureType)
                            entity_fields[key]["rawField"].append(field_name)
                            entity_fields[key]["targetField"].append(singularize(field_name))
                            entity_fields[key]["dataType"].append(f"array<{element_type}>")
                            entity_fields[key]["fieldIds"].append(field_name)
                            entity_fields[key]["isInFactIssue"].append(False)  # Arrays don't go in fact table
                            entity_fields[key]["keyField"].append(False)  # Array of scalars not key fields
                            entity_fields[key]["descriptions"].append(f"{entity}.{field_name} (array of {element_type})")
                            entity_fields[key]["isRequired"].append(False)
                            entity_fields[key]["isNullable"].append(True)
                    else:
                        # Empty array - can't infer structure
                        entity_fields[key]["rawField"].append(field_name)
                        entity_fields[key]["targetField"].append(singularize(field_name))
                        entity_fields[key]["dataType"].append("array<unknown>")
                        entity_fields[key]["fieldIds"].append(field_name)
                        entity_fields[key]["isInFactIssue"].append(False)
                        entity_fields[key]["keyField"].append(False)
                        entity_fields[key]["descriptions"].append(f"{entity}.{field_name} (empty array - structure unknown)")
                        entity_fields[key]["isRequired"].append(False)
                        entity_fields[key]["isNullable"].append(True)
            
            # SPECTRA-GRADE: Create schema rows - one per (entity, structureType) combination
            for (entity, structure_type), fields in entity_fields.items():
                # Get entitySortOrder
                if entity not in entity_sort_counter:
                    entity_sort_counter[entity] = len(entity_sort_counter)
                entity_sort_order = entity_sort_counter[entity]
                
                # Determine fact table info (from first field if any are in fact table)
                has_fact_fields = any(fields["isInFactIssue"])
                fact_table_name = process_info["factTableName"] if has_fact_fields else ""
                fact_grain = process_info["factGrain"] if has_fact_fields else ""
                
                # Determine dimension/bridge names
                dimension_name = f"dim{entity.capitalize()}" if structure_type in ["record", "array"] else ""
                bridge_name = f"bridge{entity.capitalize()}" if structure_type == "array" else ""
                
                # Create schema row
                schema_data.append({
                    "entity": entity,  # CANONICAL SOURCE ENTITY NAME (e.g., "cycle")
                    "entitySortOrder": entity_sort_order,
                    "fieldId": fields["fieldIds"][0] if fields["fieldIds"] else "",  # Primary fieldId
                    "structureType": structure_type,
                    "rawField": fields["rawField"],  # Array of raw field paths
                    "targetField": fields["targetField"],  # Array of target field names
                    "dataType": fields["dataType"],  # Array of data types
                    "isRequired": any(fields["isRequired"]),
                    "isNullable": all(fields["isNullable"]),
                    "description": "; ".join(fields["descriptions"]),  # Combined description
                    "sourceEndpoint": f"/flex/services/rest/latest/{entity}",  # Default Zephyr API path
                    "apiStatus": "discovered",
                    "group": fields["group"],
                    "groupSortOrder": fields["groupSortOrder"],
                    "notes": "Built from sample data in discovery mode",
                    "dimensionName": dimension_name,
                    "bridgeName": bridge_name,
                    "isInFactIssue": fields["isInFactIssue"],  # Array (one per targetField)
                    "keyField": fields["keyField"],  # Array (one per targetField)
                    "factTableName": fact_table_name,
                    "factGrain": fact_grain,
                })
            
            log.info(f"  == Built {len(schema_data)} schema rows from sample cycle data")
            
            # Also build project schema if project data is available
            if "projects" in sample_data and sample_data["projects"]:
                log.info("  >> Building project schema from sample project data...")
                sample_project = sample_data["projects"][0]
                project_source_entity = "project"
                
                # Build project schema using same logic as cycle
                project_entity_fields = {}
                
                for field_name, field_value in sample_project.items():
                    # Determine structure type
                    if isinstance(field_value, list):
                        structure_type = "array"
                    elif isinstance(field_value, dict):
                        structure_type = "record"
                    else:
                        structure_type = "scalar"
                    
                    entity = project_source_entity
                    key = (entity, structure_type)
                    
                    # Initialize if needed
                    if key not in project_entity_fields:
                        project_entity_fields[key] = {
                            "rawField": [],
                            "targetField": [],
                            "dataType": [],
                            "fieldIds": [],
                            "isInFactIssue": [],
                            "keyField": [],
                            "descriptions": [],
                            "isRequired": [],
                            "isNullable": [],
                            "group": "projectAttributes",
                            "groupSortOrder": 1
                        }
                    
                    # Add scalar fields
                    if structure_type == "scalar":
                        # Generate target name
                        if field_name == "id":
                            target_name = "projectId"
                        elif field_name == "name":
                            target_name = "projectName"
                        elif field_name in ("projectKey", "key"):
                            target_name = "sourceProjectKey"
                        else:
                            target_name = field_name
                        
                        data_type = infer_spectra_type(field_value)
                        is_key_field = field_name == "id" or field_name.endswith("Id")
                        
                        project_entity_fields[key]["rawField"].append(field_name)
                        project_entity_fields[key]["targetField"].append(target_name)
                        project_entity_fields[key]["dataType"].append(data_type)
                        project_entity_fields[key]["fieldIds"].append(field_name)
                        project_entity_fields[key]["isInFactIssue"].append(False)
                        project_entity_fields[key]["keyField"].append(is_key_field)
                        project_entity_fields[key]["descriptions"].append(f"{entity}.{field_name}")
                        project_entity_fields[key]["isRequired"].append(field_value is not None)
                        project_entity_fields[key]["isNullable"].append(field_value is None)
                
                # Create schema rows for project
                for (entity, structure_type), fields in project_entity_fields.items():
                    if entity not in entity_sort_counter:
                        entity_sort_counter[entity] = len(entity_sort_counter)
                    entity_sort_order = entity_sort_counter[entity]
                    
                    schema_data.append({
                        "entity": entity,
                        "entitySortOrder": entity_sort_order,
                        "fieldId": fields["fieldIds"][0] if fields["fieldIds"] else "",
                        "structureType": structure_type,
                        "rawField": fields["rawField"],
                        "targetField": fields["targetField"],
                        "dataType": fields["dataType"],
                        "isRequired": any(fields["isRequired"]),
                        "isNullable": all(fields["isNullable"]),
                        "description": "; ".join(fields["descriptions"]),
                        "sourceEndpoint": f"/flex/services/rest/latest/{entity}",
                        "apiStatus": "discovered",
                        "group": fields["group"],
                        "groupSortOrder": fields["groupSortOrder"],
                        "notes": "Built from sample data in discovery mode",
                        "dimensionName": "",
                        "bridgeName": "",
                        "isInFactIssue": fields["isInFactIssue"],
                        "keyField": fields["keyField"],
                        "factTableName": "",
                        "factGrain": "",
                    })
                
                log.info(f"  == Built {len([r for r in schema_data if r['entity'] == 'project'])} schema rows from sample project data")
        else:
            log.warning("  !! No cycles found in response - cannot build schema")
            log.warning("  !! schema_data will be empty")
    except Exception as e:
        import traceback
        log.error(f"  !! Failed to fetch/rebuild from samples: {e}")
        log.error(f"  !! Exception type: {type(e).__name__}")
        log.error(f"  !! Traceback: {traceback.format_exc()}")
        raise
    
    # Write samples to Tables/sample/ (in hierarchical order: project → releases → cycles → testcases)
    log.info("  >> Writing sample data to Tables/sample/...")
    
    # SPECTRA-GRADE: Write in hierarchical order to maintain referential integrity
    entity_write_order = ["projects", "releases", "cycles", "testcases"]

    spark.sql("CREATE DATABASE IF NOT EXISTS sample")
    
    for entity_name in entity_write_order:
        if entity_name not in sample_data:
            continue
        entities = sample_data[entity_name]
        if not entities:
            continue
        
        # #region agent log
        import json
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "H1,H2,H3,H4",
            "location": f"prepareZephyr.Notebook:877",
            "message": f"Before createDataFrame for {entity_name}",
            "data": {
                "entity_name": entity_name,
                "entity_count": len(entities),
                "first_entity_keys": list(entities[0].keys()) if entities else [],
                "first_entity_sample": {k: (type(v).__name__, str(v)[:100] if not isinstance(v, (dict, list)) else f"{type(v).__name__}({len(v) if isinstance(v, (list, dict)) else 'N/A'})") for k, v in list(entities[0].items())[:10]} if entities else {}
            },
            "timestamp": int(time.time() * 1000)
        }
        log.info(f"  DEBUG INSTRUMENT: {json.dumps(log_entry)}")
        # #endregion
        
        try:
            # SPECTRA-GRADE: Flatten nested structures for PySpark DataFrame creation
            # PySpark can't infer schema for nested structures (lists/dicts), so we flatten them
            flattened_entities = []
            for entity in entities:
                flattened_entity = {}
                for key, value in entity.items():
                    if isinstance(value, (dict, list)):
                        # Convert nested structures to JSON strings for sample tables
                        import json
                        flattened_entity[key] = json.dumps(value) if value else None
                    else:
                        # Keep scalar values as-is
                        flattened_entity[key] = value
                flattened_entities.append(flattened_entity)
            
            # #region agent log
            log_entry = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H1",
                "location": f"prepareZephyr.Notebook:920",
                "message": f"Flattened {entity_name} for DataFrame creation",
                "data": {
                    "entity_name": entity_name,
                    "original_count": len(entities),
                    "flattened_count": len(flattened_entities),
                    "nested_fields_flattened": [k for k, v in entities[0].items() if isinstance(v, (dict, list))] if entities else []
                },
                "timestamp": int(time.time() * 1000)
            }
            log.info(f"  DEBUG INSTRUMENT: {json.dumps(log_entry)}")
            # #endregion
            
            try:
                df_sample = spark.createDataFrame(flattened_entities)
            except Exception as e:
                if "CANNOT_DETERMINE_TYPE" not in str(e):
                    raise
                raw_rows = [{"raw_json": json.dumps(entity)} for entity in entities]
                df_sample = spark.createDataFrame(raw_rows)
            
            # #region agent log
            log_entry = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H1,H2,H3,H4",
                "location": f"prepareZephyr.Notebook:910",
                "message": f"Successfully created DataFrame for {entity_name}",
                "data": {
                    "entity_name": entity_name,
                    "row_count": df_sample.count(),
                    "schema_fields": [str(f) for f in df_sample.schema.fields[:5]]
                },
                "timestamp": int(time.time() * 1000)
            }
            log.info(f"  DEBUG INSTRUMENT: {json.dumps(log_entry)}")
            # #endregion
            
            sample_path = f"Tables/sample/{entity_name}"
            df_sample.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(sample_path)
            spark.sql(f"DROP TABLE IF EXISTS sample.{entity_name}")
            spark.sql(f"CREATE TABLE sample.{entity_name} USING DELTA LOCATION '{sample_path}'")
            log.info(f"  OK Created sample.{entity_name} ({df_sample.count()} rows)")
        except Exception as e:
            # #region agent log
            import traceback
            log_entry = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H1,H2,H3,H4",
                "location": f"prepareZephyr.Notebook:930",
                "message": f"Error creating DataFrame for {entity_name}",
                "data": {
                    "entity_name": entity_name,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "entity_structure": {k: type(v).__name__ for k, v in entities[0].items()} if entities and isinstance(entities[0], dict) else {},
                    "traceback": traceback.format_exc()[:500]
                },
                "timestamp": int(time.time() * 1000)
            }
            log.error(f"  DEBUG INSTRUMENT: {json.dumps(log_entry)}")
            # #endregion
            log.error(f"  !! Failed to create sample.{entity_name}: {e}")
            continue
    
    # SPECTRA-GRADE: Automated intelligence update with quality gates
    log.info("=" * 80)
    log.info("SPECTRA-GRADE: Automated Intelligence Update with Quality Gates")
    log.info("=" * 80)
    
    try:
        import json
        from datetime import datetime
        
        # QUALITY GATE 1: Validate rebuilt schema
        log.info("  >> Quality Gate 1: Validating rebuilt schema...")
        
        # Check minimum requirements
        if len(schema_data) == 0:
            raise ValueError("Rebuilt schema is empty - quality gate FAILED")
        
        # Check for required fields
        required_fields_per_entity = {
            "cycle": ["cycleId", "cycleName", "projectId"],
            "project": ["projectId", "projectName"]
        }
        
        # Collect all targetField values per entity from schema_data
        entity_target_fields = {}
        for field in schema_data:
            entity = field["entity"]
            if entity not in entity_target_fields:
                entity_target_fields[entity] = set()
            # targetField is a list/array, add all values to the set
            target_fields = field.get("targetField", [])
            if isinstance(target_fields, list):
                entity_target_fields[entity].update(target_fields)
            else:
                # Handle case where targetField might be a single string
                entity_target_fields[entity].add(target_fields)
        
        validation_errors = []
        for entity, required_fields in required_fields_per_entity.items():
            if entity in entity_target_fields:
                # Check if required fields are present in targetField arrays
                missing = set(required_fields) - entity_target_fields[entity]
                if missing:
                    validation_errors.append(f"{entity} missing required fields: {missing}")
            else:
                # Entity not found in schema_data at all
                validation_errors.append(f"{entity} not found in schema - missing all required fields: {required_fields}")
        
        if validation_errors:
            log.error(f"  !! Quality Gate FAILED: {validation_errors}")
            raise ValueError(f"Schema validation failed: {validation_errors}")
        
        log.info(f"  OK Quality Gate 1 PASSED: {len(schema_data)} fields, all required fields present")
        
        # QUALITY GATE 2: Compare with existing schema (if available in Fabric tables)
        log.info("  >> Quality Gate 2: Comparing with existing schema...")
        
        existing_field_count = 0
        try:
            # Try to read from Fabric tables first
            df_existing = spark.table("prepare.schema")
            existing_field_count = df_existing.count()
            if existing_field_count > 0:
                new_field_count = len(schema_data)
                if new_field_count < existing_field_count * 0.5:
                    log.warning(f"  !! WARNING: Rebuilt schema has {new_field_count} fields vs {existing_field_count} existing")
                    log.warning("     This might indicate incomplete rebuild - review manually")
                else:
                    log.info(f"  OK Field count reasonable: {new_field_count} rebuilt vs {existing_field_count} existing")
        except:
            log.info("  OK No existing schema to compare (first rebuild)")
        
        # QUALITY GATE 3: Structure validation
        log.info("  >> Quality Gate 3: Validating structure types...")
        
        structure_types = set(f["structureType"] for f in schema_data)
        valid_types = {"scalar", "array<object>", "array<string>", "array<number>", "array<unknown>", "object"}
        invalid_types = structure_types - valid_types
        
        if invalid_types:
            log.warning(f"  !! WARNING: Unexpected structure types: {invalid_types}")
        else:
            log.info(f"  OK All structure types valid: {structure_types}")
        
        # All quality gates passed - proceed with schema update
        log.info("=" * 80)
        log.info("  OK ALL QUALITY GATES PASSED - Proceeding with schema rebuild")
        log.info("=" * 80)
        
        # Convert schema_data to intelligence format
        discovered_schema = {
            "rebuilt_at": datetime.utcnow().isoformat() + "Z",
            "source": "rebuild=True mode (automated)",
            "quality_gates": "PASSED",
            "field_count": len(schema_data),
            "entities": {}
        }
        
        # Group fields by entity (intelligence format)
        for field in schema_data:
            entity = field["entity"]
            if entity not in discovered_schema["entities"]:
                discovered_schema["entities"][entity] = {
                    "endpoint": field.get("sourceEndpoint", ""),
                    "field_count": 0,
                    "fields": []
                }
            discovered_schema["entities"][entity]["fields"].append(field)
            discovered_schema["entities"][entity]["field_count"] += 1
        
        # Export rebuilt schema (for Git sync)
        timestamp = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
        discovered_path = f"Files/intelligence/rebuilt-schema-{timestamp}.json"
        discovered_json = json.dumps(discovered_schema, indent=2)
        
        # Write as file (Git will sync this)
        spark.sparkContext.parallelize([discovered_json]).saveAsTextFile(discovered_path)
        
        log.info(f"  OK Exported rebuilt schema: {discovered_path}")
        
        # SPECTRA-GRADE: Generate complete intelligence Python code (ready to append)
        log.info("  >> Generating complete intelligence Python code (SPECTRA-grade)...")
        
        python_code_lines = []
        python_code_lines.append("# " + "=" * 78)
        python_code_lines.append("# ZEPHYR API INTELLIGENCE (REBUILT)")
        python_code_lines.append(f"# Auto-generated from rebuild=True mode at {datetime.utcnow().isoformat()}Z")
        python_code_lines.append("# Source: Sample data analysis (perfect schema from reality)")
        python_code_lines.append("# Quality Gates: PASSED")
        python_code_lines.append("# " + "=" * 78)
        python_code_lines.append("")
        python_code_lines.append("class ZephyrIntelligence:")
        python_code_lines.append('    """Zephyr API intelligence - rebuilt from sample data."""')
        python_code_lines.append("")
        python_code_lines.append("    # Complete entity schemas (rebuilt from samples)")
        python_code_lines.append("    ENTITIES = {")
        
        # Generate ENTITIES dict
        for entity_name, entity_data in discovered_schema["entities"].items():
            python_code_lines.append(f'        "{entity_name}": {{')
            python_code_lines.append(f'            "endpoint": "{entity_data["endpoint"]}",')
            python_code_lines.append(f'            "field_count": {entity_data["field_count"]},')
            python_code_lines.append('            "fields": [')
            
            # Generate fields array
            for field in entity_data["fields"]:
                field_dict = {
                    "entity": field["entity"],
                    "entitySortOrder": field.get("entitySortOrder", 0),  # Jira pattern: ensures one row per entity
                    "fieldId": field["fieldId"],
                    "structureType": field["structureType"],
                    "rawField": field.get("rawField", []),
                    "targetField": field.get("targetField", []),
                    "dataType": field.get("dataType", []),
                    "isNullable": field.get("isNullable", True),
                    "description": field.get("description", ""),
                    "apiStatus": field.get("apiStatus", "discovered"),
                    "group": field.get("group", "attributes"),
                    "groupSortOrder": field.get("groupSortOrder", 99),
                    "notes": field.get("notes", ""),
                    "dimensionName": field.get("dimensionName", ""),
                    "bridgeName": field.get("bridgeName", ""),
                    "isInFactIssue": field.get("isInFactIssue", [False]),  # Fact table flag
                    "keyField": field.get("keyField", [False]),  # Key field flag
                    "factTableName": field.get("factTableName", ""),  # Which fact table
                    "factGrain": field.get("factGrain", ""),  # Fact table grain
                }
                
                # Convert to Python dict string (handle None, True, False)
                field_str = str(field_dict).replace("'", '"').replace("None", "None").replace("True", "True").replace("False", "False")
                python_code_lines.append(f"                {field_str},")
            
            python_code_lines.append('            ]')
            python_code_lines.append('        },')
        
        python_code_lines.append("    }")
        python_code_lines.append("")
        python_code_lines.append("    # Dependencies (preserve existing)")
        python_code_lines.append("    DEPENDENCIES = {}  # TODO: Discover from sample relationships")
        python_code_lines.append("")
        python_code_lines.append("    # Constraints (preserve existing)")
        python_code_lines.append("    CONSTRAINTS = {}  # TODO: Discover from API errors")
        python_code_lines.append("")
        python_code_lines.append("    @classmethod")
        python_code_lines.append("    def get_entity_fields(cls, entity: str):")
        python_code_lines.append('        """Get all fields for an entity."""')
        python_code_lines.append("        return cls.ENTITIES.get(entity, {}).get('fields', [])")
        python_code_lines.append("")
        python_code_lines.append("    @classmethod")
        python_code_lines.append("    def get_entity_schema(cls, entity: str):")
        python_code_lines.append('        """Get complete entity schema."""')
        python_code_lines.append("        return cls.ENTITIES.get(entity, {})")
        python_code_lines.append("")
        python_code_lines.append("    @classmethod")
        python_code_lines.append("    def get_all_constraints(cls):")
        python_code_lines.append('        """Get all constraints."""')
        python_code_lines.append("        return cls.CONSTRAINTS")
        python_code_lines.append("")
        
        # Write complete Python code to Files/
        python_code = "\n".join(python_code_lines)
        python_path = f"Files/intelligence/rebuilt-intelligence-{timestamp}.py"
        spark.sparkContext.parallelize([python_code]).saveAsTextFile(python_path)
        
        log.info(f"  OK Generated complete intelligence Python: {python_path}")
        log.info(f"     Ready to append to spectraSDK.Notebook (one command)")
        
        # SPECTRA-GRADE: Automated next steps
        log.info("=" * 80)
        log.info("SPECTRA-GRADE: Schema Rebuild Complete")
        log.info("=" * 80)
        log.info("  >> Quality Gates: PASSED")
        log.info(f"  >> Rebuilt: {len(schema_data)} fields across {len(discovered_schema['entities'])} entities")
        log.info("  >> Generated: Complete Python code (ready to append)")
        log.info("")
        log.info("  SPECTRA-GRADE NEXT STEP (One Command - Fully Automated):")
        log.info(f"    python scripts/append_discovered_intelligence.py {timestamp} --auto-commit")
        log.info("")
        log.info("  This will (FULLY AUTOMATED):")
        log.info("    1. Load: Files/intelligence/rebuilt-intelligence-{timestamp}.py")
        log.info("    2. Merge: With existing intelligence (preserve dependencies/constraints)")
        log.info("    3. Append: To spectraSDK.Notebook")
        log.info("    4. Commit: Auto-commit to Git (if --auto-commit flag)")
        log.info("    5. Push: Auto-push to Git (if --auto-commit flag)")
        log.info("    6. Sync: Fabric auto-syncs updated SDK")
        log.info("")
        log.info("  >> SELF-UPDATING: Quality gates passed → Auto-update intelligence")
        log.info("  >> Zero manual steps (if --auto-commit used)")
        log.info("=" * 80)
        
    except Exception as e:
        log.error(f"  !! Schema rebuild FAILED: {e}")
        log.error("  >> Quality gates failed - rebuilt schema NOT exported")
        log.error("  >> Review prepare.schema table manually")
        log.error("  >> Fix rebuild issues and re-run with rebuild=True")
        raise
    
else:
    # PATH 2: Load existing schema from Fabric tables (normal operation)
    log.info("Loading from prepare.schema table (existing schema)...")
    
    # SPECTRA-GRADE: Read from Fabric tables (prepare.schema, prepare.dependencies, prepare.constraints)
    # Try to read from tables first, fallback to SDK if tables don't exist
    schema_data = []
    dependencies_data = []
    constraints_data = []

    loaded_schema = False
    try:
        df_schema = spark.table("prepare.schema")
        loaded_schema = True
        log.info("  OK Loaded from Fabric table prepare.schema")
        for row in df_schema.collect():
            schema_data.append({
                "entity": row["entity"],
                "entitySortOrder": row["entitySortOrder"],
                "fieldId": row["fieldId"],
                "structureType": row["structureType"],
                "rawField": row["rawField"],
                "targetField": row["targetField"],
                "dataType": row["dataType"],
                "isRequired": row["isRequired"],
                "isNullable": row["isNullable"],
                "description": row["description"],
                "sourceEndpoint": row["sourceEndpoint"],
                "apiStatus": row["apiStatus"],
                "group": row["group"],
                "groupSortOrder": row["groupSortOrder"],
                "notes": row["notes"],
                "dimensionName": row["dimensionName"],
                "bridgeName": row["bridgeName"],
                "isInFactIssue": row["isInFactIssue"],
                "keyField": row["keyField"],
                "factTableName": row["factTableName"],
                "factGrain": row["factGrain"],
            })
    except Exception as e:
        log.warning(f"  !! Could not load prepare.schema from Fabric tables: {e}")

    if loaded_schema:
        try:
            df_dependencies = spark.table("prepare.dependencies")
            log.info("  OK Loaded from Fabric table prepare.dependencies")
            for row in df_dependencies.collect():
                dependencies_data.append({
                    "entity": row["entity"],
                    "dependsOn": row["dependsOn"],
                    "requiredBy": row["requiredBy"],
                    "dependencyCount": row["dependencyCount"],
                    "dependentCount": row["dependentCount"],
                    "isIndependent": row["isIndependent"],
                    "isLeaf": row["isLeaf"]
                })
        except Exception as e:
            log.warning(f"  !! Could not load prepare.dependencies from Fabric tables: {e}")

        try:
            df_constraints = spark.table("prepare.constraints")
            log.info("  OK Loaded from Fabric table prepare.constraints")
            for row in df_constraints.collect():
                constraints_data.append({
                    "constraintId": row["constraintId"],
                    "constraintType": row["constraintType"],
                    "entity": row["entity"],
                    "endpoint": row["endpoint"],
                    "severity": row["severity"],
                    "issue": row["issue"],
                    "impact": row["impact"],
                    "workaround": row["workaround"],
                    "workaroundStatus": row["workaroundStatus"]
                })
        except Exception as e:
            log.warning(f"  !! Could not load prepare.constraints from Fabric tables: {e}")

        if not dependencies_data:
            try:
                if "ZephyrIntelligence" in globals() and hasattr(ZephyrIntelligence, "DEPENDENCIES"):
                    for entity, deps_info in ZephyrIntelligence.DEPENDENCIES.items():
                        depends_on = deps_info.get("depends_on", [])
                        required_by = deps_info.get("required_by", [])
                        dependencies_data.append({
                            "entity": entity,
                            "dependsOn": depends_on,
                            "requiredBy": required_by,
                            "dependencyCount": len(depends_on),
                            "dependentCount": len(required_by),
                            "isIndependent": len(depends_on) == 0,
                            "isLeaf": len(required_by) == 0
                        })
                    log.info("  OK Filled prepare.dependencies from SDK intelligence")
            except Exception as e:
                log.warning(f"  !! Could not fill prepare.dependencies from SDK intelligence: {e}")

        if not constraints_data:
            try:
                if "ZephyrIntelligence" in globals() and hasattr(ZephyrIntelligence, "get_all_constraints"):
                    constraints = ZephyrIntelligence.get_all_constraints() or {}
                    for blocker in constraints.get("blockers", []):
                        constraints_data.append({
                            "constraintId": blocker.get("id", "unknown"),
                            "constraintType": "blocker",
                            "entity": blocker.get("entity", "unknown"),
                            "endpoint": blocker.get("endpoint", ""),
                            "severity": blocker.get("severity", "unknown"),
                            "issue": blocker.get("issue", ""),
                            "impact": blocker.get("impact", ""),
                            "workaround": str(blocker.get("workaround", {})),
                            "workaroundStatus": blocker.get("workaround", {}).get("status", "unknown")
                        })
                    for bug in constraints.get("bugs", []):
                        constraints_data.append({
                            "constraintId": bug.get("id", "unknown"),
                            "constraintType": "bug",
                            "entity": bug.get("entity", "unknown"),
                            "endpoint": bug.get("endpoint", ""),
                            "severity": bug.get("severity", "unknown"),
                            "issue": bug.get("issue", ""),
                            "impact": bug.get("impact", ""),
                            "workaround": str(bug.get("workaround", {})),
                            "workaroundStatus": bug.get("workaround", {}).get("status", "unknown")
                        })
                    for quirk in constraints.get("quirks", []):
                        constraints_data.append({
                            "constraintId": quirk.get("id", "unknown"),
                            "constraintType": "quirk",
                            "entity": quirk.get("entity", "unknown"),
                            "endpoint": "",
                            "severity": quirk.get("severity", "low"),
                            "issue": quirk.get("issue", ""),
                            "impact": quirk.get("impact", ""),
                            "workaround": str(quirk.get("workaround", {})),
                            "workaroundStatus": quirk.get("workaround", {}).get("status", "unknown")
                        })
                    log.info("  OK Filled prepare.constraints from SDK intelligence")
            except Exception as e:
                log.warning(f"  !! Could not fill prepare.constraints from SDK intelligence: {e}")

    if not loaded_schema:
        log.info("  >> Falling back to SDK intelligence...")
        
        # FALLBACK: Load from SDK intelligence
        # SPECTRA-GRADE: Group fields by entity+structureType (one row per entity+structureType)
        # Entity is the canonical SOURCE entity name (e.g., "cycle", "release", "requirement")
        # NOT the target field name - entity must be unique per row
        entity_fields = {}  # (entity, structureType) -> {rawField: [], targetField: [], dataType: [], ...}
        entity_sort_counter = {}  # Track sort order for each entity
        
        # SPECTRA-GRADE: Handle both SCHEMAS (intelligence.py) and ENTITIES (SDK) formats
        # SCHEMAS: JSON schema format {entity: {schema: {properties: {...}}, endpoint: "...", ...}}
        # ENTITIES: Fields array format {entity: {fields: [...], endpoint: "...", ...}}
        if hasattr(ZephyrIntelligence, 'SCHEMAS'):
            # Use SCHEMAS format (intelligence.py)
            schemas_dict = ZephyrIntelligence.SCHEMAS
            use_schemas_format = True
        elif hasattr(ZephyrIntelligence, 'ENTITIES'):
            # Use ENTITIES format (SDK)
            schemas_dict = ZephyrIntelligence.ENTITIES
            use_schemas_format = False
        else:
            raise AttributeError("ZephyrIntelligence missing both SCHEMAS and ENTITIES")
        
        for entity_name, entity_info in schemas_dict.items():
            if entity_info is None:
                continue
            # entity_name is the canonical SOURCE entity name (e.g., "cycle", "release", "requirement")
            entity = entity_name  # Use canonical source entity name
            
            # Get entitySortOrder
            if entity not in entity_sort_counter:
                entity_sort_counter[entity] = len(entity_sort_counter)
            entity_sort_order = entity_sort_counter[entity]
            
            if use_schemas_format:
                # Parse JSON schema structure: entity_info["schema"]["properties"]
                schema_info = entity_info.get("schema") or {}
                if not isinstance(schema_info, dict):
                    schema_info = {}
                properties = schema_info.get("properties", {})
                required_fields = schema_info.get("required", [])
            else:
                # Parse ENTITIES format: entity_info["fields"] array
                fields = entity_info.get("fields", [])
                # Convert ENTITIES format to properties-like structure for processing
                properties = {}
                required_fields = []
                for field in fields:
                    field_id = field.get("fieldId", "")
                    if field_id:
                        properties[field_id] = {
                            "type": field.get("dataType", ["text"])[0] if isinstance(field.get("dataType"), list) else field.get("dataType", "text")
                        }
                        if field.get("isRequired", False):
                            required_fields.append(field_id)
            
            # Group properties by structure type (scalar, array, object)
            scalar_fields = []
            array_fields = []
            object_fields = []
            
            for prop_name, prop_info in properties.items():
                prop_type = prop_info.get("type", "string")
                if prop_type == "array":
                    array_fields.append(prop_name)
                elif prop_type == "object":
                    object_fields.append(prop_name)
                else:
                    scalar_fields.append(prop_name)
            
            # Process scalar fields (one row per entity+scalar)
            if scalar_fields:
                key = (entity, "scalar")
                if key not in entity_fields:
                    entity_fields[key] = {
                        "rawField": [],
                        "targetField": [],
                        "dataType": [],
                        "fieldIds": [],
                        "isInFactIssue": [],
                        "keyField": [],
                        "descriptions": [],
                        "isRequired": [],
                        "isNullable": [],
                        "group": "attributes",
                        "groupSortOrder": 1,
                        "sourceEndpoint": entity_info.get("endpoint", ""),
                        "dimensionName": "",
                        "bridgeName": "",
                        "notes": entity_info.get("notes", ""),
                        "apiStatus": entity_info.get("status", "unknown"),
                        "factTableName": "",
                        "factGrain": "",
                    }
                
                for prop_name in scalar_fields:
                    prop_info = properties[prop_name]
                    prop_type = prop_info.get("type", "string")
                    
                    # Map JSON schema types to SPECTRA types
                    type_mapping = {
                        "integer": "integer",
                        "number": "decimal",
                        "string": "text",
                        "boolean": "boolean"
                    }
                    spectra_type = type_mapping.get(prop_type, "text")
                    
                    entity_fields[key]["rawField"].append(prop_name)
                    entity_fields[key]["targetField"].append(prop_name)
                    entity_fields[key]["dataType"].append(spectra_type)
                    entity_fields[key]["fieldIds"].append(prop_name)
                    entity_fields[key]["isInFactIssue"].append(False)  # Scalars not in fact by default
                    entity_fields[key]["keyField"].append(prop_name.endswith("Id") or prop_name == "id")
                    entity_fields[key]["descriptions"].append(f"{entity}.{prop_name}")
                    entity_fields[key]["isRequired"].append(prop_name in required_fields)
                    entity_fields[key]["isNullable"].append(prop_name not in required_fields)
            
            # Process array fields (one row per entity+array)
            for array_field in array_fields:
                key = (entity, "array")
                if key not in entity_fields:
                    entity_fields[key] = {
                        "rawField": [],
                        "targetField": [],
                        "dataType": [],
                        "fieldIds": [],
                        "isInFactIssue": [],
                        "keyField": [],
                        "descriptions": [],
                        "isRequired": [],
                        "isNullable": [],
                        "group": "relationships",
                        "groupSortOrder": 2,
                        "sourceEndpoint": entity_info.get("endpoint", ""),
                        "dimensionName": f"dim{array_field.capitalize()}" if array_field else "",
                        "bridgeName": f"bridge{array_field.capitalize()}" if array_field else "",
                        "notes": entity_info.get("notes", ""),
                        "apiStatus": entity_info.get("status", "unknown"),
                        "factTableName": "",
                        "factGrain": "",
                    }
                
                entity_fields[key]["rawField"].append(array_field)
                entity_fields[key]["targetField"].append(array_field.rstrip('s') if array_field.endswith('s') else array_field)
                entity_fields[key]["dataType"].append("array<unknown>")  # Can't infer without sample
                entity_fields[key]["fieldIds"].append(array_field)
                entity_fields[key]["isInFactIssue"].append(False)  # Arrays not in fact
                entity_fields[key]["keyField"].append(False)
                entity_fields[key]["descriptions"].append(f"{entity}.{array_field} (array)")
                entity_fields[key]["isRequired"].append(array_field in required_fields)
                entity_fields[key]["isNullable"].append(array_field not in required_fields)
            
            # Skip object fields for now (would need sample data to parse structure)
            # Objects will be handled when rebuild=True fetches samples
            
            # If using ENTITIES format (SDK), process fields directly
            if not use_schemas_format:
                # ENTITIES format: entity_info["fields"] is already an array of field definitions
                fields = entity_info.get("fields", [])
                for field_def in fields:
                    structure_type = field_def.get("structureType", "scalar")
                    key = (entity, structure_type)
                    
                    # Initialize entity_fields dict for this (entity, structureType) combination
                    if key not in entity_fields:
                        entity_fields[key] = {
                            "rawField": [],
                            "targetField": [],
                            "dataType": [],
                            "fieldIds": [],
                            "isInFactIssue": [],
                            "keyField": [],
                            "descriptions": [],
                            "isRequired": [],
                            "isNullable": [],
                            "group": field_def.get("group", "attributes"),
                            "groupSortOrder": field_def.get("groupSortOrder", 99),
                            "sourceEndpoint": entity_info.get("endpoint", ""),
                            "dimensionName": field_def.get("dimensionName", ""),
                            "bridgeName": field_def.get("bridgeName", ""),
                            "notes": entity_info.get("notes", ""),
                            "apiStatus": field_def.get("apiStatus", entity_info.get("apiStatus", "unknown")),
                            "factTableName": field_def.get("factTableName", ""),
                            "factGrain": field_def.get("factGrain", ""),
                        }
                    
                    # Add fields to arrays (grouped by entity+structureType)
                    raw_fields = field_def.get("rawField", [])
                    target_fields = field_def.get("targetField", [])
                    data_types = field_def.get("dataType", [])
                    is_in_fact = field_def.get("isInFactIssue", [False])
                    key_fields = field_def.get("keyField", [False])
                    
                    # Ensure arrays are lists (handle single values)
                    if not isinstance(raw_fields, list):
                        raw_fields = [raw_fields] if raw_fields else []
                    if not isinstance(target_fields, list):
                        target_fields = [target_fields] if target_fields else []
                    if not isinstance(data_types, list):
                        data_types = [data_types] if data_types else []
                    if not isinstance(is_in_fact, list):
                        is_in_fact = [is_in_fact] if is_in_fact else [False]
                    if not isinstance(key_fields, list):
                        key_fields = [key_fields] if key_fields else [False]
                    
                    # Align array lengths
                    max_len = max(len(raw_fields), len(target_fields), len(data_types), len(is_in_fact), len(key_fields))
                    if len(raw_fields) < max_len:
                        raw_fields.extend([raw_fields[0] if raw_fields else ""] * (max_len - len(raw_fields)))
                    if len(target_fields) < max_len:
                        target_fields.extend([target_fields[0] if target_fields else ""] * (max_len - len(target_fields)))
                    if len(data_types) < max_len:
                        data_types.extend([data_types[0] if data_types else "text"] * (max_len - len(data_types)))
                    if len(is_in_fact) < max_len:
                        is_in_fact.extend([False] * (max_len - len(is_in_fact)))
                    if len(key_fields) < max_len:
                        key_fields.extend([False] * (max_len - len(key_fields)))
                    
                    # Add to entity_fields dict
                    entity_fields[key]["rawField"].extend(raw_fields)
                    entity_fields[key]["targetField"].extend(target_fields)
                    entity_fields[key]["dataType"].extend(data_types)
                    entity_fields[key]["fieldIds"].append(field_def.get("fieldId", ""))
                    entity_fields[key]["isInFactIssue"].extend(is_in_fact)
                    entity_fields[key]["keyField"].extend(key_fields)
                    
                    # Build description: {entity}.{fieldId}
                    field_id = field_def.get("fieldId", "")
                    desc = field_def.get("description", f"{entity}.{field_id}")
                    entity_fields[key]["descriptions"].append(desc)
                    
                    entity_fields[key]["isRequired"].append(not field_def.get("isNullable", True))
                    entity_fields[key]["isNullable"].append(field_def.get("isNullable", True))
        
        # SPECTRA-GRADE: Create schema rows - one per (entity, structureType) combination
        schema_data = []
        for (entity, structure_type), fields in entity_fields.items():
            # Get entitySortOrder
            entity_sort_order = entity_sort_counter[entity]
            
            # Determine fact table info (from fields or business process mapping)
            has_fact_fields = any(fields["isInFactIssue"])
            
            # Get fact table info from first field that has it, or from business process mapping
            fact_table_name = ""
            fact_grain = ""
            if has_fact_fields:
                # Try to get from fields (if stored in existing intelligence)
                fact_table_name = fields.get("factTableName", "")
                fact_grain = fields.get("factGrain", "")
                
                # If not in fields, derive from business process mapping
                if not fact_table_name:
                    business_processes = {
                        "execution": {"factTableName": "factExecution", "factGrain": "one row per testcase-cycle execution"},
                        "requirement": {"factTableName": "factRequirementCoverage", "factGrain": "one row per testcase-requirement allocation"},
                    }
                    process_info = business_processes.get(entity, {"factTableName": "", "factGrain": ""})
                    fact_table_name = process_info["factTableName"]
                    fact_grain = process_info["factGrain"]
            
            # Determine dimension/bridge names
            dimension_name = fields["dimensionName"] if structure_type in ["record", "array"] else ""
            bridge_name = fields["bridgeName"] if structure_type == "array" else ""
            
            # Create schema row
            schema_data.append({
                "entity": entity,  # CANONICAL SOURCE ENTITY NAME (e.g., "cycle")
                "entitySortOrder": entity_sort_order,
                "fieldId": fields["fieldIds"][0] if fields["fieldIds"] else "",  # Primary fieldId
                "structureType": structure_type,
                "rawField": fields["rawField"],  # Array of raw field paths
                "targetField": fields["targetField"],  # Array of target field names
                "dataType": fields["dataType"],  # Array of data types
                "isRequired": any(fields["isRequired"]),
                "isNullable": all(fields["isNullable"]),
                "description": "; ".join(fields["descriptions"]),  # Combined description
                "sourceEndpoint": fields["sourceEndpoint"],
                "apiStatus": fields["apiStatus"],
                "group": fields["group"],
                "groupSortOrder": fields["groupSortOrder"],
                "notes": fields["notes"],
                "dimensionName": dimension_name,
                "bridgeName": bridge_name,
                "isInFactIssue": fields["isInFactIssue"],  # Array (one per targetField)
                "keyField": fields["keyField"],  # Array (one per targetField)
                "factTableName": fact_table_name,
                "factGrain": fact_grain,
            })
        
        log.info(f"  == Loaded {len(schema_data)} schema rows from {len(ZephyrIntelligence.ENTITIES)} entities (SDK FALLBACK)")
        log.info(f"     Grouped by entity+structureType (one row per combination)")
        
        # Load dependencies from SDK
        dependencies_data = []
        for entity, deps_info in ZephyrIntelligence.DEPENDENCIES.items():
            depends_on = deps_info.get("depends_on", [])
            required_by = deps_info.get("required_by", [])
            
            dependencies_data.append({
                "entity": entity,
                "dependsOn": depends_on,
                "requiredBy": required_by,
                "dependencyCount": len(depends_on),
                "dependentCount": len(required_by),
                "isIndependent": len(depends_on) == 0,
                "isLeaf": len(required_by) == 0
            })
        
        log.info(f"  Loaded {len(dependencies_data)} entity dependencies (SDK)")
        
        # Load constraints from SDK
        constraints_data = []
        constraints = ZephyrIntelligence.get_all_constraints()
        
        # Extract blockers
        for blocker in constraints.get("blockers", []):
            constraints_data.append({
                "constraintId": blocker.get("id", "unknown"),
                "constraintType": "blocker",
                "entity": blocker.get("entity", "unknown"),
                "endpoint": blocker.get("endpoint", ""),
                "severity": blocker.get("severity", "unknown"),
                "issue": blocker.get("issue", ""),
                "impact": blocker.get("impact", ""),
                "workaround": str(blocker.get("workaround", {})),
                "workaroundStatus": blocker.get("workaround", {}).get("status", "unknown")
            })
        
        # Extract bugs
        for bug in constraints.get("bugs", []):
            constraints_data.append({
                "constraintId": bug.get("id", "unknown"),
                "constraintType": "bug",
                "entity": bug.get("entity", "unknown"),
                "endpoint": bug.get("endpoint", ""),
                "severity": bug.get("severity", "unknown"),
                "issue": bug.get("issue", ""),
                "impact": bug.get("impact", ""),
                "workaround": str(bug.get("workaround", {})),
                "workaroundStatus": bug.get("workaround", {}).get("status", "unknown")
            })
        
        # Extract quirks
        for quirk in constraints.get("quirks", []):
            constraints_data.append({
                "constraintId": quirk.get("id", "unknown"),
                "constraintType": "quirk",
                "entity": quirk.get("entity", "unknown"),
                "endpoint": "",
                "severity": quirk.get("severity", "low"),
                "issue": quirk.get("issue", ""),
                "impact": quirk.get("impact", ""),
                "workaround": str(quirk.get("workaround", {})),
                "workaroundStatus": quirk.get("workaround", {}).get("status", "unknown")
            })
        
        log.info(f"  Loaded {len(constraints_data)} API constraints (SDK)")

if "dependencies_data" not in locals():
    dependencies_data = []

if "constraints_data" not in locals():
    constraints_data = []

log.info("=" * 80)
log.info(f"Intelligence loaded:")
log.info(f"  - Schemas: {len(schema_data)} fields")
log.info(f"  - Dependencies: {len(dependencies_data)} entities")
log.info(f"  - Constraints: {len(constraints_data)} items")
log.info("=" * 80)

session.add_capability("intelligenceLoaded",
                      schema_fields=len(schema_data),
                      dependencies=len(dependencies_data),
                      constraints=len(constraints_data))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# == 4b. EXECUTE (Enhance Schema from Source Samples - Only if rebuild=False) === SPECTRA

if not rebuild:
    # Only enhance existing schema if we didn't build it from samples
    log.info("=" * 80)
    log.info("Enhancing schema from Source sample data (if available)...")
    log.info("=" * 80)
    
    from pyspark.sql import functions as F
    
    # Try to enhance array structures from Source sample tables
    log.info("Analyzing cycle.cyclePhases from Source sample data...")
    try:
        sample_tables = [
            "Tables/source/sample_dimCycle",
            "Tables/source/sample_cycles", 
            "Tables/source/cycles"
        ]
        
        df_cycles = None
        for table_path in sample_tables:
            try:
                df_cycles = spark.read.format("delta").load(table_path)
                log.info(f"  Found sample data in: {table_path}")
                break
            except Exception:
                continue
        
        if df_cycles:
            cycles_with_phases = df_cycles.filter(
                F.col("cyclePhases").isNotNull() &
                (F.size(F.col("cyclePhases")) > 0)
            ).limit(1)
            
            if cycles_with_phases.count() > 0:
                sample = cycles_with_phases.first()
                phases = sample["cyclePhases"]
                
                if phases and len(phases) > 0:
                    if isinstance(phases[0], dict):
                        element_type = "object"
                    elif isinstance(phases[0], (int, float)):
                        element_type = "integer" if isinstance(phases[0], int) else "float"
                    else:
                        element_type = "string"
                    
                    # Enhance schema
                    for field in schema_data:
                        if field["entity"] == "cycle" and field["fieldId"] == "cyclePhases":
                            field["structureType"] = f"array<{element_type}>"
                            field["description"] = f"Cycle phases array (element: {element_type})"
                            log.info(f"  Enhanced: cyclePhases -> array<{element_type}>")
    except Exception as e:
        log.warning(f"  Could not enhance from Source samples: {e}")
    
    log.info("=" * 80)
    log.info("Schema enhancement complete")
    log.info("=" * 80)
else:
    log.info("  Skipping enhancement (schema built from samples in rebuild mode)")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# == 5. EXECUTE (Create Tables) ===================================== SPECTRA

if session.params["bootstrap"]:
    log.info("=" * 80)
    log.info("Creating Prepare stage tables (bootstrap mode)...")
    log.info("=" * 80)

    spark.sql("CREATE DATABASE IF NOT EXISTS prepare")
    
    # ----------------------------------------------------------------------
    # Create prepare._schema
    # ----------------------------------------------------------------------
    
    log.info("== Creating prepare.schema DataFrame...")
    
    # Complete L6 schema with 18 fields (Jira-proven pattern)
    # SPECTRA-GRADE: Complete L6 schema with fact table support + entitySortOrder (Jira pattern)
    schema_table_schema = StructType([
        # L1 Fields (Basic intelligence)
        StructField("entity", StringType(), True),           # Target dimension (singular)
        StructField("entitySortOrder", IntegerType(), True), # Jira pattern: ensures one row per entity
        StructField("fieldId", StringType(), True),          # Raw API field name
        StructField("structureType", StringType(), True),    # scalar | array
        StructField("isRequired", BooleanType(), True),
        StructField("description", StringType(), True),
        
        # L6 Fields (Jira-proven pattern)
        StructField("rawField", ArrayType(StringType()), True),      # Properties to extract
        StructField("targetField", ArrayType(StringType()), True),   # Target column names
        StructField("dataType", ArrayType(StringType()), True),      # Target data types
        StructField("isNullable", BooleanType(), True),
        StructField("group", StringType(), True),                    # Logical grouping
        StructField("groupSortOrder", IntegerType(), True),
        
        # L6+ Fields (Dimensional modeling)
        StructField("dimensionName", StringType(), True),
        StructField("bridgeName", StringType(), True),
        StructField("notes", StringType(), True),
        
        # Fact table support (SPECTRA-grade - business process driven)
        StructField("isInFactIssue", ArrayType(BooleanType()), True),  # Fact table flag (array for consistency)
        StructField("keyField", ArrayType(BooleanType()), True),      # Key field flag (primary/foreign keys)
        StructField("factTableName", StringType(), True),             # Which fact table (e.g., "factCycle", "factExecution")
        StructField("factGrain", StringType(), True),                 # Fact table grain (e.g., "one row per cycle")
        
        # Intelligence metadata
        StructField("sourceEndpoint", StringType(), True),
        StructField("apiStatus", StringType(), True),
    ])
    
    df_schema = spark.createDataFrame(schema_data, schema_table_schema)
    schema_count = df_schema.count()
    
    log.info(f"  == Schema fields: {schema_count}")
    assert schema_count > 0, "Schema DataFrame is empty"
    
    # Write to Delta
    log.info("  >> Writing prepare.schema to Delta...")
    # SPECTRA-GRADE: Jira pattern - order by groupSortOrder, entitySortOrder, entity (ensures one row per entity)
    df_schema_ordered = df_schema.orderBy("groupSortOrder", "entitySortOrder", "entity", "fieldId")
    session.delta.write(df_schema_ordered, "prepare.schema", "Tables/prepare/schema", mode="overwrite")
    session.delta.register("prepare.schema", "Tables/prepare/schema")
    log.info("  OK prepare.schema created")
    
    # ----------------------------------------------------------------------
    # Create prepare.dependencies
    # ----------------------------------------------------------------------
    
    log.info("== Creating prepare.dependencies DataFrame...")
    
    dependencies_table_schema = StructType([
        StructField("entity", StringType(), False),
        StructField("dependsOn", ArrayType(StringType()), False),
        StructField("requiredBy", ArrayType(StringType()), False),
        StructField("dependencyCount", IntegerType(), False),
        StructField("dependentCount", IntegerType(), False),
        StructField("isIndependent", BooleanType(), False),
        StructField("isLeaf", BooleanType(), False)
    ])
    
    df_dependencies = spark.createDataFrame(dependencies_data, dependencies_table_schema)
    dependencies_count = df_dependencies.count()
    
    log.info(f"  == Entity dependencies: {dependencies_count}")
    
    # Write to Delta
    log.info("  >> Writing prepare.dependencies to Delta...")
    df_dependencies_ordered = df_dependencies.orderBy("entity")
    session.delta.write(df_dependencies_ordered, "prepare.dependencies", "Tables/prepare/dependencies", mode="overwrite")
    session.delta.register("prepare.dependencies", "Tables/prepare/dependencies")
    log.info("  OK prepare.dependencies created")
    
    # ----------------------------------------------------------------------
    # Create prepare.constraints
    # ----------------------------------------------------------------------
    
    log.info("== Creating prepare.constraints DataFrame...")
    
    constraints_table_schema = StructType([
        StructField("constraintId", StringType(), False),
        StructField("constraintType", StringType(), False),
        StructField("entity", StringType(), False),
        StructField("endpoint", StringType(), True),
        StructField("severity", StringType(), False),
        StructField("issue", StringType(), False),
        StructField("impact", StringType(), False),
        StructField("workaround", StringType(), True),
        StructField("workaroundStatus", StringType(), True)
    ])
    
    df_constraints = spark.createDataFrame(constraints_data, constraints_table_schema)
    constraints_count = df_constraints.count()
    
    log.info(f"  == API constraints: {constraints_count}")
    
    # Write to Delta
    log.info("  >> Writing prepare.constraints to Delta...")
    df_constraints_ordered = df_constraints.orderBy("severity", "entity", "constraintId")
    session.delta.write(df_constraints_ordered, "prepare.constraints", "Tables/prepare/constraints", mode="overwrite")
    session.delta.register("prepare.constraints", "Tables/prepare/constraints")
    log.info("  OK prepare.constraints created")
    
    log.info("=" * 80)
    log.info("OK All Prepare tables created (bootstrap complete)")
    log.info("=" * 80)
    
    session.add_capability("prepareTablesCreated",
                          schema_fields=schema_count,
                          dependencies=dependencies_count,
                          constraints=constraints_count)
else:
    log.info("  ÔÅ® Skipping Prepare table creation (bootstrap=False)")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# == 5. VALIDATE ===================================================== SPECTRA

if session.params["bootstrap"]:
    log.info("=" * 80)
    log.info("Validating Prepare stage tables...")
    log.info("=" * 80)
    
    # Read back tables for validation
    try:
        df_schema = spark.table("prepare.schema")
        df_dependencies = spark.table("prepare.dependencies")
        df_constraints = spark.table("prepare.constraints")
    except Exception:
        df_schema = spark.read.format("delta").load("Tables/prepare/schema")
        df_dependencies = spark.read.format("delta").load("Tables/prepare/dependencies")
        df_constraints = spark.read.format("delta").load("Tables/prepare/constraints")
        spark.sql("CREATE DATABASE IF NOT EXISTS prepare")
        session.delta.register("prepare.schema", "Tables/prepare/schema")
        session.delta.register("prepare.dependencies", "Tables/prepare/dependencies")
        session.delta.register("prepare.constraints", "Tables/prepare/constraints")
    
    # Validation: Check row counts
    schema_count = df_schema.count()
    dependencies_count = df_dependencies.count()
    constraints_count = df_constraints.count()
    
    log.info(f"  == prepare.schema: {schema_count} rows")
    log.info(f"  == prepare.dependencies: {dependencies_count} rows")
    log.info(f"  == prepare.constraints: {constraints_count} rows")
    
    assert schema_count > 0, "prepare.schema is empty"
    assert dependencies_count > 0, "prepare.dependencies is empty"
    
    # Validation: Check for required L6 schema fields
    required_schema_cols = ["entity", "fieldId", "structureType", "isRequired", "rawField", "targetField", "dataType"]
    actual_schema_cols = df_schema.columns
    missing_cols = set(required_schema_cols) - set(actual_schema_cols)
    
    if missing_cols:
        log.error(f"  !! Missing columns in prepare.schema: {missing_cols}")
        raise ValueError(f"Schema validation failed: missing columns {missing_cols}")
    
    log.info("  OK All required L6 columns present")
    log.info("  OK Prepare stage validation passed")

# Standard validation (always runs)
session.validate()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# == 6. RECORD ======================================================= SPECTRA

session.record(spark=spark)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# == 7. FINALISE ===================================================== SPECTRA

session.finalise()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
