"""
Phase 1: Survey - Identify all Zephyr entities

This script generates intelligence/entities.yaml by consolidating:
- Existing hierarchy discoveries
- Bug/blocker registry knowledge  
- Endpoint analysis

Output: intelligence/entities.yaml
"""

import yaml
from pathlib import Path
from typing import List, Dict, Optional

def survey_entities() -> Dict:
    """Survey all known Zephyr entities from existing knowledge."""
    
    entities = [
        {
            "name": "project",
            "description": "Top-level Zephyr project container",
            "level": 0,
            "dependencies": [],
            "status": "✅ Working",
            "endpoints": {
                "get": "/project",
                "get_by_id": "/project/{id}",
                "create": None  # Projects created manually in UI
            },
            "lifecycle": ["active"],
            "notes": "Projects are created manually in Zephyr UI, not via API"
        },
        {
            "name": "release",
            "description": "Release entity within a project",
            "level": 0,
            "dependencies": [],
            "status": "✅ Working (with lock quirk)",
            "endpoints": {
                "get": "/release",
                "get_by_id": "/release/{id}",
                "create": "/release",
                "update": "/release/{id}",
                "delete": "/release/{id}"
            },
            "lifecycle": ["draft", "active", "completed"],
            "notes": "BLOCKER-003: Locks for >60s after creation. Workaround: Use existing releases.",
            "quirks": ["BLOCKER-003: Release lock duration >60s", "BUG-007: GET by ID returns HTTP 403"]
        },
        {
            "name": "requirement_folder",
            "description": "Folder for organizing requirements",
            "level": 0,
            "dependencies": [],
            "status": "✅ Working perfectly",
            "endpoints": {
                "create": "/requirementtree/add",
                "update": "/requirementtree/update",
                "delete": "/requirementtree/delete"
            },
            "lifecycle": ["active"],
            "notes": "Works flawlessly, no issues"
        },
        {
            "name": "requirement",
            "description": "Test requirement within a folder",
            "level": 1,
            "dependencies": ["requirement_folder"],
            "status": "✅ Working (with workaround)",
            "endpoints": {
                "create": "/requirementtree/add",  # Workaround!
                "create_broken": "/requirement",    # Original API (BROKEN)
                "update": "/requirement/{id}",
                "delete": "/requirement/{id}"
            },
            "lifecycle": ["draft", "active"],
            "notes": "BLOCKER-001: POST /requirement returns HTTP 500. Workaround: Use /requirementtree/add with parentId.",
            "quirks": ["BLOCKER-001: Direct requirement creation API broken", "Must use unique names across all runs"]
        },
        {
            "name": "cycle",
            "description": "Test cycle within a release",
            "level": 1,
            "dependencies": ["release"],
            "status": "✅ Working (with unlocked release)",
            "endpoints": {
                "get": "/cycle",
                "get_by_id": "/cycle/{id}",
                "create": "/cycle",
                "update": "/cycle/{id}",
                "delete": "/cycle/{id}"
            },
            "lifecycle": ["active", "completed"],
            "notes": "Requires unlocked release. Use existing releases to avoid lock issue.",
            "quirks": ["Fails with newly created releases due to BLOCKER-003"]
        },
        {
            "name": "testcase_folder",
            "description": "Folder for organizing test cases",
            "level": 1,
            "dependencies": ["project"],  # Assumed
            "status": "❌ Broken (BLOCKER-002)",
            "endpoints": {
                "create": "/testcasetree",
                "update": "/testcasetree",
                "delete": "/testcasetree"
            },
            "lifecycle": ["active"],
            "notes": "BLOCKER-002: POST /testcasetree returns HTTP 400 'For input string: null'. Tried 4 variations, all failed.",
            "quirks": ["BLOCKER-002: Folder API rejects valid payloads (parentId: null issue)"]
        },
        {
            "name": "testcase",
            "description": "Test case within a folder",
            "level": 2,
            "dependencies": ["testcase_folder"],
            "status": "⏸️ Blocked by testcase_folder",
            "endpoints": {
                "get": "/testcase",
                "get_by_id": "/testcase/{id}",
                "create": "/testcase",
                "update": "/testcase/{id}",
                "delete": "/testcase/{id}"
            },
            "lifecycle": ["draft", "active"],
            "notes": "Cannot test until testcase_folder API is fixed. Requires tcrCatalogTreeId (folder ID)."
        },
        {
            "name": "execution",
            "description": "Test execution linking testcase to cycle",
            "level": 3,
            "dependencies": ["testcase", "cycle"],
            "status": "⏸️ Blocked by testcase",
            "endpoints": {
                "get": "/execution",
                "get_by_id": "/execution/{id}",
                "create": "/execution",
                "update": "/execution/{id}",
                "delete": "/execution/{id}"
            },
            "lifecycle": ["not executed", "in progress", "passed", "failed", "blocked"],
            "notes": "Cannot test until testcase creation works."
        },
        {
            "name": "allocation",
            "description": "Testcase allocation to resources",
            "level": 2,
            "dependencies": ["testcase"],
            "status": "⏸️ Blocked by testcase",
            "endpoints": {
                "create": "/allocation",
                "update": "/allocation/{id}",
                "delete": "/allocation/{id}"
            },
            "lifecycle": ["active"],
            "notes": "Cannot test until testcase creation works."
        }
    ]
    
    return {
        "metadata": {
            "generated_at": "2025-12-09",
            "source": "Phase 1: Survey",
            "method": "Consolidated from existing discoveries",
            "total_entities": len(entities),
            "working_entities": len([e for e in entities if "✅" in e["status"]]),
            "broken_entities": len([e for e in entities if "❌" in e["status"]]),
            "blocked_entities": len([e for e in entities if "⏸️" in e["status"]])
        },
        "entities": entities,
        "dependency_hierarchy": {
            "level_0_independent": ["project", "release", "requirement_folder"],
            "level_1_single_dependency": ["requirement", "cycle", "testcase_folder"],
            "level_2_multiple_dependencies": ["testcase", "allocation"],
            "level_3_complex_dependencies": ["execution"]
        },
        "status_summary": {
            "working": ["project", "release", "requirement_folder", "requirement", "cycle"],
            "broken": ["testcase_folder"],
            "blocked": ["testcase", "execution", "allocation"]
        },
        "critical_blockers": [
            "BLOCKER-001: Requirement creation API broken (POST /requirement returns HTTP 500)",
            "BLOCKER-002: Testcase folder API broken (POST /testcasetree returns HTTP 400)",
            "BLOCKER-003: Release lock duration >60 seconds"
        ]
    }

def main():
    """Generate entities.yaml from survey."""
    
    print("🔍 Phase 1: Survey - Identifying all Zephyr entities...")
    print()
    
    # Survey entities
    data = survey_entities()
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "intelligence"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write entities.yaml
    output_file = output_dir / "entities.yaml"
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"✅ Survey complete!")
    print()
    print(f"📊 Results:")
    print(f"  • Total entities: {data['metadata']['total_entities']}")
    print(f"  • Working: {data['metadata']['working_entities']}")
    print(f"  • Broken: {data['metadata']['broken_entities']}")
    print(f"  • Blocked: {data['metadata']['blocked_entities']}")
    print()
    print(f"📁 Output: {output_file}")
    print()
    print("🎯 Dependency Hierarchy:")
    for level, entities in data['dependency_hierarchy'].items():
        print(f"  • {level}: {', '.join(entities)}")
    print()
    print("⚠️ Critical Blockers:")
    for blocker in data['critical_blockers']:
        print(f"  • {blocker}")
    print()
    print("✅ Phase 1 complete! Ready for Phase 2: Catalog")

if __name__ == "__main__":
    main()







