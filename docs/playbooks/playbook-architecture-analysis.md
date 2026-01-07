# Playbook Architecture Analysis

> **Question:** Is generic Fabric playbooks the best approach for SPECTRA?

**Date:** 2025-12-05  
**Status:** Analysis

---

## Current Approach: Generic Fabric Playbooks

**Location:** `Core/operations/playbooks/fabric/`

**Structure:**
- Generic playbooks with placeholders (`{sourceKey}`, `<SourceKey>`)
- Zephyr-specific examples hardcoded in places (`zephyrBaseUrl`, `DXC_ZEPHYR_API_TOKEN`)
- Mix of generic structure and source-specific details

**Example from `source.002`:**
```markdown
- Ensure parameters map to pipeline parameters: `projectKey`, `zephyrBaseUrl`, `zephyrBasePath`, `zephyrApiToken`.
- Bind `zephyrBaseUrl` → `DXC_ZEPHYR_BASE_URL`, `zephyrBasePath` → `DXC_ZEPHYR_BASE_PATH`, `zephyrApiToken` → `DXC_ZEPHYR_API_TOKEN`.
```

**Problem:** Hardcoded Zephyr variable names in supposedly generic playbook.

---

## Alternative Approaches

### Option 1: Pure Generic Templates (Current)

**Pros:**
- ✅ Single source of truth
- ✅ DRY principle
- ✅ Easy to maintain common procedures
- ✅ Consistent structure

**Cons:**
- ❌ Hard to see source-specific flow
- ❌ Mixing generic and source-specific knowledge
- ❌ Hardcoded examples (Zephyr) leak into generic playbooks
- ❌ Can't easily customize per source
- ❌ Not clear which parts are source-specific

**Verdict:** ❌ **Not ideal** - too much mixing, hard to maintain source-specific variants.

---

### Option 2: Source-Specific Playbooks Only

**Structure:**
```
Core/operations/playbooks/fabric/
├── zephyr/
│   ├── 0-setup/
│   └── 1-source/
├── jira/
│   ├── 0-setup/
│   └── 1-source/
└── xero/
    ├── 0-setup/
    └── 1-source/
```

**Pros:**
- ✅ Clear source-specific documentation
- ✅ Easy to see what applies to which source
- ✅ Can customize per source without affecting others
- ✅ Source-specific playbook flow visible

**Cons:**
- ❌ Lots of duplication
- ❌ Hard to maintain consistency
- ❌ Updates to common procedures require updating all sources
- ❌ Doesn't scale well (50 sources = 50 copies)

**Verdict:** ❌ **Not ideal** - too much duplication, maintenance nightmare.

---

### Option 3: Template + Source-Specific Instantiation (RECOMMENDED)

**Structure:**
```
Core/operations/playbooks/fabric/
├── templates/                    # Generic templates
│   ├── 0-setup/
│   │   └── setup.001-createSourceNotebook.md.template
│   └── 1-source/
│       └── source.001-createSourceNotebook.md.template
└── README.md                     # Template usage guide

Data/{source}/docs/playbooks/     # Source-specific instantiated playbooks
├── 0-setup/
│   ├── setup.001-createSourceNotebook.md  # Generated from template
│   └── setup.001-source-specific.md       # Source-specific overrides
└── 1-source/
    ├── source.001-createSourceNotebook.md
    └── source.001-source-specific.md
```

**Template Example:**
```markdown
# source.001 - createSourceNotebook

## purpose
Create the Source stage Fabric notebook for the pipeline (e.g., `source{{sourceKey}}`) with real IDs so the pipeline can reference it without dependency errors.

## procedure

1) Create the notebook artifact
```
$workspace = "{{sourceKey}}.Workspace"
$notebookName = "source{{sourceKeyCapitalized}}"
fab mkdir "$workspace/$notebookName.Notebook"
```

2) Update pipeline activity
- Update `{{sourceKey}}Pipeline.DataPipeline/pipeline-content.json`
```

**Instantiated Example (Zephyr):**
```markdown
# source.001 - createSourceNotebook

## purpose
Create the Source stage Fabric notebook for the pipeline (e.g., `sourceZephyr`) with real IDs so the pipeline can reference it without dependency errors.

## procedure

1) Create the notebook artifact
```
$workspace = "zephyr.Workspace"
$notebookName = "sourceZephyr"
fab mkdir "$workspace/$notebookName.Notebook"
```

2) Update pipeline activity
- Update `zephyrPipeline.DataPipeline/pipeline-content.json`
```

**Pros:**
- ✅ Best of both worlds: templates + source-specific
- ✅ Clear separation: template vs instantiated
- ✅ Source-specific playbooks visible in each repo
- ✅ Can override/extend per source
- ✅ Template updates propagate via regeneration
- ✅ Source-specific customizations preserved
- ✅ Aligns with parameterised template approach
- ✅ Supports GitHub Project v2 generation (source-specific playbooks)

