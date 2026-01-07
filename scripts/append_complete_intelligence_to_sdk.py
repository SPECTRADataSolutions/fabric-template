"""
Append complete intelligence (ZephyrIntelligence class) to spectraSDK notebook.

This replaces the old ZephyrIntelligence class with the new complete version that
includes Jira-style schema fields (rawField, targetField, dimensionName, etc.).
"""

from pathlib import Path

def append_intelligence_to_sdk():
    """Append ZephyrIntelligence class to spectraSDK notebook."""
    
    intel_py = Path(__file__).parent.parent / "intelligence" / "complete_intelligence.py"
    sdk_notebook = Path(__file__).parent.parent / "spectraSDK.Notebook" / "notebook_content.py"
    
    if not intel_py.exists():
        print(f"❌ ERROR: {intel_py} not found!")
        print("   Run: python scripts/generate_complete_intelligence_python.py first")
        return False
    
    if not sdk_notebook.exists():
        print(f"❌ ERROR: {sdk_notebook} not found!")
        return False
    
    # Read intelligence code
    with open(intel_py, 'r', encoding='utf-8') as f:
        intelligence_code = f.read()
    
    # Read SDK notebook
    with open(sdk_notebook, 'r', encoding='utf-8') as f:
        sdk_content = f.read()
    
    # Check if ZephyrIntelligence already exists
    if "class ZephyrIntelligence:" in sdk_content:
        print("⚠️ ZephyrIntelligence class already exists in SDK")
        print("   Removing old version...")
        
        # Find and remove old ZephyrIntelligence class
        lines = sdk_content.split('\n')
        new_lines = []
        in_zephyr_intel = False
        skip_until_next_cell = False
        
        for line in lines:
            if "class ZephyrIntelligence:" in line:
                in_zephyr_intel = True
                skip_until_next_cell = True
                continue
            
            if skip_until_next_cell:
                # Skip until we hit a CELL marker or end of class
                if line.startswith("# CELL **CELL**"):
                    skip_until_next_cell = False
                    in_zephyr_intel = False
                    new_lines.append(line)
                continue
            
            new_lines.append(line)
        
        sdk_content = '\n'.join(new_lines)
    
    # Append intelligence code as a new cell
    new_cell = f"""

# CELL **CELL**

# MARKDOWN **MARKDOWN**
# == ZEPHYR API INTELLIGENCE (COMPLETE) ================================= SPECTRA
# 
# **Complete Intelligence**: Schemas with full Jira-style metadata:
# - `entity`: Target dimension name (singular)
# - `fieldId`: Raw API field name
# - `structureType`: scalar | array
# - `rawField`: Properties to extract from source
# - `targetField`: Flattened target column names
# - `dataType`: Target data types
# - `dimensionName`: Dimension table name (for arrays)
# - `bridgeName`: Bridge table name (for many-to-many)
# 
# **Source**: API Intelligence Framework + Manual Overrides
# **Maturity**: L6 (Jira-proven pattern)

# CODE **CODE**

{intelligence_code}
"""
    
    # Append to SDK
    sdk_content += new_cell
    
    # Write back
    with open(sdk_notebook, 'w', encoding='utf-8') as f:
        f.write(sdk_content)
    
    return True

if __name__ == "__main__":
    print("=" * 80)
    print("📝 Appending Complete Intelligence to spectraSDK")
    print("=" * 80)
    
    if append_intelligence_to_sdk():
        print("\n✅ Successfully appended ZephyrIntelligence to spectraSDK!")
        print("\n" + "=" * 80)
        print("🎯 Next Steps:")
        print("  1. Commit: git add spectraSDK.Notebook/")
        print("  2. Push: git push")
        print("  3. Fabric will sync the updated SDK")
        print("  4. Run prepareZephyr in Fabric to test")
        print("=" * 80)
    else:
        print("\n❌ Failed to append intelligence to SDK")
        exit(1)

