# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # {PROJECT} API Intelligence
# 
# This notebook contains source-specific intelligence about the {PROJECT} API:
# - **Schemas**: JSON schemas for each entity
# - **Endpoints**: API endpoint catalog with methods, parameters, dependencies
# - **Dependencies**: Entity dependency relationships
# - **Constraints**: API bugs, blockers, workarounds, quirks
# 
# **Usage**: `%run {PROJECT}Intelligence` in your notebooks to load intelligence.
# 
# **Note**: This intelligence is discovered through API investigation and should be
# updated as you learn more about the {PROJECT} API.

# CELL ********************

class {PROJECT}Intelligence:
    """
    {PROJECT} API intelligence - schemas, dependencies, constraints.
    
    This class contains all source-specific knowledge about the {PROJECT} API.
    It is loaded via `%run {PROJECT}Intelligence` in notebooks.
    
    Structure:
    - SCHEMAS: JSON schemas for each entity type
    - READ_ENDPOINTS: GET endpoints for reading data
    - DEPENDENCIES: Entity dependency relationships
    - CONSTRAINTS: API bugs, blockers, workarounds, quirks
    """
    
    # ============================================================================
    # SCHEMAS
    # ============================================================================
    # JSON schemas for each entity type discovered from API responses
    # Format: {entity_name: {entity, endpoint, method, schema, notes}}
    
    SCHEMAS = {
        # Example structure (replace with your actual schemas):
        # "entity1": {
        #     "entity": "entity1",
        #     "endpoint": "/entity1",
        #     "method": "GET",
        #     "status": "✅ Working",
        #     "schema": {
        #         "$schema": "http://json-schema.org/schema#",
        #         "type": "object",
        #         "properties": {
        #             "id": {"type": "integer"},
        #             "name": {"type": "string"}
        #         },
        #         "required": ["id", "name"]
        #     },
        #     "notes": "Entity description and any special notes"
        # }
    }
    
    # ============================================================================
    # READ ENDPOINTS
    # ============================================================================
    # GET endpoints for reading data (production mode)
    # Format: {entity_name: {endpoint, method, query_params, path_params, ...}}
    
    READ_ENDPOINTS = {
        # Example structure (replace with your actual endpoints):
        # "entity1": {
        #     "endpoint": "/entity1",
        #     "method": "GET",
        #     "query_params": [],  # e.g., ["projectId", "limit"]
        #     "path_params": [],    # e.g., ["id"]
        #     "hierarchical": False,
        #     "requires_parent": None,  # e.g., "projectId"
        #     "parent_level": None,      # e.g., "projects"
        #     "status": "✅ Working"
        # }
    }
    
    # ============================================================================
    # DEPENDENCIES
    # ============================================================================
    # Entity dependency relationships (for hierarchical APIs)
    # Format: {entity: {depends_on: [parent_entities], required_for: [child_entities]}}
    
    DEPENDENCIES = {
        # Example structure (replace with your actual dependencies):
        # "entity1": {
        #     "depends_on": [],
        #     "required_for": ["entity2", "entity3"]
        # },
        # "entity2": {
        #     "depends_on": ["entity1"],
        #     "required_for": ["entity4"]
        # }
    }
    
    # ============================================================================
    # CONSTRAINTS
    # ============================================================================
    # API bugs, blockers, workarounds, quirks discovered during investigation
    # Format: {constraint_type: [list of constraints]}
    
    CONSTRAINTS = {
        "blockers": [
            # Example:
            # {
            #     "id": "BLOCKER-001",
            #     "title": "Endpoint Broken",
            #     "entity": "entity1",
            #     "endpoint": "POST /entity1",
            #     "issue": "Returns HTTP 500",
            #     "severity": "critical",
            #     "workaround": "Use alternative endpoint",
            #     "reported_to_vendor": False
            # }
        ],
        "bugs": [
            # Example:
            # {
            #     "id": "BUG-001",
            #     "title": "Validation Issue",
            #     "entity": "entity1",
            #     "issue": "Accepts invalid data",
            #     "workaround": "Validate client-side"
            # }
        ],
        "quirks": [
            # Example:
            # {
            #     "id": "QUIRK-001",
            #     "title": "Date Format Inconsistency",
            #     "issue": "Some endpoints accept 'YYYY-MM-DD', others require epoch milliseconds",
            #     "notes": "No consistent date format across API"
            # }
        ]
    }
    
    # ============================================================================
    # HELPER METHODS
    # ============================================================================
    
    @classmethod
    def get_read_endpoint_path(cls, entity: str, **params) -> str:
        """
        Get READ endpoint path with parameters filled in.
        
        Args:
            entity: Entity name (e.g., "entity1")
            **params: Path and query parameters
            
        Returns:
            Endpoint path with parameters filled in
            
        Example:
            >>> {PROJECT}Intelligence.get_read_endpoint_path("entity2", projectId=44)
            "/entity2?projectId=44"
        """
        if entity not in cls.READ_ENDPOINTS:
            raise ValueError(f"Entity '{entity}' not found in READ_ENDPOINTS")
        
        endpoint_info = cls.READ_ENDPOINTS[entity]
        endpoint = endpoint_info["endpoint"]
        
        # Fill path parameters
        for param in endpoint_info.get("path_params", []):
            if param not in params:
                raise ValueError(f"Missing required path parameter: {param}")
            endpoint = endpoint.replace(f"{{{param}}}", str(params[param]))
        
        # Add query parameters
        query_params = endpoint_info.get("query_params", [])
        query_strings = []
        for param in query_params:
            if param in params:
                query_strings.append(f"{param}={params[param]}")
        
        if query_strings:
            endpoint += "?" + "&".join(query_strings)
        
        return endpoint
    
    @classmethod
    def get_entity_dependencies(cls, entity: str) -> dict:
        """
        Get dependency information for an entity.
        
        Args:
            entity: Entity name
            
        Returns:
            Dict with 'depends_on' and 'required_for' lists
        """
        return cls.DEPENDENCIES.get(entity, {"depends_on": [], "required_for": []})
    
    @classmethod
    def get_constraints_for_entity(cls, entity: str) -> dict:
        """
        Get all constraints (blockers, bugs, quirks) for an entity.
        
        Args:
            entity: Entity name
            
        Returns:
            Dict with 'blockers', 'bugs', 'quirks' lists
        """
        result = {"blockers": [], "bugs": [], "quirks": []}
        
        for constraint_type in ["blockers", "bugs", "quirks"]:
            for constraint in cls.CONSTRAINTS.get(constraint_type, []):
                if constraint.get("entity") == entity:
                    result[constraint_type].append(constraint)
        
        return result

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Intelligence loaded successfully
print(f"✅ {PROJECT}Intelligence loaded")
print(f"   - Schemas: {len({PROJECT}Intelligence.SCHEMAS)}")
print(f"   - Read Endpoints: {len({PROJECT}Intelligence.READ_ENDPOINTS)}")
print(f"   - Dependencies: {len({PROJECT}Intelligence.DEPENDENCIES)}")
print(f"   - Constraints: {sum(len(v) for v in {PROJECT}Intelligence.CONSTRAINTS.values())}")

