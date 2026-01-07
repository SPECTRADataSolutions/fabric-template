"""
SPECTRA-GRADE: Automated intelligence update from discovery mode.

One-command script that:
1. Loads discovered intelligence Python code
2. Merges with existing intelligence (preserves dependencies/constraints)
3. Appends to spectraSDK.Notebook
4. Ready for Git commit

Usage:
    python scripts/append_discovered_intelligence.py <timestamp>
    
Example:
    python scripts/append_discovered_intelligence.py 20251210-170244
"""

import sys
from pathlib import Path
import re

def load_discovered_intelligence(timestamp: str) -> str:
    """Load discovered intelligence Python code."""
    discovered_path = Path(f"Files/intelligence/discovered-intelligence-{timestamp}.py")
    
    if not discovered_path.exists():
        print(f"❌ ERROR: {discovered_path} not found!")
        print(f"   Run prepareZephyr with discover=True first")
        return None
    
    with open(discovered_path, 'r', encoding='utf-8') as f:
        return f.read()

def merge_with_existing(discovered_code: str, existing_code: str) -> str:
    """Merge discovered intelligence with existing (preserve dependencies/constraints)."""
    
    # Extract ENTITIES from discovered
    discovered_entities_match = re.search(r'ENTITIES = \{([^}]+)\}', discovered_code, re.DOTALL)
    if not discovered_entities_match:
        print("❌ ERROR: Could not extract ENTITIES from discovered code")
        return None
    
    discovered_entities = discovered_entities_match.group(0)
    
    # Extract DEPENDENCIES and CONSTRAINTS from existing
    existing_deps_match = re.search(r'DEPENDENCIES = (\{[^}]*\})', existing_code, re.DOTALL)
    existing_constraints_match = re.search(r'CONSTRAINTS = (\{[^}]*\})', existing_code, re.DOTALL)
    
    # Build merged code
    merged_lines = []
    merged_lines.append("# " + "=" * 78)
    merged_lines.append("# ZEPHYR API INTELLIGENCE (COMPLETE - MERGED)")
    merged_lines.append("# Auto-generated from discovered schema + existing intelligence")
    merged_lines.append("# Source: discover=True mode + manual overrides")
    merged_lines.append("# " + "=" * 78)
    merged_lines.append("")
    merged_lines.append("class ZephyrIntelligence:")
    merged_lines.append('    """Zephyr API intelligence - complete schema with dimensional modeling."""')
    merged_lines.append("")
    merged_lines.append("    # Complete entity schemas (discovered + enriched)")
    merged_lines.append(discovered_entities)
    merged_lines.append("")
    
    if existing_deps_match:
        merged_lines.append("    # Dependencies (from existing intelligence)")
        merged_lines.append(f"    DEPENDENCIES = {existing_deps_match.group(1)}")
    else:
        merged_lines.append("    DEPENDENCIES = {}")
    
    merged_lines.append("")
    
    if existing_constraints_match:
        merged_lines.append("    # Constraints (from existing intelligence)")
        merged_lines.append(f"    CONSTRAINTS = {existing_constraints_match.group(1)}")
    else:
        merged_lines.append("    CONSTRAINTS = {}")
    
    merged_lines.append("")
    
    # Add helper methods from discovered
    helper_methods = re.search(r'(@classmethod.*?)(?=\n\n|\Z)', discovered_code, re.DOTALL)
    if helper_methods:
        merged_lines.append(helper_methods.group(1))
    
    return "\n".join(merged_lines)

