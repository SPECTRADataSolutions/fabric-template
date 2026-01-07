# {PROJECT} Intelligence Notebook

This notebook contains source-specific intelligence about the {PROJECT} API.

## Purpose

The intelligence notebook stores all knowledge discovered about the {PROJECT} API:
- **Schemas**: JSON schemas for each entity type
- **Endpoints**: Complete API endpoint catalog
- **Dependencies**: Entity dependency relationships
- **Constraints**: API bugs, blockers, workarounds, quirks

## Usage

Load intelligence in your notebooks:

```python
%run {PROJECT}Intelligence

# Now {PROJECT}Intelligence class is available
endpoint = {PROJECT}Intelligence.get_read_endpoint_path("entity1", projectId=44)
```

## How to Populate

1. **Discover Schemas**: Run API calls and analyze JSON responses
2. **Catalog Endpoints**: Document all available endpoints
3. **Map Dependencies**: Identify hierarchical relationships
4. **Document Constraints**: Record bugs, blockers, workarounds

## Structure

- `SCHEMAS`: Entity JSON schemas
- `READ_ENDPOINTS`: GET endpoints for data extraction
- `DEPENDENCIES`: Entity dependency graph
- `CONSTRAINTS`: API limitations and workarounds

## Best Practices

- Keep intelligence up-to-date as you discover API patterns
- Document all constraints and workarounds
- Use helper methods for endpoint path generation
- Version intelligence with your contract version

