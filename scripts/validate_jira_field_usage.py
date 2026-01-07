"""
Validate which Jira schema fields are ACTUALLY USED vs just defined.

SPECTRA-grade validation: Evidence over assumption.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def analyze_jira_schema_usage():
    """Analyze which fields in Jira's prepare._schema are actually populated."""
    
    spark = SparkSession.builder.appName("JiraSchemaValidation").getOrCreate()
    
    print("=" * 80)
    print("🔬 Jira Schema Field Usage Analysis")
    print("=" * 80)
    
    # Read Jira's prepare._schema
    df_schema = spark.read.format("delta").load("Tables/prepare/_schema")
    
    total_rows = df_schema.count()
    
    print(f"\n📊 Total schema rows: {total_rows}")
    print("\n" + "=" * 80)
    print("Field Utilization Analysis")
    print("=" * 80)
    
    # Check each field for NULL usage
    fields_to_check = [
        "group", "groupSortOrder", "entitySortOrder", "fieldId",
        "structureType", "isInApiIssue", "isInChangelog", 
        "isNullable", "defaultValue", "description", "notes",
        "initialDataType", "type", "columnOrder", "piiLevel",
        "isInFactIssue", "keyField", "dimensionName", "bridgeName"
    ]
    
    usage_stats = []
    
    for field in fields_to_check:
        # Count non-null values
        non_null = df_schema.filter(F.col(field).isNotNull()).count()
        null_count = total_rows - non_null
        pct_populated = (non_null / total_rows * 100) if total_rows > 0 else 0
        
        # Check for empty arrays
        if field in ["rawField", "targetField", "dataType", "columnOrder", "piiLevel", "isInFactIssue", "keyField"]:
            # Array field - check if non-empty
            non_empty = df_schema.filter(
                F.col(field).isNotNull() & (F.size(F.col(field)) > 0)
            ).count()
            pct_populated = (non_empty / total_rows * 100) if total_rows > 0 else 0
        
        usage_stats.append({
            "field": field,
            "populated": non_null,
            "null": null_count,
            "pct_populated": pct_populated
        })
        
        # Categorize usage
        if pct_populated >= 90:
            status = "✅ CRITICAL"
        elif pct_populated >= 50:
            status = "⚠️ MODERATE"
        elif pct_populated >= 10:
            status = "🔶 LOW"
        else:
            status = "❌ UNUSED"
        
        print(f"{field:20s} {pct_populated:6.1f}% {status}")
    
    print("\n" + "=" * 80)
    print("Recommendation Categories")
    print("=" * 80)
    print("✅ CRITICAL (>90% populated)  → MUST HAVE in canonical")
    print("⚠️ MODERATE (50-90%)          → RECOMMENDED in canonical")
    print("🔶 LOW (10-50%)               → OPTIONAL in canonical")
    print("❌ UNUSED (<10%)              → EXCLUDE from canonical")
    
    # Show sample values for key fields
    print("\n" + "=" * 80)
    print("Sample Values for Validation")
    print("=" * 80)
    
    print("\n📋 structureType values:")
    df_schema.groupBy("structureType").count().orderBy(F.desc("count")).show(truncate=False)
    
    print("\n📋 group values:")
    df_schema.groupBy("group").count().orderBy("group").show(truncate=False)
    
    print("\n📋 Sample rows with complex structures:")
    df_schema.filter(F.col("structureType") == "array").select(
        "fieldId", "structureType", "rawField", "targetField", "dataType"
    ).show(5, truncate=False)

if __name__ == "__main__":
    analyze_jira_schema_usage()






