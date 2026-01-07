# Zephyr API Intelligence - Implementation Plan V2 (Tool-Driven)

> **Date:** 2025-12-09  
> **Goal:** First implementation of API Intelligence Framework  
> **Doctrine:** `Core/doctrine/API-INTELLIGENCE-FRAMEWORK.md`  
> **Approach:** Automated, tool-driven, SPECTRA-grade

---

## 🎯 Objective

**Build complete, intimate, programmatic knowledge of Zephyr API using automated tools.**

This is the **first implementation** of the API Intelligence Framework doctrine, leveraging best-in-class Python libraries.

---

## 🛠️ Power Tools Stack

| Tool | Purpose | Stage |
|------|---------|-------|
| `httpx` | Modern async HTTP client | All stages |
| `genson` | Auto-generate JSON schemas from responses | Probe |
| `networkx` | Build dependency graphs, topological sort | Relate, Sequence |
| `schemathesis` | Property-based testing, auto test data | Validate |
| `apispec` | Export to OpenAPI 3.0 spec | Bonus |

**All tools installed via:**
```bash
pip install httpx genson networkx schemathesis apispec pyyaml
```

---

## 📋 Implementation Plan (Refactored)

### **Phase 1: Survey (30 min)** 👀

**Goal:** Identify all Zephyr entities from existing knowledge

**Approach:** 
- Leverage existing documentation and discoveries
- Use `docs/bug-and-blocker-registry.md` for known entities
- Review `endpoints.json` for entity hints

**Script to build:**
```python
# scripts/survey_entities.py
# Input: endpoints.json, bug registry, documentation
# Output: intelligence/entities.yaml
# Time: 30 minutes (mostly automated)
```

**Output:**
- `intelligence/entities.yaml` - Complete entity list with metadata

**Automation Level:** 🤖 80% (uses existing knowledge)

---

### **Phase 2: Catalog (30 min)** 📚

**Goal:** Document all Zephyr endpoints using SDK catalog

**Approach:**
- Use existing `endpoints.json` as source
- Enrich with authentication requirements
- Document HTTP methods per endpoint
- Add pagination/rate limit metadata

**Script to build:**
```python
# scripts/catalog_endpoints.py
# Input: endpoints.json (already exists!)
# Output: intelligence/endpoints.yaml
# Time: 30 minutes (transform existing data)
```

**Output:**
- `intelligence/endpoints.yaml` - Complete endpoint catalog

**Automation Level:** 🤖 90% (existing data + enrichment)

---

### **Phase 3: Probe (1.5 hours)** 🔬

**Goal:** Auto-generate schemas using `genson`

**Approach:**
1. Create ONE sample of each entity via API
2. Capture raw JSON response
3. **Use `genson` to auto-generate JSON schema**
4. Validate schema with second sample
5. Document required fields, types, enums

**Script to build:**
```python
# scripts/probe_schemas.py
import httpx
from genson import SchemaBuilder

async def probe_entity(entity_name: str, create_payload: dict):
    """Create entity, capture response, generate schema with genson."""
    
    # Create entity
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/{entity_name}", json=create_payload)
        data = response.json()
    
    # Auto-generate schema with genson
    builder = SchemaBuilder()
    builder.add_object(data)
    schema = builder.to_schema()
    
    # Save schema
    with open(f"intelligence/schemas/{entity_name}.json", "w") as f:
        json.dump(schema, f, indent=2)
    
    return schema

# Run for all entities
# Time: 1.5 hours (API calls + validation)
```

**Output:**
- `intelligence/schemas/release.json`
- `intelligence/schemas/cycle.json`
- `intelligence/schemas/testcase.json`
- `intelligence/schemas/requirement.json`
- `intelligence/schemas/execution.json`
- ... (all entities)

**Automation Level:** 🤖 95% (genson does the heavy lifting)

---

### **Phase 4: Relate (1 hour)** 🕸️

