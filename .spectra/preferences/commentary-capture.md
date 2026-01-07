# Commentary Capture System

**Purpose:** Convert conversational user commentary into structured pipeline engine preferences

---

## How It Works

1. **User provides voice commentary** (what they like, what should be different)
2. **AI captures and structures** the commentary
3. **Maps to standards** and existing preferences
4. **Updates pipeline engine preferences** file
5. **Pipeline engine reads preferences** when building pipelines

---

## Commentary Format

User will provide conversational commentary like:
- "I like how the notebook has the SPECTRA branding"
- "The table names should not have underscores"
- "Logs should go to a central log schema"
- "I prefer British English spelling"

---

## Capture Process

### Step 1: Listen to Commentary
- User reviews workspace
- Provides voice feedback
- AI captures all commentary

### Step 2: Structure Commentary
- Extract preferences
- Identify standards references
- Map to existing standards

### Step 3: Update Preferences
- Add to `orchestrator-preferences.yaml`
- Link to standards documents
- Provide orchestrator instructions

### Step 4: Generate Links
- Orchestrator provides links to standards
- Links shown when building pipeline
- Ensures transparency

---

## Example Commentary → Preference

**User says:**
> "I really like how the notebook has the SPECTRA branding in the header. That should be standard."

**Captured as:**
```yaml
notebook_structure:
  header_format:
    style: "SPECTRA-branded markdown"
    branding: "SPECTRA-grade with emojis"
    reference: "docs/standards/NOTEBOOK-FORMATTING-STANDARD.md"
```

**Pipeline engine uses:**
- When creating notebooks, applies SPECTRA branding
- Provides link to formatting standard
- Validates against preference

---

## Preference Categories

### 1. **Notebook Structure**
- Header format
- Cell structure
- Code style

### 2. **Naming Conventions**
- Table names
- Schema names
- File names

### 3. **Playbook Structure**
- Pattern (hybrid/orchestration/granular)
- Atomicity
- Purpose

### 4. **Standards Compliance**
- British English
- SPECTRA-grade quality
- Documentation requirements

### 5. **Integration Patterns**
- Variable access
- API integration
- Logging

---

## Standards Mapping

Each preference links to:
- **Standards document** (where it's defined)
- **Playbook** (how to apply it)
- **Example** (reference implementation)

---

## Pipeline Engine Integration

The pipeline engine will:
1. **Read preferences** from `pipeline-engine-preferences.yaml`
2. **Apply standards** when building pipelines
3. **Generate links** to standards documents
4. **Validate** against preferences
5. **Capture gaps** when preferences not met

---

## Version History

- **v1.0** (2025-12-11): Initial commentary capture system

---

## Next Steps

1. User provides voice commentary
2. AI structures and captures preferences
3. Update `pipeline-engine-preferences.yaml`
4. Pipeline engine reads and applies preferences
5. Pipeline built exactly as desired

