# Making Comprehensive Test Data Builder Reusable - Implementation Plan

**Date:** 2025-12-08  
**Objective:** Make comprehensive test data builder reusable across all source systems (Zephyr, Jira, Xero, etc.)

---

## 🔍 Current State: NOT Reusable

### Issues:
- ❌ **Hardcoded to Zephyr** - Specific endpoints, entity types
- ❌ **Standalone scripts** - Not in SDK, can't be used from notebooks
- ❌ **Hardcoded authentication** - Zephyr Bearer token
- ❌ **Zephyr-specific templates** - Entity types tied to Zephyr

### What IS Generic:
- ✅ Field structure analysis (scalar, record, array)
- ✅ Response comparison logic
- ✅ Schema generation patterns

---

## 🎯 SPECTRA-Grade Reusable Design

### Architecture:

**1. Generic SDK Helper Class:**
```python
class SchemaDiscoveryHelpers:
    """Generic schema discovery helpers - works for ANY REST API."""
    
    @staticmethod
    def create_entity_comprehensively(
        base_url: str,
        endpoint: str,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        logger: 'SPECTRALogger',
        timeout: int = 30
    ) -> tuple[Optional[Dict], Optional[int]]:
        """Generic entity creation - works for any REST API endpoint."""
        
    @staticmethod
    def analyze_field_structure(field_name: str, field_value: Any, path: List[str] = None) -> Dict[str, Any]:
        """Generic field analysis - already works for any JSON."""
        
    @staticmethod
    def discover_schema_from_responses(responses: List[Dict], entity_type: str) -> List[Dict[str, Any]]:
        """Discover schema from API responses - generic."""
        
    @staticmethod
    def test_validation_rules(
        base_url: str,
        endpoint: str,
        valid_payload: Dict,
        invalid_variations: List[Dict],
        headers: Dict[str, str],
        logger: 'SPECTRALogger'
    ) -> Dict[str, Any]:
        """Test validation rules by trying invalid data - generic."""
```

**2. Template-Driven Builder:**
```python
class ComprehensiveTestDataBuilder:
    """Template-driven test data builder - configurable per source."""
    
    def __init__(self, template_path: Path, session: NotebookSession):
        """Load template and configure for source system."""
        self.template = self._load_template(template_path)
        self.session = session
        self.base_url = session.ctx["full_url"]
        self.headers = self._build_headers()
    
    def build_all_entities(self) -> Dict[str, List]:
        """Build all entities from template - generic process."""
        # Generic: Load template → Create entities → Capture responses
```

**3. Source-Specific Templates:**
```yaml
# zephyr_comprehensive_test_data.yaml
source_system: "zephyr"
base_url: "${BASE_URL}"
base_path: "${BASE_PATH}"

auth:
  type: "bearer"
  header: "Authorization"
  prefix: "Bearer"
  token_var: "API_TOKEN"

entities:
  - name: "release"
    endpoint: "/release"
    method: "POST"
    payload_template: {...}
    variations: [...]
```

---

## ✅ Implementation Plan

### Phase 1: Move Generic Logic to SDK

**Add to `spectraSDK.Notebook`:**

1. **`SchemaDiscoveryHelpers` class:**
   - Generic field structure analysis
   - Generic entity creation (POST/PUT)
   - Generic response comparison
   - Generic validation testing

2. **`ComprehensiveTestDataBuilder` class:**
   - Template loader
   - Generic entity creation process
   - Response capture
   - Error handling

### Phase 2: Make Builder Template-Driven

1. **Refactor builder script:**
   - Accept template path as parameter
   - Load source-specific config
   - Use generic SDK helpers
   - Work for any source system

2. **Template structure:**
   - Source system config
   - Entity definitions
   - Relationship mappings
   - Enum variations

### Phase 3: SDK Integration

1. **Add to Prepare Stage:**
   - `PrepareStageHelpers.build_comprehensive_test_data()`
   - Uses SDK helpers
   - Template-driven

2. **Notebook Usage:**
   ```python
   # In prepareZephyr.Notebook
   builder = ComprehensiveTestDataBuilder(
       template_path="scripts/data/zephyr_comprehensive_test_data.yaml",
       session=session
   )
   entities = builder.build_all_entities()
   ```

---

## 🎯 Benefits

1. **Reusable:**
   - Same SDK helpers work for Jira, Xero, UniFi
   - Just change template file

2. **SDK-Based:**
   - Usable from notebooks
   - Available in Fabric runtime
   - Follows SPECTRA patterns

3. **Template-Driven:**
   - Source-specific in templates
   - Version-controlled
   - Easy to create new sources

4. **Modular:**
   - Generic logic in SDK
   - Source-specific in templates
   - Clear separation

---

**Recommendation:** Move to SDK + template-driven approach for SPECTRA-grade reusability.

**Should I implement this now?**

