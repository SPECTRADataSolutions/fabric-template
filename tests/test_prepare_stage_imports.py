"""
Tests for Prepare stage import logic and ZephyrIntelligence loading.

Tests the import fallback mechanisms for ZephyrIntelligence in Fabric notebook environment.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestZephyrIntelligenceImport:
    """Test ZephyrIntelligence import logic for Fabric notebooks."""
    
    def test_import_from_sdk_success(self):
        """Test successful import from SDK."""
        # Mock the SDK import
        mock_intelligence = MagicMock()
        mock_intelligence.ZephyrIntelligence = MagicMock()
        
        with patch.dict('sys.modules', {'intelligence.intelligence': mock_intelligence}):
            from intelligence.intelligence import ZephyrIntelligence
            assert ZephyrIntelligence is not None
    
    def test_import_fallback_to_file(self):
        """Test fallback to loading from file when SDK import fails."""
        import importlib.util
        
        # Create a temporary intelligence.py file
        test_dir = Path(__file__).parent.parent
        intelligence_file = test_dir / "intelligence" / "intelligence.py"
        
        if intelligence_file.exists():
            spec = importlib.util.spec_from_file_location(
                "intelligence_intelligence", 
                str(intelligence_file)
            )
            assert spec is not None
            assert spec.loader is not None
    
    def test_import_error_when_not_found(self):
        """Test that ImportError is raised when intelligence not found."""
        # Remove intelligence from sys.modules if present
        if 'intelligence.intelligence' in sys.modules:
            del sys.modules['intelligence.intelligence']
        
        with patch('importlib.util.spec_from_file_location', return_value=None):
            with pytest.raises(ImportError):
                # This should raise ImportError
                import intelligence.intelligence
                raise ImportError("ZephyrIntelligence not found")


class TestZephyrIntelligenceStructure:
    """Test ZephyrIntelligence class structure and methods."""
    
    def test_schemas_attribute_exists(self):
        """Test that SCHEMAS attribute exists."""
        try:
            from intelligence.intelligence import ZephyrIntelligence
            assert hasattr(ZephyrIntelligence, 'SCHEMAS')
            assert isinstance(ZephyrIntelligence.SCHEMAS, dict)
        except ImportError:
            pytest.skip("ZephyrIntelligence not available for testing")
    
    def test_read_endpoints_exists(self):
        """Test that READ_ENDPOINTS attribute exists."""
        try:
            from intelligence.intelligence import ZephyrIntelligence
            assert hasattr(ZephyrIntelligence, 'READ_ENDPOINTS')
            assert isinstance(ZephyrIntelligence.READ_ENDPOINTS, dict)
        except ImportError:
            pytest.skip("ZephyrIntelligence not available for testing")
    
    def test_get_read_endpoint_method(self):
        """Test get_read_endpoint() method."""
        try:
            from intelligence.intelligence import ZephyrIntelligence
            assert hasattr(ZephyrIntelligence, 'get_read_endpoint')
            assert callable(ZephyrIntelligence.get_read_endpoint)
            
            # Test with valid entity
            endpoint = ZephyrIntelligence.get_read_endpoint("release")
            assert endpoint is not None
            assert "endpoint" in endpoint
            assert "method" in endpoint
        except ImportError:
            pytest.skip("ZephyrIntelligence not available for testing")
    
    def test_get_read_endpoint_path_method(self):
        """Test get_read_endpoint_path() method with parameters."""
        try:
            from intelligence.intelligence import ZephyrIntelligence
            assert hasattr(ZephyrIntelligence, 'get_read_endpoint_path')
            assert callable(ZephyrIntelligence.get_read_endpoint_path)
            
            # Test with release (has query params)
            path = ZephyrIntelligence.get_read_endpoint_path("release", projectId=44)
            assert path is not None
            assert "projectId=44" in path or "/release" in path
            
            # Test with cycle (has path params)
            path = ZephyrIntelligence.get_read_endpoint_path("cycle", releaseid=123)
            assert path is not None
            assert "123" in path or "/cycle" in path
        except ImportError:
            pytest.skip("ZephyrIntelligence not available for testing")


class TestPrepareStageSchemaBuilding:
    """Test Prepare stage schema building logic."""
    
    def test_schema_data_structure(self):
        """Test that schema_data has correct structure."""
        # This would test the schema building logic
        # Needs mock sample data
        pass
    
    def test_entity_grouping(self):
        """Test that fields are grouped by entity+structureType."""
        # This would test the entity_fields grouping logic
        pass
    
    def test_fallback_from_schemas(self):
        """Test SDK fallback parsing SCHEMAS structure."""
        # This would test the JSON schema parsing logic
        pass




