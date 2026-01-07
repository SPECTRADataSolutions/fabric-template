"""
Unit tests for SourceStageHelpers SDK class.

Tests all static methods in the SourceStageHelpers class from spectraSDK.
Target coverage: >80%
"""
import pytest
import json
from datetime import datetime
from pyspark.sql import Row
from unittest.mock import Mock, patch, call
import requests


# ============================================================================
# PORTFOLIO TABLE TESTS
# ============================================================================

class TestCreateSourcePortfolioTable:
    """Tests for create_source_portfolio_table()"""
    
    @pytest.mark.unit
    def test_creates_portfolio_with_full_metadata(
        self, spark, mock_delta_table, mock_logger, mock_notebook_session, sample_endpoint_catalog
    ):
        """Test portfolio table creation with complete metadata."""
        from spectraSDK import SourceStageHelpers
        
        SourceStageHelpers.create_source_portfolio_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            session=mock_notebook_session,
            contract_version="1.0.0",
            auth_method="Bearer Token",
            auth_status="Success",
            endpoint_catalog=sample_endpoint_catalog,
            endpoint_success_rate=0.98,
            supports_incremental=False,
        )
        
        # Verify Delta write was called
        assert mock_delta_table.write.called
        assert mock_delta_table.register.called
        
        # Verify DataFrame creation
        assert spark.createDataFrame.called
        df_args = spark.createDataFrame.call_args[0][0]
        assert len(df_args) == 1  # Single row
        
        row = df_args[0]
        assert row.source_system == "zephyr"
        assert row.contract_version == "1.0.0"
        assert row.total_endpoints == 3
        assert row.auth_status == "Success"
    
    @pytest.mark.unit
    def test_handles_missing_endpoint_catalog(
        self, spark, mock_delta_table, mock_logger, mock_notebook_session
    ):
        """Test portfolio table creation without endpoint catalog."""
        from spectraSDK import SourceStageHelpers
        
        SourceStageHelpers.create_source_portfolio_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            session=mock_notebook_session,
            contract_version="1.0.0",
            auth_method="Bearer Token",
            auth_status="Success",
            endpoint_catalog=None,
        )
        
        # Should still create table with zeros
        df_args = spark.createDataFrame.call_args[0][0]
        row = df_args[0]
        assert row.total_endpoints == 0
        assert row.hierarchical_endpoints == 0
    
    @pytest.mark.unit
    def test_preserves_discovery_date_on_update(
        self, spark, mock_delta_table, mock_logger, mock_notebook_session
    ):
        """Test that discovery_date is preserved when updating existing portfolio."""
        from spectraSDK import SourceStageHelpers
        
        # Mock existing portfolio table
        existing_date = datetime(2025, 11, 1).date()
        spark.sql.return_value.first.return_value = Row(discovery_date=existing_date)
        
        SourceStageHelpers.create_source_portfolio_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            session=mock_notebook_session,
            contract_version="1.0.0",
            auth_method="Bearer Token",
            auth_status="Success",
        )
        
        # Verify discovery_date was queried
        assert spark.sql.called
        sql_query = spark.sql.call_args[0][0]
        assert "SELECT discovery_date FROM source.portfolio" in sql_query
    
    @pytest.mark.unit
    def test_calculates_endpoint_categories(
        self, spark, mock_delta_table, mock_logger, mock_notebook_session, sample_endpoint_catalog
    ):
        """Test endpoint category aggregation."""
        from spectraSDK import SourceStageHelpers
        
        SourceStageHelpers.create_source_portfolio_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            session=mock_notebook_session,
            contract_version="1.0.0",
            auth_method="Bearer Token",
            auth_status="Success",
            endpoint_catalog=sample_endpoint_catalog,
        )
        
        df_args = spark.createDataFrame.call_args[0][0]
        row = df_args[0]
        
        # Verify category counts are JSON
        categories = json.loads(row.endpoint_categories)
        assert "projects" in categories
        assert "releases" in categories
        assert "cycles" in categories


# ============================================================================
# CONFIG TABLE TESTS
# ============================================================================

