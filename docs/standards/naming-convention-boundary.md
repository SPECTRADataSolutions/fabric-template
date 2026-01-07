# Naming Convention Boundary: Fabric Visibility Rule

**Status:** 🟢 Canonical  
**Version:** 1.0.0  
**Date:** 2025-12-06  
**Objective:** Clarify naming convention boundary based on Fabric visibility

---

## 🎯 Core Principle

**The boundary is Fabric visibility:**

- **Before Fabric (Python code, notebooks, internal processing):** `snake_case`
- **In Fabric (Delta tables, columns visible to users):** `camelCase`

When users can see fields in Fabric UI, Power BI, or SQL queries → use `camelCase`.  
When fields are only in Python code or notebook processing → use `snake_case`.

---

## 📊 Naming Convention Matrix

| Context                         | Convention                     | Example                                                         | Rationale                              |
| ------------------------------- | ------------------------------ | --------------------------------------------------------------- | -------------------------------------- |
| **Python Variables/Parameters** | `snake_case`                   | `debug_mode`, `project_key`, `full_run_mode`                    | Pythonic convention                    |
| **Python Functions**            | `snake_case`                   | `validate_required_columns()`, `load_source_data()`             | Pythonic convention                    |
| **Delta Table Names**           | `camelCase` with schema prefix | `source.portfolio`, `prepare.schema`, `refine.factExecution`    | Schema = stage name, user-visible      |
| **Delta Column Names**          | `camelCase`                    | `executionId`, `createdDateTime`, `isPassed`, `totalExecutions` | **Fabric visibility - users see this** |
| **Power BI Measures**           | `Proper Case`                  | `Execution Rate %`, `Pass Rate %`, `Total Executions`           | User-facing, readable labels           |
| **SQL Queries (Fabric)**        | `camelCase`                    | `SELECT executionId, isPassed FROM factExecution`               | Fabric SQL convention                  |
| **Internal Notebook Variables** | `snake_case`                   | `df_enriched`, `spark_session`, `api_token`                     | Python processing, not user-facing     |
| **Pipeline Parameters**         | `snake_case`                   | `bootstrap`, `preview`, `test`                                  | Python notebook parameters             |

---

## 🔍 The Visibility Boundary

### Inside Fabric (User-Visible) → `camelCase`

**These are visible to users in Fabric UI:**

1. **Delta Table Names** (with schema prefix = stage name)

   - `source.portfolio` (Source stage)
   - `prepare.schema` (Prepare stage)
   - `refine.factExecution` (Refine stage)
   - `refine.dimProject` (Refine stage)

2. **Delta Column Names**

   - `executionId`
   - `projectId`
   - `createdDateTime`
   - `isPassed`
   - `totalExecutions`
   - `hasComment`
   - `daysSinceCycleStart`

3. **Power BI Field Names**

   - Fields imported from Delta tables (camelCase)
   - Calculated columns (camelCase)
   - **Measures (Proper Case)** - User-facing, readable labels (e.g., `Execution Rate %`, `Pass Rate %`)

4. **Fabric SQL Endpoint**
   - Column names in SQL queries
   - Table names in SQL queries

**Rule:** If a user can query it in Fabric SQL or see it in Power BI → `camelCase`

---

### Outside Fabric (Internal Processing) → `snake_case`

**These are NOT visible to users:**

1. **Python Variables**

   - `debug_mode`
   - `project_key`
   - `api_token`
   - `spark_session`

2. **Python Functions**

   - `validate_required_columns()`
   - `load_source_data()`
   - `create_portfolio_table()`

3. **Notebook Parameters**

   - `bootstrap`
   - `preview`
   - `test`

4. **Internal DataFrames (before writing to Delta)**
   - `df_enriched`
   - `df_clean`
   - Temporary processing DataFrames

**Rule:** If it's only in Python code/notebooks and never exposed to Fabric → `snake_case`

---

## 🔄 Transformation Point

**The Clean Stage is the transformation boundary:**

