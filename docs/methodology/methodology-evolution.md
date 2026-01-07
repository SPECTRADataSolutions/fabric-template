# SPECTRA Methodology Evolution

**Date**: 2025-12-10  
**Status**: ✅ Active Standard  
**Purpose**: Document the evolution of SPECTRA methodology stages

---

## Overview

The SPECTRA methodology has evolved to better align with semantic clarity and practical implementation. This document captures the changes and rationale.

---

## Methodology Change

### **Before (Original 7-Stage Pattern)**

```
Source → Prepare → Extract → Clean → Transform → Refine → Analyse
```

**Stage Responsibilities:**

1. **Source**: Catalogue & authenticate upstream systems
2. **Prepare**: Declare static control & schema config
3. **Extract**: Land raw unchanged data (JSON)
4. **Clean**: Standardise types & naming, dedupe, validate
5. **Transform**: Join & enrich to produce business-aligned entities (mononymic tables)
6. **Refine**: Model facts/dimensions & semantic structures (factIssue table - one row per issue)
7. **Analyse**: Measures & presentation layer

---

### **After (Evolved 7-Stage Pattern)**

```
Source → Prepare → Extract → Clean → Refine → Analyse
```

**Stage Responsibilities:**

1. **Source**: Catalogue & authenticate upstream systems
2. **Prepare**: Declare static control & schema config (with fact table flags)
3. **Extract**: Land raw unchanged data (JSON)
4. **Clean** (merged with Transform): 
   - **Input**: Raw JSON from Extract
   - **Output**: Mononymic tables (one row per entity/issue)
   - **Responsibilities**:
     - Standardise types & naming
     - Dedupe & validate
     - Join & enrich to produce business-aligned entities
     - Build fact tables (using `isInFactIssue` flag from Prepare)
     - Output: `factCycle`, `factProject`, etc. (one row per entity)
5. **Refine** (renamed to Enrich):
   - **Input**: Mononymic fact tables from Clean
   - **Output**: Enriched tables with business logic
   - **Responsibilities**:
     - Apply business rules
     - Add calculated fields
     - Enrich with external data
     - Create dimension tables from arrays/objects
     - Create bridge tables for many-to-many relationships
6. **Analyse**:
   - **Input**: Enriched tables from Refine
   - **Output**: Semantic model, measures, ML workflows, realtime, activator
   - **Responsibilities**:
     - Build semantic models (Power BI/Fabric)
     - Create measures & KPIs
     - ML workflows & predictions
     - Realtime processing
     - Activator patterns (event-driven)

---

## Key Changes

### 1. **Clean Merges with Transform**

**Rationale:**
- Clean stage was doing too little (just type enforcement)
- Transform stage was doing the heavy lifting (joins, enrichment, fact table building)
- Semantically, "cleaning" should mean "ready for analysis" (mononymic tables)
- Reduces stage count from 7 to 6 (more efficient)

**What Clean Now Does:**
- Takes raw JSON from Extract
- Standardises types & naming
- Deduplicates & validates
- Joins entities together
- Builds fact tables (one row per entity)
- Outputs: `factCycle`, `factProject`, etc.

### 2. **Refine Becomes Enrich**

**Rationale:**
- "Refine" was ambiguous (what are we refining?)
- "Enrich" is clearer (adding business value)
- Better semantic alignment with purpose

**What Refine (Enrich) Now Does:**
- Takes mononymic fact tables from Clean
- Applies business rules
- Adds calculated fields
- Enriches with external data
- Creates dimension tables
- Creates bridge tables

### 3. **Analyse Gets Real Purpose**

**Rationale:**
- "Analyse" was too vague (just measures?)
- Should handle actual analysis: ML, realtime, activator patterns
- Clear separation: Refine = enrichment, Analyse = analysis

**What Analyse Now Does:**
- Builds semantic models (Power BI/Fabric)
- Creates measures & KPIs
- ML workflows & predictions
- Realtime processing
- Activator patterns (event-driven)

---

## Fact Table Support

### **`isInFactIssue` Flag**

**Purpose**: Mark fields that belong in fact table (one row per entity)

**Usage in Clean Stage:**
```python
# Load schema with fact table flags
fact_fields = schema.filter(F.col("isInFactIssue") == True)
                   .filter(F.col("keyField") == True)
                   .filter(F.col("structureType") != "array")

# Build fact table by joining all fact fields
factCycle = anchor.join(entity1, on="cycleId", how="left")
                  .join(entity2, on="cycleId", how="left")
                  # ... etc
```

**Rules:**
- Only scalar fields go in fact table (arrays → dimensions/bridges)
- Only key fields (`keyField=True`) go in fact table
- Must have `isInFactIssue=True` flag
- Ensures one row per entity (grain check)

---

## Migration Guide

### **For Existing Pipelines:**

1. **Update Clean Stage:**
   - Add fact table building logic
   - Merge Transform logic into Clean
   - Output mononymic tables

2. **Update Refine Stage:**
   - Rename to "Enrich" (semantic clarity)
   - Focus on enrichment (business rules, calculated fields)
   - Create dimensions & bridges

3. **Update Analyse Stage:**
   - Add ML workflows
   - Add realtime processing
   - Add activator patterns

4. **Update Prepare Stage:**
   - Add `isInFactIssue` flag to schema
   - Add `keyField` flag to schema
   - Mark fields for fact table

---

## Benefits

1. **Semantic Clarity**: Each stage has clear, distinct purpose
2. **Efficiency**: Fewer stages (6 vs 7)
3. **Practical**: Clean does meaningful work (not just type enforcement)
4. **Scalable**: Analyse stage ready for ML/realtime/activator
5. **SPECTRA-Grade**: Fact table support built into Prepare schema

---

## References

- **Jira Implementation**: `Data/jira/6-refine/refineFacts.Notebook/notebook_content.py`
- **Schema Flags**: `isInFactIssue`, `keyField` in `prepare._schema`
- **Fact Table Pattern**: One row per entity, joins all fact fields

---

**Version**: 1.0  
**Last Updated**: 2025-12-10  
**Status**: ✅ Active Standard