class TestCreateSourceConfigTable:
    """Tests for create_source_config_table()"""
    
    @pytest.mark.unit
    def test_creates_config_with_all_settings(
        self, spark, mock_delta_table, mock_logger, mock_notebook_session
    ):
        """Test config table creation with all runtime settings."""
        from spectraSDK import SourceStageHelpers
        
        SourceStageHelpers.create_source_config_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            session=mock_notebook_session,
            sdk_version="0.3.0",
        )
        
        # Verify DataFrame creation
        assert spark.createDataFrame.called
        df_args = spark.createDataFrame.call_args[0][0]
        
        # Verify all config keys present
        config_keys = [row.config_key for row in df_args]
        expected_keys = [
            "execution_mode",
            "operation_type",
            "notebook_name",
            "stage",
            "sdk_version",
            "bootstrap_enabled",
            "preview_enabled",
        ]
        assert all(key in config_keys for key in expected_keys)
    
    @pytest.mark.unit
    def test_captures_pipeline_vs_interactive_mode(
        self, spark, mock_delta_table, mock_logger, mock_notebook_session
    ):
        """Test config correctly identifies pipeline vs interactive execution."""
        from spectraSDK import SourceStageHelpers
        
        # Test interactive mode
        mock_notebook_session.pipeline.is_active = False
        SourceStageHelpers.create_source_config_table(
            spark, mock_delta_table, mock_logger, mock_notebook_session, "0.3.0"
        )
        
        df_args = spark.createDataFrame.call_args[0][0]
        execution_mode = next(r for r in df_args if r.config_key == "execution_mode")
        assert execution_mode.config_value == "interactive"


# ============================================================================
# CREDENTIALS TABLE TESTS
# ============================================================================

class TestCreateSourceCredentialsTable:
    """Tests for create_source_credentials_table()"""
    
    @pytest.mark.unit
    def test_masks_api_token(self, spark, mock_delta_table, mock_logger):
        """Test that API token is masked correctly."""
        from spectraSDK import SourceStageHelpers
        
        SourceStageHelpers.create_source_credentials_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            api_token="test-token-12345",
            validation_status="Success",
        )
        
        df_args = spark.createDataFrame.call_args[0][0]
        row = df_args[0]
        
        # Should only show last 3 characters
        assert row.credential_value == "***345"
        assert "test-token" not in row.credential_value
    
    @pytest.mark.unit
    def test_handles_short_tokens(self, spark, mock_delta_table, mock_logger):
        """Test token masking with short tokens (<3 chars)."""
        from spectraSDK import SourceStageHelpers
        
        SourceStageHelpers.create_source_credentials_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            api_token="ab",
            validation_status="Success",
        )
        
        df_args = spark.createDataFrame.call_args[0][0]
        row = df_args[0]
        
        # Should show full mask for short tokens
        assert row.credential_value == "***"


# ============================================================================
# API VALIDATION TESTS
# ============================================================================

class TestValidateAPIAuthentication:
    """Tests for validate_api_authentication()"""
    
    @pytest.mark.unit
    @pytest.mark.api
    @patch("requests.get")
    def test_successful_authentication(self, mock_get, mock_logger, mock_projects_response):
        """Test successful API authentication."""
        from spectraSDK import SourceStageHelpers
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = mock_projects_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result, projects = SourceStageHelpers.validate_api_authentication(
            base_url="https://test.com/api",
            api_token="test-token",
            test_endpoint="/project/details",
            logger=mock_logger,
        )
        
        assert result["status"] == "Success"
        assert result["project_count"] == 3
        assert len(projects) == 3
        
        # Verify correct headers used
        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["headers"]["Authorization"] == "Bearer test-token"
    
    @pytest.mark.unit
    @pytest.mark.api
    @patch("requests.get")
    def test_authentication_failure(self, mock_get, mock_logger):
        """Test API authentication failure."""
        from spectraSDK import SourceStageHelpers
        
        # Mock failed response
        mock_get.side_effect = Exception("401 Unauthorized")
        
        result, projects = SourceStageHelpers.validate_api_authentication(
            base_url="https://test.com/api",
            api_token="bad-token",
            test_endpoint="/project/details",
            logger=mock_logger,
        )
        
        assert result["status"] == "Failed"
        assert "error" in result
        assert len(projects) == 0
    
    @pytest.mark.unit
    @pytest.mark.api
    @patch("requests.get")
    def test_respects_timeout(self, mock_get, mock_logger):
        """Test that timeout parameter is respected."""
        from spectraSDK import SourceStageHelpers
        
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        SourceStageHelpers.validate_api_authentication(
            base_url="https://test.com/api",
            api_token="test-token",
            test_endpoint="/project/details",
            logger=mock_logger,
            timeout=30,
        )
        
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["timeout"] == 30


class TestValidateAPIResourceAccess:
    """Tests for validate_api_resource_access()"""
    
    @pytest.mark.unit
    @pytest.mark.api
    @patch("requests.get")
    def test_successful_resource_access(self, mock_get, mock_logger, mock_releases_response):
        """Test successful resource access validation."""
        from spectraSDK import SourceStageHelpers
        
        mock_response = Mock()
        mock_response.json.return_value = mock_releases_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = SourceStageHelpers.validate_api_resource_access(
            base_url="https://test.com/api",
            api_token="test-token",
            resource_endpoint="/release/{projectId}",
            resource_id=1,
            logger=mock_logger,
        )
        
        assert result["status"] == "Success"
        assert result["item_count"] == 2
    
    @pytest.mark.unit
    @pytest.mark.api
    @patch("requests.get")
    def test_resource_access_failure(self, mock_get, mock_logger):
        """Test resource access failure (e.g., 403 Forbidden)."""
        from spectraSDK import SourceStageHelpers
        
        mock_get.side_effect = Exception("403 Forbidden")
        
        result = SourceStageHelpers.validate_api_resource_access(
            base_url="https://test.com/api",
            api_token="test-token",
            resource_endpoint="/release/{projectId}",
            resource_id=999,
            logger=mock_logger,
        )
        
        assert result["status"] == "Failed"
        assert "error" in result


