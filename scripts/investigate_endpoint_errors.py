#!/usr/bin/env python3
"""Investigate endpoint validation errors:
1. Why we have 224 instead of 228 endpoints
2. Which 24 endpoints are duplicates (path + method + category)
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, collect_list

spark = SparkSession.builder.getOrCreate()

print("=" * 80)
print("🔍 ENDPOINT VALIDATION ERROR INVESTIGATION")
print("=" * 80)

# Load endpoints table
df = spark.table("source.endpoints")
row_count = df.count()

print(f"\n📊 Current State:")
print(f"  - Total rows in table: {row_count}")
print(f"  - Expected: 228")
print(f"  - Missing: {228 - row_count}")

# Find duplicates (path + method + category)
print(f"\n🔴 Finding Duplicates (path + method + category):")
duplicates_df = (
    df.groupBy("endpoint_path", "http_method", "category")
    .count()
    .filter("count > 1")
    .orderBy("count", ascending=False)
)

duplicate_count = duplicates_df.count()
print(f"  - Duplicate groups: {duplicate_count}")

if duplicate_count > 0:
    print(f"\n📋 Duplicate Endpoints (showing all {duplicate_count} groups):")
    duplicates_df.show(truncate=False)
    
    print(f"\n📋 Full Details of Duplicate Endpoints:")
    # Get all duplicate endpoint details
    duplicate_keys = duplicates_df.select("endpoint_path", "http_method", "category").collect()
    
    for key in duplicate_keys:
        path = key["endpoint_path"]
        method = key["http_method"]
        category = key["category"]
        
        print(f"\n  🔴 Duplicate Group: {method} {path} ({category})")
        matching = df.filter(
            (col("endpoint_path") == path) & 
            (col("http_method") == method) & 
            (col("category") == category)
        )
        
        matching.select(
            "endpoint_path", "http_method", "category", "description", 
            "full_path", "resource"
        ).show(truncate=False)

# Check unique combinations
print(f"\n📊 Uniqueness Analysis:")
unique_path_method = df.select("endpoint_path", "http_method").distinct().count()
unique_path_method_category = df.select("endpoint_path", "http_method", "category").distinct().count()

print(f"  - Unique (path + method): {unique_path_method}")
print(f"  - Unique (path + method + category): {unique_path_method_category}")
print(f"  - Total rows: {row_count}")

if unique_path_method_category < row_count:
    print(f"  - Difference: {row_count - unique_path_method_category} duplicate rows")

# Check if catalog might have different count
print(f"\n💡 Investigation Notes:")
print(f"  - If catalog has 228 entries but table has 224, 4 entries may have:")
print(f"    * Missing required fields (null/empty endpoint_path, http_method, or category)")
print(f"    * DataFrame creation filtering")
print(f"    * Catalog parsing issues")

print("\n" + "=" * 80)

