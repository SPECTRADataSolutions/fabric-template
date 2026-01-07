"""Reset SDK to original and re-append fixed intelligence."""

from pathlib import Path

sdk_file = Path(__file__).parent.parent / "spectraSDK.Notebook" / "notebook_content.py"
intel_file = Path(__file__).parent.parent / "intelligence" / "intelligence.py"

# Reset SDK to original 6312 lines
with open(sdk_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(sdk_file, 'w', encoding='utf-8') as f:
    f.writelines(lines[:6312])

print("✅ Reset SDK to 6312 lines")

# Re-append fixed intelligence
with open(intel_file, 'r', encoding='utf-8') as f:
    intel_code = f.read()

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

print(f"✅ Re-appended fixed intelligence ({len(intel_code)} chars)")
print("📊 null → None replacement complete!")






