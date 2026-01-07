# Zephyr Prepare Stage - Fresh SPECTRA-Grade Design

**Status:** 🟢 Design Phase  
**Version:** 1.0.0  
**Date:** 2025-12-06  
**Objective:** Design Prepare stage from first principles, applying SPECTRA-grade standards

---

## 🎯 Purpose

The Prepare stage is the **metadata foundation** for a metadata-driven pipeline. It declares the contract between what the source system provides and what downstream stages expect, enabling autonomous execution without manual intervention.

**Core Principle:** Prepare is **pure metadata** — no data, no logic, no execution. It's the blueprint that tells downstream stages **what to do**, not **how to do it**.

---

## 🧠 SPECTRA Principles Applied

### 1. **Experience-First Impact**

- Metadata should be instantly readable by humans and machines
- Self-documenting structure that reveals purpose immediately
- Zero ambiguity — every field has a clear, singular purpose

### 2. **Insight Over Everything**

- Schema reveals the data structure at a glance
- Relationships are explicit, not inferred
- The "why" is embedded in the metadata

### 3. **Singular, Autonomous Genius**

- Metadata enables AI agents to execute stages autonomously
- No manual interpretation required
- Machines can validate, generate code, and execute from metadata alone

### 4. **Modular to the Core**

- Each metadata table has one job
- No coupling between metadata artifacts
- Swappable, atomic metadata components

### 5. **Self-Evolving Innovation**

- Metadata can be auto-generated from source discovery
- Self-validating structure (schema validates schema)
- Versioned for evolution tracking

### 6. **Neurodivergent By Design**

- Deterministic structure (same input = same output)
- Predictable patterns (no exceptions)
- Clear hierarchy and organisation

---

## 📋 What Should Prepare Stage Contain?

Based on SPECTRA principles, Prepare should contain **ONLY**:

1. **Schema Metadata** — Field definitions, types, structure
2. **Mapping Metadata** — Source → Target field mappings
3. **Control Metadata** — Extraction modes, watermarks, feature flags
4. **Relationship Metadata** — Entity relationships, hierarchies
5. **Quality Metadata** — Validation rules, constraints, defaults

**What Prepare should NOT contain:**

- ❌ Raw data
- ❌ Calculated values
- ❌ Business logic
- ❌ Execution state
- ❌ Secrets or credentials

---

## 🏗️ Metadata Structure Design

### Core Tables (Minimal Viable Metadata)

#### 1. `prepare.schema` — Field-Level Metadata

**Purpose:** Define every field in every entity with complete type, structure, and semantic information.

**Grain:** One row per field per entity

**Key Attributes:**

- `entity_name` (string): Entity identifier (e.g., "project", "execution")
- `field_path` (array<string>): JSON path to field (e.g., ["id"], ["dates", "startDate"])
- `field_type` (enum): `scalar` | `record` | `array` | `nested_array`
- `data_type` (enum): `text` | `integer` | `float` | `boolean` | `date` | `datetime` | `json`
- `is_required` (boolean): Field must be present
- `is_nullable` (boolean): Field can be null
- `default_value` (string): Default if missing
- `description` (string): Human-readable description
- `source_location` (string): Where field comes from (API endpoint, response path)
- `target_location` (string): Where field goes (table, column, bridge)

**Semantic Metadata:**

- `is_identifier` (boolean): Primary/foreign key indicator
- `is_timestamp` (boolean): Temporal field indicator
- `is_measure` (boolean): Quantitative value indicator
- `semantic_label` (string): Business meaning (e.g., "project_name", "execution_status")
- `pii_level` (enum): `public` | `internal` | `confidential` | `restricted`

**Relationship Metadata:**

- `references_entity` (string): Foreign key target entity
- `references_field` (string): Foreign key target field
- `creates_bridge` (boolean): Creates bridge table (for arrays)
- `bridge_table_name` (string): Bridge table name (if applicable)

**Downstream Mapping:**

- `dimension_table` (string): Target dimension table (if applicable)
- `fact_table` (string): Target fact table (if applicable)
- `bridge_table` (string): Target bridge table (if applicable)
- `column_name` (string): Target column name in destination

---

#### 2. `prepare.entities` — Entity-Level Metadata

**Purpose:** Define entities, their boundaries, and their role in the pipeline.

**Grain:** One row per entity

**Key Attributes:**

- `entity_name` (string): Entity identifier
- `entity_type` (enum): `dimension` | `fact` | `bridge` | `reference`
- `source_endpoint` (string): API endpoint for extraction
- `extraction_method` (enum): `full` | `incremental` | `snapshot` | `delta`
- `watermark_field` (string): Field used for incremental extraction
- `primary_key` (string): Primary key field name
- `natural_key` (string): Business key (if different from PK)
- `hierarchical` (boolean): Entity has parent-child relationships
- `parent_entity` (string): Parent entity name (if hierarchical)
- `parent_key_field` (string): Foreign key to parent

