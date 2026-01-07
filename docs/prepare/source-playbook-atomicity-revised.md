# Source Stage Playbook Atomicity Analysis (Revised)

**Date:** 2025-12-11  
**Purpose:** Infer missing playbooks for **pipeline construction**, not runtime execution

---

## Key Insight

**Playbooks are for BUILDING the pipeline, not RUNNING it.**

- ✅ **Playbooks:** Infrastructure setup, configuration, validation of setup
- ❌ **NOT Playbooks:** Runtime operations (these are handled by notebook with parameters)

**Runtime operations** (normal run, bootstrap, preview) are **parameters** within the notebook, not separate playbooks.

---

## What Playbooks Should Cover

### **Pipeline Construction Operations:**
1. ✅ Create notebook artifact (infrastructure)
2. ✅ Wire notebook to pipeline (infrastructure)
3. ✅ Configure endpoints bootstrap (metadata setup)
4. ✅ Validate pipeline setup (quality gates)

### **NOT Playbooks (Runtime Operations):**
- ❌ Create runtime metadata tables (happens during execution)
- ❌ Validate authentication (runtime with parameters)
- ❌ Validate hierarchical access (runtime with parameters)
- ❌ Comprehensive endpoint health check (runtime with parameters)
- ❌ Extract preview samples (runtime with `preview=True` parameter)
- ❌ Create quality gate report (runtime operation)

---

## Current Playbooks (3)

### **✅ source.001 - Create Source Notebook**
**Responsibility:** Infrastructure setup - create notebook artifact  
**Atomicity:** ✅ Perfect - Single responsibility, independently executable  
**Inputs:** Workspace, lakehouse, pipeline  
**Outputs:** Notebook artifact with `.platform` file  
**Purpose:** **Pipeline construction** - creates the notebook artifact

---

### **✅ source.002 - Add Notebook to Pipeline**
**Responsibility:** Infrastructure setup - wire notebook to pipeline  
**Atomicity:** ✅ Perfect - Single responsibility, independently executable  
**Inputs:** Notebook logicalId, workspaceId, pipeline  
**Outputs:** Pipeline activity configured  
**Purpose:** **Pipeline construction** - wires notebook into pipeline

---

### **✅ source.003 - Bootstrap Endpoints**
**Responsibility:** Metadata setup - configure endpoints bootstrap  
**Atomicity:** ✅ Perfect - Single responsibility, independently executable  
**Inputs:** Endpoints JSON, pipeline parameters  
**Outputs:** Pipeline configured for endpoints bootstrap (`init_mode` parameter)  
**Purpose:** **Pipeline construction** - configures pipeline to bootstrap endpoints

**Note:** The actual bootstrap execution happens at runtime with `init_mode=True` parameter.

---

## Missing Playbooks (1)

### **❌ source.004 - Validate Source Stage Setup**
**Responsibility:** Quality gates - validate source stage pipeline setup is complete  
**Atomicity:** ✅ Perfect - Single responsibility (setup validation)  
**Inputs:** Notebook exists, pipeline configured, parameters defined  
**Outputs:** Setup validation report, pass/fail status  
**Can run independently:** ✅ Yes (requires source.001, source.002, source.003)

**What it should validate:**
- ✅ Notebook artifact exists and synced to Git
- ✅ Notebook wired to pipeline (activity configured)
- ✅ Pipeline parameters defined (`init_mode`, `bootstrap`, `preview`, etc.)
- ✅ Variable library bound (credentials configured)
- ✅ Endpoints module exists (if bootstrap configured)
- ✅ Lakehouse dependency configured
- ✅ All IDs correct (notebookId, workspaceId, lakehouseId)

**Purpose:** **Pipeline construction validation** - ensures pipeline is ready to run

**Status:** Referenced in `source.003` but not created

---

## Revised Playbook Structure

### **Pipeline Construction (Setup):**
- `source.001` - Create source notebook ✅
- `source.002` - Add notebook to pipeline ✅
- `source.003` - Configure endpoints bootstrap ✅
- `source.004` - Validate source stage setup ❌ **NEW** (referenced but missing)

---

## What's NOT a Playbook (Runtime Operations)

These are handled by the **notebook itself** with **parameters**:

### **Runtime Operations (Not Playbooks):**
- ❌ Create runtime metadata tables → Handled by notebook with `bootstrap=True` parameter
- ❌ Validate authentication → Handled by notebook (always runs)
- ❌ Validate hierarchical access → Handled by notebook (always runs)
- ❌ Comprehensive endpoint health check → Handled by notebook (always runs)
- ❌ Extract preview samples → Handled by notebook with `preview=True` parameter
- ❌ Create quality gate report → Handled by notebook (always runs)

**These are execution-time operations, not setup operations.**

---

## Execution Flow

### **Pipeline Construction (Playbooks):**
```
1. source.001 - Create notebook ✅
2. source.002 - Add to pipeline ✅
3. source.003 - Configure bootstrap ✅
4. source.004 - Validate setup ✅ (NEW)
```

### **Pipeline Execution (Notebook with Parameters):**
```
# Normal run
bootstrap: bool = False
preview: bool = False

# Bootstrap run
bootstrap: bool = True
preview: bool = False

# Full run
bootstrap: bool = True
preview: bool = True
```

**The notebook handles all runtime operations based on parameters.**

---

## Perfect Atomicity (Revised)

### **✅ Good Atomicity (Pipeline Construction):**
- `source.001` - Create notebook (infrastructure setup)
- `source.002` - Wire to pipeline (infrastructure setup)
- `source.003` - Configure bootstrap (metadata setup)
- `source.004` - Validate setup (quality gates)

### **❌ NOT Playbooks (Runtime Execution):**
- Create runtime tables (notebook execution)
- Validate auth (notebook execution)
- Validate hierarchical (notebook execution)
- Health check (notebook execution)
- Extract samples (notebook execution with parameter)
- Quality report (notebook execution)

---

## Summary

### **Current Status:**
- ✅ 3 playbooks exist (001, 002, 003)
- ❌ 1 playbook missing (004 - validate setup)

### **Missing Playbook:**
- `source.004` - Validate source stage setup (referenced but not created)

### **What Playbooks Are For:**
- ✅ **Pipeline construction** - Setting up the pipeline infrastructure
- ✅ **Configuration** - Configuring pipeline parameters and dependencies
- ✅ **Validation** - Ensuring setup is complete and correct

### **What Playbooks Are NOT For:**
- ❌ **Runtime execution** - These are handled by notebook with parameters
- ❌ **Data operations** - These happen during pipeline execution
- ❌ **Validation during execution** - These are notebook operations

---

## Key Principle

**Playbooks = Pipeline Construction**  
**Notebook = Pipeline Execution (with parameters)**

**Separation of Concerns:**
- **Playbooks:** Build the pipeline
- **Notebook:** Run the pipeline (with parameters like `bootstrap`, `preview`, `init_mode`)

---

## Version History

- **v1.0** (2025-12-11): Initial analysis (incorrectly included runtime operations)
- **v2.0** (2025-12-11): Revised - playbooks are for pipeline construction only

---

## References

- **Source Tables Lifecycle:** `docs/source/SOURCE-TABLES-LIFECYCLE.md`
- **Source Complete Flow:** `docs/source-notebook-complete-flow.md`
- **Source Notebook:** `sourceZephyr.Notebook/notebook_content.py`
- **Current Playbooks:** `Core/operations/playbooks/fabric/1-source/`
- **Automated Orchestration:** `docs/prepare/AUTOMATED-PIPELINE-ORCHESTRATION.md`