# ============================================================================
# ENDPOINT BOOTSTRAP TESTS
# ============================================================================

class TestBootstrapEndpointsCatalog:
    """Tests for bootstrap_endpoints_catalog()"""
    
    @pytest.mark.unit
    def test_bootstraps_all_endpoints(
        self, spark, mock_delta_table, mock_logger, sample_endpoint_catalog
    ):
        """Test that all endpoints are bootstrapped to Delta."""
        from spectraSDK import SourceStageHelpers
        
        count = SourceStageHelpers.bootstrap_endpoints_catalog(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            endpoints_catalog=sample_endpoint_catalog,
        )
        
        assert count == 3
        assert mock_delta_table.write.called
        assert mock_delta_table.register.called
        
        # Verify correct table name
        write_call = mock_delta_table.write.call_args[0]
        assert write_call[1] == "source.endpoints"
    
    @pytest.mark.unit
    def test_uses_custom_catalog_name(
        self, spark, mock_delta_table, mock_logger, sample_endpoint_catalog
    ):
        """Test that custom catalog name is logged."""
        from spectraSDK import SourceStageHelpers
        
        SourceStageHelpers.bootstrap_endpoints_catalog(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            endpoints_catalog=sample_endpoint_catalog,
            catalog_name="CUSTOM_CATALOG",
        )
        
        # Verify catalog name is logged
        log_calls = [str(call) for call in mock_logger.info.call_args_list]
        assert any("CUSTOM_CATALOG" in str(call) for call in log_calls)


# ============================================================================
# PREVIEW SAMPLE TESTS
# ============================================================================

class TestExtractPreviewSample:
    """Tests for extract_preview_sample()"""
    
    @pytest.mark.unit
    @pytest.mark.api
    @patch("requests.get")
    def test_extracts_sample_for_all_resources(
        self, mock_get, spark, mock_delta_table, mock_logger, mock_projects_response
    ):
        """Test preview sample extraction for multiple resources."""
        from spectraSDK import SourceStageHelpers
        
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = mock_projects_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        resources = [
            {"name": "projects", "endpoint": "/project/details", "table": "source.projects"},
        ]
        
        count = SourceStageHelpers.extract_preview_sample(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            base_url="https://test.com/api",
            api_token="test-token",
            resources=resources,
            sample_limit=10,
        )
        
        assert count == 1
        assert mock_delta_table.write.called
    
    @pytest.mark.unit
    @pytest.mark.api
    @patch("requests.get")
    def test_respects_sample_limit(
        self, mock_get, spark, mock_delta_table, mock_logger, mock_projects_response
    ):
        """Test that sample_limit is enforced."""
        from spectraSDK import SourceStageHelpers
        
        # Mock response with 20 items
        large_response = mock_projects_response * 7  # 21 items
        mock_response = Mock()
        mock_response.json.return_value = large_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        resources = [
            {"name": "projects", "endpoint": "/project/details", "table": "source.projects"},
        ]
        
        SourceStageHelpers.extract_preview_sample(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            base_url="https://test.com/api",
            api_token="test-token",
            resources=resources,
            sample_limit=5,
        )
        
        # Verify only 5 items written (not all 21)
        write_call = mock_delta_table.write.call_args[0]
        df_data = write_call[0].data
        assert len(df_data) == 5
    
    @pytest.mark.unit
    @pytest.mark.api
    @patch("requests.get")
    def test_handles_api_failure_gracefully(
        self, mock_get, spark, mock_delta_table, mock_logger
    ):
        """Test graceful handling of API failures during preview."""
        from spectraSDK import SourceStageHelpers
        
        # Mock API failure
        mock_get.side_effect = Exception("API Error")
        
        resources = [
            {"name": "projects", "endpoint": "/project/details", "table": "source.projects"},
            {"name": "releases", "endpoint": "/release/1", "table": "source.releases"},
        ]
        
        # Should not raise, but return 0 (no tables extracted)
        count = SourceStageHelpers.extract_preview_sample(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            base_url="https://test.com/api",
            api_token="test-token",
            resources=resources,
        )
        
        assert count == 0
        
        # Verify error was logged
        assert mock_logger.error.called