**Cons:**
- ⚠️ Requires template instantiation tool
- ⚠️ Need to regenerate when templates change (automated via CI/CD)
- ⚠️ More complex initial setup

**Verdict:** ✅ **BEST APPROACH** - balances reusability with source-specific needs.

---

### Option 4: Hybrid (Template Base + Source Extensions)

**Structure:**
```
Core/operations/playbooks/fabric/
├── 0-setup/
│   └── setup.001-base.md                    # Generic base
└── 1-source/
    └── source.001-base.md                   # Generic base

Data/{source}/docs/playbooks/
├── 0-setup/
│   └── setup.001-extensions.md              # Source-specific extensions
└── 1-source/
    └── source.001-extensions.md             # Source-specific extensions
```

**Pros:**
- ✅ Template stays generic
- ✅ Source-specific extensions separate
- ✅ Clear what's generic vs source-specific

**Cons:**
- ❌ Hard to see complete playbook flow (base + extensions)
- ❌ Have to read two files
- ❌ More cognitive load

**Verdict:** ⚠️ **Acceptable but not ideal** - two files per playbook is awkward.

---

## Comparison with Other SPECTRA Domains

### Railway Playbooks
**Pattern:** Domain-specific (`railway/railway.001-*.md`)
- ✅ All Railway playbooks in one place
- ✅ Clear Railway-specific procedures
- ❌ But Railway is a single service (not template-driven)

### GitHub Playbooks
**Pattern:** Domain-specific (`github/github.001-*.md`)
- ✅ All GitHub playbooks in one place
- ✅ Clear GitHub-specific procedures
- ❌ But GitHub is a single service (not template-driven)

### Fabric Playbooks
**Pattern:** Should be template-driven (multiple sources)
- ✅ Need templates for reuse
- ✅ But also need source-specific instantiation
- ✅ Current approach mixes both (problem)

---

## Recommendation: Option 3 (Template + Instantiation)

**Why this is best for SPECTRA:**

1. **Aligns with template plan** - We're already planning parameterised templates
2. **Supports GitHub Project v2** - Source-specific playbooks generate source-specific issues
3. **Scalable** - 50 sources = 50 instantiations, not 50 manual copies
4. **Maintainable** - Template updates propagate, source-specific customizations preserved
5. **Clear visibility** - Source-specific playbooks visible in each repo
6. **Contract-driven** - Templates read from `contract.yaml`, instantiated playbooks use actual values

**Implementation:**

1. **Templates** in `Core/operations/playbooks/fabric/templates/`
   - Generic structure with placeholders
   - No hardcoded source names
   - Contract-driven variable references

2. **Instantiation Tool**
   ```python
   # Core/operations/scripts/instantiate_playbooks.py
   instantiate_playbooks(
       source_key="zephyr",
       contract_path="Data/zephyr/contract.yaml",
       output_dir="Data/zephyr/docs/playbooks/"
   )
   ```

3. **Source-Specific Playbooks** in `Data/{source}/docs/playbooks/`
   - Generated from templates
   - Can be manually extended if needed
   - Source-specific details visible

4. **CI/CD Integration**
   - Template changes trigger regeneration for all sources
   - Or: Manual regeneration when needed
   - Or: On-demand generation during project setup

---

## Migration Path

### Phase 1: Extract Templates
1. Move generic playbooks to `Core/operations/playbooks/fabric/templates/`
2. Replace all hardcoded Zephyr references with `{{placeholders}}`
3. Make templates contract-driven

### Phase 2: Build Instantiation Tool
1. Create `instantiate_playbooks.py`
2. Support `contract.yaml` as input
3. Generate source-specific playbooks

### Phase 3: Instantiate for Zephyr
1. Run instantiation tool for Zephyr
2. Verify generated playbooks are correct
3. Update Zephyr docs to reference source-specific playbooks

### Phase 4: Template Documentation
1. Document template format
2. Document instantiation process
3. Create template usage guide

---

## Conclusion

**Current approach (pure generic):** ❌ **Not ideal**
- Too much mixing of generic and source-specific
- Hardcoded examples leak through
- Hard to maintain source-specific variants

**Recommended approach (template + instantiation):** ✅ **BEST**
- Clean separation: templates vs instantiated
- Source-specific playbooks visible in each repo
- Supports GitHub Project v2 generation
- Aligns with parameterised template plan
- Scalable and maintainable

**Next Steps:**
1. Extract templates from current generic playbooks
2. Build instantiation tool
3. Instantiate for Zephyr as proof of concept
4. Document template system

---

**Status:** Ready for decision  
**Recommendation:** Proceed with Option 3 (Template + Instantiation)




