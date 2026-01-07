#!/usr/bin/env python3
"""
Monitor Zephyr Pipeline Run

Monitors a Fabric pipeline run and displays status updates until completion.
"""

import os
import sys
import time
from pathlib import Path

# Add Core/cli to path for imports
workspace_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(workspace_root / "Core" / "cli"))

from spectra.fabric import FabricClient, FabricAPIError, FabricAuthError


def get_run_status(fabric: FabricClient, workspace_id: str, pipeline_id: str, run_id: str) -> dict:
    """Get status of a pipeline run."""
    path = f"/workspaces/{workspace_id}/dataPipelines/{pipeline_id}/runs/{run_id}"
    response = fabric._request("GET", path)
    return response.json()


def monitor_pipeline(workspace_id: str, pipeline_id: str, run_id: str, interval: int = 10, max_wait: int = 600):
    """Monitor pipeline run until completion."""
    try:
        fabric = FabricClient.from_env()
    except FabricAuthError as e:
        print(f"❌ Authentication error: {e}", file=sys.stderr)
        return 1
    
    print(f"🔍 Monitoring pipeline run: {run_id}")
    print(f"   Workspace: {workspace_id}")
    print(f"   Pipeline: {pipeline_id}")
    print(f"   Check interval: {interval}s")
    print(f"   Max wait: {max_wait}s")
    print()
    
    elapsed = 0
    last_status = None
    
    while elapsed < max_wait:
        try:
            status_data = get_run_status(fabric, workspace_id, pipeline_id, run_id)
            status = status_data.get("status") or status_data.get("state") or "Unknown"
            
            # Only print if status changed
            if status != last_status:
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] Status: {status}")
                
                if "startTime" in status_data:
                    print(f"         Started: {status_data['startTime']}")
                if "endTime" in status_data:
                    print(f"         Ended: {status_data['endTime']}")
                if "duration" in status_data:
                    print(f"         Duration: {status_data['duration']}")
                
                last_status = status
                print()
            
            # Check if completed
            if status in ("Succeeded", "Failed", "Cancelled", "Completed"):
                print(f"✅ Pipeline {status.lower()}")
                
                # Show Fabric UI link
                fabric_url = f"https://app.fabric.microsoft.com/workspaces/{workspace_id}/dataPipelines/{pipeline_id}/runs/{run_id}"
                print(f"📊 View details: {fabric_url}")
                
                return 0 if status == "Succeeded" else 1
            
            time.sleep(interval)
            elapsed += interval
            
        except FabricAPIError as e:
            print(f"❌ API error: {e}", file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            print("\n⚠️  Monitoring interrupted by user")
            return 1
    
    print(f"⏱️  Timeout after {max_wait}s - pipeline may still be running")
    fabric_url = f"https://app.fabric.microsoft.com/workspaces/{workspace_id}/dataPipelines/{pipeline_id}/runs/{run_id}"
    print(f"📊 Check status: {fabric_url}")
    return 1


def run_pipeline_with_monitoring(workspace_id: str, pipeline_id: str, parameters: dict = None, interval: int = 10, max_wait: int = 600):
    """Run pipeline and monitor until completion."""
    try:
        fabric = FabricClient.from_env()
    except FabricAuthError as e:
        print(f"❌ Authentication error: {e}", file=sys.stderr)
        return 1
    
    print("🚀 Triggering pipeline run...")
    try:
        result = fabric.run_pipeline(
            workspace_id=workspace_id,
            pipeline_id=pipeline_id,
            parameters=parameters
        )
    except FabricAPIError as e:
        print(f"❌ Failed to trigger pipeline: {e}", file=sys.stderr)
        return 1
    
    run_id = result.get("id") or result.get("runId") or result.get("run_id")
    if not run_id:
        print("❌ Pipeline triggered but no run ID returned", file=sys.stderr)
        print(f"Response: {result}", file=sys.stderr)
        return 1
    
    initial_status = result.get("status") or result.get("state") or "submitted"
    print(f"✅ Pipeline triggered")
    print(f"   Run ID: {run_id}")
    print(f"   Initial status: {initial_status}")
    print()
    
    return monitor_pipeline(workspace_id, pipeline_id, run_id, interval, max_wait)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run and monitor Zephyr pipeline")
    parser.add_argument("--workspace-id", help="Fabric workspace ID", 
                       default=os.getenv("SPECTRA_DXC_ZEPHYR_FABRIC_WORKSPACE_ID", "16490dde-33b4-446e-8120-c12b0a68ed88"))
    parser.add_argument("--pipeline-id", help="Fabric pipeline ID",
                       default=os.getenv("SPECTRA_ZEPHYR_FABRIC_PIPELINE_ID", "be9d0663-d383-4fe6-a0aa-8ed4781e9e87"))
    parser.add_argument("--run-id", help="Existing run ID to monitor (skip triggering)")
    parser.add_argument("--init-mode", action="store_true", help="Set init_mode=true")
    parser.add_argument("--debug-mode", action="store_true", help="Set debug_mode=true")
    parser.add_argument("--full-run-mode", action="store_true", help="Set full_run_mode=true")
    parser.add_argument("--interval", type=int, default=10, help="Status check interval (seconds)")
    parser.add_argument("--max-wait", type=int, default=600, help="Maximum wait time (seconds)")
    
    args = parser.parse_args()
    
    parameters = {}
    if args.init_mode:
        parameters["init_mode"] = True
    if args.debug_mode:
        parameters["debug_mode"] = True
    if args.full_run_mode:
        parameters["full_run_mode"] = True
    
    if args.run_id:
        # Monitor existing run
        exit_code = monitor_pipeline(args.workspace_id, args.pipeline_id, args.run_id, args.interval, args.max_wait)
    else:
        # Run and monitor
        exit_code = run_pipeline_with_monitoring(
            args.workspace_id, 
            args.pipeline_id, 
            parameters if parameters else None,
            args.interval,
            args.max_wait
        )
    
    sys.exit(exit_code)




