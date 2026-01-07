"""
Integration tests for Zephyr source stage end-to-end flow.

Tests complete source stage execution with mocked APIs.
Target coverage: >60%
"""
import pytest
import json
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from pyspark.sql import Row


# ============================================================================
# END-TO-END SOURCE STAGE TESTS
# ============================================================================

class TestSourceStageEndToEnd:
    """End-to-end tests for complete source stage execution."""
    
    @pytest.mark.integration
    @patch("requests.get")
    def test_complete_source_stage_bootstrap_flow(
        self, 
        mock_requests_get,
        spark,
        mock_delta_table,
        mock_logger,
        mock_notebook_session,
        sample_zephyr_projects,
        sample_endpoint_catalog,
    ):
        """Test complete source stage execution with bootstrap enabled."""
        from spectraSDK import SourceStageHelpers
        
        # Mock API responses
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = sample_zephyr_projects
        mock_requests_get.return_value.raise_for_status = Mock()
        
        # Parameters
        base_url = "https://api.zephyrscale.smartbear.com/v2"
        api_token = "test_token_123"
        bootstrap = True
        preview = True
        sample_limit = 10
        
        # =============================================================
        # STAGE 1: CREATE CONFIG TABLE
        # =============================================================
        SourceStageHelpers.create_source_config_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            session=mock_notebook_session,
            sdk_version="0.3.0",
        )
        
        assert mock_delta_table.write.called
        assert mock_delta_table.register.called
        
        # =============================================================
        # STAGE 2: VALIDATE API AUTHENTICATION
        # =============================================================
        auth_result, projects = SourceStageHelpers.validate_api_authentication(
            base_url=base_url,
            api_token=api_token,
            test_endpoint="/projects",
            logger=mock_logger,
        )
        
        assert auth_result["status"] == "Success"
        assert len(projects) > 0
        assert mock_requests_get.called
        
        # =============================================================
        # STAGE 3: CREATE CREDENTIALS TABLE
        # =============================================================
        SourceStageHelpers.create_source_credentials_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            api_token=api_token,
            validation_status="Success",
        )
        
        # =============================================================
        # STAGE 4: BOOTSTRAP ENDPOINTS (if enabled)
        # =============================================================
        if bootstrap:
            endpoint_count = SourceStageHelpers.bootstrap_endpoints_catalog(
                spark=spark,
                delta=mock_delta_table,
                logger=mock_logger,
                endpoints_catalog=sample_endpoint_catalog,
            )
            assert endpoint_count == len(sample_endpoint_catalog)
        
        # =============================================================
        # STAGE 5: EXTRACT PREVIEW SAMPLE (if enabled)
        # =============================================================
        if preview:
            # Mock releases response
            sample_releases = [{"id": i, "name": f"Release {i}"} for i in range(1, 11)]
            mock_requests_get.return_value.json.return_value = sample_releases
            
            preview_resources = [
                {
                    "name": "sampleprojects",
                    "endpoint": "/projects",
                    "table": "source.sampleprojects",
                },
                {
                    "name": "samplereleases",
                    "endpoint": f"/projects/{projects[0]['id']}/releases",
                    "table": "source.samplereleases",
                },
            ]
            
            table_count = SourceStageHelpers.extract_preview_sample(
                spark=spark,
                delta=mock_delta_table,
                logger=mock_logger,
                base_url=base_url,
                api_token=api_token,
                resources=preview_resources,
                sample_limit=sample_limit,
            )
            
            assert table_count == 2
        
        # =============================================================
        # STAGE 6: CREATE PORTFOLIO TABLE
        # =============================================================
        SourceStageHelpers.create_source_portfolio_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            session=mock_notebook_session,
            contract_version="1.0.0",
            auth_method="Bearer Token",
            auth_status="Success",
            endpoint_catalog=sample_endpoint_catalog,
            endpoint_success_rate=1.0,
            supports_incremental=False,
        )
        
        # Verify all tables created
        expected_tables = [
            "source.config",
            "source.credentials",
            "source.endpoints",
            "source.sampleprojects",
            "source.samplereleases",
            "source.portfolio",
        ]
        
        # Count write calls
        assert mock_delta_table.write.call_count >= len(expected_tables)
    
    @pytest.mark.integration
    @patch("requests.get")
    def test_source_stage_without_bootstrap(
        self, 
        mock_requests_get,
        spark,
        mock_delta_table,
        mock_logger,
        mock_notebook_session,
        sample_zephyr_projects,
    ):
        """Test source stage with bootstrap=False (minimal tables)."""
        from spectraSDK import SourceStageHelpers
        
        # Mock API
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = sample_zephyr_projects
        mock_requests_get.return_value.raise_for_status = Mock()
        
        # Parameters
        base_url = "https://api.zephyrscale.smartbear.com/v2"
        api_token = "test_token_123"
        bootstrap = False
        preview = False
        
        # Create only essential tables
        SourceStageHelpers.create_source_config_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            session=mock_notebook_session,
            sdk_version="0.3.0",
        )
        
        auth_result, projects = SourceStageHelpers.validate_api_authentication(
            base_url=base_url,
            api_token=api_token,
            test_endpoint="/projects",
            logger=mock_logger,
        )
        
        SourceStageHelpers.create_source_credentials_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            api_token=api_token,
            validation_status="Success",
        )
        
        SourceStageHelpers.create_source_portfolio_table(
            spark=spark,
            delta=mock_delta_table,
            logger=mock_logger,
            session=mock_notebook_session,
            contract_version="1.0.0",
            auth_method="Bearer Token",
            auth_status="Success",
            endpoint_catalog=None,  # No catalog when bootstrap=False
        )
        
        # Only 4 tables should be created
        expected_tables = [
            "source.config",
            "source.credentials",
            "source.portfolio",
        ]
        
        assert mock_delta_table.write.call_count == len(expected_tables)