```python
# Extract/Clean Stage (snake_case internally)
df_raw = extract_data()
df_clean = df_raw.select(
    col("execution_id").alias("executionId"),  # Transform to camelCase
    col("created_date_time").alias("createdDateTime"),
    col("is_passed").alias("isPassed")
)

# Write to Delta (camelCase - user visible)
df_clean.write.format("delta").saveAsTable("factExecution")
```

**After Clean Stage:**

- All column names must be `camelCase`
- All table names must be `camelCase`
- Users will see these names in Fabric

---

## ✅ SPECTRA Standard (Canonical)

Based on `Data/jira/docs/standards/naming-conventions.md`:

### Data Columns/Fields in Delta Tables

**Convention:** `camelCase` (e.g., `issueId`, `createdDateTime`, `statusCategory`)

**Rationale:** Aligns with Microsoft Fabric/Lakehouse conventions and Power BI standards.

### Python Code & Pipeline Parameters

**Convention:** `snake_case` (e.g., `debug_mode`, `project_key`, `full_run_mode`)

**Rationale:** Pythonic convention for code readability.

---

## 🌐 Industry Best Practice

### Microsoft Fabric / Databricks Recommendation

**Official Guidance:**

- **Delta Tables:** Use `camelCase` for table and column names

- **SQL Queries:** `camelCase` is standard in Fabric SQL endpoint
- **Power BI:** `camelCase` columns are most compatible

**Rationale:**

- Fabric SQL endpoint uses camelCase by default
- Power BI imports work best with camelCase

- Consistent with Microsoft data platform conventions

### Alternative Approaches

**Some organisations use:**

- `PascalCase` for tables (e.g., `FactExecution`)
- `snake_case` for columns (e.g., `execution_id`)

**SPECTRA Choice:**

- `camelCase` for both tables and columns
- Consistent, user-friendly, Fabric-native

---

## 📋 Decision Tree

```text
Is this a Delta table name?
  → YES: Use camelCase with schema prefix (e.g., "source.portfolio", "refine.factExecution")
  → Schema = stage name (source, prepare, extract, clean, transform, refine, analyse)

Is this a Delta column name?
  → YES: Use camelCase (e.g., "executionId", "isPassed")
  → Users will see this in Fabric UI, Power BI, SQL

Is this a Python variable/parameter?
  → YES: Use snake_case (e.g., "debug_mode", "project_key")
  → Internal processing only

Is this a Python function?
  → YES: Use snake_case (e.g., "validate_required_columns")
  → Code, not user-facing

Is this a Power BI measure?
  → YES: Use Proper Case (e.g., "Execution Rate %", "Pass Rate %")
  → User-facing, readable labels in Power BI

Is this a temporary DataFrame variable?
  → YES: Use snake_case (e.g., "df_enriched")
  → Internal processing, transformed before writing to Delta
```

---

## 🎯 Examples

### ✅ Correct: camelCase for Delta Tables/Columns (with Schema Prefix)

```python
# Delta table name (with schema prefix = stage name)
df.write.format("delta").saveAsTable("refine.factExecution")  # Refine stage

# Source stage table
df_portfolio.write.format("delta").saveAsTable("source.portfolio")  # Source stage

# Prepare stage table
df_schema.write.format("delta").saveAsTable("prepare.schema")  # Prepare stage

# Delta column names (camelCase)
schema = StructType([
    StructField("executionId", LongType(), False),
    StructField("projectId", IntegerType(), False),
    StructField("isPassed", BooleanType(), True),
    StructField("totalExecutions", IntegerType(), True),
    StructField("hasComment", BooleanType(), True),
    StructField("daysSinceCycleStart", IntegerType(), True),
])
```

**User sees in Fabric:**

```sql
SELECT executionId, isPassed, totalExecutions
FROM refine.factExecution
WHERE hasComment = true
```

### ✅ Correct: Proper Case for Power BI Measures

```dax
// Power BI Measures (user-facing, readable labels)
Execution Rate % = COUNTROWS(refine.factExecution) / COUNTROWS(ALL(refine.factExecution))
Pass Rate % = DIVIDE(SUM(refine.factExecution[isPassed]), COUNTROWS(refine.factExecution))
Total Executions = COUNTROWS(refine.factExecution)
Average Execution Duration (seconds) = AVERAGE(refine.factExecution[durationSeconds])
```

