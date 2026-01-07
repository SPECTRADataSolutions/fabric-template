# Template Creation Plan

## Status: In Progress

This document tracks the creation of the SPECTRA Fabric Workspace Template from the zephyr implementation.

## Phase 1: Copy & Test ✅

- [x] Copy zephyr structure to template
- [x] Initialize git repository
- [x] Create template documentation
- [ ] Test template in new workspace (verify it works)

## Phase 2: Strip Zephyr-Specific Code

### 2.1 Remove ZephyrIntelligence from SDK
- [ ] Extract `ZephyrIntelligence` class from `spectraSDK.Notebook`
- [ ] Create `{PROJECT}Intelligence.Notebook` template
- [ ] Update SDK to be generic (no source-specific code)

### 2.2 Replace Hardcoded Values
- [ ] Replace `"zephyr"` → `"{PROJECT}"` in all files
- [ ] Replace `"zephyrVariables"` → `"{PROJECT}Variables"`
- [ ] Replace `"zephyrLakehouse"` → `"{PROJECT}Lakehouse"`
- [ ] Replace `"zephyrPipeline"` → `"{PROJECT}Pipeline"`
- [ ] Replace `"zephyrEnvironment"` → `"{PROJECT}Environment"`

### 2.3 Remove Zephyr-Specific Logic
- [ ] Remove hardcoded endpoints (`/project/details`, `/release`)
- [ ] Make API calls metadata-driven
- [ ] Remove zephyr-specific functions (`call_zephyr_api`)
- [ ] Update Prepare/Extract to read from Source stage outputs

### 2.4 Rename Files/Directories
- [ ] Rename `sourceZephyr.Notebook` → `source{PROJECT}.Notebook`
- [ ] Rename `prepareZephyr.Notebook` → `prepare{PROJECT}Config.Notebook`
- [ ] Rename `extractZephyrSample.Notebook` → `extract{PROJECT}Sample.Notebook`
- [ ] Rename all `zephyr*` files to `{PROJECT}*`

## Phase 3: Create Template Files

### 3.1 Intelligence Template
- [ ] Create `{PROJECT}Intelligence.Notebook/notebook_content.py` template
- [ ] Include example structure with placeholders
- [ ] Document how to populate intelligence

### 3.2 Contract Template
- [ ] Update `config/contracts/source.contract.yaml` with placeholders
- [ ] Create example contract structure
- [ ] Document required fields

### 3.3 Variable Library Template
- [ ] Update `{PROJECT}Variables.VariableLibrary/variables.json` with placeholders
- [ ] Document required variables
- [ ] Create `.env.example`

## Phase 4: SPECTRA-Grade Compliance

### 4.1 Documentation
- [x] README.md
- [x] SPECTRA-GRADE-COMPLIANCE.md
- [x] TEMPLATE-USAGE.md
- [ ] 7-STAGE-PIPELINE-GUIDE.md
- [ ] ARCHITECTURE.md

### 4.2 Testing
- [ ] Test setup script
- [ ] Verify placeholder replacement
- [ ] Test in new Fabric workspace
- [ ] Validate Git sync works

### 4.3 Standards
- [x] .gitignore configured
- [x] No secrets in tracked files
- [ ] All notebooks have `.platform` files
- [ ] All notebooks use correct prologue
- [ ] British English throughout

## Phase 5: GitHub Template Repository

### 5.1 Repository Configuration
- [x] Create `.github/template-repository.yml`
- [ ] Add template topics
- [ ] Configure template description

### 5.2 Initial Commit
- [ ] Stage all template files
- [ ] Create initial commit
- [ ] Push to GitHub
- [ ] Mark as template repository

## Current Status

**Phase 1**: ✅ Complete (copy done, git initialized)
**Phase 2**: ⏳ In Progress (need to strip zephyr code)
**Phase 3**: ⏳ Pending
**Phase 4**: ⏳ In Progress (documentation started)
**Phase 5**: ⏳ Pending

## Next Steps

1. Test template in new workspace (verify zephyr copy works)
2. Strip zephyr-specific code systematically
3. Create intelligence template
4. Update all placeholders
5. Test setup script
6. Push to GitHub as template repository