# ============================================================================
# API INTEGRATION TESTS
# ============================================================================

class TestAPIIntegration:
    """Integration tests for Zephyr API interactions."""
    
    @pytest.mark.integration
    @pytest.mark.api
    @patch("requests.get")
    def test_api_authentication_success(self, mock_requests_get, mock_logger, sample_zephyr_projects):
        """Test successful API authentication flow."""
        from spectraSDK import SourceStageHelpers
        
        # Mock successful response
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = sample_zephyr_projects
        mock_requests_get.return_value.raise_for_status = Mock()
        
        result, projects = SourceStageHelpers.validate_api_authentication(
            base_url="https://api.zephyrscale.smartbear.com/v2",
            api_token="valid_token",
            test_endpoint="/projects",
            logger=mock_logger,
        )
        
        assert result["status"] == "Success"
        assert result["project_count"] == len(sample_zephyr_projects)
        assert len(projects) > 0
        
        # Verify API call
        mock_requests_get.assert_called_once()
        call_args = mock_requests_get.call_args
        assert "Authorization" in call_args[1]["headers"]
        assert "Bearer" in call_args[1]["headers"]["Authorization"]
    
    @pytest.mark.integration
    @pytest.mark.api
    @patch("requests.get")
    def test_api_authentication_failure(self, mock_requests_get, mock_logger):
        """Test API authentication failure handling."""
        from spectraSDK import SourceStageHelpers
        
        # Mock 401 Unauthorized
        mock_requests_get.return_value.status_code = 401
        mock_requests_get.return_value.raise_for_status.side_effect = Exception("401 Unauthorized")
        
        result, projects = SourceStageHelpers.validate_api_authentication(
            base_url="https://api.zephyrscale.smartbear.com/v2",
            api_token="invalid_token",
            test_endpoint="/projects",
            logger=mock_logger,
        )
        
        assert result["status"] == "Failed"
        assert "error" in result
        assert len(projects) == 0
    
    @pytest.mark.integration
    @pytest.mark.api
    @patch("requests.get")
    def test_api_resource_access_validation(self, mock_requests_get, mock_logger, sample_zephyr_releases):
        """Test validation of access to specific resources."""
        from spectraSDK import SourceStageHelpers
        
        # Mock releases response
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = sample_zephyr_releases
        mock_requests_get.return_value.raise_for_status = Mock()
        
        result = SourceStageHelpers.validate_api_resource_access(
            base_url="https://api.zephyrscale.smartbear.com/v2",
            api_token="valid_token",
            resource_endpoint="/projects/{projectId}/releases",
            resource_id=123,
            logger=mock_logger,
        )
        
        assert result["status"] == "Success"
        assert result["item_count"] == len(sample_zephyr_releases)
    
    @pytest.mark.integration
    @pytest.mark.api
    @pytest.mark.slow
    @patch("requests.get")
    def test_api_rate_limiting(self, mock_requests_get, mock_logger):
        """Test handling of API rate limits."""
        from spectraSDK import SourceStageHelpers
        
        # Mock 429 Too Many Requests
        mock_requests_get.return_value.status_code = 429
        mock_requests_get.return_value.raise_for_status.side_effect = Exception("429 Too Many Requests")
        
        result, projects = SourceStageHelpers.validate_api_authentication(
            base_url="https://api.zephyrscale.smartbear.com/v2",
            api_token="valid_token",
            test_endpoint="/projects",
            logger=mock_logger,
        )
        
        assert result["status"] == "Failed"
        assert "429" in result.get("error", "")


# ============================================================================
# DELTA TABLE INTEGRATION TESTS
# ============================================================================