**Why Proper Case:** Measures are the primary user-facing elements in Power BI reports. They should be readable, professional labels that users see in visualizations.

### ✅ Correct: snake_case for Python Variables

```python
# Python variables
debug_mode = True
project_key = "PROJECT-1"
api_token = get_secret("API_TOKEN")

# Python functions
def validate_required_columns(df, schema):
    pass

def load_source_data(source_path):
    pass
```

### ✅ Correct: Transformation in Clean Stage

```python
# Extract stage (snake_case internally)
df_raw = extract_from_api()
df_raw.columns  # ["execution_id", "created_date_time", "is_passed"]

# Clean stage (transform to camelCase before writing)
df_clean = df_raw.select(
    col("execution_id").alias("executionId"),
    col("created_date_time").alias("createdDateTime"),
    col("is_passed").alias("isPassed")
)

# Write to Delta (camelCase with schema prefix - user visible)
df_clean.write.format("delta").saveAsTable("refine.factExecution")  # Refine stage
```

---

## 🚫 Anti-Patterns

### ❌ Wrong: snake_case in Delta Tables

```python
# ❌ BAD: Users will see snake_case in Fabric
df.write.format("delta").saveAsTable("fact_execution")  # Wrong! (missing schema prefix + snake_case)
df.write.format("delta").saveAsTable("refine.fact_execution")  # Wrong! (snake_case table name)
schema = StructType([
    StructField("execution_id", LongType(), False),  # Wrong! (snake_case column)
    StructField("is_passed", BooleanType(), True),   # Wrong! (snake_case column)
])
```

### ❌ Wrong: Missing Schema Prefix

```python
# ❌ BAD: Table name without schema prefix (stage name)
df.write.format("delta").saveAsTable("factExecution")  # Wrong! Should be "refine.factExecution"
```

### ❌ Wrong: camelCase in Python Variables

```python
# ❌ BAD: Not Pythonic
debugMode = True  # Wrong!
projectKey = "PROJECT-1"  # Wrong!

def validateRequiredColumns():  # Wrong!
    pass
```

### ❌ Wrong: Mixed Conventions

```python
# ❌ BAD: Mixing conventions causes confusion
df.write.format("delta").saveAsTable("factExecution")  # camelCase table
schema = StructType([
    StructField("execution_id", LongType(), False),  # snake_case column - WRONG!
])
```

---

## 🔄 Migration Pattern

When fixing naming violations:

1. **Identify boundary:** Is this user-visible in Fabric?
2. **Apply convention:** Use camelCase for Fabric, snake_case for Python
3. **Transform at Clean stage:** Convert snake_case → camelCase before writing to Delta
4. **Update references:** Fix all SQL queries, Power BI models, documentation

---

## 📚 References

- **SPECTRA Canonical Naming:** `Data/jira/docs/standards/naming-conventions.md`
- **Power Query Standards:** `Data/jira/docs/standards/powerquery-standards.md`

- **Clean Stage Standards:** `Data/jira/docs/methodology/4-clean/clean.md`
- **Microsoft Fabric Documentation:** Official Fabric naming guidance

---

## 🎯 Summary

**The Rule:**

- **Fabric-visible (tables, columns):** `camelCase` with schema prefix (stage name)
- **Power BI Measures (user-facing):** `Proper Case` (readable labels)
- **Python-only (variables, functions, params):** `snake_case`
- **Transformation point:** Clean stage converts snake_case → camelCase
  **Why:**

- Fabric/Power BI users see camelCase columns and Proper Case measures
- Delta tables use schema prefixes (stage names) for organization
- Python developers use snake_case
- Clear boundary = no confusion

**The Boundary:**

> "If a user can query it in Fabric SQL or see it in Power BI, it must be camelCase. Everything else is snake_case."

---

## 📦 Deployment

**Last Deployed:** 2025-12-06  
**Deployment Method:** Git sync to Fabric workspace  
**Status:** Active in `zephyr.Workspace`
