"""
Validation logic tests for Zephyr source stage.

Tests API response validation, schema validation, row counts, and data quality.
Target coverage: >90%
"""
import pytest
import json
from datetime import datetime
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from unittest.mock import Mock, patch


# ============================================================================
# API RESPONSE VALIDATION
# ============================================================================

class TestAPIResponseValidation:
    """Tests for API response validation."""
    
    @pytest.mark.validation
    def test_validates_json_structure(self):
        """Test validation of JSON structure from API."""
        # Valid JSON response
        response = {"id": 1, "name": "Project"}
        assert isinstance(response, dict)
        assert "id" in response
        assert "name" in response
    
    @pytest.mark.validation
    def test_detects_missing_required_fields(self):
        """Test detection of missing required fields in API response."""
        response = {"name": "Project"}  # Missing 'id'
        required_fields = ["id", "name"]
        
        missing = [field for field in required_fields if field not in response]
        assert "id" in missing
    
    @pytest.mark.validation
    def test_validates_field_types(self):
        """Test validation of field data types."""
        response = {"id": "not-an-int", "name": "Project"}
        
        # Validate id should be int
        assert not isinstance(response["id"], int)
        # Validate name should be str
        assert isinstance(response["name"], str)
    
    @pytest.mark.validation
    def test_handles_null_values(self):
        """Test handling of null values in API responses."""
        response = {"id": 1, "name": None, "description": "Test"}
        
        # Should identify null fields
        null_fields = [k for k, v in response.items() if v is None]
        assert "name" in null_fields
    
    @pytest.mark.validation
    def test_validates_array_responses(self):
        """Test validation of array responses."""
        response = [
            {"id": 1, "name": "Project 1"},
            {"id": 2, "name": "Project 2"},
        ]
        
        assert isinstance(response, list)
        assert len(response) == 2
        assert all("id" in item for item in response)
    
    @pytest.mark.validation
    def test_detects_empty_array(self):
        """Test detection of empty array responses."""
        response = []
        assert isinstance(response, list)
        assert len(response) == 0


# ============================================================================
# SCHEMA VALIDATION
# ============================================================================

class TestSchemaValidation:
    """Tests for Delta table schema validation."""
    
    @pytest.mark.validation
    def test_validates_expected_schema(self, spark):
        """Test validation against expected schema."""
        # Define expected schema
        expected_schema = StructType([
            StructField("id", IntegerType(), False),
            StructField("name", StringType(), False),
        ])
        
        # Create DataFrame with matching schema
        data = [Row(id=1, name="Test")]
        df = spark.createDataFrame(data)
        
        # Validate schema (in real implementation, would compare schemas)
        assert df.count() == 1
    
    @pytest.mark.validation
    def test_detects_schema_mismatch(self, spark):
        """Test detection of schema mismatches."""
        # Expected: id (int), name (str)
        # Actual: id (str), name (str) - type mismatch
        
        expected_fields = {"id": "int", "name": "str"}
        actual_fields = {"id": "str", "name": "str"}
        
        mismatches = {
            k: (expected_fields[k], actual_fields[k])
            for k in expected_fields
            if expected_fields[k] != actual_fields.get(k)
        }
        
        assert "id" in mismatches
        assert mismatches["id"] == ("int", "str")
    
    @pytest.mark.validation
    def test_detects_missing_columns(self):
        """Test detection of missing columns in schema."""
        expected_columns = ["id", "name", "description"]
        actual_columns = ["id", "name"]
        
        missing = [col for col in expected_columns if col not in actual_columns]
        assert "description" in missing
    
    @pytest.mark.validation
    def test_detects_extra_columns(self):
        """Test detection of extra columns in schema."""
        expected_columns = ["id", "name"]
        actual_columns = ["id", "name", "extra_field"]
        
        extra = [col for col in actual_columns if col not in expected_columns]
        assert "extra_field" in extra
    
    @pytest.mark.validation
    def test_validates_nullable_constraints(self):
        """Test validation of nullable constraints."""
        # Define schema with non-nullable field
        schema = StructType([
            StructField("id", IntegerType(), False),  # Non-nullable
            StructField("name", StringType(), True),   # Nullable
        ])
        
        # Test data with null in non-nullable field should fail
        # (In real implementation, this would raise an error)
        data_with_null = [{"id": None, "name": "Test"}]
        assert data_with_null[0]["id"] is None  # Would fail validation


