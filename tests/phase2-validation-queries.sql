-- Phase 2: Deployment Validation SQL Queries
-- Run these queries in Fabric SQL editor after each test execution

-- ============================================================================
-- 1. PORTFOLIO TABLE VALIDATION
-- ============================================================================

-- 1.1 Check portfolio table exists and has correct schema
DESCRIBE source.portfolio;

-- 1.2 Check portfolio record count (should be 1)
SELECT COUNT(*) as portfolio_count FROM source.portfolio;

-- 1.3 Validate portfolio data quality
SELECT 
    source_system,
    contract_version,
    total_endpoints,
    hierarchical_endpoints,
    endpoint_categories,
    auth_status,
    hierarchical_access_validated,
    endpoint_success_rate,
    supports_incremental,
    status,
    is_enabled,
    discovery_date,
    last_updated,
    last_auth_check
FROM source.portfolio;

-- 1.4 Validate endpoint_categories JSON is valid
SELECT 
    source_system,
    endpoint_categories,
    JSON_VALID(endpoint_categories) as is_valid_json
FROM source.portfolio;

-- 1.5 Check endpoint success rate is between 0.0 and 1.0
SELECT 
    source_system,
    endpoint_success_rate,
    CASE 
        WHEN endpoint_success_rate >= 0.0 AND endpoint_success_rate <= 1.0 
        THEN 'VALID' 
        ELSE 'INVALID' 
    END as rate_validation
FROM source.portfolio;

-- ============================================================================
-- 2. ENDPOINTS TABLE VALIDATION
-- ============================================================================

-- 2.1 Check endpoints table exists and row count (should be 228)
SELECT COUNT(*) as endpoint_count FROM source.endpoints;
-- Expected: 228

-- 2.2 Check for duplicate endpoints
SELECT 
    endpoint_path,
    http_method,
    COUNT(*) as occurrence_count
FROM source.endpoints
GROUP BY endpoint_path, http_method
HAVING COUNT(*) > 1;
-- Expected: 0 rows (no duplicates)

-- 2.3 Validate required fields are populated
SELECT 
    COUNT(*) as total_endpoints,
    SUM(CASE WHEN endpoint_path IS NULL OR endpoint_path = '' THEN 1 ELSE 0 END) as missing_path,
    SUM(CASE WHEN http_method IS NULL OR http_method = '' THEN 1 ELSE 0 END) as missing_method,
    SUM(CASE WHEN category IS NULL OR category = '' THEN 1 ELSE 0 END) as missing_category
FROM source.endpoints;
-- Expected: missing_path=0, missing_method=0, missing_category=0

-- 2.4 Category distribution
SELECT 
    category,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM source.endpoints
GROUP BY category
ORDER BY count DESC;

-- 2.5 Hierarchical vs flat endpoints
SELECT 
    hierarchical,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM source.endpoints
GROUP BY hierarchical;

-- 2.6 Endpoints requiring authentication
SELECT 
    requires_auth,
    COUNT(*) as count
FROM source.endpoints
GROUP BY requires_auth;

-- ============================================================================
-- 3. CONFIG TABLE VALIDATION
-- ============================================================================

-- 3.1 Check config table row count (should be 7)
SELECT COUNT(*) as config_count FROM source.config;
-- Expected: 7

-- 3.2 List all config entries
SELECT 
    config_key,
    config_value,
    last_updated
FROM source.config
ORDER BY config_key;

-- 3.3 Validate specific config values
SELECT 
    config_key,
    config_value,
    CASE 
        WHEN config_key = 'sdk_version' AND config_value = '0.3.0' THEN 'VALID'
        WHEN config_key = 'execution_mode' AND config_value IN ('interactive', 'pipeline') THEN 'VALID'
        WHEN config_key = 'stage' AND config_value = 'source' THEN 'VALID'
        WHEN config_key = 'notebook_name' AND config_value = 'sourceZephyr' THEN 'VALID'
        ELSE 'CHECK'
    END as validation_status
FROM source.config;

-- ============================================================================
-- 4. CREDENTIALS TABLE VALIDATION
-- ============================================================================

-- 4.1 Check credentials table row count (should be 1)
SELECT COUNT(*) as credentials_count FROM source.credentials;
-- Expected: 1

-- 4.2 Validate token masking (should show ***_XXX format)
SELECT 
    credential_type,
    credential_value,
    validation_status,
    last_validated
FROM source.credentials;

-- 4.3 Verify no plaintext tokens (should not contain full token)
-- Replace 'YOUR_TOKEN_START' with actual token prefix to verify masking
SELECT 
    credential_value,
    CASE 
        WHEN credential_value LIKE '***_%' THEN 'VALID_MASKED'
        WHEN LENGTH(credential_value) <= 10 THEN 'SHORT_ENOUGH'
        ELSE 'CHECK_MASKING'
    END as masking_validation
