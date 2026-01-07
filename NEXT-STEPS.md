# Next Steps for Template Completion

## Immediate Actions

### 1. Test Template in New Workspace ⚠️ CRITICAL
**Before stripping zephyr code, verify the copy works:**
- Create new Fabric workspace
- Connect to Git
- Sync notebooks
- Verify Source stage runs (with zephyr config)
- **This validates the base structure is sound**

### 2. Strip ZephyrIntelligence from SDK
- [ ] Find all `ZephyrIntelligence` class definitions in `spectraSDK.Notebook`
- [ ] Remove all 3 instances
- [ ] Remove `ZEPHYR_ENDPOINTS_CATALOG` constant
- [ ] Update documentation to reference `{PROJECT}Intelligence.Notebook`

### 3. Replace Hardcoded Values
- [ ] Run setup script to replace `{PROJECT}` placeholders (test first!)
- [ ] Or manually replace:
  - `"zephyr"` → `"{PROJECT}"`
  - `"zephyrVariables"` → `"{PROJECT}Variables"`
  - `"zephyrLakehouse"` → `"{PROJECT}Lakehouse"`
  - All other zephyr references

### 4. Remove Hardcoded Endpoints
- [ ] Update Prepare stage to read from `Tables/source/endpoints`
- [ ] Update Extract stage to be metadata-driven
- [ ] Remove `call_zephyr_api()` function
- [ ] Create generic API call pattern

### 5. Rename Files/Directories
- [ ] `sourceZephyr.Notebook` → `source{PROJECT}.Notebook`
- [ ] `prepareZephyr.Notebook` → `prepare{PROJECT}Config.Notebook`
- [ ] `extractZephyrSample.Notebook` → `extract{PROJECT}Sample.Notebook`
- [ ] All `zephyr*` files/directories

## Testing Checklist

After cleanup:
- [ ] Setup script works
- [ ] Placeholders replaced correctly
- [ ] Notebooks sync to Fabric
- [ ] No zephyr-specific code remains
- [ ] Intelligence template loads correctly
- [ ] SDK is generic (no source-specific code)

## GitHub Template Repository

Once cleanup is complete:
1. Commit all changes
2. Push to GitHub
3. Go to repository settings
4. Enable "Template repository" checkbox
5. Update repository description
6. Add topics/tags

## SPECTRA-Grade Validation

Before marking as complete:
- [ ] Run SPECTRA-grade compliance check
- [ ] Verify no secrets in tracked files
- [ ] Ensure all documentation complete
- [ ] Test in fresh workspace
- [ ] Validate setup script