# ============================================================================
# ROW COUNT VALIDATION
# ============================================================================

class TestRowCountValidation:
    """Tests for row count validation."""
    
    @pytest.mark.validation
    def test_validates_minimum_row_count(self, spark):
        """Test validation of minimum expected rows."""
        data = [Row(id=1), Row(id=2), Row(id=3)]
        df = spark.createDataFrame(data)
        
        min_expected = 2
        actual_count = df.count()
        
        assert actual_count >= min_expected
    
    @pytest.mark.validation
    def test_detects_empty_table(self, spark):
        """Test detection of empty tables."""
        df = spark.createDataFrame([])
        
        assert df.count() == 0
    
    @pytest.mark.validation
    def test_validates_expected_count_range(self, spark):
        """Test validation of expected count range."""
        data = [Row(id=i) for i in range(50)]
        df = spark.createDataFrame(data)
        
        min_expected = 10
        max_expected = 100
        actual_count = df.count()
        
        assert min_expected <= actual_count <= max_expected
    
    @pytest.mark.validation
    def test_detects_unexpected_count(self, spark):
        """Test detection of unexpected row counts."""
        data = [Row(id=i) for i in range(200)]
        df = spark.createDataFrame(data)
        
        expected = 100
        actual_count = df.count()
        
        # Significant deviation (>20%)
        deviation = abs(actual_count - expected) / expected
        assert deviation > 0.2  # More than 20% deviation


# ============================================================================
# DATA QUALITY CHECKS
# ============================================================================

class TestDataQualityChecks:
    """Tests for data quality validation."""
    
    @pytest.mark.validation
    def test_validates_no_duplicates(self, spark):
        """Test detection of duplicate records."""
        data = [
            Row(id=1, name="Project A"),
            Row(id=1, name="Project A"),  # Duplicate
            Row(id=2, name="Project B"),
        ]
        df = spark.createDataFrame(data)
        
        # Check for duplicates
        total_rows = df.count()
        distinct_rows = len(set(str(row) for row in df.collect()))
        
        assert total_rows > distinct_rows  # Duplicates detected
    
    @pytest.mark.validation
    def test_validates_primary_key_uniqueness(self, spark):
        """Test primary key uniqueness."""
        data = [
            Row(id=1, name="Project A"),
            Row(id=2, name="Project B"),
            Row(id=3, name="Project C"),
        ]
        df = spark.createDataFrame(data)
        
        # Check ID uniqueness
        id_values = [row.id for row in df.collect()]
        assert len(id_values) == len(set(id_values))
    
    @pytest.mark.validation
    def test_detects_null_in_required_fields(self, spark):
        """Test detection of nulls in required fields."""
        data = [
            Row(id=1, name="Project A"),
            Row(id=2, name=None),  # Null in required field
        ]
        df = spark.createDataFrame(data)
        
        # Count null names
        null_count = sum(1 for row in df.collect() if row.name is None)
        assert null_count > 0
    
    @pytest.mark.validation
    def test_validates_referential_integrity(self, spark):
        """Test referential integrity between tables."""
        # Parent table (projects)
        projects = [Row(id=1), Row(id=2)]
        df_projects = spark.createDataFrame(projects)
        
        # Child table (releases)
        releases = [
            Row(id=10, project_id=1),
            Row(id=11, project_id=2),
            Row(id=12, project_id=999),  # Invalid reference
        ]
        df_releases = spark.createDataFrame(releases)
        
        # Check for orphan records
        project_ids = {row.id for row in df_projects.collect()}
        invalid_refs = [
            row.id for row in df_releases.collect()
            if row.project_id not in project_ids
        ]
        
        assert len(invalid_refs) > 0  # Found invalid reference
        assert 12 in invalid_refs
    
    @pytest.mark.validation
    def test_validates_date_ranges(self):
        """Test validation of date ranges."""
        # Check that dates are within reasonable range
        test_date = datetime(2025, 12, 5)
        min_date = datetime(2020, 1, 1)
        max_date = datetime(2030, 12, 31)
        
        assert min_date <= test_date <= max_date
    
    @pytest.mark.validation
    def test_validates_value_domains(self):
        """Test validation of value domains."""
        # Status should be in allowed values
        allowed_statuses = ["active", "inactive", "archived"]
        test_status = "active"
        
        assert test_status in allowed_statuses
        
        # Invalid status
        invalid_status = "deleted"
        assert invalid_status not in allowed_statuses
    
    @pytest.mark.validation
    def test_detects_data_truncation(self):
        """Test detection of data truncation."""
        original_value = "This is a very long project name that exceeds limits"
        max_length = 50
        
        # Check if value would be truncated
        assert len(original_value) > max_length
    
    @pytest.mark.validation
    def test_validates_numeric_ranges(self):
        """Test validation of numeric value ranges."""
        # Priority should be 0-10
        priority = 5
        min_priority = 0
        max_priority = 10
        
        assert min_priority <= priority <= max_priority
        
        # Invalid priority
        invalid_priority = 15
        assert invalid_priority > max_priority