**Metadata:**

- `description` (string): Entity purpose and scope
- `business_activity` (string): What business activity this represents
- `grain` (string): Fact table grain (e.g., "one row per execution")
- `refresh_frequency` (string): How often entity updates

---

#### 3. `prepare.mappings` — Source → Target Mappings

**Purpose:** Explicit mappings between source fields and target structures.

**Grain:** One row per source→target mapping

**Key Attributes:**

- `source_entity` (string): Source entity name
- `source_field_path` (array<string>): Source field path
- `target_type` (enum): `dimension` | `fact` | `bridge`
- `target_entity` (string): Target entity/table name
- `target_field` (string): Target field/column name
- `transformation_type` (enum): `direct` | `flatten` | `aggregate` | `derive`
- `transformation_rule` (string): Transformation logic (if derive)

**Validation:**

- `is_validated` (boolean): Mapping has been validated
- `validation_date` (datetime): Last validation timestamp

---

#### 4. `prepare.controls` — Pipeline Control Parameters

**Purpose:** Static control values that govern pipeline execution.

**Grain:** One row per control parameter

**Key Attributes:**

- `control_name` (string): Parameter identifier
- `control_type` (enum): `watermark` | `flag` | `threshold` | `config`
- `control_value` (string): Parameter value (JSON for complex)
- `scope` (enum): `global` | `entity` | `stage`
- `entity_name` (string): Entity scope (if entity-specific)
- `stage_name` (string): Stage scope (if stage-specific)
- `description` (string): Parameter purpose

**Examples:**

- `last_extract_date` (watermark, global)
- `enable_incremental` (flag, entity: execution)
- `max_batch_size` (threshold, stage: extract)
- `test_project_id` (config, entity: project)

---

#### 5. `prepare.relationships` — Entity Relationships

**Purpose:** Explicit declaration of entity relationships for join logic.

**Grain:** One row per relationship

**Key Attributes:**

- `from_entity` (string): Source entity
- `from_field` (string): Source field (foreign key)
- `to_entity` (string): Target entity
- `to_field` (string): Target field (primary key)
- `relationship_type` (enum): `one_to_one` | `one_to_many` | `many_to_many`
- `is_required` (boolean): Relationship must exist
- `cardinality` (string): Expected cardinality (e.g., "1..\*")

**Bridge Relationships:**

- `bridge_table` (string): Bridge table name (if many-to-many)
- `bridge_from_field` (string): Bridge source field
- `bridge_to_field` (string): Bridge target field

---

## 🔄 Metadata Lifecycle

### 1. **Discovery** (Source Stage)

- API endpoints catalogued
- Sample data extracted
- Schema inferred from samples

### 2. **Declaration** (Prepare Stage)

- Schema metadata created
- Mappings defined
- Controls set
- Relationships declared

### 3. **Validation** (Prepare Stage)

- Schema coherence checks
- Mapping completeness
- Relationship integrity
- Control parameter validation

### 4. **Execution** (Downstream Stages)

- Extract uses schema + endpoints
- Clean uses schema + validation rules
- Transform uses mappings + relationships
- Refine uses mappings + dimensional model

---

## 📐 Schema Design Principles

### 1. **Atomic Metadata**

Each metadata table has one, clear purpose. No mixing of concerns.

### 2. **Explicit, Not Implicit**

Nothing is inferred. Everything is declared.

### 3. **Versioned**

Metadata evolves. Track versions for reproducibility.

### 4. **Validatable**

Schema validates schema. Metadata can validate itself.

### 5. **Machine-Executable**

AI agents can read metadata and generate code automatically.

---

## 🎯 Comparison Points

When comparing this fresh design to Jira's approach, consider:

1. **Separation of Concerns**

   - Fresh: 5 atomic tables (schema, entities, mappings, controls, relationships)
   - Jira: Mixed concerns in `_schema` table

2. **Explicitness**

   - Fresh: Explicit relationship declarations
   - Jira: Relationships inferred from field mappings

3. **Autonomy**

   - Fresh: Metadata enables autonomous execution
   - Jira: Requires manual interpretation

4. **Clarity**
   - Fresh: Entity-level metadata separate from field-level
   - Jira: All metadata in one table

---

## 🚀 Next Steps

1. ✅ Define metadata structure (this document)
2. ⏳ Design metadata validation rules
3. ⏳ Create metadata generation utilities
4. ⏳ Compare with Jira approach
5. ⏳ Choose best elements from both

---

## 📚 References

- **SPECTRA Principles:** `Core/standards/SPECTRA-GLOSSARY.md`
- **Brand Pillars:** `Data/branding/brandPillars.md`
- **Jira Pattern:** `Data/jira/docs/methodology/2-prepare/prepare.md`
- **Zephyr Research:** `Data/zephyr/docs/ZEPHYR-RESEARCH-SUMMARY.md`
