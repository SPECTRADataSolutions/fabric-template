"""
Phase 6: Uncover - Document all quirks, bugs, and workarounds

This script consolidates all known quirks from the bug registry and
discoveries into a structured intelligence document.

Output: intelligence/quirks.yaml
"""

import yaml
from pathlib import Path
from typing import List, Dict

def consolidate_quirks() -> Dict:
    """Consolidate all known quirks, bugs, and workarounds."""
    
    quirks = {
        "blockers": [
            {
                "id": "BLOCKER-001",
                "title": "Requirement Creation API Broken",
                "severity": "critical",
                "entity": "requirement",
                "endpoint": "POST /requirement",
                "issue": "Returns HTTP 500: 'Cannot invoke java.lang.Long.longValue() because id is null'",
                "impact": "Cannot create requirements via documented API",
                "workaround": {
                    "method": "Use POST /requirementtree/add with parentId",
                    "status": "✅ Working",
                    "notes": "Must create requirement_folder first, then use parentId"
                },
                "reported_to_vendor": False,
                "date_discovered": "2025-12-08"
            },
            {
                "id": "BLOCKER-002",
                "title": "Testcase Folder API Broken",
                "severity": "critical",
                "entity": "testcase_folder",
                "endpoint": "POST /testcasetree",
                "issue": "Returns HTTP 400: 'For input string: null'",
                "impact": "Cannot create testcase folders, blocks all testcase/execution/allocation creation",
                "workaround": {
                    "method": "Manual creation in UI required",
                    "status": "⚠️ Manual only",
                    "notes": "Tried 4 variations (omit parentId, parentId: null, parentId: 0, no parentId field) - all failed"
                },
                "reported_to_vendor": False,
                "date_discovered": "2025-12-08",
                "blocks": ["testcase", "execution", "allocation"]
            },
            {
                "id": "BLOCKER-003",
                "title": "Release Lock Duration >60 Seconds",
                "severity": "high",
                "entity": "release",
                "endpoint": "POST /release",
                "issue": "Newly created releases are locked for >60 seconds, preventing cycle creation",
                "impact": "Cannot create cycles immediately after release creation",
                "workaround": {
                    "method": "Use existing (old) releases for cycle creation",
                    "status": "✅ Working",
                    "notes": "Tested 15s, 30s, 60s delays - all failed. Old releases work immediately."
                },
                "reported_to_vendor": False,
                "date_discovered": "2025-12-08"
            }
        ],
        "bugs": [
            {
                "id": "BUG-007",
                "title": "Release GET by ID Returns HTTP 403",
                "severity": "medium",
                "entity": "release",
                "endpoint": "GET /release/{id}",
                "issue": "Returns HTTP 403 Forbidden even with valid API token",
                "impact": "Cannot validate release creation via GET",
                "workaround": {
                    "method": "Skip GET validation for releases",
                    "status": "✅ Working",
                    "notes": "Assume creation succeeded if POST returns 200/201"
                },
                "reported_to_vendor": False,
                "date_discovered": "2025-12-08"
            }
        ],
        "quirks": [
            {
                "id": "QUIRK-001",
                "title": "Requirement Names Must Be Unique Across All Runs",
                "severity": "low",
                "entity": "requirement",
                "issue": "API rejects duplicate requirement names even across different test runs",
                "impact": "Must use timestamps or UUIDs in requirement names",
                "workaround": {
                    "method": "Include timestamp in requirement name",
                    "status": "✅ Working",
                    "notes": "Use datetime.now().strftime('%Y%m%d%H%M%S') in name"
                },
                "date_discovered": "2025-12-08"
            },
            {
                "id": "QUIRK-002",
                "title": "Cycle Creation Requires Unlocked Release",
                "severity": "medium",
                "entity": "cycle",
                "issue": "Cannot create cycle with newly created release (locked)",
                "impact": "Must use existing releases or wait >60s",
                "workaround": {
                    "method": "Query for existing releases and use oldest one",
                    "status": "✅ Working",
                    "notes": "Oldest releases are most likely unlocked"
                },
                "date_discovered": "2025-12-08"
            },
            {
                "id": "QUIRK-003",
                "title": "Testcase Requires tcrCatalogTreeId (Folder ID)",
                "severity": "medium",
                "entity": "testcase",
                "issue": "Cannot create testcase without tcrCatalogTreeId",
                "impact": "Blocked by BLOCKER-002 (folder creation broken)",
                "workaround": {
                    "method": "None - depends on folder API fix",
                    "status": "❌ Blocked",
                    "notes": "Must fix folder API first"
                },
                "date_discovered": "2025-12-08"
            }
        ],
        "api_inconsistencies": [
            {
                "id": "INCONSISTENCY-001",
                "title": "Requirement Creation Uses Folder Endpoint",
                "entity": "requirement",
                "issue": "POST /requirement is broken, must use POST /requirementtree/add",
                "notes": "Folder and requirement creation use same endpoint, differentiated by parentId presence"
            },
            {
                "id": "INCONSISTENCY-002",
                "title": "Date Format Inconsistency",
                "entity": "multiple",
                "issue": "Some endpoints accept 'YYYY-MM-DD', others require epoch milliseconds",
                "examples": {
                    "release": "Accepts 'YYYY-MM-DD' string",
                    "cycle": "Requires epoch milliseconds (int)"
                },
                "notes": "No consistent date format across API"
            }
        ],
        "undocumented_behavior": [
            {
                "id": "UNDOCUMENTED-001",
                "title": "Release Lock Mechanism",
                "entity": "release",
                "behavior": "Releases are locked after creation for >60 seconds",
                "notes": "Not mentioned in API documentation"
            },
            {
                "id": "UNDOCUMENTED-002",
                "title": "Folder API parentId Rejection",
                "entity": "testcase_folder",
                "behavior": "API rejects parentId: null despite documentation suggesting it's valid for root folders",
                "notes": "Documentation doesn't clarify how to create root folders"
            }
        ]
    }
    
    return quirks