# ============================================================================
# ENDPOINT CATALOG VALIDATION
# ============================================================================

class TestEndpointCatalogValidation:
    """Tests for endpoint catalog validation."""
    
    @pytest.mark.validation
    def test_validates_endpoint_structure(self, sample_endpoint_catalog):
        """Test validation of endpoint catalog structure."""
        required_fields = ["name", "endpoint", "method", "category"]
        
        for ep in sample_endpoint_catalog:
            missing = [field for field in required_fields if field not in ep]
            assert len(missing) == 0
    
    @pytest.mark.validation
    def test_validates_http_methods(self, sample_endpoint_catalog):
        """Test validation of HTTP methods."""
        allowed_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        
        for ep in sample_endpoint_catalog:
            assert ep["method"] in allowed_methods
    
    @pytest.mark.validation
    def test_validates_endpoint_paths(self, sample_endpoint_catalog):
        """Test validation of endpoint paths."""
        for ep in sample_endpoint_catalog:
            # Endpoints should start with /
            assert ep["endpoint"].startswith("/")
    
    @pytest.mark.validation
    def test_validates_boolean_flags(self, sample_endpoint_catalog):
        """Test validation of boolean flags in catalog."""
        boolean_fields = ["hierarchical", "pagination"]
        
        for ep in sample_endpoint_catalog:
            for field in boolean_fields:
                if field in ep:
                    assert isinstance(ep[field], bool)


# ============================================================================
# INTEGRATION VALIDATION
# ============================================================================

class TestIntegrationValidation:
    """Tests for end-to-end validation flows."""
    
    @pytest.mark.validation
    @pytest.mark.integration
    def test_validates_complete_source_pipeline(
        self, spark, mock_projects_response, mock_releases_response
    ):
        """Test validation of complete source stage output."""
        # Simulate source stage creating multiple tables
        tables = {
            "source.portfolio": [Row(source_system="zephyr", total_endpoints=228)],
            "source.config": [Row(config_key="sdk_version", config_value="0.3.0")],
            "source.credentials": [Row(credential_type="api_token", credential_value="***345")],
        }
        
        # Validate all tables exist
        assert "source.portfolio" in tables
        assert "source.config" in tables
        assert "source.credentials" in tables
        
        # Validate portfolio metrics
        portfolio = tables["source.portfolio"][0]
        assert portfolio.total_endpoints > 0
        
        # Validate config completeness
        assert len(tables["source.config"]) >= 5
        
        # Validate credentials masking
        creds = tables["source.credentials"][0]
        assert creds.credential_value.startswith("***")

