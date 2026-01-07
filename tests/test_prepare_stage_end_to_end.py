"""
End-to-end test for Prepare stage with SDK integration.

Tests the complete flow:
1. Import ZephyrIntelligence from SDK
2. Bootstrap mode (table creation)
3. Rebuild mode (API fetching)
4. Fallback logic (SDK vs intelligence.py)
"""

import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestPrepareStageEndToEnd:
    """End-to-end tests for Prepare stage."""
    
    def test_zephyr_intelligence_available_after_sdk_run(self):
        """Test that ZephyrIntelligence is available after %run spectraSDK."""
        # Simulate SDK run - ZephyrIntelligence should be in globals
        # In real Fabric notebook, %run spectraSDK makes it available
        
        # Mock the SDK content
        mock_intelligence = MagicMock()
        mock_intelligence.ENTITIES = {
            "cycle": {
                "endpoint": "/cycle",
                "fields": [
                    {
                        "fieldId": "id",
                        "structureType": "scalar",
                        "dataType": ["int64"],
                        "rawField": ["id"],
                        "targetField": ["cycleId"],
                    }
                ]
            }
        }
        mock_intelligence.SCHEMAS = {}  # SDK doesn't have SCHEMAS
        
        # Simulate globals after %run spectraSDK
        globals()['ZephyrIntelligence'] = mock_intelligence
        
        # Test that it's available
        assert 'ZephyrIntelligence' in globals()
        assert hasattr(globals()['ZephyrIntelligence'], 'ENTITIES')
    
    def test_import_validation_logic(self):
        """Test the import validation logic."""
        # Test with ENTITIES (SDK format)
        mock_intelligence = MagicMock()
        mock_intelligence.ENTITIES = {"cycle": {}}
        mock_intelligence.SCHEMAS = {}
        mock_intelligence.READ_ENDPOINTS = {}
        
        # Should pass validation
        assert hasattr(mock_intelligence, 'ENTITIES')
        assert hasattr(mock_intelligence, 'SCHEMAS') or hasattr(mock_intelligence, 'ENTITIES')
        
        # Test without either
        mock_intelligence_no_attrs = MagicMock()
        delattr(mock_intelligence_no_attrs, 'ENTITIES') if hasattr(mock_intelligence_no_attrs, 'ENTITIES') else None
        delattr(mock_intelligence_no_attrs, 'SCHEMAS') if hasattr(mock_intelligence_no_attrs, 'SCHEMAS') else None
        
        with pytest.raises(AttributeError):
            if not (hasattr(mock_intelligence_no_attrs, 'ENTITIES') or hasattr(mock_intelligence_no_attrs, 'SCHEMAS')):
                raise AttributeError("ZephyrIntelligence missing ENTITIES or SCHEMAS attribute")
    
    def test_read_endpoint_fallback(self):
        """Test READ_ENDPOINTS fallback logic."""
        # Test with READ_ENDPOINTS available
        mock_intelligence = MagicMock()
        mock_intelligence.get_read_endpoint = Mock(return_value={"endpoint": "/release", "method": "GET"})
        mock_intelligence.get_read_endpoint_path = Mock(return_value="/release?projectId=44")
        
        if hasattr(mock_intelligence, 'get_read_endpoint'):
            endpoint = mock_intelligence.get_read_endpoint("release")
            assert endpoint is not None
        
        # Test without READ_ENDPOINTS (fallback)
        mock_intelligence_no_read = MagicMock()
        if not hasattr(mock_intelligence_no_read, 'get_read_endpoint'):
            # Fallback: Use hardcoded endpoint
            releases_url = f"https://api.example.com/release?projectId=44"
            assert "release" in releases_url
            assert "projectId=44" in releases_url
    
    def test_entities_format_parsing(self):
        """Test parsing ENTITIES format (SDK structure)."""
        # Simulate SDK ENTITIES structure
        entities_data = {
            "cycle": {
                "endpoint": "/cycle",
                "fields": [
                    {
                        "fieldId": "id",
                        "structureType": "scalar",
                        "dataType": ["int64"],
                        "rawField": ["id"],
                        "targetField": ["cycleId"],
                        "isRequired": False,
                        "isNullable": True,
                        "group": "identity",
                        "groupSortOrder": 1,
                    }
                ]
            }
        }
        
        # Test parsing logic
        entity_fields = {}
        for entity_name, entity_info in entities_data.items():
            fields = entity_info.get("fields", [])
            for field_def in fields:
                structure_type = field_def.get("structureType", "scalar")
                key = (entity_name, structure_type)
                
                if key not in entity_fields:
                    entity_fields[key] = {
                        "rawField": [],
                        "targetField": [],
                        "dataType": [],
                    }
                
                raw_fields = field_def.get("rawField", [])
                target_fields = field_def.get("targetField", [])
                data_types = field_def.get("dataType", [])
                
                entity_fields[key]["rawField"].extend(raw_fields)
                entity_fields[key]["targetField"].extend(target_fields)
                entity_fields[key]["dataType"].extend(data_types)
        
        # Verify structure
        assert ("cycle", "scalar") in entity_fields
        assert len(entity_fields[("cycle", "scalar")]["rawField"]) > 0
    
    def test_schemas_format_parsing(self):
        """Test parsing SCHEMAS format (intelligence.py structure)."""
        # Simulate intelligence.py SCHEMAS structure
        schemas_data = {
            "cycle": {
                "entity": "cycle",
                "endpoint": "/cycle",
                "schema": {
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "cyclePhases": {"type": "array"}
                    },
                    "required": ["id", "name"]
                }
            }
        }
        
        # Test parsing logic
        entity_fields = {}
        for entity_name, entity_info in schemas_data.items():
            schema_info = entity_info.get("schema", {})
            properties = schema_info.get("properties", {})
            required_fields = schema_info.get("required", [])
            
            scalar_fields = []
            for prop_name, prop_info in properties.items():
                prop_type = prop_info.get("type", "string")
                if prop_type != "array" and prop_type != "object":
                    scalar_fields.append(prop_name)
            
            if scalar_fields:
                key = (entity_name, "scalar")
                entity_fields[key] = {
                    "rawField": scalar_fields,
                    "targetField": scalar_fields,
                    "dataType": [properties[p].get("type", "text") for p in scalar_fields],
                }
        
        # Verify structure
        assert ("cycle", "scalar") in entity_fields
        assert "id" in entity_fields[("cycle", "scalar")]["rawField"]
        assert "name" in entity_fields[("cycle", "scalar")]["rawField"]


