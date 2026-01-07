# Prepare Stage Design Comparison

**Status:** 🟢 Complete  
**Version:** 1.0.0  
**Date:** 2025-12-06  
**Objective:** Compare fresh SPECTRA-grade design with Jira-based approach

---

## 🎯 Purpose

This document compares two approaches to the Prepare stage:

1. **Fresh SPECTRA-Grade Design** (`PREPARE-STAGE-FRESH-DESIGN.md`)
   - Designed from first principles
   - Applies SPECTRA brand pillars
   - No legacy constraints

2. **Jira-Based Design** (`PREPARE-STAGE-SCHEMA-DESIGN.md`)
   - Based on existing Jira pattern
   - Adapted from proven implementation
   - Includes legacy considerations

---

## 📊 Design Comparison Matrix

| Aspect | Fresh SPECTRA-Grade | Jira-Based | Winner | Notes |
|--------|---------------------|------------|--------|-------|
| **Separation of Concerns** | 5 atomic tables (schema, entities, mappings, controls, relationships) | 3 mixed tables (`_schema`, `_endpoints`, `_statusMap`) | 🟢 Fresh | Fresh design has clearer separation |
| **Entity Metadata** | Explicit entity-level metadata in `prepare.entities` | Entity metadata embedded in schema rows | 🟢 Fresh | Fresh design separates entity from field concerns |
| **Relationship Declaration** | Explicit `prepare.relationships` table | Relationships inferred from field mappings | 🟢 Fresh | Explicit relationships are clearer |
| **Control Parameters** | Dedicated `prepare.controls` table | Controls mixed in schema/config | 🟢 Fresh | Cleaner separation of control values |
| **Mapping Clarity** | Dedicated `prepare.mappings` table | Mappings embedded in schema | 🟢 Fresh | Mappings are first-class citizens |
| **Simplicity** | 5 tables to maintain | 3 tables to maintain | 🟡 Jira | Fewer tables = simpler operations |
| **Field-Level Detail** | Comprehensive field metadata | Comprehensive field metadata | 🟡 Tie | Both have good field-level coverage |
| **Downstream Mapping** | Explicit dimension/fact/bridge mappings | Explicit dimension/fact/bridge mappings | 🟡 Tie | Both support dimensional model mapping |
| **Validation Rules** | Self-validating metadata structure | Schema coherence validation | 🟡 Tie | Both support validation |
| **Autonomy Support** | Metadata enables autonomous execution | Metadata supports automation | 🟡 Tie | Both enable automation |
| **Proven Pattern** | New design (untested) | Based on working Jira implementation | 🟡 Jira | Jira has proven track record |
| **SPECTRA Alignment** | Built on SPECTRA principles | Adapted from external pattern | 🟢 Fresh | Fresh design more aligned with SPECTRA |

---

## 🔍 Detailed Comparison

### 1. Metadata Structure

#### Fresh Design: 5 Atomic Tables

```
prepare.schema        → Field-level metadata
prepare.entities      → Entity-level metadata
prepare.mappings      → Source → Target mappings
prepare.controls      → Pipeline control parameters
prepare.relationships → Entity relationships
```

**Advantages:**
- Clear separation of concerns
- Each table has one job
- Easy to extend individually
- Explicit entity definitions

**Disadvantages:**
- More tables to maintain
- More joins required for complete picture
- Higher initial complexity

#### Jira Design: 3 Mixed Tables

```
prepare._schema       → Field metadata + mappings + relationships
prepare._endpoints    → API endpoint configurations
prepare._statusMap    → Status mappings
```

**Advantages:**
- Fewer tables to manage
- All field info in one place
- Proven pattern (works in Jira)
- Simpler queries for field-level info

**Disadvantages:**
- Mixed concerns in single table
- Entity metadata not explicit
- Relationships inferred, not declared
- Control parameters mixed in

---

### 2. Entity-Level Metadata

#### Fresh Design: `prepare.entities` Table

Explicit entity definitions with:
- Entity type (dimension, fact, bridge)
- Source endpoint
- Extraction method
- Watermark configuration
- Primary/natural keys
- Hierarchy information

**Example:**
```yaml
entity_name: "execution"
entity_type: "fact"
source_endpoint: "/cycles/{cycleId}/executions"
extraction_method: "incremental"
watermark_field: "lastModifiedDate"
primary_key: "execution_id"
business_activity: "Test execution"
grain: "one row per testcase-cycle execution"
```

#### Jira Design: Embedded in Schema

Entity information inferred from:
- Group/entity fields in `_schema`
- Endpoint configurations in `_endpoints`
- Field mappings in schema

**Example:**
- Entity name from `entity` field in schema rows
- Endpoint from `_endpoints` table lookup
- Extraction method from controls/config

---

### 3. Relationship Declaration

#### Fresh Design: `prepare.relationships` Table

Explicit relationship declarations:
```yaml
from_entity: "execution"
from_field: "cycle_id"
to_entity: "cycle"
to_field: "cycle_id"
relationship_type: "many_to_one"
is_required: true
cardinality: "N:1"
```

**Advantages:**
- Relationships are first-class metadata
- Easy to validate relationship integrity
- Clear join logic for downstream stages
- Supports bridge table declarations

#### Jira Design: Inferred from Schema