**Goal:** Build dependency graph using `networkx`

**Approach:**
1. Test entity creation in isolation (from existing experiments)
2. Document which entities require others
3. **Use `networkx` to build directed graph**
4. Identify strongly connected components
5. Document optional vs required dependencies

**Script to build:**
```python
# scripts/relate_dependencies.py
import networkx as nx

# Build dependency graph
G = nx.DiGraph()

# Add nodes (entities)
G.add_nodes_from(['project', 'release', 'cycle', 'folder', 'testcase', 'execution'])

# Add edges (dependencies)
# From existing experiments, we know:
G.add_edge('cycle', 'release')      # cycle depends on release
G.add_edge('testcase', 'folder')    # testcase depends on folder
G.add_edge('execution', 'testcase') # execution depends on testcase
G.add_edge('execution', 'cycle')    # execution depends on cycle
G.add_edge('requirement', 'release') # requirement depends on release

# Validate graph (detect cycles)
if not nx.is_directed_acyclic_graph(G):
    print("⚠️ Circular dependencies detected!")
    cycles = list(nx.simple_cycles(G))
    print(f"Cycles: {cycles}")

# Export to YAML
dependencies = {
    entity: list(G.predecessors(entity)) 
    for entity in G.nodes()
}

with open("intelligence/dependencies.yaml", "w") as f:
    yaml.dump(dependencies, f)

# Time: 1 hour (mostly leveraging existing discoveries)
```

**Output:**
- `intelligence/dependencies.yaml` - Complete dependency graph
- `intelligence/dependency-graph.png` - Visual representation

**Automation Level:** 🤖 90% (networkx automates graph analysis)

---

### **Phase 5: Sequence (30 min)** 🎯

**Goal:** Determine perfect creation order using `networkx` topological sort

**Approach:**
1. **Use `networkx.topological_sort()` on dependency graph**
2. Document lock/wait requirements (from existing discoveries)
3. Identify parallel vs sequential requirements
4. Validate order with test run

**Script to build:**
```python
# scripts/sequence_creation_order.py
import networkx as nx

# Load dependency graph from Phase 4
G = load_dependency_graph()

# Auto-generate perfect creation order
try:
    creation_order = list(nx.topological_sort(G))
    print(f"Perfect creation order: {creation_order}")
except nx.NetworkXError as e:
    print(f"Cannot determine order: {e}")

# Add timing constraints (from existing discoveries)
constraints = {
    'release': {'wait_after_create': 10, 'reason': 'BLOCKER-003: Release lock duration'},
    'folder': {'status': 'broken', 'reason': 'BLOCKER-002: Folder API rejects valid payloads'}
}

# Export to YAML
order_spec = {
    'order': creation_order,
    'constraints': constraints
}

with open("intelligence/creation-order.yaml", "w") as f:
    yaml.dump(order_spec, f)

# Time: 30 minutes (topological sort is instant, validation takes time)
```

**Output:**
- `intelligence/creation-order.yaml` - Perfect sequence with constraints

**Automation Level:** 🤖 95% (topological sort is automatic)

---

### **Phase 6: Uncover (1 hour)** 🕵️

**Goal:** Document all quirks, bugs, and workarounds

**Approach:**
1. Import existing bug registry
2. Add quirks discovered during probing
3. Document lock durations
4. Capture validation rules
5. Link to GitHub issues

**Script to build:**
```python
# scripts/uncover_quirks.py
# Input: docs/bug-and-blocker-registry.md
# Output: intelligence/quirks.yaml
# Time: 1 hour (consolidate existing knowledge)
```

**Output:**
- `intelligence/quirks.yaml` - Complete quirks catalog

**Quirks to document:**
- `BUG-007`: Release GET by ID returns HTTP 403
- `BLOCKER-002`: Folder API rejects valid payloads (parentId: null issue)
- `BLOCKER-003`: Release lock duration >60 seconds
- `QUIRK-001`: Requirement names must be unique across all test runs
- `QUIRK-002`: Cycle creation requires unlocked release (use old releases)

