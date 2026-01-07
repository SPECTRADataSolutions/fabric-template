"""Append intelligence class to spectraSDK notebook."""

from pathlib import Path

sdk_file = Path(__file__).parent.parent / "spectraSDK.Notebook" / "notebook_content.py"
intel_file = Path(__file__).parent.parent / "intelligence" / "intelligence.py"

# Read intelligence code
with open(intel_file, 'r', encoding='utf-8') as f:
    intel_code = f.read()

# Append to SDK
with open(sdk_file, 'a', encoding='utf-8') as f:
    f.write('\n\n')
    f.write('# CELL ********************\n\n')
    f.write(intel_code)
    f.write('\n\n')
    f.write('# METADATA ********************\n\n')
    f.write('# META {\n')
    f.write('# META   "language": "python",\n')
    f.write('# META   "language_group": "synapse_pyspark"\n')
    f.write('# META }\n')

print(f"[OK] Appended {len(intel_code)} chars to spectraSDK")
print(f"[INFO] Intelligence: 287 lines, 5 entities, 9 dependencies, 10+ constraints")