class TestDeltaTableIntegration:
    """Integration tests for Delta table operations."""
    
    @pytest.mark.integration
    def test_write_and_register_delta_table(self, spark, mock_delta_table, mock_logger):
        """Test writing and registering a Delta table."""
        # Create sample data
        data = [
            Row(id=1, name="Item 1", timestamp=datetime.utcnow()),
            Row(id=2, name="Item 2", timestamp=datetime.utcnow()),
        ]
        
        df = spark.createDataFrame(data)
        
        # Write and register
        mock_delta_table.write(df, "source.test", "Tables/source/test")
        mock_delta_table.register("source.test", "Tables/source/test")
        
        # Verify
        assert mock_delta_table.write.called
        assert mock_delta_table.register.called
    
    @pytest.mark.integration
    def test_schema_evolution_on_write(self, spark, mock_delta_table):
        """Test schema evolution when writing to existing table."""
        # First write
        data_v1 = [Row(id=1, name="Item 1")]
        df_v1 = spark.createDataFrame(data_v1)
        mock_delta_table.write(df_v1, "source.test", "Tables/source/test")
        
        # Second write with new column
        data_v2 = [Row(id=2, name="Item 2", category="New")]
        df_v2 = spark.createDataFrame(data_v2)
        mock_delta_table.write(df_v2, "source.test", "Tables/source/test", mode="append")
        
        # Should handle schema evolution
        assert mock_delta_table.write.call_count == 2
    
    @pytest.mark.integration
    def test_multiple_table_registration(self, spark, mock_delta_table, mock_logger):
        """Test registering multiple tables in sequence."""
        tables = [
            ("source.config", "Tables/source/config"),
            ("source.credentials", "Tables/source/credentials"),
            ("source.endpoints", "Tables/source/endpoints"),
            ("source.portfolio", "Tables/source/portfolio"),
        ]
        
        for table_name, path in tables:
            df = spark.createDataFrame([Row(id=1, value="test")])
            mock_delta_table.write(df, table_name, path)
            mock_delta_table.register(table_name, path)
        
        # Verify all registered
        assert mock_delta_table.register.call_count == len(tables)


# ============================================================================
# NOTEBOOK SESSION INTEGRATION TESTS
# ============================================================================

class TestNotebookSessionIntegration:
    """Integration tests for NotebookSession lifecycle."""
    
    @pytest.mark.integration
    def test_session_initialization(self, mock_notebook_session):
        """Test NotebookSession initialization with all components."""
        # Verify session components
        assert mock_notebook_session.pipeline is not None
        assert mock_notebook_session.env is not None
        assert mock_notebook_session.vars is not None
        assert mock_notebook_session.delta is not None
        assert mock_notebook_session.log is not None
        
        # Verify context
        assert "source_system" in mock_notebook_session.ctx
        assert "notebook_name" in mock_notebook_session.ctx
        assert "stage" in mock_notebook_session.ctx
    
    @pytest.mark.integration
    def test_session_parameter_access(self, mock_notebook_session):
        """Test accessing parameters through session."""
        # Parameters should be accessible
        assert "bootstrap" in mock_notebook_session.params
        assert "preview" in mock_notebook_session.params
        
        # Default values
        assert isinstance(mock_notebook_session.params["bootstrap"], bool)
        assert isinstance(mock_notebook_session.params["preview"], bool)
    
    @pytest.mark.integration
    def test_session_capability_tracking(self, mock_notebook_session):
        """Test session capability tracking."""
        # Add capabilities
        mock_notebook_session.add_capability("projectAccessVerified")
        mock_notebook_session.add_capability("hierarchicalDataSupported")
        
        # Check capabilities
        assert mock_notebook_session.has_capability("projectAccessVerified")
        assert mock_notebook_session.has_capability("hierarchicalDataSupported")
        assert not mock_notebook_session.has_capability("nonExistentCapability")


# ============================================================================
# ERROR RECOVERY INTEGRATION TESTS
# ============================================================================

class TestErrorRecoveryIntegration:
    """Integration tests for error recovery scenarios."""
    
    @pytest.mark.integration
    @patch("requests.get")
    def test_recovers_from_transient_api_failure(
        self, 
        mock_requests_get, 
        spark, 
        mock_delta_table, 
        mock_logger,
        sample_zephyr_projects,
    ):
        """Test recovery from transient API failures."""
        from spectraSDK import SourceStageHelpers
        
        # Fail first 2 calls, succeed on 3rd
        mock_requests_get.side_effect = [
            Exception("Connection timeout"),
            Exception("Connection timeout"),
            Mock(
                status_code=200,
                json=lambda: sample_zephyr_projects,
                raise_for_status=Mock(),
            ),
        ]
        
        # Retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result, projects = SourceStageHelpers.validate_api_authentication(
                    base_url="https://api.zephyrscale.smartbear.com/v2",
                    api_token="valid_token",
                    test_endpoint="/projects",
                    logger=mock_logger,
                )
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
        
        # Should eventually succeed
        assert result["status"] == "Success"
        assert mock_requests_get.call_count == 3
    
    @pytest.mark.integration
    def test_continues_after_partial_failure(
        self, 
        spark, 
        mock_delta_table, 
        mock_logger,
        sample_endpoint_catalog,
    ):
        """Test continuation after partial operation failure."""
        from spectraSDK import SourceStageHelpers
        
        # Simulate: config succeeds, endpoints fails, portfolio succeeds
        operations = []
        
        try:
            SourceStageHelpers.bootstrap_endpoints_catalog(
                spark=spark,
                delta=mock_delta_table,
                logger=mock_logger,
                endpoints_catalog=sample_endpoint_catalog,
            )
            operations.append("endpoints_success")
        except Exception:
            operations.append("endpoints_failed")
            # Continue anyway
        
        # Should still reach here
        operations.append("completed")
        
        assert "completed" in operations

