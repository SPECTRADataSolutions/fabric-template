# Tomorrow: Fine-Tooth Comb - Perfect Canonical Order Discovery

> **Status:** 🔵 Ready for Tomorrow  
> **Date:** 2025-12-09  
> **Goal:** Discover the PERFECT order for loading all test data with ZERO dependency complaints  
> **Approach:** Systematic, one endpoint at a time, validate each step

---

## 🎯 Objective

**Find the PERFECT list of how to populate Zephyr with everything first time.**

No brute force. No guessing. No errors.

**Method:** Fine-tooth comb through each endpoint until we find a pattern where ALL test data loads cleanly.

---

## 📋 What We Know So Far (From Today's Discovery)

### ✅ **Working Endpoints (Confirmed)**
1. **Release:** `POST /release` - Works, but locks for >60s
2. **Requirement Folder:** `POST /requirementtree/add` - Works perfectly
3. **Requirement (workaround):** `POST /requirementtree/add` + `parentId` - Creates tree node
4. **Cycle:** `POST /cycle` - Works with existing/unlocked release

### ❌ **Broken Endpoints (Confirmed)**
1. **Testcase Folder:** `POST /testcasetree` - HTTP 400 "For input string: null"
2. **Requirement (direct):** `POST /requirement` - HTTP 500 "id is null"

### ⚠️ **Blockers**
1. Release locks for >60 seconds after creation
2. Folder creation API is broken
3. Cannot create testcases without folders

---

## 🔬 Tomorrow's Systematic Approach

### **Phase 1: Single Entity Tests (1 hour)**

**Goal:** Test EACH entity type individually with ONE minimal entity

**Entities to test:**
1. Release
2. Cycle
3. Requirement Folder
4. Requirement (tree node)
5. Requirement (actual - try all documented endpoints)
6. Testcase Folder (try ALL variations)
7. Testcase
8. Execution
9. Allocation
10. Phase (cycle phase)
11. Step (testcase step)
12. Attachment
13. Defect

**For each entity:**
```python
# 1. Create ONE entity with MINIMAL payload
# 2. Verify it exists (GET by ID)
# 3. Capture FULL response schema
# 4. Document what fields are REQUIRED vs OPTIONAL
# 5. Note any errors/warnings
# 6. Delete entity
# 7. Move to next
```

**Output:** `entity-test-matrix.md` - Complete list of what works/fails

---

### **Phase 2: Dependency Chain Discovery (2 hours)**

**Goal:** Build the EXACT dependency chain by testing combinations

**Method:**
```python
# For each working entity:
# 1. Can it be created alone? (no dependencies)
# 2. Does it reference other entities? (has dependencies)
# 3. What are the MINIMUM dependencies?
# 4. What are OPTIONAL dependencies?
```

**Test Matrix:**
| Entity | Depends On | Optional Deps | Can Create Alone? |
|--------|------------|---------------|-------------------|
| Release | ? | ? | ? |
| Cycle | Release? | Phases? | ? |
| Requirement | Folder? | Testcase? | ? |
| Testcase | Folder? | Steps? | ? |
| Execution | Cycle? Testcase? | Defects? | ? |
| Allocation | Requirement? Testcase? | - | ? |

**Output:** `dependency-chain-complete.md` - Full dependency graph

---

### **Phase 3: Ordering Experiments (1 hour)**

**Goal:** Test different creation orders to find the ONE that works perfectly

**Experiments:**
```
Experiment 1: Release → Cycle → Folder → Testcase → Execution
Experiment 2: Folder → Testcase → Release → Cycle → Execution
Experiment 3: Release + Folder (parallel) → Cycle + Testcase (parallel) → Execution
... etc
```

**For each experiment:**
1. Start with clean project
2. Create entities in specified order
3. Record any errors
4. Record success/fail
5. Note any "locked" or "not found" errors

**Output:** `creation-order-experiments.md` - Test results

---

### **Phase 4: Perfect Order Discovery (1 hour)**

**Goal:** Determine the ONE perfect order that works every time

