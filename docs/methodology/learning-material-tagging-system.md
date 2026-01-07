# Learning Material Tagging System

**Date:** 2025-12-11  
**Status:** 🎯 Design Phase  
**Purpose:** Tag content with learning material metadata as we build, enabling organic academy syllabus creation

---

## Vision

**"Build the academy syllabus organically by tagging everything we do"**

**Goal:** As we build the framework, tag content with learning material metadata. When building the academy, simply query for tagged items and assemble the syllabus automatically.

---

## How It Works

### **1. Tag Content as We Build**

Every document, playbook, standard, or code module can be tagged with:

```yaml
learning_material:
  is_learning_material: true
  education_level: "L1"  # L1-MVP through L7-Autonomous
  topic: "pipeline-stages"
  category: "methodology"
  prerequisites: ["source-stage", "prepare-stage"]
  learning_objectives:
    - "Understand the 7-stage SPECTRA pipeline"
    - "Know what each stage does"
    - "Understand stage dependencies"
  estimated_time: "15 minutes"
  format: "concept-explanation"
```

### **2. Query for Academy Content**

When building the academy:

```python
# Query cosmic index for learning materials
learning_materials = cosmic_index.query(
    learning_material.is_learning_material == True,
    education_level == "L1"
)

# Assemble syllabus automatically
syllabus = assemble_syllabus(learning_materials)
```

### **3. Automatic Syllabus Generation**

The academy can:
- Query all tagged learning materials
- Filter by education level
- Organise by topic/category
- Build prerequisite chains
- Generate learning paths

---

## Metadata Schema

### **Learning Material Metadata**

```yaml
learning_material:
  # Basic flags
  is_learning_material: boolean  # Is this educational content?
  is_example: boolean  # Is this an example/case study?
  is_exercise: boolean  # Is this a hands-on exercise?
  is_reference: boolean  # Is this reference material?
  
  # Education level (SPECTRA Seven Levels)
  education_level: string  # "L1" | "L2" | "L3" | "L4" | "L5" | "L6" | "L7"
  education_level_name: string  # "MVP" | "Alpha" | "Beta" | "Live" | "Reactive" | "Proactive" | "Autonomous"
  
  # Topic classification
  topic: string  # "pipeline-stages" | "notebook-formatting" | "playbook-structure"
  category: string  # "methodology" | "standards" | "playbooks" | "code-patterns"
  subcategory: string  # Optional: more specific classification
  
  # Learning path
  prerequisites: array<string>  # Topics/IDs that must be learned first
  leads_to: array<string>  # Topics/IDs this enables
  part_of_series: string  # If part of a series (e.g., "7-stages-series")
  series_order: integer  # Order within series
  
  # Learning objectives
  learning_objectives: array<string>  # What will student learn?
  key_concepts: array<string>  # Key concepts covered
  
  # Practical info
  estimated_time: string  # "15 minutes" | "1 hour" | "2 hours"
  difficulty: string  # "beginner" | "intermediate" | "advanced"
  format: string  # "concept-explanation" | "tutorial" | "reference" | "example"
  
  # Assessment
  has_assessment: boolean  # Does this have quiz/exercise?
  assessment_type: string  # "quiz" | "hands-on" | "project"
  
  # Resources
  related_materials: array<string>  # Links to related learning materials
  code_examples: array<string>  # Links to code examples
  playbook_references: array<string>  # Links to playbooks
```

---

## Integration with Cosmic Index

### **Add to Cosmic Metadata**

The cosmic index already has metadata fields. Add learning material fields:

```yaml
# Existing cosmic coordinates
org: "Core"
angle: 0
depth: 0
sphere: 0
energy: 1.0
stage: null
thought_lane: "standards"

# NEW: Learning material metadata
learning_material:
  is_learning_material: true
  education_level: "L1"
  topic: "pipeline-stages"
  category: "methodology"
  # ... etc
```

### **Query Examples**

```python
# Get all L1 learning materials
l1_materials = cosmic_index.query(
    learning_material.is_learning_material == True,
    learning_material.education_level == "L1"
)

# Get all methodology learning materials
methodology = cosmic_index.query(
    learning_material.is_learning_material == True,
    learning_material.category == "methodology"
)

# Get learning path for pipeline stages
pipeline_path = cosmic_index.query(
    learning_material.is_learning_material == True,
    learning_material.topic == "pipeline-stages"
).sort_by("series_order")
```

---

## Tagging Standards

### **Where to Tag**

1. **Documentation files** (`.md` files):
   - Frontmatter YAML block
   - Or separate `.learning.yaml` file

