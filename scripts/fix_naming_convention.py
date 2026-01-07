"""
Convert snake_case to camelCase in enrichment document.
Field names visible in Fabric must be camelCase per SPECTRA standards.
"""
import re

def snake_to_camel(snake_str):
    """Convert snake_case to camelCase."""
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])

def fix_enrichment_doc():
    """Fix naming convention in enrichment document."""
    file_path = "docs/refine/DIMENSIONAL-MODEL-ENRICHMENT.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: `field_name` -> `fieldName`
    # Match backticked field names with underscores
    pattern = r'`([a-z]+(?:_[a-z0-9]+)+)`'
    
    def replace_func(match):
        field_name = match.group(1)
        camel_name = snake_to_camel(field_name)
        return f'`{camel_name}`'
    
    # Replace in field definitions (but not in DAX formulas which may reference existing columns)
    # Only replace in enrichment fields sections
    lines = content.split('\n')
    result_lines = []
    
    for line in lines:
        # Skip DAX formula lines (they reference existing columns which may be snake_case)
        if '= `' in line and ('DIVIDE' in line or 'COUNTROWS' in line or 'AVERAGE' in line or 'SUM' in line or 'CALCULATE' in line):
            result_lines.append(line)
            continue
        
        # Replace field names in backticks
        if '`' in line and '_' in line:
            # Match field names in backticks
            line = re.sub(r'`([a-z]+(?:_[a-z0-9]+)+)`', replace_func, line)
        
        result_lines.append(line)
    
    fixed_content = '\n'.join(result_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"✅ Fixed naming convention in {file_path}")

if __name__ == "__main__":
    fix_enrichment_doc()

