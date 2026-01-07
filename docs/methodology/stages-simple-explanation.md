---
learning_material:
  is_learning_material: true
  education_level: "L1"
  education_level_name: "MVP"
  topic: "pipeline-stages"
  category: "methodology"
  subcategory: "stage-definitions"
  prerequisites: []
  leads_to: ["stage-implementation", "pipeline-orchestration"]
  part_of_series: "spectra-pipeline-fundamentals"
  series_order: 1
  learning_objectives:
    - "Understand the 7-stage SPECTRA pipeline"
    - "Know what each stage does"
    - "Understand stage dependencies"
    - "Know what each stage outputs"
  key_concepts:
    - "Source stage"
    - "Prepare stage"
    - "Extract stage"
    - "Clean stage"
    - "Transform stage"
    - "Refine stage"
    - "Analyse stage"
  estimated_time: "15 minutes"
  difficulty: "beginner"
  format: "concept-explanation"
  has_assessment: false
  related_materials:
    - "docs/methodology/METHODOLOGY-EVOLUTION.md"
    - "docs/prepare/PREPARE-STAGE-PURPOSE.md"
    - "docs/methodology/METHODOLOGY-COMPARISON.md"
---

# SPECTRA Pipeline Stages - Simple Explanation

**Date:** 2025-12-11  
**Purpose:** Simple explanation of each stage's responsibilities for confirmation

---

## The 7 Stages

```
Source → Prepare → Extract → Clean → Transform → Refine → Analyse
```

---

## Stage 1: Source

**What it does:** Sets up the connection and discovers what's available

**Simple explanation:**
- Connects to the API (Zephyr, Jira, etc.)
- Tests authentication works
- Discovers all available endpoints (e.g., 220 endpoints in Zephyr)
- Tests which endpoints work
- Creates a catalog of everything available

**Outputs:**
- `source.endpoints` - List of all API endpoints
- `source.credentials` - Authentication info (masked)
- `source.portfolio` - Summary dashboard data
- `source.config` - Configuration settings

**Think of it as:** The "handshake" stage - "Hello, what can you give me?"

---

## Stage 2: Prepare

**What it does:** Discovers the data structure and builds the perfect schema

**Simple explanation:**
- Takes all endpoints from Source
- Tests every endpoint to see what data it returns
- Creates sample tables (one table per endpoint) in `sample` schema
- Looks at the actual data structure (types, names, structure)
- Builds the perfect schema (the "canon" - the master plan)
- Documents what each field is (scalar, record, array)
- Documents field names, types, relationships

**Outputs:**
- `prepare.schema` - The master schema (canon for whole pipeline)
- `sample.{endpoint}` - One table per endpoint (220 endpoints = 220 tables)
- Schema metadata (field types, names, structure types)

**Think of it as:** The "discoverer" stage - "Here's what the data looks like"

---

## Stage 3: Extract

**What it does:** Pulls the actual data from the API

**Simple explanation:**
- Uses the schema from Prepare to know which endpoints to call
- Doesn't need ALL endpoints, just the ones needed for the final output
- Makes API calls to get the data
- Saves raw JSON to Files area
- Organises by date and project (so we can go back in history)

**Outputs:**
- Raw JSON files in Files area
- Organised by date/project structure

**Think of it as:** The "collector" stage - "Go get the data"

---

## Stage 4: Clean

**What it does:** Separates and flattens the data into individual entity tables

**Simple explanation:**
- Takes raw JSON from Extract
- Separates each top-level thing (scalar, record, array) into its own table
- Each entity gets its own table (e.g., `clean.cycle`, `clean.project`)
- Flattens complex structures (arrays, objects) into simple columns
- Renames columns to proper names
- Sets correct data types
- Keeps record identifiers (e.g., issueId, jiraKey)

**Outputs:**
- Multiple tables, one per entity (e.g., `clean.cycle`, `clean.project`)
- Each table has: recordId, recordKey, flattened entity fields
- Everything ready for Transform

**Think of it as:** The "organiser" stage - "Separate everything into neat boxes"

---

## Stage 5: Transform

**What it does:** Maps to star schema and builds the dimensional model (dimensions, facts, bridges)

**Simple explanation:**
- Takes clean entity tables
- Uses schema from Prepare to understand data structure
- **Maps to star schema** (decides which entities become dimensions, facts, bridges)
- Creates dimensions:
  - Removes duplicates
  - Removes record IDs (just keep dimension ID and attributes)
  - Adds SCD type 2 dates (for historical tracking)
- Creates bridges:
  - Just record ID + dimension ID
  - Removes everything else
  - Deduplicates
- Creates facts:
  - Only IDs and scalars (numbers, dates)
  - Text fields become "degenerate dimensions" (not in fact table)
  - Keeps fact tables efficient

**Outputs:**
- `dim*` tables (dimensions)
- `fact*` tables (fact tables)
- `bridge*` tables (bridges)

**Think of it as:** The "model builder" stage - "Map to star schema and build it"

---

## Stage 6: Refine

**What it does:** Enriches the data with business logic

**Simple explanation:**
- Takes dimensions, facts, bridges from Transform
- Adds record-level flags (e.g., "isHighPriority", "isOverdue")
- Adds groupings within dimensions (e.g., "priorityGroup", "statusCategory")
- Applies business rules
- Adds calculated fields

**Outputs:**
- Enriched dimensions (with groupings)
- Enriched facts (with flags)

**Think of it as:** The "enricher" stage - "Add business meaning"

---

## Stage 7: Analyse

**What it does:** Creates the analysis layer (semantic model, measures, ML)

**Simple explanation:**
- Takes enriched tables from Refine
- Builds semantic model (Power BI/Fabric)
- Creates measures (DAX calculations)
- Creates KPIs
- Future: Machine learning experiments
- Future: Data Activator (real-time triggers)

**Outputs:**
- Semantic model
- Measures and KPIs
- ML models (future)
- Real-time triggers (future)

**Think of it as:** The "analyst" stage - "Make it useful for analysis"

---

## The Flow (Simple)

```
Source: "What can you give me?"
  ↓
Prepare: "Here's what the data looks like"
  ↓
Extract: "Go get the data"
  ↓
Clean: "Separate into neat boxes"
  ↓
Transform: "Map to star schema and build it"
  ↓
Refine: "Add business meaning"
  ↓
Analyse: "Make it useful"
```

---

## Key Principles

1. **Each stage does ONE thing well**
2. **Each stage outputs what the next stage needs**
3. **Nothing more, nothing less**
4. **Efficient and clear**

---

## Questions to Confirm

1. **Source** - Connection and discovery? ✅
2. **Prepare** - Schema discovery from samples (NOT star schema mapping)? ✅
3. **Extract** - Pull data to Files area? ✅
4. **Clean** - Separate entities, flatten, rename? ✅
5. **Transform** - Map to star schema AND build dimensions, facts, bridges? ✅
6. **Refine** - Enrich with flags and groupings? ✅
7. **Analyse** - Semantic model, measures, ML? ✅

---

**Version:** 1.0  
**Last Updated:** 2025-12-11

