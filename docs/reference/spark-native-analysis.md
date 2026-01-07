# Is Zephyr Notebook "Spark Native"?

**Date:** 2025-12-04  
**Question:** What does "Spark native" mean and is Zephyr fully Spark native?

---

## 🎯 Short Answer

**No, Zephyr is NOT fully Spark native.**

It's a **hybrid architecture**:
- ✅ **Storage layer:** Spark native (Delta tables)
- ❌ **Extract layer:** Pure Python (requests, loops, lists)

---

## 📚 What Does "Spark Native" Mean?

### **Fully Spark Native**
All operations use Spark's distributed computing:

```python
# ✅ Spark Native
df = spark.read.json("s3://bucket/data/*.json")  # Distributed read
df_filtered = df.filter(df.status == "active")   # Distributed filter
df_aggregated = df.groupBy("project").count()     # Distributed aggregation
df_aggregated.write.format("delta").save("...")   # Distributed write

# Key characteristics:
# - No .collect() until final output
# - No Python loops over data
# - Lazy evaluation
# - Scales to TB+ datasets
# - Uses cluster resources
```

### **Python + Spark Hybrid**
Extract in Python, store in Spark:

```python
# ❌ Not Spark Native (but common for APIs)
api_data = []
for item in api.get_all():              # Python loop
    api_data.append(item)               # Python list
    
df = spark.createDataFrame(api_data)    # Convert to Spark
df.write.format("delta").save("...")    # Spark write

# Key characteristics:
# - Python does heavy lifting
# - Single-node bottleneck
# - Limited by driver memory
# - Doesn't scale to TB+ datasets
# - Only uses driver (not cluster)
```

---

## 🔍 Zephyr's Current Architecture

### **Extract Layer: Pure Python** ❌

```python
# Current approach in Zephyr
session = requests.Session()  # Python HTTP client

# Phase 1: Projects
r = session.get(f"{base_url}/project/details")
projects = r.json()  # Python list
for project in projects:  # Python loop
    dim_projects_data.append({...})  # Python list

# Phase 2: Releases
for project in dim_projects_data:  # Python loop
    r = session.get(f"{base_url}/release/project/{project_id}")
    releases = r.json()  # Python list
    for release in releases:  # Python loop
        dim_releases_data.append({...})  # Python list

# Phase 3-4: Cycles, Executions (same pattern)
```

**Characteristics:**
- 🐌 Single-threaded API calls
- 🐌 Python loops over data
- 🐌 All data in driver memory
- 🐌 No parallelization
- ✅ Simple and readable
- ✅ Good for small/medium datasets (<10GB)

### **Storage Layer: Spark Native** ✅

```python
# Convert Python data to Spark DataFrame
df = spark.createDataFrame(dim_projects_data)

# Write to Delta (Spark native)
df.write.mode("overwrite").format("delta").save("Tables/source/dimProject")
```

**Characteristics:**
- ✅ Delta Lake format (Spark native)
- ✅ ACID transactions
- ✅ Schema enforcement
- ✅ Time travel
- ✅ Scalable storage

---

## 📊 Hybrid Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ ZEPHYR SOURCE NOTEBOOK                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │ EXTRACT LAYER (Pure Python) ❌                     │   │
│  ├────────────────────────────────────────────────────┤   │
│  │                                                     │   │
│  │  • requests.Session()  (HTTP client)               │   │
│  │  • for loop  (sequential iteration)                │   │
│  │  • Python list  (in-memory storage)                │   │
│  │  • .append()  (list operations)                    │   │
│  │                                                     │   │
│  │  Bottleneck: Single driver node                    │   │
│  │  Scale limit: ~10GB (driver memory)                │   │
│  │                                                     │   │
│  └────────────────────────────────────────────────────┘   │
│                          ↓                                  │
│  ┌────────────────────────────────────────────────────┐   │
│  │ STORAGE LAYER (Spark Native) ✅                    │   │
│  ├────────────────────────────────────────────────────┤   │
│  │                                                     │   │
│  │  • spark.createDataFrame()  (convert to Spark)     │   │
│  │  • df.write.format("delta")  (distributed write)   │   │
│  │  • Delta tables  (ACID, time travel)               │   │
│  │                                                     │   │
│  │  Benefit: Scalable storage for downstream          │   │
│  │                                                     │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤔 Why Is This Approach Used?

### **API Extraction ≠ Big Data Problem**

For API data extraction, Python is often better:

| Aspect | Python Approach | Spark Native |
|--------|----------------|--------------|
| **API Pagination** | ✅ Easy (requests) | ❌ Complex (custom UDF) |
| **Rate Limiting** | ✅ Easy (time.sleep) | ❌ Hard (distributed) |
| **Error Handling** | ✅ Simple try/except | ❌ Complex (task retries) |
| **Authentication** | ✅ Native (requests) | ❌ Custom (broadcast vars) |
| **JSON Parsing** | ✅ Built-in | ✅ Built-in |
| **Hierarchical APIs** | ✅ Natural (loops) | ❌ Complex (joins) |
| **Code Readability** | ✅ Straightforward | ❌ Verbose |
| **Scale (TB+)** | ❌ Driver memory limit | ✅ Cluster parallelization |

**For Zephyr's use case:**
- Small/medium dataset (~10GB extracted data)
- Hierarchical API (project → release → cycle → execution)
- Rate limiting needed
- Complex authentication

→ **Python approach is appropriate!**

---

## 🚀 When Would Spark Native Matter?

### **Scenario 1: Massive Datasets**
If extracting 100TB+ from APIs:
```python
# Would need Spark native approach
# - Parallelize API calls across executors
# - Stream results directly to Delta
# - No driver memory accumulation
```

