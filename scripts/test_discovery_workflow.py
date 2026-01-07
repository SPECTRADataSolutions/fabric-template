"""
Test script for discovery workflow.

Simulates the full self-updating intelligence workflow:
1. Run discovery (would be in Fabric)
2. Generate Python code
3. Merge and append to SDK
4. Auto-commit (optional)

Usage:
    # Test full workflow (without auto-commit)
    python scripts/test_discovery_workflow.py
    
    # Test with auto-commit
    python scripts/test_discovery_workflow.py --auto-commit
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    print("=" * 80)
    print("🧪 Testing Discovery Workflow")
    print("=" * 80)
    print()
    print("This script tests the discovery workflow end-to-end.")
    print()
    print("📋 Steps:")
    print("  1. Run prepareZephyr in Fabric with discover=True")
    print("  2. Check Files/intelligence/ for discovered Python code")
    print("  3. Run append_discovered_intelligence.py with timestamp")
    print("  4. Review changes in spectraSDK.Notebook")
    print()
    
    # Check if discovery artifacts exist
    intelligence_dir = Path("Files/intelligence")
    if not intelligence_dir.exists():
        print("⚠️  Files/intelligence/ not found")
        print("   Run prepareZephyr with discover=True in Fabric first")
        return
    
    # Find latest discovery artifact
    discovered_files = list(intelligence_dir.glob("discovered-intelligence-*.py"))
    if not discovered_files:
        print("⚠️  No discovered intelligence files found")
        print("   Run prepareZephyr with discover=True in Fabric first")
        print(f"   Expected: Files/intelligence/discovered-intelligence-YYYYMMDD-HHMMSS.py")
        return
    
    # Get latest file
    latest_file = max(discovered_files, key=lambda p: p.stat().st_mtime)
    timestamp = latest_file.stem.replace("discovered-intelligence-", "")
    
    print(f"✅ Found discovered intelligence: {latest_file.name}")
    print(f"   Timestamp: {timestamp}")
    print()
    
    # Ask if user wants to proceed
    auto_commit = "--auto-commit" in sys.argv or "-a" in sys.argv
    
    if auto_commit:
        print("🚀 Running with --auto-commit (fully automated)")
    else:
        print("📝 Running without --auto-commit (manual commit)")
    
    print()
    response = input("Proceed with merge and append? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled")
        return
    
    # Run append script
    print()
    print("=" * 80)
    print("Running append_discovered_intelligence.py...")
    print("=" * 80)
    print()
    
    cmd = ["python", "scripts/append_discovered_intelligence.py", timestamp]
    if auto_commit:
        cmd.append("--auto-commit")
    
    try:
        result = subprocess.run(cmd, check=True)
        print()
        print("=" * 80)
        print("✅ Test Complete!")
        print("=" * 80)
        
        if auto_commit:
            print("Intelligence has been:")
            print("  ✅ Merged with existing")
            print("  ✅ Appended to spectraSDK.Notebook")
            print("  ✅ Committed to Git")
            print("  ✅ Pushed to remote")
            print()
            print("Fabric will auto-sync the updated SDK on next run")
        else:
            print("Intelligence has been:")
            print("  ✅ Merged with existing")
            print("  ✅ Appended to spectraSDK.Notebook")
            print()
            print("Next steps:")
            print("  1. Review: spectraSDK.Notebook/notebook_content.py")
            print("  2. Commit: git add spectraSDK.Notebook/")
            print("  3. Push: git push")
        
    except subprocess.CalledProcessError as e:
        print()
        print("❌ Error running append script")
        print(f"   Exit code: {e.returncode}")
        return 1

if __name__ == "__main__":
    sys.exit(main() or 0)