def generate_summary(quirks: Dict) -> Dict:
    """Generate summary statistics."""
    
    return {
        "total_blockers": len(quirks['blockers']),
        "total_bugs": len(quirks['bugs']),
        "total_quirks": len(quirks['quirks']),
        "total_inconsistencies": len(quirks['api_inconsistencies']),
        "total_undocumented": len(quirks['undocumented_behavior']),
        "critical_issues": len([b for b in quirks['blockers'] if b['severity'] == 'critical']),
        "working_workarounds": len([b for b in quirks['blockers'] if b['workaround']['status'] == '✅ Working']),
        "blocked_entities": ["testcase", "execution", "allocation"],
        "working_entities": ["project", "release", "requirement_folder", "requirement", "cycle"]
    }

def main():
    """Generate quirks.yaml from consolidated knowledge."""
    
    print("🕵️ Phase 6: Uncover - Documenting all quirks, bugs, and workarounds...")
    print()
    
    # Consolidate quirks
    quirks = consolidate_quirks()
    summary = generate_summary(quirks)
    
    # Build output
    output_data = {
        "metadata": {
            "generated_at": "2025-12-09",
            "source": "Phase 6: Uncover",
            "method": "Consolidated from bug registry and discoveries",
            "summary": summary
        },
        "quirks": quirks
    }
    
    # Save quirks.yaml
    output_dir = Path(__file__).parent.parent / "intelligence"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "quirks.yaml"
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"✅ Quirks documented!")
    print()
    print(f"📊 Summary:")
    print(f"  • Critical blockers: {summary['critical_issues']}")
    print(f"  • Total bugs: {summary['total_bugs']}")
    print(f"  • Total quirks: {summary['total_quirks']}")
    print(f"  • API inconsistencies: {summary['total_inconsistencies']}")
    print(f"  • Undocumented behaviors: {summary['total_undocumented']}")
    print()
    print(f"  • Working workarounds: {summary['working_workarounds']}/{summary['total_blockers']}")
    print(f"  • Blocked entities: {', '.join(summary['blocked_entities'])}")
    print()
    print(f"💾 Saved: {output_file}")
    print()
    print("✅ Phase 6 complete! Ready for Phase 7: Validate")

if __name__ == "__main__":
    main()







