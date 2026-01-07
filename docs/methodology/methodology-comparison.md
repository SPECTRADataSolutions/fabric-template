# Methodology Comparison: Documented vs User Commentary

**Date:** 2025-12-11  
**Purpose:** Compare existing methodology documentation with user voice commentary to identify required updates

---

## Current Methodology (METHODOLOGY-EVOLUTION.md)

### **Stage Flow:**
```
Source → Prepare → Extract → Clean → Refine → Analyse
```

### **Stage Responsibilities:**

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

## User Commentary (Voice Review)

### **Stage Flow:**
```
Source → Prepare → Extract → Clean → Transform → Refine → Analyse
```

### **Stage Responsibilities:**

1. **Source**: 
   - Outputs: `source.endpoints`, `source.credentials`, `source.portfolio`, `source.config`
   - Provides everything Prepare needs, nothing more

2. **Prepare**:
   - Discovers all endpoints (220 endpoints)
   - Tests every endpoint
   - Creates sample tables (220 tables in `sample` schema)
   - Builds perfect schema (metadata-driven, canon for whole pipeline)
   - Maps to perfect star schema (intelligence for dimensions/facts/bridges)

3. **Extract**:
   - Uses selected endpoints (not all endpoints, just what's needed)
   - Saves raw JSON to Files area (date + project structure)
   - Uses Jira logic (works really well, no need to change)

4. **Clean** (combines old Clean + Transform from Jira):
   - **Input**: Raw JSON from Files area
   - **Process**:
     1. Take JSON from files area
     2. Separate each top-level struct (scalar, record, array)
     3. Save each top-level struct as its own table in clean zone
     4. Include identifier of record (e.g., issueId, jiraKey)
     5. Flatten based on structure type (record vs array vs object)
     6. Rename and type every column
   - **Output**: Multiple tables, one per entity
     - One row per record (or multiple rows if array/object)
     - Columns: recordId, recordKey, entity fields (flattened)
     - Everything ready for Transform stage

5. **Transform** (NEW - dimensional modeling):
   - **Input**: Clean tables (one per entity)
   - **Process**:
     - Create dimensions: De-duplicate clean table, remove record ID, add SCD type 2 dates
     - Create bridges: Remove everything except record ID and dimension ID, deduplicate
     - Create facts: Only IDs and scalars (dates are IDs, text becomes degenerate dimensions)
   - **Output**: Dimensions (DIM prefix), Facts (FACT prefix), Bridges (BRIDGE prefix)
   - **Note**: "This used to be Refine's job in Jira, now Transform's job"

6. **Refine** (enrichment layer):
   - **Input**: Dimensions, facts, bridges from Transform
   - **Process**:
     - Enrich fact tables with record-level flags
     - Add groupings within dimensions
   - **Output**: Enriched dimensions and facts
   - **Note**: "Used to be dimensional modeling, now just enrichment"

7. **Analyse**:
   - **Input**: Enriched tables from Refine
   - **Process**:
     - Semantic model itself
     - Measures
     - DAX calculations
     - Machine learning experiments (future)
     - Data Activator (future)
   - **Output**: Semantic model, measures, ML workflows

---

## Key Differences

### **1. Stage Count**

| Documented | User Commentary |
|------------|-----------------|
| 6 stages (Clean merged with Transform) | 7 stages (Clean + Transform separate) |

**Difference:** User wants Clean and Transform as separate stages, not merged.

---

### **2. Clean Stage**

| Documented | User Commentary |
|------------|-----------------|
| Takes raw JSON, standardises, deduplicates, joins, builds fact tables | Takes raw JSON, separates top-level structs, saves each as own table, flattens, renames, types |

**Key Differences:**
- **Documented:** Clean builds fact tables directly
- **User:** Clean separates entities into individual tables, flattens, renames, types (no fact table building)

**User's Clean Output:**
- Multiple tables (one per entity)
- Each table has: recordId, recordKey, flattened entity fields
- Ready for Transform stage

---

### **3. Transform Stage**

| Documented | User Commentary |
|------------|-----------------|
| **MERGED INTO CLEAN** | **SEPARATE STAGE** - Creates dimensions, facts, bridges |

**Key Differences:**
- **Documented:** Transform merged into Clean
- **User:** Transform is separate stage that does dimensional modeling

**User's Transform Process:**
- Takes clean tables (one per entity)
- Creates dimensions (de-duplicate, remove record ID, SCD type 2)
- Creates bridges (record ID + dimension ID, deduplicated)
- Creates facts (only IDs and scalars, degenerate dimensions for text)
- Outputs: DIM*, FACT*, BRIDGE* tables

---

### **4. Refine Stage**

| Documented | User Commentary |
|------------|-----------------|
| Creates dimension tables, creates bridge tables, applies business rules | **Only enrichment** - flags, groupings (does NOT create dimensions/bridges) |

**Key Differences:**
- **Documented:** Refine creates dimensions and bridges
- **User:** Refine only enriches (flags, groupings) - dimensions/bridges created in Transform

**User's Refine:**
- Input: Dimensions, facts, bridges from Transform
- Process: Enrich fact tables with flags, add groupings to dimensions
- Output: Enriched dimensions and facts

---

### **5. Prepare Stage**

| Documented | User Commentary |
|------------|-----------------|
| Declare static control & schema config (with fact table flags) | Discovers all endpoints, tests them, creates 220 sample tables, builds perfect schema, maps to star schema |

**Key Differences:**
- **User adds:** Sample schema creation (220 tables for 220 endpoints)
- **User adds:** Star schema intelligence (maps endpoints to dimensions/facts/bridges)

---

### **6. Extract Stage**

| Documented | User Commentary |
|------------|-----------------|
| Land raw unchanged data (JSON) | Uses selected endpoints (not all), saves to Files area with date + project structure |

**Key Differences:**
- **User clarifies:** Not all endpoints, just selected ones (based on schema)
- **User clarifies:** Files area structure (date + project)

---

## Required Methodology Updates

### **1. Restore 7-Stage Pattern**

**Change:** Revert from 6 stages to 7 stages

```
Source → Prepare → Extract → Clean → Transform → Refine → Analyse
```

**Rationale:** User explicitly wants Clean and Transform as separate stages with distinct responsibilities.

---

### **2. Update Clean Stage Definition**

**Current (Documented):**
- Merges with Transform
- Builds fact tables

**New (User Commentary):**
- **Input:** Raw JSON from Files area
- **Process:**
  1. Separate each top-level struct (scalar, record, array)
  2. Save each as its own table in clean zone
  3. Include record identifiers (recordId, recordKey)
  4. Flatten based on structure type
  5. Rename and type every column
- **Output:** Multiple tables (one per entity), ready for Transform

**Key Change:** Clean does NOT build fact tables - it prepares entity tables for Transform.

---

### **3. Add Transform Stage Definition**

**Current (Documented):**
- Merged into Clean

**New (User Commentary):**
- **Input:** Clean tables (one per entity)
- **Process:**
  - Create dimensions (de-duplicate, remove record ID, SCD type 2)
  - Create bridges (record ID + dimension ID, deduplicated)
  - Create facts (only IDs and scalars, degenerate dimensions for text)
- **Output:** DIM*, FACT*, BRIDGE* tables

**Key Change:** Transform does dimensional modeling (this was Refine's job in Jira).

---

### **4. Update Refine Stage Definition**

**Current (Documented):**
- Creates dimension tables
- Creates bridge tables
- Applies business rules

**New (User Commentary):**
- **Input:** Dimensions, facts, bridges from Transform
- **Process:**
  - Enrich fact tables with record-level flags
  - Add groupings within dimensions
- **Output:** Enriched dimensions and facts

**Key Change:** Refine does NOT create dimensions/bridges - only enrichment.

---

### **5. Update Prepare Stage Definition**

**Current (Documented):**
- Declare static control & schema config

**New (User Commentary):**
- Discovers all endpoints (220 endpoints)
- Tests every endpoint
- Creates sample tables (220 tables in `sample` schema)
- Builds perfect schema (metadata-driven)
- Maps to perfect star schema (intelligence for dimensions/facts/bridges)

**Key Changes:**
- Add sample schema creation
- Add star schema intelligence

---

### **6. Update Extract Stage Definition**

**Current (Documented):**
- Land raw unchanged data (JSON)

**New (User Commentary):**
- Uses selected endpoints (based on schema from Prepare)
- Saves to Files area with date + project structure
- Uses Jira logic (works well, no need to change)

**Key Changes:**
- Clarify endpoint selection (not all endpoints)
- Clarify file structure (date + project)

---

## Summary of Changes Needed

1. ✅ **Restore 7-stage pattern** (Clean + Transform separate)
2. ✅ **Update Clean stage** - Entity separation, flattening, renaming, typing (NO fact tables)
3. ✅ **Add Transform stage** - Dimensional modeling (dimensions, facts, bridges)
4. ✅ **Update Refine stage** - Only enrichment (flags, groupings), NO dimension/bridge creation
5. ✅ **Update Prepare stage** - Add sample schema creation, star schema intelligence
6. ✅ **Update Extract stage** - Clarify endpoint selection, file structure

---

## Open Questions from User Commentary

1. **Historical Data Handling:**
   - Question: "How should we handle historical data in dimensions?"
   - Options:
     - Whole historical dataset in clean, filter to latest in dimension
     - Separate historical data into another table
     - Isolate current vs historical, combine when needed
   - Requirement: Need SPECTRA-grade solution

2. **Sample Efficiency:**
   - Question: "Is 220 tables in sample schema (one per endpoint) the most efficient way?"
   - Requirement: Needs validation

---

## Next Steps

1. Update `METHODOLOGY-EVOLUTION.md` with user commentary definitions
2. Update all references to 6-stage pattern → 7-stage pattern
3. Document Clean stage (entity separation, flattening)
4. Document Transform stage (dimensional modeling)
5. Document Refine stage (enrichment only)
6. Update Prepare stage (sample schema, star schema intelligence)
7. Update Extract stage (endpoint selection, file structure)
8. Address open questions (historical data, sample efficiency)

---

## Version History

- **v1.0** (2025-12-11): Initial comparison between documented methodology and user commentary

---

## References

- **Current Methodology:** `docs/methodology/METHODOLOGY-EVOLUTION.md`
- **User Preferences:** `.spectra/preferences/pipeline-engine-preferences.yaml`
- **User Commentary:** Voice review 2025-12-11