**Criteria for "perfect":**
- ✅ No dependency errors
- ✅ No "locked" errors
- ✅ No "not found" errors
- ✅ Can create everything in one pass
- ✅ No manual UI steps required (or documented if unavoidable)
- ✅ Repeatable (works every time)

**Output:** `canonical-order-final.md` - THE definitive list

---

### **Phase 5: Validation (30 min)**

**Goal:** Run the perfect order 3 times to confirm it works

**Steps:**
1. Clean project
2. Run perfect order script
3. Verify ALL entities created
4. Clean project
5. Repeat 2 more times

**Success Criteria:**
- 3/3 runs succeed
- Zero errors
- All entities present

**Output:** `validation-results.md` - Proof it works

---

## 🛠️ Tools to Build Tomorrow

### **1. Single Entity Tester**
```python
# test_single_entity.py
# Tests ONE entity type with minimal payload
# Captures full response, documents requirements
```

### **2. Dependency Chain Builder**
```python
# build_dependency_chain.py
# Tests all entity combinations
# Builds complete dependency graph
```

### **3. Order Experiment Runner**
```python
# run_order_experiment.py
# Tests specified creation order
# Records success/fail with details
```

### **4. Perfect Order Script**
```python
# create_perfect_test_data.py
# Uses discovered perfect order
# Creates complete test dataset
```

### **5. Validation Runner**
```python
# validate_perfect_order.py
# Runs perfect order 3 times
# Confirms repeatability
```

---

## 📊 Expected Outputs

### **Documents:**
1. `entity-test-matrix.md` - What works/fails for each entity
2. `dependency-chain-complete.md` - Full dependency graph
3. `creation-order-experiments.md` - All experiments + results
4. `canonical-order-final.md` - THE definitive perfect order
5. `validation-results.md` - 3-run validation proof

### **Scripts:**
1. `test_single_entity.py` - Entity tester
2. `build_dependency_chain.py` - Dependency discovery
3. `run_order_experiment.py` - Order tester
4. `create_perfect_test_data.py` - Production script
5. `validate_perfect_order.py` - Validator

---

## 🎯 Success Criteria

**We have succeeded when:**

1. ✅ We can list EVERY entity in Zephyr
2. ✅ We know EXACTLY what dependencies each has
3. ✅ We have a SINGLE canonical order that works 100% of the time
4. ✅ We can create a COMPLETE test dataset in one pass
5. ✅ We have documented ALL workarounds (if any)
6. ✅ We have validation proof (3/3 runs succeed)

---

## 🚫 What We'll Avoid Tomorrow

- ❌ Guessing at payloads
- ❌ Brute force attempts
- ❌ Skipping validation
- ❌ Assuming anything works without testing
- ❌ Moving forward with errors

---

## 📝 Current State (End of Today)

**Project Status:**
- ✅ Project is CLEAN (1 release remains - Zephyr requirement)
- ✅ No cycles, testcases, executions, requirements, folders
- ✅ Ready for fresh start

**Knowledge Gained:**
- ✅ Release locks for >60s after creation
- ✅ Folder creation API is broken
- ✅ Some entities work, some don't
- ✅ Dependencies exist but not fully mapped

**What We Need:**
- 🔵 Complete dependency graph
- 🔵 Perfect canonical order
- 🔵 Repeatable test data script
- 🔵 Validation proof

---

## ⏰ Tomorrow's Schedule (Estimated)

**Total Time:** ~5.5 hours

- Phase 1: Single Entity Tests - 1 hour
- Phase 2: Dependency Chain - 2 hours
- Phase 3: Ordering Experiments - 1 hour
- Phase 4: Perfect Order - 1 hour
- Phase 5: Validation - 30 min

**Start:** Fresh in the morning  
**End:** Complete perfect order discovered and validated

---

## 🎯 Tomorrow's Mantra

**"One endpoint at a time. Test everything. Document everything. Find the pattern."**

No brute force. No guessing. Fine-tooth comb.

---

**Status:** 🔵 Ready  
**Next Action:** Start Phase 1 tomorrow morning

