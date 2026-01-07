# Use Embedded Intelligence in prepareZephyr

## Summary
Instead of loading intelligence from files, prepareZephyr now uses `ZephyrIntelligence` class embedded in spectraSDK.

## Changes

### Old Approach (File-based)
```python
# Load from /lakehouse/default/Files/intelligence/schemas/*.json
schemas_path = base_path / "schemas"
for schema_file in schemas_path.glob("*.json"):
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_json = json.load(f)
        # ... process schema
```

### New Approach (SDK-embedded)
```python
# Load from ZephyrIntelligence (embedded in SDK)
for entity_name, entity_schema in ZephyrIntelligence.SCHEMAS.items():
    # ... process schema (already Python dict)
```

## Benefits
- ✅ **Version controlled** - Intelligence syncs with notebooks
- ✅ **No file uploads** - Everything in Git
- ✅ **Faster** - No file I/O, direct Python access
- ✅ **Type-safe** - Python dicts instead of JSON/YAML parsing
- ✅ **Self-contained** - No external dependencies

## Implementation
1. Intelligence generated as Python code: `scripts/generate_intelligence_python.py`
2. Appended to spectraSDK: `scripts/append_intelligence_to_sdk.py`
3. prepareZephyr refactored to use `ZephyrIntelligence` class