def append_to_sdk(intelligence_code: str):
    """Append merged intelligence to spectraSDK notebook."""
    sdk_notebook = Path("spectraSDK.Notebook/notebook_content.py")
    
    if not sdk_notebook.exists():
        print(f"❌ ERROR: {sdk_notebook} not found!")
        return False
    
    with open(sdk_notebook, 'r', encoding='utf-8') as f:
        sdk_content = f.read()
    
    # Remove old ZephyrIntelligence if exists
    if "class ZephyrIntelligence:" in sdk_content:
        print("⚠️  Removing old ZephyrIntelligence class...")
        lines = sdk_content.split('\n')
        new_lines = []
        skip_until_cell = False
        
        for line in lines:
            if "class ZephyrIntelligence:" in line:
                skip_until_cell = True
                continue
            
            if skip_until_cell and line.startswith("# CELL **CELL**"):
                skip_until_cell = False
                new_lines.append(line)
                continue
            
            if not skip_until_cell:
                new_lines.append(line)
        
        sdk_content = '\n'.join(new_lines)
    
    # Append new intelligence
    new_cell = f"""

# CELL **CELL**

# MARKDOWN **MARKDOWN**
# == ZEPHYR API INTELLIGENCE (COMPLETE - MERGED) =========================== SPECTRA
# 
# **Complete Intelligence**: Discovered schema + existing dependencies/constraints
# **Source**: discover=True mode (automated) + manual overrides
# **Maturity**: L6 (Jira-proven pattern)

# CODE **CODE**

{intelligence_code}
"""
    
    sdk_content += new_cell
    
    # Write back
    with open(sdk_notebook, 'w', encoding='utf-8') as f:
        f.write(sdk_content)
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ ERROR: Timestamp required")
        print("Usage: python scripts/append_discovered_intelligence.py <timestamp>")
        print("Example: python scripts/append_discovered_intelligence.py 20251210-170244")
        sys.exit(1)
    
    timestamp = sys.argv[1]
    
    print("=" * 80)
    print("SPECTRA-GRADE: Automated Intelligence Update")
    print("=" * 80)
    
    # Load discovered intelligence
    print(f"📥 Loading discovered intelligence (timestamp: {timestamp})...")
    discovered_code = load_discovered_intelligence(timestamp)
    if not discovered_code:
        sys.exit(1)
    
    # Load existing SDK intelligence (for merge)
    print("📥 Loading existing intelligence from SDK...")
    sdk_notebook = Path("spectraSDK.Notebook/notebook_content.py")
    if sdk_notebook.exists():
        with open(sdk_notebook, 'r', encoding='utf-8') as f:
            existing_code = f.read()
    else:
        existing_code = ""
    
    # Merge
    print("🔄 Merging discovered + existing intelligence...")
    merged_code = merge_with_existing(discovered_code, existing_code)
    if not merged_code:
        sys.exit(1)
    
    # Append to SDK
    print("📝 Appending merged intelligence to spectraSDK...")
    if append_to_sdk(merged_code):
        print("\n✅ SUCCESS: Intelligence updated in spectraSDK!")
        
        # SPECTRA-GRADE: Auto-commit option
        auto_commit = "--auto-commit" in sys.argv or "-a" in sys.argv
        
        if auto_commit:
            print("\n🚀 SPECTRA-GRADE: Auto-committing to Git...")
            import subprocess
            
            try:
                # Stage changes
                subprocess.run(["git", "add", "spectraSDK.Notebook/"], check=True)
                
                # Commit
                commit_msg = f"feat: Update intelligence from discovery mode (timestamp: {timestamp})"
                subprocess.run(["git", "commit", "-m", commit_msg], check=True)
                
                # Push
                subprocess.run(["git", "push"], check=True)
                
                print("✅ Auto-committed and pushed to Git!")
                print("   Fabric will sync the updated SDK automatically")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Auto-commit failed: {e}")
                print("   Manual commit required")
        else:
            print("\n" + "=" * 80)
            print("🎯 Next Steps:")
            print("  1. Review: spectraSDK.Notebook/notebook_content.py")
            print("  2. Commit: git add spectraSDK.Notebook/ && git commit -m 'feat: Update intelligence'")
            print("  3. Push: git push")
            print("  4. OR use auto-commit: python scripts/append_discovered_intelligence.py <timestamp> --auto-commit")
            print("=" * 80)
    else:
        print("\n❌ Failed to append intelligence to SDK")
        sys.exit(1)

