# Playbook Design Principles - Plain English Translation

**Date:** 2025-12-08  
**Purpose:** Translate technical terms into plain English with examples from existing playbooks

---

## 🎯 What You're Asking For (Translation)

You want each playbook to be:

1. **Idempotent** = "Safe to run multiple times - won't break if already done"
2. **Orthogonal** = "Each playbook does ONE thing and doesn't overlap with others"
3. **Deterministic** = "Same inputs always produce same results - no surprises"
4. **Modular** = "Each playbook is self-contained and can work independently"
5. **Separation of Concerns** = "Clear boundaries - each playbook has a single responsibility"

---

## 📚 Detailed Explanations with Examples

### 1. **Idempotent** = "Safe to Run Again"

**Plain English:** 
> "If I run this playbook twice, the second time should either:
> - Do nothing (because it's already done)
> - Or safely update/replace what exists
> 
> **Never** should it break, create duplicates, or cause errors."

**Example from `setup.005-createFabricPipeline.md`:**

```powershell
# ✅ IDEMPOTENT: Checks if exists first
if (-not (fab exists $pipelinePath)) {
  fab mkdir $pipelinePath -P description="$description"
} else {
  Write-Host "Pipeline $pipelineName already exists; skipping creation."
}
```

**What makes it idempotent:**
- ✅ Checks `fab exists` first
- ✅ Only creates if doesn't exist
- ✅ Skips if already exists (safe to run again)
- ✅ No error if pipeline already exists

**❌ NOT Idempotent (bad example):**
```powershell
# ❌ BAD: Will fail if pipeline already exists
fab mkdir $pipelinePath -P description="$description"
# Error: Pipeline already exists!
```

**For New Playbooks:**
- Always check if artifact exists before creating
- Use "if not exists" patterns
- Provide "skip if done" behavior
- Never assume starting from scratch

---

### 2. **Orthogonal** = "One Thing, No Overlap"

**Plain English:**
> "Each playbook does EXACTLY one job and doesn't step on other playbooks' toes.
> 
> Playbooks should be like puzzle pieces - each fits one spot, no overlap."

**Example from Existing Playbooks:**

| Playbook | Does ONE Thing | Doesn't Touch |
|----------|----------------|---------------|
| `source.001` | Creates notebook artifact | Doesn't wire it to pipeline |
| `source.002` | Wires notebook to pipeline | Doesn't create notebook (assumes `.001` did it) |
| `source.003` | Bootstraps endpoints | Doesn't create notebook or wire pipeline |

**✅ Orthogonal Pattern:**

```
source.001 → Creates notebook
    ↓ (depends on .001)
source.002 → Wires notebook to pipeline
    ↓ (depends on .001, .002)
source.003 → Bootstraps endpoints (uses notebook from .001)
```

**Each playbook:**
- Has ONE clear purpose
- Has clear dependencies (what must exist first)
- Doesn't duplicate work from other playbooks
- Can be run independently (after dependencies met)

**❌ NOT Orthogonal (bad example):**

```
source.001 → Creates notebook AND wires it to pipeline AND bootstraps endpoints
# ❌ Too many responsibilities - violates "one thing"
```

**For New Playbooks:**
- Each playbook = ONE specific task
- Clear "depends on" section
- Don't duplicate functionality from other playbooks
- Can be run standalone (if dependencies exist)

---

### 3. **Deterministic** = "Predictable Results"

**Plain English:**
> "Same inputs = Same outputs, every time.
> 
> No randomness, no "maybe this, maybe that" - always the same result."

**Example from `source.001-createSourceNotebook.md`:**

```powershell
# ✅ DETERMINISTIC: Clear inputs, predictable outputs
$workspace = "<sourceKey>.Workspace"  # ← Input
$notebookName = "source<SourceKey>"   # ← Input
fab mkdir "$workspace/$notebookName.Notebook"  # ← Always creates same thing
```

**What makes it deterministic:**
- ✅ Same `sourceKey` always produces same notebook name
- ✅ No random IDs or timestamps in names
- ✅ Clear formula: `source<SourceKey>` = predictable
- ✅ Same command always creates same artifact

**❌ NOT Deterministic (bad example):**

```powershell
# ❌ BAD: Random name each time
$randomId = Get-Random
$notebookName = "notebook-$randomId"  # ← Different name each run!
```

**For New Playbooks:**
- Use predictable naming (from contract.yaml, not random)
- Same inputs → same outputs
- Document all variables that affect behavior
- No "maybe" or "sometimes" logic

---

### 4. **Modular** = "Self-Contained Pieces"

**Plain English:**
> "Each playbook is like a LEGO brick - complete on its own, but connects with others.
> 
> You can understand and run each playbook without reading all the others."

**Example Structure:**

```markdown
# source.002 - addNotebookToPipeline

## dependencies
- `source.001` (notebook created)  ← Clear what it needs
- `setup.005` (pipeline exists)    ← Clear prerequisites

## produces
pipelineNotebookBinding:          ← Clear what it creates
  notebookId: "{notebookLogicalId}"
  status: "wired"
```

**What makes it modular:**
- ✅ Self-contained (all info in one file)
- ✅ Clear prerequisites (dependencies section)
- ✅ Clear outputs (produces section)
- ✅ Can understand without reading other playbooks

**For New Playbooks:**
- Include all context needed in the playbook
- Document dependencies clearly
- Document outputs clearly
- Don't assume reader knows other playbooks

---

### 5. **Separation of Concerns** = "Clear Job Boundaries"

**Plain English:**
> "Each playbook has ONE job and does it well.
> 
> Like a restaurant: one person takes orders, another cooks, another serves - clear boundaries."

**Example Separation:**

| Playbook | Concern (Job) | Boundary |
|----------|---------------|----------|
| `source.001` | **Create** notebook artifact | Stops after notebook exists in Fabric |
| `source.002` | **Wire** notebook to pipeline | Only connects, doesn't create |
| `source.003` | **Bootstrap** endpoints | Only handles endpoints, doesn't touch notebook creation |

**Clear Boundaries:**

```
source.001: CREATE notebook
    ↓
source.002: WIRE notebook (different concern - connection)
    ↓
source.003: BOOTSTRAP endpoints (different concern - data)
```

**❌ Poor Separation (bad example):**

```
source.001: CREATE notebook, WIRE to pipeline, BOOTSTRAP endpoints
# ❌ Too many concerns mixed together
```

**For New Playbooks:**
- One playbook = one concern
- If it does multiple things, split into multiple playbooks
- Clear "where I start, where I stop" boundaries

---

## 🔍 Pattern Analysis: Existing Playbooks

### ✅ What They Do Well

**1. Idempotent:**
- `source.003` checks prerequisites before acting
- `setup.005` checks `fab exists` before creating

**2. Orthogonal:**
- `source.001` only creates notebook
- `source.002` only wires (assumes notebook exists)
- `source.003` only bootstraps (assumes notebook + pipeline exist)

**3. Deterministic:**
- Naming patterns are formulaic: `source<SourceKey>`
- Parameters come from `contract.yaml` (predictable)
- No random elements

**4. Modular:**
- Each playbook has dependencies section
- Each playbook has produces section
- Can understand each playbook independently

**5. Separation of Concerns:**
- Clear job boundaries between playbooks
- Each does one thing

---

## ⚠️ What Could Be Improved

### 1. **Idempotency Gaps**

**`source.001` - Missing checks:**
```markdown
# Current: Assumes notebook doesn't exist
fab mkdir "$workspace/$notebookName.Notebook"

# ✅ Should be:
if (-not (fab exists "$workspace/$notebookName.Notebook")) {
  fab mkdir "$workspace/$notebookName.Notebook"
} else {
  Write-Host "Notebook already exists; skipping creation."
}
```

**`source.002` - Missing checks:**
```markdown
# Current: Assumes pipeline activity doesn't exist
# ✅ Should check if already wired before wiring
```

### 2. **Deterministic Gaps**

**`source.003` - Some manual steps:**
```markdown
# Step 4: Update Source notebook activity
# ⚠️ Manual JSON editing - could be more deterministic
# ✅ Should provide exact JSON snippet or script
```

---

## 📋 Checklist for New Playbooks

### ✅ Idempotent Checklist

- [ ] Check if artifact exists before creating
- [ ] Skip gracefully if already done
- [ ] Can run multiple times safely
- [ ] No errors if artifact already exists

**Template Pattern:**
```powershell
if (-not (fab exists $artifactPath)) {
  # Create artifact
} else {
  Write-Host "Already exists; skipping."
}
```

---

### ✅ Orthogonal Checklist

- [ ] Does ONE specific thing
- [ ] Doesn't duplicate work from other playbooks
- [ ] Clear dependencies listed
- [ ] Doesn't step on other playbooks' concerns

**Questions to Ask:**
- "Does this playbook do only ONE job?" → Yes/No
- "Can I skip this playbook and still run others?" → Should be Yes
- "Does this overlap with another playbook?" → Should be No

---

### ✅ Deterministic Checklist

- [ ] Same inputs → same outputs
- [ ] No random elements in names/IDs
- [ ] Predictable naming patterns
- [ ] All variables documented

**Questions to Ask:**
- "If I run this twice with same inputs, same result?" → Yes
- "Are there any random/date-based names?" → Should be No
- "Can I predict what will be created?" → Should be Yes

---

### ✅ Modular Checklist

- [ ] Self-contained (all context in playbook)
- [ ] Clear dependencies section
- [ ] Clear produces section
- [ ] Can understand without reading other playbooks

**Template:**
```markdown
## dependencies
- `playbook.number` (what must exist first)

## produces
artifact:
  name: "{what gets created}"
  status: "{expected state}"
```

---

### ✅ Separation of Concerns Checklist

- [ ] ONE clear job/purpose
- [ ] Clear start boundary (dependencies)
- [ ] Clear stop boundary (produces)
- [ ] Doesn't mix multiple concerns

**Questions to Ask:**
- "What is this playbook's ONE job?" → Should be clear
- "Where does this playbook's responsibility start?" → Should be clear
- "Where does it stop?" → Should be clear

---

## 🎯 Summary Translation

| Technical Term | Plain English | Example |
|----------------|---------------|---------|
| **Idempotent** | "Safe to run again" | `if (not exists) { create } else { skip }` |
| **Orthogonal** | "One thing, no overlap" | `.001` creates, `.002` wires (separate jobs) |
| **Deterministic** | "Predictable results" | Same `sourceKey` → same notebook name |
| **Modular** | "Self-contained piece" | Can understand `.002` without reading `.001` |
| **Separation of Concerns** | "Clear job boundaries" | Each playbook = one responsibility |

---

**Version:** 1.0.0  
**Status:** 🟢 Translation Complete

