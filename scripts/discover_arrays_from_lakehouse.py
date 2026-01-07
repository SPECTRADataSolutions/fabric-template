"""
Discover array contents from already-extracted lakehouse data.

Reads source tables to find populated arrays - much simpler than API calls!
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import json
from pathlib import Path

# Initialize Spark
spark = SparkSession.builder.appName("ArrayDiscovery").getOrCreate()

def discover_from_lakehouse():
    """Discover array contents from lakehouse tables."""
    
    print("=" * 80)
    print("🔍 Discovering Array Contents from Lakehouse")
    print("📂 Reading from Tables/source/*")
    print("=" * 80)
    
    discoveries = {}
    
    # 1. Discover cycle.cyclePhases
    print("\n📊 1. cycle.cyclePhases")
    try:
        df_cycles = spark.read.format("delta").load("Tables/source/cycles")
        
        # Find cycles with non-null, non-empty cyclePhases
        cycles_with_phases = df_cycles.filter(
            F.col("cyclePhases").isNotNull() &
            (F.size(F.col("cyclePhases")) > 0)
        ).limit(5)
        
        if cycles_with_phases.count() > 0:
            sample = cycles_with_phases.select("id", "cyclePhases").first()
            phases = sample["cyclePhases"]
            print(f"  ✅ Found populated cyclePhases!")
            print(f"     Type: {type(phases)}")
            print(f"     Length: {len(phases) if phases else 0}")
            if phases and len(phases) > 0:
                print(f"     First element type: {type(phases[0])}")
                print(f"     Sample: {json.dumps(phases[0] if isinstance(phases[0], dict) else phases[0], indent=2)[:300]}")
                discoveries["cyclePhases"] = {
                    "element_type": "object" if isinstance(phases[0], dict) else type(phases[0]).__name__,
                    "sample": phases[0] if isinstance(phases[0], dict) else phases[0]
                }
        else:
            print("  ⚠️ No cycles with populated cyclePhases")
            discoveries["cyclePhases"] = None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        discoveries["cyclePhases"] = None
    
    # 2. Discover requirement.requirements (would need requirementTree table)
    print("\n📊 2. requirement.requirements")
    print("  ℹ️ Skipping - no source.requirements table extracted yet")
    discoveries["requirements"] = None
    
    # 3. Discover requirement.releaseIds
    print("\n📊 3. requirement.releaseIds")
    print("  ℹ️ Skipping - no source.requirements table extracted yet")
    discoveries["releaseIds"] = None
    
    # 4. Discover requirement.categories
    print("\n📊 4. requirement.categories")
    print("  ℹ️ Skipping - no source.requirements table extracted yet")
    discoveries["categories"] = None
    
    # Save discoveries
    output_file = Path("intelligence/array-samples-from-lakehouse.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(discoveries, f, indent=2, default=str)
    
    print("\n" + "=" * 80)
    print(f"✅ Discovery complete!")
    print(f"📁 Results saved to: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    discover_from_lakehouse()