### **Scenario 2: File-Based Ingestion**
If reading from files instead of APIs:
```python
# Spark native is natural
df = spark.read.json("s3://bucket/*.json")  # Distributed read
df.write.format("delta").save("...")         # No Python needed
```

### **Scenario 3: Downstream Transformations**
Once data is in Delta, all downstream stages ARE Spark native:
```python
# Prepare, Clean, Transform stages (all Spark native)
df = spark.read.format("delta").load("Tables/source/dimProject")
df_cleaned = df.filter(...).select(...).join(...)
df_cleaned.write.format("delta").save("Tables/clean/dimProject")
```

---

## ✅ Is Zephyr's Hybrid Approach OK?

**Yes! Here's why:**

### **✅ Advantages**
1. **Appropriate for API extraction**
   - APIs are inherently sequential (pagination, rate limits)
   - Python's `requests` library is industry standard
   - Easy to read and maintain

2. **Downstream stages benefit from Spark**
   - Delta tables enable distributed processing
   - Prepare/Clean/Transform stages can scale
   - Final output is Spark native

3. **Matches data volume**
   - Zephyr APIs return ~10GB total
   - Well within driver memory limits
   - No need for distributed extraction

4. **Simple error handling**
   - Python try/except is straightforward
   - Easy to retry failed API calls
   - Clear logging and debugging

### **⚠️ Limitations**
1. **Driver memory bound**
   - Cannot extract >100GB in one run
   - Would need batching for massive datasets

2. **Single-threaded API calls**
   - Sequential, not parallel
   - Could be slower than distributed approach

3. **No cluster utilization during extract**
   - Only driver node is used
   - Cluster sits idle during extraction

---

## 🎯 Could Zephyr Be Made Fully Spark Native?

**Technically yes, but not recommended.**

### **Hypothetical Spark Native Approach**

```python
from pyspark.sql.functions import udf, explode
from pyspark.sql.types import ArrayType, StructType

# Create seed DataFrame with API endpoints
api_endpoints = [
    {"endpoint": "/project", "params": {}},
    # ... more endpoints
]
df_endpoints = spark.createDataFrame(api_endpoints)

# Define UDF to call API (runs on executors)
@udf(returnType=ArrayType(StructType([...])))
def call_api(endpoint, params):
    import requests
    # This runs on EACH executor
    response = requests.get(f"{base_url}{endpoint}", params=params)
    return response.json()

# Distribute API calls across cluster
df_results = df_endpoints.withColumn("data", call_api("endpoint", "params"))
df_results = df_results.select(explode("data").alias("row"))

# Write to Delta
df_results.write.format("delta").save("Tables/source/dimProject")
```

### **Why This Is Worse**

1. **Rate limiting breaks**
   - Multiple executors = multiple connections
   - Violates API rate limits
   - Risk of IP ban

2. **Authentication complexity**
   - Need to broadcast credentials securely
   - Each executor needs own session
   - Token refresh is complex

3. **Hierarchical APIs are awkward**
   - Need multiple passes (project → release → cycle)
   - Requires complex join logic
   - Harder to understand and debug

4. **Error handling is harder**
   - Failed tasks retry on different executors
   - Partial failures are complex
   - Debugging is difficult

5. **No real performance gain**
   - API is bottleneck, not CPU
   - Rate limits prevent parallelization
   - Network latency dominates

---

## 📝 Recommendations

### **Keep Current Hybrid Approach** ✅

**For Zephyr:**
- ✅ Source stage: Python + Spark (current)
- ✅ Prepare stage: Fully Spark native
- ✅ Clean stage: Fully Spark native
- ✅ Transform stage: Fully Spark native
- ✅ Refine stage: Fully Spark native
- ✅ Analyse stage: Fully Spark native

### **Document the Pattern**

Add to SPECTRA standards:
```
API Extraction Pattern:
- Source stage: Python for API calls, Spark for storage
- All downstream stages: Fully Spark native
- Rationale: APIs are sequential, but processing scales
```

### **Monitor for Scale**

If Zephyr data grows >50GB:
- Consider batching (extract in chunks)
- Consider streaming (write as you extract)
- Consider parallelization (if rate limits allow)

---

## 💡 Key Insights

### 1. **"Spark Native" Isn't Always Better**
Spark is designed for big data transformations, not API calls. Python is often more appropriate for API extraction.

### 2. **Hybrid Architecture Is Common**
Most real-world pipelines mix Python (orchestration, APIs) with Spark (processing, storage).

### 3. **Scale Determines Approach**
- Small datasets (<10GB): Python is fine
- Medium datasets (10-100GB): Hybrid works
- Large datasets (100GB-1TB): Consider Spark native
- Massive datasets (>1TB): Must be Spark native

### 4. **Storage Layer Matters Most**
Once data is in Delta tables, downstream stages can scale regardless of how it was extracted.

---

## 🎓 Bottom Line

**Question:** Is Zephyr fully Spark native?

**Answer:** No, but that's **intentional and appropriate**.

- ❌ Extract layer: Pure Python (sequential API calls)
- ✅ Storage layer: Spark native (Delta tables)
- ✅ All downstream stages: Spark native (distributed processing)

**This hybrid approach is:**
- ✅ Appropriate for API extraction
- ✅ Scalable for Zephyr's data volume
- ✅ Simple and maintainable
- ✅ Industry standard pattern

**Zephyr doesn't need to be fully Spark native because APIs are inherently sequential and the dataset is manageable with Python!** 🎯

