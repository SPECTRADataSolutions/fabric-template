# Preview Samples - Purpose & Design Decision

**Date:** 2025-12-08  
**Question:** Should source stage always create preview samples, or only when `preview=True`?

---

## 🔍 Current Situation

### Contract Says:
- ✅ Lists preview samples in `data_outputs` (lines 42-46)
- ✅ Obligation: "Visibility demonstrated across all hierarchy levels with preview samples"
- ✅ Purpose: "Preview samples for Prepare stage schema design" (line 88)

### Implementation Says:
- ⚠️ Only creates samples when `preview=True` parameter is set
- ⚠️ Notebook ran with `preview=False` → no samples created
- ⚠️ User checking lakehouse → no sample tables found

### The Question:
**Should preview samples:**
1. **Always exist** (required output of source stage)?
2. **Only exist when requested** (optional via `preview=True` parameter)?

---

## 🤔 Analysis

### Option A: Preview Samples Always Required

**Rationale:**
- Prepare stage needs schema samples to design the pipeline
- Contract lists them in `data_outputs` (implies they should exist)
- "Visibility demonstrated" suggests they should always be present
- Helps with debugging and understanding data structure

**Implementation:**
- Remove `if session.params["preview"]:` condition
- Always extract preview samples during source stage execution
- All 5 hierarchy levels always available

**Pros:**
- ✅ Always available for Prepare stage
- ✅ Contract alignment (data_outputs listed)
- ✅ Better observability

**Cons:**
- ❌ Extra API calls on every run (even when not needed)
- ❌ Slower source stage execution
- ❌ Data that might not be used

---

### Option B: Preview Samples Optional (Current)

**Rationale:**
- Prepare stage only needs samples during initial design
- Once schema is defined, samples aren't needed
- `preview=True` parameter makes intent explicit
- Faster normal runs (no unnecessary API calls)

**Implementation:**
- Keep `if session.params["preview"]:` condition
- Only extract when explicitly requested
- Update contract to mark samples as "optional/conditional"

**Pros:**
- ✅ Faster normal execution
- ✅ Explicit intent (preview vs production)
- ✅ No unnecessary API calls

**Cons:**
- ⚠️ Contract mismatch (listed in data_outputs but conditional)
- ⚠️ Prepare stage might need samples on first run
- ⚠️ Less observability by default

---

## 🎯 Recommendation

**Option C: Hybrid Approach** (Best of Both Worlds)

**Rationale:**
- Source stage should **always** create preview samples on **first run** (bootstrap)
- After that, samples are optional unless `preview=True`
- Prepare stage can use existing samples or request new ones

**Implementation:**
```python
# Always create samples if they don't exist (first run)
# OR if preview=True parameter is set
should_extract_preview = (
    session.params["bootstrap"] or  # First run
    session.params["preview"] or     # Explicit request
    not _samples_exist(spark)        # Missing samples
)

if should_extract_preview:
    # Extract all 5 preview samples
```

**Pros:**
- ✅ Samples always available after first run
- ✅ Fast subsequent runs (skip if samples exist)
- ✅ Contract alignment (samples available when needed)
- ✅ Explicit refresh via `preview=True`

**Cons:**
- ⚠️ Slightly more complex logic
- ⚠️ Need to check if samples exist first

---

## 📋 What Do Other Stages Need?

### Prepare Stage Requirements:

**For schema design:**
- Needs sample data to understand structure
- Needs to infer data types (scalar, record, array)
- Needs to see nullable vs mandatory fields

**Question:** Does Prepare stage:
1. **Require** samples to run? → Samples should always exist
2. **Use** samples if available? → Samples optional
3. **Fetch** its own samples? → Source doesn't need to provide

---

## 🎯 Decision Needed

**Please clarify:**

1. **Are preview samples required for Prepare stage to run?**
   - If YES → Always create them
   - If NO → Keep them optional

2. **What's the primary purpose of preview samples?**
   - Schema discovery? → Optional is fine
   - Always available for reference? → Always create
   - Debugging/observability? → Always create

3. **Should contract be updated?**
   - Mark samples as "conditional" in data_outputs?
   - Or make samples always required?

---

## 💡 My Recommendation

**Option C: Hybrid Approach**

1. **First run (`bootstrap=True`):** Always create samples
2. **Subsequent runs:** Only create if `preview=True` OR samples are missing
3. **Update contract:** Clarify that samples are "created on bootstrap or when preview=True"

This way:
- ✅ Samples available when Prepare stage needs them (after first run)
- ✅ Fast normal runs (don't recreate samples)
- ✅ Can refresh samples explicitly (`preview=True`)
- ✅ Contract aligns with implementation

---

**What do you think? Should preview samples:**
- A) Always be created (remove preview parameter check)
- B) Stay optional (keep current implementation, update contract)
- C) Hybrid (create on bootstrap/first run, then optional)

