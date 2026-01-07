# Fabric Files vs Tables Area Quirk

## Issue

When writing JSON data to the Files area in Fabric, sometimes the data ends up in the Tables area (as Delta) instead, making it invisible in the Files explorer. This requires manual intervention:
1. Right-click the item in Tables
2. Move to Files
3. Delete the incorrect entry

## Known Behavior

- **Files area**: Intended for raw JSON files, config files, unstructured data
- **Tables area**: Intended for Delta Lake tables (structured, queryable data)
- **Quirk**: Sometimes `df.write.json("Files/...")` creates a Delta table in Tables area instead

## Root Cause (Suspected)

Fabric's Spark runtime may auto-detect certain write patterns and convert them to Delta format, especially when:
- Writing structured JSON that looks like tabular data
- Using certain Spark write methods
- Writing to paths that Fabric interprets as table locations

## Workaround

**Skip Files area for structured data** - Write directly to Delta tables:
- Use `df.write.format("delta").save("Tables/...")` instead of `df.write.json("Files/...")`
- This is more reliable and provides better query capabilities
- Delta tables are the preferred storage format for structured data in Fabric

## Recommendation

For SPECTRA pipelines:
- **Files area**: Only for truly unstructured files (raw API responses, logs, etc.)
- **Tables area (Delta)**: For all structured data, config metadata, reference tables
- **Source stage endpoints**: Write directly to `Tables/source/zephyr_endpoints` (Delta table)

## References

- This quirk has been observed in multiple SPECTRA pipelines
- Jira pipeline uses Delta tables for all structured data
- Fabric best practice: Use Delta for anything that needs to be queried or referenced




