# Source Notebook Production-isation Plan

**Date:** 2025-12-06  
**Objective:** Tidy and productionise `sourceZephyr.Notebook` to SPECTRA-grade quality

---

## 🎯 Goals

1. **Minimal Notebook Code** - Only what's needed to run
2. **SDK-Driven** - Move all logic to SDK helpers
3. **Single Code Block** - All code (except `%run`) in one block
4. **SPECTRA-Grade Header** - Perfect branded markdown header
5. **Clean Structure** - Remove empty cells, comments, bloat

---

## 📋 Action List

### 1. **Move Portfolio Display to SDK** ✅
   - **Current:** Verbose portfolio display logic in notebook (lines 282-350)
   - **Action:** Create `SourceStageHelpers.display_portfolio_summary()` SDK helper
   - **Result:** Notebook just calls helper, SDK handles formatting

### 2. **Create Source Stage Executor in SDK** ✅
   - **Current:** Notebook orchestrates all operations manually
   - **Action:** Create `SourceStageHelpers.execute_source_stage()` that orchestrates:
     - Configuration tables creation
     - Authentication validation
     - Endpoints bootstrap
     - Portfolio table creation
     - Preview sample extraction
     - Portfolio display
   - **Result:** Notebook just calls one function

### 3. **Consolidate Notebook Code** ✅
   - **Current:** Multiple code blocks separated by metadata
   - **Action:** 
     - Keep `%run spectraSDK` in its own cell (magic command requirement)
     - Consolidate all other code into single code block with 7 stages
   - **Result:** Clean, minimal notebook structure

### 4. **Create SPECTRA-Branded Header** ✅
   - **Current:** Basic header with bullet points
   - **Action:** Create perfect SPECTRA-branded header that:
     - Clearly describes source stage purpose
     - No bloat, just essential info
     - SPECTRA branding/identity
   - **Result:** Professional, clear, branded header

### 5. **Remove Empty Cells & Comments** ✅
   - **Current:** Empty cells, placeholder comments, unnecessary metadata
   - **Action:** Remove all empty cells, clean up metadata, remove comments
   - **Result:** Clean, production-ready notebook

---

## 🏗️ Implementation Steps

### Step 1: Add SDK Helpers

**File:** `spectraSDK.Notebook/notebook_content.py`

1. Add `display_portfolio_summary()` to `SourceStageHelpers`
2. Add `execute_source_stage()` to `SourceStageHelpers`

### Step 2: Refactor Notebook

**File:** `sourceZephyr.Notebook/notebook_content.py`

1. Update markdown header (SPECTRA-branded)
2. Keep `%run spectraSDK` in own cell
3. Consolidate all code into single block:
   - Parameters
   - Session creation & context loading
   - Initialize
   - Execute (call SDK executor)
   - Validate
   - Record
   - Complete
4. Remove all empty cells and comments

---

## 📊 Expected Structure

```python
# MARKDOWN: SPECTRA-branded header

%run spectraSDK

# SINGLE CODE BLOCK:
# 1. Parameters
# 2. Context
# 3. Initialize
# 4. Execute (SDK orchestrator)
# 5. Validate
# 6. Record
# 7. Finalise
```

---

## ✅ Success Criteria

- ✅ Notebook code < 50 lines
- ✅ All logic in SDK
- ✅ Single code block (except `%run`)
- ✅ SPECTRA-branded header
- ✅ No empty cells or bloat
- ✅ Still works exactly the same

---

**Version:** 1.0.0  
**Date:** 2025-12-06

