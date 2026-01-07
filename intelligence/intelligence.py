# ==============================================================================
# ZEPHYR API INTELLIGENCE
# Auto-generated from intelligence/ folder
# Source: API Intelligence Framework (7-phase discovery)
# ==============================================================================

class ZephyrIntelligence:
    """Zephyr API intelligence - schemas, dependencies, constraints."""

    # Schemas from intelligence/schemas/*.json
    SCHEMAS = {
        "cycle": {
            "entity": "cycle",
            "endpoint": "/cycle",
            "method": "POST",
            "status": '✅ Working',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "environment": {
                                                            "type": "string"
                                            },
                                            "build": {
                                                            "type": "string"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "startDate": {
                                                            "type": "integer"
                                            },
                                            "endDate": {
                                                            "type": "integer"
                                            },
                                            "cycleStartDate": {
                                                            "type": "string"
                                            },
                                            "cycleEndDate": {
                                                            "type": "string"
                                            },
                                            "status": {
                                                            "type": "integer"
                                            },
                                            "revision": {
                                                            "type": "integer"
                                            },
                                            "releaseId": {
                                                            "type": "integer"
                                            },
                                            "cyclePhases": {
                                                            "type": "array"
                                            },
                                            "createdOn": {
                                                            "type": "integer"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "build",
                                            "createdOn",
                                            "cycleEndDate",
                                            "cyclePhases",
                                            "cycleStartDate",
                                            "endDate",
                                            "environment",
                                            "hasChild",
                                            "id",
                                            "name",
                                            "releaseId",
                                            "revision",
                                            "startDate",
                                            "status"
                            ]
            },
            "notes": 'Requires unlocked release. Use existing releases.'
        },
        "release": {
            "entity": "release",
            "endpoint": "/release",
            "method": "POST",
            "status": '✅ Working',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "description": {
                                                            "type": "string"
                                            },
                                            "startDate": {
                                                            "type": "integer"
                                            },
                                            "releaseStartDate": {
                                                            "type": "string"
                                            },
                                            "createdDate": {
                                                            "type": "integer"
                                            },
                                            "projectId": {
                                                            "type": "integer"
                                            },
                                            "orderId": {
                                                            "type": "integer"
                                            },
                                            "globalRelease": {
                                                            "type": "boolean"
                                            },
                                            "projectRelease": {
                                                            "type": "boolean"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            },
                                            "syncEnabled": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "createdDate",
                                            "description",
                                            "globalRelease",
                                            "hasChild",
                                            "id",
                                            "name",
                                            "orderId",
                                            "projectId",
                                            "projectRelease",
                                            "releaseStartDate",
                                            "startDate",
                                            "syncEnabled"
                            ]
            },
            "notes": 'BLOCKER-003: Locks for >60s after creation'
        },
        "requirement": {
            "entity": "requirement",
            "endpoint": "/requirementtree/add",
            "method": "POST",
            "status": '✅ Working (workaround)',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "description": {
                                                            "type": "string"
                                            },
                                            "projectId": {
                                                            "type": "integer"
                                            },
                                            "parentId": {
                                                            "type": "integer"
                                            },
                                            "categories": {
                                                            "type": "array"
                                            },
                                            "requirements": {
                                                            "type": "array"
                                            },
                                            "lastModifiedOn": {
                                                            "type": "integer"
                                            },
                                            "releaseIds": {
                                                            "type": "array"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "categories",
                                            "description",
                                            "hasChild",
                                            "id",
                                            "lastModifiedOn",
                                            "name",
                                            "parentId",
                                            "projectId",
                                            "releaseIds",
                                            "requirements"
                            ]
            },
            "notes": 'BLOCKER-001: POST /requirement broken. Using /requirementtree/add with parentId.'
        },
        "requirement_folder": {
            "entity": "requirement_folder",
            "endpoint": "/requirementtree/add",
            "method": "POST",
            "status": '✅ Working',
            "schema": {
                            "$schema": "http://json-schema.org/schema#",
                            "type": "object",
                            "properties": {
                                            "id": {
                                                            "type": "integer"
                                            },
                                            "name": {
                                                            "type": "string"
                                            },
                                            "description": {
                                                            "type": "string"
                                            },
                                            "projectId": {
                                                            "type": "integer"
                                            },
                                            "categories": {
                                                            "type": "array"
                                            },
                                            "requirements": {
                                                            "type": "array"
                                            },
                                            "lastModifiedOn": {
                                                            "type": "integer"
                                            },
                                            "releaseIds": {
                                                            "type": "array"
                                            },
                                            "hasChild": {
                                                            "type": "boolean"
                                            }
                            },
                            "required": [
                                            "categories",
                                            "description",
                                            "hasChild",
                                            "id",
                                            "lastModifiedOn",
                                            "name",
                                            "projectId",
                                            "releaseIds",
                                            "requirements"
                            ]
            },
            "notes": 'Works perfectly'
        },
        "testcase_folder": {
            "entity": "testcase_folder",
            "endpoint": "/testcasetree",
            "method": "POST",
            "status": '❌ Broken',
            "schema": None,
            "notes": 'BLOCKER-002: API rejects valid payloads (HTTP 400)'
        },
    }

    # READ endpoints for production mode (GET endpoints for reading from project 44)
    # These are used by Prepare stage to build schema from production data
    READ_ENDPOINTS = {
        "project": {
            "endpoint": "/project",
            "method": "GET",
            "description": "Get all projects",
            "read_only": True,
            "project": 44  # Production project
        },
        "release": {
            "endpoint": "/release",
            "method": "GET",
            "description": "Get releases for a project",
            "read_only": True,
            "project": 44,  # Production project
            "query_params": ["projectId"],
            "example": "/release?projectId=44"
        },
        "cycle": {
            "endpoint": "/cycle/release/{releaseid}",
            "method": "GET",
            "description": "Get cycles for a release",
            "read_only": True,
            "project": 44,  # Production project
            "path_params": ["releaseid"],
            "depends_on": "release",  # Must fetch release first
            "example": "/cycle/release/123"
        },
        "execution": {
            "endpoint": "/execution",
            "method": "GET",
            "description": "Get executions (may require cycle/testcase filters)",
            "read_only": True,
            "project": 44,  # Production project
            "depends_on": ["cycle", "testcase"]
        },
        "requirement": {
            "endpoint": "/requirement",
            "method": "GET",
            "description": "Get requirements",
            "read_only": True,
            "project": 44  # Production project
        },
        "testcase": {
            "endpoint": "/testcase",
            "method": "GET",
            "description": "Get test cases",
            "read_only": True,
            "project": 44  # Production project
        }
    }

    # Dependencies from intelligence/dependencies.yaml
    DEPENDENCIES = {'project': {'depends_on': [], 'required_by': ['testcase_folder'], 'dependency_count': 0, 'dependent_count': 1}, 'release': {'depends_on': [], 'required_by': ['cycle'], 'dependency_count': 0, 'dependent_count': 1}, 'requirement_folder': {'depends_on': [], 'required_by': ['requirement'], 'dependency_count': 0, 'dependent_count': 1}, 'requirement': {'depends_on': ['requirement_folder'], 'required_by': [], 'dependency_count': 1, 'dependent_count': 0}, 'cycle': {'depends_on': ['release'], 'required_by': ['execution'], 'dependency_count': 1, 'dependent_count': 1}, 'testcase_folder': {'depends_on': ['project'], 'required_by': ['testcase'], 'dependency_count': 1, 'dependent_count': 1}, 'testcase': {'depends_on': ['testcase_folder'], 'required_by': ['allocation', 'execution'], 'dependency_count': 1, 'dependent_count': 2}, 'execution': {'depends_on': ['testcase', 'cycle'], 'required_by': [], 'dependency_count': 2, 'dependent_count': 0}, 'allocation': {'depends_on': ['testcase'], 'required_by': [], 'dependency_count': 1, 'dependent_count': 0}}

    # Constraints from intelligence/quirks.yaml
    CONSTRAINTS = {'blockers': [{'id': 'BLOCKER-001', 'title': 'Requirement Creation API Broken', 'severity': 'critical', 'entity': 'requirement', 'endpoint': 'POST /requirement', 'issue': "Returns HTTP 500: 'Cannot invoke java.lang.Long.longValue() because id is null'", 'impact': 'Cannot create requirements via documented API', 'workaround': {'method': 'Use POST /requirementtree/add with parentId', 'status': '✅ Working', 'notes': 'Must create requirement_folder first, then use parentId'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08'}, {'id': 'BLOCKER-002', 'title': 'Testcase Folder API Broken', 'severity': 'critical', 'entity': 'testcase_folder', 'endpoint': 'POST /testcasetree', 'issue': "Returns HTTP 400: 'For input string: null'", 'impact': 'Cannot create testcase folders, blocks all testcase/execution/allocation creation', 'workaround': {'method': 'Manual creation in UI required', 'status': '⚠️ Manual only', 'notes': 'Tried 4 variations (omit parentId, parentId: null, parentId: 0, no parentId field) - all failed'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08', 'blocks': ['testcase', 'execution', 'allocation']}, {'id': 'BLOCKER-003', 'title': 'Release Lock Duration >60 Seconds', 'severity': 'high', 'entity': 'release', 'endpoint': 'POST /release', 'issue': 'Newly created releases are locked for >60 seconds, preventing cycle creation', 'impact': 'Cannot create cycles immediately after release creation', 'workaround': {'method': 'Use existing (old) releases for cycle creation', 'status': '✅ Working', 'notes': 'Tested 15s, 30s, 60s delays - all failed. Old releases work immediately.'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08'}], 'bugs': [{'id': 'BUG-007', 'title': 'Release GET by ID Returns HTTP 403', 'severity': 'medium', 'entity': 'release', 'endpoint': 'GET /release/{id}', 'issue': 'Returns HTTP 403 Forbidden even with valid API token', 'impact': 'Cannot validate release creation via GET', 'workaround': {'method': 'Skip GET validation for releases', 'status': '✅ Working', 'notes': 'Assume creation succeeded if POST returns 200/201'}, 'reported_to_vendor': False, 'date_discovered': '2025-12-08'}], 'quirks': [{'id': 'QUIRK-001', 'title': 'Requirement Names Must Be Unique Across All Runs', 'severity': 'low', 'entity': 'requirement', 'issue': 'API rejects duplicate requirement names even across different test runs', 'impact': 'Must use timestamps or UUIDs in requirement names', 'workaround': {'method': 'Include timestamp in requirement name', 'status': '✅ Working', 'notes': "Use datetime.now().strftime('%Y%m%d%H%M%S') in name"}, 'date_discovered': '2025-12-08'}, {'id': 'QUIRK-002', 'title': 'Cycle Creation Requires Unlocked Release', 'severity': 'medium', 'entity': 'cycle', 'issue': 'Cannot create cycle with newly created release (locked)', 'impact': 'Must use existing releases or wait >60s', 'workaround': {'method': 'Query for existing releases and use oldest one', 'status': '✅ Working', 'notes': 'Oldest releases are most likely unlocked'}, 'date_discovered': '2025-12-08'}, {'id': 'QUIRK-003', 'title': 'Testcase Requires tcrCatalogTreeId (Folder ID)', 'severity': 'medium', 'entity': 'testcase', 'issue': 'Cannot create testcase without tcrCatalogTreeId', 'impact': 'Blocked by BLOCKER-002 (folder creation broken)', 'workaround': {'method': 'None - depends on folder API fix', 'status': '❌ Blocked', 'notes': 'Must fix folder API first'}, 'date_discovered': '2025-12-08'}], 'api_inconsistencies': [{'id': 'INCONSISTENCY-001', 'title': 'Requirement Creation Uses Folder Endpoint', 'entity': 'requirement', 'issue': 'POST /requirement is broken, must use POST /requirementtree/add', 'notes': 'Folder and requirement creation use same endpoint, differentiated by parentId presence'}, {'id': 'INCONSISTENCY-002', 'title': 'Date Format Inconsistency', 'entity': 'multiple', 'issue': "Some endpoints accept 'YYYY-MM-DD', others require epoch milliseconds", 'examples': {'release': "Accepts 'YYYY-MM-DD' string", 'cycle': 'Requires epoch milliseconds (int)'}, 'notes': 'No consistent date format across API'}], 'undocumented_behavior': [{'id': 'UNDOCUMENTED-001', 'title': 'Release Lock Mechanism', 'entity': 'release', 'behavior': 'Releases are locked after creation for >60 seconds', 'notes': 'Not mentioned in API documentation'}, {'id': 'UNDOCUMENTED-002', 'title': 'Folder API parentId Rejection', 'entity': 'testcase_folder', 'behavior': "API rejects parentId: null despite documentation suggesting it's valid for root folders", 'notes': "Documentation doesn't clarify how to create root folders"}]}

    @classmethod
    def get_schema(cls, entity: str):
        """Get schema for an entity."""
        return cls.SCHEMAS.get(entity)

    @classmethod
    def get_dependencies(cls, entity: str):
        """Get dependencies for an entity."""
        return cls.DEPENDENCIES.get(entity, {})

    @classmethod
    def get_creation_order(cls):
        """Get entities in dependency order."""
        # Based on topological sort from intelligence/creation-order.yaml
        return ['project', 'release', 'requirement_folder', 'testcase_folder', 'cycle', 'requirement', 'testcase', 'allocation', 'execution']

    @classmethod
    def get_all_constraints(cls):
        """Get all constraints (blockers, bugs, quirks)."""
        return cls.CONSTRAINTS
    
    @classmethod
    def get_read_endpoint(cls, entity: str):
        """Get READ endpoint for an entity (production mode - GET endpoints)."""
        return cls.READ_ENDPOINTS.get(entity)
    
    @classmethod
    def get_read_endpoint_path(cls, entity: str, **params):
        """Get READ endpoint path with parameters filled in."""
        endpoint_info = cls.READ_ENDPOINTS.get(entity)
        if not endpoint_info:
            return None
        
        path = endpoint_info["endpoint"]
        
        # Fill path parameters (e.g., {releaseid} → actual release ID)
        if "path_params" in endpoint_info:
            for param in endpoint_info["path_params"]:
                if param in params:
                    path = path.replace(f"{{{param}}}", str(params[param]))
        
        # Add query parameters
        if "query_params" in endpoint_info and params:
            query_parts = []
            for param in endpoint_info["query_params"]:
                if param in params:
                    query_parts.append(f"{param}={params[param]}")
            if query_parts:
                path += "?" + "&".join(query_parts)
        
        return path