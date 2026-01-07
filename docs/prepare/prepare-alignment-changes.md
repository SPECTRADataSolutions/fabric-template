# Prepare Stage Alignment Changes

**Date:** 2025-12-11  
**Purpose:** Document all changes made to align `prepareZephyr` with `sourceZephyr` best practices and SPECTRA-grade standards

---

## Summary

This document captures all changes made to align `prepareZephyr.Notebook` with the canonical `sourceZephyr.Notebook` pattern and SPECTRA-grade standards.

---

## 1. Table Naming Convention (Legacy Cleanup)

### **Change:** Remove underscore prefixes from table names

**Before (Legacy):**
- `prepare._schema`
- `prepare._dependencies`
- `prepare._constraints`
- Paths: `Tables/prepare/_schema`, `Tables/prepare/_dependencies`, `Tables/prepare/_constraints`

**After (SPECTRA-grade):**
- `prepare.schema`
- `prepare.dependencies`
- `prepare.constraints`
- Paths: `Tables/prepare/schema`, `Tables/prepare/dependencies`, `Tables/prepare/constraints`

**Rationale:** Underscore prefixes were legacy from before we used schemas. Now we use schema prefixes (`prepare.`, `source.`) so underscores are redundant.

**Matches:** `sourceZephyr` uses `source.portfolio`, `source.config`, `source.credentials`, `source.endpoints` (no underscores)

**Commit:** `a0d982f` - "Remove: Underscore prefixes from prepare table names (prepare._schema → prepare.schema, legacy cleanup)"

---

## 2. Log Schema Standardisation

### **Change:** Central log schema (`Tables/log/{stage}log`)

**Before:**
- Logs scattered across stage schemas
- `Tables/source/sourcelog`
- `Tables/prepare/preparelog`

**After:**
- All logs in central `log` schema
- `Tables/log/sourcelog`
- `Tables/log/preparelog`
- `Tables/log/extractlog` (future)
- `Tables/log/cleanlog` (future)

**Implementation:**
- **Location:** `Data/fabric-sdk/src/spectra_fabric_sdk/session.py` (line 447)
- **Code:**
  ```python
  # Write to log table (SPECTRA-grade: all logs in central log schema)
  # Format: Tables/log/{stage}log (e.g., Tables/log/sourcelog, Tables/log/preparelog)
  log_table_path = f"Tables/log/{self.ctx['stage']}log"
  ```

**Rationale:** Centralised logging schema improves organisation and makes log discovery easier.

**Documentation:** `docs/standards/NOTEBOOK-FORMATTING-STANDARD.md` (lines 258, 368-374)

---

## 3. Variable Access Pattern (SPECTRA-grade)

### **Change:** Use correct SDK methods for variable access

**Before (Incorrect):**
```python
base_url = session.vars.get("base_url", "")
api_token = session.vars.get("api_token", "")
base_path = session.vars.get("base_path", "/rest/atm/1.0")
```

**After (SPECTRA-grade):**
```python
# Get API credentials (SPECTRA-grade: use session.variables.get_secret() for secrets, ctx for URLs)
base_url = session.ctx.get("base_url", "")
api_token = session.variables.get_secret("API_TOKEN", "")
base_path = session.ctx.get("base_path", "/rest/atm/1.0")
```

**Rationale:**
- `session.vars` doesn't exist - use `session.variables` or `session.ctx`
- Secrets should use `session.variables.get_secret()` (handles encryption)
- Context values (already loaded) should use `session.ctx.get()`

**Matches:** `sourceZephyr` uses:
- `session.variables.get_secret("API_TOKEN")` for secrets
- `session.ctx["full_url"]` for URLs

**Commits:**
- `8ef9599` - "Fix: Use session.variables.get() instead of session.vars (SPECTRA-grade variable access)"
- `cf7ade9` - "Fix: Use session.variables.get_secret() for API_TOKEN and session.ctx for base_url/base_path"

---

## 4. Logging Standards Alignment

### **Change:** Match `sourceZephyr` logging pattern