FROM source.credentials;

-- ============================================================================
-- 5. PREVIEW SAMPLE TABLES VALIDATION
-- ============================================================================

-- 5.1 Check if preview tables exist (only if preview=True)
SELECT 
    'source.sample_projects' as table_name,
    COUNT(*) as row_count
FROM source.sample_projects
UNION ALL
SELECT 
    'source.sample_releases' as table_name,
    COUNT(*) as row_count
FROM source.sample_releases
UNION ALL
SELECT 
    'source.sample_cycles' as table_name,
    COUNT(*) as row_count
FROM source.sample_cycles
UNION ALL
SELECT 
    'source.sample_executions' as table_name,
    COUNT(*) as row_count
FROM source.sample_executions
UNION ALL
SELECT 
    'source.sample_testcases' as table_name,
    COUNT(*) as row_count
FROM source.sample_testcases;
-- Expected: 2 rows per table if preview=True

-- 5.2 Validate sample data structure (example for projects)
SELECT 
    id,
    name,
    COUNT(*) as count
FROM source.sample_projects
GROUP BY id, name;
-- Should have valid structure matching API response

-- ============================================================================
-- 6. DATA QUALITY CHECKS
-- ============================================================================

-- 6.1 Check for null values in critical portfolio fields
SELECT 
    source_system,
    CASE WHEN contract_version IS NULL THEN 'NULL' ELSE 'OK' END as contract_version_check,
    CASE WHEN total_endpoints IS NULL THEN 'NULL' ELSE 'OK' END as total_endpoints_check,
    CASE WHEN auth_status IS NULL THEN 'NULL' ELSE 'OK' END as auth_status_check,
    CASE WHEN discovery_date IS NULL THEN 'NULL' ELSE 'OK' END as discovery_date_check,
    CASE WHEN last_updated IS NULL THEN 'NULL' ELSE 'OK' END as last_updated_check
FROM source.portfolio;

-- 6.2 Validate endpoint count matches catalog
SELECT 
    (SELECT COUNT(*) FROM source.endpoints) as catalog_endpoints,
    (SELECT total_endpoints FROM source.portfolio) as portfolio_endpoints,
    CASE 
        WHEN (SELECT COUNT(*) FROM source.endpoints) = (SELECT total_endpoints FROM source.portfolio)
        THEN 'MATCH'
        ELSE 'MISMATCH'
    END as validation
;
-- Expected: MATCH

-- 6.3 Validate hierarchical endpoint count
SELECT 
    (SELECT COUNT(*) FROM source.endpoints WHERE hierarchical = true) as catalog_hierarchical,
    (SELECT hierarchical_endpoints FROM source.portfolio) as portfolio_hierarchical,
    CASE 
        WHEN (SELECT COUNT(*) FROM source.endpoints WHERE hierarchical = true) = (SELECT hierarchical_endpoints FROM source.portfolio)
        THEN 'MATCH'
        ELSE 'MISMATCH'
    END as validation
;
-- Expected: MATCH

-- ============================================================================
-- 7. SCHEMA EVOLUTION CHECK
-- ============================================================================

-- 7.1 Compare portfolio schema with expected structure
SELECT 
    column_name,
    data_type,
    is_nullable
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'source' AND table_name = 'portfolio'
ORDER BY ordinal_position;
-- Expected: 15 columns with correct types

-- 7.2 Compare endpoints schema
SELECT 
    column_name,
    data_type,
    is_nullable
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'source' AND table_name = 'endpoints'
ORDER BY ordinal_position;

-- ============================================================================
-- 8. TIMESTAMP VALIDATION
-- ============================================================================

-- 8.1 Check timestamps are recent (within last hour)
SELECT 
    source_system,
    last_updated,
    DATEDIFF(minute, last_updated, CURRENT_TIMESTAMP) as minutes_ago,
    CASE 
        WHEN DATEDIFF(minute, last_updated, CURRENT_TIMESTAMP) < 60 THEN 'RECENT'
        ELSE 'OLD'
    END as freshness
FROM source.portfolio;

-- 8.2 Check discovery_date vs last_updated relationship
SELECT 
    source_system,
    discovery_date,
    CAST(last_updated AS DATE) as last_updated_date,
    CASE 
        WHEN discovery_date <= CAST(last_updated AS DATE) THEN 'VALID'
        ELSE 'INVALID'
    END as date_validation
FROM source.portfolio;
-- Expected: discovery_date <= last_updated_date

