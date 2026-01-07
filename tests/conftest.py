"""
pytest fixtures for Zephyr source stage tests.

Provides mock Spark sessions, API responses, and test data.
"""
import json
from datetime import datetime
from unittest.mock import Mock, MagicMock
import pytest
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType


# ============================================================================
# SPARK SESSION FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def spark():
    """Mock Spark session for testing."""
    spark = Mock(spec=SparkSession)
    spark.createDataFrame = Mock(side_effect=lambda data, schema=None: MockDataFrame(data))
    spark.sql = Mock(return_value=MockDataFrame([]))
    return spark


@pytest.fixture
def mock_delta_table():
    """Mock DeltaTable class for testing."""
    delta = Mock()
    delta.write = Mock()
    delta.register = Mock()
    delta.merge = Mock()
    delta.optimize = Mock()
    delta.vacuum = Mock()
    return delta


# ============================================================================
# MOCK DATAFRAME
# ============================================================================

class MockDataFrame:
    """Mock DataFrame for testing."""
    
    def __init__(self, data):
        self.data = data
        self._count = len(data) if data else 0
    
    def count(self):
        return self._count
    
    def first(self):
        return self.data[0] if self.data else None
    
    def collect(self):
        return self.data
    
    def write(self):
        return self
    
    def format(self, fmt):
        return self
    
    def mode(self, mode):
        return self
    
    def option(self, key, value):
        return self
    
    def save(self, path):
        pass


# ============================================================================
# API RESPONSE FIXTURES
# ============================================================================

@pytest.fixture
def mock_projects_response():
    """Mock Zephyr projects API response."""
    return [
        {"id": 1, "name": "Project Alpha", "key": "PA"},
        {"id": 2, "name": "Project Beta", "key": "PB"},
        {"id": 3, "name": "Project Gamma", "key": "PG"},
    ]


@pytest.fixture
def mock_releases_response():
    """Mock Zephyr releases API response."""
    return [
        {"id": 10, "name": "Release 1.0", "projectId": 1},
        {"id": 11, "name": "Release 1.1", "projectId": 1},
    ]


@pytest.fixture
def mock_cycles_response():
    """Mock Zephyr cycles API response."""
    return [
        {"id": 100, "name": "Cycle 1", "releaseId": 10},
        {"id": 101, "name": "Cycle 2", "releaseId": 10},
    ]


@pytest.fixture
def mock_api_client(mock_projects_response, mock_releases_response):
    """Mock API client with predefined responses."""
    client = Mock()
    
    def get_side_effect(url, *args, **kwargs):
        response = Mock()
        response.status_code = 200
        response.raise_for_status = Mock()
        
        if "/project/details" in url:
            response.json = Mock(return_value=mock_projects_response)
        elif "/release" in url:
            response.json = Mock(return_value=mock_releases_response)
        else:
            response.json = Mock(return_value=[])
        
        return response
    
    client.get = Mock(side_effect=get_side_effect)
    return client


# ============================================================================
# NOTEBOOK SESSION FIXTURES
# ============================================================================

@pytest.fixture
def mock_notebook_session(spark, mock_delta_table):
    """Mock NotebookSession for testing."""
    session = Mock()
    session.spark = spark
    session.delta = mock_delta_table
    session.log = Mock()
    session.ctx = {
        "source_system": "zephyr",
        "notebook_name": "sourceZephyr",
        "stage": "source",
        "workspace_id": "test-workspace",
        "lakehouse_id": "test-lakehouse",
    }
    session.params = {
        "bootstrap": True,
        "preview": True,
        "sample_limit": 10,
    }
    session.capabilities = {}
    session.has_capability = Mock(return_value=False)
    session.add_capability = Mock()
    session.validate = Mock()
    session.mark_failed = Mock()
    session.record = Mock()
    return session


@pytest.fixture
def mock_logger():
    """Mock SPECTRALogger for testing."""
    logger = Mock()
    logger.info = Mock()
    logger.debug = Mock()
    logger.warning = Mock()
    logger.error = Mock()
    return logger


# ============================================================================
# VARIABLE LIBRARY FIXTURES
# ============================================================================

@pytest.fixture
def mock_variable_library():
    """Mock Variable Library for testing."""
    return {
        "SOURCE_SYSTEM": "zephyr",
        "SOURCE_NAME": "Zephyr Scale",
        "STAGE": "source",
        "NOTEBOOK_NAME": "sourceZephyr",
        "BASE_URL": "https://test.yourzephyr.com/flex/services/rest/latest",
        "API_TOKEN": "test-token-12345",
    }


# ============================================================================
# TEST DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_endpoint_catalog():
    """Sample endpoint catalog for testing."""
    return [
        {
            "name": "Project Details",
            "endpoint": "/project/details",
            "method": "GET",
            "category": "projects",
            "hierarchical": False,
            "pagination": False,
        },
        {
            "name": "Release List",
            "endpoint": "/release/{projectId}",
            "method": "GET",
            "category": "releases",
            "hierarchical": True,
            "pagination": False,
        },
        {
            "name": "Cycle List",
            "endpoint": "/cycle/{releaseId}",
            "method": "GET",
            "category": "cycles",
            "hierarchical": True,
            "pagination": False,
        },
    ]


@pytest.fixture
def sample_portfolio_data():
    """Sample portfolio table data for testing."""
    return Row(
        source_system="zephyr",
        contract_version="1.0.0",
        discovery_date=datetime(2025, 12, 1).date(),
        total_endpoints=228,
        endpoint_categories=json.dumps({"projects": 10, "releases": 8, "cycles": 6}),
        hierarchical_endpoints=50,
        auth_method="Bearer Token",
        auth_status="Success",
        last_auth_check=datetime(2025, 12, 5, 10, 0, 0),
        hierarchical_access_validated=True,
        endpoint_success_rate=0.98,
        supports_incremental=False,
        status="active",
        is_enabled=True,
        last_updated=datetime(2025, 12, 5, 10, 0, 0),
    )


# ============================================================================
# ERROR SIMULATION FIXTURES
# ============================================================================

@pytest.fixture
def mock_api_error():
    """Simulate API error responses."""
    def create_error(status_code=500, message="Internal Server Error"):
        response = Mock()
        response.status_code = status_code
        response.text = message
        response.json = Mock(side_effect=ValueError("No JSON"))
        response.raise_for_status = Mock(side_effect=Exception(f"{status_code} {message}"))
        return response
    return create_error


@pytest.fixture
def mock_transient_failure():
    """Simulate transient failures (succeeds on retry)."""
    call_count = {"count": 0}
    
    def side_effect(*args, **kwargs):
        call_count["count"] += 1
        if call_count["count"] < 3:
            raise Exception("Transient failure")
        return Mock(status_code=200, json=Mock(return_value=[]))
    
    return side_effect

