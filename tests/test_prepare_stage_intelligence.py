"""
Test ZephyrIntelligence structure and methods.

Tests:
- READ_ENDPOINTS structure
- get_read_endpoint() method
- get_read_endpoint_path() with path params
- get_read_endpoint_path() with query params
- Missing entity handling
"""

import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import intelligence class
from intelligence.intelligence import ZephyrIntelligence


class TestZephyrIntelligenceStructure:
    """Test ZephyrIntelligence class structure."""
    
    def test_read_endpoints_exists(self):
        """Test that READ_ENDPOINTS dictionary exists."""
        assert hasattr(ZephyrIntelligence, 'READ_ENDPOINTS')
        assert isinstance(ZephyrIntelligence.READ_ENDPOINTS, dict)
        assert len(ZephyrIntelligence.READ_ENDPOINTS) > 0
    
    def test_read_endpoints_structure(self):
        """Test READ_ENDPOINTS structure for each entity."""
        for entity, endpoint_info in ZephyrIntelligence.READ_ENDPOINTS.items():
            assert "endpoint" in endpoint_info, f"{entity} missing 'endpoint'"
            assert "method" in endpoint_info, f"{entity} missing 'method'"
            assert endpoint_info["method"] == "GET", f"{entity} should be GET"
            assert "read_only" in endpoint_info, f"{entity} missing 'read_only'"
            assert endpoint_info["read_only"] is True, f"{entity} should be read_only"
    
    def test_read_endpoints_entities(self):
        """Test that required entities are in READ_ENDPOINTS."""
        required_entities = ["project", "release", "cycle"]
        for entity in required_entities:
            assert entity in ZephyrIntelligence.READ_ENDPOINTS, f"{entity} missing from READ_ENDPOINTS"


class TestZephyrIntelligenceMethods:
    """Test ZephyrIntelligence class methods."""
    
    def test_get_read_endpoint_exists(self):
        """Test that get_read_endpoint() method exists."""
        assert hasattr(ZephyrIntelligence, 'get_read_endpoint')
        assert callable(ZephyrIntelligence.get_read_endpoint)
    
    def test_get_read_endpoint_path_exists(self):
        """Test that get_read_endpoint_path() method exists."""
        assert hasattr(ZephyrIntelligence, 'get_read_endpoint_path')
        assert callable(ZephyrIntelligence.get_read_endpoint_path)
    
    def test_get_read_endpoint_valid_entity(self):
        """Test get_read_endpoint() with valid entity."""
        endpoint = ZephyrIntelligence.get_read_endpoint("release")
        assert endpoint is not None
        assert "endpoint" in endpoint
        assert endpoint["method"] == "GET"
    
    def test_get_read_endpoint_invalid_entity(self):
        """Test get_read_endpoint() with invalid entity."""
        endpoint = ZephyrIntelligence.get_read_endpoint("nonexistent")
        assert endpoint is None
    
    def test_get_read_endpoint_path_release_with_query(self):
        """Test get_read_endpoint_path() for release with query param."""
        path = ZephyrIntelligence.get_read_endpoint_path("release", projectId=44)
        assert path is not None
        assert "/release" in path
        assert "projectId=44" in path
    
    def test_get_read_endpoint_path_cycle_with_path_param(self):
        """Test get_read_endpoint_path() for cycle with path param."""
        path = ZephyrIntelligence.get_read_endpoint_path("cycle", releaseid=112)
        assert path is not None
        assert "/cycle/release" in path
        assert "112" in path
        assert "{releaseid}" not in path  # Should be replaced
    
    def test_get_read_endpoint_path_missing_params(self):
        """Test get_read_endpoint_path() with missing required params."""
        # Cycle requires releaseid
        path = ZephyrIntelligence.get_read_endpoint_path("cycle")
        # Should still return path template (or None if validation)
        # Current implementation returns path with unreplaced params
        assert path is not None
    
    def test_get_read_endpoint_path_invalid_entity(self):
        """Test get_read_endpoint_path() with invalid entity."""
        path = ZephyrIntelligence.get_read_endpoint_path("nonexistent", projectId=44)
        assert path is None
    
    def test_get_read_endpoint_path_project(self):
        """Test get_read_endpoint_path() for project (no params)."""
        path = ZephyrIntelligence.get_read_endpoint_path("project")
        assert path is not None
        assert "/project" in path


class TestZephyrIntelligenceIntegration:
    """Test ZephyrIntelligence integration scenarios."""
    
    def test_release_endpoint_full_flow(self):
        """Test full flow for release endpoint."""
        # Get endpoint info
        endpoint_info = ZephyrIntelligence.get_read_endpoint("release")
        assert endpoint_info is not None
        
        # Build path with params
        path = ZephyrIntelligence.get_read_endpoint_path("release", projectId=44)
        assert path is not None
        
        # Verify path structure
        assert path.startswith("/release")
        assert "projectId=44" in path
    
    def test_cycle_endpoint_full_flow(self):
        """Test full flow for cycle endpoint."""
        # Get endpoint info
        endpoint_info = ZephyrIntelligence.get_read_endpoint("cycle")
        assert endpoint_info is not None
        
        # Build path with params
        path = ZephyrIntelligence.get_read_endpoint_path("cycle", releaseid=112)
        assert path is not None
        
        # Verify path structure
        assert "/cycle/release" in path
        assert "112" in path
        assert "{releaseid}" not in path  # Should be replaced
    
    def test_multiple_query_params(self):
        """Test endpoint with multiple query params (if any)."""
        # Test release endpoint (has projectId)
        path = ZephyrIntelligence.get_read_endpoint_path("release", projectId=44)
        assert path is not None
        assert "projectId=44" in path


class TestZephyrIntelligenceEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_params(self):
        """Test with empty params dict."""
        path = ZephyrIntelligence.get_read_endpoint_path("project")
        assert path is not None  # Project doesn't need params
    
    def test_extra_params(self):
        """Test with extra params not in endpoint definition."""
        # Should ignore extra params
        path = ZephyrIntelligence.get_read_endpoint_path("project", projectId=44, extraParam=123)
        assert path is not None
        # Project endpoint doesn't use projectId, so it shouldn't appear
        assert "projectId" not in path or "projectId=44" in path
    
    def test_none_values(self):
        """Test with None values."""
        path = ZephyrIntelligence.get_read_endpoint_path("release", projectId=None)
        # Should handle None gracefully
        assert path is not None
    
    def test_path_param_substitution(self):
        """Test that path params are correctly substituted."""
        path = ZephyrIntelligence.get_read_endpoint_path("cycle", releaseid=112)
        assert path is not None
        # Verify {releaseid} is replaced with actual value
        assert "{releaseid}" not in path
        assert "112" in path