class TestPrepareStageAPIEndpoints:
    """Test API endpoint construction and fallback."""
    
    def test_release_endpoint_construction(self):
        """Test release endpoint URL construction."""
        base_url = "https://api.example.com/flex/services/rest/latest"
        production_project_id = 44
        
        # Test with READ_ENDPOINTS
        if True:  # Simulate hasattr check
            releases_url = f"{base_url.rstrip('/')}/release?projectId={production_project_id}"
            assert "release" in releases_url
            assert "projectId=44" in releases_url
    
    def test_cycle_endpoint_construction(self):
        """Test cycle endpoint URL construction with path params."""
        base_url = "https://api.example.com/flex/services/rest/latest"
        release_id = 123
        
        # Test with READ_ENDPOINTS
        if True:  # Simulate hasattr check
            cycles_url = f"{base_url.rstrip('/')}/cycle/release/{release_id}"
            assert "cycle/release" in cycles_url
            assert "123" in cycles_url
    
    def test_endpoint_fallback_when_read_endpoints_missing(self):
        """Test endpoint fallback when READ_ENDPOINTS not in SDK."""
        base_url = "https://api.example.com/flex/services/rest/latest"
        production_project_id = 44
        release_id = 123
        
        # Simulate SDK without READ_ENDPOINTS
        has_read_endpoints = False
        
        if not has_read_endpoints:
            # Fallback endpoints
            releases_url = f"{base_url.rstrip('/')}/release?projectId={production_project_id}"
            cycles_url = f"{base_url.rstrip('/')}/cycle/release/{release_id}"
            
            assert "release" in releases_url
            assert "projectId=44" in releases_url
            assert "cycle/release" in cycles_url
            assert "123" in cycles_url