Relationships inferred from:
- Foreign key fields in schema (`dimensionName`, `keyField`)
- Field path patterns
- Entity groupings

**Advantages:**
- Less metadata to maintain
- Relationships "just work" from field definitions
- Fewer tables to query

**Disadvantages:**
- Relationships not explicit
- Harder to validate relationship completeness
- Join logic must be inferred

---

### 4. Control Parameters

#### Fresh Design: `prepare.controls` Table

Dedicated table for all control values:
```yaml
control_name: "last_extract_date"
control_type: "watermark"
control_value: "2025-12-01"
scope: "global"
description: "Last successful extraction date"
```

**Advantages:**
- All controls in one place
- Clear scope (global, entity, stage)
- Type-safe control values
- Easy to query all controls

#### Jira Design: Mixed in Config/Schema

Control values stored in:
- Pipeline parameters
- Variable Library
- Config tables
- Embedded in schema metadata

**Advantages:**
- Controls close to usage
- Flexible storage locations

**Disadvantages:**
- Controls scattered across locations
- Harder to get complete control picture
- No single source of truth

---

### 5. Source → Target Mappings

#### Fresh Design: `prepare.mappings` Table

Explicit mapping declarations:
```yaml
source_entity: "execution"
source_field_path: ["executionDate"]
target_type: "fact"
target_entity: "factExecution"
target_field: "execution_date"
transformation_type: "direct"
```

**Advantages:**
- Mappings are explicit and queryable
- Transformation rules documented
- Validation status tracked
- Easy to audit all mappings

#### Jira Design: Embedded in Schema

Mappings embedded in schema via:
- `rawField` → source path
- `targetField` → target path
- `dimensionName` → target table
- `bridgeName` → bridge table

**Advantages:**
- Field and mapping info together
- Less duplication
- Simpler structure

**Disadvantages:**
- Mappings not queryable separately
- Harder to validate mapping completeness
- Transformation rules less explicit

---

## 🎯 SPECTRA Principle Alignment

### Experience-First Impact

**Fresh Design:** ✅
- Self-documenting structure
- Clear table purposes
- Instantly readable metadata

**Jira Design:** 🟡
- Works but requires interpretation
- Mixed concerns reduce clarity

### Insight Over Everything

**Fresh Design:** ✅
- Explicit relationships reveal structure
- Entity definitions show scope
- Mappings show transformation intent

**Jira Design:** 🟡
- Structure requires inference
- Relationships not explicit

### Singular, Autonomous Genius

**Fresh Design:** ✅
- Explicit metadata enables autonomous execution
- Relationships declared for join logic
- Controls clearly scoped

**Jira Design:** 🟡
- Metadata supports automation
- Some inference required
- Controls scattered

### Modular to the Core

**Fresh Design:** ✅
- 5 atomic tables
- Each has one job
- Swappable components

**Jira Design:** 🟡
- 3 tables but mixed concerns
- Schema table does multiple jobs
- Less modular

### Self-Evolving Innovation

**Fresh Design:** ✅
- Versioned metadata structure
- Self-validating
- Auto-generation friendly

**Jira Design:** 🟡
- Supports evolution
- Less structured for auto-generation

### Neurodivergent By Design

**Fresh Design:** ✅
- Deterministic structure
- Predictable patterns
- Clear hierarchy

**Jira Design:** 🟡
- Works but has exceptions
- Some patterns require interpretation

---

## 🏆 Recommendation

### Hybrid Approach: Best of Both Worlds

**Core Structure (Fresh Design):**
- `prepare.entities` — Explicit entity definitions
- `prepare.relationships` — Explicit relationship declarations
- `prepare.controls` — Centralised control parameters

**Field Metadata (Jira Pattern):**
- `prepare.schema` — Comprehensive field-level metadata (single table)
- Keep field metadata together (simpler queries)

**Additional Tables (As Needed):**
- `prepare.endpoints` — API endpoint configurations (if complex)
- `prepare.statusMap` — Status mappings (if needed)

**Rationale:**
1. **Entity-level metadata** deserves its own table (Fresh design wins)
2. **Relationships** should be explicit (Fresh design wins)
3. **Controls** should be centralised (Fresh design wins)
4. **Field metadata** can be unified (Jira pattern simpler)
5. **Proven patterns** from Jira reduce risk

---

## 📋 Implementation Strategy

### Phase 1: Adopt Fresh Entity Structure

1. Create `prepare.entities` table
2. Create `prepare.relationships` table
3. Create `prepare.controls` table
4. Keep existing `prepare._schema` pattern (proven)

### Phase 2: Enhance Schema Table

1. Add explicit mapping fields to schema
2. Add transformation type fields
3. Keep all field metadata together

### Phase 3: Validation & Optimization

1. Validate relationship completeness
2. Ensure control parameter coverage
3. Optimize query patterns

---

## 📚 References

- **Fresh Design:** `Data/zephyr/docs/prepare/PREPARE-STAGE-FRESH-DESIGN.md`
- **Jira-Based Design:** `Data/zephyr/docs/prepare/PREPARE-STAGE-SCHEMA-DESIGN.md`
- **SPECTRA Principles:** `Core/standards/SPECTRA-GLOSSARY.md`
- **Brand Pillars:** `Data/branding/brandPillars.md`