**Automation Level:** 🤖 60% (requires judgment on what's a quirk vs bug)

---

### **Phase 7: Validate (1 hour)** ✅

**Goal:** Prove intelligence is complete using `schemathesis`

**Approach:**
1. Export intelligence to OpenAPI spec (using `apispec`)
2. **Use `schemathesis` to auto-generate test cases**
3. Run property-based tests
4. Validate schemas match reality
5. Test creation order 3 times end-to-end

**Script to build:**
```python
# scripts/validate_intelligence.py
import schemathesis
from apispec import APISpec

# Step 1: Export to OpenAPI
spec = APISpec(
    title="Zephyr API",
    version="1.0.0",
    openapi_version="3.0.0"
)

# Add endpoints from intelligence/endpoints.yaml
# Add schemas from intelligence/schemas/*.json
# Export to intelligence/openapi.yaml

# Step 2: Run schemathesis property-based tests
schema = schemathesis.from_uri("intelligence/openapi.yaml")

@schema.parametrize()
def test_api(case):
    """Schemathesis auto-generates hundreds of test cases!"""
    response = case.call()
    case.validate_response(response)

# Step 3: Validate creation order
for run in range(3):
    validate_full_creation_sequence()

# Time: 1 hour (schemathesis does the heavy lifting)
```

**Output:**
- `intelligence/validation-report.md` - Proof of completeness
- `intelligence/openapi.yaml` - Industry standard export
- `intelligence/schemathesis-results.json` - Property-based test results

**Automation Level:** 🤖 85% (schemathesis automates test generation)

---

## 📁 Directory Structure

```
Data/zephyr/
├── intelligence/                    # NEW - API Intelligence
│   ├── README.md
│   ├── entities.yaml               # Phase 1: Survey
│   ├── endpoints.yaml              # Phase 2: Catalog
│   ├── schemas/                    # Phase 3: Probe
│   │   ├── release.json            #   (auto-generated by genson)
│   │   ├── cycle.json
│   │   ├── testcase.json
│   │   ├── requirement.json
│   │   ├── execution.json
│   │   └── folder.json
│   ├── dependencies.yaml           # Phase 4: Relate (networkx graph)
│   ├── dependency-graph.png        #   (visual representation)
│   ├── creation-order.yaml         # Phase 5: Sequence (topological sort)
│   ├── quirks.yaml                 # Phase 6: Uncover
│   ├── openapi.yaml                # Phase 7: Validate (apispec export)
│   ├── schemathesis-results.json   #   (property-based test results)
│   └── validation-report.md        #   (proof of completeness)
│
├── scripts/                         # Intelligence scripts
│   ├── survey_entities.py          # Phase 1 (30 min)
│   ├── catalog_endpoints.py        # Phase 2 (30 min)
│   ├── probe_schemas.py            # Phase 3 (1.5 hours) - uses genson
│   ├── relate_dependencies.py      # Phase 4 (1 hour) - uses networkx
│   ├── sequence_creation_order.py  # Phase 5 (30 min) - uses networkx
│   ├── uncover_quirks.py           # Phase 6 (1 hour)
│   └── validate_intelligence.py    # Phase 7 (1 hour) - uses schemathesis
│
└── docs/
    ├── api-intelligence-implementation-plan-v2.md  # This file
    └── bug-and-blocker-registry.md                 # Input for Phase 6
```

---

## ⏰ Timeline (Refactored)

**Total Time:** 6 hours (down from 7.5 hours!)

| Phase | Duration | Automation | Tool |
|-------|----------|------------|------|
| 1. Survey | 30 min | 80% | Existing knowledge |
| 2. Catalog | 30 min | 90% | endpoints.json |
| 3. Probe | 1.5 hours | 95% | **genson** |
| 4. Relate | 1 hour | 90% | **networkx** |
| 5. Sequence | 30 min | 95% | **networkx** |
| 6. Uncover | 1 hour | 60% | Bug registry |
| 7. Validate | 1 hour | 85% | **schemathesis** |

**Efficiency Gain:** 20% faster + 85%+ automated!

---

## ✅ Success Criteria

**API Intelligence is COMPLETE when:**

1. ✅ All entities documented in `entities.yaml`
2. ✅ All endpoints cataloged in `endpoints.yaml`
3. ✅ All schemas auto-generated in `schemas/*.json` (via **genson**)
4. ✅ Dependency graph validated in `dependencies.yaml` (via **networkx**)
5. ✅ Creation order works 100% in `creation-order.yaml` (via **networkx**)
6. ✅ Quirks documented in `quirks.yaml`
7. ✅ OpenAPI spec exported to `openapi.yaml` (via **apispec**)
8. ✅ Property-based tests pass in `schemathesis-results.json` (via **schemathesis**)
9. ✅ 3 validation runs successful in `validation-report.md`

---

## 🚀 Why This Approach is SPECTRA-Grade

### **1. Leverage Existing Tools**
- Don't reinvent JSON schema generation → use `genson`
- Don't reinvent graph algorithms → use `networkx`
- Don't write manual test cases → use `schemathesis`

### **2. Highly Automated**
- 85%+ automation across all phases
- Minimal manual work
- Repeatable for Jira, Xero, UniFi

### **3. Industry Standard Outputs**
- OpenAPI 3.0 spec (via `apispec`)
- JSON Schema (via `genson`)
- YAML configuration files
- Property-based test results (via `schemathesis`)

### **4. Future-Proof**
- Export to OpenAPI enables Swagger UI
- Professional bug reports to vendors
- Team can use Postman/Insomnia
- Enable AI code generation from spec

### **5. Compound Value**
- Intelligence is queryable
- Intelligence is shareable
- Intelligence is versionable
- Intelligence is reusable

---

## 🎯 Post-Implementation

**Once Zephyr intelligence is complete:**

1. ✅ Use `creation-order.yaml` to build perfect test data
2. ✅ Use `schemas/*.json` to validate Extract stage outputs
3. ✅ Use `openapi.yaml` to generate API clients
4. ✅ Use `schemathesis` to generate comprehensive test datasets
5. ✅ Share `openapi.yaml` with team (Swagger UI)
6. ✅ Apply framework to Jira (validate doctrine)
7. ✅ Apply framework to Xero (prove repeatability)

---

## 📦 Dependencies

**Install all tools:**
```bash
pip install httpx genson networkx schemathesis apispec pyyaml
```

**Versions:**
- `httpx` >= 0.27.0 (modern async HTTP)
- `genson` >= 1.2.2 (JSON schema generation)
- `networkx` >= 3.0 (graph algorithms)
- `schemathesis` >= 3.0 (property-based testing)
- `apispec` >= 6.0 (OpenAPI spec generation)
- `pyyaml` >= 6.0 (YAML parsing)

---

## 🔄 Changes from V1

| Aspect | V1 (Manual) | V2 (Tool-Driven) |
|--------|-------------|------------------|
| Schema Generation | Manual inspection | **genson** auto-generates |
| Dependency Graph | Manual testing | **networkx** graph analysis |
| Creation Order | Trial and error | **networkx** topological sort |
| Validation | Manual testing | **schemathesis** property-based |
| Export Format | Custom YAML | **OpenAPI 3.0** (industry standard) |
| Timeline | 7.5 hours | **6 hours** (20% faster) |
| Automation | ~50% | **85%+** |
| Repeatability | Medium | **High** |

---

**Status:** 🟢 Ready for Implementation  
**Start:** Now  
**Approach:** Automated, tool-driven, SPECTRA-grade  
**Doctrine:** `Core/doctrine/API-INTELLIGENCE-FRAMEWORK.md`