**Pattern (SPECTRA-grade):**
- Section headers: `log.info("=" * 80)` and `log.info("SECTION NAME")`
- Subsection headers: `log.info("== Subsection name...")`
- Actions: `log.info("  >> Action description...")`
- Success: `log.info("  OK Success message")`
- Warnings: `log.warning("  !! WARNING: Message")`
- Errors: `log.error("  !! ERROR: Message")`
- Info: `log.info("  == Info message")`

**No Unicode/emoji characters** - Use ASCII equivalents:
- ✅ `==` (not `ƒôè`)
- ✅ `>>` (not `ƒÆ¥`)
- ✅ `OK` (not `Ô£à`)
- ✅ `!!` (not `ÔØî`)

**Rationale:** Consistent logging format improves readability and matches canonical `sourceZephyr` pattern.

**Documentation:** `docs/standards/NOTEBOOK-FORMATTING-STANDARD.md`

---

## 5. Notebook Standards Application

### **Created:** Notebook Standards Application Guide

**Location:** `docs/standards/NOTEBOOK-STANDARDS-APPLICATION.md`

**Purpose:** Define what "apply notebook standards" means and how to do it

**Content:**
- Structure compliance checklist
- Code extraction to SDK process
- Logging standards alignment
- Code quality requirements (docstrings, type hints)
- Module organisation patterns

**Commit:** `f8779ac` - "Add: Notebook Standards Application Guide (what 'apply notebook standards' does)"

---

## 6. British English Enforcement

### **Change:** Added British English section to `.cursorrules`

**Location:** `.cursorrules` (workspace root)

**Content:**
- Added to Core Principles (line 685)
- Dedicated section "British English (CRITICAL - ENFORCED)" (line 689)
- Fixed all American spellings throughout file:
  - "organized" → "organised"
  - "organization" → "organisation"
  - "center" → "centre"
  - etc.

**Rationale:** Mark uses British English - all documentation, code comments, and responses must use British English.

**Commit:** `7de8ebe` - "Add: British English section to cursorrules and fix all American spellings"

---

## Files Changed

1. **`prepareZephyr.Notebook/notebook_content.py`**
   - Removed underscore prefixes from table names
   - Fixed variable access pattern
   - Aligned logging format

2. **`Data/fabric-sdk/src/spectra_fabric_sdk/session.py`**
   - Central log schema implementation (`Tables/log/{stage}log`)

3. **`docs/standards/NOTEBOOK-STANDARDS-APPLICATION.md`**
   - New document defining notebook standards application process

4. **`.cursorrules`** (workspace root)
   - Added British English section
   - Fixed American spellings

5. **`docs/standards/NOTEBOOK-FORMATTING-STANDARD.md`**
   - Documented log schema standard

---

## Commits Summary

1. `a0d982f` - Remove underscore prefixes from prepare table names
2. `35044d5` - Add comment explaining base_url/base_path separation
3. `cf7ade9` - Fix: Use session.variables.get_secret() for API_TOKEN
4. `8ef9599` - Fix: Use session.variables.get() instead of session.vars
5. `d502dea` - Test: Update prepareZephyr timestamp (Fabric sync test)
6. `f8779ac` - Add: Notebook Standards Application Guide
7. `7de8ebe` - Add: British English section to cursorrules

---

## Next Steps

**Pending (from user request):**
- Extract all modules to SDK (`PrepareStageHelpers` class)
- Simplify notebook to match `sourceZephyr` (just calls SDK helper)
- Add SPECTRA-grade docstrings to all functions
- Add complete type hints to all functions

**See:** `docs/standards/NOTEBOOK-STANDARDS-APPLICATION.md` for full application process

---

## Version History

- **v1.0** (2025-12-11): Initial documentation of alignment changes

---

## References

- **Canonical Example:** `sourceZephyr.Notebook/notebook_content.py`
- **Notebook Formatting Standard:** `docs/standards/NOTEBOOK-FORMATTING-STANDARD.md`
- **Notebook Standards Application:** `docs/standards/NOTEBOOK-STANDARDS-APPLICATION.md`
- **SDK Location:** `Data/fabric-sdk/src/spectra_fabric_sdk/`




