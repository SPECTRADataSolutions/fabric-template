#!/usr/bin/env python3
"""Check for duplicate endpoints in source.endpoints table."""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

# Initialize Spark (in Fabric this is already available)
spark = SparkSession.builder.getOrCreate()

print("=" * 80)
print("🔍 CHECKING FOR DUPLICATE ENDPOINTS")
print("=" * 80)

try:
    df = spark.table("source.endpoints")
    
    # Find duplicates by endpoint_path + http_method
    duplicates = (
        df.groupBy("endpoint_path", "http_method")
        .count()
        .filter("count > 1")
        .orderBy("count", ascending=False)
    )
    
    duplicate_count = duplicates.count()
    
    if duplicate_count > 0:
        print(f"\n❌ Found {duplicate_count} duplicate endpoint(s):\n")
        duplicates.show(truncate=False)
        
        print("\n" + "=" * 80)
        print("📋 DETAILED DUPLICATE ANALYSIS")
        print("=" * 80)
        
        # Show full details of duplicates
        for row in duplicates.collect():
            endpoint_path = row["endpoint_path"]
            http_method = row["http_method"]
            count = row["count"]
            
            print(f"\n🔴 Duplicate: {http_method} {endpoint_path} (appears {count} times)")
            
            # Show all rows with this duplicate
            matching_rows = df.filter(
                (col("endpoint_path") == endpoint_path) & 
                (col("http_method") == http_method)
            )
            matching_rows.select("endpoint_path", "http_method", "category", "hierarchical", "description").show(truncate=False)
    else:
        print("\n✅ No duplicate endpoints found!")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)