2. **Playbooks**:
   - Frontmatter in playbook file
   - Or in playbook registry

3. **Code modules**:
   - Docstring metadata
   - Or separate `.learning.yaml` file

4. **Standards documents**:
   - Frontmatter YAML
   - Or in standards registry

### **Tagging Format**

**Option 1: Frontmatter (Recommended)**

```markdown
---
learning_material:
  is_learning_material: true
  education_level: "L1"
  topic: "pipeline-stages"
  category: "methodology"
  learning_objectives:
    - "Understand the 7-stage SPECTRA pipeline"
    - "Know what each stage does"
  estimated_time: "15 minutes"
  format: "concept-explanation"
---

# SPECTRA Pipeline Stages - Simple Explanation
...
```

**Option 2: Separate File**

```
docs/methodology/STAGES-SIMPLE-EXPLANATION.md
docs/methodology/STAGES-SIMPLE-EXPLANATION.learning.yaml
```

---

## Education Levels (SPECTRA Seven Levels)

Map to SPECTRA maturity levels:

| Level | Name | Education Level | Description |
|-------|------|-----------------|-------------|
| L1 | MVP | Beginner | Basic concepts, getting started |
| L2 | Alpha | Beginner+ | Understanding patterns |
| L3 | Beta | Intermediate | Applying patterns |
| L4 | Live | Intermediate+ | Production-ready knowledge |
| L5 | Reactive | Advanced | Optimisation and monitoring |
| L6 | Proactive | Advanced+ | Intelligence and prediction |
| L7 | Autonomous | Expert | Full autonomy and mastery |

---

## Example: Tagging the Stages Explanation

```yaml
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
  part_of_series: "spetra-pipeline-fundamentals"
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
---

# SPECTRA Pipeline Stages - Simple Explanation
...
```

---

## Academy Syllabus Generation

### **Automatic Syllabus Assembly**

```python
def generate_academy_syllabus(education_level: str):
    # Query all learning materials for this level
    materials = cosmic_index.query(
        learning_material.is_learning_material == True,
        learning_material.education_level == education_level
    )
    
    # Organise by topic
    by_topic = group_by(materials, "topic")
    
    # Build learning paths (respect prerequisites)
    learning_paths = build_learning_paths(materials)
    
    # Generate syllabus
    syllabus = {
        "level": education_level,
        "topics": by_topic,
        "learning_paths": learning_paths,
        "estimated_total_time": sum(m.estimated_time for m in materials)
    }
    
    return syllabus
```

### **Learning Path Example**

```
L1 - MVP Fundamentals:
  1. Pipeline Stages (15 min) → Prerequisites: None
  2. Notebook Formatting (20 min) → Prerequisites: Pipeline Stages
  3. Playbook Structure (15 min) → Prerequisites: Pipeline Stages
  4. Source Stage (30 min) → Prerequisites: Pipeline Stages, Notebook Formatting
  ...
```

---

## Benefits

1. **Organic Growth:** Academy builds as framework builds
2. **No Duplication:** Content is the learning material
3. **Automatic:** Syllabus generation is automatic
4. **Queryable:** Easy to find learning materials
5. **Level-Based:** Aligned with SPECTRA maturity levels
6. **Prerequisite Tracking:** Learning paths respect dependencies

---

## Implementation Plan

### **Phase 1: Metadata Schema**
1. Define learning material metadata schema
2. Add to cosmic index metadata structure
3. Create tagging standards

### **Phase 2: Tagging Tools**
1. Create tagging helper script
2. Add validation for learning material metadata
3. Create query tools for academy

### **Phase 3: Academy Integration**
1. Build academy syllabus generator
2. Query cosmic index for learning materials
3. Generate learning paths
4. Build academy UI

---

## Example Tags for Current Content

### **Stages Explanation**
- `is_learning_material: true`
- `education_level: "L1"`
- `topic: "pipeline-stages"`
- `category: "methodology"`

### **Notebook Formatting Standard**
- `is_learning_material: true`
- `education_level: "L2"`
- `topic: "notebook-formatting"`
- `category: "standards"`

### **Playbook Structure Analysis**
- `is_learning_material: true`
- `education_level: "L3"`
- `topic: "playbook-structure"`
- `category: "playbooks"`

---

## Version History

- **v1.0** (2025-12-11): Initial design for learning material tagging system

---

## References

- **Seven Levels:** `Core/doctrine/THE-SEVEN-LEVELS-OF-MATURITY.md`
- **Cosmic Index:** `Core/memory/cosmos/METADATA-NAVIGATION.md`
- **Stages Explanation:** `docs/methodology/STAGES-SIMPLE-EXPLANATION.md`




