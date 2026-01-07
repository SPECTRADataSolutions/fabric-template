#!/usr/bin/env python3
"""
Check if the updated endpoints (with new metadata fields) are in the Delta table.

This script checks:
1. If source.endpoints table exists
2. What columns it has
3. If it has the new fields (full_path, query_parameters, path_parameters, resource)
4. How many endpoints are in the table
5. If there are duplicates
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

# Initialize Spark (in Fabric this is already available)
spark = SparkSession.builder.getOrCreate()

print("=" * 80)
print("CHECKING ENDPOINTS IN DELTA TABLE")
print("=" * 80)
print()

try:
    # Check if table exists
    try:
        df = spark.table("source.endpoints")
        print("✅ Table 'source.endpoints' exists")
        print()
    except Exception as e:
        print(f"❌ Table 'source.endpoints' does not exist: {e}")
        print("\n💡 You need to run Source notebook with bootstrap=True to create the table")
        exit(1)
    
    # Get schema
    print("=" * 80)
    print("TABLE SCHEMA")
    print("=" * 80)
    print()
    df.printSchema()
    print()
    
    # Get row count
    row_count = df.count()
    print(f"📊 Total endpoints in table: {row_count}")
    print()
    
    # Check for new fields
    print("=" * 80)
    print("METADATA FIELDS CHECK")
    print("=" * 80)
    print()
    
    columns = df.columns
    required_fields = ["endpoint_path", "http_method", "category"]
    new_fields = ["full_path", "query_parameters", "path_parameters", "resource"]
    
    print("Required fields:")
    for field in required_fields:
        if field in columns:
            print(f"  ✅ {field}")
        else:
            print(f"  ❌ {field} - MISSING")
    
    print("\nNew metadata fields:")
    for field in new_fields:
        if field in columns:
            print(f"  ✅ {field}")
        else:
            print(f"  ❌ {field} - MISSING (table needs to be re-bootstrapped)")
    
    print()
    
    # Check for duplicates
    print("=" * 80)
    print("DUPLICATE CHECK")
    print("=" * 80)
    print()
    
    # Check by endpoint_path + http_method (old way)
    if "endpoint_path" in columns and "http_method" in columns:
        duplicates_old = (
            df.groupBy("endpoint_path", "http_method")
            .count()
            .filter("count > 1")
        )
        dup_count_old = duplicates_old.count()
        
        if dup_count_old > 0:
            print(f"🔴 Found {dup_count_old} duplicate(s) by (endpoint_path, http_method):")
            duplicates_old.show(truncate=False)
        else:
            print("✅ No duplicates by (endpoint_path, http_method)")
        print()
    
    # Check by full_path + http_method (new way - if field exists)
    if "full_path" in columns and "http_method" in columns:
        duplicates_new = (
            df.groupBy("full_path", "http_method")
            .count()
            .filter("count > 1")
        )
        dup_count_new = duplicates_new.count()
        
        if dup_count_new > 0:
            print(f"🔴 Found {dup_count_new} duplicate(s) by (full_path, http_method):")
            duplicates_new.show(truncate=False)
        else:
            print("✅ No duplicates by (full_path, http_method)")
        print()
    else:
        print("⚠️ Cannot check duplicates by (full_path, http_method) - field not in table")
        print("   Table needs to be re-bootstrapped with updated catalog")
        print()
    
    # Sample endpoints
    print("=" * 80)
    print("SAMPLE ENDPOINTS")
    print("=" * 80)
    print()
    
    sample = df.limit(3)
    if "full_path" in columns:
        sample.select("endpoint_path", "full_path", "http_method", "category").show(truncate=False)
    else:
        sample.select("endpoint_path", "http_method", "category").show(truncate=False)
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"Total endpoints: {row_count}")
    print(f"Expected: 224 (after deduplication)")
    print()
    
    if "full_path" in columns:
        print("✅ Table has new metadata fields")
        print("   Status: Up to date")
    else:
        print("❌ Table missing new metadata fields")
        print("   Action: Re-bootstrap endpoints (run Source notebook with bootstrap=True)")
    
    if row_count == 224:
        print("✅ Row count matches expected (224)")
    elif row_count == 228:
        print("⚠️ Row count is 228 (old count with duplicates)")
        print("   Action: Re-bootstrap to get 224 unique endpoints")
    else:
        print(f"⚠️ Row count is {row_count} (expected 224)")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()

